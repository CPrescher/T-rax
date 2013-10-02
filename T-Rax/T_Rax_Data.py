from wx.lib.pubsub import Publisher as pub
from SPE_module import SPE_File
import os.path
import numpy as np
import random
import scipy.interpolate as ip
from scipy.optimize import curve_fit


class TraxData(object):
    def __init__(self):
        self.ds_calib_data = None
        self.ds_calib_param = CalibParam()
        self.us_calib_data = None
        self.us_calib_param = CalibParam()

        self.roi_data_manager =  ROIDataManager()

        self._create_dummy_img()
        self._load_calib_etalon()
        pub.sendMessage("EXP DATA CHANGED", self)
        pub.sendMessage("ROI CHANGED", self)

    def _read_roi_param(self):
        if os.path.isfile('roi_data.txt'):
            roi_list = np.loadtxt('roi_data.txt',delimiter=',')
            self.roi_data = ROIData(map(int, roi_list[0]),map(int, roi_list[1]))
        else:
            self.roi_data = ROIData([100,1000,80,90],[100,1000,10,20])

    def _create_dummy_img(self):
        self.exp_data=DummyImg(self.roi_data_manager)
        self.roi_data =self.exp_data.roi_data

    def _load_calib_etalon(self):
        self.load_us_calib_etalon('15A_lamp.txt')
        self.load_ds_calib_etalon('15A_lamp.txt')

    def load_exp_data(self, filename):
        self.exp_data = self.read_exp_image_file(filename)
        self.roi_data =self.exp_data.roi_data
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_next_exp_file(self):
        new_file_name, new_file_name_with_leading_zeros = self.exp_data.get_next_file_names()
        if os.path.isfile(new_file_name):
            self.load_exp_data(new_file_name)
        elif os.path.isfile(new_file_name_with_leading_zeros):
            self.load_exp_data(new_file_name_with_leading_zeros)

    def load_previous_exp_file(self):
        new_file_name, new_file_name_with_leading_zeros = self.exp_data.get_previous_file_names()
        if os.path.isfile(new_file_name):
            self.load_exp_data(new_file_name)
        elif os.path.isfile(new_file_name_with_leading_zeros):
            self.load_exp_data(new_file_name_with_leading_zeros)
        pub.sendMessage("EXP DATA CHANGED", self)

    def read_exp_image_file(self, file_name):
        img_file= SPE_File(file_name)
        if img_file.type=='image':
            return ExpData(img_file, self.roi_data_manager)
        elif img_file.type=='spectrum':
            return ExpSpecData(img_file, self.roi_data_manager)


    def load_ds_calib_data(self, file_name):
        self.ds_calib_data = self.read_exp_image_file(file_name)
        self.calc_spectra()
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_ds_calib_modus(self, modus):
        self.ds_calib_param.set_modus(modus)
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_ds_calib_temp(self, val):
        self.ds_calib_param.set_temp(val)
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_ds_calib_etalon(self, fname):
        self.ds_calib_param.load_etalon_spec(fname)
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_ds_calib_polynom(self, polynom):
        self.ds_calib_param.set_polynom(polynom)
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_us_calib_data(self, file_name):
        self.us_calib_data = self.read_exp_image_file(file_name)
        self.calc_spectra()
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_us_calib_modus(self, modus):
        self.us_calib_param.set_modus(modus)
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_us_calib_temp(self, val):
        self.us_calib_param.set_temp(val)
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_us_calib_etalon(self, fname):
        self.us_calib_param.load_etalon_spec(fname)
        pub.sendMessage("EXP DATA CHANGED", self)

    def set_us_calib_polynom(self, polynom):
        self.us_calib_param.set_polynom(polynom)
        pub.sendMessage("EXP DATA CHANGED", self)

    def calculate_wavelength(self,channel):
        if isinstance(channel,list):
            result = []
            for c in channel:
                result.append(self.exp_data.x_whole[c])
            return np.array(result)
        else:
            return self.exp_data.x_whole[channel]

    def calculate_ind(self, wavelength):
        result = []
        xdata = np.array( self.exp_data.x_whole)
        try:
            for w in wavelength:
                try:
                    base_ind = max(max(np.where(xdata <= w)))
                    if base_ind < len(xdata)-1:
                        result.append(int(np.round((w - xdata[base_ind]) / \
                            (xdata[base_ind + 1] - xdata[base_ind]) \
                            + base_ind)))
                    else:
                        result.append(base_ind)
                except:
                    result.append(0)
            return np.array(result)
        except TypeError:
            base_ind = max(max(np.where(xdata <= wavelength)))
            return int(np.round((wavelength - xdata[base_ind]) / \
                    (xdata[base_ind + 1] - xdata[base_ind]) \
                    + base_ind))
    
    def calc_spectra(self):
        self.exp_data.calc_spectra()
        if self.ds_calib_data is not None:
            self.ds_calib_data.calc_spectra()
        if self.us_calib_data is not None:
            self.us_calib_data.calc_spectra()

    def get_exp_file_name(self):
        return self.exp_data.filename

    def get_ds_calib_file_name(self):
        try:
            return self.ds_calib_data.filename
        except AttributeError:
            return 'Select File...'

    def get_us_calib_file_name(self):
        try:
            return self.us_calib_data.filename
        except AttributeError:
            return 'Select File...'

    def get_ds_calib_etalon_file_name(self):
        return self.ds_calib_param.get_etalon_fname()

    def get_us_calib_etalon_file_name(self):
        return self.us_calib_param.get_etalon_fname()

    def get_exp_img_data(self):
        return self.exp_data.get_img_data()

    def get_exp_graph_data(self):
        return self.exp_data.get_ds_spectrum()
             
    def get_ds_spectrum(self):
        if not self.exp_data_ds_calibration_data_same_dimension():
            return self.exp_data.ds_spectrum
        else:
            x=self.exp_data.ds_spectrum.x
            corrected_spectrum = self.exp_data.calc_corrected_ds_spectrum(self.ds_calib_data.ds_spectrum, 
                                                self.ds_calib_param.get_calibrated_spec(x))
            self.ds_fitted_spectrum = FitSpectrum(corrected_spectrum)
            return [corrected_spectrum, self.ds_fitted_spectrum]

    def exp_data_ds_calibration_data_same_dimension(self):
        try:
            return self.exp_data.get_img_dimension()==self.ds_calib_data.get_img_dimension()
        except:
            return False

    def exp_data_us_calibration_data_same_dimension(self):
        try:
            return self.exp_data.get_img_dimension()==self.us_calib_data.get_img_dimension()
        except:
            return False

    def get_ds_roi_max(self):
        return self.exp_data.calc_roi_max(self.exp_data.roi_data.ds_roi)

    def get_ds_temp(self):
        try:
            return self.ds_fitted_spectrum.T
        except AttributeError:
            return 0

    def get_us_spectrum(self):
        if not self.exp_data_us_calibration_data_same_dimension():
            return self.exp_data.us_spectrum
        else:
            x=self.exp_data.us_spectrum.x
            corrected_spectrum = self.exp_data.calc_corrected_us_spectrum(self.us_calib_data.us_spectrum, 
                                                self.us_calib_param.get_calibrated_spec(x))
            self.us_fitted_spectrum = FitSpectrum(corrected_spectrum)
            return [corrected_spectrum, self.us_fitted_spectrum]

    def get_us_roi_max(self):
        return self.exp_data.calc_roi_max(self.exp_data.roi_data.us_roi)

    def get_us_temp(self):
        try:
            return self.us_fitted_spectrum.T
        except AttributeError:
            return 0

    def get_whole_spectrum(self):
        return self.exp_data.x, self.exp_data.y_whole_spectrum

    def save_roi_data(self):
        np.savetxt('roi_data.txt', self.roi_data.get_roi_data(), delimiter=',', fmt='%.0f')     
        
    def get_x_limits(self):
        return self.exp_data.get_x_limits()

    def get_x_roi_limits(self):
        return self.calculate_wavelength(self.exp_data.roi_data.get_x_limits())

    def set_x_roi_limits_to(self, limits):
        limits_ind=self.calculate_ind(limits)
        self.roi_data.set_x_limits(limits_ind)



class GeneralData(object):
    def __init__(self, img_file, roi_data_manager):
        self._img_file= img_file
        self.roi_data=roi_data_manager.get_roi_data(img_file.get_dimension())
        self.read_parameter()
        self.calc_spectra()
    
    def read_parameter(self):
        self.filename = self._img_file.filename
        self.img_data = self._img_file.img
        self.x_whole = self._img_file.x_calibration

    def calc_spectra(self):
        raise NotImplementedError

    def get_x(self):
        raise NotImplementedError
    
    def get_ds_y(self):
        raise NotImplementedError
    
    def get_us_y(self):
        raise NotImplementedError

    def get_ds_spectrum(self):
        raise NotImplementedError

    def get_us_spectrum(self):
        raise NotImplementedError

    def get_img_dimension(self):
        return self._img_file.get_dimension()

class ImgData(GeneralData):
    def calc_spectra(self):
        x = self.x_whole[(self.roi_data.us_roi.x_min):           
                         (self.roi_data.us_roi.x_max+1)]
        self.ds_spectrum = Spectrum(x,self.calc_spectrum(self.roi_data.ds_roi))
        self.us_spectrum = Spectrum(x,self.calc_spectrum(self.roi_data.us_roi))

    def calc_spectrum(self, roi):
        roi_img=self.get_roi_img(roi)
        return np.sum(roi_img,0)/np.float(np.size(roi_img,0))

    def calc_roi_max(self, roi):
        roi_img=self.get_roi_img(roi)
        return np.max(roi_img)

    def get_roi_img(self, roi):
        return self.img_data[roi.y_min : roi.y_max+1, roi.x_min:roi.x_max+1]

    def get_x_limits(self):
        return np.array([min(self.x_whole), max(self.x_whole)])

    def get_x_whole(self):
        return self.x_whole

    def get_x(self):
        return self.ds_spectrum.x
    
    def get_ds_y(self):
        return self.ds_spectrum.y

    def get_us_y(self):
        return self.us_spectrum.y

    def get_ds_spectrum(self):
        return self.ds_spectrum

    def get_us_spectrum(self):
        return self.us_spectrum
    
class ExpData(ImgData):
    def read_parameter(self):
        super(ExpData, self).read_parameter()
        self._get_file_number()
        self._get_file_base_str()

    def get_img_data(self):
        return self.img_data

    def calc_corrected_ds_spectrum(self, calib_img_spectrum, calib_spectrum):
        response_function = calib_img_spectrum.y / calib_spectrum
        response_function[np.where(response_function==0)]=np.NaN
        corrected_exp_y = self.ds_spectrum.y / response_function
        corrected_exp_y = corrected_exp_y/max(corrected_exp_y)*max(self.ds_spectrum.y)
        self.ds_corrected_spectrum = Spectrum(self.ds_spectrum.x, corrected_exp_y)
        return self.ds_corrected_spectrum

    def calc_corrected_us_spectrum(self, calib_img_spectrum, calib_spectrum):
        response_function = calib_img_spectrum.y / calib_spectrum
        response_function[np.where(response_function==0)]=np.NaN
        corrected_exp_y = self.us_spectrum.y / response_function
        corrected_exp_y = corrected_exp_y/max(corrected_exp_y)*max(self.us_spectrum.y)
        self.us_corrected_spectrum = Spectrum(self.us_spectrum.x, corrected_exp_y)
        test = FitSpectrum(self.us_corrected_spectrum)
        return self.us_corrected_spectrum

    def _get_file_number(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        num_str = file_str.split('_')[-1]
        try:
            self._file_number = int(num_str)
            self._num_char_amount = len(num_str) #if number has leading zeros
        except ValueError:
            self._file_number = 0
            self._num_char_amount = 1

    def _get_file_base_str(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        self._file_base_str = '_'.join(file_str.split('_')[0:-1])
        self._file_ending = self.filename.split('.')[-1]

    def get_next_file_names(self):
        new_file_name = self._file_base_str + '_' + str(self._file_number + 1) + \
                        '.' + self._file_ending
        format_str='0'+str(self._num_char_amount)+'d'
        number_str=("{0:"+format_str+'}').format(self._file_number + 1)
        new_file_name_with_leading_zeros = self._file_base_str + '_' + \
                    number_str + '.' + self._file_ending
        return new_file_name, new_file_name_with_leading_zeros

    def get_previous_file_names(self):
        new_file_name = self._file_base_str + '_' + str(self._file_number - 1) + \
                        '.' + self._file_ending
        format_str='0'+str(self._num_char_amount)+'d'
        number_str=("{0:"+format_str+'}').format(self._file_number - 1)
        new_file_name_with_leading_zeros = self._file_base_str + '_' + \
                    number_str + '.' + self._file_ending
        return new_file_name, new_file_name_with_leading_zeros

class DummyImg(ExpData):
    def __init__(self, roi_data_manager):
        self.roi_data=roi_data_manager.get_roi_data([1300,100])
        self.create_img()
        self.filename = 'dummy_img.spe'

    def create_img(self):
        x=np.linspace(645,850,1300)
        y=np.linspace(0,101, 100)
        X,Y = np.meshgrid(x,y)

        Z=np.ones((len(y),len(x)))
        random.seed()
        T1=random.randrange(1700,3000,1)
        T2=T1+ random.randrange(-200,200,1)

        black1 = black_body_function(x,T1,1e-8)
        gauss1 = gauss_curve_function(y,2,80,3)
        black2 = black_body_function(x,T2,1e-8)
        gauss2 = gauss_curve_function(y,2,15,3)

        for x_ind in xrange(len(x)):
            for y_ind in xrange(len(y)):
                Z[y_ind,x_ind] = black1[x_ind]*gauss1[y_ind] +black2[x_ind]*gauss2[y_ind]
        self.img_data=Z+np.random.normal(0,.1*max(black1),(len(y),len(x)))
        self.x_whole = x
        self.calc_spectra()

    def get_img_dimension(self):
        return (1300,100)
        



class ExpSpecData(ExpData):
    def update_roi(self):
        x_max, y_max = self._img_file.get_dimension()        
        self.roi_data.set_max_x_limits(x_max-1)

    def calc_spectra(self):
        self.y_whole = self.img_data[0]
        self.x_zoom = self.x_whole[(self.roi_data.us_roi.x_min):           
                         (self.roi_data.us_roi.x_max + 1)]
        self.y_zoom = self.y_whole[(self.roi_data.us_roi.x_min):           
                         (self.roi_data.us_roi.x_max + 1)]
        self.ds_spectrum = Spectrum(self.x_whole,self.y_whole)
        self.us_spectrum = Spectrum(self.x_zoom, self.y_zoom)

    def get_img_data(self):
        raise NotImplementedError

class CalibParam(object):
    def __init__(self):
        self.modus=1
        #modi:  0 - given temperature
        #       1 - etalon spectrum

        self.temp=2000
        self.etalon_spectrum_func = None

    def set_modus(self, val):
        self.modus = val

    def set_temp(self, temp):
        self.temp = temp
        
    def load_etalon_spec(self, fname):
        try:
            data = np.loadtxt(fname, delimiter = ',')
        except ValueError:
            try:
                data = np.loadtxt(fname, delimiter = ' ')
            except ValueError:
                try:
                    data = np.loadtxt(fname, delimiter = ';')
                except:
                    data = np.loadtxt(fname, delimiter = '\t')
        self.etalon_spectrum_func = ip.interp1d(data.T[0], data.T[1],'cubic')
        self.etalon_file_name = fname

    def get_calibrated_spec(self, wavelength):
        if self.modus==0:
            y=black_body_function(wavelength, self.temp, 1)
            return y/max(y)
        elif self.modus==1:
            try:
                return self.etalon_spectrum_func(wavelength)
            except:
                pub.sendMessage("INTERPOLATION RANGE ERROR", self)
                return np.ones(np.size(wavelength))

    def get_etalon_fname(self):
        return self.etalon_file_name


class Spectrum():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_y_range(self):
        return max(self.y) - min(self.y)

    def get_x_range(self):
        return max(self.x) - min(self.x)

    def get_x_plot_limits(self):
        return [min(self.x), max(self.x)]

    def get_y_plot_limits(self, factor=0.05):
        return [min(self.y), max(self.y) + factor * self.get_y_range()]

    def get_data(self):
        return [self.x,self.y]

class FitSpectrum(Spectrum):
    def __init__(self,spectrum):
        self._orig_spectrum = spectrum
        try:
            param, cov = curve_fit(black_body_function, spectrum.x,spectrum.y,p0=[2000,1e-11])
            self.T = param[0]
            self.T_err = np.sqrt(cov[0,0])
            
            self.x = spectrum.x
            self.y = black_body_function(self.x,param[0],param[1])
        except (RuntimeError, TypeError):
            self.T = np.NaN
            self.T_err = np.NaN
            self.x = []
            self.y = []



class ROI():
    def __init__(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]

    def set_x_limit(self, xlimit):
        self.x_min = xlimit[0]
        self.x_max = xlimit[1]

    def set_y_limit(self, ylimit):
        self.y_max = ylimit[0]
        self.y_max = ylimit[1]

    def set_x_max(self, x_max):
        if self.x_max > x_max:
            self.x_max=x_max
        if self.x_min >= x_max:
            self.x_min=0;
            
    def set_y_max(self, y_max):
        if self.y_max > y_max:
            self.y_max=y_max
        if self.y_min >= y_max:
            self.y_min=y_max-1;

    def get_width(self):
        return self.x_max - self.x_min
    
    def get_height(self):
        return self.y_max - self.y_min

    def get_x_limits(self):
        return [self.x_min, self.x_max]

    def get_y_limits(self):
        return [self.y_min,self.y_max]

    def get_roi_as_list(self):
        return [self.x_min, self.x_max, self.y_min, self.y_max]

    def set_roi(self, limits):
        self.x_min = limits[0]
        self.x_max = limits[1]
        self.y_min = limits[2]
        self.y_max = limits[3]


class ROIDataManager():
    def __init__(self):
        self._img_dimensions_list = []
        self._roi_data_list = []
        self._num=0
        self._current=None

    def _exists(self, dimension):
        if self._get_dimension_ind(dimension) is not None:
            return True
        else:
            return False

    def _add(self, img_dimension, roi_data):
        self._img_dimensions_list.append(img_dimension)
        self._roi_data_list.append(roi_data)
        self._num+=1

    def _get_dimension_ind(self,img_dimension):
        for ind in range(self._num):
            if self._img_dimensions_list[ind]==img_dimension:
                self._current = ind
                return ind
        self._current=None
        return None

    def get_roi_data(self, img_dimension):
        if self._exists(img_dimension):
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]
        else:
            ds_limits = np.array([0.25*(img_dimension[0]-1), 0.75*(img_dimension[0]-1),
                                    0.8*(img_dimension[1]-1), 0.9*(img_dimension[1]-1)])
            us_limits = np.array([0.25*(img_dimension[0]-1), 0.75*(img_dimension[0]-1),
                                    0.1*(img_dimension[1]-1), 0.2*(img_dimension[1]-1)])
            ds_limits = np.round(ds_limits)
            us_limits = np.round(us_limits)

            self._add(img_dimension, ROIData(ds_limits, us_limits))
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]

    def get_current_roi(self):
        return self._roi_data_list[self._current]
        

class ROIData():
    def __init__(self, ds_limits, us_limits):
        self.ds_roi = ROI(ds_limits)
        self.us_roi = ROI(us_limits)

    def get_roi_data(self):
        data = [self.ds_roi.get_roi_as_list()]
        data.append(self.us_roi.get_roi_as_list())
        return data

    def set_ds_roi(self, ds_limits):
        self.ds_roi = ROI(ds_limits)
        self.us_roi.set_x_limit(ds_limits[:2])
        pub.sendMessage("ROI CHANGED")

    def set_us_roi(self, us_limits):
        self.us_roi = ROI(us_limits)
        self.ds_roi.set_x_limit(us_limits[:2])
        pub.sendMessage("ROI CHANGED")

    def set_max_x_limits(self, x_max):
        self.ds_roi.set_x_max(x_max)
        self.us_roi.set_x_max(x_max)

    def set_max_y_limits(self, y_max):
        self.ds_roi.set_y_max(y_max)
        self.us_roi.set_y_max(y_max)

    def set_max_limits(self, x_max, y_max):
        self.set_max_x_limits(x_max)
        self.set_max_y_limits(y_max)

    def set_x_limits(self, x_limits):
        self.set_x_min(x_limits[0])
        self.set_x_max(x_limits[1])

    def get_x_limits(self):
        return [self.ds_roi.x_min, self.ds_roi.x_max]

    def set_x_min(self, x_min):
        self.ds_roi.x_min = x_min
        self.us_roi.x_min = x_min
        pub.sendMessage("ROI CHANGED")

    def set_x_max(self, x_max):
        self.ds_roi.x_max = x_max
        self.us_roi.x_max = x_max
        pub.sendMessage("ROI CHANGED")


def black_body_function(wavelength, temp, scaling):
    wavelength = np.array(wavelength) * 1e-9
    c1 = 3.7418e-16
    c2 = 0.014388
    return scaling * c1 * wavelength ** -5 / (np.exp(c2 / (wavelength * temp)) - 1)


def gauss_curve_function(x, scaling, center, sigma):
    return scaling*np.exp(-(x-float(center))**2/(2*sigma**2))
