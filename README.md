# PDF sanitizer ![semester](https://img.shields.io/badge/Stability-alpha%20version-orange.svg)

## A batch pdf metadata removal script  

A simple python script that takes as input a directory containing pdf files and produces a subdirectory of the given directory containing the same pdf files without their original metadata.

### Requires:
* python 3.2+
* PyPDF2 library (*pip install PyPDF2*)

### Examples

The script uses as default, the current working directory, unless otherwise specified.

#### without specifying a directory

it will search for pdf files inside the folder from which it was called

```bash
$ python sanitizer.py
```

#### specifying a path to a directory
```bash
$ python sanitizer.py ~/Desktop/folder_containing_pdfs
```
