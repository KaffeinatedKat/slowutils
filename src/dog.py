#!/usr/bin/python3

# dog - concatenate files and print on the standard output

import sys
import os

args = sys.argv[1:]
file = sys.argv[0]
options = ["A", "b", "n", "E", "T", "u"]
arg_list = []
new_args = []
line_end = None
line_count = ""

help_message = f"""Usage: {file} [OPTION]... [FILE]...
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
  {file} f - g  Output f's contents, then standard input, then g's contents.
  {file}        Copy standard input to standard output.
"""
version_message = f"""dog (pyutils) 2022.07.29
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
def output(file, line_count, line_end):
    c = 1
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


#parse command line arguments
for x in args:
    if x.startswith("-") == True and x.endswith("-") == False:
        if x == "--help":
            print(help_message)
            exit(0)
        elif x == "--version":
            print(version_message)
            exit(0)
        elif x == "--show-all" or x == "-A":
            arg_list.append("E")
            arg_list.append("T")
        elif x == "--show-tabs":
            arg_list.append("T")
        elif x == "--show-ends":
            arg_list.append("E")
        elif x == "--number-nonblank" or x == "-b":
            arg_list.append("b")
            arg_list.append("n")
        elif x == "--number":
            art_list.append("n")
        else:
            arg_list += x.replace("-", "")       
    else:
        new_args += [x]


#exit with invalid options
for x in arg_list:
    if x not in options:
        print("{0}: invalid option -- '{1}'\nTry '{2} --help' for more information.".format(file, x.replace("-", ""), file))
        exit(1)


#read standard input if no file is provided
if "".join(new_args) == "":
    stdin()


#loop through files
for x in new_args:
    if x == "-":
        stdin()
    else:
        try:
            output(x, line_count, line_end)
        except FileNotFoundError:
            print(f"{file}: {x}: No such file or directory")
            exit(1)

