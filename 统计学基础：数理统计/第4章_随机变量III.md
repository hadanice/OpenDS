# 第 4 章：随机变量 III（均值方差性质、顺序统计量、条件分布与矩母函数）

> 本文对应 `课件/4 随机变量.pdf`。
>
> 这一章把随机变量工具进一步系统化：线性组合怎么求均值方差？样本最大值最小值怎么分布？条件分布如何定义？矩母函数如何统一刻画分布与求和？

---

## 0. 本章定位

第 3 章建立了期望、方差、联合分布和变量变换。  
第 4 章把这些工具组合起来，形成后续统计推断的技术底座：

```
均值方差性质 -> 样本均值/样本方差
顺序统计量 -> 最大值/最小值/MLE 边界问题
条件分布 -> Bayes 与充分性
矩母函数 -> 分布识别、和的分布、CLT
```

---

## 1. 期望的线性性

### 1.1 两个变量

只要期望存在，不需要独立：

$$
\boxed{E(aX+bY)=aE(X)+bE(Y)}
$$

### 1.2 多个变量

$$
\boxed{
E\left(\sum_{i=1}^n a_iW_i\right)=\sum_{i=1}^n a_iE(W_i)
}
$$

重要结论：期望的线性性不依赖独立性。

### 1.3 用指示变量重推二项均值

令

$$
X=I_1+\cdots+I_n
$$

其中 $I_i=1$ 表示第 $i$ 次成功。则

$$
E(X)=\sum_{i=1}^nE(I_i)=np
$$

这比直接展开二项求和更清楚。

---

## 2. 协方差与方差运算

### 2.1 协方差

$$
\boxed{\operatorname{Cov}(X,Y)=E[(X-EX)(Y-EY)]}
$$

等价形式：

$$
\boxed{\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)}
$$

### 2.2 独立与协方差

若 $X,Y$ 独立，则

$$
E(XY)=E(X)E(Y)
$$

所以

$$
\operatorname{Cov}(X,Y)=0
$$

但反过来不一定成立：协方差为 0 不保证独立。

### 2.3 线性组合方差

$$
\boxed{
\operatorname{Var}(aX+bY)=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)+2ab\operatorname{Cov}(X,Y)
}
$$

若 $X,Y$ 独立：

$$
\operatorname{Var}(aX+bY)=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)
$$

多个变量：

$$
\operatorname{Var}\left(\sum_i a_iW_i\right)
=\sum_i a_i^2\operatorname{Var}(W_i)+2\sum_{i<j}a_ia_j\operatorname{Cov}(W_i,W_j)
$$

若两两独立：

$$
\operatorname{Var}\left(\sum_i a_iW_i\right)=\sum_i a_i^2\operatorname{Var}(W_i)
$$

---

## 3. 顺序统计量

### 3.1 定义

给定随机样本 $Y_1,\dots,Y_n$，把观测值从小到大排列：

$$
Y_{(1)}\le Y_{(2)}\le \cdots\le Y_{(n)}
$$

其中 $Y_{(i)}$ 称为第 $i$ 个顺序统计量。

特别地：

$$
Y_{(1)}=Y_{\min},\quad Y_{(n)}=Y_{\max}
$$

### 3.2 最大值与最小值

若 $Y_1,\dots,Y_n$ i.i.d.，共同 CDF 为 $F$，pdf 为 $f$。

最大值：

$$
P(Y_{(n)}\le y)=P(Y_1\le y,\dots,Y_n\le y)=[F(y)]^n
$$

所以

$$
\boxed{f_{Y_{(n)}}(y)=n[F(y)]^{n-1}f(y)}
$$

最小值：

$$
P(Y_{(1)}>y)=P(Y_1>y,\dots,Y_n>y)=[1-F(y)]^n
$$

所以

$$
\boxed{f_{Y_{(1)}}(y)=n[1-F(y)]^{n-1}f(y)}
$$

### 3.3 第 $i$ 个顺序统计量

连续情形：

$$
\boxed{
f_{Y_{(i)}}(y)=
\frac{n!}{(i-1)!(n-i)!}
[F(y)]^{i-1}[1-F(y)]^{n-i}f(y)
}
$$

直觉：有 $i-1$ 个样本落在 $y$ 左边，$n-i$ 个落在 $y$ 右边，一个样本落在 $y$ 附近。

### 3.4 顺序统计量为什么重要？

它连接后续多个主题：

- 样本极值的分布；
- Uniform$(0,\theta)$ 中 $\theta$ 的 MLE 是 $Y_{(n)}$；
- 定义域含参数时，MLE 常常在边界上；
- 样本范围 $Y_{(n)}-Y_{(1)}$ 的分布。

---

## 4. 条件分布与条件期望

### 4.1 离散条件 pmf

$$
\boxed{
p_{X\mid Y}(x\mid y)=\frac{p_{X,Y}(x,y)}{p_Y(y)}
}
$$

前提是 $p_Y(y)>0$。

### 4.2 连续条件 pdf

$$
\boxed{
f_{X\mid Y}(x\mid y)=\frac{f_{X,Y}(x,y)}{f_Y(y)}
}
$$

前提是 $f_Y(y)>0$。

### 4.3 条件期望

离散：

$$
E(X\mid Y=y)=\sum_x x\,p_{X\mid Y}(x\mid y)
$$

连续：

$$
E(X\mid Y=y)=\int x\,f_{X\mid Y}(x\mid y)\,dx
$$

条件期望本质上是“给定信息后的平均值”。

---

## 5. 矩母函数（Moment Generating Function, MGF）

### 5.1 定义

随机变量 $W$ 的矩母函数定义为：

$$
\boxed{M_W(t)=E(e^{tW})}
$$

在 $t=0$ 附近存在时，它可以生成各阶矩。

### 5.2 生成矩

若 $M_W(t)$ 存在，则

$$
\boxed{E(W^r)=M_W^{(r)}(0)}
$$

即对 $M_W(t)$ 求 $r$ 阶导，再令 $t=0$。

### 5.3 分布识别

若两个随机变量的 MGF 在 0 附近相同，则它们分布相同。

这在证明“某个和仍然服从某分布”时非常好用。

### 5.4 独立和的 MGF

若 $W_1,\dots,W_n$ 独立，则

$$
\boxed{
M_{\sum_i W_i}(t)=\prod_i M_{W_i}(t)
}
$$

例：若 $X_1\sim\operatorname{Poisson}(\lambda_1)$，$X_2\sim\operatorname{Poisson}(\lambda_2)$ 且独立，则

$$
X_1+X_2\sim\operatorname{Poisson}(\lambda_1+\lambda_2)
$$

---

## 6. 特征函数

特征函数定义为：

$$
\boxed{\varphi_X(t)=E(e^{itX})}
$$

它与 MGF 类似，但优点是总是存在。渐近理论中用特征函数证明弱收敛和中心极限定理非常常见。

---

## 7. 本章知识图谱

```
                         随机变量 III
                              |
      ┌───────────────────────┼────────────────────────┐
      |                       |                        |
  均值方差性质              顺序统计量              条件与MGF
      |                       |                        |
  期望线性性             Y_(1),...,Y_(n)          条件pmf/pdf
      |                       |                        |
  协方差 Cov              最大值/最小值            条件期望
      |                       |                        |
  Var(线性组合)           第i个顺序统计量           M_W(t)=E(e^{tW})
      |                       |                        |
  独立时方差可加          极值/MLE边界             分布识别/独立和
```

---

## 8. 易错点与考点

| 误区 | 正确认识 |
|------|----------|
| 期望线性性需要独立 | 不需要独立 |
| 方差也总是线性 | 方差有协方差项，独立时才简单相加 |
| 协方差为 0 就独立 | 一般不成立，除非有额外条件如联合正态 |
| 最大值 pdf 直接是 $[F(y)]^n$ | $[F(y)]^n$ 是 CDF，pdf 要再求导 |
| 条件密度忘记除以边际密度 | $f_{X|Y}=f_{X,Y}/f_Y$ |
| MGF 总存在 | 不一定，特征函数才总存在 |

---

## 9. 关键公式速查表

| 内容 | 公式 |
|------|------|
| 期望线性性 | $E(\sum a_iX_i)=\sum a_iE(X_i)$ |
| 协方差 | $\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)$ |
| 两变量方差 | $\operatorname{Var}(aX+bY)=a^2Var(X)+b^2Var(Y)+2abCov(X,Y)$ |
| 最大值 pdf | $n[F(y)]^{n-1}f(y)$ |
| 最小值 pdf | $n[1-F(y)]^{n-1}f(y)$ |
| 第 $i$ 顺序统计量 | $\frac{n!}{(i-1)!(n-i)!}[F(y)]^{i-1}[1-F(y)]^{n-i}f(y)$ |
| 条件 pmf | $p_{X|Y}(x|y)=p_{X,Y}(x,y)/p_Y(y)$ |
| 条件 pdf | $f_{X|Y}(x|y)=f_{X,Y}(x,y)/f_Y(y)$ |
| MGF | $M_X(t)=E(e^{tX})$ |
| 独立和 MGF | $M_{\sum X_i}(t)=\prod M_{X_i}(t)$ |

---

## 10. 学习建议

1. 用指示变量理解二项分布均值和方差。
2. 顺序统计量题先写 CDF，再求导，尤其是最大值和最小值。
3. 条件分布题先求边际，再相除。
4. MGF 题要记住两个动作：求导得矩，乘积得独立和。
5. 本章公式多，但核心只有一个：从联合结构里提取需要的边际、条件或函数分布。

---

## 11. PPT 深挖：线性性、协方差与方差分解

本章前半部分的目标不是再发明新的分布，而是回答一个更常见的问题：当随机变量组合在一起时，期望、方差、协方差如何变化。PPT 的例题通常会把这一点放在联合分布、样本和顺序统计量之前，因为后面的推断都要用它。

### 11.1 期望线性性的真正含义

无论 $X$ 和 $Y$ 是否独立，只要期望存在，就有

$$
E(aX+bY+c)=aE(X)+bE(Y)+c.
$$

这条性质的强大之处在于：它不要求你知道 $aX+bY$ 的完整分布。

对离散型联合分布：

$$
E(aX+bY)=\sum_x\sum_y (ax+by)p(x,y)
=a\sum_x x p_X(x)+b\sum_y y p_Y(y).
$$

对连续型联合密度：

$$
E(aX+bY)=\int\int(ax+by)f(x,y)\,dxdy
=aE(X)+bE(Y).
$$

PPT 里常用这一点计算样本均值：

$$
E(\bar X)=E\left(\frac1n\sum_{i=1}^nX_i\right)
=\frac1n\sum_{i=1}^nE(X_i)=\mu.
$$

这里不需要先求 $\bar X$ 的密度。

### 11.2 协方差：不是“是否一起变”，而是“线性一起变”

协方差定义为

$$
\operatorname{Cov}(X,Y)=E[(X-\mu_X)(Y-\mu_Y)]
=E(XY)-E(X)E(Y).
$$

要点：

1. 若 $X,Y$ 独立，则 $E(XY)=E(X)E(Y)$，所以 $\operatorname{Cov}(X,Y)=0$。
2. 反过来不一定成立，协方差为 0 只表示没有线性相关。
3. 协方差有单位，不方便比较；相关系数

$$
\rho=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}
$$

才是标准化后的线性相关度量。

典型判断题：

| 说法 | 判断 |
|------|------|
| 独立一定不相关 | 对 |
| 不相关一定独立 | 错，一般不成立 |
| 正态联合分布中不相关可推出独立 | 对，这是正态族的特殊性质 |
| 协方差为正表示 $Y$ 一定随 $X$ 增大 | 错，只表示平均线性趋势 |

### 11.3 方差公式为什么有协方差项

从定义展开：

$$
\operatorname{Var}(aX+bY)
=E[(a(X-\mu_X)+b(Y-\mu_Y))^2].
$$

得到

$$
\operatorname{Var}(aX+bY)
=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)+2ab\operatorname{Cov}(X,Y).
$$

如果 $X,Y$ 独立，协方差项消失；如果不独立，不能简单相加。

推广到 $n$ 个变量：

$$
\operatorname{Var}\left(\sum_{i=1}^n X_i\right)
=\sum_{i=1}^n\operatorname{Var}(X_i)
+2\sum_{i<j}\operatorname{Cov}(X_i,X_j).
$$

这就是为什么样本不是独立时，样本均值方差不再简单等于 $\sigma^2/n$。

### 11.4 用指示变量推导二项分布方差

设

$$
X=\sum_{i=1}^n I_i,\qquad I_i=
\begin{cases}
1,&\text{第 }i\text{ 次成功},\\
0,&\text{否则}.
\end{cases}
$$

若 $I_i$ 独立且 $P(I_i=1)=p$，则

$$
E(I_i)=p,\qquad \operatorname{Var}(I_i)=p(1-p).
$$

所以

$$
E(X)=np,\qquad
\operatorname{Var}(X)=np(1-p).
$$

这个推导比直接对二项 pmf 求和更重要，因为它展示了“复杂计数变量 = 简单指示变量之和”的思想。后面很多期望题、抽样题、占位题都可以这样做。

---

## 12. PPT 深挖：顺序统计量

顺序统计量是本章的核心难点之一。给定独立同分布样本 $Y_1,\dots,Y_n$，排序后记为

$$
Y_{(1)}\le Y_{(2)}\le\cdots\le Y_{(n)}.
$$

其中 $Y_{(1)}$ 是最小值，$Y_{(n)}$ 是最大值。

### 12.1 最大值：先写 CDF

最大值不超过 $y$ 等价于所有样本都不超过 $y$：

$$
P(Y_{(n)}\le y)=P(Y_1\le y,\dots,Y_n\le y)
=[F(y)]^n.
$$

所以若 $Y_i$ 连续且密度为 $f$，

$$
f_{Y_{(n)}}(y)=n[F(y)]^{n-1}f(y).
$$

这类题最常见的错误是直接写“有一个等于最大值”，但连续变量“等于某个点”的概率为 0。正确路线是先处理事件，再求导。

### 12.2 最小值：转成补事件

最小值大于 $y$ 等价于所有样本都大于 $y$：

$$
P(Y_{(1)}>y)=[1-F(y)]^n.
$$

因此

$$
P(Y_{(1)}\le y)=1-[1-F(y)]^n,
$$

密度为

$$
f_{Y_{(1)}}(y)=n[1-F(y)]^{n-1}f(y).
$$

### 12.3 第 $i$ 个顺序统计量：组合计数

事件 $Y_{(i)}\in[y,y+dy]$ 的直觉是：

1. 有一个观测落在 $y$ 附近；
2. 有 $i-1$ 个观测小于 $y$；
3. 有 $n-i$ 个观测大于 $y$；
4. 对这些角色进行排列组合。

因此密度为

$$
f_{Y_{(i)}}(y)
=\frac{n!}{(i-1)!(n-i)!}
[F(y)]^{i-1}[1-F(y)]^{n-i}f(y).
$$

把 $i=1$ 和 $i=n$ 代入，可以回到最小值和最大值公式。

### 12.4 Uniform 顺序统计量的特殊简化

若 $Y_i\sim U(0,1)$，则 $F(y)=y,f(y)=1$，于是

$$
f_{Y_{(i)}}(y)
=\frac{n!}{(i-1)!(n-i)!}y^{i-1}(1-y)^{n-i},
\quad 0<y<1.
$$

这说明

$$
Y_{(i)}\sim \operatorname{Beta}(i,n-i+1).
$$

因此

$$
E[Y_{(i)}]=\frac{i}{n+1}.
$$

这条结论常用于理解样本分位数：排序后的第 $i$ 个观测大致对应总体的 $i/(n+1)$ 分位点。

### 12.5 样本极差与联合密度

样本极差

$$
R=Y_{(n)}-Y_{(1)}
$$

要同时处理最小值和最大值。连续 iid 情形下，$(Y_{(1)},Y_{(n)})$ 的联合密度为

$$
f_{Y_{(1)},Y_{(n)}}(u,v)
=n(n-1)[F(v)-F(u)]^{n-2}f(u)f(v),
\quad u<v.
$$

直觉：

1. 一个点落在 $u$ 附近；
2. 一个点落在 $v$ 附近；
3. 剩下 $n-2$ 个点落在 $(u,v)$；
4. 排列角色数为 $n(n-1)$。

如果题目要求 $R$ 的分布，通常会做变量变换：$r=v-u$，再对 $u$ 积分。

---

## 13. PPT 深挖：条件分布与 MGF

### 13.1 条件分布的统一套路

无论离散还是连续，条件分布都遵循同一个结构：

$$
\text{条件}=\frac{\text{联合}}{\text{边际}}.
$$

离散型：

$$
p_{X|Y}(x|y)=\frac{p_{X,Y}(x,y)}{p_Y(y)}.
$$

连续型：

$$
f_{X|Y}(x|y)=\frac{f_{X,Y}(x,y)}{f_Y(y)}.
$$

常见步骤：

1. 写出联合 pmf/pdf 的支持区域；
2. 对不关心的变量求和或积分，得到边际；
3. 相除；
4. 重新写清条件支持。

条件支持是最容易漏的部分。例如原支持若为 $0<x<y<1$，那么给定 $Y=y$ 后，$X$ 的支持是 $0<x<y$，不是 $0<x<1$。

### 13.2 条件二项与超几何

一个常见 PPT 题型是：设 $X\sim Bin(n,p)$，$Y\sim Bin(m,p)$ 且独立，给定 $X+Y=k$，求 $X$ 的条件分布。

有

$$
P(X=x\mid X+Y=k)
=\frac{P(X=x,Y=k-x)}{P(X+Y=k)}.
$$

代入二项 pmf 后，$p$ 的幂次会消掉，得到

$$
P(X=x\mid X+Y=k)
=\frac{\binom nx\binom m{k-x}}{\binom{n+m}{k}}.
$$

这就是超几何分布。解释是：已知总共有 $k$ 次成功，只问这 $k$ 次成功中有多少来自第一组，成功概率 $p$ 不再重要。

### 13.3 MGF 的三个用途

矩母函数定义为

$$
M_X(t)=E(e^{tX}).
$$

它有三个常用用途。

第一，求矩：

$$
M_X'(0)=E(X),\qquad M_X''(0)=E(X^2).
$$

第二，识别分布。如果两个随机变量的 MGF 在 0 附近存在且相同，则它们分布相同。

第三，处理独立和。若 $X,Y$ 独立，

$$
M_{X+Y}(t)=M_X(t)M_Y(t).
$$

例如 $X_i\sim Poisson(\lambda_i)$ 独立，则

$$
M_{X_i}(t)=\exp\{\lambda_i(e^t-1)\},
$$

所以

$$
M_{\sum X_i}(t)=\exp\left\{\left(\sum\lambda_i\right)(e^t-1)\right\},
$$

即

$$
\sum X_i\sim Poisson\left(\sum\lambda_i\right).
$$

### 13.4 常见 MGF 表

| 分布 | MGF |
|------|-----|
| Bernoulli$(p)$ | $1-p+pe^t$ |
| Binomial$(n,p)$ | $(1-p+pe^t)^n$ |
| Poisson$(\lambda)$ | $\exp\{\lambda(e^t-1)\}$ |
| Normal$(\mu,\sigma^2)$ | $\exp\{\mu t+\sigma^2t^2/2\}$ |
| Exponential$(\lambda)$ | $\lambda/(\lambda-t),\ t<\lambda$ |
| Gamma$(r,\lambda)$ | $(\lambda/(\lambda-t))^r,\ t<\lambda$ |

### 13.5 特征函数为什么出现

MGF 不一定存在，因为 $E(e^{tX})$ 可能发散。特征函数定义为

$$
\phi_X(t)=E(e^{itX}),
$$

其中 $i^2=-1$。由于 $|e^{itX}|=1$，特征函数总存在。

在本课中，特征函数主要用于理解“分布收敛”和“CLT 证明”的技术工具。考试层面通常不要求复杂计算，但要知道它比 MGF 更稳健。

---

## 14. 本章 PPT 对照复习清单

| PPT 内容 | 复习时要能做到 |
|----------|----------------|
| 期望线性性 | 不求组合变量分布也能算期望 |
| 协方差 | 会从 $E(XY)-E(X)E(Y)$ 计算 |
| 方差分解 | 能判断何时可直接相加、何时要加协方差 |
| 指示变量法 | 会推导 $Bin(n,p)$ 的均值和方差 |
| 最大值/最小值 | 会先写 CDF 再求导 |
| 第 $i$ 顺序统计量 | 会解释组合系数来源 |
| Uniform 顺序统计量 | 知道与 Beta 分布的关系 |
| 条件分布 | 会写联合、边际、条件支持 |
| 条件二项例题 | 能推出超几何分布 |
| MGF | 会求矩、识别独立和、说明存在性限制 |
| 特征函数 | 知道它总存在并服务于分布收敛 |
