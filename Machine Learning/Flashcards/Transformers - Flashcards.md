---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Transformers]]

Why is a causal mask needed in GPT but not in BERT?::GPT is trained to predict the next token, so position $i$ must not see tokens $j>i$ (that would be cheating); BERT predicts masked tokens from both sides, so full bidirectional attention is allowed.

What is the time and memory cost of attention in the sequence length $n$?::$O(n^2d)$ time and $O(n^2)$ memory for the score matrix: doubling the context quadruples the attention cost.

If $q,k$ have i.i.d. unit-variance components, what is $\mathrm{Var}(q\cdot k)$ for $d_k=64$, and after scaling?::$64$; after dividing by $\sqrt{64}=8$ it is 1.

Write the pre-LN residual update.::$x\leftarrow x+\mathrm{Sublayer}(\mathrm{LN}(x))$, applied once for attention and once for the MLP.

How many tokens does ViT-Base see for a $224\times224$ image with $16\times16$ patches?::$(224/16)^2=14^2=196$ patch tokens (plus one [CLS] token).
