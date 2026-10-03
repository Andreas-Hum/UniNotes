---
tags: [ml, project, transformers, attention]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Build a Transformer from Scratch

> [!summary] In one sentence
> Build the original encoder–decoder Transformer yourself (attention, multi-head attention, positional encoding, a decoder with cross-attention, greedy decoding) and teach it to translate messy Danish dates like *fredag den 3. oktober 2026* into `2026-10-03`.

**Notebook:** [Project - Build a Transformer from Scratch](Project%20-%20Build%20a%20Transformer%20from%20Scratch.ipynb) · topic: [[Transformers]] · all projects: [[Projects Overview]]

## What you build
1. `attention`: scaled dot-product attention with a mask (checked against PyTorch).
2. `MultiHeadAttention.forward`: split/merge heads (checked against `nn.MultiheadAttention` with the same weights).
3. `positional_encoding`: sinusoids.
4. `DecoderLayer.forward`: masked self-attention + **cross-attention** + feed-forward, pre-LN residuals.
5. `greedy_decode`: autoregressive generation.

Then: train with teacher forcing and plot where the decoder looks.

## Reference results (solution, laptop CPU)
| | value |
|---|---|
| model | 2 encoder + 2 decoder layers, d = 64, 4 heads, 172k parameters |
| data | 27k generated Danish dates in 7 formats, 1900–2099 |
| exact match on 3,000 test dates | **100 %** after 6 epochs (≈ 45 s CPU) |

The cross-attention map shows the year digits attending to *2026*, the month to *okt…* and the day to *3*, an alignment nobody programmed.

**Bug worth learning from:** multiplying embeddings by √d (as in the paper) with PyTorch's std-1 embeddings drowned the positional encoding. The model then swapped digits (*2062* for *2026*) and reached only 65 % after 15 epochs.

## Check yourself
> [!question]- Why does the decoder need two attention layers but the encoder only one?
> Self-attention lets the decoder see what it has already written (masked, so no peeking ahead); cross-attention lets it read the source. The encoder only needs to relate source characters to each other.

> [!question]- What's the difference from the Mini-GPT?
> GPT is decoder-only: one stream of text, causal self-attention, no cross-attention. Encoder–decoder models read the whole input bidirectionally first, which suits translation-like tasks.

> [!question]- Why did √d scaling hurt here?
> The paper's embeddings are initialised small (std ≈ 1/√d), so ×√d brings them to the scale of the positional encoding. `nn.Embedding` starts at std 1, so ×√d made them 8× larger than the positions, and order information got lost.

## Learn more
- [Vaswani et al. – Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Related: [[Mini-GPT on Danish]] (decoder-only) · [[Attention Mechanism]] · [[Project - BPE Tokenizer on My Notes]]

---
Back to [[00 - Machine Learning Index]].
