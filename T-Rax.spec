# -*- mode: python -*-


import os
import lib2to3


block_cipher = None
folder = os.getcwd()

lib2to3_path = os.path.dirname(lib2to3.__file__)

extra_datas = [
    ("t_rax/resources", "t_rax/resources"),
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

from t_rax import icons_path

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
          icon=os.path.join(icons_path, "t_rax.ico"))


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
                 icon=os.path.join(icons_path, "t_rax.icns"))
