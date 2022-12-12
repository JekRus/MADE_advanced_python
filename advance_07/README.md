# Homework 07: Testing

## Task description

1. Implement a predict_message_mood function that takes a 
string, an instance of the SomeModel, 
and goodness thresholds as input. The function returns:

   * "неуд" if model prediction is less than bad_threshold
   * "отл" if model prediction is greater than good_threshold
   * "норм" in other cases

2. Cover function predict_message_mood with tests.
3. Tests for Python int.
4. Tests for Python str.partition.

## Install dependencies
```commandline
$ cd path_to_repo/MADE_python/advance_07
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

# Tests

```commandline
$ python -m pytest tests
```


## Software versions
```
Name        | Version
------------------------------------------------------------------
Python      | Python 3.8.10 
```
