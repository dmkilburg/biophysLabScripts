#!/usr/bi/python

"""
This is a quick script to load the current directory's lig.dms files in time
order to vmd. 

"""

import os
import re
import sys



def main():
    directory = os.getcwd()
    name = sys.argv[1]
    num_cycles = sys.argv[2]

    command = 'vmd -f '

    for i in range(1,int(num_cycles)):
        dms_file = directory + '/' + name + '_lig_' + str(i) + '.dms' + ' '
        command += dms_file

    os.system(command)

    return

if __name__ == "__main__":
    main()
