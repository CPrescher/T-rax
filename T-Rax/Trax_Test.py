import unittest
import T_Rax_Controller as TRC
import wx

class Trax_Test(unittest.TestCase):
    def setUp(self):
        app=wx.App(None)

    def test_data_loading(self):
        TRC.TraxMainViewController()
        app.MainLoop()

if __name__ == '__main__':
    unittest.main()
