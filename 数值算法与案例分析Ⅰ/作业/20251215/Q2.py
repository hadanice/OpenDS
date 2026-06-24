import numpy as np
from scipy.sparse.linalg import eigsh, LinearOperator
from scipy.linalg import cholesky


def solve_ab_eig(A, B, k=5):
    # A, B 为 scipy.sparse 矩阵
    # 1. Cholesky 分解 B = L @ L.H
    L = np.linalg.cholesky(B)
    # 2. 定义算子 M = L.H @ A @ L,
    # AB 的特征值等同于 M 的特征值
    def matvec(v):
        return L.T.conj() @ (A @ (L @ v))

    M_op = LinearOperator(A.shape, matvec=matvec)

    # 3. Lanczos 计算最大 k 个特征值
    vals, _ = eigsh(M_op, k=k, which='LM')
    return vals