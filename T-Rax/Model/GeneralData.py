import os

import numpy as np


class GeneralData(object):
    def load_exp_file(self):
        raise NotImplementedError

    def load_next_exp_file(self):
        new_file_name, new_file_name_with_leading_zeros = self.exp_data.get_next_file_names()
        if os.path.isfile(new_file_name):
            self.load_exp_file(new_file_name)
        elif os.path.isfile(new_file_name_with_leading_zeros):
            self.load_exp_file(new_file_name_with_leading_zeros)

    def load_previous_exp_file(self):
        new_file_name, new_file_name_with_leading_zeros = self.exp_data.get_previous_file_names()
        if os.path.isfile(new_file_name):
            self.load_exp_file(new_file_name)
        elif os.path.isfile(new_file_name_with_leading_zeros):
            self.load_exp_file(new_file_name_with_leading_zeros)

    def calculate_ind(self, wavelength):
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

    def calculate_wavelength(self, channel):
        if isinstance(channel, list):
            result = []
            for c in channel:
                result.append(self.exp_data.x_whole[c])
            return np.array(result)
        else:
            return self.exp_data.x_whole[channel]

    def calculate_ind(self, wavelength):
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

    def save_roi_data(self):
        np.savetxt('roi_data.txt', self.roi.get_roi_data(), delimiter=',', fmt='%.0f')

    def get_x_limits(self):
        return self.exp_data.get_x_limits()

    def get_x_roi_limits(self):
        return self.calculate_wavelength(self.exp_data.roi.get_x_limits())

    def set_x_roi_limits_to(self, limits):
        limits_ind = self.calculate_ind(limits)
        self.roi.set_x_limit(limits_ind)

