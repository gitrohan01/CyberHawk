#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: sh run.sh <domain>"
  exit 1
fi

ping -c 4 "$1"

