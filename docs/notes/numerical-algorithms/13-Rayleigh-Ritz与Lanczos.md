# 13. Rayleigh–Ritz、Lanczos 与大规模谱计算

大规模特征值问题通常只需要少量极端或内部特征值。与其对整个矩阵做稠密分解，不如在一个低维子空间中寻找近似特征向量。

## 13.1 Rayleigh–Ritz 投影

设 $V\in\mathbb C^{n\times m}$ 列正交，试探子空间为 $\mathcal V=\operatorname{range}(V)$。把 $A$ 投影为

$$
H=V^*AV.
$$

若

$$
Hy=\theta y,
$$

则 $(\theta,u)$、$u=Vy$ 称为 Ritz 对。它满足 Galerkin 条件

$$
r=Au-\theta u\perp\mathcal V.
$$

Ritz 值是大矩阵特征值的近似，残差范数则是更直接的可信度指标。

## 13.2 Lanczos 三项递推

当 $A=A^*$ 时，Arnoldi 的 Hessenberg 矩阵退化为实对称三对角矩阵。由此得到

$$
AV_m=V_mT_m+\beta_mv_{m+1}e_m^T,
$$

其中

$$
T_m=
\begin{bmatrix}
\alpha_1&\beta_1&&\\
\beta_1&\alpha_2&\ddots&\\
&\ddots&\ddots&\beta_{m-1}\\
&&\beta_{m-1}&\alpha_m
\end{bmatrix}.
$$

三项递推只需保存少量工作向量，因此非常适合大规模 Hermitian 问题。但若要恢复多个 Ritz 向量，仍需保存或重建基。

## 13.3 有限精度与“幽灵”特征值

精确算术中 Lanczos 向量正交；有限精度下，已收敛方向会重新进入子空间，可能出现重复的 Ritz 值。常见应对方式是：

- 完全重正交化：可靠但成本高；
- 选择性重正交化：只针对已收敛方向；
- 隐式重启：保留目标谱信息，同时控制子空间大小。

判断是否收敛应查看 Ritz 残差，而不是只观察 Ritz 值是否变化。

## 13.4 内部特征值与校正方程

极端特征值通常容易由 Krylov 过程提取，内部特征值则需要谱变换或过滤：

- shift-and-invert：对 $(A-\sigma I)^{-1}$ 求极端特征值；
- FEAST：用围道积分近似目标区间的谱投影；
- Davidson：以近似逆对残差做校正；
- Jacobi–Davidson：在当前向量的正交补中求解校正方程。

这些方法的共同点是把“想要哪一段谱”编码进子空间构造过程。

## 13.5 Golub–Kahan 双对角化

对长方形矩阵 $A$，Golub–Kahan 过程交替使用 $A$ 与 $A^*$，构造

$$
AV_m=U_{m+1}\bar B_m,
\qquad A^*U_m=V_mB_m^*+	ext{边界项},
$$

其中 $B_m$ 为双对角矩阵。它是大规模奇异值算法和 LSQR 的核心，避免显式形成条件数平方的正规方程 $A^*A$。

## 13.6 矩阵函数与降维

若只需要 $f(A)b$ 而非整个 $f(A)$，可用 Lanczos 近似

$$
f(A)b\approx \|b\|_2V_mf(T_m)e_1.
$$

类似地，双线性型 $v^*f(A)v$ 可由小型三对角矩阵估计。这使谱算法与矩阵指数、迹估计和科学计算中的不确定性量化发生联系。

## 13.7 PCA 的谱视角

中心化数据矩阵 $X$ 的主成分是其右奇异向量。若只要前几个主成分，可直接对 $X$ 做 Golub–Kahan 或随机化低秩近似，无需形成协方差矩阵 $X^TX$。这既节省计算，也避免进一步放大条件数。

## 自检

1. Ritz 残差为何与试探子空间正交？
2. Lanczos 相比 Arnoldi 为什么能使用三项递推？
3. 为什么大规模 SVD 不宜先形成 $A^*A$？
