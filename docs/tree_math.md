# Tree Topology: Switch and Host Count Formulas

For a Mininet `TreeTopo(depth=d, fanout=f)`:

## Definitions

- **depth (d):** number of switch levels in the tree, root at level 1
  down to leaf switches at level `d`.
- **fanout (f):** number of child switches each switch connects to
  (branching factor), and (in this repo's `CustomTreeTopo`) the
  number of hosts attached to each leaf switch.

## Formulas

### Number of switches

$$
S = \sum_{i=0}^{d-1} f^{i} = \frac{f^{d} - 1}{f - 1} \quad (f \neq 1)
$$

If `f = 1`, the tree degenerates into a chain: `S = d`.

### Number of leaf switches

$$
L = f^{d-1}
$$

### Number of hosts

Mininet's `TreeTopo` attaches **one host per leaf switch**, so:

$$
H = f^{d-1}
$$

(This repo's `CustomTreeTopo` generalizes this to `fanout` hosts per
leaf switch if desired — adjust `_add_tree` accordingly.)

## Worked Examples

| depth (d) | fanout (f) | Switches `S` | Leaf switches `L` | Hosts `H` |
|---|---|---|---|---|
| 2 | 2 | 3  | 2  | 2  |
| 3 | 2 | 7  | 4  | 4  |
| 3 | 3 | 13 | 9  | 9  |
| 4 | 2 | 15 | 8  | 8  |
| 2 | 3 | 4  | 3  | 3  |

### Calculation walkthrough: depth=3, fanout=2

$$
S = \frac{2^3 - 1}{2 - 1} = \frac{7}{1} = 7
$$

$$
L = H = 2^{(3-1)} = 4
$$

→ **7 switches, 4 hosts** — matches Mininet's `tree,depth=3,fanout=2`.

### Calculation walkthrough: depth=3, fanout=3

$$
S = \frac{3^3 - 1}{3 - 1} = \frac{26}{2} = 13
$$

$$
H = 3^{(3-1)} = 9
$$

→ **13 switches, 9 hosts**.

## Growth Rate Observation

Going from `fanout=2` to `fanout=3` at `depth=3`:

- Hosts: 4 → 9 (a **125% increase**)
- Switches: 7 → 13 (an **86% increase**)

Host count grows **exponentially** with fanout (`H = f^(d-1)`), while
the **root switch remains a single node** through which all
inter-branch traffic must pass — making it both the primary
scalability bottleneck and a single point of failure in a pure tree
design (mitigated in practice with spanning-tree redundancy or
leaf-spine architectures).

See [`results/lab2/lab2_topology_stats.md`](../results/lab2/lab2_topology_stats.md)
for the experimental verification.
