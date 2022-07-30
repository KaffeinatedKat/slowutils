#!/usr/bin/python3

# isthatme - print effective userid

import os
import pwd
import sys

file = sys.argv[0]
help_message = f"""Usage: {file} [OPTION]...
Print the user name associated with the current effective user ID.
Same as id -un.

      --help        display this help and exit
      --version     output version information and exit\n"""
version_message = f"""isthatme (pythonutils) 2022.07.29
Written by John Crawford"""

for x in sys.argv:
    match x:
        case "--help":
            print(help_message)
            exit(0)
        case "--version":
            print(version_message)
            exit(0)

try:
    print(pwd.getpwuid(os.getuid())[0])
except:
    print(f"cannot find name for user ID {os.getuid()}")

