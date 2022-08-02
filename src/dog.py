#!/usr/bin/python3

# dog - concatenate files and print on the standard output

import sys
import os

args = sys.argv[1:]
program = sys.argv[0]
options = ["A", "b", "n", "E", "T", "u"]

help_message = f"""Usage: {program} [OPTION]... [FILE]...
Concatenate FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.

  -A, --show-all           equivalent to -ET
  -b, --number-nonblank    number nonempty output lines, overrides -n
  -E, --show-ends          display $ at end of each line
  -n, --number             number all output lines
  -T, --show-tabs          display TAB characters as ^I
  -u                       (ignored)
      --help        display this help and exit
      --version     output version information and exit

Examples:
  {program} f - g  Output f's contents, then standard input, then g's contents.
  {program}        Copy standard input to standard output.
"""
version_message = f"""dog (pyutils) 2022.08.02
Written by John Crawford"""


#stdin
def stdin():
        while True:
            try:
                print(input())
            except EOFError:
                break
            except KeyboardInterrupt:
                exit(0)


#print file line by line
def output(file, arg_list):
    c = 1
    line_end = None
    line_count = ""

    with open(file) as f:
        line = f.readline()
        
        while line:
            for x in arg_list:
                match x:
                    case "n":
                        line_count = f"{c:>6}  "
                    case "T":
                        line = line.replace("\t", "^I")
                    case "E":
                        line_end = "$\n"
                        
            if line == "\n" and "b" in arg_list:
                line_count = ""
                c -= 1

            line = line.rstrip("\n")
            print(f"{line_count}{line}", end=line_end)
            line = f.readline()
            c += 1

def get_args(): #parse command line arguments
    args = sys.argv[1:]
    arg_list, file_list = [], []

    for x in arg_list: #exit with invalid options
        if x not in options:
            print("{0}: invalid optn -- '{1}'\nTry '{2}' --help' for more information.".format(program, x.replace("-", ""), program))

    for x in args:
        if x.startswith("-") and not x.endswith("-"):
            if "--help" in x:
                print(help_message)
                exit(0)
            if "--version" in x:
                print(version_message)
                exit(0)
            if "--show-all" in x or "A" in x:
                arg_list.append("E")
                arg_list.append("T")
            if "--show-tabs" in x or "T" in x:
                arg_list.append("T")
            if "--show-ends" in x or "E" in x:
                arg_list.append("E")
            if "--number-nonblank" in x or "b" in x:
                arg_list.append("b")
                arg_list.append("n")
            if "--number" in x or "n" in x:
                arg_list.append("n")
        else:
            file_list.append(x)

    return arg_list, file_list


def main():
    arg_list, file_list = get_args()

    if sys.argv[1:] == []: #read standard input if no file is provided
        stdin()

    for x in file_list: #loop through files
        if x == "-":
            stdin()
        else:
            try:
                output(x, arg_list)
            except FileNotFoundError:
                print(f"{file}: {x}: No such file or directory")
                exit(1)


if __name__ == "__main__":
    main()
