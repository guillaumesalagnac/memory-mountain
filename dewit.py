#!/usr/bin/python

import subprocess


for mag in range(11,27):
    size = 2**mag
    # for stride in range(1,50,2):
    for stride in range(1,30,4):

        log=subprocess.check_output(["./one",
                                     str(size),
                                     str(stride)]);

        for l in log.splitlines():
            if "MB/s" in l:
                print size,stride,float(l[ l.find('=')+1: l.find('MB/s') ])
