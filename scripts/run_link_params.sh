#!/bin/bash
# run_link_params.sh
# Starts a topology with link-level bandwidth/delay applied to
# every link via TCLink (tc/netem).
#
# Usage: ./run_link_params.sh [bw_mbps] [delay_ms]
# Example: ./run_link_params.sh 1000 10

set -e

BW="${1:-1000}"
DELAY="${2:-10}"

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Starting default topology with link params: bw=${BW}Mbit, delay=${DELAY}ms..."
sudo mn --link "tc,bw=${BW},delay=${DELAY}ms"

# Once inside the CLI:
#   mininet> iperf
#   mininet> h1 ping -c 4 h2
#
# Expected RTT with delay=10ms per link: ~40ms
# (request: h1->s1->h2, reply: h2->s1->h1 = 4 link traversals)
