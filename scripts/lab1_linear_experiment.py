#!/usr/bin/env python3
"""
lab1_linear_experiment.sh (Python driver)
==========================================

Lab 1: Linear Topology — Latency & Failure Analysis

Scenario:
    Evaluate a network where traffic flows sequentially through
    multiple switches. Understand latency impact and failure risk.

Automated steps:
    1. Build a linear topology (4 hosts, 4 switches)
    2. Run pingall to verify full connectivity
    3. Measure RTT between h1 (first) and h4 (last)
    4. Run iperf between h1 and h4 to measure TCP throughput
    5. Bring down the link between intermediate switches s2-s3
    6. Re-test connectivity to observe the failure impact
    7. Restore the link and confirm recovery

Run with:
    sudo python3 scripts/lab1_linear_experiment.py
"""
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinearTopo(Topo):
    """4 switches in a chain, each with one attached host."""

    def build(self, n=4):
        switches = []
        for i in range(1, n + 1):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)
            host = self.addHost(f'h{i}', ip=f'10.0.0.{i}/8')
            self.addLink(host, switch)

        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])


def main():
    setLogLevel('info')

    topo = LinearTopo(n=4)
    net = Mininet(topo=topo)
    net.start()

    info('\n*** Step 1: Verifying full connectivity (pingall) ***\n')
    net.pingAll()

    h1, h4 = net.get('h1'), net.get('h4')

    info('\n*** Step 2: Measuring RTT between h1 and h4 (4 ping packets) ***\n')
    result = h1.cmd(f'ping -c 4 {h4.IP()}')
    info(result)

    info('\n*** Step 3: Running iperf between h1 (server) and h4 (client) ***\n')
    bw_results = net.iperf((h1, h4))
    info(f'iperf results: {bw_results}\n')

    info('\n*** Step 4: Simulating link failure between s2 and s3 ***\n')
    net.configLinkStatus('s2', 's3', 'down')

    info('\n*** Step 5: Re-testing connectivity after link failure ***\n')
    result = h1.cmd(f'ping -c 4 {h4.IP()}')
    info(result)
    net.pingAll()

    info('\n*** Step 6: Restoring the s2-s3 link ***\n')
    net.configLinkStatus('s2', 's3', 'up')

    info('\n*** Step 7: Confirming recovery ***\n')
    net.pingAll()

    info('\n*** Dropping to CLI for manual exploration (type "exit" to quit) ***\n')
    CLI(net)

    net.stop()


if __name__ == '__main__':
    main()
