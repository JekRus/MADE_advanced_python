import numpy as np
import pytest

from matmul import matmul_c_ext


def test_matmul_simple():
    matrix_a = [
        [1, 2],
        [3, 4],
    ]
    matrix_b = [
        [5, 6, 7],
        [8, 9, 10],
    ]
    matrix_ans = [
        [21, 24, 27],
        [47, 54, 61]
    ]

    matrix_result = matmul_c_ext([matrix_a, matrix_b])
    assert matrix_ans == matrix_result


def test_wrong_size():
    matrix_a = [
        [1, 2],
        [3, 4],
    ]
    matrix_b = [
        [5, 6]
    ]
    matrix_c = [
        [7, 8, 9],
        [10, 11, 12]
    ]

    with pytest.raises(ValueError):
        matmul_c_ext([matrix_a, matrix_b])
    with pytest.raises(ValueError):
        matmul_c_ext([matrix_a, matrix_b, matrix_c])
    with pytest.raises(ValueError):
        matmul_c_ext([matrix_a, matrix_c, matrix_b])


def test_chain():
    matrix_a = [
        [1, 2],
        [3, 4],
    ]
    matrix_b = [
        [5, 6, 7],
        [8, 9, 10],
    ]
    matrix_c = [
        [11],
        [12],
        [13],
    ]
    matrix_ans = [
        [870],
        [1958],
    ]

    matrix_result = matmul_c_ext([matrix_a, matrix_b, matrix_c])
    assert matrix_ans == matrix_result


def test_small_matrix():
    matrices = [
        [[1]],
        [[2]],
        [[3]],
        [[4]],
        [[5]],
        [[6]],
    ]
    matrix_ans = [[720]]
    matrix_result = matmul_c_ext(matrices)
    assert matrix_result == matrix_ans


def test_empty_list():
    with pytest.raises(ValueError):
        matmul_c_ext([])


def test_empty_matrix():
    empty_matrix = [[]]
    result = matmul_c_ext([empty_matrix])
    assert result == empty_matrix


def test_single_matrix():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    matrices = [matrix]
    matrix_result = matmul_c_ext(matrices)
    assert matrix_result == matrix


def test_random_matrices(matmul_random_test_case):
    matrix_result = matmul_c_ext(matmul_random_test_case.matrix_list)
    assert np.allclose(np.array(matrix_result), matmul_random_test_case.answer)
