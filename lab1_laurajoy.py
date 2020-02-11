__author__ = "Laura Joy Erb"
__email__ = "laurajoy@bu.edu"
__lab__ = "lab1"

"""
Lab 1 : Switching Capacity
--------------------------


The purpose of this assignment is to confirm
and further explore the result shown on Chapter 1 slide 30
of the lecture slides. The scenario describes a situation
where a number of users are sharing a 1 Mb/s link in either
a circuit-switched network or a packet-switched network.

Each user, when active, transmits at 100 kb/s. Each user is only
active 10% of the time.

In the slide, it states that the capacity of the network
based on circuit switching is 10 users, and that if
there are 35 packet switching users, then
the probability of blocking (which happens when too many
packet switching users become active at the same time) will
be 0.0004

Your task is to confirm this result and extend it by completing
the following functions: prob_block and capacity

The correct output of this program is shown below.


Instructions:
-------------
1. Download this file and rename it to lab1_XXX.py, where XXX is your BU email/login name.
For jdoe@bu.edu, the file would be called lab1_jdoe.py

2. Solve the problems below, and make sure of the following requirements:
    1. Your solution must work in a Python 3 environment. It will be tested on the VM "devbox2020"
    2. Replace the **\_\_author\_\_** and **\_\_email\_\_** fields at the top of this file with your name and email.
    3. Do not modify the function names and arguments, as this will interfere with how we validate your solution.
    You may freely add additional helper functions and classes.
    4. Document your code. This will help us give you partial credit when a solution is wrong, but the intermediary steps make sense.
"""



# Correct output
"""
Given link rate 1000000 and user rate 100000, users active 10.0%
blocking probability is 0.000424

Given link rate 1000000 and user rate 100000, users active 10.0%
blocking probability limit of 0.00043, the capacity is
10 for circuit switching and 35 for packet switching.
"""

# the following function is included so that you can calculate
# n-choose-k  or C(n,k)

from scipy.special import comb


def prob_block(R, r, active, N):
  """return the probability of blocking on a shared
  packet switched link, given these parameters:

  R - data rate of the shared link (b/s)
  r - data rate of each user when active
  active - fraction of time each user is active
  N - number of packet switching users
  """

  return 0.1


def capacity(R, r, active, block_limit):
  """return the number of users that can be supported on a
  shared link using circuit switching and using packet switching,
  given these parameters:

  R - data rate of the shared link (b/s)
  r - data rate of each user when active (b/s)
  active - fraction of time each user is active
  block_limit - maximum probability of blocking that is acceptable
    for the packet switching case.

  The return value should be a two-tuple containing the number of
  users supported by circuit switching followed by the number of
  users supported by packet switching.
  """

  return (5, 15)


def main():
    # This section is only here so you can run your python code
    # directly from the command line by typing
    #   $ python3 lab2_yourname.py
    # There is nothing to do here.
    R=1000000
    r=100000
    active = 0.1
    N=35
    pb = prob_block(R, r, active, N)

    print(f"Given link rate {R} and user rate {r}, users active {active:.1%}")
    print(f"blocking probability is {pb:.6f}")

    limit = 0.00043
    (C,P) = capacity(R, r, active, 0.00043)

    print(f"\nGiven link rate {R} and user rate {r}, users active {active:.1%}")
    print(f"blocking probability limit of {limit}, the capacity is")
    print(f"{C} for circuit switching and {P} for packet switching.")


if __name__ == '__main__':
  main()
