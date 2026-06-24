import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False
from scipy.sparse import diags, csr_matrix

import warnings
warnings.filterwarnings("ignore", message=".*does not have a glyph.*")

import time
from typing import Callable, Tuple, List


def lanczos_matrix_functional(
        A_op: Callable[[np.ndarray], np.ndarray],
        v: np.ndarray,
        f: Callable[[np.ndarray], np.ndarray],
        m: int = 100,
        full_reorth: bool = True,
        tol: float = 1e-12
) -> Tuple[float, List[float]]:
    """
    使用Lanczos算法计算 v^H f(A) v

    参数:
        A_op: 矩阵A的算子，计算 A @ x
        v: 初始向量
        f: 函数，作用于特征值
        m: 最大Lanczos迭代步数
        full_reorth: 是否完全重正交化
        tol: 收敛容差

    返回:
        result: v^H f(A) v 的近似值
        history: 收敛历史
    """
    n = len(v)

    # 标准化初始向量
    beta = np.linalg.norm(v)
    if beta == 0:
        raise ValueError("初始向量不能为零向量")
    v0 = v / beta

    # 初始化Lanczos向量和系数
    V = np.zeros((n, m + 1), dtype=v.dtype)
    alphas = np.zeros(m, dtype=np.float64)
    betas = np.zeros(m, dtype=np.float64)

    # 收敛历史
    history = []

    # 第一个Lanczos向量
    V[:, 0] = v0

    # Lanczos迭代
    for j in range(m):
        # 计算 w = A * v_j
        w = A_op(V[:, j])

        # 计算 alpha_j = v_j^T w
        alpha = np.dot(V[:, j].conj(), w).real
        alphas[j] = alpha

        # 正交化：w = w - alpha_j * v_j - beta_{j-1} * v_{j-1}
        w -= alpha * V[:, j]
        if j > 0:
            w -= betas[j - 1] * V[:, j - 1]

        # 完全重正交化（可选）
        if full_reorth:
            for i in range(j + 1):
                w -= np.dot(V[:, i].conj(), w) * V[:, i]

        # 计算 beta_j = ||w||
        beta_j = np.linalg.norm(w)

        # 检查是否收敛
        if beta_j < tol:
            # 提前终止
            m_actual = j + 1
            alphas = alphas[:m_actual]
            betas = betas[:j]  # betas长度比alphas少1
            break

        betas[j] = beta_j

        # 下一个Lanczos向量
        if j < m - 1:
            V[:, j + 1] = w / beta_j

        # 构造三对角矩阵并计算当前近似值
        T_current = construct_tridiagonal(alphas[:j + 1], betas[:j])
        result_current = compute_functional_from_tridiagonal(T_current, f, beta=beta)
        history.append(result_current)

    # 如果没有提前终止，则使用完整的m步
    if 'm_actual' not in locals():
        m_actual = m
        betas = betas[:m - 1]  # 最后一个beta不会被使用

    # 构造最终的三对角矩阵
    T = construct_tridiagonal(alphas[:m_actual], betas[:m_actual - 1])

    # 计算最终结果
    result = compute_functional_from_tridiagonal(T, f, beta=beta)

    return result, history


def construct_tridiagonal(alphas: np.ndarray, betas: np.ndarray) -> np.ndarray:
    """从Lanczos系数构造三对角矩阵"""
    m = len(alphas)
    T = np.zeros((m, m))

    for i in range(m):
        T[i, i] = alphas[i]
        if i < m - 1:
            T[i, i + 1] = betas[i]
            T[i + 1, i] = betas[i]

    return T


def compute_functional_from_tridiagonal(
        T: np.ndarray,
        f: Callable[[np.ndarray], np.ndarray],
        beta: float = 1.0
) -> float:
    """从三对角矩阵T计算 e1^T f(T) e1 * beta^2"""
    # 计算T的特征值分解
    eigvals, eigvecs = np.linalg.eigh(T)

    # 应用函数f到特征值
    f_eigvals = f(eigvals)

    # 计算 e1^T * eigvecs * diag(f_eigvals) * eigvecs^T * e1
    e1 = np.zeros(len(eigvals))
    e1[0] = 1.0

    # 更稳定的计算方法
    result = np.dot(eigvecs[0, :] * f_eigvals, eigvecs[0, :])

    # 乘以初始向量的范数平方
    return result * beta ** 2


# 测试函数
def test_lanczos_matrix_functional():
    """测试Lanczos矩阵函数二次型算法"""
    print("=" * 60)
    print("测试Lanczos算法计算矩阵函数二次型")
    print("=" * 60)

    np.random.seed(42)

    # 测试1：小型稠密矩阵，验证正确性
    print("\n1. 小型稠密矩阵验证（n=200）")
    n_small = 200

    # 生成对称正定矩阵
    X = np.random.randn(n_small, n_small)
    A_small = X @ X.T / n_small + np.eye(n_small) * 0.1

    # 初始向量
    v_small = np.random.randn(n_small)

    # 定义测试函数
    test_functions = [
        ("exp(x)", lambda x: np.exp(x)),
        ("1/(1+x)", lambda x: 1 / (1 + x)),
        ("sqrt(1+x)", lambda x: np.sqrt(1 + x)),
        ("sin(x)", lambda x: np.sin(x)),
    ]

    # 精确计算（仅对小矩阵可行）
    for func_name, f in test_functions:
        # 计算精确值
        eigvals, eigvecs = np.linalg.eigh(A_small)
        f_A = eigvecs @ np.diag(f(eigvals)) @ eigvecs.T
        exact_value = v_small @ f_A @ v_small

        # Lanczos近似
        A_op = lambda x: A_small @ x
        approx_value, history = lanczos_matrix_functional(
            A_op, v_small, f, m=50, full_reorth=True
        )

        error = abs(approx_value - exact_value) / abs(exact_value)
        print(f"  {func_name:10s} | 精确值: {exact_value:.6e} | "
              f"近似值: {approx_value:.6e} | 相对误差: {error:.2e}")

    # 测试2：大型稀疏矩阵
    print("\n2. 大型稀疏矩阵测试（n=5000）")
    n_large = 5000

    # 创建三对角矩阵（离散的1D拉普拉斯算子）
    main_diag = 2 * np.ones(n_large)
    off_diag = -np.ones(n_large - 1)

    # 使用稀疏矩阵格式
    A_sparse = diags([main_diag, off_diag, off_diag], [0, 1, -1], format='csr')

    # 初始向量
    v_large = np.random.randn(n_large)

    # 定义函数 f(x) = exp(-x)（确保函数在A的谱上定义良好）
    f_exp_neg = lambda x: np.exp(-x)

    # 定义A的算子
    def A_op_large(x):
        return A_sparse @ x

    # 运行Lanczos算法
    start_time = time.time()
    approx_value, history = lanczos_matrix_functional(
        A_op_large, v_large, f_exp_neg, m=100, full_reorth=False
    )
    elapsed_time = time.time() - start_time

    print(f"  矩阵大小: {n_large} × {n_large}")
    print(f"  计算时间: {elapsed_time:.2f}秒")
    print(f"  近似值: {approx_value:.6e}")
    print(f"  迭代步数: {len(history)}")

    # 测试3：收敛历史分析
    print("\n3. 收敛历史分析")

    # 为不同函数测试收敛性
    test_funcs_convergence = [
        ("exp(-x)", lambda x: np.exp(-x)),
        ("1/(1+10x)", lambda x: 1 / (1 + 10 * x)),
    ]

    plt.figure(figsize=(14, 10))

    for idx, (func_name, f) in enumerate(test_funcs_convergence, 1):
        # 运行Lanczos
        approx_value, history = lanczos_matrix_functional(
            A_op_large, v_large, f, m=80, full_reorth=False
        )

        # 绘制收敛历史
        plt.subplot(2, 2, idx)
        iterations = range(1, len(history) + 1)

        # 计算相对变化
        if len(history) > 1:
            rel_change = np.abs(np.diff(history) / history[:-1])
            plt.semilogy(iterations[1:], rel_change, 'b-', linewidth=2, label='相对变化')
        plt.semilogy(iterations, [1e-10] * len(history), 'r--', label='1e-10阈值')

        plt.xlabel('Lanczos迭代步数')
        plt.ylabel('相对变化')
        plt.title(f'收敛历史: v^T {func_name}(A) v')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 绘制近似值
        plt.subplot(2, 2, idx + 2)
        plt.plot(iterations, history, 'g-', linewidth=2)
        plt.xlabel('Lanczos迭代步数')
        plt.ylabel('近似值')
        plt.title(f'近似值变化: {func_name}(A)')
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('lanczos_convergence_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

    # 测试4：不同正交化策略比较
    print("\n4. 正交化策略比较")

    # 使用中型矩阵进行比较
    n_medium = 1000
    X = np.random.randn(n_medium, n_medium)
    A_medium = X @ X.T / n_medium + np.eye(n_medium) * 0.1
    v_medium = np.random.randn(n_medium)

    A_op_medium = lambda x: A_medium @ x
    f_test = lambda x: np.exp(-x)

    # 精确值（用于比较）
    eigvals, eigvecs = np.linalg.eigh(A_medium)
    f_A = eigvecs @ np.diag(f_test(eigvals)) @ eigvecs.T
    exact_medium = v_medium @ f_A @ v_medium

    # 测试不同正交化策略
    strategies = [
        ("无重正交化", False),
        ("完全重正交化", True),
    ]

    plt.figure(figsize=(12, 8))

    for i, (strategy_name, reorth) in enumerate(strategies, 1):
        approx_value, history = lanczos_matrix_functional(
            A_op_medium, v_medium, f_test, m=60, full_reorth=reorth
        )

        iterations = range(1, len(history) + 1)

        plt.subplot(2, 2, i)
        plt.semilogy(iterations, np.abs(np.array(history) - exact_medium),
                     'b-', linewidth=2, label='绝对误差')
        plt.semilogy(iterations, [1e-10] * len(history), 'r--', label='1e-10阈值')
        plt.xlabel('迭代步数')
        plt.ylabel('绝对误差')
        plt.title(f'{strategy_name}: 误差收敛')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, i + 2)
        plt.plot(iterations, history, 'g-', linewidth=2, label='近似值')
        plt.axhline(y=exact_medium, color='r', linestyle='--', label='精确值')
        plt.xlabel('迭代步数')
        plt.ylabel('近似值')
        plt.title(f'{strategy_name}: 近似值')
        plt.legend()
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('lanczos_reorth_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()

    # 测试5：不同矩阵类型的性能测试
    print("\n5. 不同矩阵类型性能测试")

    matrix_types = [
        ("对角占优", lambda n: diags([2 * np.ones(n), -np.ones(n - 1), -np.ones(n - 1)],
                                     [0, 1, -1], format='csr')),
        ("随机稀疏", lambda n: csr_matrix(np.random.randn(n, n) * (np.random.rand(n, n) > 0.95))),
    ]

    sizes = [1000, 2000, 5000]

    results = {}
    for size in sizes:
        results[size] = {}
        for mat_type_name, mat_gen in matrix_types:
            print(f"  测试 {mat_type_name} 矩阵，大小 {size}×{size}")

            A_test = mat_gen(size)
            v_test = np.random.randn(size)

            # 确保矩阵对称
            if mat_type_name == "随机稀疏":
                A_test = (A_test + A_test.T) / 2

            A_op_test = lambda x: A_test @ x
            f_simple = lambda x: 1 / (1 + np.abs(x))

            start_time = time.time()
            approx_value, history = lanczos_matrix_functional(
                A_op_test, v_test, f_simple, m=50, full_reorth=False
            )
            elapsed_time = time.time() - start_time

            results[size][mat_type_name] = {
                'time': elapsed_time,
                'iterations': len(history),
                'value': approx_value
            }

            print(f"    时间: {elapsed_time:.3f}s, 迭代步数: {len(history)}, "
                  f"结果: {approx_value:.6e}")

    # 性能总结
    print("\n性能总结:")
    print("大小\t矩阵类型\t时间(s)\t迭代步数")
    print("-" * 50)
    for size in sizes:
        for mat_type_name in matrix_types:
            name = mat_type_name[0]
            if name in results[size]:
                data = results[size][name]
                print(f"{size}\t{name:12s}\t{data['time']:.3f}\t{data['iterations']}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


# 额外的应用示例：计算迹的估计
def stochastic_trace_estimation(
        A_op: Callable[[np.ndarray], np.ndarray],
        f: Callable[[np.ndarray], np.ndarray],
        n: int,
        num_samples: int = 10,
        m: int = 50
) -> float:
    """
    使用随机Lanczos算法估计 tr(f(A))

    这是v^T f(A) v的一个应用：通过随机向量平均估计矩阵函数的迹
    """
    trace_estimate = 0.0

    for i in range(num_samples):
        # 生成随机向量
        v = np.random.randn(n)
        v = v / np.linalg.norm(v)

        # 计算 v^T f(A) v
        val, _ = lanczos_matrix_functional(A_op, v, f, m=m, full_reorth=False)
        trace_estimate += val

    # 调整估计：E[v^T f(A) v] = (1/n) tr(f(A))
    trace_estimate = trace_estimate * n / num_samples

    return trace_estimate



# 运行主测试
test_lanczos_matrix_functional()

# 额外演示：迹估计
print("\n" + "=" * 60)
print("额外演示：随机迹估计")
print("=" * 60)

# 创建测试矩阵
n_demo = 3000
X = np.random.randn(n_demo, n_demo)
A_demo = X @ X.T / n_demo + np.eye(n_demo) * 0.1

# 定义函数
f_demo = lambda x: np.exp(-x)

# 精确迹（仅对小矩阵可行）
eigvals, _ = np.linalg.eigh(A_demo)
exact_trace = np.sum(f_demo(eigvals))

# 迹估计
A_op_demo = lambda x: A_demo @ x
estimated_trace = stochastic_trace_estimation(
    A_op_demo, f_demo, n_demo, num_samples=5, m=30
)

print(f"精确迹: {exact_trace:.6e}")
print(f"估计迹: {estimated_trace:.6e}")
print(f"相对误差: {abs(estimated_trace - exact_trace) / abs(exact_trace):.2e}")