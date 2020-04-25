# -*- mode: python -*-

block_cipher = None

import os
folder = os.getcwd()

from distutils.sysconfig import get_python_lib

site_packages_path = get_python_lib()
import lib2to3

lib2to3_path = os.path.dirname(lib2to3.__file__)

extra_datas = [
    (os.path.join(lib2to3_path, 'Grammar.txt'), 'lib2to3/'),
    (os.path.join(lib2to3_path, 'PatternGrammar.txt'), 'lib2to3/'),
]


a = Analysis(['run_t_rax.py'],
             pathex=[folder],
             datas=extra_datas,
             hiddenimports=['scipy.special._ufuncs_cxx', 'scipy.integrate', 'scipy.integrate.quadrature',
                            'scipy.integrate.odepack', 'scipy.integrate._odepack', 'scipy.integrate._ode',
                            'scipy.integrate.quadpack', 'scipy.integrate._quadpack',
                            'scipy.integrate.vode', 'scipy.integrate._dop', 'scipy.integrate.lsoda',
                            'h5py.h5ac', 'h5py.defs', 'h5py.utils', 'h5py._proxy', 'pkg_resources.py2_warn',
                            'pywt._extensions._cwt'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4', 'PySide'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

## extra files for getting things to work
a.datas += [('t_rax/widget/TRaxStyle.qss', 't_rax/widget/TRaxStyle.qss', 'DATA')]
a.datas += [('t_rax/widget/NavigationStyle.qss', 't_rax/widget/NavigationStyle.qss', 'DATA')]
a.datas += [('t_rax/widget/stylesheet.qss', 't_rax/widget/stylesheet.qss', 'DATA')]


from sys import platform as _platform

platform = ''

if _platform == "linux" or _platform == "linux2":
    platform = "Linux64"
    name = "T-Rax"
elif _platform == "win32" or _platform == "cygwin":
    platform = "Win64"
    name = "T-Rax.exe"
elif _platform == "darwin":
    platform = "Mac64"
    name = "run_t_rax"

# getting the current version of Dioptas
# __version__ file for executable has prevalence over versioneer output
try:
    with open(os.path.join('dioptas', '__version__'), 'r') as fp:
        __version__ = fp.readline()
except FileNotFoundError:
    from t_rax import __version__


pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=name,
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon="t_rax/widget/icons/t_rax.ico")


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='T-Rax_{}_{}'.format(platform, __version__))

if _platform == "darwin":
    app = BUNDLE(coll,
                 name='T-Rax_{}.app'.format(__version__),
                 icon='t_rax/widget/icons/t_rax.icns')
