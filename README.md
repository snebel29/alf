# Access Log Filter
A simple access_log filter CLI tool written in python

## Prerequisites
- python3
- pip

## Installation
The tool is shipped as a package so can be integrated into any python package repository either private, or public such as [Pypi](https://pypi.python.org/pypi), but can also be installed locally
```
$ cd access_log_filter/
$ pip install .
```

or from a git repository
```
$ pip install git+https://github.com/namespace/access_log_filter.git
```

## Usage
The CLI usage is defined using [docopt](http://docopt.org/) docstring and can be found [here](./access_log_filter/cli.py)

```
Access Log Filter (alf)

Usage:
  alf <access_log> [--ip=<ip_address>]
  alf -h | --help
  alf -v | --version

Options:
  -i IP, --ip=IP     Filter by ip, CDIR notation is allowed
  -h, --help         Show the help
  -v, --version      Show version

Examples:
  alf access_log --ip 127.0.0.1
  alf access_log --ip 10.0.0.0/8
```

The installer install the package and the command line wrapper so you can consume it either from the command line
```
$ access_log_filter --ip 127.0.0.1
```

A shorthand command `alf` is installed as well and can be used instead
```
$ alf access_log --ip 10.0.0.0/8
```

or consumed as Library
```
$ python
```

## Development
Install and configure a python3 virtual environment
```
$ pyvenv .
$ source bin/activate
```

then install the development dependencies
```
$ pip install -e .[dev]
```
> NOTE: You MUST run `pip install . --upgrade` to force package re-installation while developing if any file has changed and you want to run it using the CLI wrappers

and run tests
```
$ nosetests -v
```
