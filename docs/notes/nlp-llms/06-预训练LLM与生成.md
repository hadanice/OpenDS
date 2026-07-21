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

## 6. FlashAttention、量化与服务指标

标准 attention 会把 $T\times T$ 分数矩阵写入显存再读回，长序列时高带宽内存访问常比算术运算更慢。FlashAttention 通过分块、在线 softmax 和算子融合，在片上 SRAM 中完成局部计算，避免物化完整注意力矩阵；它计算的是精确 attention，主要改变 IO 复杂度而非模型目标。

权重量化把 FP16/BF16 参数压缩到 INT8、INT4 或 FP4。若按组量化，常写为

$$
w\approx s(q-z),
$$

其中 $q$ 是低比特整数，$s$ 是缩放因子，$z$ 是零点。权重-only 量化主要节省模型存储与加载带宽；激活和 KV cache 量化还能继续省显存，但对异常值和累计误差更敏感。量化效果必须同时报告精度退化、吞吐、首 token 延迟和单 token 延迟。

在线服务区分 prefill 与 decode：前者并行计算提示，后者逐 token 串行生成。continuous batching 将不同请求的 decode 步动态拼批，提高吞吐；但大 batch、长上下文和长输出会增加排队时间。系统优化因此是 latency、throughput、显存、功耗和模型质量的多目标权衡。

## 7. LoRA 与参数高效微调

冻结原权重 $W\in\mathbb R^{d_{out}\times d_{in}}$，只学习低秩增量：

$$
W'=W+\Delta W,qquad \Delta W=\frac\alpha r BA,
$$

其中 $A\in\mathbb R^{r\times d_{in}}$，$B\in\mathbb R^{d_{out}\times r}$，$r$ 很小。训练参数从 $d_{out}d_{in}$ 降为 $r(d_{in}+d_{out})$。常将 LoRA 插在 attention 的 Q/V 或更多线性层。

QLoRA 进一步把冻结基座量化到 4 bit，在较高精度中训练 adapter，并通过量化格式与分页优化器降低显存。量化节省存储不代表所有算子都以 4 bit 训练；实际计算会解量化到适合的计算 dtype。

## 8. 模型选择与评测

比较模型时至少控制 tokenizer、提示模板、解码参数、上下文长度和评测脚本。PPL 衡量建模能力；任务基准衡量准确率、F1、EM、BLEU/ROUGE 等；开放回答还需要事实性、帮助性、安全性和人类偏好评测。单一总分不能代表所有应用。

## 9. 从静态词向量到上下文化表示

静态 word2vec 给 `bank` 一个固定向量，无法同时表达“河岸”和“银行”。ELMo 用双向 LSTM：前向 LM 根据左文预测，后向 LM 根据右文预测，再把不同层的隐藏状态按任务学习加权组合。它首次系统展示“同一个 token 的向量应随句子变化”。

ELMo 仍把预训练表示作为下游模型输入；Transformer 时代进一步把整个网络作为初始化并端到端微调。这个变化解释了预训练范式为何比“下载一个词向量表”强：浅层偏局部句法，深层偏语义与任务信息，下游可以调整所有层。

## 10. GPT 路线的关键变化

- GPT-1：decoder Transformer 的生成式预训练，再为具体任务微调；
- GPT-2：扩大模型和 WebText，强调零样本任务可由自然语言提示诱导；
- GPT-3：继续扩展模型、数据和计算，系统展示 zero/one/few-shot ICL；
- 后续 GPT 类系统：把预训练与指令微调、偏好对齐、工具和多模态系统结合。

参数规模不是唯一变量。架构细节、tokenizer、训练 token 数、数据混合与去重、优化稳定性和后训练共同决定最终能力。比较代际模型时，应区分“基座模型能力”与“聊天系统能力”。

## 11. Scaling laws 与计算最优

经验上，交叉熵 loss 对参数量 $N$、数据量 $D$、计算量 $C$ 常呈带不可约项的幂律：

$$
L(N)\approx L_\infty+aN^{-\alpha},\qquad
L(D)\approx L_\infty+bD^{-\beta}.
$$

Transformer 训练计算量可粗略写成 $C\approx 6ND$（常数依实现而异）。固定计算预算时，过大的模型会因 token 不足而欠训练，过小的模型又浪费数据；计算最优 scaling 需要同时增长 $N$ 与 $D$。课堂强调三点：幂律是经验区间规律而非物理定律；数据质量下降会破坏“更多 token 更好”；下游能力、推理成本与训练 loss 不总是同一最优点。

## 12. 解码是对模型分布的二次设计

Greedy 和 beam search 追求高概率序列，但语言模型可能把概率集中在安全、常见、短而重复的文本上。课堂 GPT-2 示例说明 beam 更宽不保证开放生成更好。随机采样通过温度与截断重新塑造分布：

- top-k 的候选数固定，分布很尖或很平时都不自适应；
- top-p 的候选集合随不确定性变化；
- repetition penalty 与 no-repeat n-gram 能止住循环，也可能误伤代码、诗歌和术语；
- stop sequence 必须在 tokenizer 级验证，字符串边界可能跨 token。

评测生成策略应固定随机种子并报告多样性、事实性、任务成功率和长度，而不是只展示一条“看起来不错”的样例。

## 13. KV Cache 的显存账本

设层数 $L$、序列长 $T$、KV 头数 $h_{kv}$、每头维度 $d_h$、每元素字节数 $b$，单请求缓存近似为

$$
2LTh_{kv}d_hb,
$$

系数 2 对应 K 与 V。并发请求和长上下文会线性放大这部分显存。PagedAttention 把缓存切成非连续页，减少不同长度请求造成的碎片；prefix caching 可复用共享系统提示的 KV，但必须保证模型、位置编码和前缀 token 完全一致。

服务指标要分开：TTFT 主要受排队、tokenization 与 prefill 影响；TPOT/ITL 主要反映 decode；吞吐取决于 batching；端到端延迟还与输出长度相关。只报告 tokens/s 容易掩盖交互体验。

## 延伸阅读

- Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
- Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- Hu et al., [LoRA](https://arxiv.org/abs/2106.09685)
