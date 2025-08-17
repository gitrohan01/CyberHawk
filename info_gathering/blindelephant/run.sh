#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/blindelephant"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_blindelephant.txt"
blindelephant.py -u "$1" > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
