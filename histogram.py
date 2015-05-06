#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import subprocess
import sys

data=[]


if len(sys.argv) == 3:
    size=int(sys.argv[1])
    stride=int(sys.argv[2])
    runcount=500
elif len(sys.argv) == 4:
    size=int(sys.argv[1])
    stride=int(sys.argv[2])
    runcount=int(sys.argv[3])
else:
    print "usage: %s SIZE STRIDE [COUNT]" % sys.argv[0]
    print "run the benchmark COUNT times (default 500), and display the results as an histogram"
    sys.exit(1)

for i in range(runcount):
    log=subprocess.check_output(["./benchmark",
                                     str(size),
                                     str(stride)]);

    for l in log.splitlines():
        if "MB/s" in l:
            print l
            data.append( float(l[ l.find('=')+1: l.find('MB/s') ]) )

plt.hist(data)
plt.xlabel("Throughput (MB/s)");
plt.ylabel("Count (out of %d)" % runcount);

plt.title("Benchmark was run %d times.\n Throughput (MB/s) min=%.1f, max=%.1f, med=%.1f, avg=%.1f" % (
    runcount, min(data),max(data),np.median(data),np.average(data) ) )

print '%d runs with size %d, stride %d -> median throughput = %.1f MB/s' % (runcount, size, stride, np.median(data))
print 'min=%.1f, max=%.1f, med=%.1f, avg=%.1f' % (min(data),max(data),np.median(data),np.average(data))


plt.show()


