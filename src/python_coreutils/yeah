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
version_message = f"""yeah (pyutils) 2022.08.02
Written by John Crawford"""


def get_args():
    args = " ".join(sys.argv[1:])
    for x in sys.argv:
        match x:
            case "--help":
                print(help_message)
                exit(0)
            case "--version":
                print(version_message)
                exit(0)
    return args


def main():
    args = get_args()

    if not args:
        args = "y"
    while True:
        try:
            print(args)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
