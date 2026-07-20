---
title: "06 特征值、极小多项式与 Jordan 标准形"
course: "高等线性代数"
---

# 06 特征值、极小多项式与 Jordan 标准形

## 1. 特征值是算子不改变方向的倍率

若 $Ax=\lambda x$ 且 $x\ne0$，则 $\lambda$ 是特征值，$x$ 是特征向量。特征多项式

$$
p_A(t)=\det(tI-A)
$$

记录特征值及其代数重数；特征空间 $\ker(A-\lambda I)$ 的维数是几何重数。总有

$$
1\le \text{几何重数}\le \text{代数重数}.
$$

矩阵可对角化，当且仅当所有特征空间的维数之和为 $n$。

## 2. Cayley–Hamilton 与极小多项式

Cayley–Hamilton 定理：

$$
p_A(A)=0.
$$

极小多项式 $m_A(t)$ 是使 $m_A(A)=0$ 的首一多项式中次数最小者，并且

$$
m_A\mid p_A.
$$

$A$ 可对角化，当且仅当 $m_A$ 在所在数域上分裂且没有重根。与特征多项式相比，极小多项式更直接记录 Jordan 块的最大尺寸。

## 3. 广义特征向量与 Jordan 链

不可对角化时，需要满足

$$
(A-\lambda I)^kx=0
$$

的广义特征向量。若向量组 $v_1,\dots,v_k$ 满足

$$
(A-\lambda I)v_1=0,qquad
(A-\lambda I)v_{j+1}=v_j,
$$

它构成一条 Jordan 链。在这组基下，$A$ 的限制表现为 Jordan 块

$$
J_k(\lambda)=
\begin{pmatrix}
\lambda&1&&\\
&\lambda&\ddots&\\
&&\ddots&1\\
&&&\lambda
\end{pmatrix}.
$$

每个复方阵都相似于若干 Jordan 块的直和。Jordan 形在理论上清晰，但在数值上对扰动敏感，因此计算中通常更偏爱 Schur 分解。

## 4. Jordan 形能立刻解决什么

写 $J=\lambda I+N$，其中 $N$ 幂零，则

$$
J^m=\sum_{j=0}^{k-1}\binom{m}{j}\lambda^{m-j}N^j.
$$

因此矩阵幂不仅由 $|\lambda|^m$ 控制，还可能带有多项式因子 $m^j$。同理，解析函数满足

$$
f(J_k(\lambda))
=\sum_{j=0}^{k-1}\frac{f^{(j)}(\lambda)}{j!}N^j.
$$

这说明不可对角化结构为何会让矩阵函数出现导数项。

## 5. Jordan–Chevalley 分解

在适当数域上，矩阵可唯一写成

$$
A=S+N,qquad SN=NS,
$$

其中 $S$ 半单（可对角化），$N$ 幂零。它把“伸缩/旋转的谱部分”与“剪切的幂零部分”分开。

## 6. Gershgorin 圆盘

对 $A=(a_{ij})$，定义第 $i$ 个行圆盘

$$
D_i=\left\{z\in\mathbb C:
|z-a_{ii}|\le\sum_{j\ne i}|a_{ij}|\right\}.
$$

Gershgorin 定理断言

$$
\sigma(A)\subseteq\bigcup_{i=1}^nD_i.
$$

若若干圆盘组成的连通分支与其余圆盘分离，且该分支包含 $k$ 个圆盘，则其中恰有 $k$ 个特征值（计重数）。它给出快速谱定位，也能用于证明严格对角占优矩阵非奇异：若所有圆盘都不含 $0$，则 $0$ 不是特征值。

## 7. 一个选择顺序

面对谱问题时可以依次问：

1. 矩阵是否 Hermite/正规？若是，直接用酉对角化。
2. 是否只要稳定计算特征值？优先 Schur 分解。
3. 是否要研究幂、极小多项式或精确结构？使用 Jordan 理论。
4. 是否只需粗略定位？先画 Gershgorin 圆盘。

## 8. 自检

- [ ] 能区分代数重数与几何重数。
- [ ] 能用极小多项式判断可对角化。
- [ ] 能从 Jordan 链写出 Jordan 块。
- [ ] 能用 Gershgorin 圆盘证明严格对角占优矩阵非奇异。

下一章：[内积空间与 QR 分解](07-内积空间与QR分解.md)。

