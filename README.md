# TimeVis
Time series visualization and analysis.

A visualization tool to visualize gene expression time series data.

## 1. Documentation

Documentation can be seen from the project [Github Page](http://gaoce.github.io/TimeVis)

## 2. Installation

We recommend you install the package under [virtualenv](https://virtualenv.pypa.io/en/latest/)

    $ pip install git+https://github.com/gaoce/TimeVis

The application depends on numpy/scipy, if it is a problem for you, try
[Anaconda](http://continuum.io/downloads).

You can also use Docker

    $ sudo docker pull gaoce/timevis

## 3. Start and stop
Start the application using the following command

    $ timevis  -h
    usage: timevis [-h] [-b] [-p PORT] [-s HOST] [-d DEBUG]

    TimeVis

    optional arguments:
      -h, --help            show this help message and exit
      -b, --browser         Enable browser
      -p PORT, --port PORT  Port
      -s HOST, --host HOST  Host
      -d DEBUG, --debug DEBUG
                            Debug mode

To use your own config file, set environment variable
`TIMEVIS_CONFIG=/path/to/config.py`.

If you are using Docker

    $ sudo docker run -p 8000:8000 gaoce/timevis timevis

The application can be accessed through `http://localhost:8000` inside your
browser.

To stop, use the keyboard shortcut `Ctrl+c`.

## 4. User Interface
Interface to define experiment information, including factors (independent
variables) and channels (dependent variables).

![Experiment Information](/docs/images/experiment.png)

Interface to query and visualize time series data based on conditions of
interest.

![Visualization](/docs/images/gene_vis.png)
