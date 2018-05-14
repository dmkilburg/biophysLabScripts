#!/usr/bin/python

"""
sorts the cycles in uwham_energy.dat files

"""

import sys

infile = "uwham_energy.dat"
column = sys.argv[1]
temp = sys.argv[2]

points = {}
    

with open(infile,'r') as f:
    for line in f:
        row = line.split()
        if int(column) == 1:
            cycle = int(row[0])

        if int(column) == 2:
            cycle = int(row[1])
        if row[2] == temp:
            if row[4]:
                energy = row[3] + " " + row[4]
            else:
                energy = row[3]
            points[cycle] = energy

output = "sorted_%s_%s" % (temp,infile)

with open(output,'w') as out:
    for key in sorted(points):
        print_line = "%s %s \n" % (key, points[key])
        out.write(print_line)
