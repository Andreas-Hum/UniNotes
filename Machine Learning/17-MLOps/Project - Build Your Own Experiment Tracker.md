---
tags: [ml, project, experiment-tracking, reproducibility]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Build Your Own Experiment Tracker

> [!summary] In one sentence
> Build a 20-line experiment tracker with JSON Lines (params, metrics, data fingerprint, git version), run a hyper-parameter sweep, pick the best run and prove it reproduces exactly.

**Notebook:** [Project - Build Your Own Experiment Tracker](Project%20-%20Build%20Your%20Own%20Experiment%20Tracker.ipynb) · topic: [[Experiment Tracking and Reproducibility]] · all projects: [[Projects Overview]]

## What you build
1. `log_run`: append one JSON record per run.
2. `best_run`: query the log for the best run by a metric.

## Reference results (solution, laptop CPU)
Sweep of an MLP on digits: best = 64 hidden units, α = 1e-4, test accuracy **0.9796**; re-running with the logged seed gives exactly 0.9796. Other seeds give 0.974–0.976, so differences below ~0.005 are noise.

## Check yourself
> [!question]- Why log a hash of the data and the git commit?
> Same code + same data + same seed ⇒ same result. If any of the three is missing, you can't tell which one changed when a result can't be reproduced.

> [!question]- Config B beats A by 0.002 with one seed each. Did B win?
> Not shown: the seed-to-seed spread is ≈ 0.005. Compare means over several seeds (or use a paired test).

---
Back to [[00 - Machine Learning Index]].
