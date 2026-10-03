---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Backpropagation]]

For $u=xy+z$ and $f=u^2$, what is $\partial f/\partial z$ in terms of $u$?::$\partial f/\partial u = 2u$ and $\partial u/\partial z = 1$ (add node copies), so $\partial f/\partial z = 2u$.

Why does the backward pass of a multiply node need the forward values?::Its local derivative with respect to one input is the *other* input, so both inputs must be cached from the forward pass.

A layer has $W\in\mathbb R^{100\times 50}$ (row convention, batch $N=32$). What shape is $\partial L/\partial W$, and how is it computed?::$100\times 50$, the same as $W$; it is $H^\top\Delta$ with $H\in\mathbb R^{32\times100}$ and $\Delta\in\mathbb R^{32\times 50}$.

A 5-layer chain of sigmoids with all pre-activations at 0 and weight 1: by how much is the gradient scaled?::Each layer contributes $w\,\sigma'(0)=0.25$, so $0.25^{5}\approx 10^{-3}$. Every extra layer divides it by 4 again.

What is $\delta^{(L)}$ for softmax + cross-entropy with $\hat p=(0.2,0.7,0.1)$ and true class 1 (the second)?::$\hat p - y = (0.2,\,-0.3,\,0.1)$.
