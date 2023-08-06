__all__ = ["CubeFitterLM", "ResultLM"]

import logging
import math
import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager

import numpy as np
import pandas as pd
from numpy.ma.core import MaskedArray
from tqdm import tqdm

from ..exceptions import InputDimError, InputShapeError
from ..utils import get_custom_attr
from .base import CubeFitter

logger = logging.getLogger(__name__)

# to inheritate from parent process (shared object), it looks like we should use fork, instead of spawn
ctx = mp.get_context('fork')

# CPU COUNT
CPU_COUNT = os.cpu_count()
logger.info(f"The number of cpus: {CPU_COUNT}")


#TODO: write new error class for fitting spaxel (reference: fc mpdaf_ext)
class CubeFitterLM(CubeFitter):
    """
    Parameters
    ----------
    data : numpy.ma.MaskedArray
        cube data; this array should be 3-d, and the ordering of its axes should be
    (wavelength,image_y,image_x) (reference: mpdaf.obj.Cube.data)
    weight : numpy.ma.MaskedArray
        cube data weight; this array should be 3-d, and has the same ordering of axes as data.
    x : numpy.array or list
        cube wavelength
    model : lmfit.CompositeModel
    nprocess : int, optional
        the number of worker processes used in parallel fitting, by default os.cpu_count()
    method : str, optional
        specifies the fitting method available in lmfit, by default 'leastsq'
    kwargs : optional
        other keyword arguments passed from lmfit.Model.fit

    Notes
    -----
    If the light version of lmfit (https://github.com/ADACS-Australia/light-lmfit-py/tree/light) is used, method "fast_leastsq" is available.
    """
    _indices = ['image_y', 'image_x']
    _lmfit_result_default = [
    'aic', 'bic', 'chisqr',
    'ndata', 'nfev',
    'nfree', 'nvarys', 'redchi',
    'success']

    def __init__(self, data, weight, x, model, nprocess=CPU_COUNT, method='leastsq', **kwargs):    
        """
        Cube fitter backed with lmfit.

        Parameters
        ----------
        data : numpy.ma.MaskedArray
            cube data; this array should be 3-d, and the ordering of its axes should be
        (wavelength,image_y,image_x) (reference: mpdaf.obj.Cube.data)
        weight : numpy.ma.MaskedArray
            cube data weight; this array should be 3-d, and has the same ordering of axes as data.
        x : numpy.array or list
            cube wavelength
        model : lmfit.Model or lmfit.CompositeModel
        nprocess : int, optional
            number of worker processes used in parallel fitting, by default "os.cpu_count()"
        method : str, optional
            fitting method available in lmfit, by default 'leastsq'
        kwargs : optional
            other keyword arguments passed from lmfit.Model.fit

        Notes
        -----
        If the light version of lmfit is used instead, method "fast_leastsq" is available.
        """
        self._data = data
        self._weight = weight
        self.x = x 
        self.model = model
        self.nprocess = nprocess
        self.fit_method = method
        self.opts = kwargs
        self.result = None
        self._input_data_check()
        self._prepare_data()
        self._create_result_container()

    def _input_data_check(self):
        """Check input data dimension and shape."""
        if self._data.ndim != 3:
            raise InputDimError(self._data.ndim)
        if self._weight is not None and self._weight.shape != self._data.shape:
            raise InputShapeError("Weight must be either None or of the same shape as data.")
        if len(self.x) != self._data.shape[0]:
            raise InputShapeError("The length of x must be equal to the length of the spectrum.")

    def _get_xy_indices(self):
        """Get the pixel index (image_y, image_x) for each spaxel."""
        y, x = self._data.shape[1], self._data.shape[2]

        indices = np.zeros((y*x, 2))
        for i in range(y):
            for j in range(x):
                indices[i*x+j] = [i,j]
        return indices

    def _convert_array(self, arr):
        """Reshape the array."""
        arr = np.transpose(arr, axes=(1,2,0)).copy(order="C")
        axis_y, axis_x = arr.shape[0], arr.shape[1]
        axis_d = arr.shape[2]
        pix = axis_y * axis_x
        arr = arr.reshape(pix, axis_d)
        return arr

    def _prepare_data(self):
        """Prepare data for parallel fitting."""
        self.data = self._convert_array(self._data)
        if self._weight is not None:
            self.weight = self._convert_array(self._weight)
        else:
            self.weight = self._weight

    def _get_param_names(self):
        """Get the param names of the model."""
        m = self.model()
        _pars = m.make_params()
        _pars_name = list(_pars.valuesdict().keys())
        self._pars_name = _pars_name

        return _pars_name

    def _set_result_columns(self):
        """Set param columns: [name, name_err] for each param."""
        _pars_name = self._get_param_names()
        _pars_col = []
        for p in _pars_name:
            _pars_col += [p, p+"_err"]
        self.result_columns = self._indices + self._lmfit_result_default + _pars_col
        
    def _create_result_container(self):
        """Create result array filled with nan value."""
        self._set_result_columns()
        n_cols = len(self.result_columns)
        result = np.zeros((self.data.shape[0], n_cols))
        result[:] = np.nan

        # get pixel indices
        indices = self._get_xy_indices()
        result[:,:2] = indices
        self.result = result

    def _read_fit_result(self, res):
        """
        Read fitting result from lmfit.

        Parameters
        ----------
        res : lmfit.ModelResult
            

        Returns
        -------
        list
            value of parameters specified in self._lmfit_result_default        
        """
        vals = []
        for name in self._lmfit_result_default:
            val = getattr(res, name)
            vals.append(val)

        pars = res.params
        for name in self._pars_name:
            val = pars[name]
            vals += [val.value, val.stderr]

        return vals
        
    def _fit_single_spaxel(self, data: np.ndarray, weight: np.ndarray or None, 
                            mask: np.ndarray, x: np.ndarray, 
                            resm: shared_memory.SharedMemory, pix_id: int):  
        """Target function for parallel cube fitting (fit_cube)."""      
        if not mask[pix_id].all():
            inx = np.where(~mask[pix_id])
            sp = data[pix_id][inx]
            sp_x = x[inx]
            sp_weight = None
            if weight is not None:
                sp_sweight = weight[pix_id][inx]            
            # start fitting    
            m = self.model()
            params = m.guess(sp, sp_x)
            res = m.fit(sp, params, x=sp_x, weights=sp_weight, method=self.fit_method, **self.opts)

            # read fitting result
            result = np.ndarray(self.result.shape, self.result.dtype, buffer=resm.buf)
            out = self._read_fit_result(res)
            result[pix_id, 2:] = out

            # display fitting process
            name = os.getpid()
            logger.info(f"subprocess: {name}; pixel: {pix_id}")
              
    def _set_default_chunksize(self, ncpu):
        return math.ceil(self.data.shape[0]/ncpu)

    def fit_cube(self, nprocess=None):
        """
        Fit cube parallelly.

        Parameters
        ----------
        nprocess : int, optional
            number of worker processes used in parallel fitting, by default None. If None, nprocess set at class instance will be used
        Returns
        -------
        result : numpy.ndarray
        """
        if nprocess is None:
            nprocess = self.nprocess
        
        # get value of chunksize (key in pool.map)
        chunksize = self._set_default_chunksize(nprocess)

        # initialize result
        self.result[:,2:] = np.nan
        

        with SharedMemoryManager() as smm:
            logger.debug("Put data into shared memory")
            shm_dd = smm.SharedMemory(size=self.data.nbytes)
            shm_dm = smm.SharedMemory(size=self.data.mask.nbytes)
            shm_x = smm.SharedMemory(size=self.x.nbytes)
            shm_r = smm.SharedMemory(size=self.result.nbytes)
            sdd = np.ndarray(self.data.data.shape, dtype=self.data.data.dtype, buffer=shm_dd.buf)
            sdd[:] = self.data.data[:]
            sdm = np.ndarray(self.data.mask.shape, dtype=self.data.mask.dtype, buffer=shm_dm.buf)
            sdm[:] = self.data.mask[:]
            sx = np.ndarray(self.x.shape, dtype=self.x.dtype, buffer=shm_x.buf)
            sx[:] = self.x[:]
            sr = np.ndarray(self.result.shape, dtype=self.result.dtype, buffer=shm_r.buf)
            sr[:] = self.result[:]
            
            sw = None
            if self.weight is not None:
                shm_wd = smm.SharedMemory(size=self.weight.nbytes)
                sw = np.ndarray(self.weight.shape, dtype=self.weight.dtype, buffer=shm_wd.buf)
                sw[:] = self.weight.data[:]

            pool = ctx.Pool(processes=nprocess)
            npix = self.result.shape[0]
           
            logger.info("Start pooling ...")
            pool.map(partial(self._fit_single_spaxel, sdd, sw, sdm, sx, shm_r), range(npix), chunksize=chunksize)
            logger.info("Finish pooling.")

        self.result[:] = sr[:]

        return self.result
            
    def fit_serial(self):
        """"Fit cube serially."""
        # initialize result 
        self.result[:, 2:] = np.nan

        # set progress bar
        npix = self.data.shape[0]

        logger.info("Fitting progress:")
        pbar = tqdm(total=npix)
    
        # fitting iteration
        for i in range(npix):
            pbar.update(1)
            sp = self.data[i,:]
            if self.weight is not None:
                sp_weight = self.weight[i,:]
            else:
                sp_weight = None
            
            if not sp.mask.all():
                m = self.model()
                params = m.guess(sp, self.x)
                res = m.fit(sp, params, x=self.x, weights=sp_weight, method=self.fit_method, **self.opts)
                out = self._read_fit_result(res)
                self.result[i,2:] = out

            # display fitting process
            logger.info(f"serial fitting -- pixel: {i}")
        
        return self.result

class ResultLM():
    """
    Result container. It can be used to collect key information (by reading attributes) from objects that generated during the fitting process.

    Parameters
    ----------
    path : str, optional
        directory to hosts "out", by default "./"
    """
    # _cube_attr = ["z", "line", "snr_threshold", "snrmap"]
    # _fit_attr = ["fit_method", "result", "result_column"]
    # _default = ["success", "aic", "bic", "chisqr", "redchi"]

    _save = ["data", "weight", "x"]

    def __init__(self, path="./"):
        """
        Result container. It can be used to collect key information (by reading attributes) from objects that generated during the fitting process.

        Parameters
        ----------
        path : str, optional
            directory to hosts "out", by default "./"
        """
        self.path = path
        self._create_output_dir()

    def _create_output_dir(self):
        """Create an 'out' folder in the directory specified by path keyword."""
        os.makedirs(self.path + "/out", exist_ok=True)
        logger.debug("Create out directory.")

    @property
    def _flatsnr(self):
        """Fill masked snr by -999."""
        return self.snr.filled(-999).flatten()

    def _create_result_df(self):
        df = pd.DataFrame(self.result, columns=self.result_columns)
        df['snr'] = self._flatsnr
        return df

    def _save_result(self, df):
        store = pd.HDFStore(self.path + "/out/result.h5")
        lname = self.line.name
        mname = self.model.__name__
        rname = lname+"_"+mname
        store.put(rname, df)
        store.close()

    # TODO: both ProcessedCube and CubeFitterLM have self._save attributes; 
    # need to find a way to separate them; or move reshape functionality 
    # from CubeFitterLM to ProcessedCube
    def _save_fit_input_data(self):
        data_dir = self.path + "/out/fitdata/"
        os.makedirs(data_dir, exist_ok=True)
        for name in self._save:
            val = getattr(self, name)
            data_name = data_dir + name
            if type(val) is MaskedArray:
                np.save(data_name + "_data", val.data)
                np.save(data_name + "_mask", val.mask)
            else:
                np.save(data_name, val)

    def _write_fit_summary(self):
        """Write out fit summary, which can also be used as config file."""
        pass

    def get_output(self, cls):
        """Get relevant attributes from other class object."""
        get_custom_attr(self, cls)

    def save(self, save_fitdata=True):
        df = self._create_result_df()
        self._save_result(df)
        if save_fitdata:
            self._save_fit_input_data()
            

        
    


    

        


        
        





    
        
    
        


    

    




