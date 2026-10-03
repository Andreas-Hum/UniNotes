---
tags: [ml, project, play, fun]
status: not-started
level: E
reviewed:
---
# Fun Projects

> [!summary] In one sentence
> Small, game-like AI projects for an evening each: a Connect Four opponent, a Danish road-trip optimiser, a rock–paper–scissors mind reader, a Sudoku solver, evolving art, an A* pathfinder, twenty questions, CartPole neuroevolution, a 1961 matchbox learner and a melody composer. Each is a notebook with TODOs, ✅ checks and hidden solutions.

| Project | The AI idea | Result with the reference solution |
|---|---|---|
| [Connect Four AI](Connect%20Four%20AI.ipynb) | minimax search + alpha–beta pruning | depth-3 search beats a random player 20/20; play it yourself with `play_human()` |
| [Danish Road Trip](Danish%20Road%20Trip.ipynb) | genetic algorithm (order crossover) for the travelling salesman | 30 towns: random 4,481 km → nearest neighbour 1,672 → GA 1,474 → NN + 2-opt 1,454 km |
| [Rock Paper Scissors Mind Reader](Rock%20Paper%20Scissors%20Mind%20Reader.ipynb) | n-gram (Markov) prediction of your next move | wins 93 % vs. a patterned bot, breaks even vs. true randomness; try `play_me()` |
| [Sudoku Solver](Sudoku%20Solver.ipynb) | constraint satisfaction: backtracking + MRV heuristic | hard puzzle: 482 search nodes with MRV vs. ~9.7 million left-to-right |
| [Evolving Art](Evolving%20Art.ipynb) | (1+1) evolution strategy / hill climbing | 50 translucent circles approximate a photo; loss more than halves in 4,000 steps |
| [A-Star Pathfinder](A-Star%20Pathfinder.ipynb) | A* search with an admissible heuristic | 60×60 maze: same 120-step path as BFS, 1,477 vs 2,551 squares expanded |
| [Twenty Questions - Danish Animals](Twenty%20Questions%20-%20Danish%20Animals.ipynb) | max-entropy questions = decision-tree splits | 24 animals guessed in 4.54 questions on average; seal/porpoise and pig/horse need a new question |
| [CartPole Neuroevolution](CartPole%20Neuroevolution.ipynb) | evolution strategy on a 4-weight linear policy | balances the full 500 steps, also from 10 unseen starts |
| [MENACE - Matchbox Tic-Tac-Toe](MENACE%20-%20Matchbox%20Tic-Tac-Toe.ipynb) | Michie's 1961 bead-counting reinforcement learner | loss rate vs. a random player 32 % → 19 % in 4,000 games |
| [Markov Melody Machine](Markov%20Melody%20Machine.ipynb) | order-k Markov chains, synthesised to WAV | order 2 composes new tunes; order 4 copies 72 % of 8-note stretches |
| 🎮 [Pixel Catch - DQN from Pixels](Pixel%20Catch%20-%20DQN%20from%20Pixels.ipynb) | Deep Q-Network with replay buffer + target network, input = raw pixels | catch rate 32 % (random) → 100 % after 400 episodes |
| 🎮 [Kuhn Poker - Learning to Bluff](Kuhn%20Poker%20-%20Learning%20to%20Bluff.ipynb) | counterfactual regret minimisation (self-play) | game value −0.0565 (theory −1/18); bluffs with the jack 22 %, bets the king 3× as often (66 %) |
| [Cipher Breaker](Cipher%20Breaker.ipynb) | bigram language model from your IT-ret notes + simulated annealing | a 234-character Danish GDPR sentence decoded 100 % correctly |
| [Battleship AI](Battleship%20AI.ipynb) | probability density over legal ship placements | 44.7 shots on average vs 96.1 for random shooting |
| [Mastermind Solver](Mastermind%20Solver.ipynb) | Knuth's 1977 minimax strategy | never more than 5 guesses; average 4.49 on 150 random codes |

## What each one teaches
- **Connect Four:** adversarial search, why move ordering makes pruning effective, and evaluation heuristics. It's the classical ancestor of AlphaZero (search + learned evaluation). See [[RL Basics and MDPs]].
- **Danish Road Trip:** optimisation without gradients: populations, selection, crossover that respects constraints (permutations), and why a good local search (2-opt) is hard to beat. See [[Calculus and Optimization]].
- **Mind Reader:** humans aren't random, and an n-gram model is a tiny language model over three "words". Measure your own entropy with [[Information Theory]].
- **Sudoku:** search with good heuristics turns an impossible search into a trivial one: MRV is "fail first". See [[Probabilistic Graphical Models]] for constraints as factors.
- **Evolving Art:** what you can and can't do without a gradient. Compare with [[Gradient Descent]] in the stretch goal (differentiable rendering).

- **A\*:** heuristic search; why an admissible heuristic keeps the path optimal.
- **Twenty questions:** entropy-maximising questions, the same rule a decision tree uses ([[Decision Trees]]).
- **CartPole:** control without gradients; a 4-number policy is enough.
- **MENACE:** reinforcement learning as bead counting, decades before deep RL ([[Q-Learning and Policy Gradients]]).
- **Melodies:** the n-gram order trade-off between nonsense and copying, by ear.

## Check yourself
> [!question]- Why does alpha–beta return exactly the same move as plain minimax?
> It only skips branches that provably can't change the minimax value at the root (a branch where the opponent already has a better alternative elsewhere). Same answer, far fewer nodes, especially with good move ordering.

> [!question]- Why does the GA need order crossover instead of "first half of parent A + second half of parent B"?
> That would produce routes that visit some towns twice and others never. OX keeps a slice of one parent and fills in the rest in the other parent's order, so every child is a valid permutation.

See also: [[Projects Overview]] · [[Personal Projects]] · [[Playgrounds]]

---
Back to [[00 - Machine Learning Index]].
