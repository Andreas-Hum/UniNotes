---
tags: [ml, rl]
---
# Q-Learning and Policy Gradients

## Value-based
- **TD(0)**: $V(s)\leftarrow V(s)+\alpha[r+\gamma V(s')-V(s)]$
- **SARSA** (on-policy): $Q(s,a)\leftarrow Q+\alpha[r+\gamma Q(s',a')-Q]$
- **Q-learning** (off-policy): $Q(s,a)\leftarrow Q+\alpha[r+\gamma\max_{a'}Q(s',a')-Q]$
- **DQN**: [[Neural Networks|neural net]] Q-function + replay buffer + target network. Extensions: Double, Dueling, Prioritized, Rainbow.

## Policy-based
REINFORCE: $\nabla_\theta J=\mathbb E[\nabla_\theta\log\pi_\theta(a\mid s)\,G_t]$; subtract a baseline to reduce variance.

## Actor–critic
Critic estimates $V$/$Q$, actor updates policy: A2C/A3C, **PPO** (clipped objective, workhorse), TRPO, SAC/TD3 (continuous control).

## Applications
Games (AlphaGo), robotics, RLHF for language models ([[Transformers]]).
Foundations: [[RL Basics and MDPs]].
