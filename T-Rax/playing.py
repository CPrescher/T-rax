#!/usr/bin/env python
from pylab import *
import numpy as np
try:
    from PIL import Image
except ImportError, exc:
    raise SystemExit("PIL must be installed to run this example")

import matplotlib.cbook as cbook

datafile = cbook.get_sample_data('lena.jpg')
lena = Image.open(datafile)
dpi = rcParams['figure.dpi']
figsize = lena.size[0]/dpi, lena.size[1]/dpi

x=np.ones((10,10))*5

figure(figsize=figsize)
ax = axes([0,0,1,1], frameon=False)
#ax.set_axis_off()
ax.set_xlim(0,6)
ax.set_ylim(0,6)
#im = imshow(lena, origin='lower',extent=[-2,4,-2,4])  # axes zoom in on portion of image
im2 = imshow(x, origin='lower',extent=[0,2,0,2], cmap='hot') # image is a small inset on axes

show()