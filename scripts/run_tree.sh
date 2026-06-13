#!/bin/bash
# run_tree.sh
# Starts a tree topology with configurable depth and fanout.
#
# Usage: ./run_tree.sh [depth] [fanout]
# Example: ./run_tree.sh 3 2

set -e

DEPTH="${1:-3}"
FANOUT="${2:-2}"

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Starting tree topology: depth=${DEPTH}, fanout=${FANOUT}..."
sudo mn --topo "tree,depth=${DEPTH},fanout=${FANOUT}"
