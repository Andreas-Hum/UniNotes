---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[CNN]]

A $7\times7$ input, $3\times3$ kernel, padding 0, stride 2. What is the output size?::$\lfloor\frac{7-3+0}{2}\rfloor+1=2+1=3$, so $3\times3$.

How many weights does a $5\times5$ conv from 16 to 32 channels have (with biases)?::$16\cdot32\cdot25=12{,}800$ weights $+32$ biases $=12{,}832$, whatever the image size.

Why does a stack of 100 residual blocks train when 100 plain layers do not?::The Jacobian of each block is $I+J_F$, so the backward signal always has an identity path; in a plain stack it is a product of 100 Jacobians, which tends to shrink or blow up exponentially.

What is the receptive field after two $3\times3$ convs with stride 1?::$r=1+2+2=5$, i.e. $5\times5$.

Is global average pooling equivariant or invariant to shifts?::Invariant: it averages over all positions, so a shift (with circular borders) leaves the result unchanged.
