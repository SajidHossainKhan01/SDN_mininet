# Lab 2 — Topology Statistics (Switches & Hosts)

Computed using the formulas in [`docs/tree_math.md`](../../docs/tree_math.md):

$$
S = \frac{f^{d} - 1}{f - 1} \qquad H = f^{d-1}
$$

## depth = 3 (Lab 2 default)

| fanout (f) | Switches (S) | Leaf switches (L) | Hosts (H) |
|---|---|---|---|
| 1 | 3  | 1 | 1  |
| 2 | 7  | 4 | 4  |
| 3 | 13 | 9 | 9  |
| 4 | 21 | 16 | 16 |

## depth = 2

| fanout (f) | Switches (S) | Leaf switches (L) | Hosts (H) |
|---|---|---|---|
| 2 | 3  | 2 | 2  |
| 3 | 4  | 3 | 3  |
| 4 | 5  | 4 | 4  |

## depth = 4

| fanout (f) | Switches (S) | Leaf switches (L) | Hosts (H) |
|---|---|---|---|
| 2 | 15 | 8  | 8  |
| 3 | 40 | 27 | 27 |

## Growth Rate: fanout 2 → 3 (depth = 3)

| Metric | fanout=2 | fanout=3 | % Change |
|---|---|---|---|
| Switches | 7 | 13 | +85.7% |
| Hosts | 4 | 9 | +125.0% |

**Conclusion:** at fixed depth, host count growth (`+125%`) outpaces
switch count growth (`+85.7%`) when fanout increases from 2 to 3 —
each additional branch adds proportionally more leaf capacity than
intermediate switching infrastructure, but concentrates more traffic
onto the same root switch.
