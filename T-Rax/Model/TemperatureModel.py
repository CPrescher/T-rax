# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore
import numpy as np
from scipy.optimize import curve_fit

from .Spectrum import Spectrum
from .RoiData import RoiDataManager
from .SpeFile import SpeFile


class TemperatureModel(QtCore.QObject):
    def __init__(self):
        super(TemperatureModel, self).__init__()
        self.us_data_spectrum = Spectrum([], [])
        self.ds_data_spectrum = Spectrum([], [])

        self.us_calibration_spectrum = Spectrum([], [])
        self.ds_calibration_spectrum = Spectrum([], [])

        self.us_corrected_spectrum = Spectrum([], [])
        self.ds_corrected_spectrum = Spectrum([], [])

        self.us_fit_spectrum = Spectrum([], [])
        self.ds_fit_spectrum = Spectrum([], [])

        self.data_img_file = None
        self._data_img = None
        self.current_frame = 0
        self.roi_data_manager = RoiDataManager()

        self.us_calibration_img_file = None
        self.ds_calibration_img_file = None

        self.us_calibration_parameter = CalibrationParameter()
        self.ds_calibration_parameter = CalibrationParameter()

        self.us_temperature = np.NaN
        self.us_temperature_error = np.NaN
        self.us_fit_spectrum = Spectrum([], [])

        self.ds_temperature = np.NaN
        self.ds_temperature_error = np.NaN
        self.ds_fit_spectrum = Spectrum([], [])

    # loading spectrum text files
    #########################################################################
    def load_us_data_spectrum(self, filename):
        self.us_data_spectrum.load(filename)

    def load_ds_data_spectrum(self, filename):
        self.ds_data_spectrum.load(filename)

    def load_us_calibration_spectrum(self, filename):
        self.us_calibration_spectrum.load(filename)

    def load_ds_calibration_spectrum(self, filename):
        self.ds_calibration_spectrum.load(filename)

    # loading spe image files:
    #########################################################################
    def load_data_image(self, filename):
        self.data_img_file = SpeFile(filename)
        if self.data_img_file.num_frames > 1:
            self.data_img = self.data_img_file.img[0]
            self.current_frame = 0
        else:
            self.data_img = self.data_img_file.img

    def load_next_img_frame(self):
        return self.set_img_frame_number_to(self.current_frame+1)

    def load_previous_img_frame(self):
        return self.set_img_frame_number_to(self.current_frame-1)

    def set_img_frame_number_to(self, frame_number):
        if frame_number < 0 or frame_number >= self.data_img_file.num_frames:
            return False
        self.current_frame = frame_number
        self.data_img = self.data_img_file.img[frame_number]
        return True

    @property
    def data_img(self):
        return self._data_img

    @data_img.setter
    def data_img(self, value):
        self._data_img = value
        self._update_data_spectra()
        self._update_us_corrected_spectrum()
        self._update_ds_corrected_spectrum()

    # calibration image files:
    #########################################################################

    def load_us_calibration_image(self, filename):
        self.us_calibration_img_file = SpeFile(filename)
        self._update_us_calibration_spectrum()
        self._update_us_corrected_spectrum()

    def load_ds_calibration_image(self, filename):
        self.ds_calibration_img_file = SpeFile(filename)
        self._update_ds_calibration_spectrum()
        self._update_ds_corrected_spectrum()


    # setting etalon interface
    #########################################################################
    def load_us_etalon_spectrum(self, filename):
        self.us_calibration_parameter.load_etalon_spectrum(filename)

    def load_ds_etalon_spectrum(self, filename):
        self.ds_calibration_parameter.load_etalon_spectrum(filename)

    # updating roi values
    def set_us_roi(self, us_limits):
        self.roi_data_manager.set_us_roi(self.data_img_file.get_dimension(), us_limits)
        self.update_spectra_from_img()

    def set_ds_roi(self, ds_limits):
        self.roi_data_manager.set_ds_roi(self.data_img_file.get_dimension(), ds_limits)
        self.update_spectra_from_img()

    def set_rois(self, ds_limits, us_limits):
        self.roi_data_manager.set_roi_data(self.data_img_file.get_dimension(), ds_limits, us_limits)
        self.update_spectra_from_img()

    # spectrum calculations
    ########################################################################
    def update_spectra_from_img(self):
        self._update_data_spectra()

        self._update_us_calibration_spectrum()
        self._update_ds_calibration_spectrum()

        self._update_us_corrected_spectrum()
        self._update_ds_corrected_spectrum()

    def _update_data_spectra(self):
        roi_data = self.roi_data_manager.get_roi_data(self.data_img_file.get_dimension())
        us_data_x = self.data_img_file.x_calibration[roi_data.us_roi.x_min:roi_data.us_roi.x_max + 1]
        ds_data_x = self.data_img_file.x_calibration[roi_data.ds_roi.x_min:roi_data.ds_roi.x_max + 1]

        ds_data_y = self._get_roi_sum(self.data_img, roi_data.ds_roi)
        us_data_y = self._get_roi_sum(self.data_img, roi_data.us_roi)

        self.us_data_spectrum.data = us_data_x, us_data_y
        self.ds_data_spectrum.data = ds_data_x, ds_data_y

    def _update_us_calibration_spectrum(self):
        if self.us_calibration_img_file is not None:
            roi_data = self.roi_data_manager.get_roi_data(self.us_calibration_img_file.get_dimension())

            us_calibration_x = self.us_calibration_img_file.x_calibration[
                               roi_data.us_roi.x_min:roi_data.us_roi.x_max + 1]
            us_calibration_y = self._get_roi_sum(self.us_calibration_img_file.img, roi_data.us_roi)

            self.us_calibration_spectrum.data = us_calibration_x, us_calibration_y

    def _update_ds_calibration_spectrum(self):
        if self.ds_calibration_img_file is not None:
            roi_data = self.roi_data_manager.get_roi_data(self.ds_calibration_img_file.get_dimension())

            ds_calibration_x = self.ds_calibration_img_file.x_calibration[
                               roi_data.ds_roi.x_min:roi_data.ds_roi.x_max + 1]
            ds_calibration_y = self._get_roi_sum(self.ds_calibration_img_file.img, roi_data.ds_roi)

            self.ds_calibration_spectrum.data = ds_calibration_x, ds_calibration_y


    def _update_us_corrected_spectrum(self):
        if len(self.us_data_spectrum) is 0:
            self.us_corrected_spectrum = Spectrum([], [])
            return

        if len(self.us_calibration_spectrum) == len(self.us_data_spectrum):
            us_x, _ = self.us_data_spectrum.data
            us_lamp_spectrum = self.us_calibration_parameter.get_lamp_spectrum(us_x)
            self.us_corrected_spectrum = calculate_real_spectrum(self.us_data_spectrum,
                                                                 self.us_calibration_spectrum,
                                                                 us_lamp_spectrum)
        else:
            self.us_corrected_spectrum = self.us_data_spectrum

    def _update_ds_corrected_spectrum(self):
        if len(self.ds_data_spectrum) is 0:
            self.ds_corrected_spectrum = Spectrum([], [])
            return

        if len(self.ds_calibration_spectrum) == len(self.ds_data_spectrum):
            ds_x, _ = self.ds_data_spectrum.data
            ds_lamp_spectrum = self.ds_calibration_parameter.get_lamp_spectrum(ds_x)
            self.ds_corrected_spectrum = calculate_real_spectrum(self.ds_data_spectrum,
                                                                 self.ds_calibration_spectrum,
                                                                 ds_lamp_spectrum)
        else:
            self.ds_corrected_spectrum = self.ds_data_spectrum

    def _get_roi_sum(self, img, roi):
        roi_img = img[roi.y_min: roi.y_max + 1, roi.x_min:roi.x_max + 1]
        return np.sum(roi_img, 0) / np.float(np.size(roi_img, 0))


    # finally the fitting function
    ##################################################################
    def fit_data(self):
        self.us_temperature, self.us_temperature_error, self.us_fit_spectrum = \
            fit_black_body_function(self.us_corrected_spectrum)
        self.ds_temperature, self.ds_temperature_error, self.ds_fit_spectrum = \
            fit_black_body_function(self.ds_corrected_spectrum)

    def fit_all_frames(self):
        cur_frame = self.current_frame
        self.blockSignals(True)

        us_temperature = []
        ds_temperature = []

        us_temperature_error = []
        ds_temperature_error = []

        for frame_ind in range(self.data_img_file.num_frames):
            self.set_img_frame_number_to(frame_ind)
            self.fit_data()
            us_temperature.append(self.us_temperature)
            ds_temperature.append(self.ds_temperature)

            us_temperature_error.append(self.us_temperature_error)
            ds_temperature_error.append(self.ds_temperature_error)

        self.set_img_frame_number_to(cur_frame)
        self.blockSignals(False)

        return us_temperature, us_temperature_error, ds_temperature, ds_temperature_error


def calculate_real_spectrum(data_spectrum, calibration_spectrum, etalon_spectrum):
    response_y = calibration_spectrum._y / etalon_spectrum._y
    response_y[np.where(response_y == 0)] = np.NaN
    corrected_y = data_spectrum._y / response_y
    corrected_y = corrected_y / np.max(corrected_y) * np.max(data_spectrum._y)
    return Spectrum(data_spectrum._x, corrected_y)


def fit_black_body_function(spectrum):
    try:
        param, cov = curve_fit(black_body_function, spectrum._x, spectrum._y, p0=[2000, 1e-11])
        T = param[0]
        T_err = np.sqrt(cov[0, 0])

        return T, T_err, Spectrum(spectrum._x, black_body_function(spectrum._x, param[0], param[1]))
    except (RuntimeError, TypeError):
        return np.NaN, np.NaN, Spectrum([], [])


def black_body_function(wavelength, temp, scaling):
    wavelength = np.array(wavelength) * 1e-9
    c1 = 3.7418e-16
    c2 = 0.014388
    return scaling * c1 * wavelength ** -5 / (np.exp(c2 / (wavelength * temp)) - 1)


class CalibrationParameter(object):
    def __init__(self, modus=0):
        self.modus = modus
        # modi: 0 - given temperature
        # 1 - etalon spectrum

        self.temperature = 2000
        self.etalon_spectrum_func = None
        self.etalon_file_name = 'Select File...'

    def set_modus(self, modus):
        self.modus = modus

    def set_temperature(self, temperature):
        self.temperature = temperature

    def load_etalon_spectrum(self, filename):
        try:
            data = np.loadtxt(filename, delimiter=',')
        except ValueError:
            try:
                data = np.loadtxt(filename, delimiter=' ')
            except ValueError:
                try:
                    data = np.loadtxt(filename, delimiter=';')
                except ValueError:
                    data = np.loadtxt(filename, delimiter='\t')
        self._etalon_x = data.T[0]
        self._etalon_y = data.T[1]

        self.etalon_file_name = filename

    def get_lamp_y(self, wavelength):
        if self.modus == 0:
            y = black_body_function(wavelength, self.temperature, 1)
            return y / max(y)
        elif self.modus == 1:
            try:
                # return self.etalon_spectrum_func(wavelength)
                # not used because scipy.interpolate is supported by pyinstaller...
                return np.interp(wavelength, self._etalon_x, self._etalon_y)
            except ValueError:
                return np.ones(np.size(wavelength))

    def get_lamp_spectrum(self, wavelength):
        return Spectrum(wavelength, self.get_lamp_y(wavelength))

    def get_etalon_filename(self):
        return self.etalon_file_name

    def set_etalon_filename(self, filename):
        self.etalon_file_name = filename

    def get_etalon_spectrum(self):
        return Spectrum(self._etalon_x, self._etalon_y)

    def set_etalon_function_from_spectrum(self, spectrum):
        try:
            self._etalon_x = spectrum.x
            self._etalon_y = spectrum.y
        except AttributeError:
            pass