# read_spe.py
import numpy as np
from numpy.polynomial.polynomial import polyval
import datetime
import time
from dateutil import parser
from matplotlib import tight_layout
from xml.dom.minidom import parseString

class SPE_File(object):
    def __init__(self, filename):
        self.filename = filename
        self._fid = open(filename, 'rb')
        self._read_parameter()
        self._load_img()
        self._fid.close()
        self.determine_type()

    def _read_parameter(self):
        self._read_size()
        self._read_datatype()
        self.xml_offset = self._read_at(678,1,np.long)        
        if self.xml_offset == [0]: #means that there is no XML present, hence it is a pre 3.0 version of the SPE
                              #file
            self._read_parameter_from_header()
        else:
            self._read_parameter_from_dom()

    def _read_size(self):
        self._xdim = np.int64(self._read_at(42, 1, np.int16)[0])
        self._ydim = np.int64(self._read_at(656, 1, np.int16)[0])

    def _read_parameter_from_header(self):
        self._read_date_time_from_header()
        self._read_calibration_from_header()
        self._read_exposure_from_header()
        self._read_detector_from_header()
        self._read_grating_from_header()
        self._read_center_wavelength_from_header()
        self._read_roi_from_header()
        self._read_num_frames_from_header()
        self._read_num_combined_frames_from_header()
        
    def _read_parameter_from_dom(self):
        self._get_xml_string()
        self._create_dom_from_xml()
        self._read_date_time_from_dom()
        self._read_calibration_from_dom()
        self._read_detector_from_dom()
        self._read_exposure_from_dom()
        self._read_grating_from_dom()
        self._read_center_wavelength_from_dom()
        self._read_roi_from_dom()
        self._select_wavelength_from_roi()
        self._read_num_frames_from_header()
        self._read_num_combined_frames_from_dom()

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
        self.exposure_time = self.exposure_time[0]

    def _read_detector_from_header(self):
        self.detector = 'unspecified'

    def _read_grating_from_header(self):
        self.grating = str(self._read_at(650,1,np.float32)[0])

    def _read_center_wavelength_from_header(self):
        self.center_wavelength = float(self._read_at(72,1,np.float32)[0])

    def _read_roi_from_header(self):
        return

    def _read_num_frames_from_header(self):
        self.num_frames=self._read_at(1446,1,np.int32)[0]

    def _read_num_combined_frames_from_header(self):
        self._num_combined_frames=1

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
        wavelength_values = wavelengths.childNodes[0]
        self.x_calibration = np.array([float(i) for i in wavelength_values.toxml().split(',')])
 
    def _read_exposure_from_dom(self):
        if len(self.dom.getElementsByTagName('Experiment')) != 1: #check if it is a real v3.0 file
            if len(self.dom.getElementsByTagName('ShutterTiming')) == 1: #check if it is a pixis detector
                self._exposure_time = self.dom.getElementsByTagName('ExposureTime')[0].childNodes[0]
                self.exposure_time = np.float(self._exposure_time.toxml()) / 1000.0
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
        self._camera = self.dom.getElementsByTagName('Camera')
        if len(self._camera) >= 1:
            self.detector = self._camera[0].getAttribute('model')
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
            self.center_wavelength = float(self._center_wavelength)
        except IndexError:
            self._read_center_wavelength_from_header()    

    def _read_roi_from_dom(self):
        try:
            self.roi_modus = str(self.dom.getElementsByTagName('ReadoutControl')[0].\
                                        getElementsByTagName('RegionsOfInterest')[0].\
                                        getElementsByTagName('Selection')[0].\
                                        childNodes[0].toxml())
            if self.roi_modus=='CustomRegions':
                self.roi_dom = self.dom.getElementsByTagName('ReadoutControl')[0].\
                                            getElementsByTagName('RegionsOfInterest')[0].\
                                            getElementsByTagName('CustomRegions')[0].\
                                            getElementsByTagName('RegionOfInterest')[0]
                self.roi_x = int(self.roi_dom.attributes['x'].value)
                self.roi_y = int(self.roi_dom.attributes['y'].value)
                self.roi_width = int(self.roi_dom.attributes['width'].value)
                self.roi_height = int(self.roi_dom.attributes['height'].value)
                self.roi_x_binning = int(self.roi_dom.attributes['xBinning'].value)
                self.roi_y_binning = int(self.roi_dom.attributes['yBinning'].value)
            elif self.roi_modus=='FullSensor':
                self.roi_x=0
                self.roi_y=0
                self.roi_width = self._xdim
                self.roi_height = self._ydim

        except IndexError:
            self.roi_x=0
            self.roi_y=0
            self.roi_width = self._xdim
            self.roi_height = self._ydim

    def _read_num_combined_frames_from_dom(self):
         self.frame_combination=self.dom.getElementsByTagName('Experiment')[0].\
                                        getElementsByTagName('Devices')[0].\
                                        getElementsByTagName('Cameras')[0].\
                                        getElementsByTagName('FrameCombination')[0]
         self.num_frames_combined = int(self.frame_combination.getElementsByTagName('FramesCombined')[0].\
                                                              childNodes[0].toxml())                                        

    def _select_wavelength_from_roi(self):
        self.x_calibration=self.x_calibration[self.roi_x: self.roi_x+self.roi_width]

    def _read_datatype(self):
        self._data_type = self._read_at(108, 1, np.uint16)[0]

    def _read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def _load_img(self):
        self.img = self.read_frame(4100)
        if self.num_frames>1:
            img_temp=[]
            img_temp.append(self.img)
            for n in xrange(self.num_frames-1):
                img_temp.append(self.read_frame())
            self.img=img_temp

    def read_frame(self,pos=None):
        if pos==None:
            pos=self._fid.tell()
        if self._data_type == 0:
            img = self._read_at(pos, self._xdim * self._ydim, np.float32)
        elif self._data_type == 1:
            img = self._read_at(pos, self._xdim * self._ydim, np.int32)
        elif self._data_type == 2:
            img = self._read_at(pos, self._xdim * self._ydim, np.int16)
        elif self._data_type == 3:
            img = self._read_at(pos, self._xdim * self._ydim, np.uint16)
        return img.reshape((self._ydim, self._xdim))
                        
    def get_dimension(self):
        return (self._xdim, self._ydim)

    def get_roi(self):
        return [self.roi_x, self.roi_x+self.roi_width-1,
                self.roi_y, self.roi_y+self.roi_height-1]

    def get_file_size(self):
        self._fid.seek(0,2)
        self.file_size = self._fid.tell()
        return self.file_size

    def get_mesh_grid(self):
        y = np.arange(self._ydim) + 1
        x = self.x_calibration
        return np.meshgrid(x,y)

    def determine_type(self):
        if self._ydim == 1:
            self.type = 'spectrum'
        elif self._ydim > 1:
            self.type = 'image'
        return self.type



if __name__ == "__main__":
    #spe_file = SPE_File('spe files\Pt_38.SPE')
    spe_file = SPE_File('D:\\Programming\\VS Projects\\T-Rax\\T-Rax\\SPE test vers3\\test_073.spe')
    #spe_file = SPE_File('binary files\lamp_15_up(v3.0).SPE')