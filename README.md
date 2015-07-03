T-Rax
===

A python GUI program for fast visual analysis of spectroscopic data collected mostly during high pressure diamond anvil 
cell experiments.

I includes separate modules for temperature fitting, pressure estimation using ruby peak or the diamond edge and a 
general module for Raman spectroscopy.
 
Currently, the only input files allowed are Princeton Instruments \*.spe file saved either from WinSpec (File Version 2) 
or Lightfield (File Version 3).

Maintainer
===

Clemens Prescher (clemens.prescher@gmail.com)
Center for Advanced Radiation Sources, University of Chicago


Requirements
===

- Python 2.7
- PyQt4
- numpy
- scipy
- pyqtgraph
- dateutils
- lmfit
- h5py
    
Installation
===

Except for PyQt4, all of those packages can be easily installed using "pip" as python package manager. If you are on 
Windows or Mac, please try to install PyQt4 by using a precompiled python distribution such as anaconda, enthought, 
winpython or Python(x,y). On Linux PyQt usually can be easily installed using the packagemanager.

Using the minimum anaconda distribution, you have to only type the following two commands:

    conda install pyqt numpy scipy h5py
    pip install pyqtgraph dateutils lmfit
    
The program itself can then be run by going into the "t-rax" directory and type:
    
    python T-Rax.py








    

