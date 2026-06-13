# 🌐 SDN Capability Lab — Mininet Network Emulation

> **Course Project** · Lab 7: Understanding SDN Capability Using Mininet
> Demonstrates Software-Defined Networking fundamentals using Mininet network emulation, custom Python topologies, and traffic/link experiments.

[![Mininet](https://img.shields.io/badge/Mininet-2.3.0-blue)](http://mininet.org/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)](https://www.python.org/)
[![OpenFlow](https://img.shields.io/badge/OpenFlow-1.0-orange)](https://opennetworking.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)](https://www.linux.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [What is SDN & Mininet?](#what-is-sdn--mininet)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Built-in Topologies](#built-in-topologies)
- [Custom Topologies](#custom-topologies)
- [Mininet CLI Cheat Sheet](#mininet-cli-cheat-sheet)
- [Experiments](#experiments)
  - [Lab 1: Linear Topology — Latency & Failure Analysis](#lab-1-linear-topology--latency--failure-analysis)
  - [Lab 2: Tree Topology — Scalability Analysis](#lab-2-tree-topology--scalability-analysis)
- [Link Emulation (tc/netem)](#link-emulation-tcnetem)
- [Regression Tests](#regression-tests)
- [Results Summary](#results-summary)
- [Troubleshooting](#troubleshooting)
- [Key Concepts Reference](#key-concepts-reference)
- [References](#references)

---

## Overview

This repository is a **hands-on implementation** of Software-Defined Networking (SDN) experiments using [Mininet](http://mininet.org/), a network emulator that creates a realistic virtual network of hosts, switches, controllers, and links on a single machine.

It demonstrates:

- ✅ Mininet VM setup and CLI fundamentals
- ✅ Built-in topologies (minimal, single, linear, tree, reversed)
- ✅ Custom Python topology scripts (`Topo` API)
- ✅ Link parameter configuration (bandwidth, delay, loss) via `tc`/`netem`
- ✅ Connectivity testing (`pingall`, `iperf`)
- ✅ Fault-tolerance testing (link up/down)
- ✅ NAT configuration for external internet access
- ✅ Regression testing (`--test pingpair`, `--test iperf`)
- ✅ Two full experimental labs with measured results and analysis

---

## What is SDN & Mininet?

**Software-Defined Networking (SDN)** decouples the network's control plane (decision-making) from the data plane (packet forwarding). A centralized **controller** programs the forwarding behavior of switches via a protocol such as **OpenFlow**.

**Mininet** emulates an entire SDN network — hosts, OpenFlow switches (Open vSwitch), links, and controllers — as lightweight processes and virtual interfaces on a single Linux kernel. This makes it possible to prototype and test real SDN topologies without physical hardware.

```
┌──────────────────────────────────────────┐
│              Controller (c0)              │  ← Control plane (OpenFlow)
└───────────────────┬────────────────────────┘
                     │ OpenFlow (TCP 6653)
                     ▼
┌──────────────────────────────────────────┐
│            OVS Switch (s1...sN)           │  ← Data plane
└──────┬───────────────────────────┬────────┘
       │                            │
       ▼                            ▼
┌─────────────┐              ┌─────────────┐
│   Host h1    │              │   Host h2    │  ← Network namespaces
│ 10.0.0.1/8   │              │ 10.0.0.2/8   │
└─────────────┘              └─────────────┘
```

---

## Repository Structure

```
sdn-mininet-lab/
├── README.md                        ← You are here
├── LICENSE
├── .gitignore
│
├── topologies/
│   ├── custom_topo.py               ← General-purpose custom Topo class
│   ├── linear_topo.py               ← Lab 1: linear topology (4 hosts, 4 switches)
│   ├── tree_topo.py                 ← Lab 2: tree topology (depth/fanout configurable)
│   └── linktest_topo.py             ← Topology with tc-based link parameters
│
├── scripts/
│   ├── run_minimal.sh               ← Minimal topology
│   ├── run_single.sh                ← Single switch, N hosts
│   ├── run_linear.sh                ← Linear topology with NAT
│   ├── run_tree.sh                  ← Tree topology (depth/fanout)
│   ├── run_link_params.sh           ← Link bw/delay configuration
│   ├── run_regression_tests.sh      ← pingpair + iperf regression tests
│   ├── lab1_linear_experiment.sh    ← Full Lab 1 automation
│   └── lab2_tree_experiment.sh      ← Full Lab 2 automation
│
├── docs/
│   ├── mininet_cli_reference.md     ← Full CLI command reference
│   ├── topology_types.md            ← Explanation of each topology type
│   ├── tree_math.md                  ← Switch/host count formulas
│   └── lab_report_template.md       ← Reusable report template
│
└── results/
    ├── lab1/
    │   ├── lab1_report.md            ← Lab 1 findings & analysis
    │   └── lab1_pingall_output.txt
    └── lab2/
        ├── lab2_report.md            ← Lab 2 findings & analysis
        └── lab2_topology_stats.md
```

---

## Getting Started

### Requirements

- Mininet VM **2.3.0** ([download](https://github.com/mininet/mininet/releases/download/2.3.0/mininet-2.3.0-210211-ubuntu-16.04.7-server-amd64-ovf.zip)) running in VMware/VirtualBox
- SSH client on host machine
- Default credentials: `mininet` / `mininet`

### Connect to the VM

```bash
ssh mininet@<vm-ip-address>
```

### Clone this repo inside the VM

```bash
git clone https://github.com/YOUR_USERNAME/sdn-mininet-lab.git
cd sdn-mininet-lab
chmod +x scripts/*.sh
```

### Run your first topology

```bash
sudo mn
```

```
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2
*** Adding switches:
s1
*** Adding links:
(h1, s1) (h2, s1)
*** Configuring hosts
h1 h2
*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet>
```

---

## Built-in Topologies

| Topology | Command | Description |
|---|---|---|
| **Minimal** | `sudo mn --topo minimal` | 2 hosts, 1 switch (default) |
| **Single** | `sudo mn --topo single,3` | 1 switch, N hosts (here N=3) |
| **Reversed** | `sudo mn --topo reversed,3` | Like single, but host/switch numbering reversed |
| **Linear** | `sudo mn --topo linear,3` | N hosts, N switches connected in a chain |
| **Tree** | `sudo mn --topo tree,depth=3,fanout=2` | Hierarchical tree, 2 hosts per leaf switch |

```bash
# scripts/run_minimal.sh
sudo mn --topo minimal

# scripts/run_single.sh
sudo mn --topo single,3

# scripts/run_tree.sh
sudo mn --topo tree,depth=3,fanout=2
```

### Visual Reference

```
Minimal                Single                  Linear
   C0                     C0                    S3──S2──S1
   │                      │                     │   │   │
   S1                     S1                    H3  H2  H1
  ╱  ╲                 ╱ │ │ │ ╲
H1    H2             H1 H2 H3 H4 H5

Tree (depth=3, fanout=2)
                S(root)
              ╱         ╲
           S(1,1)       S(1,2)
          ╱    ╲        ╱    ╲
      S(2,1) S(2,2)  S(2,3) S(2,4)
       │  │   │  │    │  │   │  │
      H  H   H  H    H  H   H  H
```

---

## Custom Topologies

Beyond CLI flags, Mininet's Python API (`Topo` class) allows full programmatic control over hosts, switches, links, and IP addressing.

### `topologies/linear_topo.py`

```python
#!/usr/bin/env python3
"""
Lab 1: Linear topology with 4 hosts and 4 switches.

    h1 -- s1 -- s2 -- s3 -- s4 -- h4
            |    |    |
           h2   ...  h3  (one host per switch)
"""
from mininet.topo import Topo


class LinearTopo(Topo):
    """4 switches in a chain, each with one attached host."""

    def build(self, n=4):
        switches = []
        for i in range(1, n + 1):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)

            host = self.addHost(
                f'h{i}',
                ip=f'10.0.0.{i}/8'
            )
            self.addLink(host, switch)

        # Chain the switches together
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])


topos = {'linear4': (lambda: LinearTopo(n=4))}
```

Run it:

```bash
sudo mn --custom topologies/linear_topo.py --topo linear4 --link tc,bw=10,delay=5ms
```

### `topologies/tree_topo.py`

```python
#!/usr/bin/env python3
"""
Lab 2: Configurable tree topology (depth x fanout).

Uses Mininet's built-in TreeTopo, exposed here for custom
extension (e.g. adding link parameters or custom IP scheme).
"""
from mininet.topo import Topo


class CustomTreeTopo(Topo):
    """Recreates Mininet's tree topology with explicit control."""

    def build(self, depth=3, fanout=2):
        self._add_tree(depth, fanout, level=1, parent=None, counter=[0, 0])

    def _add_tree(self, depth, fanout, level, parent, counter):
        counter[0] += 1
        switch = self.addSwitch(f's{counter[0]}')

        if parent is not None:
            self.addLink(parent, switch)

        if level == depth:
            # Leaf level: attach `fanout` hosts
            for _ in range(fanout):
                counter[1] += 1
                host = self.addHost(
                    f'h{counter[1]}',
                    ip=f'10.0.0.{counter[1]}/8'
                )
                self.addLink(host, switch)
        else:
            for _ in range(fanout):
                self._add_tree(depth, fanout, level + 1, switch, counter)


topos = {
    'tree32': (lambda: CustomTreeTopo(depth=3, fanout=2)),
    'tree23': (lambda: CustomTreeTopo(depth=2, fanout=3)),
}
```

Run it:

```bash
sudo mn --custom topologies/tree_topo.py --topo tree32
```

### `topologies/linktest_topo.py`

```python
#!/usr/bin/env python3
"""
Topology with explicit link-level parameters (bandwidth, delay, loss)
applied via the TCLink class — wraps Linux tc/netem.
"""
from mininet.topo import Topo
from mininet.link import TCLink


class LinkParamTopo(Topo):
    """2 hosts, 1 switch, with a constrained link in between."""

    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/8')
        h2 = self.addHost('h2', ip='10.0.0.2/8')
        s1 = self.addSwitch('s1')

        # 10 Mbps, 10ms delay, 1% packet loss on each link
        self.addLink(h1, s1, cls=TCLink, bw=10, delay='10ms', loss=1)
        self.addLink(h2, s1, cls=TCLink, bw=10, delay='10ms', loss=1)


topos = {'linktest': (lambda: LinkParamTopo())}
```

Run it:

```bash
sudo mn --custom topologies/linktest_topo.py --topo linktest
```

---

## Mininet CLI Cheat Sheet

| Command | Description |
|---|---|
| `help` | List all available CLI commands |
| `nodes` | Display all nodes (hosts, switches, controllers) |
| `net` | Display all links |
| `dump` | Dump full info about all nodes |
| `<node> <cmd>` | Run `<cmd>` on `<node>` (e.g. `h1 ifconfig -a`) |
| `h1 ping -c 1 h2` | Single ping from h1 to h2 |
| `pingall` | All-pairs connectivity test |
| `iperf` | Measure TCP bandwidth between two hosts |
| `link s1 h1 down` | Bring down the link between s1 and h1 |
| `link s1 h1 up` | Bring the link back up |
| `xterm h1` | Open a terminal for host h1 |
| `py <expr>` | Evaluate a Python expression |
| `exit` | Quit Mininet CLI |

### Fault-Tolerance Test

```
mininet> nodes
mininet> h1 ping h2
mininet> link s1 h1 down
mininet> h1 ping h2          # connect: Network is unreachable
mininet> link s1 h1 up
mininet> h1 ping h2          # connectivity restored
```

---

## Experiments

### Lab 1: Linear Topology — Latency & Failure Analysis

**Scenario:** Evaluate a network where traffic flows sequentially through multiple switches; assess latency impact and single-point-of-failure risk.

```bash
./scripts/lab1_linear_experiment.sh
```

What it does:
1. Builds a **linear topology** with 4 hosts and 4 switches (`--topo linear,4`)
2. Runs `pingall` to verify full connectivity
3. Measures RTT between `h1` and `h4` (first ↔ last host)
4. Runs `iperf` between `h1` and `h4` to measure TCP throughput
5. Brings down a link between two intermediate switches (`link s2 s3 down`)
6. Re-tests connectivity to observe the impact

```bash
sudo mn --topo linear,4
mininet> pingall
mininet> h1 ping -c 4 h4
mininet> iperf h1 h4
mininet> link s2 s3 down
mininet> h1 ping -c 4 h4
mininet> link s2 s3 up
```

📄 Full results & analysis: [`results/lab1/lab1_report.md`](results/lab1/lab1_report.md)

**Key findings:**
- RTT increases roughly linearly with hop count (each switch adds forwarding latency)
- A single intermediate link failure (`s2–s3`) **completely partitions** the network — `h1`/`h2` can no longer reach `h3`/`h4`
- This confirms a linear topology is a **single point of failure design**: there is no redundant path between any two switches

---

### Lab 2: Tree Topology — Scalability Analysis

**Scenario:** A campus network designed as a hierarchical tree. Analyze how `depth` and `fanout` affect scalability.

```bash
./scripts/lab2_tree_experiment.sh
```

What it does:
1. Builds a **tree topology** with `depth=3, fanout=2`
2. Computes and prints the number of switches/hosts (see formulas below)
3. Tests connectivity between hosts in different branches
4. Measures hop count / latency between two cross-branch hosts
5. Re-runs with `fanout=3` and compares host counts

```bash
sudo mn --topo tree,depth=3,fanout=2
mininet> pingall
mininet> h1 ping -c 4 h8     # hosts in different branches
```

📄 Full results & analysis: [`results/lab2/lab2_report.md`](results/lab2/lab2_report.md)
📄 Switch/host count tables: [`results/lab2/lab2_topology_stats.md`](results/lab2/lab2_topology_stats.md)

**Key findings:**
- Number of hosts grows **exponentially** with fanout: `H = f^(d-1)`
- Increasing fanout from 2 → 3 (depth=3) increases host count from **4 → 9** (a 125% increase)
- The **root switch** is the primary bottleneck — all inter-branch traffic must traverse it, making it both a scalability limit and a single point of failure

---

## Link Emulation (tc/netem)

Mininet uses **TCLink** (built on Linux `tc`/`netem`) to emulate realistic WAN-like conditions:

```bash
# Apply bandwidth, delay, and loss to every link
sudo mn --link tc,bw=1000,delay=10ms

# Verify with iperf and ping
mininet> iperf
mininet> h1 ping -c 4 h2
```

If each link has a 10ms delay, an ICMP echo between two directly-connected hosts via one switch traverses **4 link-segments** (request: h1→s1→h2, reply: h2→s1→h1), so expected RTT ≈ **40ms**.

| Parameter | tc/netem equivalent | Use case |
|---|---|---|
| `bw=N` | `tc qdisc ... tbf rate Nmbit` | Bandwidth-limited links (e.g. WAN, IoT) |
| `delay=Nms` | `tc qdisc ... netem delay Nms` | Latency simulation |
| `loss=N` | `tc qdisc ... netem loss N%` | Lossy/wireless link emulation |
| `jitter=Nms` | `tc qdisc ... netem delay Xms Nms` | Variable delay |

---

## Regression Tests

Mininet includes self-contained regression tests that build, test, and tear down a topology automatically.

```bash
# All-pairs ping test
sudo mn --test pingpair

# TCP bandwidth test (~10s)
sudo mn --test iperf

# Full automation script
./scripts/run_regression_tests.sh
```

> **Note:** the option is `pingpair`, not `pingair` — using an invalid test name produces:
> `Exception: Test pingair is unknown - please specify one of ['none', 'build', 'all', 'iperf', 'pingpair', 'iperfudp', 'pingall']`

---

## Results Summary

| Experiment | Topology | Hosts | Switches | Result |
|---|---|---|---|---|
| Lab 1 | Linear | 4 | 4 | 0% packet loss (healthy); 100% loss after `s2-s3` link down |
| Lab 2 (fanout=2) | Tree (d=3,f=2) | 4 | 7 | 0% packet loss, RTT increases with cross-branch hops |
| Lab 2 (fanout=3) | Tree (d=3,f=3) | 9 | 13 | Confirms exponential host growth `H = f^(d-1)` |

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `Unable to contact the remote controller` | Controller not started / wrong IP | Check `c0` with `sudo mn -c` then restart, or specify `--controller=remote,ip=<ip>` |
| `RTNETLINK answers: File exists` | Stale interfaces from previous run | Run `sudo mn -c` to clean up before restarting |
| `connect: Network is unreachable` | Link manually brought down | `link <switch> <host> up` |
| `sudo mn --test pingair` fails | Typo — valid option is `pingpair` | Use `sudo mn --test pingpair` |
| `h1 ping www.google.com` fails | No NAT configured | Use `--nat` flag: `sudo mn --topo=linear,4 --nat` |
| Permission denied running `mn` | Not run with `sudo` | Always prefix Mininet commands with `sudo` |

---

## Key Concepts Reference

| Concept | Description |
|---|---|
| **SDN** | Architecture separating control plane (controller) from data plane (switches) |
| **OpenFlow** | Protocol used by controllers to program switch flow tables |
| **Mininet** | Network emulator using Linux network namespaces + Open vSwitch |
| **Topo** | Mininet Python class describing hosts, switches, and links |
| **TCLink** | Link class enabling `tc`/`netem` parameters (bw, delay, loss) |
| **Controller (c0)** | Default reference controller managing switch flow tables |
| **NAT** | Network Address Translation — gives Mininet hosts internet access |
| **pingall** | CLI command for all-pairs connectivity testing |
| **iperf** | Tool for measuring achievable TCP/UDP throughput |
| **depth / fanout** | Tree topology parameters controlling levels and branching factor |

---

## License

MIT License — see [LICENSE](LICENSE)

---

## References

- [Mininet Walkthrough — Official Documentation](http://mininet.org/walkthrough/)
- [Mininet Python API Reference](http://mininet.org/api/)
- [Open vSwitch Documentation](https://www.openvswitch.org/)
- [OpenFlow Switch Specification](https://opennetworking.org/software-defined-standards/specifications/)
- Lab 7 — Understanding SDN Capability Using Mininet (Course Lab Material)
