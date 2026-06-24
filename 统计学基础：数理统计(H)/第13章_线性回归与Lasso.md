# 第 13 章：线性回归与 Lasso

> 本文对应 `课件/lecture13.pdf`（标题为 Generalized Linear Model，主要内容是线性回归与 Lasso）。
>
> 本章从传统线性模型进入现代高维统计：先用最小二乘建立回归推断，再用正则化和 Lasso 处理变量选择与高维预测。

---

## 0. 本章定位

前面章节主要比较均值、方差、比例。  
回归分析把问题改写为：

$$
Y \text{ 如何随多个解释变量 } X_1,\dots,X_p \text{ 改变？}
$$

知识链条：

```
线性模型
  -> 设计矩阵 X
  -> 最小二乘估计
  -> 投影与残差
  -> OLS 分布与检验
  -> 模型选择 / ANOVA / R²
  -> 正则化
  -> Lasso 稀疏估计
  -> KKT / 路径算法 / 风险界
```

这一讲的 PPT 信息量较大，可以分成两条并行主线：

1. **经典低维回归**：$p<n$，重点是最小二乘、投影几何、精确分布、置信区间、$t/F$ 检验、ANOVA、$R^2$。
2. **高维稀疏回归**：$p$ 可以很大，甚至 $p>n$，重点是正则化、Lasso、KKT、解路径、预测误差界、支持恢复。

两条主线的共同对象都是

$$
y=X\beta+\varepsilon
$$

区别在于：经典回归假设 $X^\top X$ 可逆，追求可解释的精确推断；高维回归允许变量很多，追求稳定预测和变量筛选。

### 0.1 PPT 结构导航

| PPT 板块 | 本指导对应位置 | 要解决的问题 |
|----------|----------------|--------------|
| Advertising data | 1.0、1.1 | 线性回归为什么自然出现？ |
| Linear model / design matrix | 1.2-1.4 | 如何把回归写成线性代数形式？ |
| Least squares | 2 | OLS 怎么推出来？几何意义是什么？ |
| Orthogonality / Gauss-Markov | 2.4、3.4 | 为什么残差正交？OLS 为什么最优？ |
| Statistical properties | 3-4 | $\hat\beta$、RSS、$t/F$ 统计量如何分布？ |
| Variable selection / ANOVA / $R^2$ | 4 | 如何比较 full/reduced model？ |
| Risk of least squares | 5 | 为什么高维时 OLS 有风险？ |
| Regularization | 6 | $\ell_0,\ell_1,\ell_2$ 惩罚分别做什么？ |
| Lasso KKT / uniqueness / path | 7-8 | Lasso 为什么稀疏？路径如何变化？ |
| Slow/fast rates | 9 | Lasso 预测误差为什么是这些量级？ |
| Support recovery | 9.6 | Lasso 何时能选对变量？ |
| Non-convex penalties | 9.8 | 为什么有人要改进 Lasso 的偏差？ |

---

## 1. 线性回归模型

### 1.0 从 Advertising Data 理解回归

PPT 用 Advertising data 开场：

- 样本量：$n=200$；
- 响应变量：Sales，记为 $y_i$；
- 三个解释变量：TV、Radio、Newspaper 广告预算，记为 $x_{i1},x_{i2},x_{i3}$；
- 维度：$p=3$。

我们关心的问题不是简单比较两组均值，而是：

```
在 TV、Radio、Newspaper 投放不同的情况下，Sales 的平均水平如何变化？
```

如果图上每个广告预算和销售额之间近似呈线性趋势，就可以尝试用线性模型描述：

$$
y_i=\beta_0+\beta_1x_{i1}+\beta_2x_{i2}+\beta_3x_{i3}+\varepsilon_i
$$

这里每个系数都有直观解释：

- $\beta_0$：所有广告预算为 0 时的基准销售额；
- $\beta_1$：TV 预算增加 1 个单位，其他预算固定时，平均销售额的线性变化；
- $\beta_2$：Radio 的边际线性影响；
- $\beta_3$：Newspaper 的边际线性影响。

> “其他变量固定”是多元回归系数解释的关键，否则会把变量之间的相关性误当成某个单独变量的作用。

### 1.1 标量形式

对第 $i$ 个观测：

$$
\boxed{
y_i=\beta_0+\beta_1x_{i1}+\cdots+\beta_px_{ip}+\varepsilon_i
}
$$

其中：

- $y_i$：响应变量；
- $x_{ij}$：第 $j$ 个解释变量；
- $\beta_j$：回归系数；
- $\varepsilon_i$：噪声。

通常假设：

$$
E(\varepsilon_i)=0,\quad Var(\varepsilon_i)=\sigma^2
$$

若进一步假设正态噪声：

$$
\varepsilon_i\sim N(0,\sigma^2)
$$

就可以做精确 $t/F$ 推断。

### 1.1.1 响应变量、协变量和噪声

课件中同时使用了几组术语：

| 角色 | 常见名称 |
|------|----------|
| $y_i$ | response、dependent variable、output |
| $x_i$ | covariate、independent variable、predictor、feature、input、regressor |
| $\varepsilon_i$ | noise、error、随机扰动 |

线性回归并不是说真实世界没有非线性，而是说在当前建模尺度下，我们用一个线性平均结构解释主要趋势，把剩余部分放进 $\varepsilon_i$。

### 1.1.2 噪声假设分层

不同结论需要不同强度的假设：

| 假设 | 可推出的典型结论 |
|------|------------------|
| $E(\varepsilon_i)=0$ | OLS 无偏 |
| 同方差、互不相关 | Gauss-Markov：OLS 是 BLUE |
| 正态噪声 | $\hat\beta$ 正态、RSS 卡方、$t/F$ 精确推断 |
| 独立同分布 | 便于似然、预测和渐近分析 |

所以不要把“最小二乘估计能算出来”和“$t$ 检验严格有效”混为一谈。前者主要是优化问题，后者需要概率模型。

### 1.2 矩阵形式

令

$$
y=(y_1,\dots,y_n)^\top
$$

设计矩阵：

$$
X=
\begin{pmatrix}
1&x_{11}&\cdots&x_{1p}\\
1&x_{21}&\cdots&x_{2p}\\
\vdots&\vdots&&\vdots\\
1&x_{n1}&\cdots&x_{np}
\end{pmatrix}
$$

参数：

$$
\beta=(\beta_0,\beta_1,\dots,\beta_p)^\top
$$

模型：

$$
\boxed{y=X\beta+\varepsilon}
$$

### 1.3 抽象线性模型的空间表述

PPT 给出更抽象的线性模型定义。设

$$
Y_1,\dots,Y_n\sim N(\mu,\sigma^2)
$$

线性模型就是对均值向量 $\mu$ 施加一个仿射子空间约束：

$$
\boxed{H_0:\mu-\mu_0\in\Omega_0}
$$

其中 $\Omega_0$ 是 $\mathbb R^n$ 中的线性子空间，维度为 $k$。

如果

$$
\Omega_0=\operatorname{span}\{x_1,\dots,x_k\}
$$

则可写成：

$$
\mu-\mu_0=X\beta,\quad \beta\in\mathbb R^k
$$

此时 $X$ 就是设计矩阵。

这套语言有两个好处：

1. **回归就是投影**：估计 $\mu$ 等于把 $y$ 投影到由 $X$ 张成的线性空间；
2. **模型检验就是比较子空间**：full model 与 reduced model 是两个嵌套子空间。

### 1.4 维度与截距项

若模型包含截距和 $p$ 个解释变量，则参数个数为 $p+1$。  
在 PPT 的符号里，有时 $p$ 表示变量数，有时公式里的自由度写成 $n-p-1$，原因正是截距消耗了 1 个自由度。

常见对应：

| 对象 | 维度 |
|------|------|
| 样本向量 $y$ | $n$ |
| 设计矩阵 $X$ | $n\times(p+1)$ |
| 参数 $\beta$ | $p+1$ |
| fitted space $\mathcal C(X)$ | 维度 $p+1$，若满列秩 |
| residual space | 维度 $n-p-1$ |

---

## 2. 最小二乘估计

### 2.1 目标函数

最小化残差平方和：

$$
\boxed{
\min_\beta \|y-X\beta\|_2^2
}
$$

若 $X^\top X$ 可逆，则解为：

$$
\boxed{
\hat\beta=(X^\top X)^{-1}X^\top y
}
$$

### 2.1.1 正规方程推导

展开目标函数：

$$
Q(\beta)=\|y-X\beta\|_2^2=(y-X\beta)^\top(y-X\beta)
$$

即

$$
Q(\beta)=y^\top y-2\beta^\top X^\top y+\beta^\top X^\top X\beta
$$

对 $\beta$ 求导：

$$
\frac{\partial Q}{\partial\beta}=-2X^\top y+2X^\top X\beta
$$

令导数为 0：

$$
\boxed{X^\top X\hat\beta=X^\top y}
$$

这称为正规方程。若 $X^\top X$ 可逆，就得到

$$
\hat\beta=(X^\top X)^{-1}X^\top y
$$

### 2.1.2 和最大似然的关系

若

$$
\varepsilon\sim N(0,\sigma^2I)
$$

则

$$
y\mid X\sim N(X\beta,\sigma^2I)
$$

对数似然中和 $\beta$ 有关的部分为：

$$
-\frac1{2\sigma^2}\|y-X\beta\|_2^2
$$

最大化似然等价于最小化残差平方和。因此在正态噪声下，OLS 也是 MLE。

### 2.2 拟合值与残差

拟合值：

$$
\boxed{\hat y=X\hat\beta}
$$

残差：

$$
\boxed{\hat\varepsilon=y-\hat y}
$$

残差平方和：

$$
\boxed{
RSS=\|\hat\varepsilon\|_2^2=\sum_{i=1}^n(y_i-\hat y_i)^2
}
$$

### 2.3 投影矩阵

帽子矩阵：

$$
\boxed{
H=X(X^\top X)^{-1}X^\top
}
$$

于是

$$
\hat y=Hy
$$

残差：

$$
\hat\varepsilon=(I-H)y
$$

关键几何性质：

$$
\boxed{X^\top\hat\varepsilon=0}
$$

即残差向量与 $X$ 的列空间正交。

### 2.4 投影几何：为什么残差正交？

拟合值 $\hat y=X\hat\beta$ 位于 $X$ 的列空间：

$$
\mathcal C(X)=\{Xb:b\in\mathbb R^{p+1}\}
$$

最小二乘是在这个空间中找离 $y$ 最近的点。欧氏空间中“最近点”的几何条件是：

$$
y-\hat y\perp \mathcal C(X)
$$

因为 $\mathcal C(X)$ 由 $X$ 的列向量张成，等价于

$$
X^\top(y-\hat y)=0
$$

这就是正规方程：

$$
X^\top y=X^\top X\hat\beta
$$

### 2.5 Hat matrix 的性质

$$
H=X(X^\top X)^{-1}X^\top
$$

它是投影矩阵，因此满足：

$$
H^\top=H,\quad H^2=H
$$

残差投影矩阵为：

$$
I-H
$$

也满足：

$$
(I-H)^\top=I-H,\quad (I-H)^2=I-H
$$

如果 $X$ 满列秩且有 $p+1$ 列：

$$
\operatorname{rank}(H)=p+1,\quad \operatorname{rank}(I-H)=n-p-1
$$

这解释了为什么 $RSS/\sigma^2$ 的自由度是 $n-p-1$。

---

## 3. OLS 的统计性质

### 3.1 正态噪声下的分布

若

$$
\varepsilon\sim N(0,\sigma^2I)
$$

则

$$
\boxed{
\hat\beta\sim N\left(\beta,\sigma^2(X^\top X)^{-1}\right)
}
$$

并且

$$
\boxed{
\frac{RSS}{\sigma^2}\sim\chi^2_{n-p-1}
}
$$

无偏方差估计：

$$
\boxed{
s^2=\frac{RSS}{n-p-1}
}
$$

### 3.2 单个系数的 $t$ 检验

记 $c_{jj}$ 为 $(X^\top X)^{-1}$ 的第 $j$ 个对角元素，则

$$
\boxed{
\frac{\hat\beta_j-\beta_j}{s\sqrt{c_{jj}}}\sim t_{n-p-1}
}
$$

因此 $\beta_j$ 的置信区间：

$$
\boxed{
\hat\beta_j\pm t_{\alpha/2,n-p-1}s\sqrt{c_{jj}}
}
$$

检验变量是否有用：

$$
H_0:\beta_j=0
$$

对应的 p-value 可用于变量筛选，但不能机械等同于因果结论。

### 3.2.1 $\hat\beta$ 与 RSS 独立

在正态线性模型中：

$$
\hat\beta=(X^\top X)^{-1}X^\top y
$$

是 $y$ 在线性空间 $\mathcal C(X)$ 上的投影坐标；而

$$
\hat\varepsilon=(I-H)y
$$

是 $y$ 在正交补空间上的投影。正态向量在正交子空间上的投影彼此独立，因此：

$$
\boxed{\hat\beta\ \perp\ RSS}
$$

这一步是 $t$ 统计量成立的关键：

$$
\frac{\hat\beta_j-\beta_j}{\sigma\sqrt{c_{jj}}}\sim N(0,1)
$$

而

$$
\frac{(n-p-1)s^2}{\sigma^2}=\frac{RSS}{\sigma^2}\sim\chi^2_{n-p-1}
$$

两者独立，合起来就是 $t$ 分布。

### 3.2.2 同时检验所有系数

PPT 中还给出整体二次型：

$$
\boxed{
\frac{(\hat\beta-\beta)^\top X^\top X(\hat\beta-\beta)/(p+1)}
{s^2}
\sim F_{p+1,n-p-1}
}
$$

它来自：

$$
\frac{(\hat\beta-\beta)^\top X^\top X(\hat\beta-\beta)}{\sigma^2}
\sim\chi^2_{p+1}
$$

与

$$
\frac{RSS}{\sigma^2}\sim\chi^2_{n-p-1}
$$

相互独立。

### 3.3 Gauss-Markov 定理

若噪声满足：

$$
E(\varepsilon_i)=0,\quad Var(\varepsilon_i)=\sigma^2,\quad Cov(\varepsilon_i,\varepsilon_j)=0
$$

则最小二乘估计是 BLUE：

```
Best Linear Unbiased Estimator
```

即在线性无偏估计量中方差最小。

### 3.4 Gauss-Markov 证明思路

PPT 的证明用矩阵半正定序来说明“OLS 方差最小”。

设某个线性估计量写成

$$
Ay
$$

要估计 $\beta$，无偏性要求：

$$
E(Ay)=AX\beta=\beta,\quad \forall\beta
$$

所以

$$
AX=I
$$

OLS 对应的矩阵是：

$$
A_0=(X^\top X)^{-1}X^\top
$$

任意其他线性无偏估计可写成：

$$
A=A_0+D
$$

且

$$
DX=0
$$

方差矩阵：

$$
Var(Ay)=\sigma^2AA^\top
$$

代入：

$$
AA^\top=(A_0+D)(A_0+D)^\top=A_0A_0^\top+DD^\top
$$

交叉项为 0，因为 $DX=0$。因此

$$
AA^\top\succeq A_0A_0^\top=(X^\top X)^{-1}
$$

这说明任意线性无偏估计的方差矩阵都不小于 OLS 的方差矩阵。

### 3.5 这一部分要形成的直觉

```
OLS = 投影
残差 = 正交补
正态 + 正交 = 独立
独立正态平方和 = χ²
正态 / sqrt(χ²/df) = t
两个χ²比 = F
```

这条链贯穿了第 10 章、第 12 章和本章的回归推断。

---

## 4. 预测、模型缩减与 ANOVA

### 4.1 均值响应置信区间

给定新输入向量 $x$，均值响应为 $\beta^\top x$，估计为 $\hat\beta^\top x$。

置信区间：

$$
\boxed{
\hat\beta^\top x
\pm
t_{\alpha/2,n-p-1}s
\sqrt{x^\top(X^\top X)^{-1}x}
}
$$

严格说，这里是**均值响应的置信区间**。  
若要预测一个新的随机观测值

$$
Y_{\text{new}}=x^\top\beta+\varepsilon_{\text{new}}
$$

则还要把新噪声方差 $\sigma^2$ 加进去，预测区间标准误通常为：

$$
s\sqrt{1+x^\top(X^\top X)^{-1}x}
$$

PPT 中称 prediction interval 时更接近“mean response interval”的形式，学习时要区分：

| 目标 | 标准误 |
|------|--------|
| 估计平均响应 $E(Y\mid x)$ | $s\sqrt{x^\top(X^\top X)^{-1}x}$ |
| 预测新观测 $Y_{\text{new}}$ | $s\sqrt{1+x^\top(X^\top X)^{-1}x}$ |

### 4.2 模型缩减检验

若想检验一组变量是否都无用：

$$
H_0:\beta_{i_1}=\cdots=\beta_{i_r}=0
$$

通常比较 full model 与 reduced model 的残差平方和。

课件中用投影空间语言表达：

$$
H_0:P(y)\in L(A^c)
$$

核心统计量是 F 比：

$$
\boxed{
F=
\frac{\text{reduced model 相比 full model 增加的解释平方和}/r}
{RSS_{\text{full}}/(n-p-1)}
}
$$

若 $F$ 大，说明删掉这些变量会显著恶化拟合，拒绝模型缩减。

### 4.2.1 full model 与 reduced model

设 full model 的拟合值为 $\hat y$，reduced model 的拟合值为 $\hat y_0$。

由于 reduced model 是 full model 的子模型：

$$
\mathcal C(X_0)\subset \mathcal C(X)
$$

因此可以分解：

$$
y-\hat y_0=(y-\hat y)+(\hat y-\hat y_0)
$$

并且两部分正交。于是平方和分解：

$$
\|y-\hat y_0\|^2=\|y-\hat y\|^2+\|\hat y-\hat y_0\|^2
$$

也就是：

$$
RSS_{\text{reduced}}=RSS_{\text{full}}+SS_{\text{extra}}
$$

其中

$$
SS_{\text{extra}}=\|\hat y-\hat y_0\|^2
$$

衡量被删掉变量额外解释的变异。

### 4.2.2 PPT 中的 F 统计量

若 full model 相比 reduced model 多了 $q$ 个参数，则：

$$
\boxed{
F=
\frac{(RSS_{\text{reduced}}-RSS_{\text{full}})/q}
{RSS_{\text{full}}/(n-p-1)}
\sim F_{q,n-p-1}
}
$$

PPT 写作：

$$
F=
\frac{\|\hat y-\hat y_0\|^2/(p+1-r)}
{\|y-\hat y\|^2/(n-p-1)}
$$

这只是用投影距离表达同一件事。

### 4.2.3 常见整体显著性检验

最常见的是：

$$
H_0:\beta_1=\cdots=\beta_p=0
$$

即除了截距以外所有变量都没有线性解释力。  
reduced model 只包含截距，拟合值是：

$$
\hat y_0=\bar y\mathbf 1
$$

若拒绝 $H_0$，说明至少有一个解释变量有线性关联。

### 4.2.4 Deviance / ANOVA 表

PPT 用 deviance table 或 ANOVA table 描述平方和分解。在线性回归里可理解为：

| 来源 | 平方和 | 自由度 | 均方 | F 比 |
|------|--------|--------|------|-----|
| 模型解释 | $TSS-RSS$ | $p$ | $(TSS-RSS)/p$ | $\frac{(TSS-RSS)/p}{RSS/(n-p-1)}$ |
| 残差 | $RSS$ | $n-p-1$ | $RSS/(n-p-1)$ | |
| 总变异 | $TSS$ | $n-1$ | | |

其中

$$
TSS=\sum_{i=1}^n(y_i-\bar y)^2
$$

ANOVA 表背后的几何事实仍然是：投影分量正交，所以平方和可以相加。

### 4.3 $R^2$ 与 adjusted $R^2$

$R^2$ 表示总变异中被模型解释的比例：

$$
\boxed{
R^2=1-\frac{RSS}{TSS}
}
$$

加入变量通常不会降低 $R^2$，所以 adjusted $R^2$ 会对变量数做惩罚，更适合比较复杂度不同的模型。

### 4.3.1 $R^2$ 的含义

如果不用任何解释变量，最好的预测是 $\bar y$，对应总变异：

$$
TSS=\|y-\bar y\mathbf 1\|^2
$$

使用模型后，残差变异是：

$$
RSS=\|y-\hat y\|^2
$$

所以

$$
\boxed{R^2=1-\frac{RSS}{TSS}}
$$

表示模型解释掉的总变异比例。

### 4.3.2 adjusted $R^2$

PPT 给出的修正思想是用自由度惩罚变量数量：

$$
\boxed{
R^2_{\text{adj}}
=1-\frac{RSS/(n-k)}{TSS/(n-1)}
}
$$

其中 $k$ 是模型参数个数。若包含截距和 $p$ 个变量，通常 $k=p+1$。

加入变量时：

- $RSS$ 一定不增；
- 但自由度 $n-k$ 减少；
- 如果新增变量带来的 $RSS$ 降幅不足，$R^2_{\text{adj}}$ 会下降。

因此 $R^2_{\text{adj}}$ 比 $R^2$ 更适合比较不同复杂度模型。

---

## 5. 为什么需要正则化？

当 $p$ 较大或变量高度相关时，最小二乘会出现问题：

- $X^\top X$ 不可逆；
- OLS 解不唯一；
- 预测方差大；
- 变量选择不稳定；
- $p>n$ 时传统 OLS 无法直接使用。

正则化的思想：

```
拟合数据
  + 控制模型复杂度
  -> 更稳定的预测 / 更稀疏的变量选择
```

### 5.1 最小二乘在高维下的风险

PPT 在进入 Lasso 前先讨论 Least Squares 的风险。

最小二乘问题：

$$
\min_{\beta\in\mathbb R^p}\|y-X\beta\|_2^2
$$

若

$$
\operatorname{rank}(X)=p
$$

则解唯一。

但当 $p>n$ 或列之间线性相关时：

$$
\operatorname{rank}(X)<p
$$

此时可能有无穷多个 $\beta$ 给出同样的训练误差。虽然 fitted value $X\hat\beta$ 可能仍然确定，但系数本身不稳定。

### 5.2 预测不稳定的原因

在训练样本上，两个解可能满足：

$$
X\hat\beta^{(1)}=X\hat\beta^{(2)}
$$

但对新样本 $x_0$：

$$
x_0^\top\hat\beta^{(1)}\ne x_0^\top\hat\beta^{(2)}
$$

也就是说，训练集上等价的模型，在样本外可能预测不同。

这正是高维或共线性条件下需要正则化的原因：我们不仅要拟合训练数据，还要选择一个稳定、简单、可泛化的解。

### 5.3 正则化的两种等价视角

约束形式：

$$
\min_{\beta\in C}\|y-X\beta\|_2^2
$$

惩罚形式：

$$
\min_\beta \|y-X\beta\|_2^2+P(\beta)
$$

直观区别：

| 形式 | 含义 |
|------|------|
| 约束形式 | 只在“允许的复杂度集合”中找最优拟合 |
| 惩罚形式 | 拟合误差和复杂度惩罚之间做 trade-off |

在凸问题中，很多约束形式和惩罚形式可以通过调节参数互相对应。

---

## 6. 三类正则化：Subset、Ridge、Lasso

### 6.1 约束形式

Best subset：

$$
\min_\beta \|y-X\beta\|_2^2\quad s.t.\quad \|\beta\|_0\le k
$$

Lasso：

$$
\min_\beta \|y-X\beta\|_2^2\quad s.t.\quad \|\beta\|_1\le t
$$

Ridge：

$$
\min_\beta \|y-X\beta\|_2^2\quad s.t.\quad \|\beta\|_2^2\le t
$$

### 6.2 惩罚形式

Best subset：

$$
\min_\beta \frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_0
$$

Lasso：

$$
\boxed{
\min_\beta \frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1
}
$$

Ridge：

$$
\min_\beta \frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_2^2
$$

### 6.3 三者区别

| 方法 | 惩罚 | 是否稀疏 | 特点 |
|------|------|----------|------|
| Best subset | $\ell_0$ | 是 | 直接选变量，但计算困难 |
| Lasso | $\ell_1$ | 是 | 凸优化，可变量选择 |
| Ridge | $\ell_2$ | 否 | 稳定收缩，但不会置零 |

### 6.4 三种范数的几何差异

$$
\|\beta\|_0=\sum_{j=1}^p1\{\beta_j\ne0\}
$$

统计的是非零系数个数，最直接表达“稀疏”，但优化是组合问题。

$$
\|\beta\|_1=\sum_{j=1}^p|\beta_j|
$$

是凸的，并且约束集合有尖角，最优解容易落在坐标轴上，因此产生稀疏。

$$
\|\beta\|_2=\left(\sum_{j=1}^p\beta_j^2\right)^{1/2}
$$

约束集合圆滑，主要产生连续收缩，很少把系数精确压成 0。

### 6.5 正交设计下的三类解

若 $X^\top X=I$，最小二乘系数为

$$
z=X^\top y
$$

则：

**Best subset**：

$$
\hat\beta_j=z_j1\{|z_j|>\sqrt{2\lambda}\}
$$

这是 hard-thresholding：小系数直接置零，大系数不收缩。

**Lasso**：

$$
\hat\beta_j=\operatorname{sign}(z_j)(|z_j|-\lambda)_+
$$

这是 soft-thresholding：小系数置零，大系数也向 0 收缩 $\lambda$。

**Ridge**：

$$
\hat\beta_j=\frac{z_j}{1+2\lambda}
$$

所有系数按比例缩小，不会精确置零。

### 6.6 Oracle estimator

假设真实非零集合为

$$
S=\operatorname{supp}(\beta_0),\quad s_0=|S|
$$

如果有“神谕”提前告诉我们 $S$，最理想的做法是在真实支持集上做最小二乘：

$$
\boxed{
\hat\beta_S^{oracle}=(X_S^\top X_S)^{-1}X_S^\top y,\quad
\hat\beta_{-S}^{oracle}=0
}
$$

它的样本内预测风险量级为：

$$
\frac1n\|X\hat\beta^{oracle}-X\beta_0\|_2^2
\asymp
\frac{\sigma^2s_0}{n}
$$

真实问题中 $S$ 不知道，Lasso 的目标之一就是在不知道 $S$ 的情况下尽量接近 oracle 的表现。

---

## 7. Lasso 的 KKT 条件

Lasso 解 $\hat\beta$ 满足：

$$
\boxed{
X^\top(y-X\hat\beta)=\lambda s
}
$$

其中 $s\in\partial\|\hat\beta\|_1$，逐坐标为：

$$
s_j=
\begin{cases}
1,&\hat\beta_j>0\\
-1,&\hat\beta_j<0\\
\in[-1,1],&\hat\beta_j=0
\end{cases}
$$

等价理解：

- 若变量进入模型，残差与该变量的相关达到阈值 $\lambda$；
- 若变量没进入模型，残差与该变量的相关不超过 $\lambda$。

这解释了 Lasso 为什么会产生稀疏解。

### 7.1 KKT 条件的逐坐标解释

令残差

$$
r=y-X\hat\beta
$$

KKT 条件为：

$$
X_j^\top r=\lambda s_j
$$

因此：

若 $\hat\beta_j\ne0$，

$$
|X_j^\top r|=\lambda
$$

若 $\hat\beta_j=0$，

$$
|X_j^\top r|\le\lambda
$$

这说明 Lasso 的变量选择规则是：只有当某个变量与当前残差的相关性足够大，达到阈值 $\lambda$，它才可能进入模型。

### 7.2 Lasso 解的唯一性

PPT 强调：Lasso 的系数解 $\hat\beta$ 不一定唯一，因为当 $X^\top X$ 奇异时，目标函数不是严格凸的。

但 fitted value 通常是唯一的：

$$
\boxed{X\hat\beta\text{ 唯一}}
$$

原因是平方损失关于 $X\beta$ 是严格凸的。即使有多个 $\hat\beta$，它们给出的 $X\hat\beta$ 相同。

这带来两个后果：

1. 残差 $r=y-X\hat\beta$ 唯一；
2. 最优 subgradient $s=X^\top r/\lambda$ 唯一。

### 7.3 等相关集（Equicorrelation Set）

PPT 定义等相关集：

$$
\boxed{
E=\{j: |X_j^\top(y-X\hat\beta)|=\lambda\}
}
$$

等价地：

$$
E=\{j:|s_j|=1\}
$$

它表示与 Lasso 残差相关性达到最大阈值的变量集合。

主动集：

$$
A=\operatorname{supp}(\hat\beta)
$$

一定满足：

$$
\boxed{A\subseteq E}
$$

因为若 $\hat\beta_j\ne0$，KKT 必然要求 $|s_j|=1$。  
但反过来不一定成立：某些变量达到相关阈值，却未必在某个 Lasso 解中非零。

### 7.4 给定 active set 时的解形式

若主动集为 $A$，符号为

$$
s_A=\operatorname{sign}(\hat\beta_A)
$$

KKT 在 active set 上给出：

$$
X_A^\top(y-X_A\hat\beta_A)=\lambda s_A
$$

解得：

$$
\boxed{
\hat\beta_A=(X_A^\top X_A)^{-1}(X_A^\top y-\lambda s_A),\quad
\hat\beta_{-A}=0
}
$$

与 active set 上的 OLS 解

$$
(X_A^\top X_A)^{-1}X_A^\top y
$$

相比，Lasso 多了

$$
-\lambda(X_A^\top X_A)^{-1}s_A
$$

这正是 Lasso 的 shrinkage bias 来源。

### 7.5 Lasso 的偏差

Lasso 通过 $\ell_1$ 惩罚换来稀疏性，但代价是系数向 0 收缩。  
因此即使选对了变量，系数估计也通常有偏。

这就是 PPT 后面介绍非凸惩罚的动机：希望保留稀疏性，同时减少大信号的收缩偏差。

---

## 8. Lasso 路径与软阈值

### 8.1 正交设计下的直观解

若 $X$ 的列正交，则：

Best subset 是 hard-thresholding：

$$
\hat\beta_{\text{subset}}=H_{\sqrt{2\lambda}}(X^\top y)
$$

Lasso 是 soft-thresholding：

$$
\hat\beta_{\text{lasso}}=S_\lambda(X^\top y)
$$

Ridge 是连续缩小：

$$
\hat\beta_{\text{ridge}}=\frac{X^\top y}{1+2\lambda}
$$

### 8.2 Lasso solution path

随着 $\lambda$ 从大到小：

- $\lambda$ 很大时，$\hat\beta=0$；
- 变量逐渐进入模型；
- 系数路径是分段线性的；
- 路径算法通过 KKT 条件跟踪 knot。

这与 Least Angle Regression (LARS) 密切相关。

### 8.3 为什么路径是分段线性的？

Lasso 的 KKT 条件为：

$$
X^\top(y-X\hat\beta(\lambda))=\lambda s
$$

在某一段路径上，如果 active set $A$ 和符号 $s_A$ 不变，则

$$
\hat\beta_A(\lambda)
=(X_A^\top X_A)^{-1}(X_A^\top y-\lambda s_A)
$$

这是 $\lambda$ 的线性函数。  
只有当发生下面两种事件之一时，路径才换到下一段：

1. 某个 inactive variable 与残差相关达到阈值，进入等相关集；
2. 某个 active coefficient 变成 0，离开 active set。

因此 Lasso solution path 是连续、分段线性的。

### 8.4 路径算法的起点

当 $\lambda$ 足够大时：

$$
\hat\beta(\lambda)=0
$$

由 KKT：

$$
X^\top y=\lambda s,\quad \|s\|_\infty\le1
$$

所以零解成立当且仅当：

$$
\lambda\ge \|X^\top y\|_\infty
$$

路径第一个 knot：

$$
\boxed{\lambda_1=\|X^\top y\|_\infty}
$$

当 $\lambda$ 从 $\lambda_1$ 继续下降，首先进入模型的是与 $y$ 绝对相关最大的变量。

### 8.5 hitting time 与 crossing time

PPT 中路径算法反复检查两类时间：

- **hitting time**：某个当前未选变量满足 $|X_j^\top r|=\lambda$，准备进入；
- **crossing time**：某个当前已选变量的系数沿线性路径变成 0，准备退出。

算法每一步选更早发生的事件，更新 active set 和 signs，然后继续沿新的线性方向走。

这就是 LARS in lasso mode 的核心。

### 8.6 路径算法的直观流程

```
初始化：λ1 = ||X^T y||∞, β(λ)=0
重复：
  1. 当前 active set A 和 signs sA 固定
  2. 按 βA(λ)=(XA^T XA)^(-1)(XA^T y-λsA) 线性移动
  3. 计算下一个 hitting time
  4. 计算下一个 crossing time
  5. 取较大的下一个 λ knot
  6. 更新 A 和 sA
直到 λ=0 或达到所需模型复杂度
```

高可读性的理解：Lasso 不是对每个 $\lambda$ 从头优化，而是沿着一条由 KKT 条件控制的分段直线走。

---

## 9. Lasso 的风险界：慢速率与快速率

### 9.1 慢速率

在线性模型

$$
y=X\beta_0+\varepsilon
$$

且 $\|X_j\|_2^2\le n$、高斯噪声下，Lasso 可得预测误差界，量级类似：

$$
\frac1n\|X\hat\beta-X\beta_0\|_2^2
\lesssim
\|\beta_0\|_1\sigma\sqrt{\frac{\log p}{n}}
$$

这是较一般条件下的慢速率。

### 9.2 快速率

若设计矩阵满足 compatibility condition 或 restricted eigenvalue condition，则可得到更强的 oracle 型界：

$$
\boxed{
\frac1n\|X\hat\beta-X\beta_0\|_2^2
\lesssim
\frac{\sigma^2s_0\log p}{n}
}
$$

其中：

- $s_0=|\operatorname{supp}(\beta_0)|$ 是真实非零变量个数；
- $\log p$ 是高维变量选择代价；
- 该速率接近 best subset 的理想表现。

### 9.3 支持恢复

若还满足更强条件，例如：

- true support 上设计矩阵条件良好；
- irrelevant variables 与 relevant variables 相关不太强；
- 非零系数足够大；

则 Lasso 有可能恢复真实支持集：

$$
\operatorname{supp}(\hat\beta)=\operatorname{supp}(\beta_0)
$$

### 9.4 慢速率推导的核心不等式

PPT 先考虑 bound form，取

$$
\|\hat\beta\|_1\le \|\beta_0\|_1
$$

因为 $\hat\beta$ 最小化训练误差，所以

$$
\|y-X\hat\beta\|_2^2\le \|y-X\beta_0\|_2^2
$$

代入 $y=X\beta_0+\varepsilon$：

$$
\|X\hat\beta-X\beta_0\|_2^2
\le
2\langle\varepsilon,X\hat\beta-X\beta_0\rangle
$$

再写成：

$$
2\langle X^\top\varepsilon,\hat\beta-\beta_0\rangle
\le
2\|X^\top\varepsilon\|_\infty\|\hat\beta-\beta_0\|_1
$$

由于

$$
\|\hat\beta-\beta_0\|_1\le \|\hat\beta\|_1+\|\beta_0\|_1\le2\|\beta_0\|_1
$$

得到：

$$
\|X\hat\beta-X\beta_0\|_2^2
\le
4\|\beta_0\|_1\|X^\top\varepsilon\|_\infty
$$

若 $\varepsilon\sim N(0,\sigma^2I)$ 且 $\|X_j\|_2^2\le n$，则高概率下：

$$
\|X^\top\varepsilon\|_\infty
\lesssim
\sigma\sqrt{n\log(ep/\delta)}
$$

所以：

$$
\boxed{
\frac1n\|X\hat\beta-X\beta_0\|_2^2
\lesssim
\sigma\|\beta_0\|_1\sqrt{\frac{\log(ep/\delta)}{n}}
}
$$

这就是慢速率的来源。

### 9.4.1 penalized form 的慢速率

惩罚形式：

$$
\hat\beta=\arg\min_\beta
\frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1
$$

由最优性：

$$
\frac12\|y-X\hat\beta\|_2^2+\lambda\|\hat\beta\|_1
\le
\frac12\|y-X\beta_0\|_2^2+\lambda\|\beta_0\|_1
$$

整理：

$$
\|X\hat\beta-X\beta_0\|_2^2
\le
2\langle X^\top\varepsilon,\hat\beta-\beta_0\rangle
+2\lambda(\|\beta_0\|_1-\|\hat\beta\|_1)
$$

若选择

$$
\lambda\gtrsim \|X^\top\varepsilon\|_\infty
$$

就得到与约束形式同量级的预测误差界。

### 9.5 快速率：compatibility condition

慢速率只需要列归一化，因此很一般，但速率包含 $\|\beta_0\|_1$，不一定体现真实稀疏度 $s_0$。

为了得到

$$
\frac{s_0\log p}{n}
$$

这样的快速率，需要对设计矩阵加条件。

PPT 的 compatibility condition：

对真实支持集 $S$，存在 $\phi_0>0$，使得对所有满足

$$
\|v_{-S}\|_1\le3\|v_S\|_1
$$

的 $v$，有

$$
\boxed{
\frac1n\|Xv\|_2^2
\ge
\frac{\phi_0^2}{s_0}\|v_S\|_1^2
}
$$

直觉：如果一个向量主要集中在真实支持集附近，那么 $Xv$ 不能太小。  
也就是说，设计矩阵不能把真实方向上的信号“压扁”。

在该条件下，PPT 得到：

$$
\boxed{
\frac1n\|X\hat\beta-X\beta_0\|_2^2
\le
\frac{72\sigma^2s_0\log(ep/\delta)}{n\phi_0^2}
}
$$

高概率至少为 $1-\delta$。

### 9.5.1 cone condition 从哪里来？

快速率推导中会先证明：

$$
\|\hat\beta_{-S}-\beta_{0,-S}\|_1
\le
3\|\hat\beta_S-\beta_{0,S}\|_1
$$

因为 $\beta_{0,-S}=0$，所以

$$
\|\hat\beta_{-S}\|_1
\le
3\|\hat\beta_S-\beta_{0,S}\|_1
$$

这说明误差向量 $\hat\beta-\beta_0$ 落在一个 cone 里。  
compatibility condition 正是只要求设计矩阵在这个 cone 上表现良好，而不是在整个 $\mathbb R^p$ 上满秩。

### 9.5.2 Restricted eigenvalue condition

另一个常用条件是 restricted eigenvalue：

对所有 $|J|=s_0$ 且

$$
\|v_{J^c}\|_1\le3\|v_J\|_1
$$

的 $v$，有

$$
\boxed{
\frac1n\|Xv\|_2^2\ge \phi_0^2\|v\|_2^2
}
$$

它可以推出系数误差界：

$$
\boxed{
\|\hat\beta-\beta_0\|_2^2
\lesssim
\frac{s_0\log p}{n\phi_0^4}
}
$$

直觉：虽然 $p>n$ 时 $X^\top X$ 不可能全局正定，但我们只需要它在稀疏方向上像正定矩阵。

### 9.6 支持恢复：Primal-Dual Witness

PPT 的支持恢复部分目标更强：

$$
\boxed{
\operatorname{supp}(\hat\beta)=S,\quad
\operatorname{sign}(\hat\beta_S)=\operatorname{sign}(\beta_{0,S})
}
$$

方法叫 primal-dual witness，流程：

1. 假设真实支持集 $S$ 就是 active set；
2. 在 $S$ 上解 restricted Lasso；
3. 在 $S^c$ 上构造 dual variable；
4. 验证 $S$ 上符号正确；
5. 验证 $S^c$ 上 strict dual feasibility：

$$
\|s_{-S}\|_\infty<1
$$

如果这些条件成立，就证明 Lasso 选对了变量和符号。

### 9.6.1 支持恢复所需条件

PPT 列出三类条件。

**1. Mutual incoherence**

对某个 $\gamma>0$，

$$
\boxed{
\|(X_S^\top X_S)^{-1}X_S^\top X_j\|_1\le1-\gamma,
\quad j\notin S
}
$$

含义：非真实变量不能被真实变量线性解释得太好。否则 Lasso 很难区分谁是真变量、谁是替代变量。

**2. Minimum eigenvalue**

$$
\boxed{
\Lambda_{\min}\left(\frac1nX_S^\top X_S\right)\ge C
}
$$

含义：真实变量之间不能严重共线。

**3. Minimum signal**

$$
\boxed{
\beta_{0,\min}=\min_{j\in S}|\beta_{0,j}|
\text{ 足够大}
}
$$

含义：真实非零系数必须大到能从噪声和 Lasso 收缩中被识别出来。

### 9.6.2 支持恢复比预测难

预测误差小不代表变量一定选对。  
若两个变量高度相关，选 $X_1$ 或 $X_2$ 可能预测差不多，但支持集完全不同。

因此：

```
慢速率：几乎不要求 X
快速率：要求 X 在稀疏方向上好
支持恢复：还要求非真变量与真变量低相关、真信号足够大
```

### 9.7 Minimax bounds

PPT 最后给出稀疏线性模型的 minimax prediction error：

$$
M(s_0,n,p)
=
\inf_{\hat\beta}
\sup_{\|\beta_0\|_0\le s_0}
\frac1n\|X\hat\beta-X\beta_0\|_2^2
$$

在适当条件下，上下界同阶：

$$
\boxed{
M(s_0,n,p)\asymp \frac{s_0\log(p/s_0)}{n}
}
$$

这说明 $s_0\log p/n$ 不是 Lasso 分析的偶然产物，而是高维稀疏预测问题本身的统计难度。

### 9.8 非凸惩罚：为什么要超越 Lasso？

Lasso 的 $\ell_1$ 惩罚会对所有非零系数持续施加同样的收缩，因此大信号也会被拉向 0，产生偏差。

改进思路：使用非凸惩罚，使小系数被压成 0，但大系数受到较小惩罚。

PPT 提到两类：

**$\ell_\gamma$ penalty**

$$
P(t)=t^\gamma,\quad 0<\gamma<1
$$

它比 $\ell_1$ 更强烈鼓励稀疏，但优化非凸。

**SCAD**

SCAD 的思想是：

- 小系数附近像 Lasso 一样强惩罚；
- 中等系数逐渐降低惩罚；
- 大系数几乎不再惩罚，从而减少偏差。

非凸惩罚通常有更好的统计性质，但优化更难，可能存在局部最优。

---

## 10. 本章知识图谱

```
                    线性回归与 Lasso
                            |
       ┌────────────────────┼────────────────────┐
       |                    |                    |
    经典回归              模型推断              正则化
       |                    |                    |
 y=Xβ+ε                 β_hat 分布             subset / ridge / lasso
       |                    |                    |
 最小二乘               t 检验 / CI            ℓ0 / ℓ2 / ℓ1
       |                    |                    |
 投影 H                 F 检验 / ANOVA         KKT 条件
       |                    |                    |
 残差正交               R² / adjusted R²       稀疏性 / 路径算法
                                                |
                                          慢速率 / 快速率 / 支持恢复
```

更完整地看，本章知识图谱可以展开为：

```
线性回归与 Lasso
 |
 |-- 经典线性模型
 |     |
 |     |-- 数据结构
 |     |     y_i = β0 + β1x_i1 + ... + βp x_ip + ε_i
 |     |     y = Xβ + ε
 |     |
 |     |-- 最小二乘
 |     |     min ||y-Xβ||²
 |     |     β_hat = (X'X)^(-1)X'y
 |     |
 |     |-- 几何
 |     |     H = X(X'X)^(-1)X'
 |     |     y_hat = Hy
 |     |     residual = (I-H)y
 |     |     X'residual = 0
 |     |
 |     |-- 分布
 |     |     β_hat ~ N(β, σ²(X'X)^(-1))
 |     |     RSS/σ² ~ χ²_{n-p-1}
 |     |     β_hat ⟂ RSS
 |     |
 |     |-- 推断
 |           coefficient t-test
 |           model reduction F-test
 |           ANOVA / deviance table
 |           R² / adjusted R²
 |
 |-- 高维正则化
       |
       |-- OLS 风险
       |     rank(X)<p -> 解不唯一 / 不稳定
       |
       |-- penalty
       |     ℓ0 subset: sparse but hard
       |     ℓ1 lasso: sparse and convex
       |     ℓ2 ridge: stable but not sparse
       |
       |-- Lasso 优化
       |     min 1/2||y-Xβ||² + λ||β||1
       |     KKT: X'(y-Xβ_hat)=λs
       |     active set A ⊂ equicorrelation set E
       |
       |-- Lasso 路径
       |     λ1=||X'y||∞
       |     piecewise linear path
       |     hitting / crossing events
       |
       |-- 理论
             slow rate: ||β0||1 sqrt(log p/n)
             fast rate: s0 log p/n
             support recovery: incoherence + signal strength
             minimax: s0 log(p/s0)/n
             nonconvex penalties reduce bias
```

---

## 11. 易错点与考点

| 误区 | 正确认识 |
|------|----------|
| 回归系数显著就是因果 | 显著性不等于因果，需要设计或识别假设 |
| 残差和响应变量正交 | 残差与设计矩阵列空间正交 |
| $R^2$ 越高模型越好 | 加变量可机械提高 $R^2$，要看 adjusted $R^2$ 和泛化 |
| Ridge 能做变量选择 | Ridge 收缩但通常不置零 |
| Lasso 解总唯一 | 系数不一定唯一，但 fitted value 常唯一 |
| Lasso 无偏 | Lasso 有收缩偏差 |
| $p>n$ 时 OLS 还能正常唯一 | 通常不可逆，需要正则化 |
| $R^2$ 可以直接用于变量选择 | $R^2$ 会随变量增加而不降，应看 adjusted $R^2$、验证误差或检验 |
| Lasso 选中变量就说明因果有效 | Lasso 是预测/选择工具，不自动给因果解释 |
| 快速率不需要设计条件 | 必须有 compatibility 或 restricted eigenvalue 等条件 |
| 预测好就一定支持恢复好 | 高相关变量下预测可好，但变量选择可能错 |
| $\lambda$ 越小越好 | $\lambda$ 小偏差小但方差大，可能过拟合 |

---

## 12. 关键公式速查表

| 内容 | 公式 |
|------|------|
| 线性模型 | $y=X\beta+\varepsilon$ |
| OLS | $\hat\beta=(X^\top X)^{-1}X^\top y$ |
| Hat matrix | $H=X(X^\top X)^{-1}X^\top$ |
| 残差 | $\hat\varepsilon=(I-H)y$ |
| 残差正交 | $X^\top\hat\varepsilon=0$ |
| OLS 分布 | $\hat\beta\sim N(\beta,\sigma^2(X^\top X)^{-1})$ |
| 方差估计 | $s^2=RSS/(n-p-1)$ |
| 系数 t | $(\hat\beta_j-\beta_j)/(s\sqrt{c_{jj}})$ |
| Lasso | $\min_\beta \frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1$ |
| Lasso KKT | $X^\top(y-X\hat\beta)=\lambda s$ |
| 快速率 | $\|X\hat\beta-X\beta_0\|_2^2/n\lesssim\sigma^2s_0\log p/n$ |
| 等相关集 | $E=\{j:|X_j^\top(y-X\hat\beta)|=\lambda\}$ |
| active set 解 | $\hat\beta_A=(X_A^\top X_A)^{-1}(X_A^\top y-\lambda s_A)$ |
| 第一个 knot | $\lambda_1=\|X^\top y\|_\infty$ |
| 慢速率 | $\|X\hat\beta-X\beta_0\|_2^2/n\lesssim\sigma\|\beta_0\|_1\sqrt{\log p/n}$ |
| compatibility | $\|Xv\|_2^2/n\ge(\phi_0^2/s_0)\|v_S\|_1^2$ |
| minimax rate | $M(s_0,n,p)\asymp s_0\log(p/s_0)/n$ |

---

## 13. 学习建议

1. 先把线性模型的几何图像想清楚：拟合是投影，残差与列空间正交。
2. 经典推断围绕 $\hat\beta$ 的正态分布和 $RSS$ 的卡方分布。
3. 模型缩减检验本质上比较 full model 和 reduced model。
4. 正则化要从“控制复杂度”理解，不只是为了计算。
5. Lasso 的核心是 $\ell_1$ 惩罚带来的稀疏性，KKT 条件是理解它的最好入口。
6. 高维理论重点看速率：为什么出现 $s_0\log p/n$，以及它需要什么设计条件。
7. 若时间有限，经典回归先掌握 `OLS -> 投影 -> t/F 推断`；Lasso 先掌握 `KKT -> 稀疏 -> 路径 -> 风险界`。
8. 对 Lasso 理论不要只背结论，要分清三种目标：预测误差小、系数估计准、支持集恢复正确。它们所需条件越来越强。

---

## 14. PPT 内容对照式复习清单

### 14.1 线性回归部分必须会

1. 用 Advertising data 说清楚 $n,p,y,X,\beta$ 分别是什么。
2. 从最小二乘目标函数推导正规方程。
3. 解释 $H=X(X^\top X)^{-1}X^\top$ 为什么是投影矩阵。
4. 证明或说明残差正交：

$$
X^\top(y-X\hat\beta)=0
$$

5. 写出 $\hat\beta$ 的分布：

$$
\hat\beta\sim N(\beta,\sigma^2(X^\top X)^{-1})
$$

6. 写出 RSS 的分布和自由度：

$$
RSS/\sigma^2\sim\chi^2_{n-p-1}
$$

7. 写出单个系数的 $t$ 检验统计量。
8. 写出模型缩减的 F 检验。
9. 解释 $R^2$ 为什么随变量数增加而不降。
10. 解释 adjusted $R^2$ 如何惩罚变量数。

### 14.2 Lasso 算法部分必须会

1. 说清楚 best subset、ridge、Lasso 的惩罚差异。
2. 解释为什么 $\ell_1$ 会导致稀疏。
3. 正交设计下写出 hard-thresholding、soft-thresholding、ridge shrinkage。
4. 写出 Lasso KKT：

$$
X^\top(y-X\hat\beta)=\lambda s
$$

5. 用 KKT 说明：

$$
\hat\beta_j=0\Rightarrow |X_j^\top r|\le\lambda
$$

6. 定义等相关集 $E$，并说明 $A\subseteq E$。
7. 说明 fitted value 唯一但系数不一定唯一。
8. 解释 Lasso path 为什么分段线性。
9. 写出第一个 knot：

$$
\lambda_1=\|X^\top y\|_\infty
$$

10. 说清 hitting time 与 crossing time 的含义。

### 14.3 Lasso 理论部分必须会

1. 慢速率需要的假设：列归一化 + 高斯噪声。
2. 慢速率形式：

$$
\frac1n\|X\hat\beta-X\beta_0\|^2
\lesssim
\sigma\|\beta_0\|_1\sqrt{\frac{\log p}{n}}
$$

3. 快速率为什么需要 compatibility / restricted eigenvalue。
4. 快速率形式：

$$
\frac1n\|X\hat\beta-X\beta_0\|^2
\lesssim
\frac{\sigma^2s_0\log p}{n}
$$

5. 支持恢复需要更强条件：mutual incoherence、minimum eigenvalue、minimum signal。
6. 解释为什么支持恢复比预测更难。
7. 知道 minimax rate：

$$
\frac{s_0\log(p/s_0)}{n}
$$

8. 知道非凸惩罚的目的：减少 Lasso 对大系数的偏差。
