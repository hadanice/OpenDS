import numpy as np
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False

x=np.random.randn(2, 1)
print(x)
norm_sq = x[0,0]**2 + x[1,0]**2
epsilon = 1e-15
n=int(input("请输入一个整数"))
pairs=np.zeros((2**n,2))
for k in range(2**n):
    θ=2*k*np.pi/2**n
    A = np.array([[math.cos(θ), math.sin(θ)],
              [-math.sin(θ), math.cos(θ)]])
    comp=x.T@A@x
    exact=norm_sq*math.cos(θ)
    error=abs(comp-exact)/(abs(exact)+epsilon)
    pairs[k,0]=k
    pairs[k,1]=error.item()


plt.figure(figsize=(10, 6))
plt.plot(pairs[:, 0], pairs[:, 1], 'b.', markersize=4)
plt.yscale('log') # 使用对数坐标更清晰显示微小误差
plt.xlabel('角度索引 k', fontsize=12)
plt.ylabel('相对误差（对数尺度）', fontsize=12)
plt.title(f'相对误差 (n={n})', fontsize=14)
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()