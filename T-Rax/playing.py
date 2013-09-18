import numpy as np
import random
import matplotlib.pyplot as plt
from T_Rax_Data import black_body_function, gauss_curve_function

x=np.linspace(500,900,1300)
y=np.linspace(0,101, 100)

X,Y = np.meshgrid(x,y)

Z=np.ones((len(y),len(x)))

random.seed()
T1=random.randrange(1700,3000,1)
T2=T1+ random.randrange(-200,200,1)

black1 = black_body_function(x,T1,1)
gauss1 = gauss_curve_function(y,1,80,3)
black2 = black_body_function(x,T2,1)
gauss2 = gauss_curve_function(y,1,15,3)

for x_ind in xrange(len(x)):
    for y_ind in xrange(len(y)):
        Z[y_ind,x_ind] = black1[x_ind]*gauss1[y_ind] +black2[x_ind]*gauss2[y_ind]
Z+=np.random.normal(0,.03*max(black1),(len(y),len(x)))
plt.figure()
Z=Z[50:-1,:]
print np.sum(Z, 1)
img = plt.imshow(Z, cmap = 'hot', aspect = 'auto')
img.autoscale()
plt.show()
