---
title: "第 2 讲 N-gram 语言模型"
course: "自然语言处理与大语言模型"
---

# 第 2 讲 N-gram 语言模型

> 对应 [Lecture 02 slides](https://baojian.github.io/llm-26/slides/lecture-02-slides/)；配套阅读为 SLP 第 3 章、Chen & Goodman 的 smoothing 综述等。

## 1. 语言模型与最大似然

语言模型给 token 序列赋概率。链式法则把联合分布分解为逐 token 条件概率：

$$
p(w_{1:T})=\prod_{t=1}^{T}p(w_t\mid w_{1:t-1}).
$$

训练语料由未知数据分布 $p_{\text{data}}$ 采样。最小化前向 KL

$$
\mathrm{KL}(p_{\text{data}}\|p_\theta)
$$

等价于最大化数据上的期望对数似然；经验目标为

$$
\max_\theta \frac1N\sum_{i=1}^N\log p_\theta(w^{(i)}).
$$

这条“最大似然 = 最小交叉熵”的主线会一直延伸到神经 LLM。

## 2. N-gram 的 Markov 近似

完整历史难以统计，于是作 $(N-1)$ 阶 Markov 假设：

$$
p(w_t\mid w_{1:t-1})\approx p(w_t\mid w_{t-N+1:t-1}).
$$

MLE 估计为

$$
\hat p(w_t\mid h)=\frac{C(h,w_t)}{C(h)}.
$$

句首加入足够数量的 `BOS`，句尾加入 `EOS`，使模型学习开始和结束。对未登录词可固定词表并映射为 `UNK`，或把训练集中的低频词替换为 `UNK` 后再估计概率。

### 参数与稀疏性

理论参数规模约为 $O(|\mathcal V|^N)$。自然语言的组合空间巨大，即使训练语料很大，大部分高阶 n-gram 也从未出现，因此 MLE 会把测试序列概率直接置零。

## 3. 困惑度

测试集共有 $T$ 个预测 token 时：

$$
\mathrm{PPL}=\exp\left(-\frac1T\sum_{t=1}^T \log p_\theta(w_t\mid w_{<t})\right).
$$

困惑度是平均负对数似然的指数，可理解为模型每一步面对的“有效分支数”。越低越好，但比较时必须使用相同 tokenizer、词表、边界处理和测试集；不同 token 粒度下的 PPL 不可直接横比。

内在评测看似然/PPL，便宜但不保证下游改善；外在评测把模型放入翻译、识别等任务，结论更直接但成本高。

## 4. 平滑：给未见事件留概率

### Add-$\delta$

$$
p_\delta(w\mid h)=\frac{C(h,w)+\delta}{C(h)+\delta|\mathcal V|}.
$$

Laplace 即 $\delta=1$，简单但常把过多概率质量分给未见事件；更小的 $\delta$ 通常更合理。

### 插值

将不同阶模型加权：

$$
p(w_t\mid w_{t-2},w_{t-1})=
\lambda_3 p_{\text{ML}}(w_t\mid w_{t-2},w_{t-1})+
\lambda_2 p_{\text{ML}}(w_t\mid w_{t-1})+
\lambda_1 p_{\text{ML}}(w_t),
$$

其中 $\lambda_i\ge0,\sum_i\lambda_i=1$。权重可固定，也可依历史计数动态变化。

### Backoff 与 Katz

若高阶 n-gram 有可靠计数，使用折扣后的高阶概率；否则退回低阶分布，并用归一化系数保证概率和为 1。Good-Turing 用“出现 $r$ 次的类型数”估计应分给未见事件的质量。

### Kneser-Ney

Kneser-Ney 的关键不是普通 unigram 频率，而是 continuation probability：一个词出现在多少种不同历史之后。频繁但上下文单一的词不应在回退分布里获得过高概率。插值绝对折扣形式可写为

$$
p_{\text{KN}}(w\mid h)=\frac{\max(C(h,w)-D,0)}{C(h)}+\lambda(h)p_{\text{cont}}(w).
$$

## 5. 生成与数值稳定

生成时从 $p(w_t\mid h)$ 采样，直到 `EOS`。实际计算全部在 log 空间：

$$
\log p(w_{1:T})=\sum_t\log p(w_t\mid h_t),
$$

避免很多小概率连乘下溢。若需要归一化指数，使用 log-sum-exp 技巧。

## 6. N-gram 到神经 LM

N-gram 的优点是透明、易调试、训练快；缺点是参数不能在相似上下文之间共享，且上下文窗口固定。神经 LM 用稠密向量和可学习函数替换计数表，让“相似词、相似历史”共享统计强度，但训练目标仍是相同的 next-token likelihood。

## 7. 易错点

- Bigram 的分母是历史词的计数 $C(w_{t-1})$，不是当前词计数。
- PPL 的长度归一化应与实际被预测的 token 对齐。
- 平滑不是“给零加一点”这么简单，还必须重新分配并归一化概率质量。
- 训练、验证、测试必须隔离；用测试集选平滑参数属于泄漏。
