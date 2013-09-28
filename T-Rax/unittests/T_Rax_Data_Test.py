import unittest
from T_Rax_Data import TraxData, ROI, ROIData,ROIDataManager

class Test_T_Rax_Data_Test(unittest.TestCase):
    def test_ROI_data_manager(self):
        self.roi_data_manager = ROIDataManager()
        dimensions = [[100,1000],
                      [100,500],
                      [ 10,300]]
        rois = [ROIData([10,20,100,850], [70,80,100,850]),
                ROIData([10,20,100,850], [70,80,100,850]),
                ROIData([10,20,100,850], [70,80,100,850])]
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
                         [[100,900,80,90], [100,900,10,20]])


if __name__ == '__main__':
    unittest.main()
