---
title: "08 对称特征值算法与奇异值分解"
course: "数值算法与案例分析Ⅰ"
---

# 08 对称特征值算法与奇异值分解

## 1. Hermite 结构带来额外稳定性

若 $A=A^*$，则特征值实、特征向量可正交化，并且有 Weyl 界

$$
\max_i|\lambda_i(A+E)-\lambda_i(A)|\le\|E\|_2.
$$

全部特征值的整体误差满足 Hoffman-Wielandt 界

$$
\sum_i|\lambda_i(A+E)-\lambda_i(A)|^2\le\|E\|_F^2.
$$

这比一般非正规矩阵的特征值问题温和得多。

## 2. 对称 QR 的两阶段框架

第一阶段用 Householder 相似变换把 $A$ 化为实对称三对角矩阵 $T$。第二阶段在 $T$ 上做隐式位移 QR。三对角结构让每次迭代只需 $O(n)$，而 Wilkinson 位移通常带来很快的局部收敛。

完整特征向量需要累积两阶段的正交变换；只求特征值则可节省大量存储和更新。

## 3. Jacobi 旋转法

Jacobi 法每次选择一个非零非对角元 $a_{ij}$，构造平面旋转使对应 $2\times2$ 主子块对角化。令

$$
\tau=\frac{a_{jj}-a_{ii}}{2a_{ij}},
$$

稳定地选择

$$
t=\frac{\operatorname{sign}(\tau)}{|\tau|+\sqrt{1+\tau^2}},
\quad c=(1+t^2)^{-1/2},\quad s=ct.
$$

一次旋转使非对角 Frobenius 能量至少减少 $2a_{ij}^2$。Jacobi 法适合追求高质量正交特征向量或并行计算，但通常比三对角 QR 慢。

## 4. 分治法与割线方程

把三对角矩阵拆成两个小三对角块，可写为

$$
T=\begin{pmatrix}T_1&0\\0&T_2\end{pmatrix}+\rho zz^T.
$$

对子块分别对角化后，核心变成对角矩阵加秩一修正 $D+\rho zz^T$。其新特征值满足割线方程

$$
1-\rho\sum_i\frac{z_i^2}{\lambda-d_i}=0.
$$

根与 $d_i$ 交错。数值实现必须处理重根、小 $z_i$ 和消去（deflation）。

## 5. SVD 的双对角化

直接形成 $A^*A$ 会平方条件数。Golub-Kahan 路线先用左右 Householder 变换将

$$
A=UBV^*
$$

化为上双对角矩阵 $B$，再对 $B$ 做隐式 QR 型迭代求奇异值。若 $m\gg n$，可先做 QR，把问题缩小到方阵 $R$。

奇异值也可看成块 Hermite 矩阵

$$
\begin{pmatrix}0&A\\A^*&0\end{pmatrix}
$$

的正特征值，但实际稠密算法会利用双对角结构避免尺寸翻倍。

## 6. 条件数与小奇异值

若 $A$ 满列秩，

$$
\kappa_2(A)=\frac{\sigma_1}{\sigma_n}.
$$

最小奇异值是到秩亏矩阵的 2-范数距离。计算接近零的奇异值时，相对精度比绝对精度更难保证；不能仅凭一个固定阈值判断数值秩，应结合矩阵尺度和应用容忍度。

## 7. 特征向量扰动与谱间隔

对简单特征值 $\lambda_i$，特征向量的敏感性由与其余谱的间隔

$$
\operatorname{gap}_i=\min_{j\ne i}|\lambda_i-\lambda_j|
$$

控制。若 $A$ 受到扰动 $E$，Davis-Kahan 型估计给出

$$
\sin\angle(\hat x_i,x_i)
\lesssim \frac{\|E\|_2}{\operatorname{gap}_i}.
$$

特征值误差只受 $\|E\|_2$ 控制，特征向量却会因小 gap 变得敏感。重特征值处单个特征向量没有唯一意义，应比较整个不变子空间。

若 $\|x\|=1$、$\theta=x^*Ax$，则残差 $r=Ax-\theta x$ 满足

$$
\min_i|\theta-\lambda_i|\le\|r\|_2.
$$

当 $x$ 已接近某个简单特征向量时，Rayleigh 商的特征值误差对角度通常是二阶，而向量误差是一阶。

## 8. 对称三对角问题的算法选择

约化为三对角矩阵后，可根据输出需求选择：

- 隐式 QR：可靠、易于解释，适合全谱；
- divide-and-conquer：把问题分解后合并，适合大量特征向量与并行；
- bisection + inverse iteration：利用 Sturm 序列定位指定区间特征值；
- MRRR：构造相对稳健表示，能高效计算选定特征对。

没有一个算法在所有输出规模、聚簇程度和硬件上都最优。成熟库会根据是否需要特征向量、需要多少个以及矩阵规模选择路径。

## 9. Hermite 广义特征值问题

若

$$
Ax=\lambda Bx,
\qquad A=A^*,\quad B=B^*\succ0,
$$

先做 $B=LL^*$，再化为

$$
C=L^{-1}AL^{-*},\qquad Cz=\lambda z,
\qquad x=L^{-*}z.
$$

$C$ 仍为 Hermite 矩阵，因此可以使用对称特征值算法。变换应通过三角求解实施，不要显式形成 $L^{-1}$。

## 10. 完整、经济与截断 SVD

对 $A\in\mathbb C^{m\times n}$、$m\ge n$，经济 SVD 为

$$
A=U_n\Sigma V^*,
\qquad U_n\in\mathbb C^{m\times n}.
$$

完整 SVD 还补齐 $U$ 的正交基。若只需前 $k$ 个方向，则截断 SVD

$$
A_k=U_k\Sigma_kV_k^*
$$

满足 Eckart-Young-Mirsky 定理：

$$
\min_{\operatorname{rank}(B)\le k}\|A-B\|_2=\sigma_{k+1},
$$

$$
\min_{\operatorname{rank}(B)\le k}\|A-B\|_F
=\left(\sum_{j>k}\sigma_j^2\right)^{1/2}.
$$

这使 SVD 同时成为压缩、降噪与数值秩判定的基础。

## 11. SVD 的不同数值路线

- Golub-Reinsch：双对角化后做隐式 QR，是通用稠密路线。
- one-sided Jacobi：反复正交化列，常能得到高相对精度奇异值与优质奇异向量。
- divide-and-conquer：适合计算大量奇异向量。
- 大规模稀疏矩阵：使用 Golub-Kahan/Lanczos 双对角化，只访问 $Av$ 与 $A^*u$。

形成 $A^*A$ 也许能给出大奇异值的粗略结果，但会损失小奇异值的相对精度，并平方条件数。

## 12. SVD 的扰动解释

奇异值满足稳定的绝对扰动界

$$
|\sigma_i(A+E)-\sigma_i(A)|\le\|E\|_2.
$$

奇异向量的敏感性仍由相邻奇异值的间隔控制。接近零的奇异值是否应视为零，必须结合噪声水平、矩阵尺度和应用容忍度；机器精度只是数值阈值的一部分。

## 13. 自检

- [ ] 能说明一般特征值与 Hermite 特征值的扰动差别。
- [ ] 能解释对称 QR 的“两阶段”结构。
- [ ] 知道 Jacobi 公式为什么采用稳定根。
- [ ] 能从秩一更新推导割线方程的来源。
- [ ] 知道 SVD 为什么不应直接通过 $A^*A$ 计算。
- [ ] 能区分特征值误差与特征向量误差的控制量。
- [ ] 会用截断 SVD 的最优低秩性质解释 PCA 或压缩。

下一章：[矩阵方程与矩阵函数](09-矩阵方程与矩阵函数.md)。
