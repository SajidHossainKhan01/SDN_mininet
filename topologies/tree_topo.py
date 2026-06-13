#!/usr/bin/env python3
"""
tree_topo.py
============

Lab 2: Configurable tree topology built explicitly with the Topo API.

Reproduces Mininet's built-in `--topo tree,depth=D,fanout=F` behavior,
but as an editable class so link parameters, naming, or controller
placement can be customized.

Formulas (for depth d, fanout f):
    Switches     S = (f^d - 1) / (f - 1)
    Leaf switches L = f^(d-1)
    Hosts        H = f^(d-1)   (one host per leaf switch)

Usage:
    sudo mn --custom topologies/tree_topo.py --topo tree32   # depth=3, fanout=2
    sudo mn --custom topologies/tree_topo.py --topo tree23   # depth=2, fanout=3
"""
from mininet.topo import Topo


class CustomTreeTopo(Topo):
    """Recursive tree topology: `depth` levels, `fanout` children per switch."""

    def build(self, depth=3, fanout=2):
        # counter[0] = switch index, counter[1] = host index
        counter = [0, 0]
        self._add_tree(depth, fanout, level=1, parent=None, counter=counter)

    def _add_tree(self, depth, fanout, level, parent, counter):
        counter[0] += 1
        switch = self.addSwitch(f's{counter[0]}')

        if parent is not None:
            self.addLink(parent, switch)

        if level == depth:
            # Leaf level: attach `fanout` hosts to this switch
            for _ in range(fanout):
                counter[1] += 1
                host = self.addHost(f'h{counter[1]}', ip=f'10.0.0.{counter[1]}/8')
                self.addLink(host, switch)
        else:
            for _ in range(fanout):
                self._add_tree(depth, fanout, level + 1, switch, counter)


topos = {
    'tree32': (lambda: CustomTreeTopo(depth=3, fanout=2)),
    'tree23': (lambda: CustomTreeTopo(depth=2, fanout=3)),
    'tree33': (lambda: CustomTreeTopo(depth=3, fanout=3)),
}
