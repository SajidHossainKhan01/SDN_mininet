# Mininet Topology Types

Mininet's built-in topology generators cover the most common
network shapes used for SDN experimentation. This document explains
each one, its command syntax, and when it's useful.

## 1. Minimal

The default topology: **2 hosts, 1 switch, 1 controller**.

```bash
sudo mn --topo minimal
```

```
        c0
         |
        s1
       /  \
     h1    h2
```

**Use case:** quickest sanity check that Mininet, Open vSwitch, and
the controller are working correctly.

---

## 2. Single

**1 switch, N hosts** — a star topology.

```bash
sudo mn --topo single,5
```

```
            c0
             |
            s1
       / | | | \
     h1 h2 h3 h4 h5
```

**Use case:** testing broadcast/multicast behavior, switch MAC
learning with many hosts, or simple load tests where all hosts
share one switch.

---

## 3. Reversed

Same as `single`, but with host/switch numbering reversed in the
internal data structures. Functionally equivalent topology shape
to `single`, used to test naming/ordering edge cases.

```bash
sudo mn --topo reversed,3
```

---

## 4. Linear

**N hosts and N switches**, connected in a chain — each switch has
exactly one host, and switches are linked sequentially.

```bash
sudo mn --topo linear,4
```

```
h1    h2    h3    h4
 |     |     |     |
s1 -- s2 -- s3 -- s4
```

**Use case:** studying latency accumulation across multiple hops,
and analyzing single-point-of-failure risk — see [Lab 1](../results/lab1/lab1_report.md).

---

## 5. Tree

A **hierarchical, multilevel topology** with `depth` levels and
`fanout` children per switch. Hosts are attached only at the leaf
level (one host per leaf switch in Mininet's default implementation,
though this repo's `CustomTreeTopo` supports `fanout` hosts per leaf).

```bash
sudo mn --topo tree,depth=3,fanout=2
```

```
                    s1 (root)
                 /              \
              s2                  s3
            /    \              /    \
          s4      s5          s6      s7
         /  \    /  \        /  \    /  \
       h1   h2  h3  h4      h5  h6  h7  h8
```

**Use case:** modeling hierarchical/campus networks (core →
aggregation → access layers); analyzing scalability vs. fanout —
see [Lab 2](../results/lab2/lab2_report.md) and [tree math](tree_math.md).

---

## Summary Table

| Topology | Hosts | Switches | Shape | Best for |
|---|---|---|---|---|
| Minimal | 2 | 1 | Star | Sanity checks |
| Single | N | 1 | Star | Broadcast / MAC learning tests |
| Reversed | N | 1 | Star (reordered) | Naming/ordering edge cases |
| Linear | N | N | Chain | Latency vs. hop count, SPOF analysis |
| Tree | f^(d-1) | (f^d-1)/(f-1) | Hierarchical tree | Scalability, campus network design |
