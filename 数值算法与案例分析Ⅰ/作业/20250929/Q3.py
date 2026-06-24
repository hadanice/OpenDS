import numpy as np


def generate_special_matrix(n, alpha=None, beta=None):
    if alpha is None:
        alpha = np.random.rand(n) * 10
    if beta is None:
        beta = np.random.rand(n) * 10

    A = np.zeros((n, n))

    # 第一行
    A[0, 0] = alpha[0]
    for j in range(1, n):
        A[0, j] = beta[j]  # β₂ 到 βₙ

    # 第二行到第n行
    for i in range(1, n):
        A[i, 0] = beta[i]  # β₂ 到 βₙ
        A[i, i] = alpha[i]  # α₂ 到 αₙ

    return A

def givens_rotation(a, b):
    if b == 0:
        return 1.0, 0.0
    if a == 0:
        return 0.0, np.sign(b)
    if abs(b) > abs(a):
        tau = -a / b
        s = 1.0 / np.sqrt(1 + tau * tau)
        c = s * tau
    else:
        tau = -b / a
        c = 1.0 / np.sqrt(1 + tau * tau)
        s = c * tau
    return c, s


def qr_givens_special(A):
    A = np.array(A, dtype=float)
    n = A.shape[0]
    R = A.copy()
    Q = np.eye(n)

    # 对第 i 行 (i=1 到 n-1)，消去 R[i, 0]
    for i in range(1, n):
        a = R[0, 0]  # 当前旋转作用于第0行和第i行的第0列
        b = R[i, 0]
        if b == 0:
            continue  # 已为0，无需旋转

        c, s = givens_rotation(a, b)

        # 构造 Givens 矩阵作用于 (0, i) 平面
        # 更新 R: G @ R
        # 只需更新第0行和第i行（因为其他行在第0列已是0，且结构稀疏）
        row0_old = R[0, :].copy()
        rowi_old = R[i, :].copy()
        R[0, :] = c * row0_old + s * rowi_old
        R[i, :] = -s * row0_old + c * rowi_old

        # 更新 Q: Q = Q @ G^T （因为 A = Q R => Q = (G1 G2 ...)^T）
        # 等价于 Q = Q @ G^T，而 G^T 是将 (0,i) 平面旋转 -theta
        # 所以用 [c, -s; s, c] 作用于 Q 的列
        col0_old = Q[:, 0].copy()
        coli_old = Q[:, i].copy()
        Q[:, 0] = c * col0_old + s * coli_old
        Q[:, i] = -s * col0_old + c * coli_old

    return Q, R

# 示例：生成一个 5x5 的矩阵
# 完整示例：生成矩阵 + QR 分解 + 验证
if __name__ == "__main__":
    n = 5
    # 指定 alpha 和 beta 以复现结果
    alpha = np.array([4.0, 3.0, 5.0, 2.0, 6.0])
    beta  = np.array([0.0, 1.0, 2.0, 1.5, 0.5])  # beta[0] 未使用

    A = generate_special_matrix(n, alpha=alpha, beta=beta)
    print("原始矩阵 A:")
    print(A)

    Q, R = qr_givens_special(A)
    print("\nQ 矩阵 (正交):")
    print(Q)
    print("\nR 矩阵 (上三角):")
    print(R)

    # 验证 Q @ R ≈ A
    A_reconstructed = Q @ R
    print("\nQ @ R 重建 A:")
    print(A_reconstructed)
    print("\n最大重建误差:", np.max(np.abs(A - A_reconstructed)))

    # 验证 Q 正交性: Q^T Q ≈ I
    ortho_error = np.max(np.abs(Q.T @ Q - np.eye(n)))
    print("Q 正交性误差 (||Q^T Q - I||_max):", ortho_error)