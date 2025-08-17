#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="/app/reports/info_gathering/cmseek"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_cmseek.txt"
python3 cmseek.py -u "$1" --random-agent > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
