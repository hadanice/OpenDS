# 最优化课程学习总览（Lecture 2 – Lecture 10）

> 本系列笔记覆盖凸优化课程从"凸性基础"到"一阶/二阶/不可微算法"的主线内容（对应 note 2 ~ note 10）。
> 阅读建议：先把本文看完，建立宏观地图，再按章节顺序学习。

## 一、课程的"主线故事"

最优化课程有一条非常清晰的逻辑链，可以用一句话概括：

> **先用"凸性"为问题画一个安全区 → 在安全区里用"最优性条件"刻画解 → 通过"对偶"换一个角度看问题 → 用"算法"把解算出来。**

具体到本课程：

| 章    | 名字     | 它在解决什么问题              | 它输出了什么                                                            |
| ---- | ------ | --------------------- | ----------------------------------------------------------------- |
| Ch 2 | 凸集与凸函数 | 什么样的几何对象是"友好"的？       | 一套判定凸性的工具（运算保凸 + 一阶/二阶条件 + 共轭/次梯度）                                |
| Ch 3 | 凸优化问题  | 把实际问题"改写"成可处理的标准形式    | LP、QP、QCQP、SOCP、SDP 五大模板及其等价转换                                    |
| Ch 4 | 最优性条件  | 什么样的点 $x^*$ 才是最优解     | FJ 条件、KKT 条件（必要 + 凸下充分）                                           |
| Ch 5 | 拉格朗日对偶 | 把"难解的原问题"变成"凸的对偶问题"   | 弱/强对偶、Slater、saddle point、共轭对偶、CLP/SDP 对偶                         |
| Ch 6 | 梯度下降   | 光滑问题最基础的一阶算法怎么分析      | GD、Armijo、L-smooth/strongly convex 收敛率                            |
| Ch 7 | 牛顿法    | 如何利用 Hessian 快速求解光滑问题 | Newton direction、decrement、damped/inexact Newton、self-concordance |
| Ch 8 | 拟牛顿法   | Hessian 太贵时如何近似二阶信息   | Secant equation、Wolfe、BFGS、L-BFGS、BB、Gauss-Newton                 |
| Ch 9 | 次梯度法   | 不可微凸函数如何写最优性条件和算法     | $\partial f$、nonsmooth KKT、projected subgradient、mirror descent   |
| Ch10 | 近端梯度法  | $g+h$ 结构下如何比次梯度法更快    | prox、gradient mapping、PGM、ISTA/FISTA、$O(1/k)$ 与 $O(1/k^2)$        |

第 4、5 章是同一个故事的两面：**KKT 条件就是 Lagrangian 鞍点条件**。第 6–10 章回答"怎么把解算出来"：光滑问题先用 GD/Newton/BFGS，不可微问题用 subgradient 或 prox；能利用结构时，prox 通常比普通次梯度法更高效。

## 二、知识依赖图

```
                 Ch2: 凸集 ─────────┐
                   │                │
                   ▼                ▼
                 Ch2: 凸函数 ────► Ch3: 凸优化问题模板
                   │                │
                   │  (一阶条件 / 共轭函数 / 次梯度)
                   ▼                ▼
                 Ch4: 最优性条件 (FJ → KKT)
                   │                │
                   │  (Lagrangian)  │
                   ▼                ▼
                 Ch5: 对偶（弱/强、saddle、共轭对偶、CLP/SDP）
                                    │
                                    │  (优化算法的目标函数)
                                    ▼
                 Ch6: 梯度下降（L-smooth / 强凸 / Armijo）
                                    │
                 ┌──────────────────┼──────────────────┐
                 ▼                  ▼                  ▼
          Ch7: Newton        Ch8: Quasi-Newton   Ch9: Subgradient
                 │                  │                  │
                 └──────────────┬───┘                  ▼
                                ▼                Ch10: Proximal Gradient
                         大规模数值算法             composite nonsmooth
```

**关键箭头**：
- Ch2 → Ch3：凸性是"凸优化问题"的定义。
- Ch2 一阶条件 + Ch4 KKT → Ch5 saddle point。
- Ch2 共轭函数 → Ch5 Fenchel 对偶。
- Ch2 强凸 / Lipschitz → Ch6 收敛率分析。
- Ch6 二次上界 / Armijo → Ch7 阻尼 Newton 与 Ch10 PGM 线搜索。
- Ch7 Newton system → Ch8 BFGS/L-BFGS 用 secant equation 近似二阶信息。
- Ch2 次梯度 → Ch9 不可微最优性条件 → Ch10 prox 与 gradient mapping。

## 三、按章节的核心"硬核工具"

这张表是考试和作业最常用的"工具箱"，遇到任何题目你都应该能立刻匹配到对应工具。

| 工具                                                       | 出处                    | 典型用法                                  |
| -------------------------------------------------------- | --------------------- | ------------------------------------- |
| **凸性保持运算**（交、仿射、透视、线性分式）                                 | Ch2 §1.2              | 判定一个集合是否凸                             |
| **凸函数运算法则**（非负组合、点态上确界、仿射复合、单调复合、最小化、透视）                 | Ch2 Thm 2.7           | 判定一个函数是否凸                             |
| **一阶条件** $f(y)\ge f(x)+\nabla f(x)^T(y-x)$               | Ch2 Thm 2.10          | 与 $\nabla^2 f \succeq 0$ 等价；推 KKT 充分性 |
| **二阶条件** $\nabla^2 f \succeq 0$                          | Ch2 Thm 2.11          | 大多数判凸题首选                              |
| **Schur 补**                                              | Ch2 Ex 2.12           | 把"分式/二次型"塞进 SDP/SOCP                  |
| **标准形改写**（引入松弛、x⁺-x⁻、log-sum-exp、第二阶锥技巧）                 | Ch3 §2                | LP/QP/SOCP 建模                         |
| **FJ 条件 / KKT 条件 / Slater 条件**                           | Ch4 Thm 3.1, 3.2, 3.4 | 求最优解、判定正则性                            |
| **Lagrangian 与对偶函数** $\theta(\lambda,\nu)=\inf_x L$      | Ch5 (D)               | 对偶推导第一步永远是写 L                         |
| **共轭函数** $f^*(y)=\sup_x(y^T x-f(x))$                     | Ch2 Def 2.4 + Ch5 §1  | Fenchel 对偶、LASSO/正则化对偶                |
| **proper cone & dual cone**                              | Ch5 §2.1              | 写 CLP/SDP/SOCP 的对偶                    |
| **Lipschitz 梯度（L-smooth）**                               | Ch6 Lemma 1.2         | 二次上界 → "充分下降"引理                       |
| **强凸（μ-strongly convex）**                                | Ch6 Def 1.11          | 二次下界 → 线性收敛率                          |
| **Armijo 回溯**                                            | Ch6 §1.1 + §2.1       | 步长安全网，保证下降                            |
| **Newton decrement** $\lambda^2=-\nabla f^Td$            | Ch7 §1.1.2            | Newton 停止准则、二次收敛分析                    |
| **Inexact Newton 残差条件** $\|r_k\|\le\eta_k\|\nabla f_k\|$ | Ch7 §2                | Newton-CG、局部线性/超线性/二次收敛               |
| **Secant equation** $B_{k+1}s_k=y_k$                     | Ch8 §1.1              | BFGS / L-BFGS 更新的核心约束                 |
| **Wolfe 条件**                                             | Ch8 §1.1              | 保证 $s_k^Ty_k>0$，维持拟牛顿矩阵正定             |
| **次梯度最优性** $0\in\partial f(x^*)$                         | Ch9 §1.1              | 不可微凸优化的 KKT / 最优性条件                   |
| **投影不等式**                                                | Ch9 Lemma 2.1         | 投影次梯度法收敛证明                            |
| **Proximal mapping** $\operatorname{prox}_{th}$          | Ch10 Def 1.1          | PGM / ISTA / 投影梯度的统一写法                |
| **Gradient mapping** $G_t(x)$                            | Ch10 §2               | composite 问题的 stationarity 与收敛分析      |

## 四、考察重点（从作业逆推）

把作业 A1–A8、hw07、hw9、hw10、A11、A12 按知识点归类，可以非常清楚地看出考点分布：

### 1. 判凸题（Ch2）
- **A1.1, A1.2, A1.3, A1.4**：判定集合是否凸（极集 polar、邻域 ε-neighborhood、normal cone、recession cone、Minkowski 差）。
- **A2.1, A2.2, A2.3, A2.4, A3.2, A3.3, A3.4**：判定函数是否凸 / 严格凸（指数+二次、四次范数、Schur 补技巧、∫ψ）。
- **A2.5**：可微凸函数的梯度是单调映射。

> 考点：**会用一阶 / 二阶条件、运算保凸法则、Schur 补**；理解严格凸 vs 强凸的差别。

### 2. 标准形建模（Ch3 + Ch5）
- **A3.5**：Huber 损失 → QP 建模（拆分变量）。
- **A3.6**：求和距离平方 → 是不是 SOCP？写出标准 SOCP 形式。
- **hw07.1**：双曲约束 $x^Tx \le yz$ ↔ 二阶锥；调和均值最大化、几何均值最大化的 SOCP 化。
- **hw07.2**：含 $(I+B\,\mathrm{diag}(x)B^T)^{-1}$ 的目标 → 引辅助变量 → SOCP。
- **hw07.3**：多项式平方和（SOS）+ 控制最大值 → SDP。

> 考点：**LP/QP/SOCP/SDP 的标准形**、**变量代换技巧**、**Schur 补 / SOS 把高次目标降阶**。

### 3. 最优性条件（Ch4）
- **A6.1**：Kantorovich 不等式——先写 KKT，再用 KKT 解证明 $x=(1/2,0,\dots,0,1/2)$ 最优。

> 考点：**会写 KKT 系统**、**会用 KKT 解析地求最优解**、**会从 KKT 条件出发证明不等式**。

### 4. 对偶（Ch5）
- **A5.1**：凸 QP 写对偶并求最优解。
- **A5.2**：用共轭函数表示 $\min c^Tx\ \text{s.t.}\ f(x)\le 0$ 的对偶；解释为何对偶问题恒为凸（这是对偶的"灵魂题"）。
- **A5.3**：等式约束二次问题——对偶推导 + 强对偶 + 用对偶找原问题最优。
- **A5.4**：一个 minmax 问题写成 LP；用对偶给 $V^*$ 一个下界（hint 直接说"考虑它与对偶问题的关系"）。
- **A6.2**：proper cone 性质：$x \succ_K 0 \iff \exists t>0,\ x \succeq_K ty$。
- **A6.3**：含矩阵分式 $(Ax+b)^T F(x)^{-1}(Ax+b)$ 的问题 → SDP（再次 Schur 补）。
- **A6.4**：top-r 特征值之和 $f(A)$：写成 SDP，证明凸性，把 $\min f(A(x))$ 写成 SDP。
- **hw07.5**：SOCP 的对偶（两种推导：变量替换 + 锥对偶）。

> 考点：**写对偶问题（核心技能）**、**强对偶 vs Slater**、**共轭对偶**、**proper cone 与对偶锥的对应**、**SDP 的对偶**、**对偶可以解原问题**。

### 5. 数值算法收敛性证明（Ch6）
- **A8.1 / hw07.4**：回溯线搜索的步长下界与回溯次数上界（**强凸 + Lipschitz Hessian**）。
- **A8.2**：预条件梯度法 $x_{k+1}=x_k - tP\nabla f$：误差递推；如何选 $P, t$ 让 1 步收敛到最优。
- **A8.3**：在 $Lt\in(0,1]$ 下证"双倍充分下降"；在 $Lt\in(0,2]$ 下证 $\|\nabla f(x_{n+1})\|\le \|\nabla f(x_n)\|$。
- **A8.4**：通过辅助函数 $g_x(y)=f(y)-\nabla f(x)^T y$ 证明凸 + L-smooth 函数的"反向"性质 $f(x)+\nabla f(x)^T(y-x)+\frac{1}{2L}\|\nabla f(x)-\nabla f(y)\|^2\le f(y)$。
- **A8.5**：用黄金比例步长 $t=\varphi/L$ 证 $f(x_k)-f^*\le \frac{1}{\varphi k}\cdot \frac{L}{2}\|x_0-x^*\|^2$。

> 考点：**Lipschitz 梯度的二次上界**（Lemma 1.2）、**充分下降引理**（Lemma 1.3）、**telescoping 求和**、**强凸的二次下界**、**用 $g_x$ 这种"对偶视角辅助函数"**。

### 6. Newton / Inexact Newton（Ch7）
- **hw9.1**：$\sum_i\sqrt{1+(a_i^Tx-b_i)^2}+\rho\|x\|^2/2$：证明凸性，写 $\nabla f,\nabla^2 f$，写 Newton system 和 decrement。
- **hw9.2**：log-sum-exp + 正则项：写 damped Newton，一定要说明方向通过解线性系统得到，而不是显式求逆。
- **hw9.3**：Hessian 三对角结构：Newton 方向可 $O(n)$ 求解，对比 dense Cholesky。
- **hw9.4**：modified Newton 与 inexact Newton：$\mu I$ 保证正定，残差条件控制局部收敛速度。
- **hw9.5**：logistic regression 编程：damped Newton vs inexact Newton-CG，画目标值和梯度范数曲线。

> 考点：**Newton system、Newton decrement、Hessian 正定性、结构化线性系统、CG 残差条件、线搜索**。

### 7. 拟牛顿与二阶近似（Ch8）
- **hw10.1**：BFGS 的 $B$-更新：证明对称性、secant equation、半正定/正定性，以及为什么必须要求 $s^Ty>0$。
- **hw10.2**：$H$-形式拟牛顿方向与 Wolfe curvature condition：证明下降方向、由 Wolfe 推 $s_k^Ty_k>0$，并理解任意步长可能破坏 BFGS。
- **hw10.3**：手算 L-BFGS two-loop recursion，并比较 $m=20,n=10^6$ 时的 $O(mn)$ 存储和 full BFGS 的 $O(n^2)$ 存储。
- **hw10.4**：BB1/BB2 步长从最小二乘推导，并用 Rayleigh quotient 证明 $1/M\le t_k\le 1/m$。
- **hw10.5**：logistic regression 上实现 BFGS + strong Wolfe，若 $y_k^Ts_k$ 太小则跳过更新。

> 考点：**不用 Hessian 也能近似 Newton 方向**；会比较 Newton / BFGS / L-BFGS / BB / Gauss-Newton 的成本和适用场景。

### 8. 不可微凸优化（Ch9）
- **A11.1(a)**：$\|Ax-b\|_2+\|x\|_2$ 在残差为 0 的点求次微分，重点是范数零点次微分和仿射复合。
- **A11.1(b)**：$f(x)=\inf_y\|Ay-x\|_\infty$ 的次微分，重点是 active set、$\ell_\infty$ 次微分和 $A^Ts=0$。
- **A11.2**：单调复合函数的次梯度构造：$g=\sum_i z_i g_i$。
- **A11.3**：Polyak 步长 + error bound 推线性距离收缩。
- **A11.4**：非负约束二次规划的投影梯度 support identification。

> 考点：**次梯度不是下降方向**，所以不要把 subgradient method 当成 GD；它通用但慢。

### 9. 近端梯度法（Ch10）
- **A12.1**：证明 $u=\operatorname{prox}_f(x)$、$x-u\in\partial f(u)$、变分不等式三者等价；并说明 minimizer iff fixed point。
- **A12.2**：prox 的仿射缩放、尺度变换和加线性项规则，核心是变量替换和最优性条件。
- **A12.3**：proximal mapping non-expansive，用次梯度单调性证明。
- **A12.4**：二维 $f(x)+\lvert x_1+x_2\rvert$ 手算一步 PGM，重点是检查 $t=1$ 合法和 $\lvert a^Tx\rvert$ 的 prox。
- **A12.5**：LASSO 上实现 basic PGM 与 FPGM/FISTA，比较 $O(1/k)$ 与 $O(1/k^2)$。

> 考点：**PGM 比次梯度法快的原因是保留了 $h$ 的 prox 结构**。

## 五、各章建议复习时长（按从易到难）

| 章    | 难度   | 复习节奏                                                            |
| ---- | ---- | --------------------------------------------------------------- |
| Ch2  | ★★☆  | 1.5 天，重点是**做完 A1+A2+A3 的判凸题**才算掌握                               |
| Ch3  | ★★☆  | 1 天，关键是建模"套路"——见过几次就熟了                                          |
| Ch4  | ★★★  | 1 天，必须能**徒手写 KKT 系统**并且用它解题                                     |
| Ch5  | ★★★★ | 2 天，**写对偶**是本课程的最高频考点                                           |
| Ch6  | ★★★  | 1.5 天，重点是**收敛性证明的标准套路**                                         |
| Ch7  | ★★★★ | 1.5 天，重点是 **Newton system + decrement + inexact Newton**，配合 hw9 |
| Ch8  | ★★★  | 1 天，重点是 **secant equation、Wolfe、BFGS/L-BFGS、BB**，配合 hw10        |
| Ch9  | ★★★  | 1 天，重点是 **次微分计算 + $0\in\partial f$ + Polyak 步长 + 投影梯度**，配合 A11  |
| Ch10 | ★★★  | 1 天，重点是 **prox、gradient mapping、PGM/ISTA/FISTA**，配合 A12         |

## 六、做题策略

1. **遇到判凸题**：先想"运算保凸法则"能不能直接套；不行才动二阶 Hessian。
2. **遇到建模题**：先识别"分式 / 二次型 / 矩阵正定 / 范数"四种成分各自属于哪个标准形（LP/QP/SOCP/SDP）。
3. **遇到求最优解题**：永远先写 KKT；线性约束用 Slater，几乎无脑成立。
4. **遇到写对偶**：第 1 步永远是写 $L(x,\lambda,\nu)$；第 2 步对 $x$ 求 $\inf$（必要时用共轭函数）；第 3 步整理成约束形式。
5. **遇到收敛性证明**：四步走 ——（i）由 Lipschitz 写二次上界；（ii）代入算法迭代式；（iii）用凸性 / 强凸把 $f(x)-f^*$ 与梯度联系起来；（iv）telescoping 或递推得最终率。
6. **遇到 Newton 题**：先写 $H_kd_k=-g_k$，再写 $\lambda_k^2=-g_k^Td_k$，最后讨论 Hessian 正定性和线性系统怎么解。
7. **遇到不可微题**：先求 $\partial f$，最优性条件写 $0\in\partial f$ 或 $0\in\partial f+N_C$，不要硬写梯度。
8. **遇到 composite $g+h$**：优先想 PGM；如果 $h=I_C$ 就是投影，如果 $h=\lambda\|x\|_1$ 就是 soft-thresholding。

## 七、文件清单

| 文件              | 章          |
| --------------- | ---------- |
| `README.md`     | 总览         |
| `2_凸集与凸函数.md`   | Lecture 2  |
| `3_凸优化问题.md`    | Lecture 3  |
| `4_最优性条件.md`    | Lecture 4  |
| `5_拉格朗日对偶.md`   | Lecture 5  |
| `6_梯度下降与牛顿法.md` | Lecture 6  |
| `7_牛顿法.md`      | Lecture 7  |
| `8_拟牛顿法.md`     | Lecture 8  |
| `9_次梯度与次梯度法.md` | Lecture 9  |
| `10_近端梯度法.md`   | Lecture 10 |

> 学习方式建议：每章先按"核心思想 → 工具表 → 题型分类"过一遍，然后**回到对应作业（A1～A8、hw07、hw9、hw10、A11、A12）认真做一遍**。本系列文档不直接给作业答案，但会把每道题"考什么、用什么工具、思路从哪里切入"标得很清楚。