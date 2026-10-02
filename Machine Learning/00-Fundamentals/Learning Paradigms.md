---
tags: [ml, fundamentals]
---
# Learning Paradigms

> [!summary] In one sentence
> A learning paradigm is defined by **what kind of feedback the data gives you** (labels, no labels, labels you manufacture yourself, or rewards), and that feedback decides which goals and algorithms are possible.

## Intuition first

Picture learning to sort fruit.

- A teacher hands you fruit **with name tags** and you learn to name new fruit: **supervised** learning.
- You get a crate of **untagged** fruit and notice that they fall into a few natural piles by colour and shape: **unsupervised** learning. Nobody tells you the pile names.
- Only a handful of fruit have tags but the crate is huge, so you use the piles to spread the few tags: **semi-supervised**.
- You cover half of each fruit with your hand and practise guessing the hidden half. No teacher needed, but you learn what fruit look like: **self-supervised**. Those skills transfer later when someone asks you to name fruit.
- You run a fruit stand and only learn from **profit at the end of the day**, not from correct answers: **reinforcement** learning.
- Fruit arrive one by one on a conveyor belt and you must update your judgement after each: **online** learning.
- You already know apples and pears well and learn quince from five examples: **transfer / fine-tuning**.

The key question to ask of any problem is: **what signal do I have, and when do I get it?**

![Supervised vs unsupervised on the same points](../../Attachments/ML%20Animations/Learning%20Paradigms%20-%20supervised%20vs%20unsupervised.gif)
*Same points, different feedback: on the left the colours (labels) are given and we learn a boundary; on the right we only see grey points and k-means discovers the groups itself.*

## The paradigms

| Paradigm | Data | Goal | Examples |
|---|---|---|---|
| **Supervised** | $(x, y)$ pairs | predict $y$ from $x$ | [[Linear Regression]], [[Decision Trees]], [[Neural Networks]] |
| **Unsupervised** | $x$ only | find structure | [[Clustering]], [[PCA]] |
| **Semi-supervised** | few labels + many unlabeled | use both | label propagation, pseudo-labeling |
| **Self-supervised** | labels derived from data | learn representations | masked language modeling, contrastive learning |
| **Reinforcement** | reward signal from environment | maximize return | [[Q-Learning and Policy Gradients]] |
| **Online** | stream of examples | update incrementally | perceptron, bandits |
| **Transfer / fine-tuning** | pretrained model + small data | adapt | BERT, ResNet fine-tuning |

**Why each exists.**
- **Supervised** is the most direct but labels are expensive (doctors, annotators).
- **Unsupervised** works without labels but the "structure" found may not match the categories you care about.
- **Semi-supervised** exploits the *cluster assumption*: points close together (in a dense region) probably share a label. Label propagation spreads labels along a similarity graph; pseudo-labelling trains on the model's own confident predictions.
- **Self-supervised is not unsupervised in disguise**: it *is* supervised training, but on a **pretext task** whose labels are generated from the data itself (predict a masked word, predict whether two crops come from the same image, predict a rotation). The goal is a good representation, used later downstream.
- **Reinforcement** feedback is a scalar reward that may arrive late, so the learner must solve *credit assignment* and balance *exploration vs. exploitation*.
- **Online** learning updates after every example: cheap memory, adapts to drift.
- **Transfer** helps when the source and target tasks share low-level structure (edges, word meaning) and target data are scarce. It can hurt (negative transfer) when the domains differ too much.

## The math, step by step

**Supervised objective.** Learn $f_\theta$ such that $f_\theta(x) \approx y$ by minimising $\frac1N\sum_i \ell(f_\theta(x_i), y_i)$ (see [[What is Machine Learning]]).

**Reinforcement: the return.** An agent receives rewards $r_0, r_1, r_2, \dots$. The *discounted return* is
$$G = \sum_{t=0}^{\infty} \gamma^t r_t, \qquad 0 \le \gamma < 1.$$
$\gamma$ (the discount factor) makes near rewards count more than distant ones and keeps the sum finite. The goal is a policy that maximises the expected $G$.

**Online learning: the perceptron.** For labels $y \in \{-1, +1\}$, on each new example predict $\hat y = \operatorname{sign}(w^\top x)$; if wrong ($y\, w^\top x \le 0$), update
$$w \leftarrow w + \eta\, y\, x.$$
In words: nudge $w$ towards $x$ if $x$ was a missed positive, away from it if it was a false positive.

**Online learning: incremental mean (bandits).** The running average of the rewards from an arm after $n$ pulls can be updated without storing the history:
$$Q_n = Q_{n-1} + \frac{1}{n}\big(r_n - Q_{n-1}\big).$$
New estimate = old estimate + step size × (surprise). The ε-greedy bandit picks the arm with highest $Q$ with probability $1-\varepsilon$ and a random arm with probability $\varepsilon$.

## Discriminative vs. generative
- **Discriminative** models learn $p(y\mid x)$ directly ([[Logistic Regression]], [[Support Vector Machines]]).
- **Generative** models learn $p(x, y) = p(x\mid y)p(y)$ ([[Naive Bayes]], [[Gaussian Mixture Models and EM]], [[Generative Models]]).

A generative model classifies through **Bayes' rule**:
$$p(y \mid x) = \frac{p(x\mid y)\,p(y)}{\sum_{y'} p(x\mid y')\,p(y')}.$$
Because it models how $x$ itself is produced, it can also **sample new data** (draw $y \sim p(y)$, then $x \sim p(x\mid y)$) and handle missing features. The price: it must model $p(x\mid y)$, which is hard in high dimensions, and it pays for every wrong assumption about it. Discriminative models spend all their capacity on the decision boundary and usually win on classification accuracy when data are plentiful.

## Parametric vs. non-parametric
Parametric: fixed number of parameters (linear models). Non-parametric: complexity grows with data ([[k-Nearest Neighbors]], [[Gaussian Processes]], kernel methods).

**Why it matters.** A parametric model compresses the data into a fixed-size summary: fast at prediction time, but limited by its assumptions. A non-parametric model keeps (a function of) the training data: very flexible, but memory and prediction cost grow with $N$. k-NN regression, for example, predicts $\hat f(x) = \frac1k\sum_{x_j \in N_k(x)} y_j$, the average of the $k$ nearest training targets, so it must store all of them.

**Counting parameters.** Linear regression in $d$ dimensions: $d + 1$ (weights + bias). Gaussian naive Bayes with $K$ classes and $d$ features: $Kd$ means $+\ Kd$ variances $+\ (K-1)$ free class priors.

## Worked example

**Generative classifier with Bayes' rule.** 30 % of emails are spam. The word "free" appears in 60 % of spam and 5 % of ham. An email contains "free"; is it spam?
$$p(\text{spam}\mid\text{free}) = \frac{0.6 \times 0.3}{0.6\times 0.3 + 0.05 \times 0.7} = \frac{0.18}{0.18 + 0.035} \approx 0.837.$$

**Discounted return.** Rewards $1, 0, 2$ then nothing, $\gamma = 0.9$: $G = 1 + 0.9\cdot 0 + 0.81 \cdot 2 = 2.62$.

**Perceptron step.** $w = (0, 0)$, $\eta = 1$, example $x = (1, 2)$, $y = +1$. $w^\top x = 0 \le 0$, so it is a mistake: $w \leftarrow (0,0) + (1, 2) = (1, 2)$. Now $w^\top x = 5 > 0$, correct.

**Incremental mean.** Rewards so far $2, 4$, so $Q_2 = 3$. New reward $r_3 = 6$: $Q_3 = 3 + \frac13(6 - 3) = 4$, exactly the mean of $\{2, 4, 6\}$, computed without storing the history.

## Common confusions
- **"Self-supervised = unsupervised."** Self-supervised learning uses a supervised loss on automatically created labels; unsupervised methods like clustering have no target at all.
- **"Generative means it generates images."** In this context it means it models $p(x, y)$ (or $p(x)$). Naive Bayes is generative, even though nobody uses it to make pictures.
- **"Non-parametric means no parameters."** It means the *number* of parameters is not fixed in advance; it grows with the data. k-NN still has the hyperparameter $k$.
- **"Reinforcement learning is supervised learning with rewards as labels."** Rewards evaluate actions, they do not tell you the correct action, and they may be delayed; your own actions also change what data you see.
- **"Transfer learning always helps."** Only if source and target share structure.

## Check yourself

> [!question]- You have 1 million product photos, 2 000 labelled with the product category. Which paradigms fit?
> Semi-supervised (use the unlabelled photos via pseudo-labelling or label propagation), or self-supervised pretraining on all photos followed by fine-tuning on the 2 000 labelled ones (transfer).

> [!question]- Is k-means parametric or non-parametric?
> Parametric in the sense that it has a fixed number of parameters ($k$ centroids × $d$ coordinates), independent of $N$. k-NN, in contrast, is non-parametric.

> [!question]- Logistic regression or naive Bayes: which is generative and what can it do that the other cannot?
> Naive Bayes is generative: it can sample synthetic $x$ for a given class and naturally handle missing features. Logistic regression models only $p(y\mid x)$.

> [!question]- Why do we need a discount factor $\gamma < 1$ in an infinite-horizon task?
> To keep the sum of rewards finite and to express a preference for sooner rewards.

## Practice
[Learning Paradigms - Exercises](Learning%20Paradigms%20-%20Exercises.ipynb)

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/)
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [Sutton & Barto – Reinforcement Learning: An Introduction (free)](http://incompleteideas.net/book/the-book-2nd.html)
