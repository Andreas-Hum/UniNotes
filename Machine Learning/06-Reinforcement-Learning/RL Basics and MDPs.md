---
tags: [ml, rl]
---
# RL Basics and MDPs

> [!summary] In one sentence
> Reinforcement learning is learning *what to do* by trial and error: an agent picks actions, the environment answers with rewards and new states, and a Markov decision process (MDP) is the maths that lets us define "the best long-run behaviour" and compute it.

## Intuition first

Supervised learning has a teacher who tells you the right answer for every input. Reinforcement learning (RL) has no teacher, only a **score**. Think of learning a new video game without reading the manual: you press buttons, sometimes points appear, sometimes you die, and slowly you work out which moves in which situations lead to high scores *eventually*.

The basic loop is always the same. The agent interacts with the environment: it observes a state $s_t$ → chooses an action $a_t$ → receives a reward $r_{t+1}$ and the next state $s_{t+1}$, and the loop repeats.

Three things make RL harder than supervised learning:

1. **Delayed consequences.** A chess move that looks bad now may win the game twenty moves later. The agent must assign credit for a reward to the decisions that caused it, possibly long ago.
2. **The agent creates its own data.** What it sees depends on what it does. If it never tries the unfamiliar door, it never learns what is behind it. This is the **exploration vs exploitation** dilemma.
3. **The world is random.** The same action can lead to different outcomes, so we reason about *expected* rewards.

An MDP is the clean, idealised model of this loop. Once a problem is written as an MDP we can define precisely what a "good policy" is and, if we know the rules of the world, compute it with dynamic programming. If we do not know the rules, we learn from experience instead (Monte Carlo, TD learning, Q-learning).

## The MDP $(S,A,P,R,\gamma)$

An MDP is a 5-tuple:

| Symbol | Name | Meaning |
|---|---|---|
| $S$ | states | all situations the agent can be in (grid cells, board positions, robot joint angles) |
| $A$ | actions | what the agent can do |
| $P(s'\mid s,a)$ | transition model | probability of landing in $s'$ after doing $a$ in $s$ |
| $R$ | reward function | the immediate reward, e.g. $R(s,a,s')$ |
| $\gamma\in[0,1]$ | discount factor | how much a reward one step later is worth compared with one now |

**Markov property:** $P(s'\mid s,a)$ depends only on the current state and action, not on the history of how you got there. "The present state contains everything relevant from the past." A chess position is Markov (the board says it all). A single frame of a video game where the ball's speed matters is *not* Markov, but stacking the last few frames makes it Markov again. The usual trick when a problem is not Markov: put more into the state.

## The math, step by step

### Return: what the agent wants to maximise

$$G_t=\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}=r_{t+1}+\gamma r_{t+2}+\gamma^2 r_{t+3}+\dots$$

In words: the return is the sum of all future rewards, where a reward $k$ steps in the future is shrunk by $\gamma^k$.

- $\gamma=0$: only the next reward matters (completely short-sighted).
- $\gamma$ close to 1: the far future matters almost as much as now (far-sighted).
- If every reward is a constant $c$, the geometric series gives $G_t=c/(1-\gamma)$. With $\gamma=0.9$ that is $10c$, so $1/(1-\gamma)$ is a rough "effective horizon".

The return also has a recursive form that everything below is built on:
$$G_t=r_{t+1}+\gamma G_{t+1}.$$

### Policy, value and Q

- **Policy** $\pi(a\mid s)$: the agent's behaviour, the probability of taking action $a$ in state $s$. A deterministic policy is the special case where one action has probability 1.
- **State value** $V^\pi(s)=\mathbb E_\pi[G_t\mid s_t=s]$: "how good is it to *be* in $s$ if I follow $\pi$ from now on?"
- **Action value** $Q^\pi(s,a)=\mathbb E_\pi[G_t\mid s_t=s,a_t=a]$: "how good is it to do $a$ in $s$ *and then* follow $\pi$?"

They are linked by $V^\pi(s)=\sum_a\pi(a\mid s)\,Q^\pi(s,a)$: the value of a state is the policy-weighted average of its action values.

### Bellman expectation equation

Plug $G_t=r_{t+1}+\gamma G_{t+1}$ into the definition of $V^\pi$ and take expectations step by step: first over the action the policy picks, then over where the world sends you:

$$V^\pi(s)=\sum_a\pi(a\mid s)\sum_{s'}P(s'\mid s,a)\,[R+\gamma V^\pi(s')]$$

In words: *value here = average over my actions and the world's randomness of (reward now + discounted value of where I land).* It is a consistency condition: one equation per state. For a fixed policy the equations are **linear** in the unknowns $V^\pi(s)$. In vector form, $V^\pi=R^\pi+\gamma P^\pi V^\pi$, so $V^\pi=(I-\gamma P^\pi)^{-1}R^\pi$, where $P^\pi$ is the state-to-state transition matrix under $\pi$ and $R^\pi$ the expected one-step reward. For large state spaces we iterate the equation instead of inverting the matrix (**iterative policy evaluation**).

### Bellman optimality equation

The optimal value $V^*(s)=\max_\pi V^\pi(s)$ satisfies

$$V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)\,[R+\gamma V^*(s')]$$

In words: *the best you can do from here = the best action's (reward now + discounted best value from where you land).* The average over the policy is replaced by a **max**, which makes the system non-linear, so we solve it iteratively.

The same idea for actions:
$$Q^*(s,a)=\sum_{s'}P(s'\mid s,a)\,[R+\gamma\max_{a'}Q^*(s',a')].$$
Once you have $V^*$, you get $Q^*(s,a)=\sum_{s'}P(s'\mid s,a)[R+\gamma V^*(s')]$, and the optimal policy is greedy: $\pi^*(s)=\arg\max_aQ^*(s,a)$.

## Known model (planning)

If you know $P$ and $R$, you do not need to interact with the world at all. You can *plan* with **dynamic programming**:

- **Value iteration:** start from any $V_0$ (often zeros) and repeatedly apply the optimality equation as an update, $V_{k+1}(s)=\max_a\sum_{s'}P(s'\mid s,a)[R+\gamma V_k(s')]$. Then read off the greedy policy.
- **Policy iteration:** alternate (1) *policy evaluation*: compute $V^\pi$ for the current policy (solve the linear system or iterate), and (2) *policy improvement*: make the policy greedy with respect to $V^\pi$. Repeat until the policy stops changing. It usually needs very few outer iterations.

![Value iteration on a grid world: values spreading out from the reward](../../Attachments/ML%20Animations/RL%20Basics%20and%20MDPs%20-%20value%20iteration.gif)

*Watch how value starts only at the +1 cell and spreads one cell further per sweep, shrinking by γ = 0.9 each step; the greedy arrows at the end steer around the −1 pit.*

**Why does value iteration converge?** The Bellman optimality update is a **contraction**: for any two value functions, one sweep brings them at least a factor $\gamma$ closer in max-norm, $\lVert TV-TU\rVert_\infty\le\gamma\lVert V-U\rVert_\infty$. So the error shrinks like $\gamma^k$ and the iteration reaches the unique fixed point $V^*$ from any starting point. Smaller $\gamma$ means faster convergence.

## Unknown model (learning)

Usually we do *not* know $P$ (what exactly happens when a robot pushes a cup?). Then the agent must learn from sampled experience:

- **Monte Carlo (MC):** run whole episodes, compute the actual return $G_t$ from each visited state, and average. Unbiased, but high variance and needs episodes to end.
- **TD learning:** update after every step using the *estimate* of the next state, $r_{t+1}+\gamma V(s_{t+1})$, as the target ("bootstrapping"). Lower variance, works in continuing tasks, slightly biased.

Both, and their control versions (SARSA, Q-learning, policy gradients), are in → [[Q-Learning and Policy Gradients]].

## Worked example

**A return.** Rewards $r_1=1,\ r_2=0,\ r_3=2$, then nothing, $\gamma=0.9$:
$$G_0=1+0.9\cdot0+0.9^2\cdot2=1+0+1.62=2.62.$$

**Policy evaluation on a 2-state loop.** States $A,B$. The policy always moves $A\to B$ (reward 1) and $B\to A$ (reward 0), deterministically, $\gamma=0.9$. Bellman expectation gives two linear equations:
$$V(A)=1+0.9\,V(B),\qquad V(B)=0+0.9\,V(A).$$
Substitute: $V(A)=1+0.81\,V(A)$, so $V(A)=1/0.19\approx5.26$ and $V(B)=0.9\cdot5.26\approx4.74$. $B$ is worth less because its reward is one step further away.

**One sweep of value iteration.** Add a second action in $A$: "stay" with reward 0.5 (back to $A$). Start from $V_0=0$:
- $V_1(A)=\max(\underbrace{1+0.9\cdot0}_{\text{go}},\ \underbrace{0.5+0.9\cdot0}_{\text{stay}})=1$, $V_1(B)=0$.
- $V_2(A)=\max(1+0.9\cdot0,\ 0.5+0.9\cdot1)=\max(1,1.4)=1.4$, $V_2(B)=0+0.9\cdot1=0.9$.
- $V_3(A)=\max(1+0.9\cdot0.9,\ 0.5+0.9\cdot1.4)=\max(1.81,1.76)=1.81$.

Notice that the preferred action flipped between sweeps: early estimates can be misleading, and only the converged values tell you the right policy (here staying gives $0.5/(1-0.9)=5$, less than the loop's 5.26, so "go" wins in the end).

## Concepts

- **Exploration vs exploitation.** Exploit = take the action that currently looks best; explore = try something else to learn more. Pure exploitation can lock in a mediocre choice forever.
  - **ε-greedy:** with probability $\varepsilon$ take a uniformly random action, otherwise the greedy one. Simple, but explores *undirected* (it wastes tries on clearly bad actions).
  - **UCB** (upper confidence bound): pick $\arg\max_a\big[\hat Q(a)+c\sqrt{\ln t/N(a)}\big]$, i.e. "optimism in the face of uncertainty": rarely-tried actions get a bonus. *Directed* exploration.
  - **Thompson sampling:** keep a posterior over each action's value (e.g. a Beta distribution for success rates), sample one value per action from it, and act greedily on the sample. Actions are tried in proportion to the probability that they are the best.
- **On-policy vs off-policy.** On-policy methods learn the value of the policy they are actually following (SARSA). Off-policy methods learn about one policy (often the greedy one) from data generated by another (Q-learning, learning from replay buffers or logs).
- **Model-based vs model-free.** Model-based methods know or learn $P$ and $R$ and plan with them (dynamic programming, AlphaZero-style search). Model-free methods learn values or policies directly from experience without ever modelling the dynamics (Q-learning, policy gradients).
- **Discount factor.** $\gamma$ is both a modelling choice ("how much do I care about the future?") and a mathematical convenience (it keeps infinite sums finite and makes the Bellman operator a contraction). Too small → myopic behaviour; close to 1 → slow learning and high variance.

| | Needs a model? | Learns from |
|---|---|---|
| Value / policy iteration | yes | the model (no interaction) |
| Monte Carlo | no | complete episodes |
| TD, SARSA, Q-learning | no | single transitions |

## Common confusions

- **"Reward and value are the same thing."** → Reward is the immediate signal from one step; value is the *expected discounted sum* of all future rewards. A state can have zero reward but high value (the square next to the goal).
- **"The Markov property means the world is deterministic."** → No, transitions can be random. Markov only says the *distribution* of the next state depends on the current state and action alone, not on the history.
- **"$V^*$ tells you what to do."** → Not directly. To act greedily from $V^*$ you still need the model ($P$, $R$) to look one step ahead. $Q^*$ is directly actionable ($\arg\max_aQ^*(s,a)$), which is why model-free methods learn $Q$.
- **"$\gamma<1$ only matters in infinite tasks."** → It also changes *which* policy is optimal in finite tasks: smaller $\gamma$ prefers quick small rewards over large distant ones.
- **"Value iteration needs a good initial guess."** → Because the update is a contraction, any start converges; a good start only saves sweeps.

## Check yourself

> [!question]- Rewards are +1 forever and $\gamma=0.8$. What is the return?
> A geometric series: $G=1/(1-0.8)=5$.

> [!question]- What is the difference between the Bellman expectation and optimality equations?
> The expectation equation averages over the actions of a *given* policy $\pi$ ($\sum_a\pi(a\mid s)\dots$) and is linear; the optimality equation takes the *best* action ($\max_a\dots$) and is non-linear. The first evaluates a policy, the second characterises the optimal one.

> [!question]- Why is learning $Q$ more useful than learning $V$ when you have no model?
> Acting greedily with $V$ requires predicting next states with $P$. With $Q$, you just pick $\arg\max_aQ(s,a)$, no model needed.

> [!question]- A robot only sees its current camera image but needs to know its velocity. Is this an MDP? How do you fix it?
> Not quite: a single image does not determine velocity, so the Markov property fails. Add more to the state, e.g. stack the last few frames or include velocity sensors.

> [!question]- Which exploration strategy wastes trials on actions it already knows are terrible?
> ε-greedy: its random actions are uniform. UCB and Thompson sampling direct exploration towards actions that are uncertain *and* could plausibly be best.

## Practice

[RL Basics and MDPs - Exercises](RL%20Basics%20and%20MDPs%20-%20Exercises.ipynb): returns and discounting, Bellman equations as a linear system, value iteration and policy iteration by hand and in code, Monte Carlo evaluation, and ε-greedy vs UCB vs Thompson sampling on a bandit.

## Learn more
- [Sutton & Barto (free)](http://incompleteideas.net/book/the-book-2nd.html) ch. 3–4
- [David Silver RL course](https://www.davidsilver.uk/teaching/)
- [Gymnasium](https://gymnasium.farama.org/)
- [Hugging Face Deep RL Course (free)](https://huggingface.co/learn/deep-rl-course) — hands-on introduction with Gymnasium environments
