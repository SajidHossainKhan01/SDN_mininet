#!/usr/bin/env python3
"""
linktest_topo.py
================

A minimal topology (2 hosts, 1 switch) with explicit link-level
parameters applied via Mininet's TCLink class — a thin wrapper
around Linux `tc`/`netem`.

Each link is configured with:
    - bandwidth: 10 Mbps
    - delay:     10 ms
    - loss:      1%

Expected RTT between h1 and h2 (one switch hop each way):
    h1 -> s1 -> h2  (request)  : 2 x 10ms = 20ms
    h2 -> s1 -> h1  (reply)    : 2 x 10ms = 20ms
    Total RTT                  : ~40ms

Usage:
    sudo mn --custom topologies/linktest_topo.py --topo linktest
    mininet> h1 ping -c 4 h2
    mininet> iperf h1 h2
"""
from mininet.topo import Topo
from mininet.link import TCLink


class LinkParamTopo(Topo):
    """2 hosts, 1 switch, with bandwidth/delay/loss-constrained links."""

    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/8')
        h2 = self.addHost('h2', ip='10.0.0.2/8')
        s1 = self.addSwitch('s1')

        self.addLink(h1, s1, cls=TCLink, bw=10, delay='10ms', loss=1)
        self.addLink(h2, s1, cls=TCLink, bw=10, delay='10ms', loss=1)


topos = {
    'linktest': (lambda: LinkParamTopo()),
}
