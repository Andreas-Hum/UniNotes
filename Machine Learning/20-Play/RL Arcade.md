---
tags: [ml, play, rl]
status: not-started
level:
reviewed:
---
# RL Arcade

> [!summary] In one sentence
> Build Snake and Flappy Bird from scratch as headless environments, teach an agent to play them, first with a Q-table and then with a DQN, and race the agents against a random baseline.

| Item | What you do | Time |
|---|---|---|
| [RL Snake - Q-Table to DQN](RL%20Snake%20-%20Q-Table%20to%20DQN.ipynb) | 4 exercises: state → table row, ε-greedy, the Q-learning update, DQN TD targets | ~1–2 min of compute |
| [RL Flappy Bird - Q-Table to DQN](RL%20Flappy%20Bird%20-%20Q-Table%20to%20DQN.ipynb) | 3 exercises: design the state grid, choose the death penalty, write the DQN loss | ~3–5 min of compute |
| [RL Arcade.html](RL%20Arcade.html) | watch a Q-table learn both games live in the browser, see its Q-values, play yourself | instant, no install |

Both notebooks follow the same four milestones:
1. **Environment + random agent.** A gym-like `reset()` / `step(action) → state, reward, done` in plain NumPy, plus a random-agent baseline.
2. **Tabular Q-learning** on a compact state: 11 yes/no features for Snake, a 1836-box grid for Flappy Bird.
3. **DQN in PyTorch**: replay buffer, target network, linear ε-schedule, keep-the-best checkpoint.
4. **The race**: learning curves, greedy evaluation on 100 fixed-seed games, and an animation of the winner.

Each `# TODO` cell has a ✅/❌ check and a hidden solution. The notebooks run top to bottom before you solve anything (the agents just don't learn), and every check passes once the solutions are filled in. Needs `numpy`, `matplotlib` and `torch`.

## What you should find
Measured with the solution code (mean over 100 greedy test games):

| Game | Random | Q-table | DQN |
|---|---|---|---|
| Snake, 10×10 (food eaten; seeds 0–2) | 0.16 | 17.4–19.0 | 18.7–20.7 |
| Flappy Bird (pipes, capped at 50; seeds 0–1) | 0 | 29.5–34.1 | 36.3–50.0 |

- On Snake, the **Q-table ends up within a few points of the DQN** and trains in a fraction of the time: the 11-bit state is tiny. The plateau around 15–25 comes from the state, not the algorithm. The snake sees only the three cells around its head and curls into its own body.
- On Flappy Bird the Q-table explores with ε = 0 and a zero-initialised table, so **the death penalty decides everything**: −1 gives 2.7–5.5 pipes, −10 gives 26–34 (seeds 0–3). With 1 % random actions, even −1 works.
- In the arcade, a **myopic Snake (γ = 0) beat γ = 0.9** in our runs (test mean 20–22 vs 13–19). Try it and work out why.

> [!tip]
> Do the Snake notebook first: it introduces every piece. Flappy Bird reuses them and adds the hard parts (continuous state, exploration, reward design).

## Ideas to go further
Each notebook ends with extensions: a bigger board, a 5×5 local view for the DQN, Double DQN, reward shaping, a harder Flappy Bird, and a CNN-DQN on pixels. A natural next game is Connect Four with self-play or a minimax opponent.

Theory: [[RL Basics and MDPs]] · [[Q-Learning and Policy Gradients]]

Related: [[Playgrounds]] · [[Break the Model]] · [[Guess the Output]]
