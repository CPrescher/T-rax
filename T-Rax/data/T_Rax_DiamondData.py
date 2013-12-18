from wx.lib.pubsub import pub
from SPE_module import SPE_File
import os.path
import numpy as np
import random
import scipy.interpolate as ip
from scipy.optimize import minimize
from scipy.ndimage import gaussian_filter1d

from data.T_Rax_GeneralData import TraxGeneralData
from data.T_Rax_TemperatureData import ROI, Spectrum, gauss_curve_function


class TraxDiamondData(TraxGeneralData):
    def __init__(self):
        self.roi_data_manager =  ROIDiamondManager()
        self._create_dummy_img()
        self.click_pos=1334
        self.diamond_reference_pos=1334
        self.derivative_smoothing = 5
        self.laser_line = 532 #in nm
        self.return_derivative = True

    def _create_dummy_img(self):
        self.exp_data=DummyImg(self.roi_data_manager)
        self.fitted_spectrum=Spectrum([],[])
        self.roi = self.exp_data.roi

    def load_exp_file(self, filename):
        self.exp_data = self.read_exp_image_file(filename)
        self.roi = self.exp_data.roi
        self.fitted_spectrum=Spectrum([],[])
        pub.sendMessage("EXP DIAMOND DATA CHANGED")

    def read_exp_image_file(self, file_name):
        img_file= SPE_File(file_name)
        return ExpDiamondData(img_file, self.roi_data_manager)
  
#********************DIAMOND STUFF HERE***********************
#
    
    def get_derivative_spectrum(self):
        if self.return_derivative:
            original_spectrum = self.get_spectrum()
            derivative_spectrum = Spectrum(original_spectrum.x, np.gradient(original_spectrum.y))
            derivative_spectrum.y = gaussian_filter1d(derivative_spectrum.y, self.derivative_smoothing)
            derivative_spectrum.y = float((max(original_spectrum.y)-min(original_spectrum.y)))/(max(derivative_spectrum.y)-min(derivative_spectrum.y)) * derivative_spectrum.y
            derivative_spectrum.y = derivative_spectrum.y+min(original_spectrum.y)-min(derivative_spectrum.y)
            return derivative_spectrum
        else:
            return Spectrum([],[])   

    def set_click_pos(self, pos):
        self.click_pos = pos
        pub.sendMessage("DIAMOND POS CHANGED")

    def set_diamond_reference_pos(self, pos):
        self.diamond_reference_pos=pos
        pub.sendMessage("DIAMOND POS CHANGED")

    def get_pressure(self):
        K=547
        Kp=3.75

        P=(K*(self.click_pos-self.diamond_reference_pos)/self.diamond_reference_pos)*\
            (1 + 0.5*(Kp-1)*(self.click_pos-self.diamond_reference_pos)/self.diamond_reference_pos)
        return P

    def set_laser_line(self, laser_line):
        self.laser_line=laser_line
        pub.sendMessage("EXP DIAMOND DATA CHANGED")

    def convert_reverse_cm_to_wavelength(self, reverse_cm):
        return 1/(1.0/self.laser_line-np.array(reverse_cm)/1.0e7)

    def convert_wavelength_to_reverse_cm(self, wavelength):
        return (1.0/self.laser_line-1/np.array(wavelength))*1.0e7

    def get_spectrum(self):
        wavelength_spectrum=self.exp_data.get_spectrum()
        return Spectrum(self.convert_wavelength_to_reverse_cm(wavelength_spectrum.x),
                        wavelength_spectrum.y)
                        



class ExpDiamondData(object):
    def __init__(self, img_file, roi_data_manager):
        self._img_file= img_file
        self.roi=roi_data_manager.get_roi_data(img_file.get_dimension())
        self.read_parameter()        
        self._get_file_number()
        self._get_file_base_str()
    
    def read_parameter(self):
        self.filename = self._img_file.filename
        self._img_data = self._img_file.img
        self.x_whole = self._img_file.x_calibration
        self.current_frame = 0
        self.num_frames=self._img_file.num_frames

    def img_data(self):
        if self.num_frames>1:
            return self._img_data[self.current_frame]
        else:
            return self._img_data

    def get_img_data(self):
        return self.img_data()

    def get_roi_img(self):
        return self.img_data()[self.roi.y_min : self.roi.y_max+1, 
                             self.roi.x_min : self.roi.x_max+1]

    def get_spectrum(self):
        print self.roi.x_min
        roi_img = self.get_roi_img()
        x=self.x_whole[self.roi.x_min:self.roi.x_max+1]
        y=np.sum(roi_img,0)/np.float(np.size(roi_img,0))
        return Spectrum(x, np.sum(roi_img,0)/np.float(np.size(roi_img,0)))

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

    def get_x_limits(self):
        return np.array([min(self.x_whole), max(self.x_whole)])

    
    def get_file_information(self):
        return ('{exp_time:g}s, ' +\
               '{detector}, '+\
               '{grating}, ' +\
               '{center_wavelength:g}nm').format(
                exp_time=self._img_file.exposure_time,
                detector=self._img_file.detector,
                grating= self._img_file.grating,
                center_wavelength=self._img_file.center_wavelength)


class DummyImg(ExpDiamondData):
    def __init__(self, roi_data_manager):
        self.roi=roi_data_manager.get_roi_data([1300,100])
        self.create_img()
        self.filename = 'dummy_img.spe'
        self.num_frames=1
        self.current_frame=0

    def create_img(self):
        x=np.linspace(570,580,1300)
        y=np.linspace(0,101, 100)
        X,Y = np.meshgrid(x,y)

        Z=np.ones((len(y),len(x)))
        random.seed()
        T1=random.randrange(1700,3000,1)
        T2=T1+ random.randrange(-200,200,1)

        lorenz1 = lorentz_curve(x,4,0.1,572)
        gauss1 = gauss_curve_function(y,2,80,3)
        lorenz2 = lorentz_curve(x,4,0.1,572)
        gauss2 = gauss_curve_function(y,2,15,3)

        for x_ind in xrange(len(x)):
            for y_ind in xrange(len(y)):
                Z[y_ind,x_ind] = lorenz1[x_ind]*gauss1[y_ind] +lorenz2[x_ind]*gauss2[y_ind]
        self._img_data=Z+np.random.normal(0,.01*max(lorenz1),(len(y),len(x)))
        self.x_whole = x

    def img_data(self):
        return self._img_data
    
    def get_file_information(self):
        return '10s, dummy spec, 575nm'



class ROIDiamondManager():
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

    def _add(self, img_dimension, roi):
        self._img_dimensions_list.append(img_dimension)
        self._roi_data_list.append(roi)
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
            limits = np.array([0.1*(img_dimension[0]-1), 0.9*(img_dimension[0]-1),
                               0.1*(img_dimension[1]-1), 0.2*(img_dimension[1]-1)])
            limits = np.round(limits)

            self._add(img_dimension, ROI(limits))
            return self._roi_data_list[self._get_dimension_ind(img_dimension)]

    def get_current_roi(self):
        return self._roi_data_list[self._current]


def lorentz_curve(x, int, hwhm, center):
    return int* (hwhm**2/((x-center)**2+hwhm**2))

def gauss_curve(x,int,hwhm,center):
    return int*np.exp(-(x-float(center))**2/(2*hwhm**2))

def pseudo_voigt_curve(x,int,hwhm,n, center):
    return n*lorentz_curve(x,int,hwhm,center)+\
           (1-n)*gauss_curve(x,int,hwhm,center)

