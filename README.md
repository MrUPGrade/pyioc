# pyioc
[![Build Status](https://travis-ci.org/MrUPGrade/pyioc.svg?branch=master)](https://travis-ci.org/MrUPGrade/pyioc)


PyIoC - Inversion of Control tools for python

## Development setup

### Native development environment

To install dependencies run:

```bash
pip install --upgrade -e .[dev,doc,test]
```

### Docker unit testing

To build image needed for running unit tests run (from sources root folder):

```bash
./docker/build.sh
```

**Important** 

The build command have to be re-run every time requirements.txt file will change. This is due
to time optimisation - for every python version all requirements are installed during image building.
Thanks to that unit tests run almost instantly.


After that you can run unit tests inside container for python versions 2.6, 2.7 3.3 3.4 3.5
by runnint command: 

```bash
./docker/run_tests.sh
```

