#!/usr/bin/env bash
for f in src/solutions/*.py; do
  echo -e "\nRunning $f:"
  python "$f"
done
