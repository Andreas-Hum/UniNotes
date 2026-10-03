---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Training Tricks]]

What is the expected initial cross-entropy loss for a 100-class classifier?::$\log 100\approx4.61$.

Why does He initialization use variance $2/n_{in}$ rather than $1/n_{in}$?::ReLU zeroes about half of its inputs, so $\mathbb E[h^2]=\tfrac12\mathrm{Var}(z)$; the factor 2 compensates to keep the variance constant across layers.

You train a Transformer on variable-length text. BatchNorm or LayerNorm, and why?::LayerNorm: it normalises each token's features independently of the batch and of sequence length.

Why is global-norm clipping preferred over clipping each gradient element?::It rescales all gradients by the same factor, preserving the update direction; element-wise clipping distorts the direction.

Your model cannot drive the loss on 10 training examples near zero. What does that tell you?::There is a bug or a gross misconfiguration (loss, labels, learning rate, gradient flow); fix that before training on the full dataset.
