---
tags: [ml, project, bandits, exploration]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Study Method Bandits

> [!summary] In one sentence
> Pick tonight's study method like a bandit algorithm. Implement ε-greedy, UCB1 and Thompson sampling, and measure how many evenings each wastes on worse methods (regret).

**Notebook:** [Project - Study Method Bandits](Project%20-%20Study%20Method%20Bandits.ipynb) · topic: [[RL Basics and MDPs]] · all projects: [[Projects Overview]]

## What you build
1. `eps_greedy`: explore with probability ε.
2. `ucb1`: optimism, $\hat\mu_a+\sqrt{2\ln t/n_a}$.
3. `thompson`: sample from Beta posteriors and pick the best sample.

## Reference results (solution, laptop CPU)
| policy (1,000 evenings, 30 runs) | cumulative regret |
|---|---|
| random | 136.5 |
| UCB1 | 74.1 |
| ε-greedy (0.1) | 44.4 |
| **Thompson sampling** | **35.3** |

Thompson spent 864 of 1,000 evenings on the truly best method.

## Check yourself
> [!question]- Why does UCB1 lose to ε-greedy here, even though it has better theory?
> UCB1's bonus is a worst-case bound, so it keeps re-testing arms that are close to the best (0.55 vs 0.62). Its regret grows like log t, so it wins over long horizons, not over 1,000 steps.

> [!question]- How is a bandit an RL problem?
> It's an MDP with one state: every action gives a reward and returns to the same state. Exploration vs. exploitation without the credit-assignment problem.

---
Back to [[00 - Machine Learning Index]].
