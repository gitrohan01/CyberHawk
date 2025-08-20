#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="./reports/info_gathering/wappalyzer"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_wappalyzer.txt"
npx wappalyzer "$1" > "$OUTPUT_FILE" 2>&1

cat "$OUTPUT_FILE"
