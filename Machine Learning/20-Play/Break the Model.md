---
tags: [ml, play, challenges]
status: not-started
level:
reviewed:
---
# Break the Model

> [!summary] In one sentence
> Seven challenges where you get a working model, deliberately make it fail, and then fix it – the fastest way to understand why good practices exist.

**Notebook:** [Break the Model - Challenges](Break%20the%20Model%20-%20Challenges.ipynb). Each challenge has a 💥 *Break it* task, a ✅ automatic check, a 🛠️ *Fix it* task and a hidden solution.

| # | Challenge | You break it by… | Lesson | Theory |
|---|---|---|---|---|
| 1 | The polynomial that memorised | raising the polynomial degree | overfitting; fix with ridge | [[Overfitting and Regularization]] |
| 2 | 90 % accuracy on pure noise | selecting features before cross-validation | leakage inside CV; use pipelines | [[Cross-Validation and Model Selection]] |
| 3 | The suspiciously perfect feature | adding a column known only after the outcome | target leakage | [[Common Pitfalls]] |
| 4 | The 99 % accurate fraud detector | predicting "no fraud" for everyone | accuracy on imbalanced data; use recall/PR-AUC | [[Model Evaluation and Metrics]] |
| 5 | Fool the digit classifier | an FGSM adversarial nudge | adversarial examples | [[Logistic Regression]] |
| 6 | It worked in the lab… | testing outside the training range | distribution shift, trees can't extrapolate | [[MLOps Overview]] |
| 7 | The scale that broke kNN | removing the scaler | feature scaling for distance methods | [[k-Nearest Neighbors]] |

> [!tip]
> Before opening a solution, write one sentence in your own words explaining *why* the model broke. If you can explain it, you own it.

Related: [[Playgrounds]] · [[Guess the Output]] · [[Weekly Challenges]] · [[Leaderboard]] · [[Common Pitfalls]]
