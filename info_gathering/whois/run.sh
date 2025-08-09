#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/whois"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_whois.txt"
whois "$1" > "$OUTPUT_FILE"

echo "WHOIS results saved to $OUTPUT_FILE"