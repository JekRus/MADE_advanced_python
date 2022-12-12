#include <stdlib.h>
#include <string.h>
#include "matmul.h"


double** matmul(
    double** matrix_op1,
    const size_t nrows1,
    const size_t ncols1,
    double** matrix_op2,
    const size_t nrows2,
    const size_t ncols2
) {
    if (
        (matrix_op1 == NULL) || (matrix_op2 == NULL) 
        || (nrows1 == 0) || (ncols1 == 0) || (nrows2 == 0) || (ncols2 == 0)
        || (ncols1 != nrows2)
    ) {
        return NULL;
    }

    // transpose 2nd operand for speedup

    double** matrix_op2_T = calloc(ncols2, sizeof(double*));
    for (size_t j = 0; j < ncols2; ++j) {
        matrix_op2_T[j] = calloc(nrows2, sizeof(double));

        for (size_t i = 0; i < nrows2; ++i) {
            matrix_op2_T[j][i] = matrix_op2[i][j];
        }
    }

    // init result

    double** matrix_result = calloc(nrows1, sizeof(double*));
    for (size_t i = 0; i < nrows1; ++i) {
        matrix_result[i] = calloc(ncols2, sizeof(double));
    }

    // do matmul

    for (size_t i = 0; i < nrows1; ++i) {
        for (size_t j = 0; j < ncols2; ++j) {
            for (size_t k = 0; k < ncols1; ++k) {
                matrix_result[i][j] += matrix_op1[i][k] * matrix_op2_T[j][k];
            }
        }
    }

    // clean up

    for (size_t j = 0; j < ncols2; ++j) {
        free(matrix_op2_T[j]);
        matrix_op2_T[j] = NULL;
    }
    free(matrix_op2_T);
    matrix_op2_T = NULL;
    
    return matrix_result;
}


double** matmul_chain(
    double*** const matrix_list,
    const size_t n_rows[],
    const size_t n_cols[],
    const size_t length
) {
    if ((matrix_list == NULL) || (length == 0)) {
        return NULL;
    }
    if (length == 1) {
        double** matrix_result = calloc(n_rows[0], sizeof(double*));
        for (size_t i = 0; i < n_rows[0]; ++i) {
            matrix_result[i] = calloc(n_cols[0], sizeof(double));
            for (size_t j = 0; j < n_cols[0]; ++j) {
                matrix_result[i][j] = matrix_list[0][i][j];
            }
        }
        return matrix_result;
    }
    
    double** matrix_result_prev = matrix_list[0];
    double** matrix_result = matmul(matrix_list[0], n_rows[0], n_cols[0], matrix_list[1], n_rows[1], n_cols[1]);
    
    for (size_t i = 2; i < length; ++i) {
        matrix_result_prev = matrix_result;
        matrix_result = matmul(matrix_result_prev, n_rows[0], n_cols[i - 1], matrix_list[i], n_rows[i], n_cols[i]);
        if (matrix_result_prev == NULL) {
            return NULL;
        }

        for (size_t k = 0; k < n_rows[0]; ++k) {
            free(matrix_result_prev[k]);
            matrix_result_prev[k] = NULL;
        }
        free(matrix_result_prev);
    }

    return matrix_result;
}
