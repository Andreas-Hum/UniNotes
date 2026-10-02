---
tags: [ml, deep-learning]
---
# Neural Networks

> [!summary] In one sentence
> A feed-forward neural network is a stack of "linear map, then bend" layers; the bends (non-linearities) let the stack carve curved decision boundaries and approximate essentially any function, and the whole thing is trained by gradient descent.

## Intuition first

Picture a sheet of rubber with coloured dots drawn on it. You are allowed two moves: **stretch/rotate/shear** the sheet (a linear map, plus a shift), and **fold** it along a crease (a non-linearity). After a few rounds of stretching and folding, dots that used to be hopelessly tangled can end up neatly on opposite sides of a straight line. Then a plain linear classifier on top finishes the job.

That is exactly what a neural network does:

- Each **layer** takes a vector $h^{(l-1)}$, multiplies it by a weight matrix, adds a bias (stretch + shift), and passes every entry through a fixed non-linear function $\phi$ (the fold).
- The **last layer** is just a linear model (regression, [[Logistic Regression]], or softmax regression) acting on features the earlier layers *learned* instead of features you hand-designed.

So the problem neural networks solve is **feature engineering**: instead of you inventing $x_1x_2$ or $x^2$ features, the network learns a representation in which the problem becomes easy.

![XOR points being stretched by a linear map and then folded by ReLU until a straight line separates them](../../Attachments/ML%20Animations/Neural%20Networks%20-%20XOR%20space%20folding.gif)

*Watch the grid: the linear step only shears it (still no separating line), and only after ReLU folds the negative parts onto the axes do the two colours become separable by one straight line.*

## The math, step by step

A feed-forward network composes affine maps and non-linearities:
$$h^{(l)}=\phi\big(W^{(l)}h^{(l-1)}+b^{(l)}\big),\quad \hat y=h^{(L)}$$

Symbol by symbol:

- $h^{(0)} = x$ is the input vector (e.g. 784 pixel values).
- $W^{(l)}$ is the weight matrix of layer $l$, of shape $n_l \times n_{l-1}$: row $j$ holds the weights that unit $j$ puts on every input.
- $b^{(l)}$ is the bias vector of layer $l$ (length $n_l$): a per-unit shift.
- $z^{(l)} = W^{(l)}h^{(l-1)}+b^{(l)}$ is the **pre-activation**: a weighted vote of the previous layer.
- $\phi$ is the **activation function**, applied element-wise (ReLU, tanh, …, see [[Activation Functions]]).
- $h^{(l)}$ are the **activations** (hidden features) of layer $l$; $\hat y = h^{(L)}$ is the output, where the last layer uses an output activation chosen to match the task (see below).

In words: *each unit computes a weighted sum of the previous layer, adds a bias, and squashes or clips the result.* A layer with $n_{l-1}$ inputs and $n_l$ outputs has $n_l n_{l-1}$ weights plus $n_l$ biases, i.e. $(n_{l-1}+1)\,n_l$ parameters.

### Why non-linear?
Without $\phi$ the stack collapses to one linear map and cannot solve XOR ([[Linear Models for Classification]]). Derivation in one line, for two layers:
$$W^{(2)}\big(W^{(1)}x+b^{(1)}\big)+b^{(2)} = \underbrace{W^{(2)}W^{(1)}}_{W}\,x + \underbrace{W^{(2)}b^{(1)}+b^{(2)}}_{b}.$$
By induction, any number of purely linear layers equals a single linear layer. Depth only buys you something because $\phi$ breaks this collapse. XOR (labels $0,1,1,0$ on the corners of the unit square) has no separating line in input space, so a linear model, however deep, must fail; one hidden layer with a non-linearity fixes it (animation above).

### Output + loss
The output layer and loss are chosen as a matched pair, so that the loss is the negative log-likelihood of a sensible probability model:

| Task | Output activation | Loss | Probability model |
|---|---|---|---|
| Regression | linear (identity) | MSE | Gaussian noise around $\hat y$ |
| Binary | sigmoid | BCE (binary cross-entropy) | Bernoulli |
| Multiclass | softmax | cross-entropy ([[Logistic Regression]]) | Categorical |

Softmax turns a vector of logits $z$ into probabilities $\hat p_k = e^{z_k}/\sum_j e^{z_j}$, and the cross-entropy for the true class $k$ is $L=-\log \hat p_k$. A practical point: compute it via log-softmax, $\log\hat p_k = z_k - \log\sum_j e^{z_j}$, and subtract $\max_j z_j$ first so that huge logits do not overflow. Multi-label tagging (any subset of labels) is *several independent sigmoids* with BCE, not one softmax.

### Universal approximation
**Universal approximation**: one hidden layer with enough units approximates any continuous function on a compact set. Depth gives efficiency.

Why it is believable: with ReLU, $a\,\mathrm{ReLU}(x-c)$ is a "hinge" that starts at $x=c$ with slope $a$. Summing hinges gives any piecewise-linear function: three hinges make a tent (bump), and sums of shifted, scaled tents can trace any continuous curve as closely as you want, just as a fine polyline approximates a curve.

What the theorem does *not* say: how many units you need (can be astronomically many), that gradient descent will *find* those weights, or that the network will *generalise* from finite data. Depth helps on all three in practice: deep networks reuse intermediate features (edges → textures → parts → objects), so they can represent many functions with exponentially fewer units than a shallow one.

## Worked example

A network with 2 inputs, 2 ReLU hidden units, and one linear output:
$$W^{(1)}=\begin{pmatrix}2&1\\-1&1\end{pmatrix},\ b^{(1)}=\begin{pmatrix}-1\\0\end{pmatrix},\quad W^{(2)}=\begin{pmatrix}1&-3\end{pmatrix},\ b^{(2)}=2,\quad x=\begin{pmatrix}1\\-1\end{pmatrix}.$$

1. Pre-activation: $z^{(1)} = W^{(1)}x+b^{(1)} = (2\cdot1+1\cdot(-1)-1,\ -1\cdot1+1\cdot(-1)+0) = (0,\,-2)$.
2. ReLU: $h^{(1)}=(\max(0,0),\max(0,-2)) = (0,0)$. Both units are "off" for this input.
3. Output: $\hat y = 1\cdot0 - 3\cdot0 + 2 = 2$.

Now take $x=(2,1)$: $z^{(1)}=(4,-1)$, $h^{(1)}=(4,0)$, $\hat y = 4+2 = 6$. Different inputs switch different units on, and that switching pattern is what makes the overall function piecewise linear instead of linear.

**Parameter count** for a $100\to 50\to 5$ MLP: $(100+1)\cdot 50 + (50+1)\cdot 5 = 5050+255 = 5305$ parameters, almost all in the first layer. Wide input layers dominate the count.

## The wider picture

- **Training**: [[Backpropagation]] + [[Optimizers]]; initialization (He/Xavier) matters, see [[Training Tricks]]. Backpropagation computes $\partial L/\partial W^{(l)}$ for every layer in one backward sweep; the optimizer turns those gradients into weight updates. Initialization matters because a badly scaled start makes activations (and gradients) shrink or blow up layer after layer.
- Non-linearities: [[Activation Functions]]. ReLU is the default for hidden layers; GELU in Transformers; sigmoid/softmax mainly at the output.
- Architectures: [[CNN]] (images), [[RNN and LSTM]] (sequences), [[Transformers]] (everything now), [[Graph Neural Networks]]. These are all the same "linear map + non-linearity" idea with weights *shared* in a way that matches the data's structure (across image positions, time steps, tokens, graph edges).
- Regularization: weight decay, dropout, early stopping, augmentation ([[Overfitting and Regularization]]). Neural networks have enough capacity to memorise training data, so these are what make them generalise.

## Common confusions

- **"More layers without activations = more power."** No: linear layers compose to one linear layer. Without $\phi$ a 10-layer net is a linear model (it can still differ in how it *trains*, but not in what it can represent).
- **"Universal approximation means a one-hidden-layer net is all you need."** It guarantees existence, not efficiency, learnability or generalisation. Deep nets are used precisely because they need far fewer units and train well.
- **"Softmax for multi-label problems."** Softmax forces the probabilities to sum to 1 (exactly one class). For "any subset of labels" use one sigmoid + BCE per label.
- **"Neurons are like brain neurons."** The biological analogy is loose; a unit is just a weighted sum followed by a fixed function.
- **"The hidden units have to mean something."** They are whatever features make the final linear layer's job easy; they are often not human-interpretable.

## Check yourself

> [!question]- A network with layer sizes $20\to 10\to 3$ has how many parameters?
> $(20+1)\cdot 10 + (10+1)\cdot 3 = 210 + 33 = 243$.

> [!question]- Why can't a deep network with $\phi(z)=z$ solve XOR?
> The composition of affine maps is affine, so the whole network is one linear model; XOR's classes are not linearly separable in input space.

> [!question]- You need to predict a probability distribution over 5 star ratings. Output layer and loss?
> 5 output units with softmax, trained with cross-entropy.

> [!question]- What does the universal approximation theorem fail to guarantee?
> How many hidden units are needed, that gradient descent finds the approximating weights, and that the trained network generalises beyond the training data.

> [!question]- In the worked example, why did the output not depend on $W^{(2)}$ for $x=(1,-1)$?
> Both hidden units had $z\le 0$, so ReLU output 0 for both; only the output bias $b^{(2)}=2$ remained.

## Practice

[Neural Networks - Exercises](Neural%20Networks%20-%20Exercises.ipynb): concepts (non-linearity, output/loss pairing, depth), forward passes and XOR by hand, a tent function from ReLUs, a stable softmax cross-entropy, and training small MLPs on two moons and digits.

## Learn more
- [MIT 6.S191 — Introduction to Deep Learning (lecture playlist)](https://www.youtube.com/playlist?list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI) · [course site & labs](https://introtodeeplearning.com/)
- [3Blue1Brown – Neural Networks](https://www.3blue1brown.com/topics/neural-networks)
- [Nielsen – Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) (chapter 4 gives a visual proof of universal approximation)
- [Dive into Deep Learning](https://d2l.ai/)
- [colah – Neural Networks, Manifolds, and Topology](https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/) (the "stretch and fold the space" picture)
