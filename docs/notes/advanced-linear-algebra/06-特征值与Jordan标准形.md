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
(A-\lambda I)v_1=0,\qquad
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
A=S+N,\qquad SN=NS,
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

若干圆盘组成的连通分支若与其余圆盘分离，且该分支包含 $k$ 个圆盘，则其中恰有 $k$ 个特征值（计重数）。它给出快速谱定位，也能用于证明严格对角占优矩阵非奇异：若所有圆盘都不含 $0$，则 $0$ 不是特征值。

## 7. 用核空间维数恢复 Jordan 块

固定特征值 $\lambda$，令 $N=A-\lambda I$ 在广义特征子空间上作用，并记

$$
d_k=\dim\ker N^k,\qquad d_0=0.
$$

一个长度为 $s$ 的 Jordan 链对 $d_k$ 的贡献是 $\min(k,s)$，所以

$$
d_k-d_{k-1}
=\text{大小至少为 }k\text{ 的 Jordan 块个数}.
$$

进而，大小恰为 $k$ 的块数为

$$
(d_k-d_{k-1})-(d_{k+1}-d_k)
=2d_k-d_{k-1}-d_{k+1}.
$$

例如若

$$
d_1=2,\quad d_2=4,\quad d_3=5,\quad d_4=5,
$$

则至少为 $1,2,3$ 阶的块数依次为 $2,2,1$，所以 Jordan 块大小为 $3$ 和 $2$。这套方法比“猜 Jordan 形再验证”可靠得多。

## 8. Cayley–Hamilton 的系数比较证明

从伴随矩阵恒等式出发：

$$
(tI-A)\operatorname{adj}(tI-A)=p_A(t)I.
$$

把 $\operatorname{adj}(tI-A)$ 展开成以 $t$ 为变量的矩阵多项式，再比较各次幂系数，会得到一串关于这些系数矩阵与 $A$ 的递推关系。将关系依次乘上 $A$ 的幂并相加，所有中间项望远镜式消去，最终留下

$$
p_A(A)=0.
$$

这里不能把“行列式等式中的 $t$ 直接替换为矩阵 $A$”当作证明；真正合法的是先把恒等式视为标量变量 $t$ 的多项式恒等式，再比较系数。

## 9. Gershgorin 定理的一行核心证明

若 $Ax=\lambda x$，取满足 $|x_i|=\max_j|x_j|$ 的指标 $i$。第 $i$ 行给出

$$
(\lambda-a_{ii})x_i=\sum_{j\ne i}a_{ij}x_j.
$$

两边取绝对值并除以 $|x_i|>0$：

$$
|\lambda-a_{ii}|
\le\sum_{j\ne i}|a_{ij}|\frac{|x_j|}{|x_i|}
\le\sum_{j\ne i}|a_{ij}|.
$$

因此每个特征值至少落在一个行圆盘中。圆盘分支的精确计数结论则可通过连续变形 $A(t)=D+t(A-D)$ 得到：圆盘逐渐张开时，分离分支中的特征值个数不可能跳变。

## 10. 一个选择顺序

面对谱问题时可以依次问：

1. 矩阵是否 Hermite/正规？若是，直接用酉对角化。
2. 是否只要稳定计算特征值？优先 Schur 分解。
3. 是否要研究幂、极小多项式或精确结构？使用 Jordan 理论。
4. 是否只需粗略定位？先画 Gershgorin 圆盘。

## 11. 自检

- [ ] 能区分代数重数与几何重数。
- [ ] 能用极小多项式判断可对角化。
- [ ] 能从 Jordan 链写出 Jordan 块。
- [ ] 能用 Gershgorin 圆盘证明严格对角占优矩阵非奇异。
- [ ] 能由 $\dim\ker(A-\lambda I)^k$ 的增长恢复 Jordan 块大小。
- [ ] 能指出 Cayley–Hamilton 证明中不能直接“代入矩阵”的原因。

下一章：[内积空间与 QR 分解](07-内积空间与QR分解.md)。
