# vmemprof

Usage: vmemprof.py <vmprof.dat>

Where vmprof.dat is a profile file generated by vmprof with memory
profiling.

It visualizes total RSS of your program vs time and shows tracebacks
for each point. The example flask server will resample the data.

The basic interactive feature is zoom in, which can be done by clicking
on two points on the graph. Tracebacks will have all the python functions
on the stack (but not say Cython, pending future improvements to vmprof).

Usage:

```console
sudo apt-get install python-dev
pip install -r requirements.txt
python -m vmprof --mem -o vmprof-mem.dat
python vmemprof.py vmprof-mem.dat
```

Alternatively, the following modifications have to be done to the program,
if you're not using the command line interface, but the programmable API:

```console
import vmprof
tmpfile = open("vmprof-mem.dat", "w")
vmprof.enable(tmpfile.fileno(), 0.01, True)
try:
   ... # your program
finally:
   vmprof.disable()
```

Would write to a file "vmprof-mem.dat" vmprof information including
the memory data. Note that this profile is also usable for normal vmprof
usage.

## Interpreting the data

Data shown on the Y axis is the total memory consumed by the process
in kilobytes (or megabytes). The X axis corresponds to the sample number
and roughly correspond to the timestamp, depending on your sampling rate.

You can hover over the graph to see the traceback at each point in time.

Clicking on the graph twice would zoom in to a specific area if the resolution
is not high enough
