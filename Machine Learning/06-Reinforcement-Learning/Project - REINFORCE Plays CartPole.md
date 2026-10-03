---
tags: [ml, project, policy-gradients, games]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - REINFORCE Plays CartPole

> [!summary] In one sentence
> Train a small neural-network policy to balance CartPole with REINFORCE: play an episode, compute discounted returns, and push up the log-probability of actions in proportion to how well things went.

**Notebook:** [Project - REINFORCE Plays CartPole](Project%20-%20REINFORCE%20Plays%20CartPole.ipynb) · topic: [[Q-Learning and Policy Gradients]] · all projects: [[Projects Overview]]

## What you build
1. `discounted_returns`: backward pass + normalisation (a simple baseline).
2. `pg_loss`: $-\sum_t\log\pi_\theta(a_t|s_t)\,G_t$.

## Reference results (solution, laptop CPU)
Policy: 4 → 32 → 2 MLP, Adam lr 0.01. Reached a 20-episode average of **479 steps** (500 = perfect) after 301 episodes, about 15 s on a CPU.

## Check yourself
> [!question]- Why does normalising the returns help so much?
> Without a baseline every action in a long episode gets pushed up (all returns are positive), and the gradient is mostly noise. Subtracting the mean makes better-than-average actions go up and worse ones go down.

> [!question]- How is this related to RLHF?
> PPO, used in RLHF, is a policy-gradient method: the "episode" is a generated answer, the reward comes from a reward model, and clipping keeps updates small.

---
Back to [[00 - Machine Learning Index]].
