#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

host "$1"

