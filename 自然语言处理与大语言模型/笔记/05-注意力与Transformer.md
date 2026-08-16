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

## 9. 机器翻译目标与教师强制

Transformer 最初用于条件语言建模。给定平行语料 $(x^{(i)},y^{(i)})$，训练目标为

$$
\mathcal L=-\sum_i\sum_t\log p_\theta
(y_t^{(i)}\mid y_{<t}^{(i)},x^{(i)}).
$$

训练时 decoder 输入是真实目标句右移一位，因果 mask 使位置 $t$ 看不到未来标签；所有位置仍可在一次矩阵计算中并行。推理时没有真实目标前缀，只能逐 token 生成，这解释了“训练高度并行、解码仍然串行”的区别。

原论文使用标签平滑。若平滑系数为 $\epsilon$，真实类不再占概率 1，而与其他类别分享一小部分质量。它降低过度自信，改善 BLEU，但可能让训练 perplexity 看起来略差，因此不能机械用训练 loss 判断泛化。

## 10. Encoder、Decoder 与 Cross-Attention 的数据流

Encoder self-attention 的 Q/K/V 都来自源序列，只有 padding mask。Decoder 的第一层 attention 使用 causal mask，Q/K/V 都来自目标前缀；cross-attention 中 Q 来自 decoder，K/V 来自 encoder 最终表示：

$$
\operatorname{CrossAttn}(H_y,H_x)
=\operatorname{softmax}\left(
\frac{H_yW^Q(H_xW^K)^T}{\sqrt{d_k}}
\right)H_xW^V.
$$

因此 decoder 可以一边保持目标端语言流畅，一边按当前位置读取源端证据。纯 decoder LLM 把指令、资料和回答拼成一个因果序列，不再使用独立 cross-attention。

## 11. Add & Norm、Pre-LN 与 Post-LN

原始 Transformer 是 Post-LN：子层输出先与残差相加，再做 LayerNorm。现代深层 LLM 常用 Pre-LN：先归一化再进入子层，残差主干保持更接近恒等映射，梯度更稳定。两者不是仅改变一行代码：初始化、学习率、最终是否需要额外 LayerNorm 都会不同。

LayerNorm 对单个 token 的隐藏维归一化：

$$
\operatorname{LN}(x)=\gamma\odot
\frac{x-\mu}{\sqrt{\sigma^2+\varepsilon}}+\beta.
$$

它不依赖 batch 大小。RMSNorm 省去减均值，只按均方根缩放，计算更简单，已被许多 decoder-only 模型采用。

## 12. 参数量估算

若模型维度为 $d$、FFN 维度为 $d_{ff}$，一层标准 Transformer 的主要权重是：

- Q/K/V 与输出投影：约 $4d^2$；
- 两层 FFN：约 $2dd_{ff}$；
- LayerNorm 与 bias：相对较小。

当 $d_{ff}=4d$ 时，每层约 $12d^2$ 参数。再加 token embedding $\lvert\mathcal V\rvert d$ 与输出头；若输入输出权重绑定，可以少一份大词表矩阵。课堂以 $d=768$、12 层、词表 30522 为例，可得到约 110M 量级，这与 BERT-base 对上。参数量估算是检查实现 shape 和显存预算的有效手段。

## 13. 复杂度要按训练与解码分别看

Self-attention 的矩阵计算约为 $O(T^2d)$，线性投影和 FFN 约为 $O(Td^2)$。当 $T\ll d$ 时，FFN/投影可能更贵；当上下文很长时，$T^2$ 注意力成为瓶颈。训练能在 $T$ 个位置并行，自回归 decode 却一次只有一个 query，此时 KV cache 的读带宽往往比 FLOPs 更关键。
