#!/bin/bash
# lab1_linear_experiment.sh
# Wrapper for the Python-based Lab 1 experiment driver.
#
# Usage: ./lab1_linear_experiment.sh

set -e

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo "[*] Running Lab 1: Linear Topology - Latency & Failure Analysis"
sudo python3 "$(dirname "$0")/lab1_linear_experiment.py"
