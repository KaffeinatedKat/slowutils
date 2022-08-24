# pyutils
A few of the coreutils written in python becuase why not

Below is the list of programs I have rewritten thus far, and how they differ from the original (they are all slower)

## Requirements

* python 3+

## Install

```
git clone https://github.com/KaffeinatedKat/pyutils
cd pyutils
sudo ./install.sh
```

* requires root privilege to write to /usr/local/bin

# Programs

## dog - ([cat](https://github.com/coreutils/coreutils/blob/master/src/cat.c))
concatenate files and print on the standard output

* does not support `-v, --show-nonprinting` (or related options)
* does not support `-s, --squeeze-blank` 

## abolish - ([rm](https://github.com/coreutils/coreutils/blob/master/src/rm.c))
file deletion utility

* does not support ``-i prompt before every removal\n
-I promt one before removing more than three files, or recursively\n
--interactive prompt according to WHEN: never, once (-I), or always (-i); without WHEN, prompt always\n
--one-file-system when removing a hierarchy recursively, skip any directory that is on a file system different from that of the corresponding command line argument\n
--no-preserve-root do not treat '/' specially\n
--preserve-root[all] do not remove '/'``

## yeah - ([yes](https://github.com/coreutils/coreutils/blob/master/src/yes.c))
output a string repeatedly until killed

* program behaves identically to `yes`

## isthatme ([whoami](https://github.com/coreutils/coreutils/blob/master/src/whoami.c))
print effective userid

* program should behave identically to `whoami`
