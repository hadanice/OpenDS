---
title: "附录 B Readings 导读"
course: "自然语言处理与大语言模型"
---

# 附录 B Readings 导读

这份导读按“论文解决了什么问题”组织。阅读顺序优先于年份顺序：先建立主线，再深入实现与扩展。

## 1. 基础教材

### Speech and Language Processing

Jurafsky & Martin 的 [SLP 3rd edition draft](https://web.stanford.edu/~jurafsky/slp3/) 是课程最直接的伴读教材。建议顺序：正则/分词 → n-gram → 分类与向量 → 神经网络/RNN → Transformer/LLM → 问答与 RAG。阅读时把教材公式与课程 notebook 的变量形状逐项对应。

### Natural Language Processing, Jacob Eisenstein

更偏统计学习与结构化建模，适合补充概率、线性模型、表示学习与传统 NLP 的统一视角。无需逐章通读，可在 NB/LR、embedding 和序列模型处查阅。

## 2. Tokenization

| 阅读 | 解决的问题 | 阅读重点 |
| --- | --- | --- |
| Gage, BPE (1994) | 用频繁 pair 合并进行压缩 | 原始算法与 NLP 版 BPE 的差别 |
| Kudo, Unigram (2018) | 对多种子词切分建模与采样 | unigram likelihood、Viterbi、regularization |
| Scaling Laws with Vocabulary (2024) | 词表大小与计算/性能怎样共同缩放 | token 数、embedding 参数与 FLOPs 的权衡 |
| Getting the Most out of Your Tokenizer (2024) | tokenizer 设计如何影响预训练 | 压缩率之外的下游指标与多语公平性 |

阅读结论：tokenizer 不是无关紧要的预处理，而是决定模型序列长度、参数、语言覆盖和训练成本的组成部分。

## 3. 统计语言模型

Chen & Goodman 的 smoothing 实证综述系统比较 Additive、Good-Turing、Katz、Kneser-Ney 等方法。重点不是背每个变体，而是理解三件事：从已见事件折扣概率质量、把质量分给未见事件、用合理的低阶分布回退。

Google 早期大规模机器翻译与语言模型资料展示 n-gram 在工业规模的工程价值；“更大语料 + 高效存储/查询”曾是核心路线，也帮助理解后来神经 LM 为什么必须解决容量与计算问题。

## 4. Transformer 与预训练

### Attention Is All You Need

必读图 1 与公式：scaled dot-product attention、multi-head、位置编码、encoder/decoder block。复现时重点核对 mask 与张量维度，而不是照抄架构图。

### GPT-1 / GPT-2

- GPT-1：生成式预训练能否成为多任务 NLP 的通用初始化？
- GPT-2：足够规模的自回归 LM 能否通过自然语言提示进行零样本迁移？

二者建立 decoder-only 从预训练、微调走向 prompting 的路线。

### BERT / ALBERT

- BERT：双向 Transformer 如何用 MLM 预训练并以极小任务头适配多种理解任务？
- ALBERT：如何通过 embedding factorization、跨层共享和 SOP 降参数并改进句间任务？

阅读时区分“参数量、计算量、激活显存”，参数共享并不等于按相同比例减少 FLOPs。

### T5

T5 把所有任务统一成 text-to-text，并系统比较架构、目标、数据和迁移设置。重点理解 span corruption 与 encoder–decoder 为何适合条件生成。

## 5. 开放基础模型

LLaMA 1/2 讨论高质量数据、计算效率、开放权重与 chat alignment。阅读技术报告时建议用统一表格记录：参数、训练 token、上下文、tokenizer、数据声明、架构改动、后训练方法和评测，避免只比较排行榜单一数字。

## 6. 后训练与推理强化

建议补读：

- [InstructGPT](https://arxiv.org/abs/2203.02155)：SFT → RM → PPO 的完整人类反馈流水线；
- [PPO](https://arxiv.org/abs/1707.06347)：概率比、clipping 与多 epoch 更新；
- [DPO](https://arxiv.org/abs/2305.18290)：如何把偏好优化化为直接分类目标；
- [DeepSeekMath](https://arxiv.org/abs/2402.03300)：GRPO 与数学推理训练背景。

阅读 RL 论文时必须分清：采样策略、旧策略、参考策略、奖励模型和 value model；很多混淆都来自把它们统称为“模型”。

## 7. RAG

- [RAG](https://arxiv.org/abs/2005.11401)：把 parametric memory 与 non-parametric retrieval 结合；
- [DPR](https://arxiv.org/abs/2004.04906)：用双塔对比学习进行开放域问答检索；
- BM25 相关资料：理解稀疏检索为何在专有名词和精确匹配上仍强。

读 RAG 论文时把改进定位到 ingestion、retrieval、reranking、context construction、generation 或 evaluation 中的一层；若只报端到端正确率，很难知道提升来自哪里。

## 8. 论文阅读模板

每篇论文用一页回答：

1. 旧方法的具体瓶颈是什么？
2. 新方法改变了数据、目标、架构还是推理系统？
3. 核心公式中每个随机变量与分布是什么？
4. 与最强 baseline 是否公平比较？
5. 消融真正支持哪些因果结论？
6. 结果在哪些数据、规模和算力下成立？
7. 有哪些未评估的失败、安全或成本问题？
8. 若只复现一个最小实验，应该复现什么？

课程仓库 `papers/` 保存了授课使用的版本；引用时建议再核对论文官方页面或 arXiv 最新版本。
