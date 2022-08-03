#!/usr/bin/python3

# dog - concatenate files and print on the standard output

import sys
import os

args = sys.argv[1:]
program = sys.argv[0]
options = ["-A", "--show-all", "-b", "--number-nonblank", "-E", "--show-ends", "-n", "--number", "-T", "--show-tabs", "-u", "--help", "--version"]

help_message = f"""Usage: {program} [OPTION]... [FILE]...
Concatenate FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.

  {options[0]},  {options[1]}            equivalent to -ET
  {options[2]},  {options[3]}     number nonempty output lines, overrides -n
  {options[4]},  {options[5]}           display $ at end of each line
  {options[6]},  {options[7]}              number all output lines
  {options[8]},  {options[9]}           display TAB characters as ^I
  {options[10]}                         (ignored)
      {options[11]}        display this help and exit
      {options[12]}     output version information and exit

Examples:
  {program} f - g  Output f's contents, then standard input, then g's contents.
  {program}        Copy standard input to standard output.
"""
version_message = f"""dog (pyutils) 2022.08.02
Written by John Crawford"""


def stdin(line_count, line_end, tab, arg_list, row_count): #standard input
    while True:
        try:
            line = input()
            print(line)

            if "-n" in arg_list or "-b" in arg_list: #show line count
                line_count = f"{row_count:>6}  "
            if line == "" and "-b" in arg_list: #dont count empty lines
                line_count = ""
                row_count -= 1

            row_count += 1
            print("{0}{1}".format(line_count, line.replace("\t", tab)), end=line_end)
        except EOFError:
            break
        except KeyboardInterrupt:
            exit(0)

    return row_count #return row_count for future lines


def output(file, arg_list, tab, line_end, line_count, row_count): #print file line by line
    with open(file) as f:
        line = f.readline().replace("\t", tab)
        
        while line:
            if "-n" in arg_list or "-b" in arg_list:
                line_count = f"{row_count:>6}  "
            if line == "\n" and "-b" in arg_list:
                line_count = ""
                row_count -= 1
            
            line = line.rstrip("\n")
            print(f"{line_count}{line}", end=line_end)
            line = f.readline().replace("\t", tab)
            row_count += 1

    return row_count #return row_count for future lines


def get_args(): #parse command line arguments
    args, arg_list, file_list = [], [], []
    tab = "\t"
    line_end = None
    line_count = ""
    row_count = 1
    
    for x in sys.argv[1:]:
        if x.startswith("--"): #add arguments such as --show-tabs into array as ['--show-tabs']
            args.append(x)
        elif x.startswith("-") and not x.endswith("-"): #add arguments such as -bET into array as ['-b', '-E', '-T']
            for z in list(x):
                if z != "-":
                    args += [f"-{z}"]
        else: #add everything else normally
            args.append(x)
        
    for x in args:
        if x.startswith("-") and not x.endswith("-"): #check for arguments (ex. -b)
            if x not in options: #exit with invalid options
                print("{0}: invalid option -- '{1}'\nTry '{2}' --help' for more information.".format(program, x.replace("-", ""), program))
                exit(1)   

            if "--help" in x:
                print(help_message)
                exit(0)
            if "--version" in x:
                print(version_message)
                exit(0)
            if "--show-all" in x or "A" in x:
                x = "-A"
                line_end = "$\n"
                tab = "^I"
                arg_list += [x]
            if "--show-tabs" in x or "T" in x:
                x = "-T"
                tab = "^I"
                arg_list += [x]
            if "--show-ends" in x or "E" in x:
                x = "-E"
                line_end = "$\n"
                arg_list += [x]
            if "--number-nonblank" in x or "b" in x:
                x = "-b"
                arg_list += [x]
            if "--number" in x or "n" in x:
                x = "-n"
                arg_list += [x]
        else: #everything else goes to into output()
            file_list.append(x)

    return arg_list, file_list, tab, line_end, line_count, row_count


def main():
    arg_list, file_list, tab, line_end, line_count, row_count = get_args()
    
    if sys.argv[1:] == []: #read stdin if no file is provided
        stdin(line_count, line_end, tab, arg_list, row_count)

    for x in file_list: #loop through files
        if x == "-": #stdin if file is '-'
            row_count = stdin(line_count, line_end, tab, arg_list, row_count)
        else:
            try:
                row_count = output(x, arg_list, tab, line_end, line_count, row_count)
            except FileNotFoundError:
                print(f"{program}: {x}: No such file or directory")
                exit(1)


if __name__ == "__main__":
    main()
