import numpy as np
from scipy.linalg import pascal
np.set_printoptions(suppress=True, precision=12)
np.set_printoptions(linewidth=1000)
n=int(input("输入矩阵维数： "))
P=pascal(n, kind='symmetric')
L=np.linalg.cholesky(P)
print("L=\n", L)
print("L.T=\n",L.T)
print("L@L.T=\n", L @ L.T)