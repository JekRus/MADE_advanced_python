from typing import List
from dataclasses import dataclass
from functools import reduce
import pytest
import numpy as np

from matmul import Matrix


def generate_random_matrix_list(
        n_matrix: int,
        min_size: int,
        max_size: int,
        seed: int
) -> List[Matrix]:
    np.random.seed(seed)
    matrices = []
    if min_size != max_size:
        sizes_chain = np.random.randint(min_size, max_size, (n_matrix + 1,))
    else:
        sizes_chain = np.full((n_matrix + 1,), max_size)
    for i in range(1, n_matrix + 1):
        matrices.append(np.random.rand(sizes_chain[i - 1], sizes_chain[i]))
    matrices = [matrix.tolist() for matrix in matrices]
    return matrices


@dataclass
class MatmulTestCaseData:
    matrix_list: List[Matrix]
    answer: Matrix


@pytest.fixture(
    scope="module",
    params=[
        {'n_matrix': 1, 'seed': 1},
        {'n_matrix': 1, 'seed': 2},
        {'n_matrix': 1, 'seed': 3},
        {'n_matrix': 1, 'seed': 4},
        {'n_matrix': 1, 'seed': 5},

        {'n_matrix': 2, 'seed': 1},
        {'n_matrix': 2, 'seed': 2},
        {'n_matrix': 2, 'seed': 3},
        {'n_matrix': 2, 'seed': 4},
        {'n_matrix': 2, 'seed': 5},

        {'n_matrix': 3, 'seed': 1},
        {'n_matrix': 3, 'seed': 2},
        {'n_matrix': 3, 'seed': 3},
        {'n_matrix': 3, 'seed': 4},
        {'n_matrix': 3, 'seed': 5},

        {'n_matrix': 5, 'seed': 1},
        {'n_matrix': 5, 'seed': 2},
        {'n_matrix': 5, 'seed': 3},
        {'n_matrix': 5, 'seed': 4},
        {'n_matrix': 5, 'seed': 5},

        {'n_matrix': 10, 'seed': 1},
        {'n_matrix': 10, 'seed': 2},
        {'n_matrix': 10, 'seed': 3},
        {'n_matrix': 10, 'seed': 4},
        {'n_matrix': 10, 'seed': 5},
    ]
)
def matmul_random_test_case(request):
    matrix_list = generate_random_matrix_list(
        min_size=1, max_size=10, **request.param
    )
    matrix_ans = reduce(np.matmul, map(np.array, matrix_list))
    yield MatmulTestCaseData(matrix_list, matrix_ans)


@pytest.fixture(scope="module")
def matmul_benchmark_test_case():
    matrix_list = generate_random_matrix_list(
        n_matrix=10, min_size=10, max_size=500, seed=42
    )
    matrix_ans = reduce(np.matmul, map(np.array, matrix_list))
    yield MatmulTestCaseData(matrix_list, matrix_ans)
