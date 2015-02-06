# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from wx.lib.pubsub import pub
from model.RoiData import RoiData
from .TemperatureData import ExpDataFromImgData

class TemperatureSettings():
    def __init__(self, data):
        try:
            us_calibration_filename_str = data.get_us_calibration_data().filename
        except AttributeError:
            us_calibration_filename_str = 'Select File...'

        try:
            ds_calibration_filename_str = data.get_ds_calibration_data().filename
        except AttributeError:
            ds_calibration_filename_str = 'Select File...'

        self.ds_calib_file_name = ds_calibration_filename_str
        self.us_calib_file_name = us_calibration_filename_str

        self.ds_etalon_file_name = data.get_ds_calibration_parameter().get_etalon_filename()

        try:
            self.ds_etalon_spectrum = data.ds_calibration_parameter.get_etalon_spectrum()
        except AttributeError:
            self.ds_etalon_spectrum = []

        self.us_etalon_file_name = data.get_us_calibration_parameter().get_etalon_filename()

        try:
            self.us_etalon_spectrum = data.us_calibration_parameter.get_etalon_spectrum()
        except AttributeError:
            self.us_etalon_spectrum = []

        self.ds_calibration_modus = data.get_ds_calibration_parameter().modus
        self.us_calibration_modus = data.get_us_calibration_parameter().modus

        self.ds_calibration_temperature = data.get_ds_calibration_parameter().temp
        self.us_calibration_temperature = data.get_us_calibration_parameter().temp

        self.ds_roi = data.get_roi_data().get_ds_roi()
        self.us_roi = data.get_roi_data().get_us_roi()

        if not data.ds_calibration_data is None:
            try:
                self.ds_img_data = data.ds_calibration_data.get_img_data()
            except:
                self.ds_calibration_spectrum = data.ds_calibration_data.img_data
            self.ds_x_calibration = data.ds_calibration_data.x_whole

        if not data.us_calibration_data is None:
            try:
                self.us_img_data = data.us_calibration_data.get_img_data()
            except:
                self.us_calibration_spectrum = data.us_calibration_data.img_data
            self.us_x_calibration = data.us_calibration_data.x_whole
        self.img_dimension = data.exp_data.get_img_dimension()

    @staticmethod
    def load_settings(settings, data):
        data.roi_data_manager._add(settings.img_dimension, RoiData(settings.ds_roi, settings.us_roi))
        data.roi_data = data.roi_data_manager.get_roi_data(data.exp_data.get_img_dimension())
        data.exp_data.roi_data = data.roi_data

        if not settings.ds_calib_file_name == 'Select File...':
            data.ds_calibration_data = ExpDataFromImgData(settings.ds_img_data, settings.ds_calib_file_name,
                                                          settings.ds_x_calibration, data.roi_data_manager)
        else:
            data.ds_calibration_data = None

        if not settings.us_calib_file_name == 'Select File...':
            data.us_calibration_data = ExpDataFromImgData(settings.us_img_data, settings.us_calib_file_name,
                                                          settings.us_x_calibration, data.roi_data_manager)
        else:
            data.us_calibration_data = None

        data.ds_calibration_parameter.set_etalon_filename(settings.ds_etalon_file_name)
        data.us_calibration_parameter.set_etalon_filename(settings.us_etalon_file_name)
        data.ds_calibration_parameter.set_etalon_spectrum(settings.ds_etalon_spectrum)
        data.us_calibration_parameter.set_etalon_spectrum(settings.us_etalon_spectrum)

        data.get_ds_calibration_parameter().set_modus(settings.ds_calibration_modus, False)
        data.get_us_calibration_parameter().set_modus(settings.us_calibration_modus, False)
        data.get_ds_calibration_parameter().set_temperature(settings.ds_calibration_temperature, False)
        data.get_us_calibration_parameter().set_temperature(settings.us_calibration_temperature, False)
        data.calculate_spectra()
        pub.sendMessage("EXP DATA CHANGED")
