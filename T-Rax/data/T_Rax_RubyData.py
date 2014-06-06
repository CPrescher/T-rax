from wx.lib.pubsub import pub
from SPE_module import SPE_File
import numpy as np
import random
from scipy.optimize import minimize

from data.T_Rax_TemperatureData import ROI, Spectrum, gauss_curve_function
from data.T_Rax_GeneralData import TraxGeneralData


class TraxRubyData(TraxGeneralData):
    def __init__(self):
        self.roi_data_manager =  ROIRubyManager()        
        self._create_dummy_img()
        self.click_pos=694.35
        self.ruby_reference_pos=694.35
        self.temperature=300
        self.ruby_condition = 'hydrostatic'

    def _create_dummy_img(self):
        self.exp_data=DummyImg(self.roi_data_manager)
        self.fitted_spectrum=Spectrum([],[])
        self.roi = self.exp_data.roi

    def load_exp_file(self, filename):
        self.exp_data = self.read_exp_image_file(filename)
        self.roi = self.exp_data.roi
        self.fitted_spectrum=Spectrum([],[])
        pub.sendMessage("EXP RUBY DATA CHANGED")

    def read_exp_image_file(self, file_name):
        img_file= SPE_File(file_name)
        return ExpRubyData(img_file, self.roi_data_manager)
    
#********************RUBY STUFF HERE***********************
#
    
    def set_click_pos(self, pos):
        self.click_pos = pos
        pub.sendMessage("RUBY POS CHANGED")

    def set_ruby_reference_pos(self, pos):
        self.ruby_reference_pos=pos
        pub.sendMessage("RUBY POS CHANGED")

    def set_temperature(self, temperature):
        self.temperature = temperature
        pub.sendMessage("RUBY POS CHANGED")
    
    def set_ruby_condition(self, condition):
        self.ruby_condition=condition
        pub.sendMessage("RUBY POS CHANGED")

    def get_pressure(self):
        A=1904
        k=0.46299
        l=0.0060823
        m=0.0000010264
        if self.ruby_condition =='hydrostatic':
           B=7.665
        if self.ruby_condition == 'non-hydrostatic':
           B=5
        A_temperature_corrected=A + (k*(self.temperature - 298))
        lambda0_temperature_corrected=self.ruby_reference_pos + \
            (l*(self.temperature - 298)) + (m*((self.temperature - 298)**2))
        ratio=(self.click_pos/lambda0_temperature_corrected)**B
        P=(A_temperature_corrected/B)*ratio - (A_temperature_corrected/B)
        return P

    def fit_spectrum(self):
        x0=self.create_p0()
        bounds=self.create_limits()
        res = minimize(self.fitting_function, self.create_p0(), method='L-BFGS-B',
                              bounds=self.create_limits())
        self.set_click_pos(np.max(res.x[2:4]))
        fit_x =np.linspace(np.min(self.exp_data.get_spectrum().x), np.max(self.exp_data.get_spectrum().x),1000)
        self.fitted_spectrum=Spectrum(fit_x, self.fitting_function_helper(fit_x,\
                                                               res.x[0],res.x[1],res.x[2],\
                                                               res.x[3],res.x[4],res.x[5],\
                                                               res.x[6],res.x[7],res.x[8],\
                                                               res.x[9]))
        pub.sendMessage("RUBY POS CHANGED")

    def create_p0(self):
        intensities=[np.max(self.exp_data.get_spectrum().y),np.max(self.exp_data.get_spectrum().y)*0.5]
        positions=[self.click_pos,self.click_pos-1.5]
        hwhm =[0.1,0.1]
        n =[1,1]
        constants=[np.min(self.exp_data.get_spectrum().y),0]
        return intensities+positions+hwhm+n+constants

    def create_limits(self):
        intensities=[[0,None],[0,None]]
        positions=[[690,850],[690,850]]
        hwhm = [[0,5],[0,5]]
        n=[[0,1],[0,1]]
        constants=[[None,None],[None,None]]
        return intensities+positions+hwhm+n+constants
    
    def fitting_function(self, param):
        x=self.exp_data.get_spectrum().x
        y=self.exp_data.get_spectrum().y
        int1=param[0] 
        int2=param[1] 
        pos1=param[2]
        pos2=param[3]
        hwhm1=param[4]
        hwhm2=param[5]
        n1=param[6]
        n2=param[7]
        a=param[8]
        b=param[9]
        fit_y=self.fitting_function_helper(x,int1, int2, pos1,pos2,hwhm1, hwhm2,n1,n2,a,b)
        return np.sum((fit_y-y)**2)


    def fitting_function_helper(self,x,int1, int2, pos1,pos2,hwhm1, hwhm2,n1,n2,a,b):
        y=pseudo_voigt_curve(x,int1,hwhm1,n1,pos1)
        y+=pseudo_voigt_curve(x,int2,hwhm2,n2,pos2)
        y+=a+b/100.*x
        return y
                        

    def get_fitted_spectrum(self):
        return self.fitted_spectrum



class ExpRubyData(object):
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

    def get_filename(self):
        return self.filename

    def get_img_data(self):
        return self.img_data()

    def get_roi_img(self):
        return self.img_data()[self.roi.y_min : self.roi.y_max+1, 
                             self.roi.x_min : self.roi.x_max+1]

    def get_spectrum(self):
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
    
    def get_file_information_string(self):
        return ('{exp_time:g}s, ' +\
               '{detector}, '+\
               '{grating}, ' +\
               '{center_wavelength:g}nm').format(
                exp_time=self._img_file.exposure_time,
                detector=self._img_file.detector,
                grating= self._img_file.grating,
                center_wavelength=self._img_file.center_wavelength)


class DummyImg(ExpRubyData):
    def __init__(self, roi_data_manager):
        self.roi=roi_data_manager.get_roi_data([1300,100])
        self.create_img()
        self.filename = 'dummy_img.spe'
        self.current_frame=0;

    def create_img(self):
        x=np.linspace(650,750,1300)
        y=np.linspace(0,101, 100)
        X,Y = np.meshgrid(x,y)

        Z=np.ones((len(y),len(x)))
        random.seed()
        T1=random.randrange(1700,3000,1)
        T2=T1+ random.randrange(-200,200,1)

        lorenz1 = lorentz_curve(x,4,0.5,700)+lorentz_curve(x,3,0.5,698)
        gauss1 = gauss_curve_function(y,2,80,3)
        lorenz2 = lorentz_curve(x,4,0.5,700)+lorentz_curve(x,3,0.5,698)
        gauss2 = gauss_curve_function(y,2,15,3)

        for x_ind in xrange(len(x)):
            for y_ind in xrange(len(y)):
                Z[y_ind,x_ind] = lorenz1[x_ind]*gauss1[y_ind] +lorenz2[x_ind]*gauss2[y_ind]
        self._img_data=Z+np.random.normal(0,.01*max(lorenz1),(len(y),len(x)))
        self.x_whole = x

    def img_data(self):
        return self._img_data

    
    def get_file_information_string(self):
        return '10s, dummy spec, 700nm'



class ROIRubyManager():
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