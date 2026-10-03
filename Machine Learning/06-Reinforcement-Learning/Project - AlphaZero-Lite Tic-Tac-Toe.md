---
tags: [ml, project, alphazero, mcts, games]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - AlphaZero-Lite Tic-Tac-Toe

> [!summary] In one sentence
> Build the AlphaZero loop on tic-tac-toe: a policy/value network guides Monte Carlo tree search, search results from self-play become the training targets, and the agent goes from losing half its games against perfect play to never losing.

**Notebook:** [Project - AlphaZero-Lite Tic-Tac-Toe](Project%20-%20AlphaZero-Lite%20Tic-Tac-Toe.ipynb) · topic: [[Q-Learning and Policy Gradients]] · all projects: [[Projects Overview]]

## What you build
1. `puct_select`: AlphaZero's exploration rule $Q+c\,P\sqrt{\sum N}/(1+N)$.
2. `az_loss`: policy cross-entropy against the search distribution + value MSE against the game result.

MCTS, self-play and the arena are given.

## Reference results (solution, laptop CPU)
| | win | draw | loss |
|---|---|---|---|
| untrained vs perfect player (20 games) | 0 | 10 | 10 |
| trained vs random player (40) | 36 | 4 | 0 |
| **trained vs perfect player (20)** | 0 | **20** | **0** |

12 iterations × 25 self-play games, ≈ 15 s on a CPU.

## Check yourself
> [!question]- Why train the policy on the MCTS visit counts instead of the moves actually played?
> Search is a policy-improvement operator: its visit distribution is better than the raw network. Training on it distils the search into the network, which then makes the next search better.

> [!question]- Why Dirichlet noise at the root?
> Without it, self-play keeps repeating the same games and never discovers moves the network currently dislikes.

## Learn more
- [Silver et al. – Mastering Chess and Shogi by Self-Play (AlphaZero)](https://arxiv.org/abs/1712.01815)
- More games: [[RL Arcade]] · [[Fun Projects]]

---
Back to [[00 - Machine Learning Index]].
