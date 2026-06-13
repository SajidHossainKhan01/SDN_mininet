#!/usr/bin/env python3
"""
lab2_tree_experiment.py
========================

Lab 2: Tree Topology — Scalability Analysis

Scenario:
    A campus network designed as a hierarchical (tree) topology.
    Analyze how depth and fanout affect scalability and performance.

Automated steps:
    1. Build a tree topology with depth=3, fanout=2
    2. Print computed switch/host counts (see docs/tree_math.md)
    3. Run pingall to verify connectivity
    4. Measure latency between two hosts in different branches
    5. Print a comparison table for fanout=2 vs fanout=3 (depth=3)

Run with:
    sudo python3 scripts/lab2_tree_experiment.py
"""
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class CustomTreeTopo(Topo):
    """Recursive tree topology: `depth` levels, `fanout` children per switch."""

    def build(self, depth=3, fanout=2):
        counter = [0, 0]
        self._add_tree(depth, fanout, level=1, parent=None, counter=counter)

    def _add_tree(self, depth, fanout, level, parent, counter):
        counter[0] += 1
        switch = self.addSwitch(f's{counter[0]}')

        if parent is not None:
            self.addLink(parent, switch)

        if level == depth:
            for _ in range(fanout):
                counter[1] += 1
                host = self.addHost(f'h{counter[1]}', ip=f'10.0.0.{counter[1]}/8')
                self.addLink(host, switch)
        else:
            for _ in range(fanout):
                self._add_tree(depth, fanout, level + 1, switch, counter)


def switch_count(depth, fanout):
    """S = (f^d - 1) / (f - 1), or S = d if f == 1."""
    if fanout == 1:
        return depth
    return (fanout ** depth - 1) // (fanout - 1)


def host_count(depth, fanout):
    """H = f^(d-1)"""
    return fanout ** (depth - 1)


def main():
    setLogLevel('info')

    depth, fanout = 3, 2

    info(f'\n*** Building tree topology: depth={depth}, fanout={fanout} ***\n')
    topo = CustomTreeTopo(depth=depth, fanout=fanout)
    net = Mininet(topo=topo)
    net.start()

    s = switch_count(depth, fanout)
    h = host_count(depth, fanout)
    info(f'*** Expected switches: {s}, Expected hosts: {h} ***\n')

    info('\n*** Step 1: Verifying full connectivity (pingall) ***\n')
    net.pingAll()

    # Pick two hosts from different branches: h1 and the last host
    h1 = net.get('h1')
    last_host = net.get(f'h{h}')

    info(f'\n*** Step 2: Measuring latency between h1 and h{h} (different branches) ***\n')
    result = h1.cmd(f'ping -c 4 {last_host.IP()}')
    info(result)

    info('\n*** Step 3: Scalability comparison (depth=3) ***\n')
    info('| fanout | switches | hosts |\n')
    info('|--------|----------|-------|\n')
    for f in (2, 3):
        info(f'| {f}      | {switch_count(depth, f):<8} | {host_count(depth, f):<5} |\n')

    info('\n*** Dropping to CLI for manual exploration (type "exit" to quit) ***\n')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    main()
