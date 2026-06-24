import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
import matplotlib.pyplot as plt


def gmres(A, b, maxiter=100, tol=1e-6):
    n = len(b)
    x = np.zeros(n)
    r = b - A @ x
    beta = np.linalg.norm(r)
    V = np.zeros((n, maxiter + 1))
    H = np.zeros((maxiter + 1, maxiter))
    V[:, 0] = r / beta
    res_hist = [beta]

    for k in range(1, maxiter + 1):
        w = A @ V[:, k - 1]
        for j in range(k):
            H[j, k - 1] = V[:, j].dot(w)
            w -= H[j, k - 1] * V[:, j]
        H[k, k - 1] = np.linalg.norm(w)
        if H[k, k - 1] < tol:
            break
        V[:, k] = w / H[k, k - 1]

        y = np.linalg.lstsq(H[:k + 1, :k], np.array([beta] + [0] * k), rcond=None)[0]
        x = x + V[:, :k] @ y
        r = b - A @ x
        res_hist.append(np.linalg.norm(r))

    return x, res_hist


n = 1000
A_sym = sp.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
b_sym = np.ones(n)
x_sym, res_sym = gmres(A_sym, b_sym)

A_non_sym = sp.rand(n, n, density=0.05, format='csc')
b_non_sym = np.ones(n)
x_non_sym, res_non_sym = gmres(A_non_sym, b_non_sym)

plt.figure(figsize=(10, 6))
plt.semilogy(res_sym, 'b-', label='Symmetric')
plt.semilogy(res_non_sym, 'r-', label='Nonsymmetric')
plt.xlabel('Iteration')
plt.ylabel('Residual norm')
plt.legend()
plt.title('GMRES Residual History')
plt.grid(True)
plt.show()