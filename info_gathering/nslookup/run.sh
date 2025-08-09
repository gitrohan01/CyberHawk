#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/nslookup"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_nslookup.txt"
nslookup "$1" > "$OUTPUT_FILE"

echo "NSLOOKUP results saved to $OUTPUT_FILE"

