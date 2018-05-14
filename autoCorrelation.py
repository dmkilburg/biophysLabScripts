#!/usr/bin/python

"""
Function that computes the autocorrelation function :

  C_t = (<x_n*x_n+t> - <x_n>)/(<x_n^2> - <x_n>^2)

This assumes that the data is a timeseries.

Input data should be in 2 columns, col 1 = time, col 2 = energy_data

It also follows the simplification that stops the computation if the C_t < 0 from 
J. Chem Theory Comput, 3,1 2007 by Chodera et al.

Usage: autoCorrelation.py infile outfile

"""

import sys
import math
from stats import Array
import numpy as np

class System(object):

    def __init__(self,data_lists):

        self.data_lists = [Array(x) for x in data_lists]
        self.m = len(data_lists)
        self.N = Array([x.n for x in self.data_lists]) # lists of lengths for each list



    def cum_mean(self):
        return sum([x.mean() for x in self.data_lists])/self.N.mean() # sum of the means 
    

    def minus(self,mu):
        return [x.minus_constant(mu) for x in self.data_lists] # returns data list with mu sub
        
    def cum_variance(self):
        return sum([x.squared() for x in self.data_lists])
    
def auto_correlation(flucts,N_k,N,sigma2,Navg,K):

    Ct = []
    g = 1.0
    t = 1

    while (t < N_k.max() - 1):
        numerator = 0.0
        denom = 0.0
        
        for k in range(K):
            if (t >= N_k.data[k]):
                continue
            dx_n = flucts.data_lists[k]
            y = Array(dx_n.data[0:(N_k.data[k] - t)])
            z = Array(dx_n.data[t:N_k.data[k]])
            x = Array(y.multiply_by(z))
            #x = Array(dx_n.data[0:(N_k.data[k] - t)].multiply_by(dx_n.data[t:N_k.data[k]]))
            numerator += x.Sum()
            denom += float(x.n)

        C = numerator/denom
        
        C = C/sigma2
        
        Ct.append([t,C])
        
        if C <= 0.0 and t > 10 :
            break
    
        g += 2.0 * C * (1.0 - float(t) / Navg) 

        t += 1
    
    if g < 1.0 :
        g = 1.0

    return g

def calc_equilibrium(A_t):
    
    T = len(A_t)
    g_t = np.ones([T-1], np.float32)
    Neff_t = np.ones([T-1],np.float32)
    
    for t in range(0,T-1):
        g_t[t] = get_efficiency(A_t[t:T])
        Neff_t[t] = (T - t + 1)/g_t[t]

    Neff_max = Neff_t.max()
    t = Neff_t.argmax()
    g = g_t[t]
    for i in range(T-1):
        print "%s %s %s" % (i, g_t[i],Neff_t[i])

    return (t, g, Neff_max)
    
def get_efficiency(dgbind):

    energy = Array(dgbind)
    truncated_energy = System(energy.rev_cumulative_data()) ## returns truncated lists energy[i:]
 
    K = truncated_energy.m # number of timeseries
    N_k = truncated_energy.N # list of lengths of each timeseries
    Navg = N_k.mean() 
    N = N_k.Sum()
    mu = truncated_energy.cum_mean()
    fluctuation = System(truncated_energy.minus(mu))
    sigma2 = fluctuation.cum_variance()/float(N)

    return auto_correlation(fluctuation,N_k,N,sigma2,Navg,K)



def main():
    
    dgbind = []
    time = []

    infile = sys.argv[1]
    #outfile = sys.argv[2]
    with open(infile, 'r') as f:
        for line in f:
            col = line.split()
            dgbind.append(float(col[1]))
            time.append(float(col[0]))

    
        
    t, g, Neff = calc_equilibrium(dgbind)
    print t
    print g
    print Neff

"""
    with open(outfile, 'w') as out:

        out.write("!# g = %s , tau = %s  \n" % (g, tau))
        for i in range(len(Ct)):
            out.write("%s %s \n" % (Ct[i][0], Ct[i][1])) 
"""

if __name__ == "__main__":
    main()
