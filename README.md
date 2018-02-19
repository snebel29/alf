# Access Log Filter (ALF)
A simple access_log filter CLI tool written in python

![Alf](https://vignette.wikia.nocookie.net/mugen/images/a/ab/Alf.gif/revision/latest?cb=20121216142416)

## Prerequisites
- Linux
- Most of python3 versions should work, however the tool was developed with `3.5.3` which is the recommended version until full compatibility is verified, refer to [Install python 3.5.3](https://github.com/snebel29/alf#install-python-353)
- pip

## Installation
The tool is shipped as a package so can be integrated into any python package repository either private, or public such as [Pypi](https://pypi.python.org/pypi), but can also be installed locally
```
$ git clone https://github.com/snebel29/alf.git
$ cd alf/
$ pip install .
```

or from a git repository
```
$ pip install git+https://github.com/namespace/access_log_filter.git
```

## Usage
The CLI usage is defined using [docopt](http://docopt.org/) docstring which can be found [here](./access_log_filter/cli.py)

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

The installer installs the package and the command line wrapper so you can consume it from the command line
```
$ access_log_filter --ip 127.0.0.1
```

A shorthand command `alf` is installed as well and can be used instead
```
$ alf access_log --ip 10.0.0.0/8
```

but can also consumed as a library, note that filter() returns a generator
```
$ python
>>> from access_log_filter import AccessLog, IpFilter
>>> access_log = AccessLog('tests/fixtures/public_access.log.txt')
>>> ip_filter = IpFilter('31.184.238.0/24')
>>> for record in access_log.filter(ip_filter):
>>>     print(record)
...
...
```

> :warning: The filter function in its current version is picky and skips bad lines with either a bad access_log schema or a bad ip address, future versions may handle it optionally.

## Development

### Prerequisites
- Most of python3 versions should work, however the tool was developed with `3.5.3` which is the recommended version until full compatibility is verified, refer to [Install python 3.5.3](https://github.com/snebel29/alf#install-python-353)
- pip

### Installation
Install the development dependencies
```
$ pip install -e .[dev]
```
> NOTE: You MUST run `pip install . --upgrade` to force package re-installation while developing if any file has changed and you want to run it using the CLI wrappers

and run the tests
```
$ tests/test_end_to_end.sh
```
Unit and integration tests are supposed to be run using [nose](http://nose.readthedocs.io/en/latest/) depending on your virtualenvironment setup you might run it differently, but you should always run it with python3

Typically you would only run
```
$ nosetests -v
```

But I've noticed that some times nose keeps running the test suite with python2 and failing with some import and undefined errors, reload your environment
```
$ source bin/activate
```
or force running with python3
```
$ nosetests-3.4 -v
$ python nosetests -v
$ python3 nosetests -v
```

## Install-python-3.5.3

### Prerequisites
- Linux with bash
- [pyenv](https://github.com/pyenv/pyenv)
- pyvenv comes with python3

## Install
```
$ pyenv install 3.5.3
```

Install and configure a virtual environment
```
$ pyvenv .
$ source bin/activate
```

## Road Map
Just some ideas for the moment...

- Compatibility with major python 2 and 3 versions
- Docker image
- More flexible and configurable access_log schema
- Alert on and/or count bad lines (not honoring the schema)
- Add more filters such as by HTTP method, HTTP version, referrer, etc..
- Multifiltering
- Allow negative filters (plus the existent positive ones)
- Custom and more extensible filters using callables
- Add matching filter callbacks (To run functions when a filter match)
- ...
