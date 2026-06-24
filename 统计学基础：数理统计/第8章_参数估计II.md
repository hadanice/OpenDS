# 第 8 章：参数估计 (Part II)

> 本文对应 `课件/8 EstimationⅡ.pdf`（复旦大学 孙新伟 老师 PPT）。
>
> 这一章是上一章（MLE、CRLB）的**理论深化**。如果说上一章在教你"怎么估计"，这一章就在告诉你"什么样的估计才好""数据里多少信息是真正有用的"。
>
> 四大板块：
> 1. **指数族（Exponential Family）**
> 2. **充分性（Sufficiency）**
> 3. **一致性（Consistency）**
> 4. **贝叶斯估计（Bayesian Estimation）**

---

## 0. 总览：为什么要学这些？

上一章我们学到：
- **MLE** 是个好估计方法
- **Fisher 信息**告诉我们参数能被估计得多准
- **CRLB** 给出了无偏估计方差的下界

但还有几个深刻的问题没回答：
- 拿到 $n$ 个样本，**有没有办法把它们浓缩成几个数字**而不丢失关于参数的信息？→ 充分性
- 一类长得"特别好看"的分布（Bernoulli、Normal、Poisson、Gamma...）有什么共同的好性质？→ 指数族
- 当样本量 $n\to\infty$，估计量会不会**收敛到真值**？→ 一致性
- 我**已有先验知识**怎么办？怎么把它和数据结合？→ 贝叶斯估计

---

## 1. 指数族（Exponential Family）

### 1.1 为什么要研究"指数族"？

观察一下我们见过的分布：

| 分布 | pdf 形式 |
|------|---------|
| Bernoulli | $p^x(1-p)^{1-x}$ |
| Poisson | $\dfrac{e^{-\lambda}\lambda^x}{x!}$ |
| Normal | $\dfrac{1}{\sqrt{2\pi}\sigma}e^{-(x-\mu)^2/(2\sigma^2)}$ |
| Gamma | $\dfrac{\lambda^r}{\Gamma(r)}x^{r-1}e^{-\lambda x}$ |

它们看起来形状各异，但**都可以写成同一种形式**：

$$
\boxed{f_\theta(x) = \exp\big\{\eta(\theta)^\top T(x) - \xi(\theta)\big\}\,h(x)}
$$

这就是"指数族"。把它们统一起来研究，能一次性证出很多深刻定理。

### 1.2 严格定义

**定义**：参数族 $\{P_\theta : \theta \in \Theta\}$ 称为**指数族**，若存在
- $T(x)$：随机 $p$ 维向量（**充分统计量**）
- $\eta(\theta)$：参数空间到 $\mathbb{R}^p$ 的映射（**自然参数函数**）
- $h(x) \ge 0$：和 $\theta$ 无关的函数
- $\xi(\theta)$：归一化常数（保证 pdf 积分为 1）

使得：
$$
f_\theta(x) = \exp\{\eta(\theta)^\top T(x) - \xi(\theta)\}h(x)
$$

其中 $\xi(\theta) = \log\int \exp\{\eta(\theta)^\top T(x)\}h(x)dx$。

### 1.3 自然参数化（Canonical Form）

最常见的**简化形式**：直接令 $\eta = \eta(\theta)$，把参数换成 $\eta$ 本身：

$$
f_\eta(x) = \exp\{\eta^\top T(x) - \zeta(\eta)\}h(x)
$$

- $\eta$：**自然参数（natural parameter）**
- $\Xi = \{\eta(\theta) : \theta\in\Theta\}$：**自然参数空间**
- 若 $\Xi$ 包含一个开集，称该指数族**满秩（full rank）**

> **直观**：自然参数化就是把分布按"最舒服的坐标"重写一遍。原参数 $\theta$（比如 Bernoulli 的 $\pi$）有 $0\le\pi\le 1$ 的约束，但换成 $\eta=\log\frac{\pi}{1-\pi}$（log-odds）就可以自由地在 $\mathbb{R}$ 里取值了。

### 1.4 例 1：Bernoulli

$$
p(x|\pi) = \pi^x(1-\pi)^{1-x}
= \exp\Big\{x\log\frac{\pi}{1-\pi} + \log(1-\pi)\Big\}
$$

对照定义：
- $\eta = \log\dfrac{\pi}{1-\pi}$（**logit/对数几率**）
- $T(x) = x$
- $\zeta(\eta) = -\log(1-\pi) = \log(1+e^\eta)$
- $h(x) = 1$

> **要点**：$\eta$ 和 $\pi$ 一一对应（$\pi = \dfrac{e^\eta}{1+e^\eta}$，正是 sigmoid！）。这就是逻辑回归的来源。

### 1.5 例 2：Poisson

$$
p(x|\lambda) = \frac{\lambda^x e^{-\lambda}}{x!} = \frac{1}{x!}\exp\{x\log\lambda - \lambda\}
$$

对照：
- $\eta = \log\lambda$
- $T(x) = x$
- $\zeta(\eta) = \lambda = e^\eta$
- $h(x) = 1/x!$

### 1.6 例 3：Normal $\mathcal{N}(\mu,\sigma^2)$

$$
p(x|\mu,\sigma^2) = \frac{1}{\sqrt{2\pi}}\exp\Big\{\frac{\mu}{\sigma^2}x - \frac{1}{2\sigma^2}x^2 - \frac{\mu^2}{2\sigma^2} - \log\sigma\Big\}
$$

对照（注意是 2 维参数）：
- $\eta = \big(\dfrac{\mu}{\sigma^2},\ -\dfrac{1}{2\sigma^2}\big)^\top$
- $T(x) = (x, x^2)^\top$
- $\zeta(\eta) = \dfrac{\mu^2}{2\sigma^2} + \log\sigma$
- $h(x) = \dfrac{1}{\sqrt{2\pi}}$

### 1.7 例 4：Multinomial（一个坑！）

朴素写法：
$$
p(x|\pi) = \frac{n!}{x_1!\cdots x_m!}\exp\Big\{\sum_{i=1}^m x_i\log\pi_i\Big\}
$$

但这样写**不是满秩**！因为约束 $\sum\pi_i = 1$，自然参数 $\eta = (\log\pi_1,\dots,\log\pi_m)$ 落在一个**低维流形**上，不含开集。

**修正**：消去最后一个 $\pi_m = 1 - \sum_{i=1}^{m-1}\pi_i$，把 multinomial 写成：

$$
p(x|\pi) = h(x)\exp\Big\{\sum_{i=1}^{m-1}\log\frac{\pi_i}{1-\sum_{j<m}\pi_j}\cdot x_i + n\log(1-\sum\pi_i)\Big\}
$$

这时：
- $\eta_i = \log\dfrac{\pi_i}{1-\sum_{j=1}^{m-1}\pi_j}$，$i=1,\dots,m-1$（softmax 的反函数！）
- $T(x) = (x_1,\dots,x_{m-1})$
- 现在 $\eta\in\mathbb{R}^{m-1}$ 自由，**满秩**

> **要点**：自然参数维度 = "真正的自由参数"个数。Multinomial 看起来 $m$ 维，实际只有 $m-1$ 个自由度。

### 1.8 矩生成函数（Moment Generating Function）

**定理**：自然参数化的指数族，若 $\eta_0$ 是 $\Xi$ 的内点，则 $T(X)$ 的 m.g.f. 在 $0$ 附近有限，且：

$$
\boxed{\psi_{\eta_0}(t) = \exp\{\zeta(\eta_0+t) - \zeta(\eta_0)\}}
$$

**证明**（很短，关键是用归一化条件）：
$$
\psi_{\eta_0}(t) = E[e^{t^\top T(X)}] = \int e^{t^\top T(x)}e^{\eta_0^\top T(x) - \zeta(\eta_0)}h(x)dx
$$
$$
= e^{-\zeta(\eta_0)}\int e^{(\eta_0+t)^\top T(x)}h(x)dx = e^{-\zeta(\eta_0)}\cdot e^{\zeta(\eta_0+t)}
$$

**推论**（极有用！）：

$$
\boxed{E[T(X)] = \frac{\partial\zeta}{\partial\eta},\quad \text{Var}(T(X)) = \frac{\partial^2\zeta}{\partial\eta\partial\eta^\top}}
$$

即：**对 $\zeta(\eta)$ 求一阶导得期望，求二阶导得方差**。

### 例：Bernoulli 验算

$\zeta(\eta) = \log(1+e^\eta)$。

$$
\frac{d\zeta}{d\eta} = \frac{e^\eta}{1+e^\eta} = \pi = E(X) \quad\checkmark
$$

$$
\frac{d^2\zeta}{d\eta^2} = \frac{e^\eta}{(1+e^\eta)^2} = \pi(1-\pi) = \text{Var}(X) \quad\checkmark
$$

> **回顾上一章**：$\text{Var}(T) = I(\eta)$（指数族里 Fisher 信息 = 充分统计量的方差），现在你知道为什么了：**因为 $I(\eta) = -E[\partial^2 \ln f/\partial\eta^2] = \partial^2\zeta/\partial\eta^2 = \text{Var}(T)$**。

---

## 2. 充分性（Sufficiency）

### 2.1 直觉：数据压缩不丢信息

假设你抛硬币 100 次，得到 100 个 0/1。如果有人问你 $p$ 大概是多少，你**不需要**报告完整序列，**只需要告诉对方"正面出现了几次"**就够了。

这就是充分性的精髓：**统计量 $T(X)$ 已经"吸收"了样本里关于 $\theta$ 的全部信息**。

### 2.2 严格定义

**定义**：统计量 $T(X)$ 称为**充分（sufficient）**的，若给定 $T$ 后，$X$ 的条件分布**与 $\theta$ 无关**：

$$
P(X = x \mid T(X) = t,\, \theta) = P(X = x \mid T(X) = t)
$$

> **解读**：知道了 $T$ 之后，原始数据 $X$ 不再带任何额外的关于 $\theta$ 的信息。$X$ 在给定 $T$ 时的"残余随机性"和参数无关。

### 2.3 例：二项的充分统计量

$X_1,\dots,X_n$ i.i.d. $\text{Bernoulli}(\theta)$，令 $T = \sum X_i$。

- 边际：$P(T = t) = \binom{n}{t}\theta^t(1-\theta)^{n-t}$
- 联合：$P(X = x, T = t) = \theta^t(1-\theta)^{n-t}$（当 $\sum x_i = t$）

条件分布：
$$
P(X = x \mid T = t) = \frac{\theta^t(1-\theta)^{n-t}}{\binom{n}{t}\theta^t(1-\theta)^{n-t}} = \frac{1}{\binom{n}{t}}
$$

**和 $\theta$ 完全无关**！所以 $T = \sum X_i$ 是充分统计量。

直观解释：知道有 $t$ 个正面后，所有"$t$ 个正面在哪几次出现"的排列方式都同样可能，与 $\theta$ 无关。

### 2.4 因子分解定理（Factorization Theorem）

**问题**：每次都用条件分布去验证太麻烦了。有没有更直接的判定方法？**有**——这是本章最重要的工具之一。

**定理**：$T(X)$ 充分 $\iff$ pdf 可以分解为：

$$
\boxed{f_\theta(x) = g_\theta(T(x))\cdot h(x)}
$$

其中：
- $g_\theta$：只通过 $T(x)$ 依赖于 $\theta$
- $h(x)$：完全不依赖 $\theta$

**用法**：拿到一个 pdf，看它如何随 $\theta$ 变化——能从 $x$ 中"剥离"出来一个量 $T(x)$ 使 $\theta$ 只通过它出现，那 $T$ 就是充分统计量。

### 2.5 推论：指数族的充分统计量

对指数族 $f_\theta(x) = \exp\{\eta(\theta)^\top T(x) - \xi(\theta)\}h(x)$，

**$T(X)$ 自然就是充分统计量**！（因为 $\theta$ 只通过 $T(x)$ 出现）

| 分布 | 充分统计量 |
|------|-----------|
| Bernoulli | $\sum X_i$ |
| Poisson | $\sum X_i$ |
| Normal | $(\sum X_i, \sum X_i^2)$ |
| Multinomial | 各类频数 |

### 2.6 例：截断族（Truncation Families）

$f_\theta(x) = c(\theta)\varphi(x)\mathbf{1}_{(a,b)}(x)$，$\theta = (a,b)$。

联合 pdf：
$$
\prod_{i=1}^n f_\theta(x_i) = [c(\theta)]^n \mathbf{1}_{(a,\infty)}(x_{(1)})\mathbf{1}_{(-\infty,b)}(x_{(n)}) \prod_{i=1}^n \varphi(x_i)
$$

按因子分解：$\theta$ 只通过 $(x_{(1)}, x_{(n)})$ 出现，所以 $T = (X_{(1)}, X_{(n)})$ 充分。

### 2.7 例：顺序统计量始终是充分的（弱意义）

对任意 i.i.d. 样本：
$$
\prod f(x_i) = \prod f(x_{(i)})
$$

所以 $T(X) = (X_{(1)}, \dots, X_{(n)})$ **总是充分的**——但这没什么压缩，等于把数据排了个序。

### 2.8 最小充分（Minimal Sufficient）

充分统计量不唯一。比如 $X$ 自己、$(X_{(1)},\dots,X_{(n)})$、$\sum X_i$ 对 Bernoulli 都充分，但**压缩程度不同**。

**定义**：$T$ 是**最小充分**，若对任何其他充分统计量 $S$，都存在函数 $\psi$ 使 $T = \psi(S)$ 几乎必然成立。

> **直觉**：最小充分 = 把数据压缩到不能再压缩，但仍保留所有 $\theta$ 信息。

### 2.9 辅助统计量（Ancillary Statistic）

**定义**：统计量 $V(X)$ 称为**辅助的（ancillary）**，若 $V$ 的分布**完全不依赖 $\theta$**。

**例**：$X_i \sim \mathcal{N}(\mu, 1)$，$V = X_1 - X_2 \sim \mathcal{N}(0, 2)$，与 $\mu$ 无关。

**意义**：辅助统计量"看不见 $\theta$"——它只反映分布的"形状特征"或"无关随机性"。

> **关键认识**：如果一个充分统计量 $T$ 的某个非常数函数是辅助的，说明 $T$ 里还混有"和 $\theta$ 无关的内容"——它没把数据压缩到极致。
>
> 真正"干净"的充分统计量应该满足：它的非常数函数都不能是辅助的。这就引出了**完备性**。

### 2.10 完备性（Completeness）

**定义**：统计量 $T$ 称为**完备**，若对任何 Borel 函数 $f$：

$$
E_\theta[f(T)] = 0,\ \forall\theta \implies f(T) = 0\ \text{a.s.}
$$

> **解读**：唯一能让 $T$ 的函数对所有 $\theta$ 期望为 0 的"诚实候选"，就是恒等于 0 的那个函数。换言之，$T$ 没有"虚假"的随机成分让 $E[f(T)]$ 偶然为 0。

**关键定理**：**完备 + 充分 ⟹ 最小充分**。

**指数族大定理**：满秩指数族里，自然 $T(X)$ 完备且充分。

### 2.11 例：Uniform $U(0,\theta)$ 的 $X_{(n)}$

$f_\theta(x) = \theta^{-n}\mathbf{1}_{[0,\theta]}(x_{(n)})$，所以 $X_{(n)}$ 充分（因子分解）。

证完备：$X_{(n)}$ 的 pdf 为 $nx^{n-1}/\theta^n$，$0\le x\le\theta$。

设 $E_\theta[f(X_{(n)})] = 0$，即
$$
\int_0^\theta f(x)\cdot \frac{nx^{n-1}}{\theta^n}dx = 0,\ \forall\theta > 0
$$

记 $G(\theta) = \int_0^\theta f(x)x^{n-1}dx$，则 $G(\theta) = 0$ 对所有 $\theta$ 成立。

求导：$G'(\theta) = f(\theta)\theta^{n-1} = 0$ ⟹ $f(\theta) = 0$（因为 $\theta > 0$）。

故 $X_{(n)}$ 完备。

### 2.12 Basu 定理（漂亮且实用！）

**定理**：设 $T$ 是**有界完备充分**统计量，$V$ 是**辅助**统计量，则 $T \perp V$（独立）。

**意义**：常用来"绕开"复杂的联合分布计算。

### 2.13 Basu 定理的经典应用：$\bar X$ 与 $S^2$ 独立

设 $X_1,\dots,X_n \sim \mathcal{N}(\mu,\sigma^2)$，**$\sigma$ 已知**：

- $\bar X$ 充分完备（指数族的）
- $S^2 = \dfrac{1}{n-1}\sum(X_i - \bar X)^2 = \dfrac{1}{n-1}\sum(Z_i - \bar Z)^2$ 其中 $Z_i = X_i - \mu \sim \mathcal{N}(0,\sigma^2)$ —— **不依赖 $\mu$**，所以是辅助统计量！
- 由 Basu 定理，**$\bar X \perp S^2$**

由于 $\sigma$ 任意，对一般 $\mathcal{N}(\mu, \sigma^2)$ 也成立。

**进一步**：用 m.g.f. 可推出 $(n-1)S^2/\sigma^2 \sim \chi^2_{n-1}$。

具体地：
$$
n\Big(\frac{\bar X - \mu}{\sigma}\Big)^2 + \frac{(n-1)S^2}{\sigma^2} = \sum_{i=1}^n \Big(\frac{X_i - \mu}{\sigma}\Big)^2 \sim \chi^2_n
$$

左边第一项 $\sim \chi^2_1$，且与 $S^2$ 独立。由 m.g.f.：
$$
\text{m.g.f. of }(n-1)S^2/\sigma^2 = \frac{(1-2t)^{-n/2}}{(1-2t)^{-1/2}} = (1-2t)^{-(n-1)/2}
$$

正是 $\chi^2_{n-1}$ 的 m.g.f.，证毕。

---

## 3. 一致性（Consistency）

### 3.1 直觉

无偏性是"平均行为"——估计量的期望等于真值。但即便无偏，它的方差可能大得离谱。

**一致性**问的是：当样本量 $n$ 越来越大，$\hat\theta_n$ 是不是会**越来越接近**真值 $\theta$？

### 3.2 严格定义

$\hat\theta_n$ 称为 $\theta$ 的**一致估计**，若**依概率收敛**到 $\theta$：

$$
\boxed{\forall\varepsilon > 0,\ \lim_{n\to\infty}P(|\hat\theta_n - \theta| < \varepsilon) = 1}
$$

记作 $\hat\theta_n \xrightarrow{p} \theta$。

> **直观**：随着 $n$ 增大，$\hat\theta_n$ "落在真值附近"的概率越来越高，最终趋于 1。

### 3.3 例 1：Uniform 的 $X_{(n)}$ 是一致的

$Y_1,\dots,Y_n \sim U(0,\theta)$，$\hat\theta_n = Y_{\max} = X_{(n)}$。

我们知道 $E(Y_{\max}) = \frac{n}{n+1}\theta$，**有偏**。但是否一致？

$Y_{\max}$ 的 pdf：$f_{Y_{\max}}(y) = ny^{n-1}/\theta^n$。

$$
P(|\hat\theta_n - \theta| < \varepsilon) = P(\theta - \varepsilon < Y_{\max} \le \theta) = \int_{\theta-\varepsilon}^\theta \frac{ny^{n-1}}{\theta^n}dy
$$
$$
= \Big[\frac{y^n}{\theta^n}\Big]_{\theta-\varepsilon}^\theta = 1 - \Big(\frac{\theta-\varepsilon}{\theta}\Big)^n
$$

由于 $(\theta-\varepsilon)/\theta < 1$，$n\to\infty$ 时收敛到 0。所以：

$$
\lim_{n\to\infty}P(|\hat\theta_n - \theta| < \varepsilon) = 1 - 0 = 1
$$

✅ **$Y_{\max}$ 一致（虽然有偏）**。

### 3.4 工具：Chebyshev / Markov 不等式

**Markov 不等式**：$X \ge 0$，$t > 0$：
$$
P(X \ge t) \le \frac{E[X]}{t}
$$
更一般地，对 $p > 0$：
$$
P(|X| \ge t) \le \frac{E|X|^p}{t^p}
$$

**Chebyshev 不等式**（$\varphi$ 非负不减偶函数）：
$$
\varphi(t)P(|X| \ge t) \le E[\varphi(X)]
$$

最常用形式（取 $\varphi(x)=x^2$）：
$$
\boxed{P(|X - \mu| \ge t) \le \frac{\text{Var}(X)}{t^2}}
$$

### 3.5 例 2：样本均值是一致的

$X_1,\dots,X_n$ i.i.d.，$E(X) = \mu$，$\text{Var}(X) = \sigma^2 < \infty$。

$\hat\mu_n = \bar X$，则 $E(\hat\mu_n) = \mu$，$\text{Var}(\hat\mu_n) = \sigma^2/n$。

由 Chebyshev：
$$
P(|\hat\mu_n - \mu| < \varepsilon) \ge 1 - \frac{\sigma^2/n}{\varepsilon^2} = 1 - \frac{\sigma^2}{n\varepsilon^2}
$$

$n\to\infty$ 时右边趋于 1。✅ **$\bar X$ 是 $\mu$ 的一致估计**（这就是**弱大数定律**！）。

> **要点**：方差有限 + 渐近无偏 ⟹ 一致。

### 3.6 MLE 的一致性与渐近最优性

接下来这部分是 **本章最深的理论**。我们已知：
- MLE 不一定无偏
- CRLB 给出无偏估计的方差下界 $1/I(\theta)$

**核心问题**：MLE 在大样本下表现如何？

### 3.7 渐近正态性 + 渐近最优性

**定义**：估计量序列 $\{\hat\theta_n\}$ 称为**渐近正态**，若存在正定矩阵 $V_n(\theta)$ 使得：

$$
[V_n(\theta)]^{-1/2}(\hat\theta_n - \theta) \xrightarrow{d} \mathcal{N}_k(0, I_k)
$$

- $V_n(\theta)$ 是渐近协方差矩阵
- 若 $V_{1n}(\theta) \le V_{2n}(\theta)$，则 $\hat\theta_{1n}$ **渐近上更有效**

**渐近最优**的定义：

$$
\boxed{\hat\theta_n\text{ 渐近最优}\iff V_n(\theta) = [I_n(\theta)]^{-1}}
$$

即渐近方差**达到 CRLB 的极限**。

### 3.8 关键定理（MLE 渐近最优）

**定理（粗略版）**：在合适的正则性条件下：

1. 似然方程 $s_n(\hat\theta_n) := \dfrac{\partial \ell}{\partial\theta}(\hat\theta_n) = 0$ 存在解，且 $\hat\theta_n \xrightarrow{p}\theta$（一致）；
2. 任何**一致**的似然方程根 $\tilde\theta_n$ 都是**渐近最优**的，即
   $$
   \sqrt n(\tilde\theta_n - \theta) \xrightarrow{d}\mathcal{N}\big(0,\, I_1(\theta)^{-1}\big)
   $$

> **意义重大**：MLE 在大样本下不仅一致，而且**自动达到 CRLB**。这就是 MLE 在统计学里地位如此之高的根本原因。

### 3.9 参数变换下的渐近性

若想估计 $\vartheta = g(\theta)$，用 $\hat\vartheta_n = g(\hat\theta_n)$，由**Delta 方法**：

$$
\sqrt n(\hat\vartheta_n - \vartheta) \xrightarrow{d}\mathcal{N}\big(0,\, [\nabla g(\theta)]^\top V(\theta)\nabla g(\theta)\big)
$$

并且
$$
[\nabla g]^\top V \nabla g \ge [\bar I_n(\vartheta)]^{-1}
$$

——同样达到 CRLB 极限。

---

## 4. 贝叶斯估计（Bayesian Estimation）

### 4.1 频率派 vs. 贝叶斯派

|       | 频率派（之前学的） | 贝叶斯派 |
|-------|-------------------|----------|
| 参数 $\theta$ | **未知常数** | **随机变量** |
| 出发点 | 似然 $f(x|\theta)$ | 先验 $\pi(\theta)$ + 似然 |
| 推理基础 | "重复实验下的频率" | "更新主观信念" |
| 输出 | 点估计 + CI | 后验分布 |

### 4.2 故事：寻找失踪的核潜艇

1968 年 USS Scorpion 核潜艇失踪。海军专家 John Craven 把可能区域分成 $n$ 格，让老潜艇长们先**主观估计**每格的概率 $P(A_1),\dots,P(A_n)$（**先验**）。

按概率最大的区域 $k$ 搜索，**没找到**。怎么办？

由 Bayes 定理：
$$
P(A_k | B_k^c) = \frac{P(B_k^c | A_k)P(A_k)}{P(B_k^c | A_k)P(A_k) + P(B_k^c | A_k^c)P(A_k^c)}
$$

更新后得到新概率 $P^*(A_k) < P(A_k)$（搜索失败降低了它的可信度），其他 $P^*(A_i)$ 也要重新归一化，再选最大的搜下一块。

最终在 Azores 附近找到了。**这就是贝叶斯方法的实战范例**。

### 4.3 简单例子：Poisson 参数

某话务中心 5 分钟来电 $X \sim \text{Poisson}(\Lambda)$。历史经验：

$$
P(\Lambda = 8) = 0.25,\quad P(\Lambda = 10) = 0.75
$$

这是**离散先验**。现在观察 $X = 7$，求**后验**。

$$
P(\Lambda = 10 | X = 7) = \frac{P(X = 7|\Lambda = 10)\cdot 0.75}{P(X=7|\Lambda=8)\cdot 0.25 + P(X=7|\Lambda=10)\cdot 0.75}
$$
$$
= \frac{(0.090)(0.75)}{(0.140)(0.25) + (0.090)(0.75)} \approx 0.659
$$

所以 $P(\Lambda = 8 | X = 7) = 0.341$。

**对比**：先验 $P(\Lambda = 10) = 0.75$ → 后验 $0.659$。观察 $X = 7$（比较小）后，对"$\Lambda$ 等于较大的 10"的信念**减弱了**，对"较小 8"的信念**加强了**。这正是贝叶斯更新的精髓。

### 4.4 后验分布的一般公式

**定义**：先验 $\pi(\theta)$、似然 $f(w|\theta)$，则**后验**：

$$
\boxed{g(\theta|w) = \frac{f(w|\theta)\pi(\theta)}{\int f(w|\theta)\pi(\theta)d\theta}}
$$

口诀：**后验 ∝ 似然 × 先验**。

分母 $\int f(w|\theta)\pi(\theta)d\theta = m(w)$ 称为**边际似然**或 evidence，仅起归一化作用。

### 4.5 例：Beta + Binomial（共轭！）

Max 想估计销售比例 $\theta$。

**模型**：$X | \theta \sim \text{Binomial}(n, \theta)$。

**先验**：基于经验，$\theta$ 大概在 0.035 附近，不超过 0.07。选 **Beta 分布**：
$$
\pi(\theta) = \frac{\Gamma(r+s)}{\Gamma(r)\Gamma(s)}\theta^{r-1}(1-\theta)^{s-1}
$$

观察 $X = k$，**后验**：

$$
g(\theta|k) \propto \binom{n}{k}\theta^k(1-\theta)^{n-k}\cdot \theta^{r-1}(1-\theta)^{s-1}
$$
$$
= \theta^{k+r-1}(1-\theta)^{n-k+s-1}\cdot\text{const}
$$

这恰好是 **Beta($k+r, n-k+s$)** 的核！所以

$$
\boxed{\theta | X = k \sim \text{Beta}(k+r,\, n-k+s)}
$$

> **共轭先验（conjugate prior）**：先验和后验属于**同一族分布**。Beta 是 Binomial 的共轭。这让计算异常简洁。
>
> 取 $r = 4, s = 102$ 满足 Max 的要求：$E[\theta] = 4/106 \approx 0.038$，且大部分质量在 $0.07$ 左侧。

### 4.6 例：Gamma + Poisson（也是共轭！）

$X_i \sim \text{Poisson}(\theta)$ i.i.d.，$W = \sum X_i \sim \text{Poisson}(n\theta)$。

**先验**：Gamma 分布
$$
\pi(\theta) = \frac{\mu^s}{\Gamma(s)}\theta^{s-1}e^{-\mu\theta}
$$

**后验**：
$$
g(\theta|w) \propto \frac{(n\theta)^w e^{-n\theta}}{w!}\cdot \theta^{s-1}e^{-\mu\theta} \propto \theta^{w+s-1}e^{-(\mu+n)\theta}
$$

即 **Gamma($w+s, \mu+n$)**！

> 飓风预测案例：$n = 100$ 年里观测 $w = 164$ 次，先验取 $s=88, \mu=50$，后验为 Gamma(252, 150)。

### 4.7 边际分布（Marginal）

有时候关心的不是 $\theta$，而是 $W$ 的"无条件分布":

$$
m(w) = \int g(w,\theta)d\theta = \int f(w|\theta)\pi(\theta)d\theta
$$

**例**：Poisson 似然 + Gamma 先验：
$$
m(w) = \int_0^\infty \frac{1}{w!}\frac{\mu^s}{\Gamma(s)}\theta^{w+s-1}e^{-(\mu+1)\theta}d\theta
$$
$$
= \frac{\Gamma(w+s)}{w!\Gamma(s)}\Big(\frac{\mu}{\mu+1}\Big)^s\Big(\frac{1}{\mu+1}\Big)^w
$$

这是**负二项分布**！这解释了为什么"Poisson + Gamma 异质性 → 负二项"——心理学错误率、保险索赔次数等都是这种结构。

### 4.8 贝叶斯点估计：损失函数 + 风险

后验是个**分布**，怎样从中提取一个**点**作为估计？

**定义**：损失函数 $L(\hat\theta, \theta) \ge 0$，$L(\theta,\theta) = 0$。

**风险（risk）** = 损失关于**后验分布**的期望：

$$
\boxed{R(\hat\theta) = E_{\theta|w}[L(\hat\theta, \theta)] = \int L(\hat\theta, \theta)g(\theta|w)d\theta}
$$

**Bayes 估计** = 使风险最小的 $\hat\theta$。

### 4.9 两个最重要的损失函数

**定理**：

| 损失 $L(\hat\theta, \theta)$ | Bayes 估计 |
|------------------------------|------------|
| $|\hat\theta - \theta|$（绝对损失） | 后验**中位数** |
| $(\hat\theta - \theta)^2$（平方损失） | 后验**均值** |

**平方损失证明**（极简）：

$$
E(W - b)^2 = E[(W-\mu) + (\mu - b)]^2 = \text{Var}(W) + (\mu - b)^2
$$

显然在 $b = \mu$ 时最小。所以 Bayes 估计 = 后验均值。

**绝对损失证明**（思路）：

设 $W$ 的中位数为 $m$。
$$
E|W - m| = \int_{-\infty}^m (m-w)f(w)dw + \int_m^\infty (w-m)f(w)dw
$$

利用中位数的性质 $\int_{-\infty}^m f = \int_m^\infty f = 1/2$，可以证明 $E|W - m| \le E|W - b|$ 对任何 $b$ 成立。

### 4.10 例：Poisson + Gamma 的 Bayes 估计

后验是 Gamma$(w+s, \mu+n)$，均值 $= \dfrac{w+s}{\mu+n}$。

**平方损失下** Bayes 估计：

$$
\boxed{\hat\theta_{\text{Bayes}} = \frac{w + s}{\mu + n}}
$$

**关键观察**：把它分解一下：

$$
\frac{w+s}{\mu+n} = \frac{n}{\mu+n}\cdot\underbrace{\frac{w}{n}}_{\text{MLE}} + \frac{\mu}{\mu+n}\cdot\underbrace{\frac{s}{\mu}}_{\text{先验均值}}
$$

这是**MLE 和先验均值的加权平均**！

- $n$ 大（数据多）→ 偏向 MLE
- $\mu$ 大（先验"权威"）→ 偏向先验
- $n\to\infty$ → Bayes 估计 → MLE（**数据淹没先验**）

> **这是贝叶斯方法的精髓**：先验提供初始信念，数据不断更新，最终被数据"主导"。先验"假数据量"为 $\mu$，真实数据量为 $n$，按比例混合。

### 4.11 例：Max 的库存问题（非对称损失）

Max 估计 $\hat\theta$，准备 $n\hat\theta$ 张盗版。

- 若 $\hat\theta < \theta$：少备货 $n(\theta - \hat\theta)$ 张，每张损失 $c$ 元
- 若 $\hat\theta > \theta$：多备货 $n(\hat\theta - \theta)$ 张，每张存储费 $d$ 元

$$
L(\hat\theta, \theta) = \begin{cases}cn(\theta - \hat\theta) & \hat\theta < \theta\\ dn(\hat\theta - \theta) & \hat\theta > \theta\end{cases}
$$

这是**非对称损失**。最优 $\hat\theta$ 是后验分布的某个**分位点**（具体是 $c/(c+d)$ 分位点）。

> **意义**：贝叶斯框架很灵活——你可以根据问题的实际经济损失来设计损失函数，得到针对性的最优决策。

---

## 5. 知识体系总览

```
                        参数估计 II
                            |
        ┌────────────┬──────┴───┬────────────────┐
        |            |          |                |
     指数族        充分性     一致性          贝叶斯估计
        |            |          |                |
   ┌────┼────┐   ┌──┼──┐   ┌──┼──┐         ┌──┼──┐
  定义 自然 各分  充分 因子 完备  依概率  Cheb./   先验 后验  Bayes
       参数 布例  统计 分解 性    收敛  Markov   ↓    ↓    估计
                  量   定理            (MLE)   π(θ) g(θ|x) (loss)
                       Basu             ↓               平方→均值
                      ✓ X̄⊥S²       渐近最优        绝对→中位数
                                    (达到CRLB)
```

---

## 6. 易错点与考点

| 误区 | 正确认识 |
|------|----------|
| 充分统计量唯一 | 不！样本本身、顺序统计量都充分。**最小**充分才唯一（等价类） |
| 充分 ⇒ 完备 | 错！需要单独验证完备性 |
| 完备 ⇒ 充分 | 错！是两个独立概念 |
| MLE 总是最优 | 在**大样本**下渐近最优，小样本不一定 |
| 一致 ⇒ 无偏 | 错！$Y_{\max}$ 有偏但一致 |
| 无偏 ⇒ 一致 | 错！需要方差也要趋于 0 |
| 共轭先验是唯一选择 | 不！只是计算方便。但任何先验都合法 |
| Bayes 估计就是后验均值 | 不！取决于损失函数 |
| 数据多了就不需要先验 | 对，$n\to\infty$ 时先验被数据淹没 |

---

## 7. 关键公式速查表

| 内容 | 公式 |
|------|------|
| 指数族 | $f_\theta(x) = \exp\{\eta(\theta)^\top T(x) - \xi(\theta)\}h(x)$ |
| 自然形式 | $f_\eta(x) = \exp\{\eta^\top T(x) - \zeta(\eta)\}h(x)$ |
| m.g.f. | $\psi_\eta(t) = \exp\{\zeta(\eta+t) - \zeta(\eta)\}$ |
| $E[T]$ | $\partial\zeta/\partial\eta$ |
| $\text{Var}[T]$ | $\partial^2\zeta/\partial\eta\partial\eta^\top = I(\eta)$ |
| 因子分解定理 | $f_\theta(x) = g_\theta(T(x))h(x) \iff T$ 充分 |
| 完备性 | $E_\theta[f(T)] = 0\ \forall\theta\implies f(T) = 0$ |
| Basu 定理 | 完备充分 $\perp$ 辅助 |
| 一致性 | $\lim_n P(|\hat\theta_n - \theta| < \varepsilon) = 1$ |
| Chebyshev | $P(|X - \mu| \ge t) \le \text{Var}(X)/t^2$ |
| MLE 渐近 | $\sqrt n(\hat\theta_n - \theta)\xrightarrow{d}\mathcal{N}(0, I_1^{-1})$ |
| Bayes 后验 | $g(\theta|x) \propto f(x|\theta)\pi(\theta)$ |
| 平方损失 → | 后验均值 |
| 绝对损失 → | 后验中位数 |
| Beta/Binomial | $\theta|k \sim\text{Beta}(k+r,\, n-k+s)$ |
| Gamma/Poisson | $\theta|w \sim\text{Gamma}(w+s,\, \mu+n)$ |

---

## 8. 学习路径建议

这一章理论密度高，建议按以下顺序消化：

**第一遍（混个脸熟）**：
1. 看懂指数族的统一形式，确认 Bernoulli/Poisson/Normal 都能套进去
2. 理解充分性的直觉（"压缩不丢信息"），背下因子分解定理
3. 一致性 = 弱大数定律的精神
4. 贝叶斯就是 "先验 × 似然 ∝ 后验"

**第二遍（推导）**：
1. 自己推一遍 Bernoulli 的指数族表达，验证 $E[T] = \pi$、$\text{Var}[T] = \pi(1-\pi)$
2. 自己用因子分解证明 Bernoulli/$\sum X_i$ 充分
3. 自己用 Chebyshev 推 $\bar X$ 一致
4. 自己推 Beta + Binomial → Beta 后验

**第三遍（理论的味道）**：
1. 完备性的"代数对偶性"——为什么"$E[f(T)]=0\Rightarrow f=0$" 等价于"没有冗余"
2. Basu 定理为什么成立的几何直觉（"完备充分"和"辅助"是正交方向）
3. MLE 渐近最优 = "大样本下达到 CRLB"
4. Bayes 估计 = MLE + 先验加权平均（共轭情况下）

---

## 9. 与上一章的对照

| 上一章 (MLE/CRLB) | 本章 (扩展) |
|------------------|------------|
| MLE 怎么算 | MLE 在大样本下渐近最优 |
| Fisher 信息 $I(\theta)$ | 在指数族里 $I(\eta) = \text{Var}(T)$ |
| CRLB 给方差下界 | MLE 渐近达到 CRLB |
| 无偏性 | 一致性（更弱但更有用） |
| 频率派点估计 | 贝叶斯估计（用先验） |
| 没说"哪些数据有用" | 充分性告诉你"全部有用信息浓缩在 $T(X)$" |
| 没强调分布的统一结构 | 指数族给出统一框架 |

如果某一节还卡，告诉我具体页码或概念，我可以再展开讲。祝学习顺利！

---

## 10. PPT 级补充：指数族的结构化读法

指数族的一般形式可写为

$$
f(y;\eta)=h(y)c(\eta)\exp\left\{\sum_{j=1}^k Q_j(\eta)T_j(y)\right\}.
$$

更常见的自然参数形式是

$$
f(y;\eta)=h(y)\exp\{\eta^\top T(y)-A(\eta)\}.
$$

这里每一部分都有角色：

| 符号 | 作用 |
|------|------|
| $h(y)$ | 与参数无关的基准测度 |
| $\eta$ | 自然参数 |
| $T(y)$ | 自然统计量 |
| $A(\eta)$ | log normalizer，保证积分为 1 |

### 10.1 Bernoulli 例子

Bernoulli pmf 为

$$
p(y;\pi)=\pi^y(1-\pi)^{1-y},\qquad y=0,1.
$$

改写：

$$
p(y;\pi)=\exp\left\{
y\log\frac{\pi}{1-\pi}
+\log(1-\pi)
\right\}.
$$

因此自然参数是

$$
\eta=\log\frac{\pi}{1-\pi},
$$

自然统计量是

$$
T(y)=y,
$$

log normalizer 为

$$
A(\eta)=\log(1+e^\eta).
$$

并且

$$
E_\eta[T(Y)]=A'(\eta),\qquad
\operatorname{Var}_\eta(T(Y))=A''(\eta).
$$

### 10.2 Poisson 例子

Poisson pmf：

$$
p(y;\lambda)=e^{-\lambda}\frac{\lambda^y}{y!}
=\frac1{y!}\exp\{y\log\lambda-\lambda\}.
$$

自然参数：

$$
\eta=\log\lambda.
$$

于是

$$
A(\eta)=e^\eta,
$$

所以

$$
E(Y)=A'(\eta)=e^\eta=\lambda,
$$

$$
\operatorname{Var}(Y)=A''(\eta)=e^\eta=\lambda.
$$

### 10.3 Normal 均值例子

若 $\sigma^2$ 已知，

$$
Y\sim N(\mu,\sigma^2).
$$

密度可写为

$$
f(y;\mu)
=\frac1{\sqrt{2\pi}\sigma}
\exp\left\{
-\frac{y^2}{2\sigma^2}
+\frac{\mu}{\sigma^2}y
-\frac{\mu^2}{2\sigma^2}
\right\}.
$$

自然参数为

$$
\eta=\frac{\mu}{\sigma^2},
$$

自然统计量为

$$
T(y)=y.
$$

这说明很多熟悉分布其实都共享同一套指数族结构。

---

## 11. PPT 级补充：充分性、因子分解与信息压缩

充分统计量回答的问题是：关于参数 $\theta$，数据中哪些信息是必要且足够的？

### 11.1 因子分解定理

统计量 $T(Y)$ 对 $\theta$ 充分，当且仅当联合密度可写为

$$
f(y;\theta)=g(T(y),\theta)h(y).
$$

其中 $h(y)$ 不含 $\theta$。这表示参数相关部分只通过 $T(y)$ 依赖数据。

### 11.2 Bernoulli 样本

若

$$
Y_i\sim Bernoulli(\pi),
$$

联合 pmf 为

$$
L(\pi)=\pi^{\sum y_i}(1-\pi)^{n-\sum y_i}.
$$

因此

$$
T(Y)=\sum_{i=1}^nY_i
$$

是充分统计量。

解释：只要知道成功次数，样本的具体排列顺序对 $\pi$ 没有额外信息。

### 11.3 Normal 样本

若

$$
Y_i\sim N(\mu,\sigma^2)
$$

且两个参数都未知，联合密度中的参数相关部分可通过

$$
\sum Y_i,\qquad \sum Y_i^2
$$

表达，因此

$$
T(Y)=\left(\sum Y_i,\sum Y_i^2\right)
$$

是充分统计量。

等价地，也可用

$$
(\bar Y,S^2)
$$

表达。

### 11.4 最小充分性的直觉

充分统计量可能不唯一。最小充分统计量是“不能再压缩而不损失参数信息”的统计量。

直觉：

1. $Y_1,\dots,Y_n$ 包含所有原始信息；
2. 充分统计量保留所有关于参数的信息；
3. 最小充分统计量去掉与参数无关的冗余。

---

## 12. PPT 级补充：一致性、渐近正态与 MLE

### 12.1 一致性的检查思路

估计量 $\hat\theta_n$ 一致表示

$$
\hat\theta_n\to_p\theta.
$$

常用证明路线：

1. 写出估计量；
2. 用 LLN 说明样本均值或样本矩收敛到总体矩；
3. 用连续映射定理得到参数函数的收敛。

方法矩估计尤其适合这个套路。

### 12.2 MLE 一致性的直觉

MLE 最大化样本平均 log-likelihood：

$$
\frac1n\ell_n(\theta)=\frac1n\sum_{i=1}^n\log f(Y_i;\theta).
$$

由 LLN，它会接近

$$
E_{\theta_0}[\log f(Y;\theta)].
$$

在可识别条件下，这个期望在真实参数 $\theta_0$ 处最大，因此 MLE 会靠近 $\theta_0$。

### 12.3 MLE 渐近正态

在正则条件下，

$$
\sqrt n(\hat\theta-\theta_0)
\to_d
N(0,I_1(\theta_0)^{-1}).
$$

多参数情形为

$$
\sqrt n(\hat\theta-\theta_0)
\to_d
N_p(0,I_1(\theta_0)^{-1}).
$$

这条结论连接：

1. 第 6 章 CLT；
2. 第 7 章 Fisher 信息；
3. 本章 MLE 渐近最优；
4. 后续回归参数的渐近推断。

---

## 13. PPT 级补充：完备性、Basu 与 UMVU

### 13.1 完备性的含义

统计量 $T$ 完备表示：如果

$$
E_\theta[g(T)]=0
$$

对所有 $\theta$ 都成立，则

$$
P_\theta(g(T)=0)=1
$$

对所有 $\theta$ 成立。

直觉是：$T$ 的函数中不存在一个“对所有参数均值都为 0 但自身不为 0”的隐藏冗余方向。

### 13.2 完备充分统计量为什么重要

Lehmann-Scheffe 定理说：若 $T$ 是完备充分统计量，且 $\delta(T)$ 是 $g(\theta)$ 的无偏估计量，则 $\delta(T)$ 是唯一的 UMVU 估计量。

这把几个概念串起来：

| 概念 | 作用 |
|------|------|
| 充分 | 不丢参数信息 |
| 完备 | 不含无用冗余 |
| 无偏 | 目标正确 |
| UMVU | 在无偏类中方差最小 |

### 13.3 Basu 定理的直觉

Basu 定理：完备充分统计量与任何辅助统计量独立。

辅助统计量的分布不依赖参数。直觉上，完备充分统计量承载全部参数信息，而辅助统计量不含参数信息，两者方向正交，因此独立。

经典例子：正态样本中，$\bar Y$ 与标准化残差方向独立。

---

## 14. PPT 级补充：贝叶斯估计的计算模板

贝叶斯推断的核心公式：

$$
\pi(\theta\mid y)
\propto
L(\theta;y)\pi(\theta).
$$

后验 = 似然 × 先验，再归一化。

### 14.1 Beta-Binomial

若

$$
Y\mid p\sim Bin(n,p),
$$

先验

$$
p\sim Beta(\alpha,\beta),
$$

则后验为

$$
p\mid y\sim Beta(\alpha+y,\beta+n-y).
$$

后验均值：

$$
E(p\mid y)=\frac{\alpha+y}{\alpha+\beta+n}.
$$

可以写成先验均值和样本比例的加权平均。

### 14.2 Gamma-Poisson

若

$$
Y_i\mid\lambda\sim Poisson(\lambda),
$$

先验

$$
\lambda\sim Gamma(\alpha,\beta)
$$

其中 $\beta$ 是 rate，则后验为

$$
\lambda\mid y\sim Gamma\left(\alpha+\sum y_i,\beta+n\right).
$$

### 14.3 Bayes estimator

在平方损失下，Bayes 估计量是后验均值：

$$
\hat\theta_B=E(\theta\mid y).
$$

在绝对损失下，Bayes 估计量是后验中位数。

在 0-1 损失或 MAP 思路下，常看后验众数。

---

## 15. 本章 PPT 对照复习清单

| PPT 内容 | 复习时要能做到 |
|----------|----------------|
| 指数族形式 | 会识别 $h(y),\eta,T(y),A(\eta)$ |
| Bernoulli 指数族 | 会推出 logit 自然参数 |
| Poisson 指数族 | 会由 $A'(\eta),A''(\eta)$ 得均值方差 |
| Normal 指数族 | 知道固定方差时自然统计量是 $Y$ |
| 因子分解 | 会证明 Bernoulli 的 $\sum Y_i$ 充分 |
| Normal 充分统计量 | 会写 $(\sum Y_i,\sum Y_i^2)$ |
| 一致性 | 会用 LLN + 连续映射证明 |
| MLE 渐近正态 | 能和 Fisher 信息联系 |
| 完备性 | 能解释“无冗余”的含义 |
| Lehmann-Scheffe | 知道完备充分 + 无偏推出 UMVU |
| Basu 定理 | 理解完备充分与辅助统计量独立 |
| Bayes 后验 | 会写 posterior proportional to likelihood times prior |
| 共轭先验 | 会推 Beta-Binomial 和 Gamma-Poisson |
