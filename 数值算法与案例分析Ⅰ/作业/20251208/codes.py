import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import norm, eigh


# Two-pass Modified Gram-Schmidt reorthogonalization of a new vector w
# against the existing basis V[:, :k+1]. Returns the orthogonalized w.
def reorthogonalize(w, V, k):
    # V: (n, m) array, k: current index (we orthogonalize against V[:, :k+1])
    if k < 0:
        return w
    for _ in range(2):
        for j in range(k + 1):
            coeff = np.dot(V[:, j], w)
            w -= coeff * V[:, j]
    return w


# Lanczos algorithm with MGS2 reorthogonalization applied to the new residual w
def lanczos_mgs2(A, v, num_iter, tol=1e-14):
    n = A.shape[0]
    V = np.zeros((n, num_iter + 1))
    alpha = np.zeros(num_iter)
    beta = np.zeros(num_iter)
    T = np.zeros((num_iter, num_iter))

    V[:, 0] = v / norm(v)
    m = num_iter
    terminated = False
    for k in range(num_iter):
        w = A.dot(V[:, k])
        alpha[k] = np.dot(V[:, k], w)
        w = w - alpha[k] * V[:, k]
        if k > 0:
            w = w - beta[k - 1] * V[:, k - 1]

        # Reorthogonalize the new residual against current basis (two-pass MGS)
        w = reorthogonalize(w, V, k)

        beta_k = norm(w)
        beta[k] = beta_k

        # Handle breakdown / early termination
        if beta_k <= tol * max(1.0, norm(alpha[:k+1])):
            # Lanczos has converged exactly (lucky breakdown) or numerical breakdown
            m = k + 1
            terminated = True
            # set T diagonal for current k
            T[k, k] = alpha[k]
            break

        if k < num_iter - 1:
            V[:, k + 1] = w / beta_k

        # Fill tridiagonal entries
        T[k, k] = alpha[k]
        if k < num_iter - 1:
            T[k, k + 1] = beta[k]
            T[k + 1, k] = beta[k]

    if not terminated:
        m = num_iter

    # Trim outputs to the actual computed size
    T = T[:m, :m]
    V = V[:, :m]
    alpha = alpha[:m]
    beta = beta[:m]
    return T, V, alpha, beta


# Standard three-term Lanczos (no reorthogonalization)
def lanczos_standard(A, v, num_iter, tol=1e-14):
    n = A.shape[0]
    V = np.zeros((n, num_iter + 1))
    alpha = np.zeros(num_iter)
    beta = np.zeros(num_iter)
    T = np.zeros((num_iter, num_iter))

    V[:, 0] = v / norm(v)
    m = num_iter
    terminated = False
    for k in range(num_iter):
        w = A.dot(V[:, k])
        alpha[k] = np.dot(V[:, k], w)
        w = w - alpha[k] * V[:, k]
        if k > 0:
            w = w - beta[k - 1] * V[:, k - 1]

        beta_k = norm(w)
        beta[k] = beta_k

        # breakdown check
        if beta_k <= tol * max(1.0, norm(alpha[:k+1])):
            m = k + 1
            terminated = True
            T[k, k] = alpha[k]
            break

        if k < num_iter - 1:
            V[:, k + 1] = w / beta_k

        T[k, k] = alpha[k]
        if k < num_iter - 1:
            T[k, k + 1] = beta[k]
            T[k + 1, k] = beta[k]

    if not terminated:
        m = num_iter

    T = T[:m, :m]
    V = V[:, :m]
    alpha = alpha[:m]
    beta = beta[:m]
    return T, V, alpha, beta


# Utilities to compute Ritz histories and diagnostics
def ritz_history(T):
    # returns array of largest Ritz value for each k=1..m where m = T.shape[0]
    m = T.shape[0]
    ritz_vals = np.zeros(m)
    for k in range(1, m + 1):
        Tk = T[:k, :k]
        w, v = eigh(Tk)
        ritz_vals[k - 1] = w[-1]  # largest eigenvalue
    return ritz_vals


def max_orthogonality_violation(V):
    G = V.T.dot(V)
    m = G.shape[0]
    I = np.eye(m)
    off = np.abs(G - I)
    np.fill_diagonal(off, 0.0)
    return off.max()


def run_experiment(n=1000, num_iter=200, seed=0, save_prefix="results"):
    np.random.seed(seed)
    A = np.diag(np.linspace(1, 1000, n))
    v = np.random.rand(n)
    true_lambda = np.max(np.diag(A))
    # true eigenvector for diagonal matrix is a canonical basis vector
    idx = int(np.argmax(np.diag(A)))
    e_true = np.zeros(n)
    e_true[idx] = 1.0

    # Run MGS2 Lanczos
    T_mgs2, V_mgs2, a_mgs2, b_mgs2 = lanczos_mgs2(A, v, num_iter)
    T_std, V_std, a_std, b_std = lanczos_standard(A, v, num_iter)

    # Ritz histories
    ritz_mgs2 = ritz_history(T_mgs2)
    ritz_std = ritz_history(T_std)

    # Compute eigenvalue errors
    eig_err_mgs2 = np.abs(ritz_mgs2 - true_lambda)
    eig_err_std = np.abs(ritz_std - true_lambda)

    # Compute Ritz vector approximation error for the largest Ritz
    def vec_errors(T, V):
        m = T.shape[0]
        errs = np.zeros(m)
        for k in range(1, m + 1):
            Tk = T[:k, :k]
            wk, vk = eigh(Tk)
            y = vk[:, -1]
            x_hat = V[:, :k].dot(y)
            # normalize
            x_hat = x_hat / norm(x_hat)
            # account for sign ambiguity
            errs[k - 1] = min(norm(x_hat - e_true), norm(x_hat + e_true))
        return errs

    vec_err_mgs2 = vec_errors(T_mgs2, V_mgs2)
    vec_err_std = vec_errors(T_std, V_std)

    # Orthogonality violations
    ortho_mgs2 = max_orthogonality_violation(V_mgs2)
    ortho_std = max_orthogonality_violation(V_std)

    # Per-iteration orthogonality history
    def ortho_history(V):
        m = V.shape[1]
        hist = np.zeros(m)
        for k in range(1, m + 1):
            G = V[:, :k].T.dot(V[:, :k])
            I = np.eye(k)
            off = np.abs(G - I)
            np.fill_diagonal(off, 0.0)
            hist[k - 1] = off.max()
        return hist

    ortho_hist_mgs2 = ortho_history(V_mgs2) if V_mgs2.shape[1] > 0 else np.array([])
    ortho_hist_std = ortho_history(V_std) if V_std.shape[1] > 0 else np.array([])

    # Save separate convergence plots for each algorithm (eigenvalue error and vector error)
    eps = np.finfo(float).eps

    def safe_clip(arr):
        return np.clip(np.nan_to_num(arr, nan=eps, posinf=None, neginf=eps), eps, None)

    # MGS2 convergence plot
    if len(eig_err_mgs2) > 0:
        kx = np.arange(1, len(eig_err_mgs2) + 1)
        y_eig = safe_clip(eig_err_mgs2)
        y_vec = safe_clip(vec_err_mgs2)
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        axs[0].plot(kx, y_eig, marker='o', markersize=4, linewidth=1, label='|λ_hat - λ| (MGS2)')
        axs[0].set_yscale('log')
        axs[0].set_ylabel('Eigenvalue error')
        axs[0].grid(True)
        axs[0].legend()

        axs[1].plot(kx, y_vec, marker='o', markersize=4, linewidth=1, label='vector err (MGS2)')
        axs[1].plot(kx, y_vec ** 2, '--', linewidth=1, label='(vector err)^2 (MGS2)')
        axs[1].set_yscale('log')
        axs[1].set_xlabel('Iteration k')
        axs[1].set_ylabel('Vector error')
        axs[1].grid(True)
        axs[1].legend()

        fig.suptitle('MGS2 convergence (algebraically largest eigenvalue and vector)')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(f"{save_prefix}_mgs2_convergence.png")
        plt.close(fig)

    # Standard convergence plot
    if len(eig_err_std) > 0:
        kx = np.arange(1, len(eig_err_std) + 1)
        y_eig = safe_clip(eig_err_std)
        y_vec = safe_clip(vec_err_std)
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        axs[0].plot(kx, y_eig, marker='s', markersize=4, linewidth=1, label='|λ_hat - λ| (Standard)')
        axs[0].set_yscale('log')
        axs[0].set_ylabel('Eigenvalue error')
        axs[0].grid(True)
        axs[0].legend()

        axs[1].plot(kx, y_vec, marker='s', markersize=4, linewidth=1, label='vector err (Standard)')
        axs[1].set_yscale('log')
        axs[1].plot(kx, y_vec ** 2, '--', linewidth=1, label='(vector err)^2 (Standard)')
        axs[1].set_xlabel('Iteration k')
        axs[1].set_ylabel('Vector error')
        axs[1].grid(True)
        axs[1].legend()

        fig.suptitle('Standard Lanczos convergence (algebraically largest eigenvalue and vector)')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(f"{save_prefix}_std_convergence.png")
        plt.close(fig)

    # Per-algorithm scatter plot eig error vs (vec_err)^2 and slope fit
    def fit_log_slope(x, y):
        mask = (x > 0) & (y > 0)
        if np.sum(mask) < 2:
            return None
        lx = np.log(x[mask])
        ly = np.log(y[mask])
        A = np.vstack([lx, np.ones_like(lx)]).T
        b, a = np.linalg.lstsq(A, ly, rcond=None)[0]
        return b

    slope_mgs2 = None
    slope_std = None
    if len(eig_err_mgs2) > 0 and len(vec_err_mgs2) > 0:
        x = safe_clip(vec_err_mgs2 ** 2)
        y = safe_clip(eig_err_mgs2)
        plt.figure()
        plt.scatter(x, y, marker='o', s=20, label='MGS2')
        slope_mgs2 = fit_log_slope(x, y)
        if slope_mgs2 is not None:
            plt.title(f'MGS2: slope (log-log) ≈ {slope_mgs2:.3f}')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('(vector error)^2')
        plt.ylabel('|λ_hat - λ|')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{save_prefix}_eig_vs_vecsq_mgs2.png")
        plt.close()

    if len(eig_err_std) > 0 and len(vec_err_std) > 0:
        x = safe_clip(vec_err_std ** 2)
        y = safe_clip(eig_err_std)
        plt.figure()
        plt.scatter(x, y, marker='s', s=20, label='Standard')
        slope_std = fit_log_slope(x, y)
        if slope_std is not None:
            plt.title(f'Standard: slope (log-log) ≈ {slope_std:.3f}')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('(vector error)^2')
        plt.ylabel('|λ_hat - λ|')
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{save_prefix}_eig_vs_vecsq_std.png")
        plt.close()

    # Plot orthogonality history
    plt.figure()
    plotted = False
    if ortho_hist_mgs2.size > 0:
        oh_mgs2 = np.clip(np.nan_to_num(ortho_hist_mgs2, nan=eps, posinf=None, neginf=eps), eps, None)
        plt.plot(np.arange(1, len(oh_mgs2) + 1), oh_mgs2, marker='o', markersize=4, linewidth=1, label='orthogonality (MGS2)')
        plotted = True
    if ortho_hist_std.size > 0:
        oh_std = np.clip(np.nan_to_num(ortho_hist_std, nan=eps, posinf=None, neginf=eps), eps, None)
        plt.plot(np.arange(1, len(oh_std) + 1), oh_std, marker='s', markersize=4, linewidth=1, label='orthogonality (Standard)')
        plotted = True
    if plotted:
        plt.yscale('log')
        plt.xlabel('Iteration k')
        plt.ylabel('max |V^T V - I| (off-diag)')
        plt.title('Orthogonality history')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{save_prefix}_orthogonality.png")
    else:
        with open(f"{save_prefix}_orthogonality.txt", 'w', encoding='utf-8') as f:
            f.write('No orthogonality history data to plot for either method.\n')
    plt.close()

    # Orthogonality violation plot (single numbers printed and saved as text)
    with open(f"{save_prefix}_summary.txt", 'w', encoding='utf-8') as f:
        f.write(f"true_λ = {true_lambda}\n")
        f.write(f"MGS2: basis cols = {V_mgs2.shape[1]}, max ortho violation = {ortho_mgs2}\n")
        f.write(f"Standard: basis cols = {V_std.shape[1]}, max ortho violation = {ortho_std}\n")
        f.write(f"MGS2: eig_err length = {len(eig_err_mgs2)}, vec_err length = {len(vec_err_mgs2)}, ortho_hist length = {len(ortho_hist_mgs2)}\n")
        f.write(f"Standard: eig_err length = {len(eig_err_std)}, vec_err length = {len(vec_err_std)}, ortho_hist length = {len(ortho_hist_std)}\n")
        f.write(f"final eigenvalue error MGS2 = {eig_err_mgs2[-1] if len(eig_err_mgs2)>0 else None}\n")
        f.write(f"final eigenvalue error Standard = {eig_err_std[-1] if len(eig_err_std)>0 else None}\n")
        f.write(f"slope (log-log) MGS2 = {slope_mgs2}\n")
        f.write(f"slope (log-log) Standard = {slope_std}\n")

    print("Experiment finished. Results saved:")
    outputs = [f"{save_prefix}_mgs2_convergence.png", f"{save_prefix}_std_convergence.png", f"{save_prefix}_eig_vs_vecsq_mgs2.png", f"{save_prefix}_eig_vs_vecsq_std.png", f"{save_prefix}_orthogonality.png", f"{save_prefix}_summary.txt"]
    for p in outputs:
        print(f" - {p}")
    return {
        'T_mgs2': T_mgs2,
        'V_mgs2': V_mgs2,
        'T_std': T_std,
        'V_std': V_std,
        'eig_err_mgs2': eig_err_mgs2,
        'eig_err_std': eig_err_std,
        'vec_err_mgs2': vec_err_mgs2,
        'vec_err_std': vec_err_std,
        'ortho_mgs2': ortho_mgs2,
        'ortho_std': ortho_std,
    }


if __name__ == '__main__':
    # smaller size by default so this script runs quickly; change args above for larger tests
    res = run_experiment(n=1000, num_iter=200, seed=1, save_prefix="lanczos_results")
