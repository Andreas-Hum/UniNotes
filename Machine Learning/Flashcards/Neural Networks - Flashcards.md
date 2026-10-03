---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Neural Networks]]

A network with layer sizes $20\to 10\to 3$ has how many parameters?::$(20+1)\cdot 10 + (10+1)\cdot 3 = 210 + 33 = 243$.

Why can't a deep network with $\phi(z)=z$ solve XOR?::The composition of affine maps is affine, so the whole network is one linear model; XOR's classes are not linearly separable in input space.

You need to predict a probability distribution over 5 star ratings. Output layer and loss?::5 output units with softmax, trained with cross-entropy.

What does the universal approximation theorem fail to guarantee?::How many hidden units are needed, that gradient descent finds the approximating weights, and that the trained network generalises beyond the training data.

In the worked example, why did the output not depend on $W^{(2)}$ for $x=(1,-1)$?::Both hidden units had $z\le 0$, so ReLU output 0 for both; only the output bias $b^{(2)}=2$ remained.
