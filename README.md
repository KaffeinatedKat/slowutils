# Pyutils
A few of the coreutils written in python becuase why not

Below is the list of programs I have rewritten thus far, and how they differ from the original

The names are synonyms of the orignial program name

## Install

```
git clone https://github.com/KaffeinatedKat/pyutils
cd pyutils
sudo ./install.sh
```

* requires root privilege to write to /usr/local/bin

# Programs

## kitty - ([cat](https://github.com/coreutils/coreutils/blob/master/src/cat.c))
concatenate files and print on the standard output

* does not support `-v, --show-nonprinting` (or related options)
* does not support `-s, --squeeze-blank` 

## yeah - ([yes](https://github.com/coreutils/coreutils/blob/master/src/yes.c))
output a string repeatedly until killed

* program behaves identically to `yes`

## isthatme ([whoami](https://github.com/coreutils/coreutils/blob/master/src/whoami.c))
print effective userid

* program should behave identically to `whoami`
