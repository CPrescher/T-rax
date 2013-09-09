from wx.lib.pubsub import Publisher as pub
from SPE_module import SPE_File
import os.path

class TraxData(object):
    def __init__(self):
        return

    def load_data(self, file_name):
        self.file_name = file_name
        self._get_file_number()
        self._get_file_base_str()
        self._img_file = SPE_File(file_name)
        self.img_data = self._img_file.img
        self.x, self.y = self._img_file.get_mesh_grid()
        self.y_whole_spectrum = self.img_data.sum(axis=0)
        self.x_whole_spectrum = self._img_file.x_calibration
        pub.sendMessage("DATA CHANGED", self)

    def load_next_file(self):
        new_file_name=self._file_base_str + '_' + str(self._file_number+1) + '.SPE'
        if os.path.isfile(new_file_name):
            self.load_data(new_file_name)

    def load_previous_file(self):
        new_file_name=self._file_base_str + '_' + str(self._file_number-1) + '.SPE'
        if os.path.isfile(new_file_name):
            self.load_data(new_file_name)

    def _get_file_number(self):
        file_str=''.join(self.file_name.split('.')[0:-1])
        num_str=file_str.split('_')[-1]
        self._file_number=int(num_str)

    def _get_file_base_str(self):
        file_str=''.join(self.file_name.split('.')[0:-1])
        self._file_base_str =''.join(file_str.split('_')[0:-1])
             
        

    def get_whole_spectrum(self):
        return self.x_whole_spectrum, self.y_whole_spectrum

    def get_img_data(self):
        return self.x, self.y, self.img_data

        
