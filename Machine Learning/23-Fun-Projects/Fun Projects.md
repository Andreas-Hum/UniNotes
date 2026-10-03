---
tags: [ml, project, play, fun]
status: not-started
level: E
reviewed:
---
# Fun Projects

> [!summary] In one sentence
> Five small, game-like AI projects for an evening each: a Connect Four opponent, a Danish road-trip optimiser, a rock–paper–scissors mind reader, a Sudoku solver and evolving art. Each is a notebook with TODOs, ✅ checks and hidden solutions.

| Project | The AI idea | Result with the reference solution |
|---|---|---|
| [Connect Four AI](Connect%20Four%20AI.ipynb) | minimax search + alpha–beta pruning | depth-3 search beats a random player 20/20; play it yourself with `play_human()` |
| [Danish Road Trip](Danish%20Road%20Trip.ipynb) | genetic algorithm (order crossover) for the travelling salesman | 30 towns: random 4,481 km → nearest neighbour 1,672 → GA 1,474 → NN + 2-opt 1,454 km |
| [Rock Paper Scissors Mind Reader](Rock%20Paper%20Scissors%20Mind%20Reader.ipynb) | n-gram (Markov) prediction of your next move | wins 93 % vs. a patterned bot, breaks even vs. true randomness; try `play_me()` |
| [Sudoku Solver](Sudoku%20Solver.ipynb) | constraint satisfaction: backtracking + MRV heuristic | hard puzzle: 482 search nodes with MRV vs. ~9.7 million left-to-right |
| [Evolving Art](Evolving%20Art.ipynb) | (1+1) evolution strategy / hill climbing | 50 translucent circles approximate a photo; loss more than halves in 4,000 steps |

## What each one teaches
- **Connect Four:** adversarial search, why move ordering makes pruning effective, and evaluation heuristics. It's the classical ancestor of AlphaZero (search + learned evaluation). See [[RL Basics and MDPs]].
- **Danish Road Trip:** optimisation without gradients: populations, selection, crossover that respects constraints (permutations), and why a good local search (2-opt) is hard to beat. See [[Calculus and Optimization]].
- **Mind Reader:** humans aren't random, and an n-gram model is a tiny language model over three "words". Measure your own entropy with [[Information Theory]].
- **Sudoku:** search with good heuristics turns an impossible search into a trivial one: MRV is "fail first". See [[Probabilistic Graphical Models]] for constraints as factors.
- **Evolving Art:** what you can and can't do without a gradient. Compare with [[Gradient Descent]] in the stretch goal (differentiable rendering).

## Check yourself
> [!question]- Why does alpha–beta return exactly the same move as plain minimax?
> It only skips branches that provably can't change the minimax value at the root (a branch where the opponent already has a better alternative elsewhere). Same answer, far fewer nodes, especially with good move ordering.

> [!question]- Why does the GA need order crossover instead of "first half of parent A + second half of parent B"?
> That would produce routes that visit some towns twice and others never. OX keeps a slice of one parent and fills in the rest in the other parent's order, so every child is a valid permutation.

See also: [[Projects Overview]] · [[Personal Projects]] · [[Playgrounds]]

---
Back to [[00 - Machine Learning Index]].
