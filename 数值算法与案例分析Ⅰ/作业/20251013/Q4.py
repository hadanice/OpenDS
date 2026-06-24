import numpy as np
import matplotlib.pyplot as plt

def CGS(A):
    m,n=A.shape
    Q=np.zeros((m,n), dtype=A.dtype)
    R=np.zeros((n,n), dtype=A.dtype)
    for i in range(n):
        Q[:,i]=A[:,i]
        for j in range(i):
            R[j,i]=np.vdot(Q[:,j],A[:,i])
            Q[:,i]-=Q[:,j]*R[j,i]
        R[i,i]=np.linalg.norm(Q[:,i])
        Q[:,i]/=R[i,i]
    return Q,R

def MGS(A):
    m,n=A.shape
    Q=np.zeros((m,n), dtype=A.dtype)
    R=np.zeros((n,n), dtype=A.dtype)
    for i in range(n):
        Q[:,i]=A[:,i]
        for j in range(i):
            R[j,i]=np.vdot(Q[:,j],Q[:,i])
            Q[:,i]-=Q[:,j]*R[j,i]
        R[i,i]=np.linalg.norm(Q[:,i])
        Q[:,i]/=R[i,i]
    return Q,R

def CGS2(A):
    m,n=A.shape
    Q=np.zeros((m,n), dtype=A.dtype)
    R=np.zeros((n,n), dtype=A.dtype)
    for i in range(n):
        Q[:,i]=A[:,i]
        for j in range(i):
            R[j,i]=np.vdot(Q[:,j],A[:,i])
            Q[:,i]-=Q[:,j]*R[j,i]
        for j in range(i):
            r=np.vdot(Q[:,j],Q[:,i])
            R[j,i]+=r
            Q[:,i]-=r*Q[:,j]
        R[i,i]=np.linalg.norm(Q[:,i])
        Q[:,i]/=R[i,i]
    return Q,R

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


def visualize_qr_methods(A, methods, titles):
    n = A.shape[1]
    num_methods = len(methods)

    # 存储结果
    ortho_losses = []
    residuals = []
    Qs, Rs = [], []

    for method in methods:
        Q, R = method(A)
        Qs.append(Q)
        Rs.append(R)
        ortho_loss = np.abs(Q.conj().T @ Q - np.eye(n))
        residual = np.linalg.norm(A - Q @ R, ord='fro')
        ortho_losses.append(ortho_loss)
        residuals.append(residual)

    # ===== 图1: 正交性损失热图 =====
    fig1, axes1 = plt.subplots(1, num_methods, figsize=(5 * num_methods, 4))
    if num_methods == 1:
        axes1 = [axes1]


    #越深数值越小，越浅数值越大，更黑的图显示更低的Q*Q-I
    for idx in range(num_methods):
        im = axes1[idx].imshow(ortho_losses[idx], cmap='hot', vmin=0)
        axes1[idx].set_title(f'{titles[idx]}\nOrthogonality Loss', fontsize=12)
        axes1[idx].set_xlabel('j')
        axes1[idx].set_ylabel('i')
        plt.colorbar(im, ax=axes1[idx], shrink=0.8)
        max_val = ortho_losses[idx].max()
        axes1[idx].text(0.05, 0.95, f'max={max_val:.1e}',
                        transform=axes1[idx].transAxes,
                        color='white', fontsize=10,
                        bbox=dict(facecolor='black', alpha=0.6))

    plt.tight_layout()
    plt.show()

    # ===== 图2: 残差 ||A - QR||_F 柱状图 =====
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    bars = ax2.bar(titles, residuals, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:num_methods])
    ax2.set_yscale('log')
    ax2.set_ylabel(r'$\|A - QR\|_F$ (Frobenius norm)', fontsize=12)
    ax2.set_title('Reconstruction Residuals of QR Decompositions', fontsize=14)
    ax2.grid(True, which="both", ls="--", linewidth=0.5)

    y_min, y_max = min(residuals) * 0.9, max(residuals) * 1.05  # 下限缩小10%，上限扩大1倍
    ax2.set_ylim(bottom=y_min, top=y_max)

    # 在柱子上标注数值
    for bar, res in zip(bars, residuals):
        height = bar.get_height()
        y_pos = height *1.02
        ax2.text(bar.get_x() + bar.get_width() / 2.,y_pos,
                 f'{res:.1e}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 生成复矩阵 (m >= n)
    m, n = 100, 20
    for i in range(5):
        np.random.seed(i)
        A = np.random.randn(m, n) + 1j * np.random.randn(m, n)

        # 定义要比较的方法
        methods = [CGS, MGS, CGS2, MGS2]
        titles = ['CGS', 'MGS', 'CGS+Reorth', 'MGS+Reorth']

        # 可视化
        visualize_qr_methods(A, methods, titles)
