---
tags: [ml, rl]
---
# RL Basics and MDPs

Agent interacts with environment: state $s_t$ → action $a_t$ → reward $r_{t+1}$, next state.

## MDP $(S,A,P,R,\gamma)$
Markov property: $P(s'\mid s,a)$ depends only on current state. Return $G_t=\sum_k\gamma^kr_{t+k+1}$.

- **Policy** $\pi(a\mid s)$; **value** $V^\pi(s)=\mathbb E_\pi[G_t\mid s]$; **Q** $Q^\pi(s,a)$.
- **Bellman expectation**: $V^\pi(s)=\sum_a\pi(a\mid s)\sum_{s'}P(s'\mid s,a)[R+\gamma V^\pi(s')]$
- **Bellman optimality**: $V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)[R+\gamma V^*(s')]$

## Known model (planning)
Value iteration, policy iteration (dynamic programming).

## Unknown model
Monte Carlo, TD learning → [[Q-Learning and Policy Gradients]].

## Concepts
Exploration vs exploitation (ε-greedy, UCB, Thompson sampling), on/off-policy, model-based vs model-free, discount factor.
