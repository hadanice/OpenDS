import numpy as np
import matplotlib.pyplot as plt
#Q1 content
def ridge_bidiagonal_givens(A, b, lam):
    m,n=A.shape
    sqrt_lam=np.sqrt(lam)
    A_tilde=np.vstack([A,sqrt_lam*np.eye(n)])
    c=np.concatenate([b,np.zeros(n)])

    for j in range(n):
        for i in range(m+n-1,j,-1):
            if A_tilde[i,j] != 0:
                a,b_val=A_tilde[j,j],A_tilde[i,j]
                r=np.hypot(a,b_val)
                if r==0:
                    c_g,s_g=1.0, 0.0
                else:
                    c_g,s_g=a/r,b_val/r
                A_tilde[[j,i],j:] = np.array([
                    c_g*A_tilde[j,j:]+s_g*A_tilde[i,j:],
                    -s_g*A_tilde[j,j:]+c_g*A_tilde[i,j:]
                ])
                c[j],c[i]=c_g*c[j]+s_g*c[i],-s_g*c[j]+c_g*c[i]

    R,c_reduced=A_tilde[:n],c[:n]
    x=np.zeros(n)
    for i in range(n-1,-1,-1):
        x[i]=(c_reduced[i]-R[i,i+1:]@x[i+1:])/R[i,i]
    return x

#Q2 content
def householder_qr_Ct(C):
    """
    对 C^T (形状 n x p) 做 Householder QR（只做前 p 次反射）。
    输入:
        C: shape (p, n)
    返回:
        R: shape (p, p) 上三角矩阵，使得 C^T 被反射后前 p 行 = R
        vs: list of length p，每个是长度 n 的反射向量 v (第 k 个反射从位置 k 开始非零)
        taus: list of length p，每个是对应的 tau
    说明:
        在原 Ct = C.T (n x p) 上原地做变换以得到 R，返回的 vs, taus 可以用于
        右乘变换 A <- A * H_k (H_k = I - tau v v^T) 或用于作用于向量 y。
    """
    C = np.asarray(C)
    p, n = C.shape
    Ct = C.T.copy()   # Ct: n x p
    n_rows, n_cols = Ct.shape
    vs = []
    taus = []
    for k in range(n_cols):
        x = Ct[k:, k].copy()
        normx = np.linalg.norm(x)
        if normx == 0:
            tau = 0.0
            v = np.zeros_like(x)
            v[0] = 1.0
        else:
            alpha = -np.sign(x[0]) * normx
            v_small = x.copy()
            v_small[0] -= alpha
            v_small = v_small / np.linalg.norm(v_small)
            tau = 2.0
            v = v_small
        v_full = np.zeros(n_rows)
        v_full[k:] = v
        if tau != 0.0:
            sub = Ct[k:, k:]
            vt_sub = v @ sub
            sub -= np.outer(v, tau * vt_sub)
            Ct[k:, k:] = sub
        vs.append(v_full)
        taus.append(tau)
    R = Ct[:p, :].T.copy()  # shape p x p
    return R, vs, taus

def apply_reflectors_right(A, vs, taus):
    """
    对矩阵 A (m x n) 做右乘一系列反射器 H_k=I-tau_k v_k v_k^T，
    即 A <- A * H1 * H2 * ... （按 vs, taus 的顺序）
    vs 中每个 v 长度为 n。
    """
    A = A.copy()
    for v, tau in zip(vs, taus):
        if tau == 0.0:
            continue
        Av = A @ v
        A -= np.outer(Av, tau * v)
    return A

def apply_reflectors_left_vec(y, vs, taus):
    """
    将 y (长度 n) 左乘 Q = H1 H2 ... （反射器按顺序）：
    y <- Q y
    注意这里 Hk 都是作用在长度 n 向量上的。
    """
    y = y.copy()
    for v, tau in zip(vs, taus):
        if tau == 0.0:
            continue
        vy = v @ y
        y -= tau * v * vy
    return y

def solve_lse_via_qr_ct(A, b, C, d, rcond=1e-12):
    """
    使用对 C^T 做 QR 的方法求解带等式约束的最小二乘问题。
    返回 x (长度 n)。
    """
    A = np.asarray(A)
    b = np.asarray(b)
    C = np.asarray(C)
    d = np.asarray(d)
    m, n = A.shape
    p = C.shape[0]
    assert C.shape[1] == n
    assert d.shape[0] == p
    # 1. 对 C^T 做 Householder QR，得到 R (p x p) 和反射器
    R, vs, taus = householder_qr_Ct(C)
    # 2. 解 R^T y1 = d  -> y1 长度 p
    # 注意 R 是上三角，R^T 是下三角
    y1 = np.linalg.solve(R.T, d)
    # 3. 用反射器把 A 右乘 Q （不显式构造 Q）
    AQ = apply_reflectors_right(A, vs, taus)  # shape m x n
    A1 = AQ[:, :p] if p > 0 else np.zeros((m, 0))
    A2 = AQ[:, p:] if p < n else np.zeros((m, 0))
    # 4. 构造 b_hat = b - A1 y1
    b_hat = b - A1 @ y1 if p > 0 else b.copy()
    # 5. 对 y2 做无约束最小二乘： minimize ||A2 y2 - b_hat||
    if A2.shape[1] == 0:
        y2 = np.zeros(0)
    else:
        # 使用 np.linalg.lstsq 求解
        y2, *_ = np.linalg.lstsq(A2, b_hat, rcond=rcond)
    # 6. 合并 y，并恢复 x = Q y（Q = H1 H2 ...）
    y = np.concatenate([y1, y2]) if p < n else y1.copy()
    # 7. x = Q y
    x = apply_reflectors_left_vec(y, vs, taus)
    return x

def test_random(seed=0, trials=5):
    rng = np.random.default_rng(seed)
    for t in range(trials):
        m = rng.integers(10, 60)
        n = rng.integers(6, 20)
        p = rng.integers(0, min(n, 6)+1)  # 最多 6 个约束，且 p<=n
        A = rng.standard_normal((m, n))
        x_true = rng.standard_normal(n)
        C = rng.standard_normal((p, n)) if p > 0 else np.zeros((0, n))
        d = C @ x_true if p > 0 else np.zeros(0)
        b = A @ x_true + 0.1 * rng.standard_normal(m)  # 加少量噪声
        x_hat = solve_lse_via_qr_ct(A, b, C, d)
        ATA = A.T @ A
        ATb = A.T @ b
        if p > 0:
            KKT = np.block([[ATA, C.T],
                            [C, np.zeros((p, p))]])
            rhs = np.concatenate([ATb, d])
            sol = np.linalg.lstsq(KKT, rhs, rcond=None)[0]
            x_kkt = sol[:n]
        else:
            x_kkt, *_ = np.linalg.lstsq(A, b, rcond=None)
        err_x = np.linalg.norm(x_hat - x_kkt) / max(1.0, np.linalg.norm(x_kkt))
        res_norm = np.linalg.norm(A @ x_hat - b)
        cons_violation = np.linalg.norm(C @ x_hat - d) if p > 0 else 0.0
        print(f"trial {t}: m={m}, n={n}, p={p}, rel_err_x={err_x:.3e}, ||Ax-b||={res_norm:.3e}, ||C x - d||={cons_violation:.3e}")

if __name__ == "__main__":
    test_random(seed=42, trials=8)


#Q5 content
def power_iteration_history(A,tol=1e-20,max_iter=1000):
    n=A.shape[0]
    u=np.ones(n)
    rho_history=[]
    prev_rho=0
    for i in range(max_iter):
        y=A@u
        rho=np.linalg.norm(y,ord=np.inf)
        rho_history.append(rho)
        u=y/rho
        if abs(rho-prev_rho)<tol:
            break
        prev_rho=rho
    return rho_history

np.random.seed(98)
A=np.random.rand(1000, 1000)

convergence_history = power_iteration_history(A)

plt.figure(figsize=(10, 6))
plt.plot(convergence_history, '-o', markersize=4)
plt.xlabel('Iteration Times')
plt.ylabel('Estimated Spectral Radius')
plt.title('Convergence of Power Iteration for $\\rho(A)$')
plt.grid(True)
plt.show()