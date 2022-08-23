#!/usr/bin/python3

# abolish - for deleting files n stuff

import sys
import os
import shutil


class Options:
    program = sys.argv[0]
    files = []
    args = []
    folder = False
    recursive = False
    force = False
    empty_folder = False
    verbose = False
    success = False
    verbose_message = ""
    path = ""



class Exceptions(Options):
    def FileNotFound(self, Object):
        print(f"{self.program}: cannot abolish '{Object.path}': No such file or directory")
    
    def IsAFolder(self, Object):
        print(f"{self.program}: cannot abolish '{Object.path}': Is a directory")
        
    def MissingOperand(self, Object):
        print(f"{self.program}: missing operand\nTry '{self.program} --help' for more information.")

    def FolderNotEmpty(self, Object):
        print(f"{self.program}: cannot abolish '{Object.path}': Directory not empty")


help_message = f"""Usage: {Options.program} [OPTION]... [FILE]...
Remove (unlink) the FILE(s).

  -f, --force           ignore nonexistent files and arguments, never prompt
  -r, -R, --recursive   remove directories and their contents recursively
  -d, --dir             remove empty directories
      --help        display this help and exit
      --version     output version information and exit

By default, rm does not remove directories.  Use the --recursive (-r or -R)
option to remove each listed directory, too, along with all of its contents.

To remove a file whose name starts with a '-', for example '-foo',
use this command:

  {Options.program} ./-foo

Note that if you use abolish to remove a file, it might be possible to recover
some of its contents, given sufficient expertise and/or time.  For greater
assurance that the contents are truly unrecoverable, consider using shred(1)."""


def delete_file(Object, Error):
    Object.verbose_message = "removed"
    
    try:
        os.remove(Object.path)
        Object.success = True
    except FileNotFoundError:
        if not Object.force:
            Error.FileNotFound(Object)
            return 0


def delete_folder(Object, Error):
    Object.verbose_message = "removed directory"
    
    if Object.recursive: 
        shutil.rmtree(Object.path)
        Object.success = True
        return

    if Object.empty_folder: #remove empty directories
        try:
            os.rmdir(Object.path)
            Object.success = True
        except OSError:
            Error.FolderNotEmpty(Object) # -f does not ignore "Directory not empty" error
        return

    if not Object.recursive:
        Error.IsAFolder(Object)

def get_args(Object, Error):
    for x in sys.argv[1:]: 
        if x.startswith("--"): # add long options as one entry
            Object.args.append(x)
        elif x.startswith("-"): # add combined short options indivdually
            for z in list(x):
                if z != "-": # prevent ["--"] from being added
                    Object.args += [f"-{z}"]
        else: # add everything else normally
            Object.args.append(x)

    for x in Object.args:
        if x.startswith("-"):
            if "--help" in x:
                print(help_message)
                exit(0)
            if "-r" in x.lower() or "--recursive" in x: #recursive '-r'
                print("delete that bad boi")
                Object.recursive = True
            if "-f" in x.lower() or "--force" in x:
                Object.force = True
            if "-d" in x.lower() or "--dir" in x:
                Object.empty_folder = True
            if "-v" in x.lower() or "--verbose" in x:
                Object.verbose = True
        else:
            Object.files.append(x)



def main():
    Opts = Options()
    Error = Exceptions()
    get_args(Opts, Error)
    
    if len(sys.argv[1:]) == 0: #exit with no input
        Error.MissingOperand(Opts)
        exit(1)

    for x in Opts.files: #parse files/folders to delete
        Opts.success = False
        Opts.path = x
        Opts.folder = os.path.isdir(os.path.join(Opts.path)) # directory or file?
        
        if Opts.folder:
            delete_folder(Opts, Error)
        elif not Opts.folder:
            delete_file(Opts, Error)
        
        if Opts.verbose and Opts.success: # print verbose message if file deletion successful
           print(f"{Opts.verbose_message} '{Opts.path}'")


if __name__ == '__main__':
    main()
