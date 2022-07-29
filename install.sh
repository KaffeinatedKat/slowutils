#!/bin/bash

path=/usr/local/bin/

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cp src/dog.py "$path"dog
cp src/no.py "$path"no