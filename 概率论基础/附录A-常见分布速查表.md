# 附录A 常见分布速查表

本附录汇总课程中反复出现的分布。参数化方式与正文保持一致：Gamma 分布采用形状 $r$、率参数 $\lambda$，即密度中含 $e^{-\lambda x}$。

## 1. 离散分布

| 分布 | 记号 | 取值 | 分布律 | 期望 | 方差 |
|---|---|---|---|---:|---:|
| 单点分布 | $\xi=a$ a.s. | $\{a\}$ | $P(\xi=a)=1$ | $a$ | $0$ |
| Bernoulli | $Bernoulli(p)$ | $0,1$ | $P(\xi=1)=p$ | $p$ | $p(1-p)$ |
| 二项 | $B(n,p)$ | $0,\ldots,n$ | $\binom nkp^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| 超几何 | $H(N,M,n)$ | 合法整数 $k$ | $\frac{\binom Mk\binom{N-M}{n-k}}{\binom Nn}$ | $nM/N$ | $n\frac MN(1-\frac MN)\frac{N-n}{N-1}$ |
| Poisson | $P(\lambda)$ | $0,1,\ldots$ | $e^{-\lambda}\frac{\lambda^k}{k!}$ | $\lambda$ | $\lambda$ |
| 几何 | $Geom(p)$ | $1,2,\ldots$ | $(1-p)^{k-1}p$ | $1/p$ | $(1-p)/p^2$ |
| 离散均匀 | $U\{1,\ldots,n\}$ | $1,\ldots,n$ | $1/n$ | $(n+1)/2$ | $(n^2-1)/12$ |

超几何分布的合法范围：

$$
\max(0,n-(N-M))\le k\le \min(n,M).
$$

## 2. 连续分布

| 分布 | 记号 | 支撑 | 密度 | 期望 | 方差 |
|---|---|---|---|---:|---:|
| 均匀 | $U(a,b)$ | $(a,b)$ | $\frac1{b-a}$ | $(a+b)/2$ | $(b-a)^2/12$ |
| 指数 | $Exp(\lambda)$ | $(0,\infty)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| 正态 | $N(\mu,\sigma^2)$ | $\mathbb R$ | $\frac1{\sqrt{2\pi}\sigma}e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ |
| Gamma | $\Gamma(r,\lambda)$ | $(0,\infty)$ | $\frac{\lambda^r}{\Gamma(r)}x^{r-1}e^{-\lambda x}$ | $r/\lambda$ | $r/\lambda^2$ |
| $\chi^2$ | $\chi_n^2$ | $(0,\infty)$ | $\Gamma(n/2,1/2)$ | $n$ | $2n$ |
| Cauchy | $Cauchy(0,1)$ | $\mathbb R$ | $\frac1{\pi(1+x^2)}$ | 不存在 | 不存在 |
| Beta | $Beta(\alpha,\beta)$ | $(0,1)$ | $\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}x^{\alpha-1}(1-x)^{\beta-1}$ | $\frac{\alpha}{\alpha+\beta}$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |

## 3. 分布函数

指数分布：

$$
F(x)=
\begin{cases}
0,& x\le 0,\\
1-e^{-\lambda x},& x>0.
\end{cases}
$$

标准正态：

$$
\Phi(x)=\frac1{\sqrt{2\pi}}\int_{-\infty}^{x}e^{-t^2/2}\,dt.
$$

标准 Cauchy：

$$
F(x)=\frac12+\frac1\pi\arctan x.
$$

## 4. 概率母函数

| 分布 | $G(s)=E(s^\xi)$ |
|---|---|
| Bernoulli | $1-p+ps$ |
| 二项 $B(n,p)$ | $(1-p+ps)^n$ |
| Poisson $P(\lambda)$ | $e^{\lambda(s-1)}$ |
| 几何，取值 $1,2,\ldots$ | $\frac{ps}{1-(1-p)s}$ |
| 几何，取值 $0,1,\ldots$ | $\frac{p}{1-(1-p)s}$ |

用母函数求矩：

$$
E\xi=G'(1).
$$

$$
Var(\xi)=G''(1)+G'(1)-[G'(1)]^2.
$$

独立和：

$$
G_{\xi+\eta}(s)=G_\xi(s)G_\eta(s).
$$

## 5. 特征函数

| 分布 | $\varphi(t)=E(e^{it\xi})$ |
|---|---|
| 单点 $a$ | $e^{ita}$ |
| Bernoulli | $1-p+pe^{it}$ |
| 二项 $B(n,p)$ | $(1-p+pe^{it})^n$ |
| Poisson $P(\lambda)$ | $\exp\{\lambda(e^{it}-1)\}$ |
| 均匀 $U(a,b)$ | $\frac{e^{itb}-e^{ita}}{it(b-a)}$，$t\ne 0$ |
| 指数 $Exp(\lambda)$ | $\frac{\lambda}{\lambda-it}$ |
| Gamma $\Gamma(r,\lambda)$ | $\left(\frac{\lambda}{\lambda-it}\right)^r$ |
| 正态 $N(\mu,\sigma^2)$ | $\exp(i\mu t-\sigma^2t^2/2)$ |
| 标准 Cauchy | $e^{-|t|}$ |

独立和：

$$
\varphi_{\xi+\eta}(t)=\varphi_\xi(t)\varphi_\eta(t).
$$

线性变换：

$$
\varphi_{a\xi+b}(t)=e^{itb}\varphi_\xi(at).
$$

## 6. 常见关系

Bernoulli 和二项：

$$
\sum_{i=1}^{n}Bernoulli(p)=B(n,p)
$$

其中变量独立。

Poisson 可加性：

$$
\sum_{i=1}^{n}P(\lambda_i)=P\left(\sum_{i=1}^{n}\lambda_i\right)
$$

其中变量独立。

Gamma 可加性：

$$
\Gamma(r_1,\lambda)+\Gamma(r_2,\lambda)
=\Gamma(r_1+r_2,\lambda)
$$

其中变量独立且率参数相同。

正态可加性：

$$
N(\mu_1,\sigma_1^2)+N(\mu_2,\sigma_2^2)
=N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)
$$

其中变量独立。

$\chi^2$ 与正态：

$$
\sum_{i=1}^{n}Z_i^2\sim \chi_n^2,\qquad Z_i\sim N(0,1)\text{ 独立}.
$$

$t$ 分布：

$$
\frac{Z}{\sqrt{V/n}}\sim t_n,\qquad
Z\sim N(0,1),\ V\sim \chi_n^2,\ Z\perp V.
$$

Cauchy 分布：

$$
\frac{Z_1}{Z_2}\sim Cauchy(0,1),\qquad
Z_1,Z_2\sim N(0,1)\text{ 独立}.
$$

Beta 分布：

$$
\frac{X}{X+Y}\sim Beta(\alpha,\beta),
$$

其中：

$$
X\sim\Gamma(\alpha,\lambda),\quad
Y\sim\Gamma(\beta,\lambda),\quad
X\perp Y.
$$

## 7. 选择分布的线索

- 独立重复成功次数：二项分布。
- 不放回抽样成功次数：超几何分布。
- 稀有事件计数：Poisson 分布。
- 等待首次成功次数：几何分布。
- 连续均匀随机点：均匀分布。
- 等待时间且有无记忆性：指数分布。
- 多个独立指数等待时间之和：Gamma 分布。
- 独立标准正态平方和：$\chi^2$ 分布。
- 大量独立小影响之和：正态分布。
- 标准正态比值：Cauchy 或 $t$ 分布。

