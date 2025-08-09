#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/dig"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_dig.txt"
dig "$1" > "$OUTPUT_FILE"

echo "DIG results saved to $OUTPUT_FILE"

