---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Optimizers]]

With a constant gradient, by what factor does momentum with $\beta=0.99$ amplify the step?::$1/(1-\beta)=100$.

For $f(w)=\tfrac12(w_1^2+25w_2^2)$, what is the largest stable learning rate for plain GD, and what is $\kappa$?::$\eta<2/\lambda_{\max}=2/25=0.08$; $\kappa=25/1=25$.

Why does AdaGrad stall in long training runs, and how does RMSProp fix it?::$G_t$ is a sum of squared gradients that only grows, so the step $\eta/\sqrt{G_t}$ goes to zero; RMSProp uses a moving average, which forgets old gradients and stays at the current gradient scale.

What does $\hat v_t$ correct for in Adam?::The bias towards zero from initialising $v_0=0$: early EMA values equal $(1-\beta_2^t)$ times the true average, so dividing by $1-\beta_2^t$ un-biases them.

In the warm-up + cosine schedule above, what is $\eta$ at the very end ($t=T$)?::$\cos\pi=-1$, so $\eta_T=\eta_{\max}\cdot\tfrac12(1-1)=0$.
