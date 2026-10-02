---
tags: [ml, deep-learning, sequence]
---
# RNN and LSTM

> [!summary] In one sentence
> A recurrent network reads a sequence one step at a time and carries a hidden state $h_t$ forward as its "memory", reusing the same weights at every step; the LSTM adds a gated cell state $c_t$ with an (almost) additive update so that gradients, and therefore memories, can survive over long sequences.

## Intuition first

Read this sentence word by word. You do not restart your understanding at every word: you keep a running summary ("someone is reading... a sentence... word by word") and update it as each new word arrives. A **recurrent neural network (RNN)** does exactly this. At step $t$ it combines the new input $x_t$ with its previous summary $h_{t-1}$ to get a new summary $h_t$.

Two consequences:

- **Weight sharing through time.** The same update rule (same matrices) is applied at every step, just as a CNN applies the same kernel at every position. So the number of parameters does not depend on the sequence length, and the model can read sequences of any length.
- **Long paths for the gradient.** To learn that word 1 matters for the prediction at word 50, the error signal must travel backwards through 49 copies of the update. If each copy shrinks the signal a bit, almost nothing arrives (**vanishing gradients**); if each copy grows it, it explodes.

The **LSTM** fixes this with a separate "conveyor belt", the cell state $c_t$. Information on the belt is only *scaled by a forget gate and added to*, never squashed through a full matrix multiplication and nonlinearity. If the forget gate stays near 1, the memory (and its gradient) rides along almost unchanged for hundreds of steps.

![Gradient bars under an unrolled RNN shrink by 0.6 per step while the LSTM cell path keeps them near 1](../../Attachments/ML%20Animations/RNN%20and%20LSTM%20-%20gradient%20flow.gif)

*Watch the bars fill in from the loss backwards: in the plain RNN each step multiplies the gradient by about 0.6, so after six steps only 5 % is left, while along the LSTM cell path a forget gate of 0.97 keeps 83 %.*

## The math, step by step

### The vanilla RNN

$$h_t=\phi(W_hh_{t-1}+W_xx_t+b)$$

- $x_t\in\mathbb R^d$: input at step $t$; $h_t\in\mathbb R^H$: hidden state; $h_0$ is usually zeros.
- $W_x\in\mathbb R^{H\times d}$ maps the input in, $W_h\in\mathbb R^{H\times H}$ maps the old state to the new one, $b$ is a bias, $\phi$ a nonlinearity (usually $\tanh$).
- Shared weights across time: the same $W_h,W_x,b$ at every step. Parameters: $H(d+H)+H$.
- An output, if needed, is read off each state: $y_t=W_yh_t+b_y$.

### Training: backpropagation through time

"Unroll" the loop into a deep feed-forward network with one layer per time step (all layers sharing weights), then run ordinary backprop ([[Backpropagation]]). Because the weights are shared, the gradient for $W_h$ is the **sum** of its gradients from every time step.

### The problem: gradients vanish or explode

Gradients vanish/explode over long sequences. By the chain rule, how much $h_T$ depends on an early state is a product of per-step Jacobians:

$$\frac{\partial h_T}{\partial h_0}=\prod_{t=1}^{T}\frac{\partial h_t}{\partial h_{t-1}}=\prod_{t=1}^{T}\mathrm{diag}\big(\phi'(a_t)\big)\,W_h$$

where $a_t$ is the pre-activation. In the scalar linear case $h_t=w\,h_{t-1}+x_t$ this is simply $w^T$:

- $|w|<1$: $w^T\to0$ exponentially (vanishing): early inputs cannot be learned from.
- $|w|>1$: $w^T\to\infty$ (exploding): training blows up.

For matrices the same happens with the singular values of $W_h$, and $|\tanh'|\le1$ only makes vanishing worse. Exploding gradients have a cheap fix, **gradient clipping**: if the global norm $\sqrt{\sum_k\lVert g_k\rVert^2}$ exceeds a threshold, rescale all gradients by the same factor (direction kept, length capped). Vanishing gradients need an architectural fix: the LSTM.

### The LSTM

Gates control a cell state $c_t$:
$f_t=\sigma(\cdot)$ (forget), $i_t=\sigma(\cdot)$ (input), $o_t=\sigma(\cdot)$ (output),
$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t,\quad h_t=o_t\odot\tanh c_t$.

Written out, with $[x_t;h_{t-1}]$ the concatenation of input and previous hidden state:

$$f_t=\sigma(W_f[x_t;h_{t-1}]+b_f),\quad i_t=\sigma(W_i[x_t;h_{t-1}]+b_i),\quad o_t=\sigma(W_o[x_t;h_{t-1}]+b_o)$$
$$\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)$$

What each piece does:

- $\sigma$ outputs numbers in $(0,1)$, so every gate is a soft on/off switch, element by element ($\odot$ is element-wise multiplication).
- **Forget gate** $f_t$: how much of the old memory $c_{t-1}$ to keep.
- **Input gate** $i_t$ and candidate $\tilde c_t$: what new information to write, and how much of it.
- **Output gate** $o_t$: how much of the (squashed) memory to expose as the hidden state $h_t$.

Why it fixes vanishing gradients: along the cell path,

$$\frac{\partial c_t}{\partial c_{t-1}}=f_t \quad(\text{ignoring the indirect paths through the gates}),\qquad \frac{\partial c_T}{\partial c_0}=\prod_t f_t.$$

There is no weight matrix and no $\tanh'$ in this product, only the forget gates, which the network can learn to hold near 1. This is the "constant error carousel".

An LSTM layer has four blocks of the RNN's size, so $4\big(H(d+H)+H\big)$ parameters.

### The GRU

**GRU**: fewer gates, similar performance. It merges the cell and hidden state and uses two gates (convention used in the exercises, as in d2l):

$$z=\sigma(W_z[x;h]+b_z),\quad r=\sigma(W_r[x;h]+b_r),\quad \tilde h=\tanh(W_c[x;\,r\odot h]+b_c),\quad h'=z\odot h+(1-z)\odot\tilde h$$

- **Update gate** $z$ plays the role of forget + input gate together: keep the old state ($z\approx1$) or overwrite it.
- **Reset gate** $r$ decides how much of the old state is used when proposing the candidate.
- Three blocks instead of four: $3\big(H(d+H)+H\big)$ parameters.

## Worked example

**Unrolling a scalar RNN.** $h_t=\tanh(0.5\,h_{t-1}+x_t)$, $h_0=0$, inputs $x=(1,0,-1)$:

- $h_1=\tanh(0+1)=0.7616$
- $h_2=\tanh(0.5\cdot0.7616+0)=\tanh(0.3808)=0.3634$
- $h_3=\tanh(0.5\cdot0.3634-1)=\tanh(-0.8183)=-0.6741$

The first input's influence fades by about half each step, unless new inputs reinforce it.

**One LSTM step.** Gates $f_t=0.9$, $i_t=0.2$, $o_t=0.8$, candidate $\tilde c_t=0.5$, old cell $c_{t-1}=1$:

- $c_t=0.9\cdot1+0.2\cdot0.5=1.0$
- $h_t=0.8\cdot\tanh(1.0)=0.8\cdot0.7616=0.609$

**Vanishing vs exploding in numbers.** Linear scalar RNN with $T=50$: $0.9^{50}\approx0.005$, $1.1^{50}\approx117$. A forget gate held at $0.99$ for 100 steps gives $0.99^{100}\approx0.37$: a third of the gradient survives 100 steps.

**Parameter count**, $d=10$, $H=20$: RNN $20\cdot30+20=620$; LSTM $4\cdot620=2480$; GRU $3\cdot620=1860$.

## Variants

Bidirectional, stacked, seq2seq with attention. Largely replaced by [[Transformers]] for NLP, but still used for small/streaming problems.

- **Bidirectional**: one RNN reads left-to-right, another right-to-left, and their states are concatenated, so each position sees both past and future context. Great for tagging a whole sentence; impossible for real-time prediction, because the future has not arrived yet.
- **Stacked** (deep): the hidden states of one RNN layer are the inputs of the next.
- **Seq2seq with attention**: an encoder RNN reads the input, a decoder RNN writes the output; attention lets the decoder look back at all encoder states instead of a single summary vector. This attention mechanism is the direct ancestor of the Transformer.
- **Why Transformers won**: an RNN must process steps one after another (no parallelism over time) and squeezes all history into a fixed-size state. Self-attention connects every pair of positions directly and trains in parallel.
- **Why RNNs survive**: constant memory and constant work per new step, which is ideal for streaming data, on-device models and small datasets (and modern state-space models revive this idea).

## Common confusions

- "An RNN has a separate set of weights per time step." → One set, reused at every step; unrolling only copies it for the backward pass.
- "LSTMs fix exploding gradients." → They mainly fix *vanishing* gradients; exploding gradients are still handled with gradient clipping.
- "The forget gate forgets when it is 1." → $f_t=1$ means *keep everything*; $f_t=0$ means wipe the memory.
- "The hidden state and the cell state are the same thing." → $c_t$ is the long-term memory; $h_t=o_t\odot\tanh c_t$ is a filtered view of it used for outputs and for the gates.
- "Bidirectional RNNs work for live speech recognition." → They need the whole sequence first; streaming tasks need unidirectional models.

## Check yourself

> [!question]- Why does the number of RNN parameters not depend on the sequence length?
> The same $W_h$, $W_x$ and $b$ are reused at every time step (weight sharing through time).

> [!question]- In the linear scalar RNN $h_t=w\,h_{t-1}+x_t$, what is $\partial h_T/\partial h_0$, and what happens for $w=0.5$, $T=10$?
> $w^T=0.5^{10}\approx0.001$: the gradient from step 10 back to step 0 has essentially vanished.

> [!question]- Which LSTM equation creates the "gradient highway", and why?
> $c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t$: the old cell is only multiplied by the forget gate and added to, so $\partial c_t/\partial c_{t-1}=f_t$, with no weight matrix or squashing derivative.

> [!question]- How many parameters does an LSTM layer have compared with a vanilla RNN of the same sizes?
> Four times as many: one RNN-sized block each for $f$, $i$, $o$ and $\tilde c$.

> [!question]- What does gradient clipping by global norm do to the direction of the update?
> Nothing: all gradients are scaled by the same factor, so only the length is capped.

## Practice

[RNN and LSTM - Exercises](RNN%20and%20LSTM%20-%20Exercises.ipynb): weight sharing, why the LSTM fixes vanishing gradients, GRU and bidirectional RNNs, unrolling and LSTM steps by hand, parameter counts, the constant error carousel, then NumPy implementations of an RNN forward pass, BPTT, vanishing/exploding experiments, LSTM and GRU cells, gradient clipping and a bidirectional RNN.

## Learn more

- [Dive into Deep Learning](https://d2l.ai/)
- [colah – Understanding LSTMs](https://colah.github.io/)
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
- [Karpathy – The Unreasonable Effectiveness of Recurrent Neural Networks](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)
