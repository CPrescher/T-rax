# read_spe.py
import numpy as np
from numpy.polynomial.polynomial import polyval
import datetime
import time
from dateutil import parser
from matplotlib import tight_layout
import matplotlib.pyplot as plt
from pylab import show, meshgrid,figure 
from xml.dom.minidom import parseString

class SPE_File(object):
    def __init__(self, filename):
        self.filename=filename
        self._fid = open(filename, 'rb')
        self._read_parameter()
        self._load_img()
        self._fid.close()
        self.determine_type()

    def _read_parameter(self):
        self._read_size()
        self._read_datatype()
        self._read_x_calibration_and_exposure_time()

    def _read_size(self):
        self._xdim = np.int64(self._read_at(42, 1, np.int16)[0])
        self._ydim = np.int64(self._read_at(656, 1, np.int16)[0])


    def _read_x_calibration_and_exposure_time(self):
        self.xml_offset = self._read_at(678,1,np.long)        
        if self.xml_offset == [0]: #means that there is no XML present, hence it is a pre 3.0 version of the SPE
                              #file
                              
            self._read_date_time_from_header()
            self._read_calibration_from_header()
            self._read_exposure_from_header()
            self._read_detector_from_header()
            self._read_grating_from_header()
            self._read_center_wavelength_from_header()
        else:
            self._get_xml_string()
            self._create_dom_from_xml()
            self._read_date_time_from_dom()
            self._read_calibration_from_dom()
            self._read_detector_from_dom()
            self._read_exposure_from_dom()
            self._read_grating_from_dom()
            self._read_center_wavelength_from_dom()

    
    def _read_date_time_from_header(self):
        rawdate = self._read_at(20, 9, np.int8)
        rawtime = self._read_at(172, 6, np.int8)
        strdate = ''.join([chr(i) for i in rawdate])
        strdate += ''.join([chr(i) for i in rawtime])
        self.date_time = datetime.datetime.strptime(strdate,"%d%b%Y%H%M%S")


    def _read_calibration_from_header(self):
        x_polynocoeff = self._read_at(3263,6,np.double)
        x_val = np.arange(self._xdim) + 1
        self.x_calibration = np.array(polyval(x_val, x_polynocoeff))

    def _read_exposure_from_header(self):
        self.exposure_time = self._read_at(10,1,np.float32)

    def _read_detector_from_header(self):
        self.detector = 'unspecified'

    def _read_grating_from_header(self):
        self.grating = str(self._read_at(650,1,np.float32)[0])

    def _read_center_wavelength_from_header(self):
        self.center_wavelength = self._read_at(72,1,np.float32)[0]

    def _create_dom_from_xml(self):
        self.dom = parseString(self.xml_string)

    def _get_xml_string(self):
        xml_size = self.get_file_size() - self.xml_offset
        xml = self._read_at(self.xml_offset, xml_size, np.byte)
        self.xml_string = ''.join([chr(i) for i in xml])
        fid = open('spe_xml.xml', 'w')
        for line in self.xml_string:
            fid.write(line)
        fid.close()

    def _read_date_time_from_dom(self):
        date_time_str = self.dom.getElementsByTagName('Origin')[0].getAttribute('created')
        self.date_time = parser.parse(date_time_str)

    def _read_calibration_from_dom(self):
        spe_format = self.dom.childNodes[0]
        calibrations = spe_format.getElementsByTagName('Calibrations')[0]
        wavelengthmapping = calibrations.getElementsByTagName('WavelengthMapping')[0]
        wavelengths = wavelengthmapping.getElementsByTagName('Wavelength')[0]
        #wavelengths = self.dom.getElementsByTagName('Wavelength')[0]
        wavelength_values = wavelengths.childNodes[0]
        self.x_calibration = np.array([float(i) for i in wavelength_values.toxml().split(',')])
 
    def _read_exposure_from_dom(self):
        if len(self.dom.getElementsByTagName('Experiment')) != 1: #check if it is a real v3.0 file
            if len(self.dom.getElementsByTagName('ShutterTiming')) ==1: #check if it is a pixis detector
                self._exposure_time = self.dom.getElementsByTagName('ExposureTime')[0].childNodes[0]
                self.exposure_time = np.float(self._exposure_time.toxml())/1000.0
            else:
                self._exposure_time = self.dom.getElementsByTagName('ReadoutControl')[0].\
                                      getElementsByTagName('Time')[0].childNodes[0].nodeValue
                self._accumulations = self.dom.getElementsByTagName('Accumulations')[0].childNodes[0].nodeValue
                self.exposure_time = np.float(self._exposure_time) * np.float(self._accumulations)
        else: #this is searching for legacy experiment:
            self._exposure_time = self.dom.getElementsByTagName('LegacyExperiment')[0].\
                                 getElementsByTagName('Experiment')[0].\
                                 getElementsByTagName('CollectionParameters')[0].\
                                 getElementsByTagName('Exposure')[0].attributes["value"].value
            self.exposure_time = np.float(self._exposure_time.split()[0])

    def _read_detector_from_dom(self):
        self._camera=self.dom.getElementsByTagName('Camera')
        if len(self._camera)>=1:
            self.detector=self._camera[0].getAttribute('model')
        else:
            self.detector = 'unspecified'

    def _read_grating_from_dom(self):
        try:
            self._grating = self.dom.getElementsByTagName('Devices')[0].\
                                     getElementsByTagName('Spectrometer')[0].\
                                     getElementsByTagName('Grating')[0].\
                                     getElementsByTagName('Selected')[0].childNodes[0].toxml()
            self.grating = self._grating.split('[')[1].split(']')[0].replace(',', ' ')
        except IndexError:
            self._read_grating_from_header()

    def _read_center_wavelength_from_dom(self):
        try:
            self._center_wavelength = self.dom.getElementsByTagName('Devices')[0].\
                                               getElementsByTagName('Spectrometer')[0].\
                                               getElementsByTagName('Grating')[0].\
                                               getElementsByTagName('CenterWavelength')[0].\
                                               childNodes[0].toxml()
            self.center_wavelength= int(self._center_wavelength)
        except IndexError:
            self._read_center_wavelength_from_header()    

    def _read_datatype(self):
        self._data_type = self._read_at(108, 1, np.uint16)[0]

    def _read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def _load_img(self):
        if self._data_type == 0:
            img = self._read_at(4100, self._xdim * self._ydim, np.float32)
        elif self._data_type == 1:
            img = self._read_at(4100, self._xdim * self._ydim, np.int32)
        elif self._data_type == 2:
            img = self._read_at(4100, self._xdim * self._ydim, np.int16)
        elif self._data_type == 3:
            img = self._read_at(4100, self._xdim * self._ydim, np.uint16)
        self.img = img.reshape((self._ydim, self._xdim))
                        
    def get_dimension(self):
        return (self._xdim, self._ydim)

    def get_file_size(self):
        self._fid.seek(0,2)
        self.file_size = self._fid.tell()
        return self.file_size

    def get_mesh_grid(self):
        y = np.arange(self._ydim) + 1
        x = self.x_calibration
        return np.meshgrid(x,y)

    def determine_type(self):
        if self._ydim==1:
            self.type = 'spectrum'
        elif self._ydim>1:
            self.type = 'image'
        return self.type



if __name__ == "__main__":
    #spe_file = SPE_File('spe files\Pt_38.SPE')
    spe_file = SPE_File('D:\\Programming\\VS Projects\\T-Rax\\T-Rax\\SPE test vers3\\test_073.spe')
    #spe_file = SPE_File('binary files\lamp_15_up(v3.0).SPE')

  #img = spe_file.img
  #x,y = spe_file.get_mesh_grid()
  #
  #
  #img_fig = figure()
  #imgplot = plt.imshow(img, aspect='auto', cmap='gray')
  #y_spec = img.sum(axis=0)
  #x_spec = spe_file.x_calibration
  #
  #print np.size(y_spec)
  #print np.size(x_spec)
  #
  #figure()
  #plt.plot(x_spec,y_spec)
  #plt.xlim(650,850)
  #
  #plt.tight_layout()
  #show()