import numpy as np
import pandas as pd


#递归回代，自底向上逐层收缩矩阵
def solution1(U,b):
    n=len(b)
    b[n-1]=b[n-1]/U[n-1,n-1]
    for i in range(n-1):
        b[i]=b[i]-b[n-1]*U[i,n-1]
    if n>1:
        solution1(U[:n-1,:n-1],b[:n-1])
        return U,b
    else:    
        return U,b

#向量回代，比递归更高效    
def solution2(U,b):
    n=len(b)
    
    for i in range(n-1,-1,-1):
        b[i] = (b[i] - U[i, i+1:] @ b[i+1:]) / U[i, i]
    return U,b

def generate(n):
    U=np.triu(np.random.randn(n,n))
    b=np.random.randn(n)
    return U,b


print("输入要生成的上三角矩阵维数")
n = int(input("请输入一个整数: "))
U,b=generate(n)
U,b=solution2(U,b)
col_b=np.column_stack([b])
print(f"{col_b}")