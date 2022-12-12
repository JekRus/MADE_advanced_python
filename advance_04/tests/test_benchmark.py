import numpy as np

from matmul import matmul, matmul_c_ext


def test_matmul_benchmark(benchmark, matmul_benchmark_test_case):
    matrix_result = benchmark(
        matmul, matmul_benchmark_test_case.matrix_list
    )
    assert np.allclose(np.array(matrix_result), matmul_benchmark_test_case.answer)


def test_matmul_c_ext_benchmark(benchmark, matmul_benchmark_test_case):
    matrix_result = benchmark(
        matmul_c_ext, matmul_benchmark_test_case.matrix_list
    )
    assert np.allclose(np.array(matrix_result), matmul_benchmark_test_case.answer)
