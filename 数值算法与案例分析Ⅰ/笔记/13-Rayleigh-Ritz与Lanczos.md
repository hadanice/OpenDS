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

标量形式为

$$
w=Av_j-\beta_{j-1}v_{j-1},\qquad
\alpha_j=v_j^*w,
$$

$$
w\leftarrow w-\alpha_jv_j,\qquad
\beta_j=\|w\|_2,\qquad v_{j+1}=w/\beta_j.
$$

对称性使 $v_i^*Av_j=0$ 当 $|i-j|>1$，因此 Arnoldi 的长正交化在精确算术中缩短为三项递推。

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

shift-and-invert 最有效但每步需解线性系统；谱折叠 $(A-\sigma I)^2$ 不需求解，却会平方间隔并可能让条件恶化。FEAST 用数值围道积分把区间内特征向量近似投影出来，主要成本是一组可并行的复位移线性系统。

Jacobi-Davidson 对近似对 $(\theta,u)$ 求校正 $s\perp u$：

$$
(I-uu^*)(A-\theta I)(I-uu^*)s=-r,
\qquad r=Au-\theta u.
$$

该方程通常只需近似求解，再把 $s$ 加入试探空间。

## 13.5 Golub–Kahan 双对角化

对长方形矩阵 $A$，Golub–Kahan 过程交替使用 $A$ 与 $A^*$，构造

$$
AV_m=U_{m+1}\bar B_m,
\qquad A^*U_m=V_mB_m^*+\text{边界项},
$$

其中 $B_m$ 为双对角矩阵。它是大规模奇异值算法和 LSQR 的核心，避免显式形成条件数平方的正规方程 $A^*A$。

递推可写成

$$
\beta_ku_k=Av_k-\alpha_{k-1}u_{k-1},
\qquad
\alpha_kv_{k+1}=A^*u_k-\beta_kv_k.
$$

LSQR 在小型双对角最小二乘问题上递推，数学上与对正规方程使用 CG 有联系，但数值上从不形成 $A^*A$，因此更适合大型稀疏最小二乘。

## 13.6 矩阵函数与降维

若只需要 $f(A)b$ 而非整个 $f(A)$，可用 Lanczos 近似

$$
f(A)b\approx \|b\|_2V_mf(T_m)e_1.
$$

类似地，双线性型 $v^*f(A)v$ 可由小型三对角矩阵估计。这使谱算法与矩阵指数、迹估计和科学计算中的不确定性量化发生联系。

## 13.7 PCA 的谱视角

中心化数据矩阵 $X$ 的主成分是其右奇异向量。若只要前几个主成分，可直接对 $X$ 做 Golub–Kahan 或随机化低秩近似，无需形成协方差矩阵 $X^TX$。这既节省计算，也避免进一步放大条件数。

## 13.8 Ritz 对的误差与选择

对 Hermite $A$，若 Ritz 对 $(\theta,u)$ 归一化，必有某个特征值满足

$$
\min_i|\lambda_i-\theta|\le\|Au-\theta u\|_2.
$$

若目标特征值与其余谱的距离为 $\delta$，则向量夹角近似受 $\|r\|_2/\delta$ 控制。由此可见，选择“最接近目标位移的 Ritz 值”还不够，必须同时检查残差和谱间隔。

对极端特征值，Krylov 多项式在谱区间端点的逼近能力最强，Lanczos 往往先收敛两端、后收敛内部。这与 Chebyshev 多项式在区间端点外快速增长的性质一致。

## 13.9 重启动与锁定

基长度不能无限增长。常见策略有：

- 显式重启：保留若干 Ritz 向量重新开始，简单但可能丢失信息；
- 隐式重启 Lanczos：用一串隐式 QR 位移过滤不需要的 Ritz 方向；
- thick restart：一次保留多个近似不变方向；
- 锁定/亏损：已收敛方向不再参与活动迭代。

重启的本质是保留有用谱信息、压缩无用方向。保留维数太小会停滞，太大则失去控制成本的意义。

## 13.10 PINVIT 与 LOBPCG

对 $A=A^*$，预条件反迭代用

$$
x_{k+1}=x_k-M^{-1}(Ax_k-\theta_kx_k)
$$

构造校正方向，再在扩大的子空间中做 Rayleigh-Ritz。局部最优块预条件共轭梯度法（LOBPCG）同时使用当前块 $X_k$、预条件残差块 $W_k$ 和上一轮方向块 $P_k$，在

$$
\operatorname{span}\{X_k,W_k,P_k\}
$$

中选局部最优 Ritz 向量。它适合一次求若干个最小特征对，但必须仔细维护块之间的正交性。

## 13.11 Krylov 矩阵函数的误差视角

Arnoldi 情形近似为

$$
f(A)b\approx \|b\|_2V_mf(H_m)e_1.
$$

若 $f$ 是次数小于 $m$ 的多项式，该式精确；一般解析函数则由多项式或有理逼近误差控制。矩阵指数、线性系统（$f(z)=1/z$）和时间演化都可放在这一框架中。

若要计算 $v^*f(A)v$，Hermite 情形可用 Lanczos 三对角矩阵得到 Gauss 型求积；若需要双线性型 $u^*f(A)v$，还可由极化恒等式转化为若干二次型。

## 13.12 PCA 与几何最小二乘

给定样本列 $x_1,\ldots,x_m$，先计算均值

$$
\bar x=\frac1m\sum_{i=1}^m x_i
$$

并形成中心化矩阵

$$
C=[x_1-\bar x,\ldots,x_m-\bar x].
$$

寻找最佳 $k$ 维仿射子空间等价于

$$
\min_{Q^*Q=I}\|(I-QQ^*)C\|_F^2.
$$

解由 $C$ 的前 $k$ 个左奇异向量给出，最小误差为 $\sum_{j>k}\sigma_j(C)^2$。这一定理同时解释了 PCA、总最小二乘和最佳低秩逼近。

## 自检

1. Ritz 残差为何与试探子空间正交？
2. Lanczos 相比 Arnoldi 为什么能使用三项递推？
3. 为什么大规模 SVD 不宜先形成 $A^*A$？
4. 隐式重启保留了什么、过滤了什么？
5. LOBPCG 每轮的三个块分别承担什么作用？
