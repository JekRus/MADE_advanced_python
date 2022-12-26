# Homework 07: Type annotations

## Task description

1. Implement a mechanism for metrics collection.
2. Check type annotations with mypy.

Metrics interface:

1. Class `Stats` is responsible for managing the collection of metrics.

   * `Stats` should be used as Singleton or as a class without creating instances;
   * `collect` returns all currently collected non-empty statistics and resets 
   the values of all metrics;
   * `timer`, `avg`, `count` return a metric by its name. 
   If a metric of the given type with the given name does not exist, 
   then a new one is created, registered in `Stats`, and returned.

2. The classes `MetricTimer`, `MetricAvg`, `MetricCount` 
are responsible for a metric with a specific name and type.

   * `get_name` returns the full name of the metric: the name passed to the constructor + the type of the metric separated by a dot;
   * `get_value` returns the current value of the metric or `None` if the current value is empty;
   * `add` adds a new value according to the rules of this metric;
   * `clear` clears the metric to zero state;
   * `MetricTimer` collects the total execution time;
   * `MetricTimer` can be used as a context manager;
   * `MetricCount` collects the number of calls;
   * `MetricAvg` collects the arithmetic mean of the passed values;
   * `MetricCount` and `MetricAvg` should work independently of each other.

## Solution

* Metrics are implemented in metric_collector.py. 
* Tests are in the directory tests.

## How to reproduce

### Install dependencies
```commandline
$ cd path_to_repo/MADE_python/advance_08
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Run tests

```commandline
$ python -m pytest tests
```


## Software versions
```
Name        | Version
------------------------------------------------------------------
Python      | Python 3.8.10 
```
