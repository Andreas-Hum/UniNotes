---
tags: [ml, project, naive-bayes, classification]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - SMS Spam Filter

> [!summary] In one sentence
> Write a Naive Bayes spam filter from scratch by counting words, match scikit-learn to four decimals, then pick a threshold that never blocks a real message.

**Notebook:** [Project - SMS Spam Filter](Project%20-%20SMS%20Spam%20Filter.ipynb) · topic: [[Naive Bayes]] · all projects: [[Projects Overview]]

## What you build
1. `fit_nb`: Laplace-smoothed word counts → log likelihoods, log priors.
2. `score`: log posterior = log prior + Σ log P(word | class).
3. `spammiest_words`: the largest log-likelihood ratios.

## Reference results (solution, laptop CPU)
| | value |
|---|---|
| test accuracy (yours = scikit-learn) | 0.9849 |
| spam precision / recall / F1 | 0.977 / 0.909 / 0.942 |
| spam caught with **zero** real messages blocked | 86 % |

Spammiest words: *claim, prize, 150p, tone, guaranteed, awarded…*

## Check yourself
> [!question]- Why sum log-probabilities instead of multiplying probabilities?
> A 30-word message multiplies 30 numbers below 0.01, which underflows to 0.0 in floating point. Logs turn the product into a stable sum, and argmax is unchanged.

> [!question]- What does Laplace smoothing protect against?
> A word seen only in ham (count 0 in spam) would give P(word|spam) = 0 and veto spam no matter what else the message says.

## Learn more
- [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)

---
Back to [[00 - Machine Learning Index]].
