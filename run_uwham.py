#!/usr/bin/python

""" 
Little thingy that calls uwham_analysis.R on a data set and poops out dgbind values.


"""

import os
import sys
import re





def get_files(directory):
    
    file_list = []
    for entry in os.listdir(directory):
        m = re.match("^c[0-9]+_c[0-9]+\.dat",entry)
        if m != None:
            file_list.append(entry)

    return file_list


def print_data(num_temps,start,end,temps,dgbinds,error):
    with open("uwham_energy.dat",'a')as out:
        
        for i in range(num_temps):
            energy_line = "%s %s %s %s %s \n" % (start,end,temps[i],dgbinds[i],error)
            out.write(energy_line)
    return


def run_uwham_and_extract(file_list,num_temp):
    dgbind_list = []
    for entry in file_list:
        m = re.match("^c([0-9]+)_c([0-9]+)\.dat",entry)
        q = m.groups()
        cyc_start = q[0]
        cyc_end = q[1]
        
        first_line = "uwham for cycles %s to %s" % (q[0],q[1])
        with open("tmp_data.dat",'w') as out:
            with open(entry,'r') as f:
                for line in f:
                    out.write(line)
        with open("data_uwham.dat",'w') as datfile:
            datfile.write(first_line)

        os.system("R < uwham_analysis.R --no-save >> data_uwham.dat 2>&1")
        string = "^c[(]"
        with open("data_uwham.dat",'r') as infile:
            string = "^c[(]"
            dgbind_list = []
            has_error = False
            for line in infile:
                string = "^c[(]"
                if line.startswith("> tempt <-"):
                    row = line.split()
                    for i in range(num_temp):
                        string += "([0-9]+)\,"
                    string = string[:-2] + "[)]"
                    
                    n = re.match(string,row[3])
                    
                    temps = n.groups()
                if line.startswith("> sqrt(out$ve)/bet"):
                    nxt_line = infile.next()
                    while not nxt_line.startswith("> "):
                        print nxt_line
                        if nxt_line.startswith("Warning "):
                            break
                        row = nxt_line.split()
                        std_dev = row
                        nxt_line = infile.next()
                    error = std_dev.pop()
                    
                if line.startswith("> #DGbind as a function "):
                    line1 = infile.next()
                    data_line = infile.next()
                    
                    column = data_line.split()
                    for i in range(1,num_temp+1):
                        dgbind_list.append(column[i])
    
                if line.startswith("Error"):
                    has_error = True
                    break
        if has_error:
            pass
        else:
            print_data(num_temp,cyc_start,cyc_end,temps,dgbind_list,error)
                
                        
    return

################### MAIN ######################

 
def main():
    num_temp = int(sys.argv[1])
    directory = os.getcwd()
    file_list = get_files(directory)
    run_uwham_and_extract(file_list,num_temp)


    return



if __name__ == "__main__":
    main()
