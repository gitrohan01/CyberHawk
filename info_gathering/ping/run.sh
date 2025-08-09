#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <host>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/ping"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_ping.txt"
ping -c 4 "$1" > "$OUTPUT_FILE"

echo "Ping results saved to $OUTPUT_FILE"
