import unittest
from T_Rax_Data import TraxData, ROI, ROIData,ROIDataManager

class Test_T_Rax_Data_Test(unittest.TestCase):
    def test_ROI_data_manager(self):
        self.roi_data_manager = ROIDataManager()
        dimensions = [[100,1000],
                      [100,500],
                      [ 10,300]]
        rois = [ROIData(None,[10,20,100,850], [70,80,100,850]),
                ROIData(None,[10,20,100,850], [70,80,100,850]),
                ROIData(None,[10,20,100,850], [70,80,100,850])]

if __name__ == '__main__':
    unittest.main()
