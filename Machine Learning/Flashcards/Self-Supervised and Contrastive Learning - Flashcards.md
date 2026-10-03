---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Self-Supervised and Contrastive Learning]]

Why does a loss that only pulls positive pairs together fail?::The constant map (every input to the same embedding) makes all positives agree perfectly: collapse. Something must push apart or break the symmetry (negatives, stop-gradient, EMA teacher, reconstruction).

What is the InfoNCE loss of a fully collapsed encoder with $2N-1$ candidates?::All similarities are equal, so $p_{\text{pos}}=1/(2N-1)$ and $\ell=\log(2N-1)$.

What does lowering the temperature $\tau$ do?::It sharpens the softmax, so the loss and gradients concentrate on the hardest negatives; too low becomes unstable, too high treats all negatives alike.

What is a linear probe, and why use it?::A linear classifier trained on frozen features; it measures how linearly separable the representation is without letting fine-tuning hide a weak encoder.

Which family does MAE belong to, and what is its pretext task?::Masked modeling: reconstruct the pixels of randomly masked image patches.
