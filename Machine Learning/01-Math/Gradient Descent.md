---
tags: [ml, math, optimization]
status: not-started
notebook: not-started
level:
reviewed:
---
# Gradient Descent

> [!summary] In one sentence
> Gradient descent minimizes a loss by repeatedly taking a small step in the direction that decreases it fastest, $\theta_{t+1}=\theta_t-\eta\nabla_\theta L(\theta_t)$; almost every model in ML, from logistic regression to GPT, is trained by some variant of this one line.

## Intuition first

You are on a foggy hillside and want to reach the valley floor. You cannot see far, but you can feel which way the ground slopes under your feet. So you take a step downhill, feel again, take another step, and so on. That is gradient descent:
- The **gradient** $\nabla L$ is the direction of steepest *ascent*; you go the opposite way.
- The **learning rate** $\eta$ is your stride length. Tiny strides: you will get there, eventually. Huge strides: you overshoot the valley and land higher up on the other side, possibly bouncing further each time.
- **Stochastic** gradient descent is doing this while slightly drunk: each step is based on a random handful of examples, so the direction is noisy, but on average it is right and each step is much cheaper.
- **Momentum** is letting yourself roll like a heavy ball: you keep some of your previous velocity, so random sideways jitter cancels out and consistent downhill directions build up speed.

**What problem does it solve?** Most losses have no closed-form minimizer (or one that is too expensive, like inverting a huge matrix). Gradient descent only needs the gradient, which [[Backpropagation]] computes in about the cost of one forward pass, and it scales to billions of parameters.

## The math, step by step

$$\theta_{t+1}=\theta_t-\eta\,\nabla_\theta L(\theta_t)$$

- $\theta_t$: parameters at step $t$; $L$: the loss (average over training examples); $\nabla_\theta L$: vector of partial derivatives; $\eta>0$: learning rate (step size).
- Why the negative gradient: by the first-order Taylor expansion, $L(\theta-\eta g)\approx L(\theta)-\eta\lVert g\rVert^2$ with $g=\nabla L$, which is a decrease whenever $g\neq0$ and $\eta$ is small enough. Among all directions of a given length, $-g$ decreases $L$ fastest.

### Variants
| Variant | Gradient computed on | Trade-off |
|---|---|---|
| Batch | all $N$ samples | exact, slow |
| **Stochastic (SGD)** | 1 sample | noisy, cheap, escapes bad minima |
| **Mini-batch** | $B$ samples (32–512) | standard; GPU friendly |

Why mini-batches work: if $L=\frac1N\sum_i\ell_i$, the mini-batch gradient $g_B=\frac1B\sum_{i\in B}\nabla\ell_i$ (batch drawn uniformly at random) is an **unbiased** estimate, $\mathbb E[g_B]=\nabla L$, with variance shrinking like $1/B$. So each step points the right way on average, at a fraction of the cost. Larger $B$ means less noise but diminishing returns (doubling $B$ only cuts the noise std by $\sqrt2$) and fills the GPU; noise also helps escape saddle points and sharp minima.

An **epoch** = one pass over the data = $N/B$ steps.

## Learning rate

![Same bowl, three learning rates](../../Attachments/ML%20Animations/Gradient%20Descent%20-%20learning%20rate%20too%20small%20vs%20good%20vs%20too%20big.gif)
*On $L=\theta^2$ (curvature 2): with $\eta=0.08$ the ball creeps; with $\eta=0.4$ it is at the bottom in a few steps; with $\eta=1.05>2/2$ every step overshoots further and the iterates fly off.*

- Too large → diverges/oscillates; too small → slow.
- For quadratics, stable if $\eta<2/\lambda_{max}(H)$. **Derivation**: for $L=\frac12\theta^\top H\theta$, $\nabla L=H\theta$, so $\theta_{t+1}=(I-\eta H)\theta_t$. Along the eigenvector with eigenvalue $\lambda_i$ the error is multiplied by $(1-\eta\lambda_i)$ each step. Convergence needs $|1-\eta\lambda_i|<1$ for every $i$, i.e. $0<\eta<2/\lambda_i$; the binding one is $\lambda_{\max}$. With $1<\eta\lambda<2$ the sign flips every step (oscillating but converging); beyond 2 it explodes.
- The slowest direction is the flattest one, shrinking by $1-\eta\lambda_{\min}$ per step. The best fixed step $\eta^*=\frac2{\lambda_{\max}+\lambda_{\min}}$ gives a contraction factor $\frac{\kappa-1}{\kappa+1}$ with $\kappa=\lambda_{\max}/\lambda_{\min}$ the condition number: badly conditioned problems (long ravines) are slow. This is why we standardize features.
- Schedules: step decay, cosine, warm-up, 1-cycle.
  - *Step decay*: divide $\eta$ by 10 at fixed epochs.
  - *Cosine*: $\eta_t=\eta_{\min}+\frac12(\eta_{\max}-\eta_{\min})(1+\cos(\pi t/T))$, smoothly from large to small.
  - *Warm-up*: start tiny and ramp up over the first steps, so early large, unreliable gradients (and adaptive optimizer statistics) do not blow things up.
  - *1-cycle*: ramp up then down within one run; often trains fastest.
- **Backtracking line search** (when you can afford extra function evaluations): start with a big step $t$ and shrink $t\leftarrow\beta t$ until the Armijo condition $L(\theta-t g)\le L(\theta)-\alpha t\lVert g\rVert^2$ holds.

## Momentum

![Plain GD zig-zags across a ravine; momentum rolls along it](../../Attachments/ML%20Animations/Gradient%20Descent%20-%20momentum%20vs%20plain%20GD%20in%20a%20ravine.gif)
*Same step size on a long narrow bowl (condition number 50). Red, plain GD, bounces between the steep walls and crawls along the floor; yellow, momentum ($\beta=0.7$), averages the bouncing away and builds speed along the floor, arriving after 25 steps.*

$v\leftarrow\beta v+\nabla L,\ \theta\leftarrow\theta-\eta v$ — smooths noise, accelerates along ravines. Adaptive variants in [[Optimizers]].

Why: unrolling, $v_t=\sum_{k\le t}\beta^{t-k}\nabla L(\theta_k)$, an exponentially weighted sum of past gradients. Components that flip sign every step (the zig-zag across a ravine, or SGD noise) cancel out; components that point the same way every step add up, to an effective step of about $\eta/(1-\beta)$ (10× for $\beta=0.9$). Typical $\beta=0.9$.

## Convergence
Convex + L-smooth: $O(1/t)$; strongly convex: linear rate. SGD needs decaying $\eta$.
- **L-smooth**: the gradient is Lipschitz with constant $L$, i.e. curvature at most $L$ (here $L$ is a number, not the loss). With $\eta=1/L$, the loss gap after $t$ steps is at most $\frac{L\,\lVert\theta_0-\theta^*\rVert^2}{2t}$: sublinear, error $\propto1/t$ (10× more steps for 10× less error).
- **Strongly convex** (curvature $\ge\mu>0$): error shrinks by a constant factor each step, like $(1-\mu/L)^t$: "linear" convergence (a straight line on a log plot; each step gains a fixed number of digits).
- **SGD needs decaying $\eta$**: with constant $\eta$, the gradient noise never vanishes even at the optimum, so iterates bounce around in a "noise floor" whose size scales with $\eta$. Convergence to the exact minimum needs $\sum_t\eta_t=\infty$ (can travel any distance) and $\sum_t\eta_t^2<\infty$ (noise eventually averages out), e.g. $\eta_t\propto1/t$.

## Debugging
Overfit a tiny batch first; check loss goes down; gradient-check numerically. See [[Training Tricks]].
- **Overfit a tiny batch** (e.g. 10 examples): a working model + optimizer must drive training loss near zero. If not, the bug is in the model, loss or gradient, not in the data size.
- **Read the loss curve**: diverging or NaN → $\eta$ too large (or a bug); flat from the start → $\eta$ too small or dead gradients; noisy but trending down → fine (try larger $B$ or smaller $\eta$ later); train down but validation up → overfitting, not an optimizer problem.
- **Gradient check**: compare analytic gradients with centred differences $\frac{L(\theta+he_i)-L(\theta-he_i)}{2h}$ ($h\approx10^{-5}$, float64); relative error around $10^{-7}$ is good, $10^{-2}$ means a bug.

## Worked example

$L(\theta)=(\theta-3)^2$, so $\nabla L=2(\theta-3)$. Start $\theta_0=0$, $\eta=0.1$.
1. $\nabla L(0)=-6$ → $\theta_1=0-0.1(-6)=0.6$.
2. $\nabla L(0.6)=-4.8$ → $\theta_2=0.6+0.48=1.08$.
3. Pattern: the error $\theta-3$ goes $-3\to-2.4\to-1.92$, multiplied by $1-\eta\cdot2=0.8$ each step (linear convergence). Stability needs $\eta<2/2=1$; $\eta=0.5$ would land on 3 in one step; $\eta=1$ would bounce between 0 and 6 forever.

Momentum by hand with $\beta=0.9$, constant gradient $g=1$: $v=1,\,1.9,\,2.71,\,3.44,\dots\to\frac1{1-0.9}=10$. The ball accelerates to 10× the plain step.

## Common confusions
- **"The gradient points to the minimum."** → It points to the steepest *local* ascent. In a ravine it points mostly across the ravine, not along it, which is why plain GD zig-zags.
- **"Bigger batch is always better."** → Each step is more accurate but more expensive, and you take fewer steps per epoch; very large batches often need a larger $\eta$ plus warm-up and can generalize worse.
- **"Loss went up for one step, so training is broken."** → With SGD the loss per mini-batch is noisy. Look at a smoothed curve or the epoch average.
- **"If the loss decreases, the gradient is correct."** → A slightly wrong gradient can still decrease the loss. Gradient-check numerically.
- **"With constant $\eta$, SGD converges to the minimum."** → It converges to a noisy neighbourhood of it; you need a decaying schedule to settle.

## Check yourself

> [!question]- On $L=\frac12(\theta_1^2+100\theta_2^2)$, what is the largest stable step size, and why is convergence slow?
> $\lambda_{\max}=100$, so $\eta<0.02$. Along $\theta_1$ (curvature 1) the error then shrinks by at least $1-0.02=0.98$ per step: hundreds of steps. Condition number 100.

> [!question]- Why is the mini-batch gradient unbiased?
> Each example is equally likely to be in the batch, so $\mathbb E[\frac1B\sum_{i\in B}\nabla\ell_i]=\frac1N\sum_i\nabla\ell_i=\nabla L$ by linearity of expectation.

> [!question]- What is the effective step size of momentum with $\beta=0.9$ in a direction where the gradient is constant?
> $\eta/(1-\beta)=10\eta$.

> [!question]- Linear vs sublinear: how many more steps to go from error $10^{-2}$ to $10^{-4}$?
> Sublinear $O(1/t)$: 100× more steps. Linear (factor $\rho<1$ per step): a fixed extra number of steps, $\ln(100)/\ln(1/\rho)$.

> [!question]- Your loss is NaN after 50 steps. First two things to try?
> Lower the learning rate (and/or add warm-up or gradient clipping), and check for numerical issues such as `log(0)` or an unstable softmax. Then overfit a tiny batch to confirm the pipeline works.

## Practice
[Gradient Descent - Exercises](Gradient%20Descent%20-%20Exercises.ipynb): batch vs mini-batch, loss-curve reading, stability limit and optimal fixed step, momentum as an exponential sum, linear vs sublinear rates, then code: a generic GD loop, the divergence threshold, mini-batch SGD and its noise floor, momentum on a ravine, schedules, gradient checks and backtracking line search.

## Learn more
- [Dive into Deep Learning](https://d2l.ai/) – Optimization chapter
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 7
- [3Blue1Brown – Neural Networks](https://www.3blue1brown.com/topics/neural-networks)
- [distill.pub – Why Momentum Really Works](https://distill.pub/2017/momentum/): interactive explanation of momentum on ravines.
- [Stanford CS231n – Optimization notes](https://cs231n.github.io/optimization-1/)
