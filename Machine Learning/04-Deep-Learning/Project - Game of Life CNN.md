---
tags: [ml, project, cnn]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Game of Life CNN

> [!summary] In one sentence
> Implement Conway's Game of Life, hand-set the weights of a 2-layer CNN so it computes Life exactly, then see whether gradient descent can find such weights on its own.

**Notebook:** [Project - Game of Life CNN](Project%20-%20Game%20of%20Life%20CNN.ipynb) · topic: [[CNN]] · all projects: [[Projects Overview]]

## What you build
1. `life_step`: the rules with `np.roll` (torus).
2. `hand_wire`: kernel computes s = 2·neighbours + self; four ReLUs build a bump that is 1 exactly when 5 ≤ s ≤ 7.
3. Experiment: train the same net from random weights with 4 vs 32 channels.

## Reference results (solution, laptop CPU)
| | result |
|---|---|
| hand-wired 4-channel CNN | exact on 500 random boards |
| trained, 4 channels (3 seeds) | perfect in 2/3 runs (one stuck at 71.5 % cell accuracy) |
| trained, 32 channels (3 seeds) | perfect in 3/3 runs |

## Check yourself
> [!question]- Why does a 4-channel solution exist, yet training sometimes fails?
> Existence is about expressivity; training is about the loss landscape. With minimal width there are few good basins and many bad local minima. Extra channels give more random starting points for a good unit (the lottery-ticket hypothesis).

## Learn more
- [Springer & Kenyon – It's Hard for Neural Networks To Learn the Game of Life](https://arxiv.org/abs/2009.01398)

---
Back to [[00 - Machine Learning Index]].
