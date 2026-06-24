import numpy as np


def find_rank(black_box_A, n, max_rank=50):
    # black_box_A: 映射 x -> Ax 的函数
    # 1. 生成比预估秩略大的随机矩阵
    k = max_rank + 10
    Omega = np.random.randn(n, k)

    # 2. 通过黑盒计算 Y = A @ Omega
    Y = np.zeros((n, k))
    for i in range(k):
        Y[:, i] = black_box_A(Omega[:, i])

    # 3. 对 Y 进行奇异值分解 (SVD)
    s = np.linalg.svd(Y, compute_uv=False)

    # 4. 统计显著大于 0 的奇异值数量
    tol = s[0] * max(n, k) * np.finfo(float).eps
    actual_rank = np.sum(s > tol)
    return actual_rank