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

## 7. 对齐、安全与红队

对齐目标不仅是“更受偏好模型喜欢”。helpfulness、honesty 与 harmlessness 可能冲突：过度安全会拒绝正常请求，过度迎合会产生谄媚或无依据肯定。安全训练通常组合有害请求与安全回答数据、偏好优化、规则约束和推理时分类器；任何单层防线都可能被绕过。

红队评测主动构造越狱、提示注入、隐私提取、危险能力和多轮诱导案例。结果应按风险类型、严重度和攻击成功率分层，并保留正常任务能力作为对照，防止只降低风险分数却同时破坏可用性。训练集、奖励模型和 judge 可能共享盲点，因此还需要独立测试、人工复核与部署后的事件监测。

## 8. 强化学习符号与策略梯度

在 LLM 中，状态 $s_t=(x,y_{<t})$，动作 $a_t=y_t$，一条完整回复形成轨迹 $\tau$。回报、价值与优势为

$$
G_t=\sum_{k=t}^{T}\gamma^{k-t}r_k,
\quad V^\pi(s)=\mathbb E[G_t\mid s_t=s],
\quad A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s).
$$

策略梯度使用 log-derivative trick：

$$
\nabla_\theta J(\theta)=
\mathbb E_{\tau\sim\pi_\theta}
\left[\sum_t\nabla_\theta\log\pi_\theta(a_t\mid s_t)G_t\right].
$$

减去只依赖状态的 baseline 不改变期望，却能显著降方差。Actor–Critic 用 value model 学 baseline；GAE 用 TD 残差

$$
\delta_t=r_t+\gamma V(s_{t+1})-V(s_t),\qquad
\hat A_t=\sum_{l\ge0}(\gamma\lambda)^l\delta_{t+l}
$$

在偏差与方差之间折中。RLHF 常把 RM 的序列级分数放在末 token，再把逐 token KL 惩罚加入奖励。

## 9. PPO 裁剪到底限制什么

重要性比 $r_t>1$ 表示新策略提高了该动作概率，$r_t<1$ 表示降低。若 $A_t>0$，更新应提高概率，但超过 $1+\epsilon$ 后不再奖励继续提高；若 $A_t<0$，更新应降低概率，但低于 $1-\epsilon$ 后不再奖励继续降低。`min` 与 clip 共同构成一个悲观代理目标，避免同一批旧策略数据被反复利用时策略走得太远。

PPO 并不保证实际 KL 一定小于阈值，所以实现还会监控 `approx_kl`，必要时 early stop 或自适应 $\beta$。关键监控项包括：policy reward、non-score reward、KL、clip fraction、entropy、value loss、explained variance、回复长度和真实验证集能力。

## 10. 四模型数据流与显存压力

经典 PPO-RLHF 同时涉及：

1. actor/policy：生成并更新；
2. reference：冻结，用于 KL；
3. reward model：冻结，为完整回复打分；
4. critic/value：更新，估计每个 token 的价值。

rollout 阶段主要是推理，update 阶段才反向传播。大模型系统会使用共享 backbone、LoRA、ZeRO/FSDP、张量并行、生成引擎与训练引擎切换等方式节省显存。课堂的小型 GPT-2 demo 能展示算法数据流，但不能用其输出质量代表 InstructGPT 规模结果。

## 11. DPO 的推导直觉与边界

KL 正则化 RL 的最优策略满足

$$
\pi^*(y\mid x)\propto
\pi_{ref}(y\mid x)\exp(r(x,y)/\beta).
$$

把奖励差写成策略与参考策略的 log-ratio，再代入 Bradley–Terry 损失，可得 DPO：

$$
\mathcal L_{DPO}=-\log\sigma\left(
\beta\left[
\log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)}-
\log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}
\right]\right).
$$

它省掉显式 RM、critic 和在线 rollout，训练像普通 pairwise classification；但数据是离线的，无法探索数据集中没有的回复，也仍会继承偏好标注的长度、风格和群体偏差。

## 延伸阅读

- Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- Schulman et al., [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
- Rafailov et al., [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)
