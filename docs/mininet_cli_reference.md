# Mininet CLI Reference

A complete reference of the Mininet CLI commands used in this lab.

## Connecting to the Mininet VM

```bash
ssh mininet@<vm-ip-address>
# Username: mininet
# Password: mininet
```

## Starting a Topology

```bash
sudo mn                       # default minimal topology
sudo mn --topo minimal        # 2 hosts, 1 switch
sudo mn --topo single,3       # 1 switch, 3 hosts
sudo mn --topo reversed,3      # like single, reversed numbering
sudo mn --topo linear,3       # 3 hosts, 3 switches in a chain
sudo mn --topo tree,depth=3,fanout=2
```

## Inspection Commands

| Command | Purpose |
|---|---|
| `help` | List all documented CLI commands |
| `help <topic>` | Help for a specific command |
| `nodes` | List all nodes (hosts, switches, controllers) |
| `net` | List all links between nodes |
| `dump` | Dump detailed info (IP, PID) for every node |
| `links` | Show link status (up/down) |
| `ports` | Show switch port mappings |

### Example output

```
mininet> nodes
available nodes are:
c0 h1 h2 s1

mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0
c0

mininet> dump
<Host h1: h1-eth0:10.0.0.1 pid=1442>
<Host h2: h2-eth0:10.0.0.2 pid=1445>
<OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=1451>
<Controller c0: 127.0.0.1:6653 pid=1435>
```

## Running Commands on Nodes

If the first word typed is a node name, the rest of the line runs
on that node's network namespace:

```
mininet> h1 ifconfig -a
mininet> h1 ping -c 1 h2
mininet> s1 ovs-ofctl dump-flows s1
```

## Connectivity Testing

```
mininet> h1 ping -c 1 h2      # single ping
mininet> pingall              # all-pairs ping
mininet> pingallfull          # all-pairs ping, verbose
mininet> iperf                # TCP bandwidth between two default hosts
mininet> iperf h1 h3          # TCP bandwidth between specific hosts
mininet> iperfudp 10M h1 h2   # UDP bandwidth test at 10 Mbps
```

## Fault Tolerance / Link Manipulation

```
mininet> link s1 h1 down      # disable both halves of the veth pair
mininet> h1 ping h2            # connect: Network is unreachable
mininet> link s1 h1 up         # restore the link
mininet> h1 ping h2            # connectivity restored
```

When a link is brought down, switches receive an **OpenFlow Port
Status Change** notification from the controller.

## Terminals and Python

```
mininet> xterm h1             # open an xterm for host h1
mininet> py net.hosts          # evaluate a Python expression
mininet> py h1.IP()
```

## Exiting

```
mininet> exit
```

If Mininet exits uncleanly, always clean up before the next run:

```bash
sudo mn -c
```

## Advanced Startup Options

### NAT for Internet Access

```bash
sudo mn --topo=linear --nat -i 10.10.10.0/24
sudo mn --topo=linear,4 --nat
```

```
mininet> h1 ping -c 1 www.google.com
```

### Link Parameters (bandwidth, delay)

```bash
sudo mn --link tc,bw=1000,delay=10ms
```

```
mininet> iperf
mininet> h1 ping -c 4 h2
```

With a 10ms delay per link, an ICMP echo between two hosts on the
same switch traverses 4 link segments (2 each way), giving an
expected RTT of approximately **40ms**.

### Regression Tests

```bash
sudo mn --test pingpair    # build, all-pairs ping, teardown
sudo mn --test iperf       # build, run iperf, teardown (~10s)
```

> ⚠️ `pingair` is **not** a valid test name. The correct value is
> `pingpair`. Valid options:
> `none, build, all, iperf, pingpair, iperfudp, pingall`
