# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:10:42 2020

@author: stras
"""

import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


xyz=np.array([[1,0,0],
             [0,-2,0],
             [0,2,0],
             [1,0,1],
             [0,-2,1],
             [0,2,1],
             [1,0,2],
             [0,-2,2],
             [0,2,2]])

X= xyz[:,0]
Y= xyz[:,1]
Z= xyz[:,2]*100


ploty,plotz, = np.meshgrid(np.linspace(np.min(Y),np.max(Y),10),\
                           np.linspace(np.min(Z),np.max(Z),10))
plotx = interp.griddata((Y,Z),X,(ploty,plotz),method='linear')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(plotx,ploty,plotz,cstride=1,rstride=1,cmap='viridis')  # or 'hot'

fig = plt.figure(5)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z)
plt.show()

zVal = 150
yVal = 1
xInterp = interp.griddata((Y,Z),X,(yVal,zVal),method='linear')

print(xInterp)


