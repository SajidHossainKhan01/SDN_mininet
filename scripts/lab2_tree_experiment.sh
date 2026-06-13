#!/bin/bash
# lab2_tree_experiment.sh
# Wrapper for the Python-based Lab 2 experiment driver.
#
# Usage: ./lab2_tree_experiment.sh

set -e

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Running Lab 2: Tree Topology - Scalability Analysis"
sudo python3 "$(dirname "$0")/lab2_tree_experiment.py"
