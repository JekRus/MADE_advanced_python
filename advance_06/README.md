# Homework 06: Asynchronous url fetcher

## Description

Script for downloading a list of urls 
using asynchronous programming.

## Install
```commandline
$ cd path_to_repo/MADE_python/advance_06
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

```commandline
$ mkdir results
$ python fetcher.py -c 10 -i urls.txt -o results
```

## Tests

```commandline
$ python -m pytest tests
```

Arguments:  
**-c**  
      Number of simultaneous corutines.  
**-i**  
      Path to the input file containing urls.  
**-o**  
      Path to the directory for storing loaded files.  


## Software versions
```
Name        | Version
------------------------------------------------------------------
Python      | Python 3.8.10 
```
