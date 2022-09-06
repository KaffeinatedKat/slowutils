#!/usr/bin/python3

# abolish - for deleting files n stuff

import sys
import os
import shutil


class Variables:
    program = os.path.realpath(__file__)
    files = []
    args = []
    recursive = False
    force = False
    empty_folder = False
    verbose = False
    success = False
    annoy = False
    delete_empty = False
    verbose_message = ""

    help_message = f"""Usage: {program} [OPTION]... [FILE]...
Remove (unlink) the FILE(s).

  -i                    prompt before every removal
  -f, --force           ignore nonexistent files and arguments, never prompt
  -r, -R, --recursive   remove directories and their contents recursively
  -d, --dir             remove empty directories
      --help        display this help and exit
      --version     output version information and exit

By default, rm does not remove directories.  Use the --recursive (-r or -R)
option to remove each listed directory, too, along with all of its contents.

To remove a file whose name starts with a '-', for example '-foo',
use this command:

  {program} ./-foo

Note that if you use abolish to remove a file, it might be possible to recover
some of its contents, given sufficient expertise and/or time.  For greater
assurance that the contents are truly unrecoverable, consider using shred(1)."""





class Exceptions(Variables):
    def FileNotFound(self, File):
        print(f"{self.program}: cannot abolish '{File.path}': No such file or directory")
    
    def IsAFolder(self, File):
        print(f"{self.program}: cannot abolish '{File.path}': Is a directory")
        
    def MissingOperand(self):
        print(f"{self.program}: missing operand\nTry '{self.program} --help' for more information.")

    def FolderNotEmpty(self, File):
        print(f"{self.program}: cannot abolish '{File.path}': Directory not empty")



class Path:
    def __init__(self):
        self.path = ""
        self.is_file = False
        self.is_folder = False
        self.is_symlink = False
        self.folders = []

    def get_type(self):
        self.is_file = not os.path.isdir(self.path)
        self.is_folder = os.path.isdir(self.path)
        self.is_symlink = os.path.islink(self.path)


    def ask_delete(self, Vars, Error):
        self.get_type()

        if self.is_symlink:
            if stdin(f"{Vars.program}: remove symbolic link '{self.path}'? "):
                self.delete(Vars, Error)
        
        elif self.is_folder:
            if not Vars.recursive:
                Error.IsAFolder(self)
            elif len(os.listdir(self.path)) == 0: # if folder is empty
                if Vars.delete_empty or Vars.recursive:
                    if stdin(f"{Vars.program}: remove directory '{self.path}'? ").lower().startswith("y"):
                        self.delete(Vars, Error)
            elif Vars.recursive:
                if not len(os.listdir(self.path)) == 0 and self.path not in self.folders: # decend into directory if folder not empty
                    self.folders += [self.path] # dont decend back into a directory if you dont remove everything from that directory
                    if stdin(f"{Vars.program}: decend into directory '{self.path}'? ").lower().startswith("y"):
                        self.delete_folder(Vars, Error)

        elif self.is_file:
            if stdin(f"{Vars.program}: remove regular file '{self.path}'? ").lower().startswith("y"):
                self.delete(Vars, Error)



    def delete_folder(self, Vars, Error):
        directory = self.path
        for x in os.listdir(self.path):
            self.path = os.path.join(directory + "/" + x)
            self.ask_delete(Vars, Error)
        
        self.path = directory
        self.ask_delete(Vars, Error)



    def delete(self, Vars, Error):
        if self.is_symlink:
            Vars.verbose_message = "removed"
            os.unlink(self.path)

        elif self.is_file: # files
            Vars.verbose_message = "removed"
            try:
                os.remove(self.path)
                Vars.success = True
            except FileNotFoundError:
                if not Vars.force:
                    Error.FileNotFound(self)

        elif self.is_folder: # directories
            Vars.verbose_message = "removed directory"
    
            if Vars.recursive: # delete full directories
                shutil.rmtree(self.path)
                Vars.success = True

            elif Vars.delete_empty: #remove empty directories
                try:
                    os.rmdir(self.path)
                    Vars.success = True
                except OSError:
                    Error.FolderNotEmpty(self) # -f does not ignore "Directory not empty" error

            elif not Vars.recursive: # -r nor -d were set
                Error.IsAFolder(self)

        if Vars.verbose and Vars.success: # print verbose message if file deletion successful
           print(f"{Vars.verbose_message} '{self.path}'")



def stdin(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        exit("")



def get_args(Vars, File, Error):
    for x in sys.argv[1:]: 
        if x.startswith("--"): # add long options as one entry
            Vars.args.append(x)
        elif x.startswith("-"): # add combined short options indivdually
            for z in list(x):
                if z != "-": # prevent ["--"] from being added
                    Vars.args += [f"-{z}"]
        else: # add everything else normally
            Vars.args.append(x)

    for x in Vars.args:
        if x.startswith("-"):
            if "--help" in x:
                print(Vars.help_message)
                exit(0)
            if "-r" in x.lower() or "--recursive" in x: #recursive '-r'
                Vars.recursive = True
            if "-f" in x.lower() or "--force" in x:
                Vars.force = True
            if "-d" in x.lower() or "--dir" in x:
                Vars.delete_empty = True
            if "-v" in x.lower() or "--verbose" in x:
                Vars.verbose = True
            if "-i" in x.lower():
                Vars.annoy = True
        else:
            Vars.files.append(x)



def main():
    Vars = Variables()
    Error = Exceptions()
    File = Path()
    get_args(Vars, File, Error)
    
    if len(sys.argv[1:]) == 0: #exit with no input
        Error.MissingOperand()
        exit(1)

    for x in Vars.files: #parse files/folders to delete
        Vars.success = False
        File.path = os.path.join(x)
        File.get_type()
        
        
        if Vars.annoy:
            File.ask_delete(Vars, Error)
        elif not Vars.annoy:
            File.delete(Vars, Error)
        
        

if __name__ == '__main__':
    main()
