# read_spe.py
import numpy as np
from numpy.polynomial.polynomial import polyval
import time
from matplotlib import tight_layout
import matplotlib.pyplot as plt
from pylab import show, meshgrid,figure 
from xml.dom.minidom import parseString

class SPE_File(object):
    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._read_parameter()
        self._load_img()
        self._fid.close()

    def _read_parameter(self):
        self._read_size()
        self._read_date_time()
        self._read_x_calibration_and_exposure_time()
        self._read_datatype()

    def _read_size(self):
        self._xdim = np.int64(self._read_at(42, 1, np.int16)[0])
        self._ydim = np.int64(self._read_at(656, 1, np.int16)[0])

    def _read_date_time(self):
        rawdate = self._read_at(20, 9, np.int8)
        rawtime = self._read_at(172, 6, np.int8)
        strdate = ''.join([chr(i) for i in rawdate])
        strdate += ''.join([chr(i) for i in rawtime])
        self._date_time = time.strptime(strdate,"%d%b%Y%H%M%S")

    def _read_x_calibration_and_exposure_time(self):
        self.xml_offset = self._read_at(678,1,np.long)        
        if self.xml_offset == [0]: #means that there is no XML present, hence it is a pre 3.0 version of the SPE
                              #file
            self.x_calibration = self._read_calibration_from_header()
            self.exp_time = self._read_exposure_from_header()
        else:
            self.dom = self._create_dom_from_xml()
            self.x_calibration = self._read_calibration_from_dom()
            self.exp_time = self._read_exposure_from_dom(dom)

    def _read_calibration_from_header(self):
        x_polynocoeff = self._read_at(3263,6,np.double)
        x_val = np.arange(self._xdim) + 1
        x_calibration = polyval(x_val, x_polynocoeff)
        return x_calibration

    def _read_exposure_from_header(self):
        return self._read_at(10,1,np.float)

    def _create_dom_from_xml(self):
        return parseString(self.xml_string)

    def _get_xml_string(self):
        xml_size = self.get_file_size() - self.xml_offset
        xml = self._read_at(xml_offset, xml_size, np.byte)
        self.xml_string=''.join([chr(i) for i in xml])

    def _read_calibration_from_dom(self,dom):
        spe_format = dom.childNodes[0]
        calibrations = spe_format.getElementsByTagName('Calibrations')[0]
        wavelengthmapping = calibrations.getElementsByTagName('WavelengthMapping')[0]
        wavelengths = wavelengthmapping.getElementsByTagName('Wavelength')[0]
        wavelength_values = wavelengths.childNodes[0]
        return [float(i) for i in wavelength_values.toxml().split(',')]
 
    def _read_exposure_from_dom(self):
        spe_format = self.dom.childNodes[0]
        origin = spe_format.getElementsByTagName('DataHistories')[0].\
                        getElementsByTagName('DataHistory')[0].\
                        getElementsByTagName('Origin')[0]
        if len(origin.getElementsByTagName('Experiment')) != 1: #check if it is a real v3.0 file
            exposure_time = origin.getElementsByTagName('Experiment')[0].\
                        getElementsByTagName('Devices')[0].\
                        getElementsByTagName('Cameras')[0].\
                        getElementsByTagName('Camera')[0].\
                        getElementsByTagName('ShutterTiming')[0].\
                        getElementsByTagName('ExposureTime')[0]

        else: #this is searching for legacy experiment:
            exposure_time = origin.getElementsByTagName('LegacyExperiment')[0].\
                                 getElementsByTagName('Experiment')[0].\
                                 getElementsByTagName('CollectionParameters')[0].\
                                 getElementsByTagName('Exposure')[0].attributes["value"].value

        self.exposure_time = np.float(exposure_time.split()[0])

    def _read_datatype(self):
        self._data_type = self._read_at(108, 1, np.uint16)[0]
        print self._data_type

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
        y=np.arange(self._ydim)+1
        x=self.x_calibration
        return np.meshgrid(x,y)



if __name__ == "__main__":
    spe_file = SPE_File('spe files\Pt_230.SPE')
    #spe_file = SPE_File('binary files\lamp_15_up(v3.0).SPE')
    img = spe_file.img
    x,y = spe_file.get_mesh_grid()

   
    img_fig = figure()
    imgplot = plt.imshow(img, aspect='auto', cmap='gray')
    y_spec=img.sum(axis=0)
    x_spec=spe_file.x_calibration

    figure()
    plt.plot(x_spec,y_spec)
    plt.xlim(650,850)

    plt.tight_layout()
    show()