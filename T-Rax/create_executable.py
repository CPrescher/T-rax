from distutils.core import setup
import py2exe, sys
import matplotlib
import matplotlib.backends.backend_qt4agg

sys.argv.append('py2exe')


setup(data_files = matplotlib.get_py2exe_datafiles(),
      windows = ['run_T-Rax.py'],
      options = {'py2exe': {'includes': ["wx.lib.pubsub.*", "wx.lib.pubsub.core.*", 
                           "wx.lib.pubsub.core.kwargs.*", "matplotlib.backends.backend_tkagg"],
                          'packages' :  ['matplotlib', 'pytz'],
                          'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                         'libgobject-2.0-0.dll',
                                         'libgdk_pixbuf-2.0-0.dll',
                                         'libgtk-win32-2.0-0.dll',
                                         'libglib-2.0-0.dll',
                                         'libcairo-2.dll',
                                         'libpango-1.0-0.dll',
                                         'libpangowin32-1.0-0.dll',
                                         'libpangocairo-1.0-0.dll',
                                         'libglade-2.0-0.dll',
                                         'libgmodule-2.0-0.dll',
                                         'libgthread-2.0-0.dll',
                                        ]}})