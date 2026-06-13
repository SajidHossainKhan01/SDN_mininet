#!/bin/bash
# run_linear.sh
# Starts a linear topology with N hosts/switches and NAT enabled
# for internet access from inside Mininet hosts.
#
# Usage: ./run_linear.sh [N]

set -e

N="${1:-4}"

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Starting linear topology: ${N} hosts, ${N} switches, with NAT..."
sudo mn --topo "linear,${N}" --nat

# Example once inside the CLI:
#   mininet> h1 ping -c 1 www.google.com
