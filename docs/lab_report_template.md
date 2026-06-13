# Lab Report Template

Use this template to document new Mininet experiments consistently.

---

## Title

`Lab N: <Short descriptive title>`

## Scenario

_Describe the network design question being investigated and its
real-world relevance (e.g. campus network, ISP backbone, IoT mesh)._

## Topology

```bash
sudo mn --topo <type>,<params>
```

_Include an ASCII diagram of the topology._

## Tasks Performed

1. ...
2. ...
3. ...

## Commands Used

```
mininet> pingall
mininet> h1 ping -c 4 hN
mininet> iperf h1 hN
mininet> link sX sY down
```

## Raw Output

```
<paste relevant CLI output here>
```

## Analysis

### Connectivity

_Pingall results — % packet loss, any unreachable pairs._

### Latency (RTT)

_How does RTT change with hop count / topology depth?_

### Throughput

_iperf results — bandwidth achieved, any bottlenecks._

### Fault Tolerance

_What happens when a link/switch fails? Is the topology resilient?_

## Discussion Questions

_Answer any "Try yourself" / "Comment on" questions from the lab
sheet here._

## Conclusion

_Summarize the key takeaway — e.g. "Topology X is unsuitable for Y
because of Z; an alternative design would be..."_
