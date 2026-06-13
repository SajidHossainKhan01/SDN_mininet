#!/bin/bash
# run_regression_tests.sh
# Runs Mininet's built-in self-contained regression tests:
#   - pingpair: minimal topology, all-pairs ping
#   - iperf:    minimal topology, TCP bandwidth test (~10s)
#
# Usage: ./run_regression_tests.sh

set -e

echo "[*] Cleaning up any previous Mininet state..."
sudo mn -c > /dev/null 2>&1 || true

echo ""
echo "=== Running pingpair regression test ==="
sudo mn --test pingpair

echo ""
echo "=== Running iperf regression test (takes ~10s) ==="
sudo mn --test iperf

echo ""
echo "[*] Regression tests complete."

# NOTE: 'pingair' is NOT a valid option. The correct name is 'pingpair'.
# Valid --test values: none, build, all, iperf, pingpair, iperfudp, pingall
