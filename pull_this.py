#!/bin/usr/python

"""
A short script used to pull certain data from repl.cycle. ... dat" file

Usage: pull_this.py data_file [-c][-l][-t][-r] 

-l : pull data by lambda value
-c : pull data by cycle 
-t : pull data by temperature
-r : pull data by replica

"""


import sys
import argparse


def pull_replicas(data,num):
    for i in range(num+1):
        output = "r%s.dat" % i
        with open(data,'r') as f:
            for line in f:
                row = line.split()
                if int(row[0]) == i:
                    with open(output,'a') as out:
                        out.write(line)
                elif int(row[0]) > i:
                    break
            
    return


def pull_lambda(data,t_lambda):

    output = "lambda_%s.dat" % t_lambda
    epsilon = .00001
    sigma = 0
    count = 0
    with open(output,'w') as out:
        with open(data,'r') as f:
            for line in f:
                row = line.split()
                lambda_val = float(row[5])
                ebind = float(row[6])
                if lambda_val >= (t_lambda - epsilon) and lambda_val <= (t_lambda + epsilon):
                    out.write(line)
                    sigma += ebind
                    count += 1
    avg_ebind = sigma/count
    print "Average ebind = ", avg_ebind
    return


def pull_temp(data,temp):

    output = "%s_data.dat" % temp
    with open(output, 'w') as out:
        with open(data,'r') as f:
            for line in f:
                row = line.split()
                line_temp = float(row[4])
                line_temp = int(line_temp)
                if line_temp == int(temp):
                    out.write(line)

    return

def get_outfiles(table,cycle):
    outfile_list = []
    for row in table:
        if cycle >= row[0] and cycle <= row[1]:
            outfile_list.append(row[2])
        
    return outfile_list

def pull_cycles(data,sort_type,start,step,term_cycle):
    
    table = []
    for i in range(start,term_cycle,step):
        if sort_type == 1:
            outfile = "c%s_c%s.dat" % (i,i+step)
            table.append([i,i+step,outfile])
            
        if sort_type == 2:
            outfile = "c%s_c%s.dat" % (start,i+step)
            table.append([start,i+step,outfile])

        if sort_type == 3:
            outfile = "c%s_c%s.dat" % (i,term_cycle)
            table.append([i,term_cycle,outfile])

    with open(data,'r') as f:
        for line in f:
            row = line.split()
            cycle = int(row[1])
            out_files = get_outfiles(table,cycle)
            for entry in out_files:
                with open(entry,'a') as out:
                    out.write(line)

    return



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', action='store', help='input file name')
    parser.add_argument('-c', action='store_true',dest='cycle',default=False,
                        help='option to pull cycles')
    parser.add_argument('-r',action='store_true',dest='replica',default=False,
                        help='option to pull replicas')
    parser.add_argument('-t',action='store_true',dest='temp',default=False,
                        help='option to select temperature')
    parser.add_argument('-l',action='store_true',dest='lamb',default=False,
                        help='option to select by lambda value')
    options = parser.parse_args()


    if options.cycle:
        sort_options,start,step,term_cycle = raw_input('Enter sort option: (1:block,2:forward,3:backward) start, step and cutoff_cycle ').split()
        sort_options = int(sort_options)
        step = int(step)
        term_cycle = int(term_cycle)
        start = int(start)
        if sort_options == 1 or sort_options == 2 or sort_options == 3:
            pull_cycles(options.infile,sort_options,start,step,term_cycle)
        else:
            print "No such option."
            sys.exit(1)


    if options.replica:
        num_replicas = raw_input('Enter number of replicas: ')
        pull_replicas(options.infile,int(num_replicas))


    if options.temp:
        target_temp = raw_input('Enter temperature: ')
        pull_temp(options.infile,target_temp)

    if options.lamb:
        target_lambda = raw_input('Enter lambda: ')
        pull_lambda(options.infile,float(target_lambda))

    if options.cycle == False and options.replica == False and options.temp == False and options.lamb == False:
        print "You need to choose at least one option. Use -h or --help for usage options"
        sys.exit(1)

    return

    

if __name__ == "__main__":
    main()
