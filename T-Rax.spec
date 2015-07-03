# -*- mode: python -*-
folder = 't-rax'

a = Analysis([os.path.join(folder, 't-rax.py')],
             pathex=[folder],
             hiddenimports=['scipy.special._ufuncs_cxx', 'scipy.integrate', 'scipy.integrate.quadrature',
                            'scipy.integrate.odepack', 'scipy.integrate._odepack', 'scipy.integrate._ode',
                            'scipy.integrate.quadpack', 'scipy.integrate._quadpack',
                            'scipy.integrate.vode', 'scipy.integrate._dop', 'scipy.integrate.lsoda',
                            'h5py.h5ac'],
             hookspath=None,
             runtime_hooks=None)

## extra files for getting things to work
a.datas += [('widget/TRaxStyle.qss', 't-rax/widget/TRaxStyle.qss', 'DATA')]
a.datas += [('widget/NavigationStyle.qss', 't-rax/widget/NavigationStyle.qss', 'DATA')]


pyz = PYZ(a.pure)

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
    name = "T-Rax"

import sys
sys.path.append(a.pathex[0])

from controller.MainController import get_version
version = get_version()

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=name,
          debug=False,
          strip=None,
          upx=True,
          console=False)


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='T-Rax_{}_{}'.format(platform, version))

if _platform == "darwin":
    app = BUNDLE(coll,
                 name='T-Rax_{}.app'.format(version))
