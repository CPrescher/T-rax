from distutils.core import setup
import py2exe
import matplotlib

setup(data_files = matplotlib.get_py2exe_datafiles(),
      windows = ['run_T-Rax.py'],
      options = {'py2exe': {'includes': ["wx.lib.pubsub.*", "wx.lib.pubsub.core.*", 
                           "wx.lib.pubsub.core.kwargs.*"]}})
