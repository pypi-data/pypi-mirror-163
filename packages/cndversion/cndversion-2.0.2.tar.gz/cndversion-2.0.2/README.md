# cndversion

The definitive tools to manage VERSION and CHANGES files (based on semver)

# Installation

```
pip install cndversion
```

# Usage

Help accessible from here
```
cndversion --help
```

## Setup a new project in a folder
```python
cndversion -f mylib
```

if will create
```
project
│   VERSION
│   CHANGES  
└───mylib
│   │   __init__.py
│   │   __version__.py
│   │   VERSION 
```

## Bump to major version
```python
cndversion -M
```

it will increase the major version in mylib/VERSION file and add commit message to CHANGES

## Bump to minor version
```python
cndversion -m
```

it will increase the minor version in mylib/VERSION file and add commit message to CHANGES

## Bump to patch version
```python
cndversion -p
```

it will increase the patch version in mylib/VERSION file and add commit message to CHANGES

# What in each file ?
### VERSION
This file content is the path for the "real" VERSION file (use for compatibilities with somes old tools)
```bash
>>>> cat VERSION
mylib/VERSION
```

### CHANGES
This file is just empty
```bash
>>>> cat CHANGE

```

### mylib/__init__.py
Simply include in the beginning of the file the __version__ file
```bash
>>>> cat mylib/__init__.py
from .__version__ import (__version__)  # noqa: F401
```

### mylib/__version__.py
Allow you to include VERSION into the package (usefull for lib)
```bash
>>>> cat mylib/__version__.py
import pkg_resources


path = pkg_resources.resource_filename('mylib', 'VERSION')
__version__ = open(path).read()

```

### mylib/VERSION
This file is the real version number
```bash
>>>> cat mylib/VERSION
0.1.1
```