#!/usr/bin/env python3
"""
linear_topo.py
==============

Lab 1: Linear topology with N hosts and N switches connected in a chain.

    h1        h2        h3        h4
     \\         \\         \\         \\
     s1 ------ s2 ------ s3 ------ s4

Each switch has exactly one attached host. Switches are chained
sequentially, so traffic between h1 and h4 must traverse all
four switches — making this a textbook single-point-of-failure
("daisy chain") design.

Usage:
    sudo mn --custom topologies/linear_topo.py --topo linear4
    sudo mn --custom topologies/linear_topo.py --topo linear4 --link tc,bw=10,delay=5ms
"""
from mininet.topo import Topo


class LinearTopo(Topo):
    """N switches in a chain, each with one attached host."""

    def build(self, n=4):
        switches = []

        for i in range(1, n + 1):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)

            host = self.addHost(f'h{i}', ip=f'10.0.0.{i}/8')
            self.addLink(host, switch)

        # Chain the switches together: s1-s2, s2-s3, s3-s4, ...
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])


topos = {
    'linear4': (lambda: LinearTopo(n=4)),
}
