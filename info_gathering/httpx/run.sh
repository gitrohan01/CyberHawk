#!/bin/sh
exec httpx "$@"

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

httpx -silent -status-code -title "$1"
