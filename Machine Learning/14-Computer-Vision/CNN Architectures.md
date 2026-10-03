---
tags: [ml, vision, deep-learning]
---
# CNN Architectures

> [!summary] In one sentence
> The history of image classifiers is a series of ideas for going **deeper without breaking training** (small filters, batch norm, residual connections) and then **spending compute more wisely** (bottlenecks, depthwise convolutions, compound scaling), until Vision Transformers showed attention can do it too.

## Intuition first
A convolution layer slides small filters over the image and asks "is this pattern here?" Early layers find edges, middle layers find textures and parts, late layers find objects. Each architecture below is an answer to: *how do we stack more of these layers, cheaply, while still being able to train them?*

## Building blocks (recap)
- **Output size:** $\lfloor (W-F+2P)/S\rfloor+1$ for input width $W$, filter $F$, padding $P$, stride $S$.
- **Parameters of a conv layer:** $(F\cdot F\cdot C_{in}+1)\cdot C_{out}$.
- **Receptive field** grows with depth: two stacked $3\times3$ convs see $5\times5$, three see $7\times7$ – with fewer parameters ($2\cdot9C^2=18C^2$ or $27C^2$ vs $25C^2$ or $49C^2$).
- **Pooling** downsamples; **global average pooling** replaces big fully connected heads.
- Details in [[CNN]].

## The milestones
| Model | Year | Key idea | Why it mattered |
|---|---|---|---|
| **LeNet-5** | 1998 | conv → pool → conv → pool → FC | first practical CNN (digits) |
| **AlexNet** | 2012 | ReLU, dropout, GPUs, data augmentation | won ImageNet by a huge margin – started the deep learning boom |
| **VGG** | 2014 | only $3\times3$ convs, very deep (16–19 layers) | simple, uniform design; showed depth helps |
| **GoogLeNet / Inception** | 2014 | parallel $1\times1$, $3\times3$, $5\times5$ branches; $1\times1$ "bottleneck" convs to cut channels | accuracy at a fraction of VGG's cost |
| **BatchNorm** | 2015 | normalise activations per mini-batch | much faster, more stable training |
| **ResNet** | 2015 | **residual connections** $y=F(x)+x$ | trains 100+ layers; the default backbone for years |
| **DenseNet** | 2016 | each layer gets all previous feature maps | feature reuse, fewer parameters |
| **MobileNet** | 2017 | **depthwise separable** convolutions | runs on phones |
| **EfficientNet** | 2019 | **compound scaling** of depth, width and resolution together | best accuracy per FLOP at the time |
| **ViT** | 2020 | split the image into $16\times16$ patches → tokens → [[Transformers]] | attention matches CNNs given enough data |
| **ConvNeXt** | 2022 | modernised ResNet using ViT design choices (big kernels, LayerNorm, GELU) | pure CNN competitive with ViTs again |

## The math, step by step
### Why residual connections work
A residual block computes $y=x+F(x)$. Backpropagating through it:
$$\frac{\partial L}{\partial x}=\frac{\partial L}{\partial y}\Big(I+\frac{\partial F}{\partial x}\Big)$$
The identity term $I$ gives the gradient a direct path to early layers, so it does not vanish even when $\partial F/\partial x$ is small. And if the best thing a block can do is nothing, it only has to learn $F(x)=0$ – easier than learning the identity with a plain stack of layers. Before ResNet, a 56-layer plain network had **higher training error** than a 20-layer one: an optimisation problem, not overfitting.

### $1\times1$ convolutions (bottlenecks)
A $1\times1$ conv mixes channels at each pixel. The ResNet bottleneck block does $1\times1$ (reduce $256\to64$) → $3\times3$ (at 64 channels) → $1\times1$ (expand back to 256). Parameters: $256\cdot64+9\cdot64^2+64\cdot256\approx70\text{k}$ instead of $2\cdot9\cdot256^2\approx1.2\text{M}$ for two $3\times3$ convs at 256 channels.

### Depthwise separable convolutions
A standard conv costs $F^2\,C_{in}\,C_{out}$ multiplications per pixel. Splitting it into a **depthwise** conv (one $F\times F$ filter per channel: $F^2C_{in}$) followed by a **pointwise** $1\times1$ conv ($C_{in}C_{out}$) gives a cost ratio of
$$\frac{F^2C_{in}+C_{in}C_{out}}{F^2C_{in}C_{out}}=\frac1{C_{out}}+\frac1{F^2}\approx\frac19\ \text{ for }F=3.$$

### EfficientNet compound scaling
Scale depth $d=\alpha^\phi$, width $w=\beta^\phi$ and resolution $r=\gamma^\phi$ together, with $\alpha\beta^2\gamma^2\approx2$, so each step of $\phi$ roughly doubles FLOPs. Scaling only one dimension saturates quickly.

### Vision Transformer
An $H\times W$ image with patch size $P$ gives $N=HW/P^2$ tokens ($224^2/16^2=196$). Each patch is flattened and linearly projected to dimension $d$, a learnable [CLS] token and position embeddings are added, and a standard Transformer encoder follows. ViT lacks the CNN's built-in **inductive biases** (locality, translation equivariance), so it needs more data (or strong augmentation/distillation, e.g. DeiT) to beat CNNs, but scales better.

## Transfer learning in practice
1. Take an ImageNet-pretrained backbone (`timm` / `torchvision`).
2. Replace the classification head with one for your classes.
3. Train the head with the backbone frozen; then unfreeze and fine-tune everything with a small learning rate.
4. Use the backbone's normalisation statistics and input resolution.
With a few hundred images per class this usually beats training from scratch by a wide margin.

## Common confusions
- **"Deeper is always better."** → Without residuals or normalisation, very deep plain nets train **worse**.
- **"Residual connections fix overfitting."** → They fix optimisation (gradient flow); overfitting needs regularisation and data.
- **"ViT has replaced CNNs."** → CNNs remain strong, especially with little data, on edge devices and as detection/segmentation backbones; ConvNeXt shows the gap is mostly about training recipes.
- **"$1\times1$ convs do nothing."** → They mix channels and change channel count cheaply.

## Check yourself
> [!question]- Input $224\times224\times3$, a conv with 64 filters $7\times7$, stride 2, padding 3. Output size and parameters?
> $\lfloor(224-7+6)/2\rfloor+1=112$ → $112\times112\times64$; parameters $(7\cdot7\cdot3+1)\cdot64=9{,}472$.

> [!question]- Why could a 56-layer plain network have higher **training** error than a 20-layer one, and how does ResNet fix it?
> Optimisation difficulty: gradients degrade and identity mappings are hard to learn through stacked non-linear layers. Skip connections give an identity path, so extra layers can at worst learn $F(x)=0$.

> [!question]- How many tokens does a ViT with patch size 16 get from a $384\times384$ image?
> $(384/16)^2=576$ (+1 [CLS]).

## Practice

[CNN Architectures - Exercises](CNN%20Architectures%20-%20Exercises.ipynb): residual connections, inductive biases and transfer learning, then output-size, parameter and FLOP arithmetic (ResNet stem and bottleneck, depthwise separable convs, EfficientNet scaling, ViT tokens), and NumPy implementations of a VGG-16 shape tracer, plain vs residual gradient flow, 2D convolution, depthwise separable convolution, ViT patch embedding and batch normalisation.

## Learn more
- [ResNet — He et al. 2015](https://arxiv.org/abs/1512.03385)
- [EfficientNet — Tan & Le 2019](https://arxiv.org/abs/1905.11946)
- [ViT — Dosovitskiy et al. 2020](https://arxiv.org/abs/2010.11929)
- [ConvNeXt — Liu et al. 2022](https://arxiv.org/abs/2201.03545)
- [Stanford CS231n](https://cs231n.stanford.edu/) · [timm library](https://github.com/huggingface/pytorch-image-models)

See [[CNN]], [[Computer Vision Overview]], [[Object Detection]], [[Image Segmentation]].
