---
tags: [ml, project, bayesian, state-space]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Kalman Filter Tracker

> [!summary] In one sentence
> Track a cyclist through noisy GPS with a Kalman filter: Bayesian inference with Gaussians, one predict-and-update step per second, and it even estimates the speed you never measured.

**Notebook:** [Project - Kalman Filter Tracker](Project%20-%20Kalman%20Filter%20Tracker.ipynb) · topic: [[Bayesian Inference]] · all projects: [[Projects Overview]]

## What you build
1. `predict`: prior $x\leftarrow Fx$, $P\leftarrow FPF^\top+Q$.
2. `update`: gain $K=PH^\top(HPH^\top+R)^{-1}$, posterior mean and covariance.

## Reference results (solution, laptop CPU)
| | error |
|---|---|
| raw GPS (σ = 8 m) | 10.86 m |
| **Kalman filter** | **5.21 m** |
| speed (never measured) | 0.89 m/s |

## Check yourself
> [!question]- In 1-D, a prior N(0, 4) and a measurement 2 with variance 4 give what posterior, and why?
> N(1, 2): equal variances mean equal trust, so the mean is the average, and combining two independent pieces of evidence halves the variance (precisions add: 1/4 + 1/4 = 1/2).

> [!question]- What happens if R is set far too small?
> The filter trusts every GPS fix almost completely: K → 1, and the track becomes as jumpy as the raw GPS.

---
Back to [[00 - Machine Learning Index]].
