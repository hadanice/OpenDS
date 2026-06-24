import numpy as np


def gauss_elim_no_pivot(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    # 前向消元
    for k in range(n-1):
        # 检查主元是否为0
        if abs(A[k, k]) < 1e-12:
            raise ValueError(f"主元 A[{k},{k}] 为零，无法继续消元")

        # 消去第k列下方的元素
        for i in range(k + 1, n):
            factor=A[i,k]/A[k,k]
            A[i,k:]-=factor*A[k,k:]
            b[i]-=factor*b[k]

    # 回代求解
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x

def gauss_elim_pivot(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    # 前向消元（带部分选主元）
    for k in range(n - 1):
        # 部分选主元：在第k列从第k行到最后一行中找绝对值最大的元素
        max_row = k + np.argmax(np.abs(A[k:, k]))

        # 如果最大元素为0，说明矩阵奇异
        if abs(A[max_row, k]) < 1e-12:
            raise ValueError("矩阵奇异，无唯一解")

        # 交换行（如果需要）
        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            b[[k, max_row]] = b[[max_row, k]]

        # 消去第k列下方的元素
        for i in range(k + 1, n):
            factor = A[i, k] / A[k, k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]

    # 回代求解
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x

def tridiag_linear_system(n,head,main_val,off_val,up_val):
    b=np.full(n,15)
    b[0],b[-1]=head,14
    print(b)
    A=np.diag(np.full(n,main_val))+np.diag(np.full(n-1,up_val),1)+np.diag(np.full(n-1,off_val),-1)
    print(A)
    return A,b

if __name__ == "__main__":
    A,b=tridiag_linear_system(100,7,6,8,1)
    x1=gauss_elim_no_pivot(A,b)
    x2=gauss_elim_pivot(A,b)
    print(x1,x2)
