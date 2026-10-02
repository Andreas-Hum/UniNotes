---
tags: [ml, deep-learning]
---
# Activation Functions

> [!summary] In one sentence
> The activation function $\phi$ is the element-wise non-linearity that stops a neural network from collapsing into a linear model, and its *derivative* decides how well gradients survive the trip back through many layers.

## Intuition first

In a [[Neural Networks|neural network]], every unit computes a weighted sum $z$ and then passes it through $\phi$. Without $\phi$, stacking layers would be pointless: a composition of linear maps is still linear. So $\phi$ is the "fold" or "bend" that gives networks their expressive power.

But there is a second job that matters just as much in practice. During [[Backpropagation]], the gradient flowing backwards is multiplied by $\phi'(z)$ at *every* layer. Think of each layer as a pipe with a valve:

- If the valve is mostly closed ($\phi'$ small, e.g. the flat tails of a sigmoid), after 20 layers almost nothing gets through: **vanishing gradients**. The early layers stop learning.
- If the valve is fully open where the unit is active ($\phi'=1$, ReLU for $z>0$), gradients pass through undamped.
- If a valve is stuck shut for every input ($\phi'=0$ always), that unit is **dead**: it never updates again.

So choosing an activation is a trade-off between *shape* (what outputs look like: bounded? zero-centred? smooth?) and *gradient flow* (how big is $\phi'$, and where is it zero?).

![Sigmoid, tanh, ReLU and GELU morphing into each other, with their derivatives on the right](../../Attachments/ML%20Animations/Activation%20Functions%20-%20shapes%20and%20derivatives.gif)

*Watch the right panel: the sigmoid's derivative never gets above 0.25 and dies in the red tails, tanh reaches 1 only at $z=0$, ReLU is a clean 0/1 step, and GELU is a smooth version of that step.*

## The catalogue

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

## The math, step by step

### Sigmoid
$\sigma(z)=\frac1{1+e^{-z}}$ squashes any real number into $(0,1)$, so it reads naturally as a probability. Its derivative has a neat form:
$$\sigma'(z)=\frac{e^{-z}}{(1+e^{-z})^2}=\sigma(z)\big(1-\sigma(z)\big).$$
In words: the slope is largest when the output is 0.5 (at $z=0$, slope $0.25$) and tends to 0 as the output approaches 0 or 1. That is **saturation**: a confident sigmoid unit barely passes any gradient. A second problem: outputs are always positive (not zero-centred). If all inputs $h_i$ to the next unit are positive, then $\partial L/\partial w_i=\delta\,h_i$ all share the sign of $\delta$, so the weights of that unit can only all go up or all go down together, giving zig-zag updates.

### Tanh
$\tanh z = 2\sigma(2z)-1$ is a stretched, shifted sigmoid with range $(-1,1)$, so it *is* zero-centred. Its derivative $\tanh'(z)=1-\tanh^2 z$ reaches $1$ at $z=0$ (four times the sigmoid's peak), but it still saturates for large $|z|$.

### ReLU
$\mathrm{ReLU}(z)=\max(0,z)$, with $\phi'(z)=1$ for $z>0$ and $0$ for $z<0$ (at exactly 0 frameworks just pick 0). It is cheap (a comparison), it does not saturate for positive inputs, and it produces sparse activations. Its weakness is **dying ReLU**: if a big update pushes a unit's bias very negative, then $z<0$ for every input, the gradient is 0 for every input, and the unit can never recover. Remedies: smaller learning rates, sensible initialization, or an activation with a non-zero negative slope.

### Leaky ReLU / PReLU, ELU / SELU
$\max(\alpha z, z)$ with a small $\alpha$ (e.g. $0.01$) keeps a tiny slope for $z<0$, so no unit is ever completely dead; PReLU *learns* $\alpha$. ELU replaces the negative part with a smooth curve $\alpha(e^z-1)$ that saturates at $-\alpha$, pushing mean activations towards zero. SELU is ELU with two specific constants chosen so that, with the right initialization ($\mathcal N(0,1/n_{in})$) and standardised inputs, activations keep mean $\approx0$ and variance $\approx1$ through a deep fully connected net without any normalization layers: "self-normalizing".

### GELU and Swish / SiLU
$\mathrm{GELU}(z)=z\,\Phi(z)$, where $\Phi$ is the standard normal CDF: multiply $z$ by "the probability that a standard normal is below $z$". For large positive $z$, $\Phi\approx1$ (behaves like the identity); for large negative $z$, $\Phi\approx0$ (outputs 0). In between it is smooth with a small negative dip. Swish/SiLU $z\sigma(z)$ is the same idea with the logistic CDF. Both are smooth everywhere (nicer optimisation) and are the standard choice in [[Transformers]] and many modern CNNs. Swish's derivative is $\sigma(z)+z\sigma(z)(1-\sigma(z))$, which can slightly exceed 1.

### Softmax
$\mathrm{softmax}(z)_k=e^{z_k}/\sum_j e^{z_j}$ maps a vector of scores to a probability distribution. Two facts to remember:
- **Shift invariance**: adding the same constant to every $z_k$ does not change the output, so implementations subtract $\max_j z_j$ to avoid overflow.
- **Jacobian**: $\partial p_i/\partial z_j=p_i([i=j]-p_j)$, i.e. $J=\mathrm{diag}(p)-pp^\top$. Combined with cross-entropy it simplifies to $\hat p-y$.

Dividing logits by a temperature $T$ before softmax makes the distribution sharper ($T<1$, towards argmax) or flatter ($T>1$, towards uniform); this is used in sampling from language models and in knowledge distillation. Softmax couples all units (they compete), which is why it belongs at the output, not in hidden layers.

## Worked example

Take $z=2$:
- Sigmoid: $\sigma(2)=1/(1+e^{-2})\approx0.881$; slope $0.881\cdot0.119\approx0.105$.
- Tanh: $\tanh 2\approx0.964$; slope $1-0.964^2\approx0.071$.
- ReLU: output $2$, slope $1$.

Now chain 10 layers that each sit at $z=2$. The gradient is multiplied by $0.105^{10}\approx 10^{-10}$ (sigmoid), $0.071^{10}\approx 3\times10^{-12}$ (tanh), or $1^{10}=1$ (ReLU). This is the whole vanishing-gradient story in three lines.

Softmax of $z=(3,1,0)$: $e^z\approx(20.09,\,2.72,\,1)$, sum $\approx23.80$, so $p\approx(0.844,\,0.114,\,0.042)$. Adding 100 to every entry gives exactly the same $p$.

GELU vs. Swish at $z=-0.5$: GELU $=-0.5\,\Phi(-0.5)\approx-0.154$; Swish $=-0.5\,\sigma(-0.5)\approx-0.189$. Both let a little negative signal through, unlike ReLU.

## How to choose (rules of thumb)

- **Hidden layers of CNNs/MLPs**: ReLU (with He initialization), or Leaky ReLU / GELU / Swish if you see dead units or want a bit more accuracy.
- **Transformer MLP blocks**: GELU (or SwiGLU-style variants).
- **Recurrent gates** ([[RNN and LSTM]]): sigmoid for gates (they must be in (0,1) to act as "how much to let through"), tanh for candidate states.
- **Deep fully connected nets with no normalization**: SELU with its matching initialization.
- **Output layer**: identity (regression), sigmoid (binary / multi-label), softmax (one-of-$K$ classes).

## Common confusions

- **"ReLU isn't differentiable, so we can't backprop through it."** It is non-differentiable only at the single point $z=0$; using any subgradient there (0 is standard) works fine.
- **"Sigmoid and softmax are interchangeable."** Sigmoid treats each output independently (multi-label); softmax makes outputs compete and sum to 1 (one class).
- **"Saturation only matters for sigmoid."** Tanh saturates too, and so does the negative side of ELU. ReLU "saturates" at 0 for all $z<0$, which is the dying-ReLU problem.
- **"The activation choice is independent of initialization."** The right weight variance depends on $\phi$: He ($2/n_{in}$) compensates for ReLU zeroing half its inputs; Xavier suits tanh ([[Training Tricks]]).
- **"Leaky ReLU's $\alpha$ must be tuned carefully."** Small values like $0.01$ usually work; the point is just that the gradient is never exactly zero.

## Check yourself

> [!question]- What is the maximum of $\sigma'(z)$ and where is it attained?
> $0.25$ at $z=0$, because $\sigma(0)=0.5$ and $\sigma'=\sigma(1-\sigma)=0.5\cdot0.5$.

> [!question]- Why can a dead ReLU unit not recover on its own?
> Its pre-activation is negative for every input, so its output and its gradient are 0 for every input; no gradient ever reaches its weights or bias.

> [!question]- Which activation would you use for LSTM gates, and why?
> Sigmoid: a gate multiplies a signal by a value in (0,1), meaning "what fraction to let through".

> [!question]- Why subtract $\max_j z_j$ before computing softmax?
> Softmax is shift invariant, so the result is unchanged, but the largest exponent becomes $e^0=1$, which prevents overflow for large logits.

> [!question]- Why is tanh usually preferred over sigmoid in hidden layers (when you must use one of them)?
> It is zero-centred and its derivative at 0 is 1 rather than 0.25, so gradients shrink less per layer.

## Practice

[Activation Functions - Exercises](Activation%20Functions%20-%20Exercises.ipynb): saturation, dying ReLU, zero-centring, derivatives of sigmoid/tanh/Swish, the softmax Jacobian, a stable sigmoid, softmax temperature, counting dead units, gradient flow through depth, and SELU's self-normalization.

## Learn more
- [Dive into Deep Learning](https://d2l.ai/)
- [Understanding Deep Learning – Prince (free)](https://udlbook.github.io/udlbook/)
- [Stanford CS231n notes – Neural Networks Part 1 (activation functions)](https://cs231n.github.io/neural-networks-1/)
- [GELU paper (Hendrycks & Gimpel)](https://arxiv.org/abs/1606.08415)
