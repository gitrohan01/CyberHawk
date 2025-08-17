#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/wpscan"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_wpscan.txt"
wpscan --url "$1" --no-update > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
