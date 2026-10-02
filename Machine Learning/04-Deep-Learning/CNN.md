---
tags: [ml, deep-learning, vision]
---
# Convolutional Neural Networks

> [!summary] In one sentence
> A CNN slides small, shared filters (kernels) over an image so that every layer looks for the same local pattern everywhere, which exploits **locality** and **translation equivariance**, needs far fewer parameters than a dense layer, and builds up from edges to textures to object parts as the **receptive field** grows with depth.

## Intuition first

Imagine checking a large photo for cats with a magnifying glass. You would not learn a separate "cat detector" for the top-left corner, another for the centre, and so on: a whisker looks like a whisker wherever it is. You would learn **one small detector** and **slide it everywhere**. That is a convolutional layer.

Two assumptions about images make this work:

- **Locality**: the pixels that matter for "is there an edge here?" are the nearby ones. A small kernel (say $3\times3$) only looks at a small neighbourhood.
- **Translation equivariance**: if the cat moves 10 pixels to the right, the feature map should move 10 pixels to the right too. Using the *same* weights at every position (**weight sharing**) gives this for free.

A dense (fully connected) layer makes neither assumption. Every output is connected to every pixel, so it needs an enormous number of weights and must learn "whisker at position (3,5)" and "whisker at position (40,17)" as two unrelated things.

Stacking conv layers then gives a hierarchy: layer 1 finds edges, layer 2 combines edges into corners and textures, deeper layers combine those into eyes, wheels and faces. Each deeper unit "sees" a larger patch of the original image.

![A 3x3 Sobel kernel sliding over a 6x6 image with a vertical edge, filling in a 4x4 feature map](../../Attachments/ML%20Animations/CNN%20-%20convolution%20sliding.gif)

*Watch the yellow window: the same nine weights are used at every position, and the output is large (4) only where the window straddles the dark-to-light edge and 0 on flat regions.*

## The math, step by step

### The convolution (really cross-correlation)

$$(I*K)(i,j)=\sum_{m,n}I(i+m,\,j+n)\,K(m,n)$$

- $I$ is the input image (or feature map), $K$ the kernel, $(i,j)$ the output position, and $(m,n)$ runs over the kernel's positions.
- In words: place the kernel with its corner at $(i,j)$, multiply overlapping numbers element-wise, add them up. That single number is one output pixel.
- Strictly this is **cross-correlation**; true convolution flips the kernel, $\sum_{m,n}I(i-m,j-n)K(m,n)$. Deep-learning libraries skip the flip because the kernel is learned anyway, so a flipped kernel is just a different set of learned weights.
- With $C_{in}$ input channels the kernel has shape $C_{in}\times k\times k$ and the sum also runs over channels; each of the $C_{out}$ kernels produces one output channel. Add a bias per output channel.

### Output size

$$\Big\lfloor\frac{W-F+2P}{S}\Big\rfloor+1$$

- $W$: input width (or height), $F$: filter size, $P$: zero padding on each side, $S$: stride (step between window positions).
- Why: after padding the input is $W+2P$ wide; the first window occupies $F$ of it, and every further step of $S$ adds one output, so the number of positions is $\frac{W+2P-F}{S}+1$, rounded down if it does not divide evenly.
- "Same" padding with stride 1 means $P=(F-1)/2$, so the output size equals the input size.

### Parameter count

A conv layer has $C_{in}C_{out}k^2$ weights (plus $C_{out}$ biases), **independent of the image size**. A dense layer between the same input and output volumes has (input size) × (output size) weights, which grows with the square of the number of pixels.

### Pooling

**Pooling** (max or average) takes a small window (typically $2\times2$, stride 2) and summarises it with one number. It gives:

- **downsampling**: half the width and height, so later layers are cheaper and see more context;
- some **invariance**: a max-pool output does not change if the strongest activation moves a little inside its window.

### Equivariance vs invariance

For a shift operator $T$ and a layer $f$:

- **equivariant**: $f(Tx)=T f(x)$, shifting the input shifts the output (conv layers with stride 1, ignoring borders);
- **invariant**: $f(Tx)=f(x)$, the output does not change (global average pooling; max-pool approximately, for small shifts).

A classifier wants the final answer to be invariant ("cat" no matter where), while the intermediate feature maps should be equivariant (they need to keep track of *where* things are).

### Receptive field

The **receptive field** of a unit is the patch of the input image that can influence it, and it **grows with depth**. With the "jump" $j_l=j_{l-1}s_l$ (distance in input pixels between neighbouring units of layer $l$, $j_0=1$) and $r_0=1$:

$$r_l=r_{l-1}+(k_l-1)\,j_{l-1}$$

Each new $k\times k$ layer adds $k-1$ units of the layer below, and each of those is $j_{l-1}$ input pixels apart. Strides and pooling increase $j$, so they make the receptive field grow much faster.

![Three stacked 3-wide convolutions: the receptive field of one top unit grows from 3 to 5 to 7 input cells](../../Attachments/ML%20Animations/CNN%20-%20receptive%20field.gif)

*Follow the yellow unit down: each layer adds $k-1=2$ cells to what it can see, so three $3\times3$ layers see a $7\times7$ patch; two of them already see $5\times5$ with fewer weights than one $5\times5$ layer (the VGG idea).*

### Backward pass (what the exercises implement)

- Gradient w.r.t. the kernel: $\frac{\partial L}{\partial K}$ is the cross-correlation of the input $I$ with the upstream gradient $G=\partial L/\partial O$, because every kernel weight touched every window.
- Gradient w.r.t. the input: a "full" convolution of $G$ with the flipped kernel.
- Max-pool backward: the gradient goes only to the position that was the max in each window; the others get 0. Average-pool spreads it evenly.
- **im2col** turns convolution into one big matrix multiplication: unroll every window into a column, stack the kernels as rows, multiply. That is how fast libraries implement it.

## Worked example

**Edge detection by hand** (the animation). Input: a $6\times6$ image, 0 in the left three columns, 1 in the right three. Kernel: the vertical Sobel filter

$$K=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}$$

- Window over columns 0–2 (all zeros): output 0.
- Window over columns 1–3: only the right column is 1, so the output is $1+2+1=4$.
- Window over columns 2–4: left column 0, middle column ignored (weights 0), right column 1: again $4$.
- Window over columns 3–5 (all ones): $-4+0+4=0$.

Every row gives $(0,4,4,0)$: a $4\times4$ map (check: $\lfloor\frac{6-3+0}{1}\rfloor+1=4$) that lights up exactly at the edge.

**Output sizes.** $W=32,F=5,P=2,S=1$: $\frac{32-5+4}{1}+1=32$ ("same"). AlexNet's first layer, $W=227,F=11,P=0,S=4$: $\frac{216}{4}+1=55$. $W=28,F=3,P=1,S=2$: $\lfloor 13.5\rfloor+1=14$.

**Conv vs dense.** From a $32\times32\times3$ image to a $32\times32\times64$ map:

- $3\times3$ conv: $3\cdot64\cdot9=1{,}728$ weights $+64$ biases $=1{,}792$.
- dense: $3{,}072\times65{,}536\approx 2\times10^8$ weights. More than 100,000 times more.

**Receptive field with a pool.** conv $3\times3$ s1 → $r=3, j=1$; max-pool $2\times2$ s2 → $r=3+1\cdot1=4, j=2$; conv $3\times3$ s1 → $r=4+2\cdot2=8$.

## Milestones

LeNet → AlexNet → VGG (3×3 stacks) → **ResNet** (skip connections: $y=F(x)+x$) → Inception/EfficientNet → ConvNeXt; Vision Transformers ([[Transformers]]) compete.

- **LeNet** (1990s): small CNN for handwritten digits; conv → pool → conv → pool → dense.
- **AlexNet** (2012): much bigger, ReLU, dropout, GPUs; won ImageNet by a wide margin and started the deep-learning boom.
- **VGG**: only $3\times3$ convs, stacked. Two $3\times3$ layers have the receptive field of one $5\times5$ but fewer weights ($2\cdot9C^2=18C^2$ vs $25C^2$) and an extra nonlinearity.
- **ResNet**: $y=F(x)+x$. The block only has to learn the *residual* $F$; if the best thing is to do nothing, it can output $F=0$. Backprop gets $\frac{\partial y}{\partial x}=I+\frac{\partial F}{\partial x}$, so across many blocks the gradient is a product of $(I+J_{F_l})$ terms instead of a product of $J_{F_l}$ terms, and it does not vanish. This made 100+ layer networks trainable.
- **Inception / EfficientNet**: parallel branches of different kernel sizes; principled scaling of depth, width and resolution together.
- **ConvNeXt**: a CNN modernised with Transformer-era design choices; shows CNNs remain competitive with ViTs.

## Tasks

Classification, detection (YOLO, Faster R-CNN), segmentation (U-Net, Mask R-CNN), 1D CNN for audio/time series. A 1-D convolution with kernel $(\tfrac13,\tfrac13,\tfrac13)$ is just a moving average, so 1-D CNNs generalise classic signal filters. See [[Computer Vision Overview]] for the full task table and metrics.

## Tricks

BatchNorm, data augmentation, transfer learning from ImageNet, mixed precision ([[Training Tricks]]).

- **Transfer learning** is the default with small datasets: start from ImageNet weights, freeze early layers (generic edges/textures), fine-tune later ones with a small learning rate.
- **Augmentation** must respect the task: a horizontal flip is harmless for cats but can be wrong for chest X-rays (the heart is on one side) or text.
- **BatchNorm** with tiny batches is noisy; when fine-tuning on small data, keep its statistics frozen.

## Common confusions

- "Convolution in CNNs is mathematical convolution." → It is cross-correlation (no kernel flip); since the kernel is learned, it makes no difference.
- "Pooling makes CNNs fully translation invariant." → Conv layers are equivariant; pooling adds only *local*, approximate invariance. Real invariance comes from global pooling at the end (and from augmentation).
- "More parameters come from bigger images." → Conv parameter count $C_{in}C_{out}k^2$ does not depend on image size; only the compute and activation memory do.
- "Deeper is always better." → Plain deep stacks get *worse* (vanishing gradients, hard optimisation); ResNet skip connections are what make depth pay off.
- "A $3\times3$ network only sees $3\times3$ pixels." → Each layer only looks at $3\times3$ of the layer below, but the receptive field in the input grows with every layer.

## Check yourself

> [!question]- A $7\times7$ input, $3\times3$ kernel, padding 0, stride 2. What is the output size?
> $\lfloor\frac{7-3+0}{2}\rfloor+1=2+1=3$, so $3\times3$.

> [!question]- How many weights does a $5\times5$ conv from 16 to 32 channels have (with biases)?
> $16\cdot32\cdot25=12{,}800$ weights $+32$ biases $=12{,}832$, whatever the image size.

> [!question]- Why does a stack of 100 residual blocks train when 100 plain layers do not?
> The Jacobian of each block is $I+J_F$, so the backward signal always has an identity path; in a plain stack it is a product of 100 Jacobians, which tends to shrink or blow up exponentially.

> [!question]- What is the receptive field after two $3\times3$ convs with stride 1?
> $r=1+2+2=5$, i.e. $5\times5$.

> [!question]- Is global average pooling equivariant or invariant to shifts?
> Invariant: it averages over all positions, so a shift (with circular borders) leaves the result unchanged.

## Practice

[CNN - Exercises](CNN%20-%20Exercises.ipynb): equivariance vs invariance, why ResNet skips help, transfer learning on a small medical dataset, output sizes, conv vs dense parameter counts, convolution and receptive fields by hand, then NumPy implementations of conv2d, a Sobel edge detector, im2col, conv and max-pool backward passes, an equivariance test, residual gradients and a 1-D conv.

## Learn more

- [Stanford CS231n](https://cs231n.stanford.edu/) · [notes](https://cs231n.github.io/)
- [Dive into Deep Learning](https://d2l.ai/)
- [ResNet paper](https://arxiv.org/abs/1512.03385)
- [3Blue1Brown – But what is a convolution?](https://www.youtube.com/watch?v=KuXjwB4LzSA)
- [A guide to convolution arithmetic (Dumoulin & Visin)](https://arxiv.org/abs/1603.07285)
- [Distill – Feature Visualization](https://distill.pub/2017/feature-visualization/) (what the layers actually detect)
