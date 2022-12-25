# Homework 02: Thread-based url scraper

## Description

Client-server app for urls processing using threads.

## Install
```commandline
$ cd path_to_repo/MADE_python/advance_02
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

Server:

```commandline
$ python server.py -w 10 -k 5
```

Client:

```commandline
$ python client.py 5 urls.txt
```

## Tests

```commandline
$ python -m pytest tests
```

Server CLI arguments:  
**-w**  
      Number of thread-workers.  
**-k**  
      Number of most common words to send to a client.  


Client CLI arguments:  
**n_threads**  
      Number thread-workers.  
**filename**  
      Path to the input file containing urls.  


## Software versions
```
Name        | Version
------------------------------------------------------------------
Python      | Python 3.8.10 
```
