---
title: "第 6 讲 预训练 LLM 与生成"
course: "自然语言处理与大语言模型"
---

# 第 6 讲 预训练 LLM 与生成

> 对应 [Lecture 06 slides](https://baojian.github.io/llm-26/slides/lecture-06-slides/)；覆盖预训练范式、GPT/BERT/T5、解码、数据与扩展、高效推理和 LoRA。

## 1. 预训练—微调范式

预训练用海量无标注文本学习通用参数 $\hat\theta_{PT}$，下游从该点优化较小任务损失：

$$
\hat\theta_{PT}\approx\arg\min_\theta\mathcal L_{PT}(\theta),qquad
\hat\theta_{FT}\approx\arg\min_\theta\mathcal L_{FT}(\theta;\hat\theta_{PT}).
$$

静态 embedding 只预训练输入层；现代预训练初始化几乎全部网络参数，并产生上下文化表示。三类主要目标：

- Causal LM：按左到右预测，GPT 类。
- Masked LM：恢复被遮盖 token，BERT 类。
- Denoising/Span corruption：恢复被破坏片段，T5 类。

## 2. GPT 系列与上下文学习

Decoder-only Transformer 直接优化

$$
\mathcal L_{CLM}=-\sum_t\log p_\theta(w_t\mid w_{<t}).
$$

GPT-1 展示“生成式预训练 + 判别式微调”；GPT-2 强化零样本任务迁移；GPT-3 通过模型、数据和算力扩展展示 few-shot/in-context learning：只在提示中给示例而不更新权重。上下文学习不是参数更新，表现对示例顺序、格式、标签词与分布敏感。

## 3. 自回归解码

### 确定性搜索

- Greedy：每步取最大概率，快但局部最优、易重复。
- Beam search：保留 $k$ 个累计分数最高前缀，适合输出长度较可预测的翻译/摘要；开放生成中高似然不等于高质量。
- 长度归一化与重复 n-gram 惩罚可减少短输出偏好和循环，但属于启发式修正。

### 随机采样

温度缩放：

$$
p_T(w_i)=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)}.
$$

$T<1$ 更尖锐，$T>1$ 更随机。Top-$k$ 只保留概率最高的 $k$ 个 token；Top-$p$ 选择累计质量至少为 $p$ 的最小候选集，能随分布尖锐程度动态改变集合大小。实践中应同时报告 temperature、top-p/k、seed、最大长度与停止条件。

## 4. 数据、计算与 scaling law

模型能力来自模型参数、训练 token、数据质量和训练计算的共同作用。数据流水线包括采集、语言/领域识别、去重、质量过滤、隐私与安全清洗、混合配比和污染检查。

Scaling law 描述 loss 随模型、数据或算力呈近似幂律下降。计算最优训练强调模型大小与 token 数应匹配：参数做大但数据不足会欠训练；重复低质量数据也不能等价替代新鲜高质量 token。基准污染会让模型“记住答案”，必须用时间切分、近重复检测和私有测试集审计。

## 5. KV Cache 与推理

自回归第 $t$ 步只产生一个新 token。若每步重算所有历史 K/V，会重复大量计算。KV cache 保存每层历史 keys/values，新一步只计算新 token 的 Q/K/V，再让 Q 关注缓存：prefill 可并行处理提示，decode 每步串行且常受显存带宽限制。

缓存量近似随

$$
O(L\cdot T\cdot d_{kv})
$$

增长，其中 $L$ 为层数。MQA 让所有 query heads 共享一组 K/V，GQA 让若干 query heads 共享，显著减少缓存与带宽，代价是可能牺牲少量表达能力。

## 6. LoRA 与参数高效微调

冻结原权重 $W\in\mathbb R^{d_{out}\times d_{in}}$，只学习低秩增量：

$$
W'=W+\Delta W,qquad \Delta W=\frac\alpha r BA,
$$

其中 $A\in\mathbb R^{r\times d_{in}}$，$B\in\mathbb R^{d_{out}\times r}$，$r$ 很小。训练参数从 $d_{out}d_{in}$ 降为 $r(d_{in}+d_{out})$。常将 LoRA 插在 attention 的 Q/V 或更多线性层。

QLoRA 进一步把冻结基座量化到 4 bit，在较高精度中训练 adapter，并通过量化格式与分页优化器降低显存。量化节省存储不代表所有算子都以 4 bit 训练；实际计算会解量化到适合的计算 dtype。

## 7. 模型选择与评测

比较模型时至少控制 tokenizer、提示模板、解码参数、上下文长度和评测脚本。PPL 衡量建模能力；任务基准衡量准确率、F1、EM、BLEU/ROUGE 等；开放回答还需要事实性、帮助性、安全性和人类偏好评测。单一总分不能代表所有应用。

## 8. 自检清单

- 能比较 CLM、MLM 与 span corruption。
- 能说明 greedy、beam、top-k、top-p 与 temperature 的取舍。
- 能区分 prefill 与 decode，并解释 KV cache 的收益与显存成本。
- 能推导 LoRA 参数量，解释 $r$ 与 $\alpha$。
- 能说明 scaling law 不是“只把模型做大”。

## 延伸阅读

- Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
- Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- Hu et al., [LoRA](https://arxiv.org/abs/2106.09685)
