---
title: "自然语言处理与大语言模型笔记"
course: "自然语言处理与大语言模型"
---

# 自然语言处理与大语言模型笔记

本组笔记对应复旦大学 `CS40008.01 NLP and LLMs`（2026 春，周宝健老师）。第 1–10 讲按课程 slides 的知识顺序整理，并用指定 readings 与课堂记录补足推导；第 11–12 讲根据 Week 14–16 的课堂原文整理扩散语言模型和大语言模型智能体。

## 章节导航

| 讲次 | 主题 | 核心内容 |
| --- | --- | --- |
| 1 | [文本预处理与分词](01-文本预处理与分词.md) | 规范化、BPE、WordPiece、Unigram 与词表权衡 |
| 2 | [N-gram 语言模型](02-N-gram语言模型.md) | MLE、平滑、插值、回退与困惑度 |
| 3 | [文本分类与词向量](03-文本分类与词向量.md) | Naive Bayes、Logistic Regression、PMI 与 Word2Vec |
| 4 | [神经语言模型与序列建模](04-神经语言模型与序列建模.md) | NPLM、RNN、LSTM、Encoder–Decoder 与优化 |
| 5 | [注意力与 Transformer](05-注意力与Transformer.md) | Q/K/V、多头注意力、位置编码与三种架构 |
| 6 | [预训练 LLM、生成与推理系统](06-预训练LLM与生成.md) | GPT、解码、scaling、KV cache、FlashAttention 与量化 |
| 7 | [BERT 与评测基准](07-BERT与评测基准.md) | MLM、下游微调、GLUE/MMLU 与评测有效性 |
| 8 | [SFT、奖励模型与 PPO](08-SFT奖励模型与PPO.md) | 指令微调、偏好学习、RLHF、DPO 与安全对齐 |
| 9 | [GRPO 与推理强化学习](09-GRPO与推理强化学习.md) | 组内相对优势、RLVR、奖励设计与训练稳定性 |
| 10 | [RAG 检索增强生成](10-RAG检索增强生成.md) | 稀疏/稠密检索、重排、grounding 与分层评测 |
| 11 | [扩散语言模型](11-扩散语言模型.md) | DDPM、变分目标、D3PM、mask 转移与并行去噪 |
| 12 | [大语言模型智能体](12-大语言模型智能体.md) | action、reasoning、memory、planning、数据与评测 |

## 全局知识图谱

```mermaid
flowchart LR
  A[原始文本] --> B[规范化与分词]
  B --> C[N-gram 与统计语言模型]
  B --> D[稀疏特征与词向量]
  D --> E[神经语言模型]
  E --> F[注意力与 Transformer]
  F --> G[GPT / BERT / T5 预训练]
  G --> H[SFT 与偏好对齐]
  H --> I[PPO / GRPO 推理强化]
  G --> J[RAG 外部知识]
  G --> K[扩散语言模型]
  G --> L[LLM Agent]
  J --> L
  I --> L
  K --> M[生成模型前沿]
```

## 贯穿课程的五条主线

1. **概率建模**：链式法则 → 最大似然 → 交叉熵 → 困惑度 → 自回归与扩散生成。
2. **表示学习**：one-hot → 计数向量 → 静态词向量 → 上下文化表示 → 大模型隐状态。
3. **架构演进**：前馈网络 → RNN/LSTM → 注意力 → Transformer → 预训练基础模型。
4. **训练与对齐**：预训练 → SFT/LoRA → 偏好模型 → PPO/GRPO → 安全与可靠性。
5. **系统与交互**：KV cache/量化 → RAG → 工具调用 → 记忆、规划与智能体评测。

## 统一符号

| 符号 | 含义 |
| --- | --- |
| $\mathcal V$ | 词表，大小为 $\lvert\mathcal V\rvert$ |
| $w_{1:T}$ | 长度为 $T$ 的 token 序列 |
| $d$ | 隐藏维度；$h$ 为注意力头数；$d_k=d/h$ |
| $\theta$ | 模型参数；$p_\theta$ 为模型分布 |
| $x,y$ | 输入与标签；偏好学习中也表示 prompt 与 response |
| $\pi_\theta$ | 作为策略的语言模型 |
| $x_t$ | 扩散过程第 $t$ 步的状态，$x_0$ 为干净样本 |

主要资料：[课程官网](https://baojian.github.io/llm-26/)、[课程仓库](https://github.com/baojian/llm-26) 与 Jurafsky & Martin 的 [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/)。
