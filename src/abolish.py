#!/usr/bin/python3

# abolish - for deleting files n stuff

import sys
import os
import shutil

help_message = """-r, -R, --recursive    remove directories and their contents recursively
-b, -B, --tester    idek, test and find out"""


class Options:
    program = sys.argv[0]
    files = []
    args = []
    folder = False
    recursive = False
    force = False
    empty_folder = False
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


def delete_file(Object, Error):
    try:
        os.remove(Object.path)
    except FileNotFoundError:
        if not Object.force:
            Error.FileNotFound(Object)


def delete_folder(Object, Error):
    if Object.empty_folder: #remove empty directories
        try:
            os.rmdir(Object.path)
        except OSError:
            Error.FolderNotEmpty(Object) #force does not ignore "Directory not empty" error
        return 0

    if Object.recursive: 
        shutil.rmtree(Object.path)
    elif not Object.force: #ignore errors
        Error.IsAFolder(Object)


def get_args(Object, Error):
    for x in sys.argv[1:]: 
        if x.startswith("--"): #add long options as one entry
            Object.args.append(x)
        elif x.startswith("-"): #add combined short options indivdually
            for z in list(x):
                if z != "-": #prevent ["--"] from being added
                    Object.args += [f"-{z}"]
        else: #add everything else normally
            Object.args.append(x)

    for x in Object.args:
        if x.startswith("-"):
            if "--help" in x:
                print(help_message)
                exit(0)
            if "-r" in x.lower() or "--recursive" in x: #recursive '-r'
                print("delete that bad boi")
                Object.recursive = True
            if "-b" in x.lower() or "--tester" in x:
                print("some thing idek lol")
            if "-f" in x.lower() or "--force" in x:
                Object.force = True
            if "-d" in x.lower() or "--dir" in x:
                Object.empty_folder = True
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
        Opts.path = x
        Opts.folder = os.path.isdir(os.path.join(Opts.path))
        if Opts.folder:
            delete_folder(Opts, Error)
        else:
            delete_file(Opts, Error)


if __name__ == '__main__':
    main()
