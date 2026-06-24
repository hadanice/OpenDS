import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.linalg import hilbert, lu_factor, lu_solve, norm

#Q3 content
def invit(A, mu, max_it=100, tol=1e-10):
    n = A.shape[0]
    x = np.random.randn(n)
    x = x / np.linalg.norm(x)
    eigs = []
    res = []
    Ash = A - mu * np.eye(n)
    lu, piv = lu_factor(Ash)
    for i in range(max_it):
        y = lu_solve((lu, piv), x)
        rq = (x.T @ A @ x) / (x.T @ x)
        eigs.append(rq)
        x_new = y / np.linalg.norm(y)
        r = np.linalg.norm(x_new - x)
        res.append(r)
        x = x_new
        if r < tol:
            break
    return eigs, res, i + 1

def rqi(A, mu0, max_it=100, tol=1e-12):
    n = A.shape[0]
    x = np.random.randn(n)
    x = x / np.linalg.norm(x)
    mu = mu0
    eigs = []
    res = []
    for i in range(max_it):
        rq = (x.T @ A @ x) / (x.T @ x)
        eigs.append(rq)
        mu = rq
        Ash = A - mu * np.eye(n)
        lu, piv = lu_factor(Ash)
        y = lu_solve((lu, piv), x)
        x_new = y / np.linalg.norm(y)
        r = np.linalg.norm((A @ x_new) - rq * x_new)
        res.append(r)
        x = x_new
        if r < tol:
            break
    return eigs, res, i + 1

np.random.seed(42)
n = 200
A = hilbert(n)
mu = 2.0

print("INVIT:")
t0 = time.time()
e1, r1, it1 = invit(A, mu)
t1 = time.time() - t0
print(f"Eig: {e1[-1]:.15f}")
print(f"It: {it1}")
print(f"Time: {t1:.6f}s")

print("\nRQI:")
t0 = time.time()
e2, r2, it2 = rqi(A, mu)
t2 = time.time() - t0
print(f"Eig: {e2[-1]:.15f}")
print(f"It: {it2}")
print(f"Time: {t2:.6f}s")

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.semilogy(range(len(e1)), [abs(v - e1[-1]) for v in e1], 'b-o', label='INVIT')
plt.semilogy(range(len(e2)), [abs(v - e2[-1]) for v in e2], 'r-s', label='RQI')
plt.xlabel('Iter')
plt.ylabel('Eig Err')
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 2)
plt.semilogy(r1, 'b-o', label='INVIT')
plt.semilogy(r2, 'r-s', label='RQI')
plt.xlabel('Iter')
plt.ylabel('Res')
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 3)
plt.bar(['INVIT', 'RQI'], [t1, t2])
plt.ylabel('Time (s)')

plt.tight_layout()
plt.show()


#Q4 content
def eig_back_sub(A):
    n=A.shape[0]
    eig_list=[]
    for i in range(n):
        u=A[i,i]
        B=A-u*np.eye(n)
        x=np.zeros(n,dtype=float)
        x[i]=1
        for j in range(i-1,-1,-1):
                x[j]=-(B[j,j+1:]@x[j+1:])/B[j,j]
        x/=np.linalg.norm(x)
        eig_list.append(x)
    return eig_list

np.random.seed(0)

for size in [10,100,1000]:
    A = np.triu(np.random.randn(size, size))
    diag_vals = np.random.permutation(np.arange(1, size + 1))
    np.fill_diagonal(A, diag_vals)
    V_my = eig_back_sub(A)
    vals_lib, V_lib = np.linalg.eig(A)
    max_err = 0.0
    for i in range(size):
        v_my = V_my[i]
        j = np.argmin(np.abs(vals_lib - A[i, i]))
        v_lib = V_lib[:, j]
        v_lib /= np.linalg.norm(v_lib)
        err = min(np.linalg.norm(v_my-v_lib), np.linalg.norm(v_my + v_lib))
        max_err = max(max_err, err)

    print(f"n={size}: max eigenvector error = {max_err:.2e}")


# Q5 content
def householder(A):
    A = np.asarray(A, dtype=np.float64).copy()
    n = A.shape[0]
    Q = np.eye(n, dtype=np.float64)
    for i in range(n - 2):
        x = A[i+1:,i].copy()
        norm_x = norm(x)
        if norm_x == 0.0:
            continue
        alpha = -np.copysign(norm_x, x[0])
        v = x.copy()
        v[0] -= alpha
        v_norm = np.linalg.norm(v)
        if v_norm == 0.0:
            continue
        v /= v_norm
        A[i+1:,i:] -= 2.0 * np.outer(v,v @ A[i+1:,i:])
        A[:,i+1:] -= 2.0 * np.outer(A[:,i+1:] @ v,v)
        Q[:,i+1:] -= 2.0 * np.outer(Q[:,i+1:] @ v,v)
    return A,Q


def Arnoldi_MGS(A):
    A = np.asarray(A, dtype=np.float64).copy()
    n = A.shape[0]
    Q = np.zeros((n, n), dtype=np.float64)
    H = np.zeros((n, n), dtype=np.float64)
    q0 = np.random.randn(n)
    Q[:, 0] = q0 / norm(q0)
    tol = np.finfo(np.float64).eps * norm(A)
    for j in range(n):
        v = A @ Q[:, j]
        for i in range(j + 1):
            H[i, j] = Q[:, i] @ v
            v -= H[i, j] * Q[:, i]
        if j < n - 1:
            h_next = norm(v)
            if h_next <= tol:
                if j + 1 < n:
                    H[j + 1:, j] = 0.0
                break
            H[j + 1, j] = h_next
            Q[:, j + 1] = v / h_next
    return H, Q

np.random.seed(0)
sizes = [10,100,1000,2000]
for n in sizes:
    print(f"\n{'=' * 40}")
    print(f"\nTesting n = {n}")
    A = np.random.randn(n, n)

    print(f"\nHouseholder")
    h, q = householder(A)
    err_sim = np.linalg.norm(q.T @ A @ q - h, ord='fro')
    err_orth = np.linalg.norm(q.T @ q - np.eye(n), ord='fro')
    print(f" ||Q*AQ-H||F = {err_sim:.2e}")
    print(f" ||Q*Q-I||F  = {err_orth:.2e}")

    print(f"\nArnoldi_MGS")
    H, Q = Arnoldi_MGS(A)
    err_sim = np.linalg.norm(Q.T @ A @ Q - H, ord='fro')
    err_orth = np.linalg.norm(Q.T @ Q - np.eye(n), ord='fro')
    print(f" ||Q*AQ-H||F = {err_sim:.2e}")
    print(f" ||Q*Q-I||F  = {err_orth:.2e}")
