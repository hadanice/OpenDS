---
title: "附录 A 实验与课程项目指南"
course: "自然语言处理与大语言模型"
---

# 附录 A 实验与课程项目指南

课程强调 `read → implement → experiment → explain`。本附录把各讲 notebook 与课程作业串成一条可复现路线。

## 1. 四个阶段性实验

| 阶段 | 建议交付 | 必做验证 |
| --- | --- | --- |
| Tokenization + Word2Vec | 从零 BPE、词向量训练与分析 | 可逆编码、merge 单测、相似词/偏见案例 |
| Transformer Block | raw PyTorch MHA/Block、注意力可视化 | shape、mask、未来信息泄漏、梯度检查 |
| Fine-tuning | 小型 Qwen/Llama 的 LoRA/QLoRA | base vs tuned、消融、显存与吞吐 |
| RAG | 垂直 PDF/语料问答系统 | retrieval 与 generation 分层指标、引用核验 |

## 2. 最小可复现实验规范

每次实验至少固定并记录：

```yaml
data:
  name: dataset-name
  split: train/validation/test
  preprocessing: version-or-script
model:
  checkpoint: exact-name
  revision: commit-or-tag
training:
  seed: 42
  optimizer: adamw
  learning_rate: ...
  batch_size: ...
  epochs_or_steps: ...
generation:
  temperature: ...
  top_p: ...
  max_new_tokens: ...
```

同时保存 `requirements`/environment、运行命令、Git commit、日志与最终 checkpoint 配置。不要只上传一个“在当前机器上恰好能跑”的 notebook。

## 3. 调试顺序

### 数据

先打印若干 tokenize 后样本、标签 mask 和长度分布。大量模型 bug 实际是数据错位、特殊 token 重复或截断位置不对。

### 单 batch 过拟合

让模型在极小数据上把 loss 降到很低。若做不到，优先检查 forward、loss、optimizer、`train()` 模式和梯度，而不是继续调大模型。

### 形状与数值

对关键张量写 assertion；监控 NaN/Inf、梯度范数、logit 范围和有效 token 数。混合精度出错时先用 FP32 复现。

### 基线

每个复杂方法必须有简单 baseline：BPE 对字符切分；神经分类对 TF-IDF + LR；LoRA 对 zero/few-shot；RAG 对无检索与 BM25。

## 4. 消融实验模板

一次只改变一个因素，并报告平均值与方差：

| 主题 | 可消融因素 |
| --- | --- |
| Tokenizer | vocab size、byte fallback、normalization |
| Transformer | head 数、位置编码、Pre/Post-LN |
| LoRA | rank、target modules、data size |
| Generation | temperature、top-p、prompt template |
| RAG | chunk size、overlap、retriever、top-k、reranker |
| RL | group size、KL 系数、reward 组成、采样温度 |

## 5. 项目选题与研究问题

课程项目可走三类：研究型（新目标/结构或系统消融）、应用型（端到端工具/agent）、系统型（推理加速、量化或服务）。好问题应满足：

- 有清晰输入、输出与成功标准；
- 有公开或合法可用的数据；
- 有至少一个可复现 baseline；
- 能在现有算力内完成；
- 不把“接一个 API 做 UI”本身当研究贡献；
- 对隐私、版权、偏见和错误使用有风险说明。

### 一页 proposal

1. 问题与动机；
2. 数据与许可；
3. 方法和系统图；
4. baselines 与 metrics；
5. 预期消融；
6. 时间表、成员分工、算力；
7. 风险与 fallback。

## 6. 报告结构

最终报告建议按：摘要 → 问题定义 → 相关工作 → 数据 → 方法 → 实验设置 → 主结果 → 消融/错误分析 → 局限与伦理 → 结论。结果表要同时给效果、成本和方差；挑选案例时既展示成功也展示代表性失败。

## 7. 提交前检查

- [ ] 新环境可从 README 一条命令启动。
- [ ] 数据未误传个人信息、密钥或受限内容。
- [ ] 训练与测试无重复/泄漏。
- [ ] 指标脚本有小样本单元测试。
- [ ] 所有图表标明数据、坐标、单位和误差。
- [ ] 外部模型、代码、数据和 AI 工具已注明来源。
- [ ] 结论没有超出实验支持范围。
