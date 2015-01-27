import os

import numpy as np
from helper import FileNameIterator

class GeneralData(object):
    def __init__(self):
        self.file_name_iterator = FileNameIterator()

    def load_exp_file(self, filename):
        raise NotImplementedError

    def load_next_data_file(self):
        next_file_name = self.file_name_iterator.get_next_filename()
        if next_file_name is not None:
            self.load_exp_file(next_file_name)

    def load_previous_data_file(self):
        previous_file_name = self.file_name_iterator.get_previous_filename()
        if previous_file_name is not None:
            self.load_exp_file(previous_file_name)

    def get_index_from(self, wavelength):
        """
        calculating image index for a given index
        :param wavelength: wavelength in nm
        :return: index
        """
        result = []
        xdata = np.array(self.exp_data.x_whole)
        try:
            for w in wavelength:
                try:
                    base_ind = max(max(np.where(xdata <= w)))
                    if base_ind < len(xdata) - 1:
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

    def get_wavelength_from(self, index):
        """
        Calculates the wavelength in nm from a given index.
        :param index:
        :return: wavelength in nm
        """
        if isinstance(index, list):
            result = []
            for c in index:
                result.append(self.exp_data.x_whole[c])
            return np.array(result)
        else:
            return self.exp_data.x_whole[index]

    def calc_spectra(self):
        self.exp_data.calc_spectra()

    def get_exp_file_name(self):
        return self.exp_data.filename

    def get_exp_img_data(self):
        return self.exp_data.get_img_data()

    def get_exp_graph_data(self):
        return self.exp_data.get_ds_spectrum()

    def get_spectrum(self):
        return self.exp_data.get_spectrum()

    def get_roi_max(self):
        return self.exp_data.calc_roi_max(self.exp_data.roi.roi)

    def get_whole_spectrum(self):
        return self.exp_data.x, self.exp_data.y_whole_spectrum

    def get_x_limits(self):
        return self.exp_data.get_x_limits()

    def get_x_roi_limits(self):
        return self.get_wavelength_from(self.exp_data.roi.get_x_limits())

    def set_x_roi_limits_to(self, limits):
        limits_ind = self.get_index_from(limits)
        self.roi.set_x_limit(limits_ind)

