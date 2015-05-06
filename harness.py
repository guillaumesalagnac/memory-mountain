#!/usr/bin/env python

# note that this script is written for python2, but it should be
# straightforward to port it to python3

import numpy as np

import subprocess

# repeat execution for this number of times, and only keep the median
# value. (simplistic way to reduce noise)
count = 20

for mag in range(10,27): # from 2^10 (1kB) to 2^27 (64MB)
    size = 2**mag
    for stride in range(1,30,2):

        results=[]
        for repeat in range(count):
            log=subprocess.check_output(["./benchmark",
                                         str(size),
                                         str(stride)]);

            for l in log.splitlines():
                if "MB/s" in l:
                    results.append( float(l[ l.find('=')+1: l.find('MB/s') ]) ) 

        print size,stride,np.median(results)
