import numpy as np
import math
import matplotlib.pyplot as plt

def MGS2(A):
    m,n=A.shape
    Q=np.zeros((m,n), dtype=A.dtype)
    R=np.zeros((n,n), dtype=A.dtype)
    for i in range(n):
        Q[:,i]=A[:,i]
        for j in range(i):
            R[j,i]=np.vdot(Q[:,j],Q[:,i])
            Q[:,i]-=Q[:,j]*R[j,i]
        for j in range(i):
            r=np.vdot(Q[:,j],Q[:,i])
            R[j,i]+=r
            Q[:,i]-=r*Q[:,j]
        R[i,i]=np.linalg.norm(Q[:,i])
        Q[:,i]/=R[i,i]
    return Q,R

def best_line(A,b):
    Q,R=MGS2(A)
    Qb=Q.T@b
    return np.linalg.solve(R,Qb)

def vis(A,b):
    x_points=A[:,1]
    y_points=b
    x=best_line(A,b)
    k=x[1]
    t=x[0]
    x_line=np.linspace(min(x_points)-0.5,max(x_points)+0.5,100)
    y_line=k*x_line+t
    plt.figure(figsize=(8, 6))
    plt.scatter(x_points, y_points, color='red', label='Data Points')
    plt.plot(x_line, y_line, color='blue', label=f'y = {k}x + {t}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatter Points with BEST Line')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    A=np.array([[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10]],dtype=float)
    b=np.array([math.log(3),math.log(4),math.log(5),math.log(6),
                math.log(7),math.log(8),math.log(9),math.log(10)])
    vis(A,b)