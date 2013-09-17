from wx.lib.pubsub import Publisher as pub
from SPE_module import SPE_File
import os.path
import numpy as np
import scipy.interpolate as ip
from scipy.optimize import curve_fit


class TraxData(object):
    def __init__(self):
        self._read_roi_param()
        self._read_calib_param()
        self.ds_calib_data = None
        self.us_calib_data = None

    def _read_roi_param(self):
        if os.path.isfile('roi_data.txt'):
            roi_list = np.loadtxt('roi_data.txt',delimiter=',')
            self.roi_data = ROIData(self, map(int, roi_list[0]),map(int, roi_list[1]))
        else:
            self.roi_data = ROIData(self, [10,20,100,1000],[80,90,100,1000])

    def _read_calib_param(self):
        self.ds_temp = 2000
        self.us_temp = 2000
        #read 15A lamp calibration:
        data = np.loadtxt("Temperature Calibration\\15A Lamp.txt", delimiter = ',')
        self.etalon_spectrum_func = ip.interp1d(data.T[0], data.T[1],'cubic')

    def load_exp_data(self, filename):
        self.exp_data = self.read_exp_image_file(filename)
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
            return ExpData(img_file, self.roi_data)
        elif img_file.type=='spectrum':
            return ExpSpecData(img_file, self.roi_data)

    def load_ds_calib_data(self, file_name):
        self.ds_calib_data = ImgData(file_name, self.roi_data)
        self.calc_spectra()
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_us_calib_data(self, file_name):
        self.us_calib_data = ImgData(file_name, self.roi_data)
        self.calc_spectra()
        pub.sendMessage("EXP DATA CHANGED", self)

    def get_wavelength(self,channel):
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
                base_ind = max(max(np.where(xdata <= w)))
                result.append(int(np.round((w - xdata[base_ind]) / \
                    (xdata[base_ind + 1] - xdata[base_ind]) \
                    + base_ind)))
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
        return self.exp_data.filename.split('\\')[-1]

    def get_ds_calib_file_name(self):
        return self.ds_calib_data.filename.split('\\')[-1]

    def get_us_calib_file_name(self):
        return self.us_calib_data.filename.split('\\')[-1]

    def get_exp_img_data(self):
        return self.exp_data.get_img_data()

    def get_exp_graph_data(self):
        return self.exp_data.get_ds_spectrum()
             
    def get_ds_spectrum(self):
        if self.ds_calib_data == None:
            return self.exp_data.ds_spectrum
        else:
            corrected_spectrum = self.exp_data.calc_corrected_ds_spectrum(self.ds_calib_data.ds_spectrum, 
                                                self.etalon_spectrum_func(self.exp_data.ds_spectrum.x))
            fitted_spectrum = FitSpectrum(corrected_spectrum)
            return [corrected_spectrum, fitted_spectrum]

    def get_us_spectrum(self):
        if self.us_calib_data == None:
            return self.exp_data.us_spectrum
        else:
            corrected_spectrum = self.exp_data.calc_corrected_us_spectrum(self.us_calib_data.us_spectrum, 
                                                self.etalon_spectrum_func(self.exp_data.us_spectrum.x))
            fitted_spectrum = FitSpectrum(corrected_spectrum)
            return [corrected_spectrum, fitted_spectrum]

    def get_whole_spectrum(self):
        return self.exp_data.x, self.exp_data.y_whole_spectrum

    def save_roi_data(self):
        np.savetxt('roi_data.txt', self.roi_data.get_roi_data(), delimiter=',', fmt='%.0f')     
        
    def get_x_limits(self):
        return self.exp_data.get_x_limits()



class GeneralData(object):
    def __init__(self, img_file, roi_data):
        self.roi_data=roi_data
        self._img_file= img_file
        self.read_parameter()
        self.update_roi()
        self.calc_spectra()
    
    def read_parameter(self):
        self.filename = self._img_file.filename
        self.img_data = self._img_file.img
        self.x_whole = self._img_file.x_calibration

    def calc_spectra(self):
        raise NotImplementedError

    def update_roi(self):
        x_max, y_max = self._img_file.get_dimension()        
        self.roi_data.set_max_limits(x_max-1, y_max-1)

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

class ImgData(GeneralData):
    def calc_spectra(self):
        x = self.x_whole[(self.roi_data.us_roi.x_min):           
                         (self.roi_data.us_roi.x_max + 1)]
        self.ds_spectrum = Spectrum(x,self.calc_spectrum(self.roi_data.ds_roi))
        self.us_spectrum = Spectrum(x,self.calc_spectrum(self.roi_data.us_roi))

    def calc_spectrum(self, roi):
        spec = []
        for x_ind in range(roi.x_min,roi.x_max + 1):
            spec_val = 0
            for y_ind in range(roi.y_min,roi.y_max + 1):
                spec_val+=self.img_data[y_ind][x_ind]    
            spec.append(spec_val)
        return np.array(spec)

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
        corrected_exp_y = self.ds_spectrum.y / response_function
        self.ds_corrected_spectrum = Spectrum(self.ds_spectrum.x, corrected_exp_y)
        return self.ds_corrected_spectrum

    def calc_corrected_us_spectrum(self, calib_img_spectrum, calib_spectrum):
        response_function = calib_img_spectrum.y / calib_spectrum
        corrected_exp_y = self.us_spectrum.y / response_function
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
        self._file_base_str = ''.join(file_str.split('_')[0:-1])
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
        self.y_min = limits[0]
        self.y_max = limits[1]
        self.x_min = limits[2]
        self.x_max = limits[3]

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

    def get_list(self):
        return [self.y_min, self.y_max, self.x_min, self.x_max]


class ROIData():
    def __init__(self, parent, ds_limits, us_limits):
        self.parent = parent
        self.ds_roi = ROI(ds_limits)
        self.us_roi = ROI(us_limits)

    def get_roi_data(self):
        data = [self.ds_roi.get_list()]
        data.append(self.us_roi.get_list())
        return data

    def set_ds_roi(self, ds_limits):
        self.ds_roi = ROI(ds_limits)
        self.us_roi.set_x_limit(ds_limits[2:])
        self.parent.calc_spectra()
        pub.sendMessage("ROI CHANGED", self.parent)

    def set_us_roi(self, us_limits):
        self.us_roi = ROI(us_limits)
        self.ds_roi.set_x_limit(us_limits[2:])
        self.parent.calc_spectra()
        pub.sendMessage("ROI CHANGED", self.parent)

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

    def set_x_min(self, x_min):
        self.ds_roi.x_min = x_min
        self.us_roi.x_min = x_min
        self.parent.calc_spectra()
        pub.sendMessage("ROI CHANGED", self.parent)

    def set_x_max(self, x_max):
        self.ds_roi.x_max = x_max
        self.us_roi.x_max = x_max
        self.parent.calc_spectra()
        pub.sendMessage("ROI CHANGED", self.parent)


def black_body_function(wavelength, temp, scaling):
    wavelength = np.array(wavelength) * 1e-9
    c1 = 3.7418e-16
    c2 = 0.014388
    return scaling * c1 * wavelength ** -5 / (np.exp(c2 / (wavelength * temp)) - 1)

