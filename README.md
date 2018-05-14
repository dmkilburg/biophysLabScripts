
# CompMolBioPhys Lab Scripts

**This a repo contains some quick python 2.7 scripts that I wrote in 2014 during my first year in the lab to manage data and use lab software more efficiently.**

This repo contains the following scripts:

- `pull_this.py` : This is a script that reads in a BEDAM output file, repl.cycle.totE.potE.temp.lambda.ebind.dat . The name of the data file is a required argument when calling the script. The data file should have 7 columns delimited with white space that contain: replica number, cycle number, total energy, potential energy,  temperature, lambda value, and ebind energy. This scripts subsets the data based on criteria given after an optional argument is selected. This script has 4 optional arguments: `[-l]` to subset by lambda value, `[-c]` to subset by cycle number. There are 3 options within this subset: 1.block,2.forward, 3.backward, this identifies the order direction to subset the cycle data, you may then specify a start step and end integer value. The output of this option is used for the run_uwham.py script. `[-r]` to subset by replica . `[-t]` to subset by temperature. 

- `run_uwham.py` : This script is a wrapper that runs the uwham_analysis.R script multiple times and logs the calculated binding energy for the selected grouping of cycles to a file named `uwham_energy.dat`. The number of temperature values is a required argument. uwham_analysis.R must be in the same directory.

- `sort_energy.py`: This script reads the `uwham_energy.dat` file and outputs a new file that is subsetted by selected temperature and sorted by cycle as the output. This is for convenience as a plotting library such as gnuplot requires data to be ordered. If loading into a dataframe, this is unnecessary. Required arguments are (1 or 2) for which column of cycles you want it sorted by and (temp).

- `cycleTotime.py`: changes the cycle column to a time [ns] based on the number of picoseconds/cycle chosen during the start of the simulation.

**The above scripts are used to quickly calculate the data necessary to plot  the reverse cumulative and forward cumulative binding energies as a function of time for a given simulation. Examples of these types of plots and their relevance can be found in this publication: [Assessment of Single Decoupling Method](https://www.frontiersin.org/articles/10.3389/fmolb.2018.00022/full)**

Below is an example of the procedure to run these scripts via command line. `UWHAM` is available [here](http://www.stat.rutgers.edu/home/ztan/research.html)

` python pull_this.py -c repl.cycle.totE.potE.temp.lambda.ebind.dat 
  Enter sort option: (1:block,2:forward,3:backward) start, step and cutoff_cycle) 3 0 5 150`
  
`python run_uwham.py 4`

`python sort_energy.py 1 300`
