#!/usr/bin/python3

# yeah - output a string repeatedly until killed

import sys

file = sys.argv[0]
help_message = f"""Usage: {file} [STRING]...
  or:  {file} OPTION
Repeatedly output a line with all specified STRING(s), or 'y'.

      --help        display this help and exit
      --version     output version information and exit
"""
version_message = f"""{file} (pythonutils) 2022.07.29
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
    args = "y"

while True:
    try:
        print(args)
    except KeyboardInterrupt:
        break

