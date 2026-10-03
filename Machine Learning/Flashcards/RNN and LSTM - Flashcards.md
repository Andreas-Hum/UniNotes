---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[RNN and LSTM]]

Why does the number of RNN parameters not depend on the sequence length?::The same $W_h$, $W_x$ and $b$ are reused at every time step (weight sharing through time).

In the linear scalar RNN $h_t=w\,h_{t-1}+x_t$, what is $\partial h_T/\partial h_0$, and what happens for $w=0.5$, $T=10$?::$w^T=0.5^{10}\approx0.001$: the gradient from step 10 back to step 0 has essentially vanished.

Which LSTM equation creates the "gradient highway", and why?::$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t$: the old cell is only multiplied by the forget gate and added to, so $\partial c_t/\partial c_{t-1}=f_t$, with no weight matrix or squashing derivative.

How many parameters does an LSTM layer have compared with a vanilla RNN of the same sizes?::Four times as many: one RNN-sized block each for $f$, $i$, $o$ and $\tilde c$.

What does gradient clipping by global norm do to the direction of the update?::Nothing: all gradients are scaled by the same factor, so only the length is capped.
