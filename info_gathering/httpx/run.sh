#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="./reports/info_gathering/httpx"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_httpx.txt"
echo "$1" | httpx -title -status-code -tech-detect -server -ip > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
