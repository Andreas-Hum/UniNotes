---
tags: [ml, deep-learning, optimization]
---
# Optimizers

> [!summary] In one sentence
> Optimizers decide how to turn a (noisy) gradient into a weight update: plain SGD steps straight downhill, momentum adds inertia to smooth out zig-zags, adaptive methods (AdaGrad, RMSProp, Adam) give every parameter its own step size, and AdamW adds properly decoupled weight decay.

## Intuition first

Build on [[Gradient Descent]]: $w \leftarrow w - \eta\,g$, where $g=\nabla L(w)$ and $\eta$ is the learning rate.

Real loss surfaces are not round bowls. A very common shape is a **long, narrow ravine**: steep walls in one direction, a gentle slope along the floor. Plain gradient descent has a dilemma there:

- The gradient points mostly *across* the ravine (towards the nearest wall), not along it.
- A learning rate large enough to make progress along the floor makes you bounce from wall to wall; a rate small enough to stop the bouncing makes progress along the floor painfully slow.

Two fixes, and modern optimizers combine both:

1. **Momentum** (a heavy ball instead of a hiker): keep a running velocity. The across-the-ravine components flip sign every step and cancel out; the along-the-floor components always point the same way and add up. Result: less zig-zag, more speed where it matters.
2. **Adaptive step sizes** (per-parameter learning rates): divide each coordinate's step by a running estimate of how big that coordinate's gradients usually are. Steep directions get small steps, flat directions get big ones, so the ravine effectively becomes a round bowl.

![SGD, momentum and Adam racing through a narrow elliptical ravine towards the minimum](../../Attachments/ML%20Animations/Optimizers%20-%20SGD%20vs%20momentum%20vs%20Adam.gif)

*All three runs take the same 30 steps. Watch SGD (red) bounce between the steep walls and crawl along the floor, momentum (blue) damp the bouncing and reach the star, and Adam (yellow) take an almost straight, evenly sized path (and overshoot a little).*

## The optimizers at a glance

| Optimizer | Key idea |
|---|---|
| SGD + momentum | velocity accumulates gradient |
| Nesterov | gradient at look-ahead point |
| AdaGrad | per-parameter rate $\eta/\sqrt{\sum g^2}$ |
| RMSProp | exponential moving average of $g^2$ |
| **Adam** | momentum + RMSProp with bias correction ($\beta_1=0.9,\beta_2=0.999,\epsilon=10^{-8}$) |
| **AdamW** | Adam with decoupled weight decay (default for Transformers) |
| Lion, Adafactor, LAMB | memory- or large-batch-oriented variants |

## The math, step by step

Notation: $g_t$ is the (mini-batch) gradient at step $t$, $\eta$ the learning rate, all operations on vectors are element-wise.

### Why plain GD struggles: the stability limit
On a quadratic $f(w)=\tfrac12\sum_i\lambda_i w_i^2$, GD updates each coordinate independently: $w_i\leftarrow(1-\eta\lambda_i)\,w_i$. This converges only if $|1-\eta\lambda_i|<1$ for all $i$, i.e.
$$\eta < \frac{2}{\lambda_{\max}}.$$
The slowest direction then shrinks by a factor $1-\eta\lambda_{\min}\approx 1-2\lambda_{\min}/\lambda_{\max}=1-2/\kappa$ per step, where $\kappa=\lambda_{\max}/\lambda_{\min}$ is the **condition number**. A ravine is just a large $\kappa$: the steep direction caps the learning rate, and the flat direction then takes $O(\kappa)$ steps.

### SGD + momentum
$$v_t=\beta v_{t-1}+g_t,\qquad w_t=w_{t-1}-\eta\,v_t.$$
The velocity $v$ is a running sum of past gradients, discounted by $\beta$ (typically $0.9$). If the gradient is constant, $v_t\to g/(1-\beta)$, so momentum multiplies the effective step by $1/(1-\beta)$ (10× for $\beta=0.9$) in consistent directions, while oscillating components largely cancel. (Some libraries write $v_t=\beta v_{t-1}+(1-\beta)g_t$; that is the same thing with $\eta$ rescaled.)

### Nesterov momentum
Evaluate the gradient at the **look-ahead point** $w-\eta\beta v$ (where momentum is about to carry you) instead of at $w$. If you are about to overshoot, the look-ahead gradient already points back, so Nesterov brakes earlier and oscillates less. The PyTorch form is $v\leftarrow\beta v+g$, $w\leftarrow w-\eta(g+\beta v)$.

### AdaGrad
$$G_t=G_{t-1}+g_t^2,\qquad w_t=w_{t-1}-\eta\,\frac{g_t}{\sqrt{G_t}+\epsilon}.$$
Each parameter's rate is $\eta/\sqrt{\sum g^2}$: parameters with big or frequent gradients slow down, rare ones (e.g. embeddings of rare words) keep large steps. The flaw: $G_t$ only grows, so the effective rate decays like $1/\sqrt t$ and eventually stalls, which is bad for the long training runs of deep networks.

### RMSProp
Replace the sum by an **exponential moving average** (EMA):
$$s_t=\rho\,s_{t-1}+(1-\rho)\,g_t^2,\qquad w_t=w_{t-1}-\eta\,\frac{g_t}{\sqrt{s_t}+\epsilon}.$$
Old gradients are forgotten at rate $\rho$ ($\approx0.9$), so the step size adapts to the *recent* gradient scale and does not decay to zero. Under a constant gradient $g$, the step tends to $\eta\,g/|g|=\eta$.

### Adam
Momentum on $g$ plus RMSProp on $g^2$, with a correction for starting at zero:
$$m_t=\beta_1 m_{t-1}+(1-\beta_1)g_t,\qquad v_t=\beta_2 v_{t-1}+(1-\beta_2)g_t^2,$$
$$\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad \hat v_t=\frac{v_t}{1-\beta_2^t},\qquad w_t=w_{t-1}-\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.$$
In words: $m$ is a smoothed gradient ("which way"), $\sqrt{v}$ a smoothed gradient magnitude ("how big usually"), and their ratio is a step of roughly size $\eta$ in each coordinate, regardless of the gradient's scale.

**Why bias correction?** With $m_0=0$ and a constant input $x$, an EMA gives $m_t=(1-\beta^t)\,x$, so early on it badly underestimates $x$ (with $\beta_2=0.999$, $v_{10}$ has only reached about 1% of its target). Dividing by $1-\beta^t$ removes exactly this bias. Without it, $v$ is far too small in the first steps and the first updates are much larger than intended.

### AdamW: decoupled weight decay
For SGD, adding $\frac\lambda2\|w\|^2$ to the loss is the same as shrinking weights, $w\leftarrow(1-\eta\lambda)w$. For Adam it is not: the L2 gradient $\lambda w$ gets divided by $\sqrt{\hat v}$ like every other gradient, so weights with large gradient history are barely regularised. AdamW applies the decay **outside** the adaptive step:
$$w_t=w_{t-1}-\eta\Big(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}+\lambda\,w_{t-1}\Big),$$
so every weight shrinks at the same relative rate. This is the default for [[Transformers]].

### Lion, Adafactor, LAMB
Lion keeps only a momentum buffer and steps by its sign (less memory than Adam). Adafactor stores a factored (row × column) approximation of $v$ for large matrices, also to save memory. LAMB rescales Adam's update per layer ("trust ratio") so very large batches stay stable.

## Worked example

Minimise $f(w)=w^2$ (gradient $2w$) from $w_0=1$ with $\eta=0.1$.

**SGD:** $w_1=1-0.1\cdot2=0.8$, $w_2=0.8-0.1\cdot1.6=0.64$. Each step multiplies $w$ by $0.8$.

**Momentum ($\beta=0.9$):**
- $v_1=2$, $w_1=1-0.1\cdot2=0.8$.
- $v_2=0.9\cdot2+1.6=3.4$, $w_2=0.8-0.34=0.46$.

The remembered velocity made the second step more than twice as large, so momentum is already ahead (0.46 vs. 0.64). On this round bowl it will later overshoot and oscillate a bit; in a ravine that inertia is what carries it along the floor.

**Adam's scale invariance:** two parameters with first gradients $100$ and $0.01$. After bias correction, $\hat m_1=g_1$ and $\hat v_1=g_1^2$, so the first step is $\eta\,g_1/|g_1|$: both parameters move by $\approx\eta$. Plain SGD would move the first one $10^4$ times further than the second.

**Warm-up + cosine:** warm up linearly to $\eta_{\max}$ over $t_w$ steps, then
$$\eta_t=\eta_{\max}\cdot\tfrac12\Big(1+\cos\big(\pi\,\tfrac{t-t_w}{T-t_w}\big)\Big),\quad t_w\le t\le T.$$
With $\eta_{\max}=10^{-3}$, $t_w=100$, $T=1000$: halfway through the decay ($t=550$) the cosine is $\cos(\pi/2)=0$, so $\eta=0.5\times10^{-3}$.

## Practical

- Adam: $\eta\approx10^{-3}$ (CNN/MLP), $10^{-4}$ for transformers; SGD+momentum often generalizes better for vision. A common explanation is that Adam's per-parameter scaling lets it settle into sharper minima, while SGD's noise favours flatter ones; people still default to Adam because it works out of the box with far less learning-rate tuning.
- Use warm-up + cosine/linear decay. **Warm-up** protects the start: Adam's $\hat v$ estimates are unreliable in the first steps and the random initial weights produce large, poorly aligned gradients, so a small rate avoids early blow-ups (especially with large batches). **Decay** at the end lets the iterate settle into the minimum instead of bouncing around at the noise level of the mini-batch gradient.
- Gradient clipping (norm 1.0) for [[RNN and LSTM]] and [[Transformers]]: rescale the whole gradient vector when its norm exceeds 1.0, which caps the damage of a rare huge gradient (exploding gradients, loss spikes) without changing its direction.
- If training diverges, lower $\eta$ first; if it is just slow, try momentum/Adam before raising $\eta$.

## Common confusions

- **"Adam + L2 regularisation = AdamW."** No: with Adam the L2 gradient is rescaled by $1/\sqrt{\hat v}$, so the effective decay differs per weight. AdamW decouples it.
- **"Adaptive methods don't need a learning rate."** They still have $\eta$ and it still matters; they just make it less sensitive to gradient scale.
- **"Momentum means bigger steps, so it's less stable."** Momentum allows a larger stable rate on ill-conditioned problems and damps oscillation across ravines; it can overshoot, which is what Nesterov reduces.
- **"$\epsilon$ is just for numerical safety."** Mostly, but if it is large compared with $\sqrt{\hat v}$ it turns Adam into something closer to SGD with momentum.
- **"Bias correction matters all the time."** Only for the first few hundred / thousand steps; once $\beta^t\approx0$ it does nothing.

## Check yourself

> [!question]- With a constant gradient, by what factor does momentum with $\beta=0.99$ amplify the step?
> $1/(1-\beta)=100$.

> [!question]- For $f(w)=\tfrac12(w_1^2+25w_2^2)$, what is the largest stable learning rate for plain GD, and what is $\kappa$?
> $\eta<2/\lambda_{\max}=2/25=0.08$; $\kappa=25/1=25$.

> [!question]- Why does AdaGrad stall in long training runs, and how does RMSProp fix it?
> $G_t$ is a sum of squared gradients that only grows, so the step $\eta/\sqrt{G_t}$ goes to zero; RMSProp uses a moving average, which forgets old gradients and stays at the current gradient scale.

> [!question]- What does $\hat v_t$ correct for in Adam?
> The bias towards zero from initialising $v_0=0$: early EMA values equal $(1-\beta_2^t)$ times the true average, so dividing by $1-\beta_2^t$ un-biases them.

> [!question]- In the warm-up + cosine schedule above, what is $\eta$ at the very end ($t=T$)?
> $\cos\pi=-1$, so $\eta_T=\eta_{\max}\cdot\tfrac12(1-1)=0$.

## Practice

[Optimizers - Exercises](Optimizers%20-%20Exercises.ipynb): momentum and Nesterov, Adam vs. AdamW, the effective rate of momentum, bias correction, AdaGrad and the stability limit by hand, writing SGD/momentum/Nesterov/Adam/AdaGrad/RMSProp from scratch, an optimizer race, and a warm-up + cosine scheduler.

## Learn more
- [Dive into Deep Learning](https://d2l.ai/) – Optimization chapter
- [Adam paper](https://arxiv.org/abs/1412.6980)
- [Distill – Why Momentum Really Works](https://distill.pub/2017/momentum/) (interactive)
- [Ruder – An overview of gradient descent optimization algorithms](https://www.ruder.io/optimizing-gradient-descent/)
- [AdamW paper – Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)
