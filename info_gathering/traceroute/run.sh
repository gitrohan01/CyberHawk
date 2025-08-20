#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <host>"
  exit 1
fi

OUTPUT_DIR="./reports/info_gathering/traceroute"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_traceroute.txt"
traceroute "$1" > "$OUTPUT_FILE"

echo "Traceroute results saved to $OUTPUT_FILE"

