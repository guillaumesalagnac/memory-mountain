#!/usr/bin/env python

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import math


def h_speed(speed,pos):
    """convert speed to human-readable form."""
    suffixes=['MB/s','GB/s']
    unit=0
    speed=int(speed)# initially in MB/s
    while speed>1000:
        speed/=1000
        unit+=1
    return str(speed)+suffixes[unit]

def h_size(size,pos):
    """convert size to human-readable form."""
    suffixes=['B','kB','MB','GB']
    unit=0
    size=int(2**size)# initially in bytes
    while size>1024:
        size/=1024
        unit+=1
    return str(size)+suffixes[unit]

fig = plt.figure()
ax = fig.gca(projection='3d')

with open("data.txt") as f:
    data = f.read()

data = data.splitlines()


x = [int(row.split(' ')[1]) for row in data]

y = [int(row.split(' ')[0])  for row in data]
y = np.log2(y)


z = [float(row.split(' ')[2]) for row in data]



ax.plot_trisurf(x,y,z,cmap='rainbow')

ax.set_xlabel('Stride')
ax.set_xlim(0)

ax.set_ylabel('Working set size')
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(h_size))
ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.set_ylim(11)
ax.invert_yaxis()

ax.set_zlabel('Throughput')
ax.zaxis.set_major_formatter(mpl.ticker.FuncFormatter(h_speed))

    # FormatStrFormatter('%d MB/s'))


plt.show()

# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#         linewidth=0, antialiased=False)
# ax.set_zlim(-1.01, 1.01)

# ax.zaxis.set_major_locator(LinearLocator(10))

# fig.colorbar(surf, shrink=0.5, aspect=5)

# plt.show()

