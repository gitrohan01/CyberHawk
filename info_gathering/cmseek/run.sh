#!/bin/sh
exec cmseek.py "$1"

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

python3 cmseek.py "$1"
