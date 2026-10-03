---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Attention Mechanism]]

Why does a decoder-only LLM need a causal mask during training but can use a KV cache during inference?::Training processes the whole sequence in parallel, so the mask stops position $i$ from seeing the tokens it is meant to predict. At inference tokens arrive one by one; past keys/values never change, so they are cached and only the new token's query is computed.

With $d=512$ and $h=8$, what is $d_k$, and what is the shape of the score tensor for batch 4 and 100 tokens?::$d_k=64$; scores are $4\times8\times100\times100$.

What happens to the attention distribution if you forget the $\sqrt{d_k}$ scaling with $d_k=1024$?::Score magnitudes grow by about $\sqrt{1024}=32$×, so softmax becomes nearly one-hot and its gradients nearly zero; training becomes slow or unstable.

If you shuffle the input tokens of a self-attention layer without positional encodings, what happens to the outputs?::They are shuffled in the same way (permutation equivariance): attention by itself knows nothing about order.
