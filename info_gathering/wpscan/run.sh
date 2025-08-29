#!/bin/sh
exec wpscan "$@"

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

wpscan --url "$1" --no-update
