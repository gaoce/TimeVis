# TimeVis
Time series visualization and analysis. 

A visualization tool to visualize gene expression time series data.

## Documentation

Documentation can be seen from [Github Page](http://gaoce.github.io/TimeVis)

## Installation

We recommend you install the package under virtualenv

    $ pip install git+https://github.com/gaoce/TimeVis

The application depends on numpy/scipy, if it is a problem for you, try 
[Anaconda](http://continuum.io/downloads).

## Start and stop
Start the application using the following command
	
    $ timevis -b

To stop, use `C-c`.

## User Interface
Interface to define experiment information, including factors (independent
variables) and channels (dependent variables).

![Experiment Information](/docs/images/experiment.png)

Interface to query and visualize time series data based on conditions of
interest.

![Visualization](/docs/images/gene_vis.png)

## Software Structure

![Structure](/docs/images/arch.png)
