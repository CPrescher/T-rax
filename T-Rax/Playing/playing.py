import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

cdict = {
  'red'  :  ( (0.0, 1.0, 1.0),
              (0.5, 0.0, 0.0), 
              (1.0, 1.0, 1.0)),
  'green':  ( (0.0, 1.0, 1.0), 
              (0.5, 1.0, 1.0),
              (1.0, 0.0, 0.0)),
  'blue' :  ( (0.0, 0.0, 0.0), 
              (0.5, 0.0, 0.0),
              (1.0, 0.0, 0.0))
}
cmap = mpl.colors.LinearSegmentedColormap('test', cdict)
#cmap = mpl.colors.ListedColormap([(1,0,0),(1,1,0)])
x=np.linspace(0,256,256)
y=np.zeros(np.size(x))
colors=cmap(x/256.0)
print colors
plt.scatter(x,y, s=50, color=colors)
plt.show()


