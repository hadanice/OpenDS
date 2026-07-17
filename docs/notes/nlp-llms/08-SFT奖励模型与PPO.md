---
title: "第 8 讲 SFT、奖励模型与 PPO"
course: "自然语言处理与大语言模型"
---

# 第 8 讲 SFT、奖励模型与 PPO

> 对应课程 `lecture-08-sft-rm-ppo`。本讲讨论从“会续写”到“会按人类意图回答”的经典 RLHF 三阶段流程。

## 1. 后训练全景

预训练模型拟合互联网文本，并不天然遵循指令。经典对齐流水线：

```text
基础模型 → 指令数据 SFT → 偏好数据训练奖励模型 → PPO 优化策略
                    └──────── 冻结参考策略，约束漂移 ────────┘
```

目标通常概括为 helpful、honest、harmless，但这些概念并非单一可观测标量；数据规范和评测协议与算法同样重要。

## 2. Supervised Fine-Tuning

SFT 数据由 prompt $x$ 和目标回复 $y=(y_1,\ldots,y_T)$ 构成：

$$
\mathcal L_{SFT}=-\sum_t m_t\log\pi_\theta(y_t\mid x,y_{<t}),
$$

其中 $m_t$ 通常只在 assistant 回复 token 上为 1，system/user 内容只提供上下文。Chat template、角色边界、BOS/EOS 与 generation prompt 必须和推理一致。

高质量 SFT 的关键是覆盖面、正确性、多样性、难度和格式一致；海量低质合成数据可能让模型学会冗长、模板化或错误推理。训练可全量更新，也可用 LoRA/QLoRA；验证不仅看 loss，还要用任务集检查指令遵循与灾难性遗忘。

## 3. 偏好数据与奖励模型

对同一 prompt 收集 preferred response $y_w$ 与 rejected response $y_l$。奖励模型输出标量 $r_\phi(x,y)$。Bradley–Terry 偏好模型：

$$
p(y_w\succ y_l\mid x)=\sigma(r_\phi(x,y_w)-r_\phi(x,y_l)).
$$

对应损失：

$$
\mathcal L_{RM}=-\log\sigma(r_w-r_l).
$$

训练关注排序而非奖励绝对值。数据中应随机左右位置，控制长度与风格偏差，保留 annotator agreement，并用 held-out pair accuracy、校准和切片分析评估。

### Reward hacking

策略会利用奖励模型漏洞，例如堆砌礼貌措辞、无依据地自信或输出异常长答案。高 RM 分不保证真实质量，因此需要 KL 约束、独立评测、红队和周期性刷新反馈。

## 4. 把语言模型视为策略

状态是 prompt 与已生成前缀，动作是下一个 token，策略为 $\pi_\theta(a_t\mid s_t)$。完整回复后获得序列级奖励。为了不偏离 SFT/reference 模型，常优化

$$
\max_\theta\;\mathbb E_{y\sim\pi_\theta(\cdot\mid x)}
[r_\phi(x,y)]-\beta\,\mathrm{KL}(\pi_\theta\|\pi_{ref}).
$$

KL 惩罚提供“信任区域”，$\beta$ 太小易 reward hacking，太大则几乎学不动。

## 5. PPO

用旧策略采样后，概率比为

$$
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{old}(a_t\mid s_t)}.
$$

clipped surrogate objective：

$$
L^{clip}=\mathbb E_t\left[
\min\left(r_tA_t,\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)A_t\right)
\right].
$$

优势 $A_t$ 衡量动作相对 baseline 的好坏；critic/value model 估计回报并用 GAE 降方差。完整损失还包含 value loss、entropy bonus 与 KL/奖励项。

### 一轮 PPO 的数据流

1. 从 prompt 数据采样，用 $\pi_{old}$ 生成回复并保存 log-prob。
2. 奖励模型打分，减去 reference KL，形成 token/sequence reward。
3. critic 估计 value，用 GAE 计算 advantage 与 return。
4. 对同一 rollout 做若干 mini-batch epoch，更新 policy 与 value。
5. 监控 reward、KL、clip fraction、entropy、value error 和真实任务指标。

PPO 工程复杂：同时维护 policy、reference、reward、value 四个模型或头，且 rollout 占大量推理成本。

## 6. 与 DPO 的关系

DPO 从 KL 正则化的偏好优化推导出直接的二分类目标，无需显式训练 RM 或在线 rollout。它更简单稳定，但依赖固定偏好数据，不能像在线 RL 那样自由接入可验证奖励和交互环境。算法选择取决于反馈来源、算力、稳定性与是否需要在线探索。

## 7. 自检清单

- 能说明 SFT loss 为什么只 mask assistant token。
- 能从 pairwise preference 写出 RM 损失。
- 能解释 reference model 与 KL 惩罚的作用。
- 能写出 PPO probability ratio 与 clip objective。
- 能列出 reward hacking、长度偏差和 judge 偏差的诊断方法。

## 延伸阅读

- Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- Schulman et al., [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
- Rafailov et al., [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)
