#!/bin/bash
# run_single.sh
# Starts a single-switch topology with N hosts (default N=3).
#
# Usage: ./run_single.sh [N]

set -e

N="${1:-3}"

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Starting single topology: 1 switch, ${N} hosts..."
sudo mn --topo "single,${N}"
