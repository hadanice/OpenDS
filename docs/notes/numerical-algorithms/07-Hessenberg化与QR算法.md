---
title: "07 Hessenberg 化、位移 QR 与 Francis 迭代"
course: "数值算法与案例分析Ⅰ"
---

# 07 Hessenberg 化、位移 QR 与 Francis 迭代

## 1. QR 迭代在做什么

无位移 QR 迭代为

$$
A_k=Q_kR_k,qquad A_{k+1}=R_kQ_k.
$$

因为

$$
A_{k+1}=Q_k^*A_kQ_k,
$$

每一步都是酉相似变换，特征值不变。累积的 $Q$ 同时执行一种子空间迭代；在合适条件下，$A_k$ 趋向上三角 Schur 形。

## 2. 先约化为上 Hessenberg 形

若每步都对稠密 $A_k$ 做 QR，成本为 $O(n^3)$，总成本过高。先用 Householder 相似变换得到

$$
H=Q^*AQ,
$$

其中 $H$ 只有第一条次对角线以下为零。一次约化成本 $O(n^3)$；Hessenberg 矩阵每步 QR 只需 $O(n^2)$，且结构在迭代中保持。

对 Hermite 矩阵，Hessenberg 形进一步退化为三对角矩阵。

## 3. 位移加速收敛

位移 QR 为

$$
H_k-\mu_kI=Q_kR_k,qquad
H_{k+1}=R_kQ_k+\mu_kI.
$$

常见选择：

- Rayleigh 位移：$\mu_k=(H_k)_{nn}$。
- Wilkinson 位移：取右下 $2\times2$ 子块中更接近 $(H_k)_{nn}$ 的特征值。

位移越接近正在收敛的特征值，次对角元素通常衰减越快。

## 4. 亏损与分块

当

$$
|h_{i+1,i}|\le c u(|h_{ii}|+|h_{i+1,i+1}|)
$$

时，可把 $h_{i+1,i}$ 置零，将问题分成两个较小块。好的亏损判据应考虑局部尺度，而不是只用固定绝对阈值。

实矩阵的实 Schur 形允许 $2\times2$ 对角块，以表示共轭复特征值对。

## 5. 隐式 Q 定理与 Francis 双位移

对实 Hessenberg 矩阵，直接使用一对复位移会引入复运算。Francis 双位移使用右下 $2\times2$ 子块的迹 $s$ 与行列式 $t$，隐式作用多项式

$$
p(H)=H^2-sH+tI.
$$

只需用 $p(H)e_1$ 的前三个分量构造第一个 Householder 反射。该反射在 Hessenberg 带外制造一个小“鼓包”，随后用一系列局部反射把鼓包向右下追赶并移出矩阵。

隐式 Q 定理保证：只要第一列和 Hessenberg 结构确定，这串正交相似变换就等价于显式双位移 QR，但无需形成 $p(H)$ 或完整 QR 分解。

## 6. 从 Schur 形恢复特征向量

若

$$
A=QTQ^*,
$$

先在上三角/准上三角 $T$ 上通过回代求特征向量 $y$，再令 $x=Qy$。接近重根时，回代和特征向量本身都可能病态，需要缩放以避免溢出。

## 7. 扰动视角

若 $A=X\Lambda X^{-1}$ 可对角化，Bauer-Fike 定理给出

$$
\min_{\lambda\in\sigma(A)}|\tilde\lambda-\lambda|
\le\kappa_2(X)\|E\|_2
$$

对 $A+E$ 的任一特征值 $\tilde\lambda$ 成立。非正规矩阵即使特征值算法后向稳定，前向特征值误差也可能因 $\kappa(X)$ 大而显著。

## 8. 自检

- [ ] 能解释 Hessenberg 预处理如何把每步成本降为 $O(n^2)$。
- [ ] 能写出位移 QR 的相似关系。
- [ ] 能说明实 Schur 形为何允许 $2\times2$ 块。
- [ ] 能用“制造鼓包—追赶鼓包”描述 Francis 双位移。

下一章：[对称特征值与 SVD 算法](08-对称特征值与SVD算法.md)。
