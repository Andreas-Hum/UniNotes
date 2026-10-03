---
tags: [ml, deep-learning, optimization]
status: not-started
notebook: not-started
level:
reviewed:
---
# Backpropagation

> [!summary] In one sentence
> Backpropagation is the chain rule applied backwards through a computation graph, reusing intermediate results so that one backward pass (costing about as much as 2–3 forward passes) gives the gradient of the loss with respect to *every* parameter.

## Intuition first

Efficient application of the chain rule on a computation graph ([[Matrix Calculus Cheatsheet]]).

Imagine a factory assembly line: raw material ($x$) passes through stations (layers), each one transforming it, and at the end a quality inspector scores the product (the loss $L$). The inspector is unhappy. Who should change what, and by how much?

The inspector tells the *last* station "if your output had been a bit higher, my score would change by this much" (a gradient). That station knows how its own output depends on its knobs and on its inputs, so it can (1) work out how to turn its own knobs, and (2) pass a message back to the previous station: "here is how *your* output affects the final score". Each station only needs **local** knowledge plus the message from downstream. That message-passing from the end to the start is backpropagation.

Why not just wiggle each weight and see what happens (finite differences)? A network with $P$ parameters would need about $2P$ forward passes for central differences; with $P=10^7$ that is hopeless. Backprop gets all $P$ partial derivatives for the price of roughly one forward and one backward pass. Finite differences are still useful as a **gradient check** on small inputs, to catch bugs in hand-written backward passes.

![A computation graph: values flow forward left to right, then gradients flow backward right to left](../../Attachments/ML%20Animations/Backpropagation%20-%20computation%20graph.gif)

*Watch how each backward step multiplies the incoming (upstream) gradient by one local derivative, and how $-6$ is computed once at the $+$ node and then reused for both $b$ and the $\times$ branch.*

## The math, step by step

### The one rule
If $L$ depends on a variable $a$ only through $u$, then
$$\frac{\partial L}{\partial a} = \underbrace{\frac{\partial L}{\partial u}}_{\text{upstream}}\cdot\underbrace{\frac{\partial u}{\partial a}}_{\text{local}}.$$
If $a$ feeds into several nodes, add up the contributions from each path. Every node only needs to know its local derivative; everything else arrives as the upstream gradient.

Three node types are enough to understand most of backprop:
- **Add** ($u=a+b$): local derivatives are 1, so it *copies* the upstream gradient to both inputs.
- **Multiply** ($u=ab$): $\partial u/\partial a = b$, so it *swaps*: each input gets the upstream gradient times the *other* input. This is why forward values must be cached.
- **Element-wise function** ($h=\phi(z)$): multiplies the upstream gradient by $\phi'(z)$; this is the "gate" that can shrink gradients.

### For an MLP
Forward: $z^{(l)}=W^{(l)}h^{(l-1)}+b^{(l)},\ h^{(l)}=\phi(z^{(l)})$.

Backward with $\delta^{(l)}=\partial L/\partial z^{(l)}$ (the "error signal" at layer $l$'s pre-activations):
$$\delta^{(L)}=\nabla_{h}L\odot\phi'(z^{(L)}),\quad \delta^{(l)}=\big(W^{(l+1)\top}\delta^{(l+1)}\big)\odot\phi'(z^{(l)})$$
$$\frac{\partial L}{\partial W^{(l)}}=\delta^{(l)}h^{(l-1)\top},\qquad \frac{\partial L}{\partial b^{(l)}}=\delta^{(l)}$$

Reading each formula in words:

1. **Output layer.** $\delta^{(L)}$: how the loss changes with the last pre-activation = (how the loss changes with the output) × (how the output changes with its pre-activation). $\odot$ is element-wise multiplication because $\phi$ acts element-wise.
2. **Recursion.** $z^{(l+1)} = W^{(l+1)}h^{(l)}+\dots$ means $h^{(l)}$ influences the loss through every unit of layer $l+1$; summing those paths is exactly multiplying by $W^{(l+1)\top}$. Then pass through the local gate $\phi'(z^{(l)})$.
3. **Weights.** $z^{(l)}_j = \sum_i W^{(l)}_{ji}h^{(l-1)}_i + b_j$, so $\partial z_j/\partial W_{ji} = h^{(l-1)}_i$. Hence $\partial L/\partial W_{ji} = \delta_j h_i$: an outer product "error at the output side × activation at the input side". A weight changes a lot only if its input was active *and* its output unit had a large error.
4. **Biases.** $\partial z_j/\partial b_j = 1$, so the bias gradient is just $\delta^{(l)}$.

With a mini-batch in row convention ($H\in\mathbb R^{N\times n_{in}}$, $Z=HW+b$, upstream $\Delta=\partial L/\partial Z$): $\partial L/\partial W = H^\top\Delta$, $\partial L/\partial b=$ column sums of $\Delta$, $\partial L/\partial H = \Delta W^\top$. A quick sanity check: every gradient has the same shape as the thing it is a gradient of.

### The softmax + cross-entropy shortcut
Softmax + cross-entropy: $\delta^{(L)}=\hat p-y$.

With $\hat p=\mathrm{softmax}(z)$, one-hot $y$ and $L=-\sum_k y_k\log\hat p_k$, the messy softmax Jacobian $\partial\hat p_i/\partial z_j=\hat p_i([i=j]-\hat p_j)$ cancels against the $1/\hat p$ from the log, leaving "prediction minus target". The same thing happens for sigmoid + BCE ($\delta=p-y$) and linear + MSE ($\delta=\hat y-y$ for $L=\tfrac12(\hat y-y)^2$). This is a big reason these output/loss pairs are standard: the error signal is simple and does not saturate.

## Worked example

The graph in the animation: $L=(wx+b-y)^2$ with $x=2$, $w=3$, $b=1$, $y=10$.

**Forward** (cache every value):
- $u = wx = 6$
- $z = u + b = 7$
- $L = (z-y)^2 = (7-10)^2 = 9$

**Backward** (upstream × local):
- $\partial L/\partial L = 1$
- $\partial L/\partial z = 2(z-y) = 2(7-10) = -6$
- $\partial L/\partial b = -6 \cdot 1 = -6$ (add node copies)
- $\partial L/\partial u = -6 \cdot 1 = -6$ (add node copies)
- $\partial L/\partial w = -6 \cdot x = -12$ (multiply node swaps: uses the cached $x=2$)
- $\partial L/\partial x = -6 \cdot w = -18$ (uses the cached $w=3$)

Check one by hand: $L(w)=(2w-9)^2$, $dL/dw = 4(2w-9) = 4(-3) = -12$, matching the backward pass. Gradient descent would now *increase* $w$ and $b$ (negative gradients), pushing $z$ up towards $y=10$.

## Practical notes

- **Cost.** Cost ≈ 2–3× a forward pass; cache activations (memory ↔ gradient checkpointing trade-off). The backward pass does roughly two matrix products per layer (one for $\partial L/\partial W$, one for $\partial L/\partial h$) versus one in the forward pass. All the cached $h^{(l-1)}$ and $z^{(l)}$ are why training needs far more memory than inference. Gradient checkpointing stores only every $k$-th layer's activations and recomputes the rest during the backward pass: less memory, about one extra forward pass of compute; with $k\approx\sqrt L$ memory grows like $O(\sqrt L)$.
- **Vanishing / exploding gradients**: products of Jacobians; mitigated by ReLU, residual connections, normalization, gradient clipping ([[Training Tricks]]). Unrolling the recursion, $\delta^{(1)}$ contains a product of $L-1$ factors of the form $W^{(l+1)\top}\mathrm{diag}(\phi'(z^{(l)}))$. If these typically shrink vectors (e.g. sigmoid, whose $\phi'\le 0.25$), the product decays exponentially with depth; if they stretch, it explodes. ReLU keeps $\phi'=1$ on active units; residual connections add an identity path ($h+F(h)$ has Jacobian $I+\dots$); normalization keeps the scale of $z$ in check; clipping caps the size of an exploding update.
- Automatic differentiation in PyTorch/JAX does this for you ([[PyTorch Recipes]]). Reverse-mode autodiff records the graph during the forward pass, topologically sorts it, then calls each node's local backward rule in reverse order, *accumulating* (`+=`) gradients when a value is used more than once. That is exactly what Karpathy's micrograd implements in ~100 lines.

## Common confusions

- **"Backprop is the learning algorithm."** Backprop only computes gradients. The learning (updating weights) is done by an optimizer such as SGD or Adam ([[Optimizers]]).
- **"Backprop is a special neural-network trick."** It is reverse-mode automatic differentiation: the plain chain rule, organised to reuse work. It applies to any differentiable computation graph.
- **"Gradients overwrite."** When a variable feeds several nodes, its gradients from each path must be *summed*; forgetting the `+=` is a classic micrograd bug.
- **"We need $\partial L/\partial x$ for the input."** Usually not for training (inputs are data), but it is computed anyway on the way and is used for saliency maps and adversarial examples.
- **"A small gradient means we are near the optimum."** It can also mean saturated units or vanishing gradients; look at per-layer gradient norms.

## Check yourself

> [!question]- For $u=xy+z$ and $f=u^2$, what is $\partial f/\partial z$ in terms of $u$?
> $\partial f/\partial u = 2u$ and $\partial u/\partial z = 1$ (add node copies), so $\partial f/\partial z = 2u$.

> [!question]- Why does the backward pass of a multiply node need the forward values?
> Its local derivative with respect to one input is the *other* input, so both inputs must be cached from the forward pass.

> [!question]- A layer has $W\in\mathbb R^{100\times 50}$ (row convention, batch $N=32$). What shape is $\partial L/\partial W$, and how is it computed?
> $100\times 50$, the same as $W$; it is $H^\top\Delta$ with $H\in\mathbb R^{32\times100}$ and $\Delta\in\mathbb R^{32\times 50}$.

> [!question]- A 5-layer chain of sigmoids with all pre-activations at 0 and weight 1: by how much is the gradient scaled?
> Each layer contributes $w\,\sigma'(0)=0.25$, so $0.25^{5}\approx 10^{-3}$. Every extra layer divides it by 4 again.

> [!question]- What is $\delta^{(L)}$ for softmax + cross-entropy with $\hat p=(0.2,0.7,0.1)$ and true class 1 (the second)?
> $\hat p - y = (0.2,\,-0.3,\,0.1)$.

## Practice

[Backpropagation - Exercises](Backpropagation%20-%20Exercises.ipynb): finite differences vs. backprop, vanishing gradients, checkpointing, chain rule and full backward passes by hand, gradient-checked layers, a full MLP, and your own micrograd.

## Learn more
- [3Blue1Brown – Neural Networks](https://www.3blue1brown.com/topics/neural-networks) (chapters "What is backpropagation really doing?" and "Backpropagation calculus")
- [Karpathy – Zero to Hero](https://karpathy.ai/zero-to-hero.html) (micrograd)
- [Nielsen – Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) ch. 2
- [colah – Calculus on Computational Graphs: Backpropagation](https://colah.github.io/posts/2015-08-Backprop/)
- [Stanford CS231n notes – Backpropagation, intuitions](https://cs231n.github.io/optimization-2/)
