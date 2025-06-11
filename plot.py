#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import math
import sys

def pretty_speed(speed,pos):
    """convert speed to human-readable form.
'speed' is given in bytes.
'pos' is a dummy parameter, required by matplotlib's FuncFormatter.
    """
    suffixes=['MB/s','GB/s']
    unit=0
    speed=int(speed)# initially in MB/s
    while speed>1000:
        speed/=1000. # 1000 or 1024 ? cf pretty.c
        unit+=1
    # only keep the decimal part when there is one !
    string=str(speed)
    if string[-2:] == ".0":
        string=string[:-2]
    return string+suffixes[unit]

def pretty_size(logsize,pos):
    """convert size to human-readable form.
'logsize' is the log of the size we want to represent.
'pos' is a dummy parameter, required by matplotlib's FuncFormatter.
"""
    
    suffixes=['B','kB','MB','GB']
    unit=0
    size=int(2**logsize)# now in bytes
    while size>1000:
        size//=1000
        unit+=1
    return str(size)+suffixes[unit]

if len(sys.argv)==2:
    with open(sys.argv[1]) as f:
        data = f.read()
else:
    print("usage: plot.py DATAFILE")
    sys.exit(1)
    
data = data.splitlines()

# stride
x = [int(row.split(' ')[1]) for row in data]

# working set size
y = [int(row.split(' ')[0])  for row in data]
y = np.log2(y) # we cheat to get a logarithmic Y axis

# throughput
z = [float(row.split(' ')[2]) for row in data]

# plot setup
fig=plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # reduce whitespace margins around plot (I hope?)
ax =fig.add_subplot(projection='3d')
ax.invert_yaxis()

ax.plot_trisurf(x,y,z,cmap='rainbow',edgecolors='black')

xlim=ax.get_xlim()
if xlim[0] > xlim[1]:
    ax.view_init(elev=15,azim=130)
else:
    ax.view_init(elev=15,azim=-50)
        
ax.set_xlabel('Stride (bytes)')
# ax.set_xlim(right=0) # seems to be useless nowadays ?!?

ax.set_ylabel('Working set size')
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_size))

ax.set_zlabel('Throughput',labelpad=20)
ax.tick_params(axis='z', pad=10) # 
ax.zaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_speed))
plt.show()
