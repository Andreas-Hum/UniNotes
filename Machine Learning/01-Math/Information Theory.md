---
tags: [ml, math, information-theory]
status: not-started
notebook: not-started
level:
reviewed:
---
# Information Theory

> [!summary] In one sentence
> Information theory measures uncertainty and surprise in bits: entropy is how unpredictable a distribution is, cross-entropy is how surprised a model is by the real data (the standard classification loss), and KL divergence is the gap between the two, i.e. how wrong the model's beliefs are.

## Intuition first

**Surprise.** If an event has probability $p$, seeing it carries $-\log_2p$ bits of "surprise". A fair coin landing heads: 1 bit. A 1-in-1024 event: 10 bits. Something certain: 0 bits; you learned nothing.

**Entropy** is the *average* surprise of a distribution: how hard its outcomes are to predict. A fair coin (1 bit) is maximally unpredictable; a coin that lands heads 90% of the time is fairly predictable (0.47 bits). It is also the minimum average number of yes/no questions (bits) needed to encode outcomes with the best possible code.

**Cross-entropy** is the average surprise when outcomes come from the real distribution $p$ but you *expect* them according to your model $q$. If your model is wrong you are surprised more often than necessary, so $H(p,q)\ge H(p)$. The excess, the extra bits you pay for using the wrong model, is the **KL divergence**.

Analogy: entropy is the length of the best possible Morse code for English. Cross-entropy is the length you get if you designed the code for French and use it on English. KL is the waste.

**What problem does it solve?** It gives ML its most-used loss (cross-entropy), the impurity measure for [[Decision Trees]], a way to compare distributions (KL, used in VAEs, variational inference, distillation, RLHF), and a test for any kind of dependence between variables (mutual information).

![As the model distribution q moves toward the data distribution p, cross-entropy falls to the entropy](../../Attachments/ML%20Animations/Information%20Theory%20-%20cross-entropy%20equals%20entropy%20plus%20KL.gif)
*Watch the bar on the right: its green part, $H(p)=1.75$ bits, never changes because it depends only on the data; training shrinks the red part, $D_{KL}(p\Vert q)$, from 0.87 bits to 0 as the blue model bars match the yellow data outlines.*

## The math, step by step

Logs base 2 give **bits**, natural logs give **nats** (what libraries use); they differ by a factor $\ln2$. Convention: $0\log0=0$.

- **Entropy** $H(p)=-\sum p\log p$ — uncertainty. Used for split criteria in [[Decision Trees]].
  - Read it as $\mathbb E_{x\sim p}[-\log p(x)]$: the expected surprise.
  - $0\le H(p)\le\log K$ for $K$ outcomes; 0 for a certain outcome, $\log K$ for the uniform distribution.
  - Binary entropy: $H(\theta)=-\theta\log\theta-(1-\theta)\log(1-\theta)$, peaking at 1 bit for $\theta=\frac12$.
- **Cross-entropy** $H(p,q)=-\sum p\log q$ — the classification loss in [[Logistic Regression]] and [[Neural Networks]].
  - With a one-hot label ($p$ puts all mass on the true class $y$), it collapses to $-\log q_y$: minus the log-probability the model gave the correct class. Confident and right: near 0. Confident and wrong: huge.
  - Computed stably from logits $z$: $-\log\mathrm{softmax}(z)_y=-z_y+\log\sum_k e^{z_k}$, with the log-sum-exp evaluated after subtracting $\max_kz_k$ (no overflow, no $\log0$).
- **KL divergence** $D_{KL}(p\Vert q)=\sum p\log\frac pq\ge0$, asymmetric.
  - $\ge0$ (Gibbs' inequality): $-D_{KL}=\sum p\log\frac qp\le\log\sum p\frac qp=\log1=0$ by Jensen's inequality ($\log$ is concave). Equality iff $p=q$.
  - **Asymmetric**: $D_{KL}(p\Vert q)\neq D_{KL}(q\Vert p)$ in general, so it is not a distance. $D_{KL}(p\Vert q)$ is infinite if $q=0$ somewhere $p>0$.
  - **Forward KL** $D_{KL}(p\Vert q)$ (fit $q$ to data $p$) is *mass-covering*: $q$ must put probability wherever $p$ does. **Reverse KL** $D_{KL}(q\Vert p)$ (used in [[Variational Inference]]) is *mode-seeking*: $q$ may ignore some modes of $p$ but must not put mass where $p$ has none.
  - Two Gaussians: $D_{KL}\big(\mathcal N(\mu_1,\sigma_1^2)\Vert\mathcal N(\mu_2,\sigma_2^2)\big)=\log\frac{\sigma_2}{\sigma_1}+\frac{\sigma_1^2+(\mu_1-\mu_2)^2}{2\sigma_2^2}-\frac12$.
  - When you can only sample from $p$: Monte Carlo estimate $D_{KL}\approx\frac1n\sum_i\log\frac{p(x_i)}{q(x_i)}$ with $x_i\sim p$.
- **The key identity**: $H(p,q)=H(p)+D_{KL}(p\Vert q)$ (expand $\log\frac pq=\log p-\log q$). Minimizing cross-entropy = minimizing KL to the data distribution, because $H(p)$ does not depend on the model. It is also the same as maximum likelihood ([[Probability for ML]]).
- **Mutual information** $I(X;Y)=H(X)-H(X\mid Y)$ — feature selection ([[Feature Engineering]]).
  - In words: how many bits knowing $Y$ saves you about $X$. Symmetric, $\ge0$, and 0 iff $X$ and $Y$ are independent.
  - Equivalent forms: $I(X;Y)=H(X)+H(Y)-H(X,Y)=D_{KL}\big(p(x,y)\Vert p(x)p(y)\big)$.
  - Unlike correlation it detects *any* dependence, including non-linear ones: for $Y=X^2$ with symmetric $X$ the correlation is 0 but the MI is large.
- **ELBO** in [[Variational Inference]] and VAEs ([[Generative Models]]) is built from KL: $\log p(x)=\underbrace{\mathbb E_{q(z)}[\log p(x\mid z)]-D_{KL}(q(z)\Vert p(z))}_{\text{ELBO}}+D_{KL}\big(q(z)\Vert p(z\mid x)\big)$. Since the last KL is $\ge0$, the ELBO is a lower bound on the log-evidence; maximizing it pushes $q$ toward the true posterior.
- **Jensen–Shannon** divergence: symmetric, used in original GAN analysis. $\mathrm{JS}(p,q)=\frac12D_{KL}(p\Vert m)+\frac12D_{KL}(q\Vert m)$ with $m=\frac12(p+q)$; it is always finite and bounded by $\log2$. The original GAN with an optimal discriminator minimizes $2\,\mathrm{JS}(p_{\text{data}},p_g)-\log4$.

### Information gain
Information gain $=H(\text{parent})-\sum\frac{n_k}{n}H(\text{child}_k)$.

It is the drop in entropy from splitting a node into children of sizes $n_k$, each child weighted by its share of the samples. A decision tree picks the split with the largest gain. It is exactly the mutual information between the split outcome and the label, estimated on that node.

## Worked example

**Entropy.** Biased coin, $P(\text{heads})=0.9$: $H=-(0.9\log_20.9+0.1\log_20.1)=0.9(0.152)+0.1(3.32)\approx0.47$ bits. Fair coin: 1 bit.

**Cross-entropy for one prediction.** The model gives the true class probability 0.7: loss $=-\ln0.7\approx0.36$ nats. If it gave 0.1: $-\ln0.1\approx2.30$. Being confidently wrong is punished hard.

**The animation's numbers.** $p=(\frac12,\frac14,\frac18,\frac18)$, $q=(0.1,0.2,0.3,0.4)$.
1. $H(p)=\frac12(1)+\frac14(2)+\frac18(3)+\frac18(3)=1.75$ bits.
2. $H(p,q)=-(\frac12\log_20.1+\frac14\log_20.2+\frac18\log_20.3+\frac18\log_20.4)\approx2.62$ bits.
3. $D_{KL}(p\Vert q)=2.62-1.75\approx0.87$ bits. The other direction, $D_{KL}(q\Vert p)\approx0.75$ bits: asymmetric.

**Information gain.** Parent: 5 positive, 5 negative ($H=1$ bit). Split into (4+, 1−) and (1+, 4−), each with $H(0.8)\approx0.722$. Gain $=1-(\frac5{10}0.722+\frac5{10}0.722)\approx0.28$ bits.

## Common confusions
- **"KL is a distance."** → It is not symmetric and does not satisfy the triangle inequality. Use JS (or its square root) if you need something symmetric.
- **"Cross-entropy and KL are different objectives."** → For a fixed data distribution they differ by the constant $H(p)$, so they have the same minimizer and the same gradients with respect to the model.
- **"Entropy of a continuous variable behaves like the discrete one."** → Differential entropy can be negative and depends on units; KL and mutual information remain well-behaved.
- **"Zero correlation means zero information."** → Mutual information catches non-linear dependence that correlation misses.
- **"$\log$ base does not matter."** → It only rescales (bits vs nats), but mixing them gives numbers off by $\ln2\approx0.69$.

## Check yourself

> [!question]- What is the maximum entropy of a distribution over 8 outcomes, and which distribution achieves it?
> $\log_28=3$ bits, achieved by the uniform distribution.

> [!question]- Why does minimizing cross-entropy over the model $q$ also minimize $D_{KL}(p\Vert q)$?
> $H(p,q)=H(p)+D_{KL}(p\Vert q)$ and $H(p)$ does not depend on $q$.

> [!question]- $p=(1,0)$, $q=(0.5,0.5)$. Compute $D_{KL}(p\Vert q)$ and $D_{KL}(q\Vert p)$.
> $D_{KL}(p\Vert q)=1\cdot\log_2\frac1{0.5}=1$ bit. $D_{KL}(q\Vert p)=\infty$, because $q$ puts mass on an outcome where $p$ is 0.

> [!question]- Why compute cross-entropy from logits instead of `-log(softmax(z))`?
> Softmax can underflow to exactly 0 (then $\log0=-\infty$) or overflow in $e^{z}$. Using $-z_y+\mathrm{logsumexp}(z)$ with the max subtracted is exact and stable.

> [!question]- $X$ and $Y$ are independent. What is $I(X;Y)$?
> 0: knowing $Y$ does not reduce uncertainty about $X$, and $p(x,y)=p(x)p(y)$ makes the KL form zero.

## Practice
[Information Theory - Exercises](Information%20Theory%20-%20Exercises.ipynb): entropy as uncertainty, forward vs reverse KL, the cross-entropy = entropy + KL identity, mutual information vs correlation, by-hand KL between Gaussians and Gibbs' inequality, then code: stable cross-entropy from logits, the best split by information gain, mutual information, Jensen–Shannon and Monte Carlo KL.

## Learn more
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [Deep Learning book – Goodfellow et al.](https://www.deeplearningbook.org/) ch. 3
- [Chris Olah – Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/): the clearest picture-based explanation of entropy, cross-entropy and KL.
