#!/usr/bin/env python3
"""
custom_topo.py
==============

A general-purpose, parameterized Mininet topology used as a
starting point for ad-hoc experiments.

Builds N hosts connected to a single switch, with each host
assigned a sequential IP in the 10.0.0.0/8 block — equivalent
to `--topo single,N` but expressed in Python so it can be
extended (custom link params, naming, controllers, etc.).

Usage:
    sudo mn --custom topologies/custom_topo.py --topo custom,5
"""
from mininet.topo import Topo


class CustomTopo(Topo):
    """Single switch with N hosts."""

    def build(self, n=3):
        switch = self.addSwitch('s1')

        for i in range(1, n + 1):
            host = self.addHost(f'h{i}', ip=f'10.0.0.{i}/8')
            self.addLink(host, switch)


topos = {
    'custom': (lambda n=3: CustomTopo(n=n)),
}
