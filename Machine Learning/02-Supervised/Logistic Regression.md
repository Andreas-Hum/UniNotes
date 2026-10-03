---
tags: [ml, supervised, classification]
status: not-started
notebook: not-started
level:
reviewed:
---
# Logistic Regression

> [!summary] In one sentence
> Logistic regression computes a linear score $w^\top x+b$ and squashes it through the S-shaped sigmoid to get a probability, then learns $w$ by making the observed labels as likely as possible (minimising cross-entropy).

## Intuition first

Suppose you want to predict whether a student passes an exam from the hours they studied. A straight line is a bad fit for a yes/no answer: it happily predicts "probability 1.4" for someone who studied 40 hours, and a single extreme student can tilt the whole line. What we really want is a curve that stays between 0 and 1, sits near 0 for few hours, near 1 for many hours, and switches smoothly somewhere in the middle.

That is exactly the **sigmoid** $\sigma(z) = 1/(1+e^{-z})$. Logistic regression keeps the familiar linear score $z = w^\top x + b$ (think of it as "evidence for class 1") and turns evidence into probability with the sigmoid:
- $z = 0$ → probability $0.5$ (undecided),
- large positive $z$ → probability near 1,
- large negative $z$ → probability near 0.

An everyday analogy: a dimmer switch rather than a light switch. The linear score turns the knob; the sigmoid maps knob position to brightness, never below "off" or above "fully on". The weight $w$ controls how *fast* the light comes on (steepness), and $b$ shifts *where* it comes on.

**What problem does it solve?** Binary (and, via softmax, multiclass) classification with **probabilities** you can trust and **coefficients** you can interpret. It is the default baseline for tabular classification and the building block of neural networks.

![Gradient descent bending a flat sigmoid into an S-curve that fits 0/1 labels](../../Attachments/ML%20Animations/Logistic%20Regression%20-%20fitting%20the%20sigmoid.gif)
*Watch the curve start flat at 0.5, steepen and slide as the log-loss $L$ falls; the dashed line where $\hat p=0.5$ ($wx+b=0$) is the decision boundary.*

## The math, step by step

### The model
$$p(y=1\mid x)=\sigma(w^\top x+b)=\frac1{1+e^{-(w^\top x+b)}}$$

Decision boundary $w^\top x+b=0$ is a hyperplane.

- $x\in\mathbb R^D$ input, $w\in\mathbb R^D$ weights, $b$ bias, $\hat p = p(y=1\mid x)$ the predicted probability.
- Inverting the sigmoid shows what the linear part really models: $\log\frac{\hat p}{1-\hat p} = w^\top x + b$. The **log-odds** (the *logit*) is linear in $x$.
- Predict class 1 when $\hat p \ge 0.5$, i.e. when $w^\top x + b \ge 0$. So the boundary is a line in 2D, a plane in 3D, a hyperplane in general. $w$ is perpendicular to it, and the signed distance of $x$ from it is $(w^\top x+b)/\|w\|$.

**Useful sigmoid identities** (used constantly in derivations):
- $\sigma(-z) = 1 - \sigma(z)$ (symmetry),
- $\sigma'(z) = \sigma(z)\,(1-\sigma(z))$ (derivative expressed through itself),
- $\sigma^{-1}(p) = \log\frac{p}{1-p}$ (logit).

### Loss
Negative log-likelihood (binary cross-entropy):
$$L=-\sum_i y_i\log\hat p_i+(1-y_i)\log(1-\hat p_i)$$
Convex; gradient $\nabla_w=X^\top(\hat p-y)$. No closed form → [[Gradient Descent]] or IRLS (Newton).

Where the loss comes from: treat each label as a coin flip with head-probability $\hat p_i$. The likelihood of all labels is $\prod_i \hat p_i^{\,y_i}(1-\hat p_i)^{1-y_i}$; take $-\log$ and you get $L$. In words: **for a positive example the loss is $-\log\hat p$, for a negative one $-\log(1-\hat p)$**. Confidently wrong predictions are punished without limit ($-\log 0 = \infty$), confidently right ones cost almost nothing. This connects to cross-entropy and KL divergence in [[Information Theory]].

**Deriving the gradient** (for one sample, $z = w^\top x + b$):
1. $\frac{\partial L}{\partial \hat p} = -\frac{y}{\hat p} + \frac{1-y}{1-\hat p}$.
2. $\frac{\partial \hat p}{\partial z} = \hat p(1-\hat p)$ (sigmoid identity).
3. Multiply: $\frac{\partial L}{\partial z} = -y(1-\hat p) + (1-y)\hat p = \hat p - y$. Beautifully simple: *prediction minus truth*.
4. $\frac{\partial z}{\partial w} = x$, so $\nabla_w L = (\hat p - y)\,x$; summing over samples gives $\nabla_w=X^\top(\hat p-y)$ (and $\partial L/\partial b = \sum_i(\hat p_i - y_i)$).

This is the same form as the linear-regression gradient, with $\hat p$ in place of $\hat y$. But because $\hat p$ depends non-linearly on $w$, setting it to zero has **no closed-form solution**.

**Why it is convex.** The Hessian is $H = X^\top S X$ with $S = \operatorname{diag}(\hat p_i(1-\hat p_i))$. Every diagonal entry is positive, so $v^\top H v = \sum_i s_i (x_i^\top v)^2 \ge 0$: positive semidefinite, hence convex, hence any local minimum is global.

**IRLS = Newton's method.** Newton's update $w \leftarrow w - H^{-1}\nabla$ becomes $w \leftarrow w - (X^\top S X)^{-1}X^\top(\hat p - y)$. Rearranged, each step solves a *weighted least-squares* problem with weights $S$ that are recomputed every iteration: "iteratively reweighted least squares". It converges in a handful of iterations but each costs $O(D^3)$.

## Multiclass
**Softmax** $p_k=\frac{e^{z_k}}{\sum_j e^{z_j}}$ with cross-entropy; gradient $\hat p-y$.

- One weight vector per class: $z_k = w_k^\top x + b_k$. Softmax turns the $K$ scores into positive numbers that sum to one.
- With a one-hot target $y$, the loss is $-\log p_{\text{true class}}$, and $\partial L/\partial z = \hat p - y$: the same "prediction minus truth" pattern.
- With $K=2$, softmax reduces to the sigmoid of the score difference $z_1 - z_0$.
- In practice subtract $\max_k z_k$ before exponentiating to avoid overflow (it does not change the result).

## Worked example

**Forward pass.** $w = (2, -1)$, $b = -0.5$, $x = (1, 1)$.
- $z = 2 - 1 - 0.5 = 0.5$, so $\hat p = \sigma(0.5) = 1/(1+e^{-0.5}) \approx 0.622$. Predict class 1.
- If the true label is $y=1$: loss $= -\log 0.622 \approx 0.474$. If $y = 0$: loss $= -\log 0.378 \approx 0.973$.
- Gradient for $y=1$: $\hat p - y = -0.378$, so $\nabla_w = -0.378\cdot(1,1)$ and $\partial L/\partial b = -0.378$. A GD step *adds* a multiple of $x$ to $w$, pushing $z$ (and $\hat p$) up for this point.

**Reading a coefficient.** If $w_j = 0.7$, increasing feature $j$ by one unit adds $0.7$ to the log-odds, i.e. multiplies the odds $\frac{p}{1-p}$ by $e^{0.7} \approx 2.0$. It does *not* add a fixed amount to the probability: near $p=0.5$ the effect on $p$ is large, near 0 or 1 it is small.

**Softmax by hand.** Scores $z = (2, 1, 0)$: $e^z \approx (7.39, 2.72, 1.00)$, sum $11.11$, so $\hat p \approx (0.665, 0.245, 0.090)$. If the true class is the second, $y = (0,1,0)$, the loss is $-\log 0.245 \approx 1.41$ and $\partial L/\partial z = \hat p - y \approx (0.665, -0.755, 0.090)$: raise the true class's score, lower the others.

## Notes
- Perfectly separable data ⇒ weights diverge; add L2 ([[Overfitting and Regularization]]).
- Coefficients = log-odds change per unit feature.
- Calibrated probabilities out of the box (unlike [[Support Vector Machines]]).
- It is a single-neuron [[Neural Networks|neural network]].

The *why* behind each:
- **Divergence on separable data.** If a hyperplane separates the classes perfectly, multiplying $w$ and $b$ by 2 keeps the same boundary but makes every $\hat p$ closer to 0 or 1, which strictly lowers the loss. So the optimum is at $\|w\|\to\infty$ and the sigmoid becomes a step function. An L2 penalty $\lambda\|w\|^2$ makes huge weights costly and gives a finite, unique solution.
- **Why not plain linear regression on 0/1 labels?** Its outputs are not probabilities (they leave $[0,1]$), and far-away but correctly classified points still produce big squared errors that drag the boundary towards them.
- **Calibration.** Because the model is trained to maximise likelihood, its probabilities tend to match observed frequencies (of the cases given $\hat p = 0.8$, about 80% are positive), as long as the model is not badly misspecified or heavily regularised. SVM scores are margins, not probabilities.
- **Discriminative vs generative.** Logistic regression models $p(y\mid x)$ directly. Generative models such as [[Naive Bayes]] or LDA model $p(x\mid y)p(y)$ and derive $p(y\mid x)$ with Bayes' rule. LDA with shared covariance yields the *same functional form* (a sigmoid of a linear score) but fits it differently; logistic regression makes fewer assumptions and usually wins with enough data.
- **Single neuron.** A neuron computes $\sigma(w^\top x + b)$: logistic regression is a one-layer network with sigmoid activation and cross-entropy loss. Stacking such units with hidden layers is what lets neural networks draw non-linear boundaries.

See also [[Linear Models for Classification]], [[Information Theory]].

## Common confusions
- *"It's called regression, so it predicts numbers."* → It regresses the **log-odds**, but it is used as a **classifier**.
- *"A coefficient of 0.7 means +0.7 probability."* → It means +0.7 in log-odds, i.e. odds × $e^{0.7}$.
- *"The boundary must be curved because the sigmoid is curved."* → The boundary is where $w^\top x+b=0$, a hyperplane. The sigmoid only shapes how probability changes *across* it. Curved boundaries need non-linear features.
- *"Training loss going to zero is good."* → On separable data it means the weights are running off to infinity; regularise.
- *"Threshold must be 0.5."* → 0.5 minimises error rate with equal costs; with unequal costs or imbalanced classes move the threshold.

## Check yourself

> [!question]- Derive $\partial L/\partial z$ for one sample of binary cross-entropy.
> $\partial L/\partial \hat p = -y/\hat p + (1-y)/(1-\hat p)$ and $\partial\hat p/\partial z = \hat p(1-\hat p)$; the product simplifies to $\hat p - y$.

> [!question]- Why is the logistic loss convex in $w$?
> Its Hessian $X^\top S X$ with $S=\operatorname{diag}(\hat p_i(1-\hat p_i))$, all entries $\ge 0$, is positive semidefinite.

> [!question]- What happens to $w$ when gradient descent runs on linearly separable data without regularisation?
> $\|w\|$ grows without bound: scaling $w$ up keeps the boundary but lowers the loss, so the sigmoid sharpens into a step. Add L2 regularisation or stop early.

> [!question]- Weight vector $w=(3,4)$, $b=-5$. How far is the boundary from the origin, and in which direction does $w$ point?
> The boundary $3x_1+4x_2=5$ is at distance $|b|/\|w\| = 5/5 = 1$ from the origin; $w$ is perpendicular to it and points towards the class-1 side.

> [!question]- With softmax scores $z=(1,1,1)$, what are the probabilities?
> All equal: $1/3$ each. Softmax depends only on differences between scores.

## Practice
[Logistic Regression - Exercises](Logistic%20Regression%20-%20Exercises.ipynb): why not linear regression on 0/1, diverging weights, sigmoid identities, BCE and its gradient, Hessian and convexity, softmax, a stable log-loss, GD and Newton/IRLS from scratch, softmax regression on Iris, and a calibration check.

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 4
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 4
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
- [Stanford CS229 lecture notes](https://cs229.stanford.edu/main_notes.pdf): logistic regression, Newton's method and softmax (generalised linear models)
