---
tags: [ml, deep-learning]
---
# Activation Functions

| Name | $\phi(z)$ | Pros / cons |
|---|---|---|
| Sigmoid | $\frac1{1+e^{-z}}$ | outputs in (0,1); saturates → vanishing gradients |
| Tanh | $\tanh z$ | zero-centred; still saturates |
| **ReLU** | $\max(0,z)$ | cheap, no saturation for $z>0$; "dying ReLU" |
| Leaky ReLU / PReLU | $\max(\alpha z,z)$ | fixes dead units |
| ELU / SELU | smooth negative part | self-normalizing (SELU) |
| **GELU** | $z\,\Phi(z)$ | standard in [[Transformers]] |
| Swish / SiLU | $z\sigma(z)$ | smooth, good in deep nets |
| Softmax | $e^{z_k}/\sum e^{z_j}$ | output layer for classes |

Choice affects [[Backpropagation]] gradient flow and [[Training Tricks]] such as initialization (He for ReLU, Xavier for tanh).

## Learn more
- [Dive into Deep Learning](https://d2l.ai/)
- [Understanding Deep Learning – Prince (free)](https://udlbook.github.io/udlbook/)
