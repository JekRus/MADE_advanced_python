from functools import reduce
from ctypes import cdll, c_size_t, c_double, POINTER

from typing import List


Matrix = List[List[float]]


def is_valid_matrix(matrix: Matrix) -> bool:
    """
    Checks if the argument is a valid Matrix.

    Parameters
    ----------
    matrix : Matrix

    Returns
    -------
    bool
    """

    if not isinstance(matrix, list):
        return False
    if not all(isinstance(row, list) for row in matrix):
        return False
    n_rows = len(matrix)
    if n_rows == 0:
        return False
    n_cols = len(matrix[0])
    if not all(len(row) == n_cols for row in matrix):
        return False
    if not all(
            isinstance(matrix[i][j], (int, float))
            for j in range(n_cols) for i in range(n_rows)
    ):
        return False
    return True


def matmul_two_op(matrix_op1: Matrix, matrix_op2: Matrix) -> Matrix:
    """
    Performs matrix multiplication of the operands.

    Parameters
    ----------
    matrix_op1 : Matrix
    matrix_op2 : Matrix

    Returns
    -------
    Matrix
        The result of matrix multiplication.
    """

    if not (is_valid_matrix(matrix_op1) and (is_valid_matrix(matrix_op2))):
        raise TypeError(
            f"Wrong type of operands in matmul."
            f"Expected [Matrix, Matrix], got "
            f"[{type(matrix_op1)}, {type(matrix_op2)}]."
        )

    n_rows_op1 = len(matrix_op1)
    n_cols_op1 = len(matrix_op1[0])
    n_rows_op2 = len(matrix_op2)
    n_cols_op2 = len(matrix_op2[0])

    if n_cols_op1 != n_rows_op2:
        raise ValueError(
            f"Can not multiply operands with sizes "
            f"[{n_rows_op1}, {n_cols_op1}] and [{n_rows_op2}, {n_cols_op2}]."
        )

    matrix_result = [
        [0 for _ in range(n_cols_op2)] for _ in range(n_rows_op1)
    ]

    for i in range(n_rows_op1):
        for j in range(n_cols_op2):
            matrix_result[i][j] = sum(
                matrix_op1[i][k] * matrix_op2[k][j] for k in range(n_cols_op1)
            )
    return matrix_result


def matmul(matrix_list: List[Matrix]) -> Matrix:
    """
    Performs chained matrix multiplication of matrices
    in the parameter list.

    Parameters
    ----------
    matrix_list : List[Matrix]

    Returns
    -------
    Matrix
        The result of chained matrix multiplication.
    """

    if not isinstance(matrix_list, list):
        raise TypeError(
            f"Wrong type of matrix_list."
            f" Must be list, got {type(matrix_list)}"
        )
    if len(matrix_list) == 0:
        raise ValueError("Matrix list is empty.")
    return reduce(matmul_two_op, matrix_list)


def transform_matrix_to_ctypes(matrix: Matrix):
    """
    Transforms Python Matrix object into ctypes compatible object.

    Parameters
    ----------
    matrix : Matrix

    Returns
    -------
    Object
        ctypes compatible version of the input object.
    """

    rows = []
    for i, row in enumerate(matrix):
        rows.append((c_double * len(matrix[i]))(*row))
    return (POINTER(c_double) * len(rows))(*rows)


def transform_size_list_to_ctypes(size_list: List[int]):
    """
    Transform Python List[int] into ctypes compatible object.

    Parameters
    ----------
    size_list : List[int]

    Returns
    -------
    Object
        ctypes compatible version of the input object.
    """

    return (c_size_t * len(size_list))(*size_list)


def transform_ctypes_to_matrix(matrix_c, n_rows: int, n_cols: int):
    """
    Transforms ctypes double** object into Python Matrix object.

    Parameters
    ----------
    matrix_c : ctypes representation of double**
    n_rows : int
    n_cols : int

    Returns
    -------
    Matrix
        Python Matrix object
    """

    if matrix_c:
        return [matrix_c[i][:n_cols] for i in range(n_rows)]
    return None


def matmul_c_ext(matrix_list: List[Matrix]) -> Matrix:
    """
    Performs chained matrix multiplication of matrices
    in the parameter list using C functions.

    Parameters
    ----------
    matrix_list : List[Matrix]

    Returns
    -------
    Matrix
        The result of chained matrix multiplication.
    """

    if not isinstance(matrix_list, list):
        raise TypeError(
            f"Wrong type of matrix_list."
            f" Must be list, got {type(matrix_list)}"
        )
    if len(matrix_list) == 0:
        raise ValueError("Matrix list is empty.")
    if not all(is_valid_matrix(matrix) for matrix in matrix_list):
        raise ValueError(
            "Wrong matrix format."
        )

    #  prepare C function
    matmul_lib = cdll.LoadLibrary("c_package/lib/matmul.so")
    matmul_chain = matmul_lib.matmul_chain
    matmul_chain.argtypes = [
        POINTER(POINTER(POINTER(c_double))),
        POINTER(c_size_t),
        POINTER(c_size_t),
        c_size_t
    ]
    matmul_chain.restype = POINTER(POINTER(c_double))

    #  prepare arguments
    n_rows = [len(matrix) for matrix in matrix_list]
    n_cols = [len(matrix[0]) for matrix in matrix_list]
    n_rows_c = transform_size_list_to_ctypes(n_rows)
    n_cols_c = transform_size_list_to_ctypes(n_cols)
    matrices_c = [transform_matrix_to_ctypes(matrix) for matrix in matrix_list]
    matrix_list_c = (POINTER(POINTER(c_double)) * len(matrices_c))(*matrices_c)

    #  call and transform the result
    result_c = matmul_chain(
        matrix_list_c, n_rows_c, n_cols_c, c_size_t(len(matrix_list))
    )
    result = transform_ctypes_to_matrix(result_c, n_rows[0], n_cols[-1])
    if result is None:
        raise ValueError("Result can not be calculated. Check the parameters.")
    return result
