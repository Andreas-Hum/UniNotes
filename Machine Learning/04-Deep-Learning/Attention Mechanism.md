---
tags: [ml, deep-learning, attention, transformers]
---
# Attention Mechanism

> [!summary] In one sentence
> Attention lets each position build its output as a **weighted average of values**, where the weights come from how well its **query** matches every **key**: $\mathrm{softmax}(QK^\top/\sqrt{d_k})V$.

## Intuition first
Think of a library search. You walk in with a **query** ("books about cats"). Every book has a **key** (its catalogue entry) and a **value** (its content). You score every catalogue entry against your query, turn the scores into percentages, and leave with a blend of the contents, weighted towards the best matches.

Attention does this with vectors, and it is **soft**: instead of picking the single best match (a hard lookup), every value contributes a bit, so the whole operation is differentiable and can be trained with [[Backpropagation]].

Why it matters: an [[RNN and LSTM|RNN]] has to squeeze everything it has read into one hidden state. Attention lets the model **look back directly** at any position, however far away. That solved the bottleneck in machine translation (Bahdanau et al. 2014) and later became the whole architecture ([[Transformers]], "Attention Is All You Need").

## Where Q, K and V come from
Given input token vectors stacked as rows of $X\in\mathbb R^{n\times d}$, three learned matrices project them:
$$Q=XW_Q,\quad K=XW_K,\quad V=XW_V,\qquad W_Q,W_K\in\mathbb R^{d\times d_k},\ W_V\in\mathbb R^{d\times d_v}$$
- **Query** $q_i$: what token $i$ is looking for.
- **Key** $k_j$: what token $j$ offers as a match.
- **Value** $v_j$: what token $j$ hands over if it is attended to.
The same token gets three different "roles" because matching (keys) and content (values) are different jobs.

| Kind | Queries from | Keys/values from | Used in |
|---|---|---|---|
| **Self-attention** | sequence $X$ | the same $X$ | encoder, decoder |
| **Cross-attention** | decoder states | encoder outputs | translation, image captioning, text-to-image |
| **Causal (masked) self-attention** | $X$ | only positions $\le i$ | GPT-style decoders |

## The math, step by step
**1. Scores.** $S=QK^\top\in\mathbb R^{n\times n}$, with $S_{ij}=q_i\cdot k_j$ (dot-product similarity).

**2. Scale.** Divide by $\sqrt{d_k}$. If the entries of $q$ and $k$ are independent with mean 0 and variance 1, then $q\cdot k=\sum_{t=1}^{d_k}q_tk_t$ has variance $d_k$. Without scaling, large $d_k$ gives huge scores, softmax saturates to almost one-hot, and the gradients vanish.

**3. Mask (optional).** Add $M_{ij}=-\infty$ where attention is not allowed: future positions (causal mask) or padding tokens. After softmax these weights become exactly 0.

**4. Softmax row-wise.** $A=\mathrm{softmax}(S/\sqrt{d_k}+M)$, so every row sums to 1: $A_{ij}=\dfrac{e^{s_{ij}/\sqrt{d_k}}}{\sum_{j'}e^{s_{ij'}/\sqrt{d_k}}}$.

**5. Mix values.** Output $O=AV\in\mathbb R^{n\times d_v}$, i.e. $o_i=\sum_jA_{ij}v_j$.

$$\boxed{\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}+M\Big)V}$$

## Multi-head attention
One head can only express one kind of relation (e.g. "which noun does this pronoun refer to"). With $h$ heads, each has its own projections of size $d_k=d_v=d/h$:
$$\mathrm{head}_i=\mathrm{Attention}(XW_Q^{(i)},XW_K^{(i)},XW_V^{(i)}),\qquad \mathrm{MHA}(X)=\mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)W_O$$
with $W_O\in\mathbb R^{d\times d}$. The total cost is about the same as one big head, but the heads can specialise (syntax, coreference, position, …).

**Shapes for one layer** ($n$ tokens, model width $d$, $h$ heads, batch $B$):

| Tensor | Shape |
|---|---|
| $X$ | $B\times n\times d$ |
| $Q,K,V$ after split into heads | $B\times h\times n\times d/h$ |
| scores $QK^\top$ | $B\times h\times n\times n$ |
| output after concat + $W_O$ | $B\times n\times d$ |
| parameters | $4d^2$ (+ biases) |

## Cost and efficient variants
- Time $O(n^2d)$ and memory $O(n^2)$ per layer for the score matrix: the bottleneck for long sequences.
- **KV cache** (inference): when generating token $t$, the keys and values of tokens $1..t-1$ do not change, so store them and compute only the new query. Generation then costs $O(n d)$ per token instead of recomputing everything.
- **Multi-query (MQA) / grouped-query attention (GQA):** heads share keys and values (all heads, or groups of heads), shrinking the KV cache with little quality loss. Used in Llama 2/3 and most modern LLMs.
- **FlashAttention:** the exact same maths, computed in tiles that stay in fast GPU memory, so the $n\times n$ matrix is never written out. Faster and uses $O(n)$ memory.
- **Sparse / sliding-window / linear attention:** restrict or approximate which pairs interact to get below $O(n^2)$.
- **Positional information:** attention itself is permutation-invariant (shuffle the tokens and the outputs shuffle the same way), so position must be added: sinusoidal or learned embeddings, **RoPE** or **ALiBi** (see [[Transformers]]).

## Before Transformers: additive attention
Bahdanau (2014) scored with a small network instead of a dot product: $e_{ij}=v^\top\tanh(W_sh_{i-1}+W_hh_j)$, then $\alpha_{ij}=\mathrm{softmax}_j(e_{ij})$ and the context vector $c_i=\sum_j\alpha_{ij}h_j$ fed the RNN decoder. Luong (2015) introduced the cheaper multiplicative (dot-product) score that Transformers use.

## Worked example
Two tokens, $d_k=2$, no mask.
$Q=\begin{pmatrix}1&0\\0&1\end{pmatrix}$, $K=\begin{pmatrix}1&0\\1&1\end{pmatrix}$, $V=\begin{pmatrix}10&0\\0&10\end{pmatrix}$.

1. $QK^\top=\begin{pmatrix}1&1\\0&1\end{pmatrix}$.
2. Divide by $\sqrt2$: $\begin{pmatrix}0.707&0.707\\0&0.707\end{pmatrix}$.
3. Softmax row 1: equal scores → $(0.5,0.5)$. Row 2: $e^0=1$, $e^{0.707}=2.03$ → $(0.33,0.67)$.
4. $O=AV$: row 1 $=0.5(10,0)+0.5(0,10)=(5,5)$; row 2 $=0.33(10,0)+0.67(0,10)=(3.3,6.7)$.

Token 1's query matches both keys equally, so it gets an even blend; token 2's query only matches key 2, so its output leans towards $v_2$ (but never fully, because softmax never gives exactly 0).

**With a causal mask:** token 1 may only see itself → row 1 becomes $(1,0)$ and $o_1=(10,0)$; row 2 is unchanged.

## In code
```python
import torch, torch.nn.functional as F

def attention(q, k, v, mask=None):            # q,k,v: (..., n, d_k)
    scores = q @ k.transpose(-2, -1) / q.size(-1) ** 0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    return F.softmax(scores, dim=-1) @ v

n = 5
causal = torch.tril(torch.ones(n, n))          # 1 = allowed, 0 = future
# PyTorch's built-in (uses FlashAttention when available):
# F.scaled_dot_product_attention(q, k, v, is_causal=True)
```

## Common confusions
- **"Q, K and V are different inputs."** → In self-attention they are three projections of the **same** input. Only in cross-attention do queries come from a different sequence.
- **"Attention weights explain the model."** → They show where information was mixed in one layer and head, not why the prediction was made; residual paths and MLPs matter too.
- **"$\sqrt{d_k}$ is a tuning trick."** → It keeps the score variance at about 1 regardless of head size, which keeps softmax out of saturation.
- **"Masking means multiplying by 0 after softmax."** → Add $-\infty$ **before** softmax; zeroing afterwards breaks the sum-to-one property.
- **"More heads = more parameters."** → With $d_k=d/h$ the parameter count stays $4d^2$.

## Check yourself
> [!question]- Why does a decoder-only LLM need a causal mask during training but can use a KV cache during inference?
> Training processes the whole sequence in parallel, so the mask stops position $i$ from seeing the tokens it is meant to predict. At inference tokens arrive one by one; past keys/values never change, so they are cached and only the new token's query is computed.

> [!question]- With $d=512$ and $h=8$, what is $d_k$, and what is the shape of the score tensor for batch 4 and 100 tokens?
> $d_k=64$; scores are $4\times8\times100\times100$.

> [!question]- What happens to the attention distribution if you forget the $\sqrt{d_k}$ scaling with $d_k=1024$?
> Score magnitudes grow by about $\sqrt{1024}=32$×, so softmax becomes nearly one-hot and its gradients nearly zero; training becomes slow or unstable.

> [!question]- If you shuffle the input tokens of a self-attention layer without positional encodings, what happens to the outputs?
> They are shuffled in the same way (permutation equivariance): attention by itself knows nothing about order.

## Practice

[Attention Mechanism - Exercises](Attention%20Mechanism%20-%20Exercises.ipynb): Q/K/V roles, masks and temperature, causal attention, shape and KV-cache arithmetic (with GQA) by hand, then NumPy implementations of batched masked attention, cross-attention, multi-head attention with reshapes, additive attention, incremental decoding with a KV cache, grouped-query attention, the online softmax behind FlashAttention and the backward pass.

## Learn more
- [Attention Is All You Need — Vaswani et al. 2017](https://arxiv.org/abs/1706.03762)
- [Neural Machine Translation by Jointly Learning to Align and Translate — Bahdanau et al. 2014](https://arxiv.org/abs/1409.0473)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [FlashAttention — Dao et al. 2022](https://arxiv.org/abs/2205.14135)
- [GQA — Ainslie et al. 2023](https://arxiv.org/abs/2305.13245)
- [Karpathy — Let's build GPT](https://karpathy.ai/zero-to-hero.html)

See [[Transformers]], [[RNN and LSTM]], [[LLMs Overview]].
