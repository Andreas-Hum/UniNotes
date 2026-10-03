---
tags: [ml, project, monte-carlo, games]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Blackjack Monte Carlo Control

> [!summary] In one sentence
> Learn blackjack from wins and losses alone with first-visit Monte Carlo control and an ε-greedy policy, and compare the learned strategy with basic strategy.

**Notebook:** [Project - Blackjack Monte Carlo Control](Project%20-%20Blackjack%20Monte%20Carlo%20Control.ipynb) · topic: [[RL Basics and MDPs]] · all projects: [[Projects Overview]]

## What you build
1. `eps_greedy`: explore or exploit.
2. `mc_update`: running average of the final reward for first visits.

## Reference results (solution, laptop CPU)
300,000 training hands, evaluated on 50,000:

| policy | expected reward per hand |
|---|---|
| random | −0.456 |
| hit below 17 (like the dealer) | −0.073 |
| **learned (MC control)** | **−0.047** |

Even the best policy loses: that's the house edge.

## Check yourself
> [!question]- Why Monte Carlo instead of TD here?
> Episodes are very short (a few decisions) and only the final reward matters, so full returns have low variance and need no bootstrapping.

> [!question]- Why does the learned policy stick on 13 against a dealer 6?
> The dealer must hit until 17 and busts often when showing 2–6, so risking your own bust is worse than waiting.

---
Back to [[00 - Machine Learning Index]].
