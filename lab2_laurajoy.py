import subprocess
import statistics

__author__ = "Laura Joy Erb"
__email__ = "laurajoy@bu.edu"
__lab__ = "lab2"

""" # EC441

## Lab 2 -- Traceroute

Traceroute is a simple utility that can be run from any Internet host. When the user
specifies a certain host destination name, Traceroute shows the name and roundtrip
time of each router along the way from the source to the destination (including).

1. Download this file and rename it to lab2_XXX.py, where XXX is your BU email/login name. 
For jdoe@bu.edu, the file would be called lab2_jdoe.py

2. Solve the problems below, and make sure of the following requirements:
    1. Your solution must work in a Python 3 environment.
    2. Replace the **\_\_author\_\_** and **\_\_email\_\_** fields at the top of this file with your name and email.
    3. Do not modify the function names and arguments, as this will interfere with how we validate your solution. You may freely add additional helper functions and classes.
    4. Document your code. This will help us give you partial credit when a solution is wrong, but the intermediary steps make sense. 
"""


def lab2_problem1(host='bu.edu'):
    """ ### Problem 1: Simple Traceroute

You have seen in class how the traceroute command-line utility can be used to measure the roundtrip time to a specific host. A simple example of how to call traceroute from within Python is given here:

    for s in _raw_traceroute('bu.edu'): 
        print(s.split('  ')) 
        # then do something with the extracted output 

By default, traceroute only queries three times per 'TTL'. Look up the manpage of traceroute to find out how to change the number of queries. Then, adapt the helper function (or write your own new implementation below) such that the traceresult variable contains a traceroute run that uses 10 queries. You may have to look up the documentation for Python's 'subprocess' module to see how to change its input.

**Goal:** This function should return a list of traceroute output strings (similar to the helper function) with timing data from 10 query probes.
"""

    # this is essentially the same as the helper function, with the addition of the query arg
    # adding the "-q 10" argument increases the # of probe queries to 10
    tr = subprocess.run(
        ["traceroute", "-q 10", host], stdout=subprocess.PIPE)  # executing traceroute as a subprocess
    # return a list of strings containing the traceroute output
    return tr.stdout.decode("utf-8").split('\n')


def lab2_problem2():
    """ ### Problem 2

1.  Run traceroute on the website of the University of Florida, www.ufl.edu.
2.  For each hop, calculate the average roundtrip time, as well as the standard deviation (use the stdev function from the statistics package)
3.  Return a list of (avg, stdev) tuples for each hop.

A code skeleton is given below for reference, feel free to adapt or replace.
    """
    traceresult = _raw_traceroute("www.ufl.edu")
    hopstats = []
    for t in traceresult:
        # extract times
        print(t)
        trace_array = t.split('  ')
        if len(trace_array) > 4:
            # times = ['3.141 ms', '5.926 ms', '5.358 ms']
            times = [trace_array[2], trace_array[3], trace_array[4]]
            index = 0
            for time in times:
                times[index] = float(time[:-3])
                index += 1

        # times = [3.141, 5.926, 5.358]

        avg = sum(times) / len(times)     # calculate average
        std = statistics.stdev(times)     # calculate standard deviation
        hopstats.append((avg, std))
    return hopstats


def lab2_problem3():
    """ ### Problem 3

1. Run traceroutes for the following university domains:
    a. stanford.edu
    b. www.ethz.ch
    c. www.tum.de
2. Return a list that contains integers representing
    * the hops that are common between a. and b.
    * the hops that are common between a. and c.
    * the hops that are common between b. and c.
    """
    commonhops = [0, 0, 0]

    # do the thing

    return commonhops


""" ### Helper Functions

Helper functions are defined with a leading underscore (e.g. def _helper_function()). 
These functions are provided for your convenience, you may use them as provided, 
change them, or use an alternative solution altogether.
"""


def _raw_traceroute(host):
    """ The helper function **_raw_traceroute(host)** calls traceroute on a 
    host and returns a list of the results.
    """
    tr = subprocess.run(
        ["traceroute", host], stdout=subprocess.PIPE)  # executing traceroute as a subprocess
    # return a list of strings containing the traceroute output
    return tr.stdout.decode("utf-8").split('\n')


# This section is only here so you can run your python code
# directly from the command line by typing
#   $ python3 lab2_yourname.py
# There is nothing to do here.


def main():
    # long_trace = lab2_problem1()
    hops = lab2_problem2()

    for item in hops:
        print(item)

    # lab2_problem3()


if __name__ == "__main__":
    main()
