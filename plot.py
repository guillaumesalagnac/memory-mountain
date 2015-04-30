#!/usr/bin/env python

# note that this script is written for python2, but it should be
# straightforward to port it to python3

from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt
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
        size/=1000
        unit+=1
    return str(size)+suffixes[unit]

fig = plt.figure()
ax = fig.gca(projection='3d')


if len(sys.argv)==2:
    with open(sys.argv[1]) as f:
        data = f.read()
else:
    print "usage: plot.py DATAFILE"
    sys.exit(1)
    
data = data.splitlines()

# stride
x = [int(row.split(' ')[1]) for row in data]

# working set size
y = [int(row.split(' ')[0])  for row in data]
y = np.log2(y) # we cheat to get a logarithmic Y axis

# throughput
z = [float(row.split(' ')[2]) for row in data]
 
ax.plot_trisurf(x,y,z,cmap='rainbow')

ax.set_xlabel('Stride')
ax.set_xlim(0)

ax.set_ylabel('Working set size')
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_size))
ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.set_ylim(11)
ax.invert_yaxis()

ax.set_zlabel('Throughput')
ax.zaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_speed))

plt.show()
