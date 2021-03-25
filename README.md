# goestools monitor written in python

# Realtime gauges and constellation plot...

![Output of GoesToolsMon](./images/example.png)

# and datalogging too...

![Plot of GoesToolsMon data](./images/plots.png)

# Dependencies:
A working installation of GOESTOOLS: https://github.com/pietern/goestools

Python bindings for nanomsg: https://github.com/nanomsg/nnpy

Both plotly and dash packages: https://plotly.com/

Python matplotlib: https://matplotlib.org/

The commands ```sudo apt install libnanomsg-dev``` and then ```sudo pip3 install python3 nnpy plotly dash matplotlib``` will install the dependencies on a Debian/Ubuntu based system.

Once you have done that, ```python3 goestoolsmon.py``` will run the monitor. If you have the web page enabled, point your browser to ```http://localhost:8050``` to see the gauges, and if you have the datalogging enabled, running ```python3 plot.py``` will create a set of graphs of the data.
