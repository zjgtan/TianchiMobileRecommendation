import sys
import re

path = sys.argv[1]

fd = open(path + "/data", "w")

for ix, line in enumerate(sys.stdin):
    if ix == 0: continue
    print >> fd, line.rstrip()
 
