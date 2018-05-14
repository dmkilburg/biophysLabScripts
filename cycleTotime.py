#!/usr/bin/python

import sys

infile = sys.argv[1]
outfile = sys.argv[2]
cyctime = int(sys.argv[3]) ## Number of ps/cycle


with open(outfile,'w') as out:
    with open(infile,'r') as f:
        for line in f:
            row = line.split()
            time_ns = int(row[0]) * cyctime/1000.0
            out.write("%s %s %s \n" % (time_ns, row[1],row[2]))
        
