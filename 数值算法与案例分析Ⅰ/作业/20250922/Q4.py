import numpy as np
from scipy.linalg import eig

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

# 构造矩阵 A
F16 = fibonacci(16)
F17 = fibonacci(17)
F18 = fibonacci(18)
A = np.array([[F16, F17],
              [F17, F18]], dtype=float)

print("Matrix A:")
print(A)

# 计算特征值和特征向量
eigvals, eigvecs = eig(A)

# 按特征值的绝对值排序
idx_sorted = np.argsort(np.abs(eigvals))
eigvals_sorted = np.real(eigvals[idx_sorted])
eigvecs_sorted = np.real(eigvecs[:, idx_sorted])

lambda_small = eigvals_sorted[0]   # 小特征值
lambda_large = eigvals_sorted[1]   # 大特征值

v_small = eigvecs_sorted[:, 0]     # 对应小 λ 的特征向量
v_large = eigvecs_sorted[:, 1]     # 对应大 λ 的特征向量

# 归一化（∞-范数）
v_small = v_small / np.linalg.norm(v_small, np.inf)
v_large = v_large / np.linalg.norm(v_large, np.inf)

print(f"\nSorted Eigenvalues (by |λ|):")
print(f"λ_small ≈ {lambda_small:.8f} (|λ| = {abs(lambda_small):.2e})")
print(f"λ_large ≈ {lambda_large:.8f} (|λ| = {abs(lambda_large):.2e})")
print(f"v_small = [{v_small[0]:.6f}, {v_small[1]:.6f}]^T")
print(f"v_large = [{v_large[0]:.6f}, {v_large[1]:.6f}]^T")

# ====================
# Case 1: ||δb||/||b|| 小，但 ||δx||/||x|| 大
# ====================
# b 沿大特征值方向 → x 较小
b1 = v_large.copy()
x1 = np.linalg.solve(A, b1)
print("\n",x1)
# δb 沿小特征值方向 → δx 会被放大
eps = 1e-6
delta_b1 = v_small * eps  # 小扰动，但方向不同！
delta_x1 = np.linalg.solve(A, delta_b1)

rel_db1 = np.linalg.norm(delta_b1, np.inf) / np.linalg.norm(b1, np.inf)
rel_dx1 = np.linalg.norm(delta_x1, np.inf) / np.linalg.norm(x1, np.inf)

print("\n=== Case 1: ||δb||/||b|| small, ||δx||/||x|| large ===")
print(f"||δb||_∞ / ||b||_∞ = {rel_db1:.2e}")
print(f"||δx||_∞ / ||x||_∞ = {rel_dx1:.2e}")
print(f"Ratio (||δx||/||x||) / (||δb||/||b||) = {rel_dx1 / rel_db1:.2e}")

# ====================
# Case 2: ||δb||/||b|| 大，但 ||δx||/||x|| 小
# ====================
# b 沿小特征值方向 → x 很大
b2 = v_small.copy()
x2 = np.linalg.solve(A, b2)
print("\n",x2)
# δb 沿大特征值方向 → δx 很小
eps2 = 1e3
delta_b2 = v_large * eps2  # 大扰动
delta_x2 = np.linalg.solve(A, delta_b2)

rel_db2 = np.linalg.norm(delta_b2, np.inf) / np.linalg.norm(b2, np.inf)
rel_dx2 = np.linalg.norm(delta_x2, np.inf) / np.linalg.norm(x2, np.inf)

print("\n=== Case 2: ||δb||/||b|| large, ||δx||/||x|| small ===")
print(f"||δb||_∞ / ||b||_∞ = {rel_db2:.2e}")
print(f"||δx||_∞ / ||x||_∞ = {rel_dx2:.2e}")
print(f"Ratio (||δx||/||x||) / (||δb||/||b||) = {rel_dx2 / rel_db2:.2e}")

# 理论条件数
cond_A = abs(lambda_large / lambda_small)
print(f"\nTheoretical condition number κ(A) = |λ_large / λ_small| ≈ {cond_A:.2e}")