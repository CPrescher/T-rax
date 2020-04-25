# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import versioneer

setup(name='t_rax',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='GPLv3',
      author='Clemens Prescher, Eran Greenberg',
      author_email="clemens.prescher@gmail.com",
      url='https://github.com/erangre/T-rax/',
      install_requires=['numpy', 'scipy', 'qtpy', 'pyqtgraph', 'h5py', 'lmfit', 'pyshortcuts'],
      package_dir={'t_rax': 't_rax'},
      # packages=find_packages(),
      packages=['t_rax', 't_rax.controller', 't_rax.model', 't_rax.model.helper', 't_rax.widget'],
      package_data={'t_rax.widget': ['*.qss', 'icons/*']},
      entry_points = {'console_scripts' : ['run_t_rax = t_rax:run_t_rax']},
      description='GUI program for optical spectroscopy',
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   ],
)
