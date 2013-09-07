import T_Rax_Data as TRData
import T_Rax_View as TRView
import wx

class TraxMainViewController(object):
    def __init__(self):
        self.data=TRData.TraxData()
        self.view=TRView.TraxMainWindow(self)


if __name__=="__main__":
    app=wx.App(None)
    TraxMainViewController()
    app.MainLoop()

