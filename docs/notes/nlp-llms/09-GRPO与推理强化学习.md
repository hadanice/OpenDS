---
title: "第 9 讲 GRPO 与推理强化学习"
course: "自然语言处理与大语言模型"
---

# 第 9 讲 GRPO 与推理强化学习

> 对应课程 `lecture-09-grpo-old`。重点是理解 GRPO 如何用同一 prompt 的多条回复构造相对优势，并区分可验证奖励带来的推理强化与普通偏好对齐。

## 1. 从 PPO 到 GRPO

PPO 用 value/critic 估计 baseline，训练成本和显存高。Group Relative Policy Optimization 对每个 prompt $x$ 从旧策略采样 $G$ 条回复 $y_1,\ldots,y_G$，获得奖励 $r_i$，以组内统计构造优势：

$$
A_i=\frac{r_i-\operatorname{mean}(r_{1:G})}
{\operatorname{std}(r_{1:G})+\varepsilon}.
$$

因此无需单独 critic：同一问题的其他候选就是 baseline。若整组奖励相同，优势接近 0，这个 prompt 几乎不提供学习信号。

## 2. GRPO 目标

对回复 token 的重要性比

$$
\rho_{i,t}(\theta)=
\frac{\pi_\theta(y_{i,t}\mid x,y_{i,<t})}
{\pi_{old}(y_{i,t}\mid x,y_{i,<t})}.
$$

常见 clipped 目标为

$$
\mathcal L_{GRPO}= -\frac1G\sum_i\frac1{|y_i|}\sum_t
\min\left(\rho_{i,t}A_i,
\operatorname{clip}(\rho_{i,t},1-\epsilon,1+\epsilon)A_i\right)
+\beta D_{KL}(\pi_\theta\|\pi_{ref}).
$$

组级奖励被广播到回复 token；长度归一化避免长回复仅因 token 更多而产生更大梯度。实现变体在 KL 估计、按 token/序列聚合和标准差归一化上可能不同，比较实验时必须写清公式。

## 3. 可验证奖励 RLVR

数学、代码和结构化任务可用规则提供较可靠奖励：

- 数学：最终答案规范化后 exact match；
- 代码：编译、单元测试与沙箱执行；
- 格式：XML/JSON 标签、长度、工具调用语法；
- 证明/过程：可加入过程检查器，但验证器本身也可能有漏洞。

总奖励可组合：

$$
r=w_{acc}r_{acc}+w_{fmt}r_{fmt}+w_{safe}r_{safe}+\cdots.
$$

奖励设计决定模型会优化什么。只奖励最终答案可能学到碰巧猜中或利用解析器；格式奖励太大可能产生“格式完美但内容错误”的模型。

## 4. 推理能力与可见思维链

强化学习可以增加探索，使模型发现更长的分解、验证和回溯策略，但“输出更长”不等于“推理更好”。需要区分：

- answer accuracy 是否提升；
- pass@k 与单次准确率；
- 推理 token/延迟成本；
- 对题型、难度和语言的泛化；
- 过程是否忠实，还是仅生成看似合理的解释。

公开 chain-of-thought 还涉及安全、隐私和可操纵性；应用可以让模型内部计算并只输出简洁可验证解释。

## 5. 训练稳定性

### 采样多样性

温度过低时组内回复相同，优势退化；过高时大量无效样本。组大小 $G$ 增加相对估计稳定性，也线性提高 rollout 成本。

### 奖励尺度

组内标准化使不同 prompt 的奖励尺度更可比，但当标准差极小时会放大噪声。可设置 $\varepsilon$、过滤全同组、使用不除标准差的变体，或增加难度课程学习。

### KL 与熵

KL 太弱会模式坍塌或奖励利用，太强则限制学习；熵过快下降意味着探索消失。监控每种 reward、组内方差、回复长度、KL、entropy、clip ratio 和离线能力回归。

## 6. 端到端伪代码

```python
for prompts in loader:
    responses, old_logp = rollout(old_policy, prompts, group_size=G)
    rewards = verifier(prompts, responses)
    advantages = group_normalize(rewards)

    new_logp = policy.log_prob(prompts, responses)
    ratio = (new_logp - old_logp).exp()
    pg = minimum(ratio * advantages,
                 ratio.clip(1 - eps, 1 + eps) * advantages)
    loss = -masked_mean(pg) + beta * kl_to_reference(...)
    loss.backward()
    optimizer.step()
```

真实系统还需冻结 rollout snapshot、处理 padding mask、分布式生成、去重、奖励超时与可复现 seed。

## 7. GRPO 的边界

- 相对奖励只告诉“组内谁更好”，不会自动修复有偏 verifier。
- 全错组没有有效正方向，全对组也缺少区分信号。
- 算法省掉 critic，但 rollout、验证和多模型服务仍昂贵。
- 在不可验证的开放问答上，依赖 RM/judge 会重新引入偏见和 reward hacking。
