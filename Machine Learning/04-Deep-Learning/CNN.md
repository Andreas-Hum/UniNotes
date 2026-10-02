---
tags: [ml, deep-learning, vision]
---
# Convolutional Neural Networks

Exploit **locality** and **translation equivariance** via shared kernels.

- Convolution: $(I*K)(i,j)=\sum_{m,n}I(i+m,j+n)K(m,n)$ (really cross-correlation).
- Output size: $\lfloor\frac{W-F+2P}{S}\rfloor+1$.
- Pooling (max/avg) → invariance + downsampling. Parameter count: $C_{in}C_{out}k^2$ vs. dense layer.
- **Receptive field** grows with depth.

## Milestones
LeNet → AlexNet → VGG (3×3 stacks) → **ResNet** (skip connections: $y=F(x)+x$) → Inception/EfficientNet → ConvNeXt; Vision Transformers ([[Transformers]]) compete.

## Tasks
Classification, detection (YOLO, Faster R-CNN), segmentation (U-Net, Mask R-CNN), 1D CNN for audio/time series.

## Tricks
BatchNorm, data augmentation, transfer learning from ImageNet, mixed precision ([[Training Tricks]]).

## Learn more
- [Stanford CS231n](https://cs231n.stanford.edu/) · [notes](https://cs231n.github.io/)
- [Dive into Deep Learning](https://d2l.ai/)
- [ResNet paper](https://arxiv.org/abs/1512.03385)
