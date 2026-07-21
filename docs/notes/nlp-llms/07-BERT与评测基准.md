---
title: "第 7 讲 BERT 与评测基准"
course: "自然语言处理与大语言模型"
---

# 第 7 讲 BERT 与评测基准

> 对应课程 `lecture-07-bert-benchmarks` 与 [BERT](https://arxiv.org/abs/1810.04805)、[ALBERT](https://arxiv.org/abs/1909.11942) 等 readings。

## 1. 为什么需要双向编码器

自回归模型在位置 $t$ 只能看左侧，而许多理解任务需要同时使用左右语境。BERT 使用 Transformer encoder，让每个 token 关注整句，再通过自监督遮盖构造训练信号。

输入表示是三部分之和：

$$
e_i=e_i^{token}+e_i^{position}+e_i^{segment}.
$$

`[CLS]` 常作为序列级表示，`[SEP]` 分隔句段，`[MASK]` 用于预训练。subword token 与原词标签对齐时，序列标注任务需明确只标首子词还是把标签扩展到所有子词。

## 2. Masked Language Modeling

选择位置集合 $M$，最小化

$$
\mathcal L_{MLM}=-\sum_{i\in M}\log p_\theta(w_i\mid w_{\setminus M}).
$$

原始 BERT 通常抽 15% token：其中 80% 换成 `[MASK]`、10% 换成随机 token、10% 保持不变，缓解预训练出现 `[MASK]` 而下游不出现的差异。MLM 不是严格的序列联合概率分解，因此 BERT 擅长表示与补全，不像 decoder LM 那样自然进行从左到右长文本生成。

### NSP 与后续改进

Next Sentence Prediction 判断句 B 是否真实接在句 A 后面。后续工作发现数据构造和训练规模影响很大，RoBERTa 去掉 NSP 并改进动态 masking、数据与训练；ALBERT 用跨层参数共享和 embedding factorization 降参数，并用 sentence-order prediction 替代 NSP。

## 3. Fine-tuning 模式

| 任务 | 读取表示 | 输出头 | 常见指标 |
| --- | --- | --- | --- |
| 句子分类 | `[CLS]` 或 pooled output | Linear + softmax | Accuracy/F1/MCC |
| 句对分类 | 拼接为 A/B segments | Linear + softmax | Accuracy/F1 |
| Token 分类 | 每个 token hidden state | Linear/CRF | span/token F1 |
| 抽取式问答 | 每个 token | start/end logits | EM/F1 |

全量微调更新所有参数，通常学习率小、epoch 少；线性探测冻结 encoder，只训练头部，用于测量表示中是否线性可读；adapter/LoRA 介于二者之间。小数据上需多随机种子报告均值和方差。

## 4. GLUE、SuperGLUE 与 QA

GLUE 汇总语法可接受性、情感、句对相似/释义、自然语言推理等任务，指标因任务而异；不能把所有任务都错误地用 accuracy。SuperGLUE 提高难度并增加常识、指代和阅读理解。

SQuAD 抽取式 QA 的 exact match 要求规范化后完全一致，token F1 衡量预测与答案 token 的重叠。存在多个参考答案时通常取最高分。生成式 QA 还需评估语义正确性、证据支持与拒答行为，字符串重叠不足以衡量事实性。

## 5. 评测设计原则

一个可信实验应明确：

1. 数据 split 与预处理；
2. 模型 checkpoint 与 revision；
3. prompt/template、max length、truncation；
4. 超参数搜索空间和选择依据；
5. 多次运行方差、置信区间或显著性；
6. 错误类型与典型失败案例；
7. 训练数据污染与近重复审计。

Macro-F1 先算每类 F1 再平均，适合重视少数类；micro-F1 汇总所有样本，更受大类支配。类别不平衡时只看 accuracy 会掩盖模型完全忽略少数类的问题。

## 6. Benchmark 的局限

- 测试集可能饱和，分数差异小于标注噪声。
- leaderboard 容易导致对测试集的隐式过拟合。
- 静态数据不能覆盖领域迁移、鲁棒性、安全性与成本。
- 数据污染会把记忆误当泛化。
- LLM-as-a-judge 可扩展但有位置、长度、风格和同源偏差，必须校准并抽样人工复核。

## 7. BERT 输入与预训练细节

句对输入通常写成：

```text
[CLS] sentence A [SEP] sentence B [SEP]
```

token、位置和 segment embedding 相加后进入 encoder。原始 BERT-base 为 12 层、隐藏维 768、12 个头，约 110M 参数；BERT-large 为 24 层、隐藏维 1024、16 个头，约 340M 参数。模型并不是把 `[CLS]` 天生规定为“整句语义”，而是在预训练与下游监督中让该位置逐渐承担序列级汇聚功能。

MLM 每次只在抽中的位置计算词表交叉熵，因此单位序列得到的监督信号少于 causal LM。它换来的优势是被预测 token 同时看到左右上下文。动态 masking 在不同 epoch 重新选择遮盖位置，能让同一文本产生更多训练信号。

## 8. RoBERTa、ALBERT 与 T5 的设计比较

RoBERTa 表明原始 BERT 的许多增益来自训练得更充分：更多数据、更大 batch、更长训练、动态 masking，并去掉 NSP。ALBERT 用两种方法减参：把词表 embedding 维度与隐藏维度解耦，以及跨层共享 Transformer 参数；它还用句序预测区分相邻顺序，避免 NSP 的主题捷径。

T5 把所有任务统一成 text-to-text，使用 encoder–decoder 和 span corruption：连续片段替换成 sentinel token，decoder 生成被删片段。三种预训练结构可概括为：

| 模型族 | 上下文可见性 | 自监督目标 | 自然输出形式 |
| --- | --- | --- | --- |
| BERT/RoBERTa | 双向 | MLM | 表示、分类、抽取 |
| GPT | 因果左到右 | next token | 自由文本生成 |
| T5 | encoder 双向、decoder 因果 | span denoising | 条件文本生成 |

## 9. 从 GLUE 到现代能力基准

课程回顾的基准可按能力拆分：GLUE/SuperGLUE 测语言理解，MMLU 测多学科选择题，GSM8K/AIME 测数学推理，HumanEval/LiveCodeBench 测代码，SWE-bench 测真实仓库修复，Agent 类基准测多步环境交互。题型越接近真实系统，自动判分越难，成本与可复现性问题也越突出。

选择题准确率要明确答案解析方式：比较选项 token 的条件概率、让模型生成字母、还是用正则抽取最终答案，会得到不同结果。生成任务的 pass@k 也不能与单次 accuracy 混为一谈；它衡量多次采样中至少一次成功的概率。

## 10. 误差分析比排行榜名次更有信息

先建立可复现总分，再按长度、领域、类别频率、语言、推理步数和是否需要外部知识切片。对每类抽取真阳性、假阳性、假阴性，区分数据错误、知识缺失、推理错误、格式解析失败与拒答错误。两个模型总分相近时，切片可能揭示完全不同的能力边界。

若同一团队反复观察测试集并据此改模型，测试集事实上已成为验证集。可靠做法是保留未触碰的最终集、记录每次评测决策，并报告置信区间。对于人类或 LLM judge，还要随机回答顺序、隐藏模型身份、测量评审一致率，并用人工抽样校准。
