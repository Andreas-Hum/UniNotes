---
tags: [ml, deep-learning, sequence]
---
# RNN and LSTM

Recurrent net: $h_t=\phi(W_hh_{t-1}+W_xx_t+b)$, shared weights across time; trained with backpropagation through time ([[Backpropagation]]).

## Problem
Gradients vanish/explode over long sequences.

## LSTM
Gates control a cell state $c_t$:
$f_t=\sigma(\cdot)$ (forget), $i_t=\sigma(\cdot)$ (input), $o_t=\sigma(\cdot)$ (output),
$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t,\quad h_t=o_t\odot\tanh c_t$.
**GRU**: fewer gates, similar performance.

## Variants
Bidirectional, stacked, seq2seq with attention. Largely replaced by [[Transformers]] for NLP, but still used for small/streaming problems.

## Learn more
- [Dive into Deep Learning](https://d2l.ai/)
- [colah – Understanding LSTMs](https://colah.github.io/)
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
