#ifndef MATMUL_H
#define MATMUL_H

double** matmul(
    double** matrix_op1,
    const size_t nrows1,
    const size_t ncols1,
    double** matrix_op2,
    const size_t nrows2,
    const size_t ncols2
);

double** matmul_chain(
    double*** const matrix_list,
    const size_t n_rows[],
    const size_t n_cols[],
    const size_t length
);

#endif /* MATMUL_H */
