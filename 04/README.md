# Homework 04: Matrix multiplication using C

## Description

Matrix multiplication implemented in two different ways:
1. Using pure Python;
2. Using CDLL and ctypes.

## Results 
The functions are compared using pytest-benchmark.

```
--------------------------------------------------------------------------------------------- benchmark: 2 tests ---------------------------------------------------------------------------------------------
Name (time in ms)                      Min                   Max                  Mean              StdDev                Median                 IQR            Outliers     OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_matmul_c_ext_benchmark       186.0399 (1.0)        194.6349 (1.0)        191.3371 (1.0)        2.8943 (1.0)        191.5501 (1.0)        1.7906 (1.0)           2;1  5.2264 (1.0)           6           1
test_matmul_benchmark           6,275.8347 (33.73)    8,633.3103 (44.36)    6,955.5717 (36.35)    951.0672 (328.61)   6,638.4364 (34.66)    689.4437 (385.03)        1;1  0.1438 (0.03)          5           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

## How to reproduce
1. Build CDLL from C source code:
```commandline
$ cd path_to_repo/MADE_python/04/src/c_package
$ make
```
2. Prepare virtual environment:
```commandline
cd path_to_repo/MADE_python/04/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run tests and benchmark:
```commandline
$ cd path_to_repo/MADE_python/04/src
$ python -m pytest tests
```

## Versions
```
Name        | Version
------------------------------------------------------------------
C compiler  | Apple clang version 14.0.0 (clang-1400.0.29.102)
Python      | Python 3.8.10 
```
