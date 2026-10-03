---
tags: [ml, project, mdp, dynamic-programming]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Gridworld Value Iteration

> [!summary] In one sentence
> Solve a slippery winter walk from campus to Jomfru Ane Gade (with a −10 harbour) exactly with value iteration, verify it by solving the Bellman expectation equation as a linear system, and see how slip and discount change the policy.

**Notebook:** [Project - Gridworld Value Iteration](Project%20-%20Gridworld%20Value%20Iteration.ipynb) · topic: [[RL Basics and MDPs]] · all projects: [[Projects Overview]]

## What you build
1. `value_iteration`: Bellman optimality backups until convergence.
2. `evaluate_policy`: $V^\pi=(I-\gamma P_\pi)^{-1}R_\pi$.

## Reference results (solution, laptop CPU)
Evaluating the greedy policy reproduces V* (Bellman consistent). With slip 0 the best path hugs the harbour; with slip 0.4 the agent goes the long way round; with γ = 0.5 states far from the goal are worth almost nothing.

## Check yourself
> [!question]- Why does value iteration converge?
> The Bellman optimality operator is a γ-contraction in the max norm, so the error shrinks by at least a factor γ per sweep.

> [!question]- Value iteration needs P and R. What do you do without them?
> Learn from sampled transitions: Q-learning or SARSA ([[Q-Learning and Policy Gradients]]).

---
Back to [[00 - Machine Learning Index]].
