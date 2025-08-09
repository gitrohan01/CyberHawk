#!/bin/bash
TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi
nslookup "$TARGET"
