---
tags: [ml, deep-learning, nlp, attention]
---
# Transformers

> [!summary] In one sentence
> A Transformer processes a whole sequence at once and lets every token decide, through learned query–key comparisons, how much to read from every other token (attention), stacking this with small per-token MLPs, residual connections and LayerNorm into the architecture behind BERT, GPT, ViT and modern LLMs.

*Attention Is All You Need* (Vaswani et al., 2017).

See also [[Attention Mechanism]] for a deeper look at Q, K, V, masking, multi-head shapes and KV caching.

## Intuition first

Consider "The cat sat because **it** was tired." To understand *it*, you look back at the other words and decide that *cat* is the one that matters. Attention turns that into arithmetic:

- Every token emits a **query** ("what am I looking for?"), a **key** ("what do I contain?") and a **value** ("what will I hand over if you pick me?").
- A token compares its query with every key (dot products). High score = relevant.
- A softmax turns the scores into weights that are positive and sum to 1.
- The token's new representation is the weighted average of all values.

It is a soft, differentiable dictionary lookup: instead of retrieving the one entry whose key matches exactly, you retrieve a blend of all entries, weighted by how well they match.

Why this beat RNNs ([[RNN and LSTM]]): an RNN passes information step by step, so a link between word 1 and word 50 has to survive 49 updates, and the steps cannot run in parallel. In attention every pair of tokens is connected directly (path length 1), and all positions are computed at once on a GPU.

![Attention weights from the query "it" concentrate on "cat"; switching the query to "tired" changes the pattern](../../Attachments/ML%20Animations/Transformers%20-%20attention%20weights.gif)

*Watch the raw scores turn into softmax weights that sum to 1 (the bars), the thickest arc land on "cat", and the whole pattern change when a different token asks the question: each token gets its own weighting.*

## Scaled dot-product attention

$$\mathrm{Attn}(Q,K,V)=\mathrm{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V$$

Multi-head: several attention maps in parallel, concatenated. Cost $O(n^2d)$ in sequence length.

## The math, step by step

**1. Projections.** Stack the $n$ token embeddings as rows of $X\in\mathbb R^{n\times d}$. Learned matrices give
$Q=XW_Q,\ K=XW_K,\ V=XW_V$, with $Q,K\in\mathbb R^{n\times d_k}$ and $V\in\mathbb R^{n\times d_v}$. In self-attention all three come from the same $X$; in cross-attention (encoder–decoder) $Q$ comes from the decoder and $K,V$ from the encoder.

**2. Scores.** $S=QK^\top/\sqrt{d_k}\in\mathbb R^{n\times n}$. Entry $S_{ij}=q_i\cdot k_j/\sqrt{d_k}$ says how relevant token $j$ is to token $i$.

**3. Why divide by $\sqrt{d_k}$.** If the components of $q$ and $k$ are independent with mean 0 and variance 1, then $q\cdot k=\sum_{m=1}^{d_k}q_mk_m$ is a sum of $d_k$ terms of variance 1, so $\mathrm{Var}(q\cdot k)=d_k$. For $d_k=512$ typical scores are around $\pm22$, the softmax becomes nearly one-hot (saturates) and its gradients vanish. Dividing by $\sqrt{d_k}$ brings the variance back to 1.

**4. Softmax, row by row.** $A=\mathrm{softmax}(S)$, each row sums to 1: $A_{ij}=\frac{e^{S_{ij}}}{\sum_{j'}e^{S_{ij'}}}$. Implement it stably by subtracting the row maximum first (the result is unchanged, but $e^{\cdot}$ cannot overflow).

**5. Mix the values.** Output $=AV$: row $i$ is $\sum_j A_{ij}v_j$.

**Masks.** A **causal mask** sets $S_{ij}=-\infty$ for $j>i$ before the softmax, so a token cannot look at the future (decoders, GPT). A **padding mask** hides padding tokens.

**Multi-head attention.** Split the width $d$ into $h$ heads of size $d_k=d/h$, run attention in each with its own projections, concatenate and mix with $W_O$:
$$\mathrm{MHA}(X)=\mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)\,W_O,\qquad \mathrm{head}_i=\mathrm{Attn}(XW_Q^{(i)},XW_K^{(i)},XW_V^{(i)})$$
Different heads can specialise (one tracks syntax, another coreference like it→cat) at roughly the cost of one full-width head.

**Cost.** The projections cost $O(nd^2)$; the score matrix $QK^\top$ and the product $AV$ cost $O(n^2d)$ time and $O(n^2)$ memory. For long sequences the $n^2$ term dominates, which is why long-context work focuses on making attention cheaper (FlashAttention, sparse or linear attention).

**Positions.** Attention by itself is **permutation-equivariant**: shuffling the input rows just shuffles the output rows, so "dog bites man" and "man bites dog" look the same. Position information must be added. Sinusoidal encodings:
$$PE_{p,2i}=\sin\!\big(p/10000^{2i/d}\big),\qquad PE_{p,2i+1}=\cos\!\big(p/10000^{2i/d}\big)$$
(each pair of dimensions is a clock ticking at a different speed). **RoPE** instead rotates each pair $(x_{2i},x_{2i+1})$ of a query/key at position $m$ by angle $m\theta_i$, $\theta_i=10000^{-2i/d}$, so that $q_m\cdot k_n$ depends only on the offset $m-n$.

## Block

Self-attention → add & LayerNorm → position-wise MLP → add & LayerNorm. Residual connections as in [[CNN|ResNet]]. Positional information: sinusoidal, learned, RoPE, ALiBi.

- **Self-attention** mixes information *between* tokens.
- **Position-wise MLP** ($W_2\,\mathrm{ReLU}(W_1x)$, usually $d_{ff}=4d$) processes each token *on its own*; most parameters live here.
- **Add (residual)**: $x+\mathrm{Sublayer}(x)$ keeps an identity path for the gradient, exactly the ResNet trick.
- **LayerNorm** normalises each token vector: $\hat x=(x-\mu)/\sqrt{\sigma^2+\epsilon}$, $y=\gamma\odot\hat x+\beta$, with $\mu,\sigma^2$ computed over that token's features (not over the batch).
- The order above is the original **post-LN** block, $x\leftarrow\mathrm{LN}(x+\mathrm{Sublayer}(x))$. Modern models use **pre-LN**, $x\leftarrow x+\mathrm{Sublayer}(\mathrm{LN}(x))$, which leaves the residual path completely clean and trains more stably in deep stacks.

Parameters of one block with width $d$: attention $4d^2$ ($W_Q,W_K,W_V,W_O$) plus MLP $2\cdot d\cdot4d=8d^2$, so about $12d^2$ (plus biases and LayerNorm).

## Worked example

One query $q=(2,0)$, three keys $k_1=(1,0)$, $k_2=(0,1)$, $k_3=(1,1)$, values $v_1=(1,0)$, $v_2=(0,1)$, $v_3=(2,2)$, $d_k=2$.

1. Dot products: $q\cdot k=(2,0,2)$. Scaled by $1/\sqrt2$: $(1.414,\,0,\,1.414)$.
2. Softmax: $e^{1.414}=4.11$, $e^0=1$, so the weights are $(4.11,1,4.11)/9.23=(0.446,\,0.108,\,0.446)$.
3. Output: $0.446\,(1,0)+0.108\,(0,1)+0.446\,(2,2)=(1.34,\,1.00)$.

Keys 1 and 3 match the query equally well and dominate; key 2 is orthogonal to the query but still gets a little weight, because softmax never gives exactly zero.

**Sizes in practice.** One encoder block with $d=512$, $h=8$, $d_{ff}=2048$: attention $4(512^2+512)=1{,}050{,}624$, MLP $2{,}099{,}712$, about $3.15$M parameters in total ($\approx12d^2$). The **KV-cache** of a 32-layer decoder with $d=4096$, context 2048, fp16: $2\,(K,V)\times32\times2048\times4096\times2\text{ bytes}=1$ GiB per sequence.

## Families

| Type | Example | Objective |
|---|---|---|
| Encoder-only | BERT | masked LM |
| Decoder-only | GPT, Llama | next-token prediction |
| Encoder–decoder | T5, original | seq2seq |
| Vision | ViT | patches as tokens |

- **Encoder-only** uses no mask (every token sees the whole input): good for understanding tasks such as classification and retrieval.
- **Decoder-only** uses a causal mask and generates one token at a time: the LLM architecture ([[LLMs Overview]]).
- **Encoder–decoder**: bidirectional encoder, causal decoder plus cross-attention; natural for translation and summarisation.
- **ViT** cuts an image into $16\times16$ patches, embeds each as a token, and runs a plain encoder (see [[Computer Vision Overview]]).

## Training recipe

AdamW + warm-up + cosine decay, pre-LN, mixed precision, gradient clipping ([[Optimizers]], [[Training Tricks]]).

Why each: warm-up avoids huge, badly-estimated Adam steps at the start, when the second-moment estimates are still noisy; cosine decay anneals to a fine solution; pre-LN keeps gradients well-scaled through many layers; clipping guards against rare loss spikes; mixed precision halves memory and speeds up matrix multiplications.

## Beyond

Fine-tuning, LoRA, RLHF ([[Q-Learning and Policy Gradients]]), retrieval-augmented generation, KV-cache, FlashAttention. Graph attention: [[Graph Neural Networks]].

- **LoRA**: freeze the big weights and learn a low-rank update $\Delta W=BA$; cheap fine-tuning.
- **KV-cache**: during generation, keys and values of past tokens do not change, so store them and compute only the new token's row.
- **FlashAttention**: the same exact attention, computed in tiles that fit in fast on-chip memory, never materialising the $n\times n$ matrix.

## Common confusions

- "Attention weights explain the model's decision." → They show where information was read from in one layer and head, not a faithful causal explanation.
- "Self-attention knows word order." → Without positional information it is permutation-equivariant; order comes only from the positional encodings.
- "$\sqrt{d_k}$ is a tuning hack." → It exactly cancels the growth $\mathrm{Var}(q\cdot k)=d_k$ and keeps the softmax out of saturation.
- "Multi-head attention costs $h$ times more." → Each head works in $d/h$ dimensions, so the total cost is about that of a single full-width head.
- "LayerNorm is BatchNorm along another axis, so it depends on the batch." → It normalises each token over its own features and behaves identically at training and test time.

## Check yourself

> [!question]- Why is a causal mask needed in GPT but not in BERT?
> GPT is trained to predict the next token, so position $i$ must not see tokens $j>i$ (that would be cheating); BERT predicts masked tokens from both sides, so full bidirectional attention is allowed.

> [!question]- What is the time and memory cost of attention in the sequence length $n$?
> $O(n^2d)$ time and $O(n^2)$ memory for the score matrix: doubling the context quadruples the attention cost.

> [!question]- If $q,k$ have i.i.d. unit-variance components, what is $\mathrm{Var}(q\cdot k)$ for $d_k=64$, and after scaling?
> $64$; after dividing by $\sqrt{64}=8$ it is 1.

> [!question]- Write the pre-LN residual update.
> $x\leftarrow x+\mathrm{Sublayer}(\mathrm{LN}(x))$, applied once for attention and once for the MLP.

> [!question]- How many tokens does ViT-Base see for a $224\times224$ image with $16\times16$ patches?
> $(224/16)^2=14^2=196$ patch tokens (plus one [CLS] token).

## Practice

[Transformers - Exercises](Transformers%20-%20Exercises.ipynb): permutation equivariance, the model families, pre-LN and warm-up, attention and $\sqrt{d_k}$ by hand, parameter, compute and KV-cache counts, then NumPy implementations of stable softmax and attention, softmax saturation, causal masking, multi-head attention, sinusoidal encodings, RoPE, LayerNorm forward/backward and a full pre-LN encoder block.

## Learn more

- [MIT 6.S191 — sequence models & transformers lecture](https://www.youtube.com/playlist?list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Karpathy – Zero to Hero](https://karpathy.ai/zero-to-hero.html) (build GPT)
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/)
- [3Blue1Brown – Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc)
