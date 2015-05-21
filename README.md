# TimeVis
Time series visualization and analysis. 

A visualization tool to visualize gene expression time series data.

# Documentation

Documentation can be seen from [Github Page](http://gaoce.github.io/TimeVis)

# Installation and start

We recommend you install the package under virtualenv

    $ pip install git+https://github.com/gaoce/TimeVis

The application depends on numpy/scipy, if it is a problem for you, try 
[Anaconda](http://continuum.io/downloads).

After installation, start the application at command line.
	
    $ timevis -b

# User Interface
Interface to define experiment information, including factors (independent
variables) and channels (dependent variables).

![Experiment Information](/docs/images/experiment.png)

<!--
Interface to define experimental conditions, namely the levels of factors for
each well in the plates.

![Layout Information](/docs/images/layout.png)
-->

Interface to query and visualize time series data based on conditions of
interest.

![Visualization](/docs/images/gene_vis.png)

# Software Structure

![Structure](/docs/images/arch.png)
