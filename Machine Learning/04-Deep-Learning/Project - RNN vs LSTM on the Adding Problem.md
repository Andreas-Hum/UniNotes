---
tags: [ml, project, rnn, lstm, memory]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - RNN vs LSTM on the Adding Problem

> [!summary] In one sentence
> Write an LSTM cell by hand (matching PyTorch exactly) and race a plain RNN against an LSTM on the adding problem: remember two marked numbers across 50 time steps.

**Notebook:** [Project - RNN vs LSTM on the Adding Problem](Project%20-%20RNN%20vs%20LSTM%20on%20the%20Adding%20Problem.ipynb) · topic: [[RNN and LSTM]] · all projects: [[Projects Overview]]

## What you build
1. `lstm_cell`: input/forget/candidate/output gates and the additive cell state.
2. `adding_problem`: the data generator.

## Reference results (solution, laptop CPU)
Validation MSE after 1,500 steps (baseline = 1/6 ≈ 0.167):

| | T = 10 | T = 50 |
|---|---|---|
| RNN | 0.0059 | **0.1608** (≈ baseline: learned nothing) |
| LSTM | 0.0003 | **0.0013** |

## Check yourself
> [!question]- Why does the plain RNN fail at T = 50 but not T = 10?
> Its gradient to early inputs is a product of ~T Jacobians with norm < 1, so it vanishes exponentially. The LSTM's cell state is updated additively (c' = f⊙c + i⊙g), so with f ≈ 1 the gradient flows back almost unchanged.

> [!question]- Why is the baseline MSE 1/6?
> Predicting the mean (1.0) of a sum of two independent U(0,1) variables gives MSE = its variance = 2·(1/12) = 1/6.

---
Back to [[00 - Machine Learning Index]].
