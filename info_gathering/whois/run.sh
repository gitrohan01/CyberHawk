#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

OUTPUT_FILE="/app/output/${1}_whois.txt"
whois "$1" > "$OUTPUT_FILE"

echo "WHOIS results saved to $OUTPUT_FILE"

