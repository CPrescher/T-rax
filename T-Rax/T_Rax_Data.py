from wx.lib.pubsub import Publisher as pub
from SPE_module import SPE_File
import os.path
import numpy as np
import scipy.interpolate as ip


class ImgData(object):
    def __init__(self,filename, roi_data):
        self.filename = filename
        self.roi_data=roi_data
        self._img_file = SPE_File(filename)
        self.img_data = self._img_file.img        
        self.x_whole_spectrum =  self._img_file.x_calibration
        self.calc_spectra()

    def calc_spectra(self):
        self.x = self._img_file.x_calibration[(self.roi_data.us_roi.x_min):           
                                            (self.roi_data.us_roi.x_max+1)]
        self.y_ds_spectrum = self.calc_spectrum(self.roi_data.ds_roi)
        self.y_us_spectrum = self.calc_spectrum(self.roi_data.us_roi)

    def calc_spectrum(self, roi):
        spec=[]
        for x_ind in range(roi.x_min,roi.x_max+1):
            spec_val=0
            for y_ind in range(roi.y_min,roi.y_max+1):
                spec_val+=self.img_data[y_ind][x_ind]    
            spec.append(spec_val)
        return np.array(spec)

    def get_x_limits(self):
        return np.array([min(self.x_whole_spectrum), max(self.x_whole_spectrum)])

    

class ExpData(ImgData):
    def __init__(self, filename, roi_data):
        super(ExpData, self).__init__(filename, roi_data)
        self._get_file_number()
        self._get_file_base_str()

    def _get_file_number(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        num_str = file_str.split('_')[-1]
        try:
            self._file_number = int(num_str)
        except ValueError:
            self._file_number = 0

    def _get_file_base_str(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        self._file_base_str = ''.join(file_str.split('_')[0:-1])

    def load_next_file(self):
        new_file_name = self._file_base_str + '_' + str(self._file_number + 1) + '.SPE'
        if os.path.isfile(new_file_name):
            self.load_exp_data(new_file_name)

    def load_previous_file(self):
        new_file_name = self._file_base_str + '_' + str(self._file_number - 1) + '.SPE'
        if os.path.isfile(new_file_name):
            self.load_exp_data(new_file_name)



class TraxData(object):
    def __init__(self):
        self._read_roi_param()
        self._read_calib_param()
        self.ds_calib_img_data = None
        self.us_calib_img_data = None

    def _read_roi_param(self):
        if os.path.isfile('roi_data.txt'):
            roi_list = np.loadtxt('roi_data.txt',delimiter=',')
            self.roi_data = ROIData(self, map(int, roi_list[0]),map(int, roi_list[1]))
        else:
            self.roi_data = ROIData(self, [10,20,100,1000],[80,90,100,1000])

    def _read_calib_param(self):
        self.ds_temp=2000;
        self.us_temp=2000;
        #read 15A lamp calibration:
        data=np.loadtxt("Temperature Calibration\\15A Lamp.txt", delimiter = ',')
        self.etalon_spectrum_func = ip.interp1d(data.T[0], data.T[1])


    def load_exp_data(self, file_name):
        self.exp_data = ExpData(file_name, self.roi_data)
        pub.sendMessage("EXP DATA CHANGED", self)

    def load_ds_calib_data(self, file_name):
        self.ds_calib_data = ImgData(file_name, self.roi_data)

    def load_us_calib_data(self, file_name):
        self.ds_calib_data = ImgData(file_name, self.roi_data)

    def get_wavelength(self,channel):
        if isinstance(channel,list):
            result=[]
            for c in channel:
                result.append(self.exp_data.x_whole_spectrum[c])
            return np.array(result)
        else:
            return self.exp_data.x_whole_spectrum[channel]

    def calculate_ind(self, wavelength):
        result=[]
        xdata=self.exp_data.x_whole_spectrum
        for w in wavelength:
            base_ind= max(max(np.where(xdata<=w)))
            result.append((w-xdata[base_ind])/  \
                (xdata[base_ind+1]-xdata[base_ind]) \
                +base_ind)
        return np.array(result)
    
    def calc_spectra(self):
        self.exp_data.calc_spectra()

    def get_exp_file_name(self):
        return self.exp_data.filename.split('\\')[-1]

    def get_exp_img_data(self):
        return self.exp_data.img_data
             
    def get_ds_spectrum(self):
        return self.exp_data.x,self.exp_data.y_ds_spectrum

    def get_us_spectrum(self):
        return self.exp_data.x,self.exp_data.y_us_spectrum

    def get_whole_spectrum(self):
        return self.exp_data.x, self.exp_data.y_whole_spectrum

    def save_roi_data(self):
        np.savetxt('roi_data.txt', self.roi_data.get_roi_data(), delimiter=',', fmt='%.0f')     
        
    def get_x_limits(self):
        return self.exp_data.get_x_limits()


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
        data=[self.ds_roi.get_list()]
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


def black_body_function(wavelength, temp, scaling):
    wavelength=np.array(wavelength)*1e-9
    c1=3.7418e-16
    c2=0.014388
    return scaling*c1*wavelength**-5/(np.exp(c2/(wavelength*temp))-1)

