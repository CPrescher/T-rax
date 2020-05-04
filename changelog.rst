Version 1.4.1 (04.05.2020)
--------------------------
    - fixed bug for loading unspecified SPE files (xml_offset is negative for some reason)
    - zooming out with a single right click in a graph or image widget is now working correctly

Version 1.4
-----------
    - fixed a bug for spe files with collected in LineSensor mode (spectroscopy mode)

Version 1.3
-----------
    - fixed a bug for spe files with asian characters inside the xml description

Version 1.2
-----------
    - temperature mode 'save data' files are now saved separately for upstream (us) and downstream (ds), to also
      enable saving for different sized region of interests
    - fitted temperatures are now automatically saved in a T_log.txt file inside the folder of the data file
    - it is now possible to batch fit many spe files, the output will be saved in the above mentioned log-file
    - in Raman mode overlays can be used for comparison of different measurements
    - in Raman Mode the current mouse pointer position is now displayed in nm an cm^-1

Version 1.1
-----------
    - fixed automatic file loading
    - inverted y axes for images in the ROI window
    - automatic ruby fitting

Version 1.0
-----------
    - complete rewrite of the program, now using a different graphics library

Version 0.2032
--------------
    - fixed a bug which was causing errors when loading calibration files and changing the calibration methods

Version 0.2031
--------------
    - added a right click option in the Temperature ROI view, it will reset the values to the initial start values
    being 0.05 and 0.95

Version 0.203
-------------
    - remade the next file algorithm, to now also handle files without using an underscore as separation

Version 0.202
-------------
    - added an intensity histogram to the temperature roiview
    - with this it is now possible to manipulate the vmin and vmax of the image

Version 0.201
-------------
    - diamond modus 'derivative' is now called options
    - diamond modus 'options' now has an extra text field for changing the laser wavelength
    - fixed a bug in the diamond roiview which was causing the x-axis labels to be clumped on the left side