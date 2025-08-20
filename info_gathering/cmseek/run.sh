#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <url>"
  exit 1
fi

OUTPUT_DIR="./reports/info_gathering/cmseek"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${1}_cmseek.txt"

# ✅ Correct relative path
python3 ./info_gathering/cmseek/cmseek.py -u "$1" --random-agent > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
