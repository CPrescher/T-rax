import unittest
from T_Rax_Data import TraxData, ROI, ROIData,ROIDataManager

class Test_T_Rax_Data_Test(unittest.TestCase):
    def test_ROI_data_manager(self):
        self.roi_data_manager = ROIDataManager()
        dimensions = [[100,1000],
                      [100,500],
                      [ 10,300]]
        rois = [ROIData([100,850,10,20], [100,850,70,80]),
                ROIData([100,850,10,20], [100,850,70,80]),
                ROIData([100,850,10,20], [100,850,70,80])]
        for ind in range(len(dimensions)):
            self.roi_data_manager._add(dimensions[ind], rois[ind])
        
        self.assertEqual(self.roi_data_manager._get_dimension_ind(dimensions[2]),2)
        self.assertEqual(self.roi_data_manager._get_dimension_ind(dimensions[1]),1)

        self.assertEqual(self.roi_data_manager.get_roi_data(dimensions[2]).get_roi_data(),
                         rois[2].get_roi_data())

        self.assertTrue(self.roi_data_manager._exists(dimensions[0]))
        self.assertTrue(self.roi_data_manager._exists(dimensions[1]))
        self.assertTrue(self.roi_data_manager._exists(dimensions[2]))
        self.assertFalse(self.roi_data_manager._exists([20,400]))

        self.roi_data_manager.get_roi_data([1001,101])
        self.assertTrue(self.roi_data_manager._exists([1001,101]))
        self.assertEqual(self.roi_data_manager.get_roi_data([1001,101]).get_roi_data(),
                         [[250,750,80,90], [250,750,10,20]])

        self.roi_data_manager._add([1001,101],ROIData([100,1000,10,20],[234,789,12,34]))
        self.assertEqual(self.roi_data_manager.get_roi_data([1001,101]).get_roi_data(),
                         [[100,1000,10,20],[234,789,12,34]])

    def test_settings(self):
        data=TraxData()
        data.roi_data.ds_roi.set_roi([100,500,10,20])
        data.roi_data.us_roi.set_roi([100,500,80,90])
        initial_settings = data.get_settings()
        self.assertEqual(initial_settings.ds_calibration_temperature,2000)
        self.assertEqual(initial_settings.us_calibration_temperature,2000)
        self.assertEqual(initial_settings.ds_calib_file_name, 'Select File...')
        self.assertEqual(initial_settings.us_calib_file_name, 'Select File...')
        self.assertEqual(initial_settings.ds_etalon_file_name, '15A_lamp.txt')
        self.assertEqual(initial_settings.us_etalon_file_name, '15A_lamp.txt')
        self.assertEqual(initial_settings.ds_calibration_modus,1)
        self.assertEqual(initial_settings.us_calibration_modus,1)
        self.assertEqual(initial_settings.ds_roi, [100,500,10,20])
        self.assertEqual(initial_settings.us_roi, [100,500,80,90])

        data.load_ds_calib_data('unittests/unittest files/dn_15.SPE')
        data.load_us_calib_data('unittests/unittest files/up_15.SPE')
        data.load_exp_data('unittests/unittest files/SPE_v2_PIXIS.SPE')
        data.set_ds_calib_temp(1500)
        data.set_ds_calib_modus(0)
        calib_settings = data.get_settings()
        
        self.assertEqual(calib_settings.ds_calib_file_name, 'unittests/unittest files/dn_15.SPE')
        self.assertEqual(calib_settings.us_calib_file_name, 'unittests/unittest files/up_15.SPE')

        data.load_settings(initial_settings)
        self.assertEqual(data.get_ds_calib_temperature(),2000)
        self.assertNotEqual(data.get_ds_roi, [100,500,10,20])
        self.assertNotEqual(data.get_us_roi, [100,500,80,90])
        



if __name__ == '__main__':
    unittest.main()
