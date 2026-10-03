---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Activation Functions]]

What is the maximum of $\sigma'(z)$ and where is it attained?::$0.25$ at $z=0$, because $\sigma(0)=0.5$ and $\sigma'=\sigma(1-\sigma)=0.5\cdot0.5$.

Why can a dead ReLU unit not recover on its own?::Its pre-activation is negative for every input, so its output and its gradient are 0 for every input; no gradient ever reaches its weights or bias.

Which activation would you use for LSTM gates, and why?::Sigmoid: a gate multiplies a signal by a value in (0,1), meaning "what fraction to let through".

Why subtract $\max_j z_j$ before computing softmax?::Softmax is shift invariant, so the result is unchanged, but the largest exponent becomes $e^0=1$, which prevents overflow for large logits.

Why is tanh usually preferred over sigmoid in hidden layers (when you must use one of them)?::It is zero-centred and its derivative at 0 is 1 rather than 0.25, so gradients shrink less per layer.
