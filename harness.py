#!/usr/bin/env python

# note that this script is written for python2, but it should be
# straightforward to port it to python3

import subprocess

for mag in range(11,27): # from 2^11 (2kB) to 2^27 (64MB)
    size = 2**mag
    for stride in range(1,30,2):

        log=subprocess.check_output(["./benchmark",
                                     str(size),
                                     str(stride)]);

        for l in log.splitlines():
            if "MB/s" in l:
                print size,stride,float(l[ l.find('=')+1: l.find('MB/s') ])
