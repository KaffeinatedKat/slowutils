#!/usr/bin/python3

# dog - concatenate files and print on the standard print_line

import sys
import os



class Variables:
    def __init__(self):
        self.program = sys.argv[0]
        self.args = sys.argv[1:]
        self.options = ["-A", "--show-all", "-b", "--number-nonblank", "-E", "--show-ends", "-n", "--number", "-T", "--show-tabs", "-u", "-s", "--squeeze-blank", "-v", "--help", "--version"]
        self.line_count = 1
        self.show_tabs = "\t"
        self.show_ends = "\n"
        self.surpress_empty = False
        self.show_nonprinting = False
        self.args = []
        self.arg_list = []
        self.file_list = []
        self.help_message = f"""Usage: {self.program} [OPTION]... [FILE]...
Concatenate FILE(s) to standard print_line.

With no FILE, or when FILE is -, read standard input.

  {self.options[0]},  {self.options[1]}            equivalent to -ET
  {self.options[2]},  {self.options[3]}     number nonempty print_line lines, overrides -n
  {self.options[4]},  {self.options[5]}           display $ at end of each line
  {self.options[6]},  {self.options[7]}              number all print_line lines
  {self.options[11]}, {self.options[12]}        suppress repeated empty output lines
  {self.options[8]},  {self.options[9]}           display TAB characters as ^I
  {self.options[10]}                         (ignored)
      {self.options[13]}        display this help and exit
      {self.options[14]}     print_line version information and exit

Examples:
  {self.program} f - g  Output f's contents, then standard input, then g's contents.
  {self.program}        Copy standard input to standard print_line.
"""
        self.version_message = f"""dog (pyutils) 2022.09.07
Written by John Crawford"""



class Path:
    def __init__(self):
        self.last_line = ""
        self.current_line = ""
        self.line_count = 1
        self.show_line_count = ""
        self.path = ""


    def count_line(self, Vars):
        if "-n" in Vars.arg_list or "-b" in Vars.arg_list:
            self.show_line_count = f"{self.line_count:>6}  "
        if self.current_line == "" and "-b" in Vars.arg_list: #dont count empty lines
            self.show_line_count = ""
            self.line_count -= 1
        self.line_count += 1
       

    def line_history(self):
        self.last_line = self.current_line
        self.current_line = self.next_line


    def print_line(self, Vars): #print file line by line
        with open(self.path, mode="rb") as f: # show_nonprinting, this shit works as is, please never touch this unreadable mess again
            self.current_line = bytearray()
            self.last_line = bytearray()
            self.count_line(Vars)
            byte = f.read(1)

            while byte:   
                if Vars.show_nonprinting:
                    if byte == b'\x09':
                        self.current_line += b'\t'
                    elif b'\x00' <= byte <= b'\x08' or b'\x0a' <= byte <= b'\x1f':
                        if byte != b'\x0a':
                            self.current_line += str.encode('^') + (int.from_bytes(byte, "big") + 64).to_bytes(1, "big")
                    elif b'\x20' <= byte <= b'\x7e':
                        self.current_line += byte
                    elif byte == b'\x7f':
                        self.current_line += str.encode('^?')
                    elif b'\x80' <= byte <= b'\x9f':
                        self.current_line += str.encode('M-^') + (int.from_bytes(byte, "big") - 64).to_bytes(1, "big")
                    elif b'\xa0' <= byte <= b'\xfe':
                        self.current_line += str.encode('M-') + (int.from_bytes(byte, "big") - 128).to_bytes(1, "big")
                    else:
                        self.current_line += str.encode('M-^?')
                else:
                    if b'\x20' <= byte <= b'\x7e':
                        self.current_line += byte

                if byte == b'\n': # line has ended
                    if not Vars.surpress_empty:
                        print(f"{self.show_line_count}{self.current_line.decode()}", end=Vars.show_ends)
                    else:
                        if self.current_line == bytearray(b'') and self.last_line == bytearray(b''):
                            self.line_count -= 1
                        else:
                            print(f"{self.show_line_count}{self.current_line.decode()}", end=Vars.show_ends)

                    self.last_line = self.current_line
                    self.current_line = bytearray()  
                    self.count_line(Vars)
                byte = f.read(1)

            if Vars.show_nonprinting:
                print(f"{self.show_line_count}{self.current_line.decode()}", end="")

                


        #else:
            #with open(self.path, mode=self.mode) as f:
                #self.current_line = f.readline().replace("\t", Vars.show_tabs)
                #while self.current_line:
                    #self.next_line = f.readline().replace("\t", Vars.show_tabs)  
                    #self.current_line = self.current_line.rstrip("\n")
                    #self.count_line(Vars)

                    #if not Vars.surpress_empty:
                    #    print(f"{self.show_line_count}{self.current_line}\r", end=Vars.show_ends)
                    #elif Vars.surpress_empty:
                        #if self.last_line == "" and self.current_line == "": # if current and last lines are empty, dont print current blank line
                       #     self.line_count -= 1 # dont count surpressed lines
                      #  else:
                     #       print(f"{self.show_line_count}{self.current_line}\r", end=Vars.show_ends)

                    #self.line_history()



def stdin(Vars, File): #standard input
    File.last_line = None
    while True:
        try:
            File.current_line = input()
            File.count_line(Vars)
            if not Vars.surpress_empty:
                print(f"{File.show_line_count}{File.current_line}\r", end=Vars.show_ends)
            elif Vars.surpress_empty:
                if File.last_line == "" and File.current_line == "": # if current and last lines are empty, dont print current blank line
                    File.line_count -= 1 # dont count surpressed lines
                else:
                    print(f"{File.show_line_count}{File.current_line}\r", end=Vars.show_ends)

            File.line_history()

        except EOFError:
            break
        except KeyboardInterrupt:
            exit(0)



def get_args(Vars, File): #parse command line arguments
    for x in sys.argv[1:]:
        if x.startswith("--"): #add arguments such as --show-tabs into array as ['--show-tabs']
            Vars.args.append(x)
        elif x.startswith("-") and not x.endswith("-"): #add arguments such as -bET into array as ['-b', '-E', '-T']
            for z in list(x):
                if z != "-":
                    Vars.args += [f"-{z}"]
        else: #add everything else normally
            Vars.args.append(x)
       
    for x in Vars.args:
        if x.startswith("-") and not x.endswith("-"): #check for arguments (ex. -b)
            if x not in Vars.options: #exit with invalid options
                print("{0}: invalid option -- '{1}'\nTry '{2}' --help' for more information.".format(Vars.program, x.replace("-", ""), Vars.program))
                exit(1)  

            if "--help" in x:
                print(Vars.help_message)
                exit(0)
            if "--version" in x:
                print(Vars.version_message)
                exit(0)
            if "--show-all" in x or "A" in x:
                x = "-A"
                Vars.show_ends = "$\n"
                Vars.show_tabs = "^I"
                Vars.arg_list += [x]
            if "--show-tabs" in x or "T" in x:
                x = "-T"
                Vars.show_tabs = "^I"
                Vars.arg_list += [x]
            if "--show-ends" in x or "E" in x:
                x = "-E"
                Vars.show_ends = "$\n"
                Vars.arg_list += [x]
            if "--number-nonblank" in x or "b" in x:
                x = "-b"
                Vars.arg_list += [x]
            if "--number" in x or "n" in x:
                x = "-n"
                Vars.arg_list += [x]
            if "s" in x:
                Vars.surpress_empty = True
            if "v" in x:
                Vars.show_nonprinting = True
        else: #everything else goes to into print_line()
            Vars.file_list.append(x)



def main():
    Vars = Variables()
    File = Path()
    get_args(Vars, File)

    if sys.argv[1:] == []: #read stdin if no file is provided
        stdin(Vars, File)

    for x in Vars.file_list: #loop through files
        if x == "-": #stdin if file is '-'
            stdin(Vars, File)
        else:
            try:
                File.path = os.path.join(x)
                File.print_line(Vars)
            except FileNotFoundError:
                print(f"{program}: {x}: No such file or directory")
                exit(1)


if __name__ == "__main__":
    main()
