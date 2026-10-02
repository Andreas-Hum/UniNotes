---
tags: [ml, deep-learning, nlp, attention]
---
# Transformers

*Attention Is All You Need* (Vaswani et al., 2017).

## Scaled dot-product attention
$$\mathrm{Attn}(Q,K,V)=\mathrm{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V$$
Multi-head: several attention maps in parallel, concatenated. Cost $O(n^2d)$ in sequence length.

## Block
Self-attention → add & LayerNorm → position-wise MLP → add & LayerNorm. Residual connections as in [[CNN|ResNet]]. Positional information: sinusoidal, learned, RoPE, ALiBi.

## Families
| Type | Example | Objective |
|---|---|---|
| Encoder-only | BERT | masked LM |
| Decoder-only | GPT, Llama | next-token prediction |
| Encoder–decoder | T5, original | seq2seq |
| Vision | ViT | patches as tokens |

## Training recipe
AdamW + warm-up + cosine decay, pre-LN, mixed precision, gradient clipping ([[Optimizers]], [[Training Tricks]]).

## Beyond
Fine-tuning, LoRA, RLHF ([[Q-Learning and Policy Gradients]]), retrieval-augmented generation, KV-cache, FlashAttention. Graph attention: [[Graph Neural Networks]].
