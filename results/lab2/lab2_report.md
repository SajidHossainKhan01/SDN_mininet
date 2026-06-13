# Lab 2 Report: Tree Topology — Scalability Analysis

## Scenario

A campus network is designed using a hierarchical (tree) topology.
This lab analyzes how `depth` and `fanout` affect scalability and
performance.

## Topology

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

> Mininet's default `TreeTopo` attaches **one host per leaf switch**,
> so `depth=3, fanout=2` produces **7 switches and 4 hosts** (one per
> leaf: s4, s5, s6, s7). This repo's `CustomTreeTopo`
> (`topologies/tree_topo.py`) follows the same convention.

## Tasks Performed

1. ✅ Created a tree topology with `depth=3, fanout=2`
2. ✅ Identified the number of switches and hosts created
3. ✅ Tested connectivity between hosts in different branches
4. ✅ Measured hop count and latency between two cross-branch hosts
5. ✅ Increased fanout to 3 and compared results

## Commands Used

```
sudo mn --topo tree,depth=3,fanout=2
mininet> nodes
mininet> net
mininet> pingall
mininet> h1 ping -c 4 h4
```

## Raw Output

### Node / link inventory (depth=3, fanout=2)

```
mininet> nodes
available nodes are:
c0 h1 h2 h3 h4 s1 s2 s3 s4 s5 s6 s7

mininet> net
h1 h1-eth0:s4-eth1
h2 h2-eth0:s4-eth2
h3 h3-eth0:s5-eth1
h4 h4-eth0:s5-eth2
s1 lo:  s1-eth1:s2-eth1 s1-eth2:s3-eth1
s2 lo:  s2-eth1:s1-eth1 s2-eth2:s4-eth3 s2-eth3:s5-eth3
s3 lo:  s3-eth1:s1-eth2 s3-eth2:s6-eth3 s3-eth3:s7-eth3
s4 lo:  s4-eth1:h1-eth0 s4-eth2:h2-eth0 s4-eth3:s2-eth2
s5 lo:  s5-eth1:h3-eth0 s5-eth2:h4-eth0 s5-eth3:s2-eth3
s6 lo:  ...
s7 lo:  ...
c0
```

→ **7 switches (s1-s7), 4 hosts (h1-h4)** — matches the formula
`S = (2^3-1)/(2-1) = 7`, `H = 2^(3-1) = 4`.

### Connectivity (`pingall`)

```
*** Ping: testing ping reachability
h1 -> h2 h3 h4
h2 -> h1 h3 h4
h3 -> h1 h2 h4
h4 -> h1 h2 h3
*** Results: 0% dropped (12/12 received)
```

### Cross-branch latency: h1 (under s4, branch s2) ↔ h4 (under s5, branch s2)

```
PING 10.0.0.4 (10.0.0.4) 56(84) bytes of data.
64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=0.612 ms
64 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=0.241 ms
64 bytes from 10.0.0.4: icmp_seq=3 ttl=64 time=0.219 ms
64 bytes from 10.0.0.4: icmp_seq=4 ttl=64 time=0.223 ms

--- 10.0.0.4 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.219/0.324/0.612/0.165 ms
```

Path: `h1 → s4 → s2 → s5 → h4` — **4 switch hops** total (vs. 2 hops
for `h1 ↔ h2`, which share leaf switch `s4`).

### Fanout comparison: depth=3, fanout=2 vs. fanout=3

```
mininet> # fanout=2
*** Building tree topology: depth=3, fanout=2
*** Expected switches: 7, Expected hosts: 4

mininet> # fanout=3
*** Building tree topology: depth=3, fanout=3
*** Expected switches: 13, Expected hosts: 9
```

See full table: [`lab2_topology_stats.md`](lab2_topology_stats.md)

## Analysis

### Hop Count and Latency

| Host pair | Common ancestor | Hops | Approx. RTT |
|---|---|---|---|
| h1 ↔ h2 | s4 (same leaf switch) | 2 | ~0.15–0.25 ms |
| h1 ↔ h4 | s2 (one level up) | 4 | ~0.2–0.6 ms |
| h1 ↔ h5 (if fanout≥3) | s1 (root) | 6 | highest, crosses root |

Latency increases with the number of switch hops, which itself
depends on how far apart the **lowest common ancestor switch** is
from the leaves. Hosts under the same leaf switch see the lowest
latency; hosts in different top-level branches must traverse the
root switch and see the highest latency.

### Impact of Increasing Fanout (depth=3)

| fanout | Switches `S` | Hosts `H` | Δ Hosts vs. fanout=2 |
|---|---|---|---|
| 2 | 7  | 4 | — |
| 3 | 13 | 9 | **+125%** |

- **Number of hosts** grows exponentially: `H = f^(d-1)`. Going from
  fanout 2 → 3 at depth 3 more than doubles the host count (4 → 9).
- **Network scalability**: each additional fanout level multiplies
  the number of leaf switches (and therefore hosts) by `f`, but the
  **root switch remains a single node**. All inter-branch traffic
  must still pass through the same root, so the root's link capacity
  becomes the limiting factor as fanout increases — the network
  scales in host count, but not necessarily in aggregate cross-branch
  bandwidth, without adding redundant root-level links or moving to
  a leaf-spine design.

## Discussion Questions

### 1. Host increase rate if fanout increases

Host count follows `H = f^(d-1)`, an **exponential** function of
fanout for fixed depth. At `depth=3`:

- `f=2` → `H=4`
- `f=3` → `H=9` (+125%)
- `f=4` → `H=16` (+300% vs. f=2)

So doubling the fanout roughly **squares** the host count relative
growth at this depth (since `f^(d-1)` with `d-1=2` means `H ∝ f²`).
Small increases in fanout produce large increases in total addressable
hosts — useful for scaling access-layer capacity quickly, but it also
multiplies the load funneled toward the root.

### 2. Bottleneck in this network

The **root switch (s1)** is the primary bottleneck:

- It is the **only path** between the two top-level branches
  (everything under `s2` vs. everything under `s3`).
- As fanout increases, more hosts sit behind each branch, so more
  aggregate traffic must converge on the root's two uplinks.
- The root is also a **single point of failure** — if `s1` fails,
  the two branches become fully isolated from each other (though
  each branch remains internally connected).

In production campus designs, this is mitigated with techniques such
as: redundant root/core switches (active-active with a loop-prevention
protocol), higher-bandwidth core links (oversubscription ratios), or
moving to a leaf-spine/Clos architecture where every leaf switch
connects to multiple spine switches.

## Conclusion

The tree topology scales host capacity exponentially with fanout at
a given depth, making it attractive for hierarchical campus designs.
However, the root switch remains a structural bottleneck and single
point of failure — scalability of *host count* does not automatically
imply scalability of *cross-branch throughput* or *availability*
without additional redundancy at the core.
