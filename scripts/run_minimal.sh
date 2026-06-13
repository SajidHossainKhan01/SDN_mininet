#!/bin/bash
# run_minimal.sh
# Starts Mininet's default minimal topology: 2 hosts, 1 switch, 1 controller.
#
# Usage: ./run_minimal.sh

set -e

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Starting minimal topology (2 hosts, 1 switch)..."
sudo mn --topo minimal
