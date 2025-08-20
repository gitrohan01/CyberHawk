#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="./reports/info_gathering/whatweb"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_whatweb.txt"
whatweb "$1" > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
