#!/usr/bin/python3

# no - output a string repeatedly until killed

import sys

help_message = """Usage: yes [STRING]...
  or:  yes OPTION
Repeatedly output a line with all specified STRING(s), or 'y'.

      --help        display this help and exit
      --version     output version information and exit
"""
version_message = """no (pythonutils) 2022.07.23
Written by John Crawford"""
args = " ".join(sys.argv[1:])


for x in sys.argv:
    if x == "--help":
        print(help_message)
        exit(0)
    elif x == "--version":
        print(version_message)
        exit(0)


if not args:
    args = "n"

while True:
    try:
        print(args)
    except KeyboardInterrupt:
        break

