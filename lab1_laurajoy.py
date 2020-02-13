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

"""



# Correct output
"""
Given link rate 1000000 and user rate 100000, users active 10.0%
blocking probability is 0.000424

Given link rate 1000000 and user rate 100000, users active 10.0%
blocking probability limit of 0.00043, the capacity is
10 for circuit switching and 35 for packet switching.
"""

from scipy.special import comb
import math


def prob_block(R, r, active, N):
  """return the probability of blocking on a shared
  packet switched link, given these parameters:

  R - data rate of the shared link (b/s)
  r - data rate of each user when active
  active - fraction of time each user is active
  N - number of packet switching users
  """
  max_at_once = math.floor(R / r)
  sum = 0

  for i in range(N - max_at_once):
      sum += comb(N, max_at_once + i + 1) * (active)**(max_at_once + i + 1) * (1 - active)**(N - (max_at_once + i + 1))

  return sum


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

    circuit_users = math.floor(R / r)

    prob = 0.0
    packet_users = 0

    while(prob < block_limit):
        packet_users += 1
        prob = prob_block(R, r, active, packet_users)

    packet_users -= 1
    return (circuit_users, packet_users)


def main():

    R = 1000000
    r = 100000
    N = 35
    active = 0.1
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
