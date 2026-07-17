---
title: "第 5 讲 注意力与 Transformer"
course: "自然语言处理与大语言模型"
---

# 第 5 讲 注意力与 Transformer

> 对应课程 `lecture-05-transformers` 与经典论文 [Attention Is All You Need](https://arxiv.org/abs/1706.03762)。

## 1. 从对齐到注意力

给定 query $q$、keys $k_i$、values $v_i$，注意力先计算相关性，再对 value 加权：

$$
e_i=\operatorname{score}(q,k_i),\qquad
\alpha_i=\frac{e^{e_i}}{\sum_j e^{e_j}},\qquad
c=\sum_i\alpha_i v_i.
$$

它把“所有信息压进一个固定向量”改为按当前需要读取。Q/K 决定寻址，V 承载被聚合内容。

## 2. Scaled Dot-Product Attention

对矩阵输入：

$$
\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.
$$

除以 $\sqrt{d_k}$ 是因为独立分量点积方差随维度增长；不缩放会让 softmax 过度饱和、梯度变小。mask $M$ 在禁止位置加 $-\infty$：padding mask 屏蔽补齐 token，causal mask 屏蔽未来 token。

张量形状检查是实现关键。设 batch $B$、序列长 $T$、模型维 $d$：

```text
X: (B,T,d)
Q,K,V: (B,h,T,d_k)
scores: (B,h,T,T)
output: (B,h,T,d_k) → concat → (B,T,d)
```

softmax 必须沿最后的 key 维进行。

## 3. Multi-Head Attention

每个头学习不同投影：

$$
\text{head}_i=\operatorname{Attention}(QW_i^Q,KW_i^K,VW_i^V),
$$

$$
\operatorname{MHA}=\operatorname{Concat}(\text{head}_1,\ldots,\text{head}_h)W^O.
$$

多头使模型能同时关注不同位置与关系，但“某头一定对应某种语言学结构”不是保证；注意力权重也不自动等于因果解释。

## 4. Transformer Block

标准 block 包含 token mixing 的自注意力和逐位置 channel mixing 的 FFN：

$$
\operatorname{FFN}(x)=W_2\phi(W_1x+b_1)+b_2.
$$

每层还使用残差、LayerNorm 与 dropout。现代大模型常用 Pre-LN：

$$
x'=x+\operatorname{MHA}(\operatorname{LN}(x)),qquad
y=x'+\operatorname{FFN}(\operatorname{LN}(x')).
$$

残差给深层网络提供恒等路径；LayerNorm 在每个 token 的特征维上归一化，不依赖 batch 统计，适合变长序列。

## 5. 位置信息

纯自注意力对输入置换等变，需要显式位置机制。

原论文正弦位置编码：

$$
PE_{(pos,2i)}=\sin(pos/10000^{2i/d}),\quad
PE_{(pos,2i+1)}=\cos(pos/10000^{2i/d}).
$$

此外有 learned absolute embedding、相对位置 bias、RoPE 和 ALiBi。RoPE 将 Q/K 的二维分量按位置旋转，使点积自然携带相对位置；长上下文外推仍依赖训练分布、频率缩放和注意力实现，不能只靠提高 `max_length`。

## 6. 三种架构

| 架构 | 可见上下文 | 典型预训练 | 擅长 |
| --- | --- | --- | --- |
| Encoder-only | 双向 | masked LM | 分类、抽取、表示 |
| Decoder-only | 左到右 causal | next-token LM | 开放生成、统一提示接口 |
| Encoder–Decoder | encoder 双向，decoder 因果并 cross-attend | denoising/span corruption | 翻译、摘要、条件生成 |

Decoder block 的 masked self-attention 只能看已生成前缀；encoder–decoder 还增加 cross-attention，其 Q 来自 decoder，K/V 来自 encoder。

## 7. 复杂度与局限

标准 self-attention 时间/显存核心为 $O(T^2)$，FFN 通常为 $O(Td^2)$。短序列时 FFN 也可能占主要 FLOPs；长序列时注意力矩阵成为瓶颈。RNN 的路径长度为 $O(T)$ 且不可完全并行，自注意力任意两 token 的交互路径为 $O(1)$，训练并行性更好。

常见优化包括 FlashAttention（精确但减少 HBM 往返）、稀疏/滑窗注意力、MQA/GQA 与 KV cache。它们改变系统开销，不应与模型学习目标混为一谈。

## 8. 从零实现检查表

- `d_model % n_heads == 0`。
- mask 在 softmax 前施加，且 dtype/设备一致。
- reshape 后正确 transpose，合并头前调用 contiguous 或等价安全操作。
- dropout 只在训练模式启用。
- causal 单元测试：改变未来 token 不应影响当前位置输出。
- attention 行概率和应约为 1，被 mask 位置应约为 0。

## 9. 自检清单

- 能由 Q/K/V 解释 self-attention 与 cross-attention。
- 能写出 scaled dot-product attention 并标注全部形状。
- 能比较 causal mask 和 padding mask。
- 能说明残差、LayerNorm、FFN 与位置编码各自作用。
- 能解释 Transformer 更易并行，但长上下文仍昂贵。
