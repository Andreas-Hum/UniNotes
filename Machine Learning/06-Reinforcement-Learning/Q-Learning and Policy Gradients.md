---
tags: [ml, rl]
status: not-started
notebook: not-started
level:
reviewed:
---
# Q-Learning and Policy Gradients

> [!summary] In one sentence
> When you do not know the rules of the world, you can either learn **how good each action is** (value-based: TD, SARSA, Q-learning, DQN) or directly learn **which actions to take** by nudging a policy towards what worked (policy gradients), and actor–critic methods combine both.

## Intuition first

In [[RL Basics and MDPs]] we solved MDPs when we *knew* the transition probabilities. Real problems rarely hand you $P(s'\mid s,a)$. A robot does not know the physics of every object; a game-playing agent does not know its opponent. It has to learn from experience, one transition $(s,a,r,s')$ at a time.

There are two big families of ideas:

- **Value-based: "keep a scorecard."** For every situation and action, keep an estimate of how much reward it eventually brings ($Q(s,a)$). After each step, compare what you predicted with what actually happened plus what you now predict for the next state, and move your estimate a little towards that. Then act by picking the action with the best score. This is like a chess player who, after each game, revises their gut feeling for positions: "that position felt good, but I lost from there, so it is worse than I thought."
- **Policy-based: "reinforce what worked."** Keep a probability for each action and directly make actions that led to high returns more likely, and those that led to low returns less likely. This is how you learn to throw darts: you do not compute a value table, you just repeat motions that hit near the bullseye.

**Actor–critic** methods do both: an *actor* (the policy) chooses actions, and a *critic* (a value function) judges them so the actor gets a less noisy learning signal.

## Value-based

### TD(0): learning from one step

$$V(s)\leftarrow V(s)+\alpha\big[r+\gamma V(s')-V(s)\big]$$

- $\alpha$: learning rate (how far to move each time).
- $r+\gamma V(s')$: the **TD target**, a one-step guess of the return: the reward actually received plus the *current estimate* of the next state's value.
- $\delta=r+\gamma V(s')-V(s)$: the **TD error**, how surprised we are. Positive → things went better than expected → raise $V(s)$.

This is "bootstrapping": we update a guess using another guess. Compared with Monte Carlo (which waits for the full return $G_t$), TD has **lower variance** (one random reward instead of a whole episode of them) but is **biased** (the target uses an imperfect $V(s')$), and it can learn from incomplete episodes and continuing tasks.

### SARSA (on-policy)

$$Q(s,a)\leftarrow Q+\alpha\big[r+\gamma Q(s',a')-Q\big]$$

The name lists the data it needs: $(S,A,R,S',A')$. The target uses $a'$, the action the agent **actually takes next** with its current (e.g. ε-greedy) policy. So SARSA learns the value of the policy it is following, exploration included. That makes it *cautious*: on the classic cliff-walking task it learns a safer path away from the edge, because it knows its own random moves sometimes fall off.

### Q-learning (off-policy)

$$Q(s,a)\leftarrow Q+\alpha\big[r+\gamma\max_{a'}Q(s',a')-Q\big]$$

The only change is $Q(s',a')\to\max_{a'}Q(s',a')$: the target assumes the agent will act *greedily* from $s'$, whatever it actually does. So Q-learning learns $Q^*$ (the optimal policy's values) while behaving exploratorily. That is what **off-policy** means: the *target policy* (greedy) differs from the *behaviour policy* (ε-greedy). Because the update only needs $(s,a,r,s')$, it can learn from old data, other agents' data, or a replay buffer. On the cliff it learns the optimal path right along the edge (and falls off more often during training).

![Q-learning on a corridor: values propagating backwards from the goal](../../Attachments/ML%20Animations/Q-Learning%20and%20Policy%20Gradients%20-%20Q-values%20propagating.gif)

*Watch how only the cell next to the goal learns in episode 1; each further episode pushes value one cell further back, discounted by γ, exactly as the update formula on top says.*

### Maximisation bias and Double Q-learning

$\max_{a'}Q(s',a')$ over *noisy* estimates is biased upwards: $\mathbb E[\max_a\hat Q(a)]\ge\max_a\mathbb E[\hat Q(a)]$. If all actions are truly worth 0 but estimates are noisy, the max is still positive. **Double Q-learning** keeps two estimates and uses one to *pick* the action and the other to *evaluate* it: target $r+\gamma Q_B\big(s',\arg\max_{a'}Q_A(s',a')\big)$, which removes most of the bias.

### DQN: Q-learning with a neural network

For huge state spaces (Atari screens) a table is impossible, so DQN uses a [[Neural Networks|neural net]] Q-function $Q_\theta(s,a)$ + a replay buffer + a target network:

- **Experience replay:** store transitions and train on random mini-batches. Breaks the strong correlation between consecutive frames and reuses data (possible because Q-learning is off-policy).
- **Target network** $Q_{\theta^-}$: compute targets $r+\gamma\max_{a'}Q_{\theta^-}(s',a')$ with a copy of the network that is only updated every $C$ steps. Otherwise the target moves every time you update, like chasing your own shadow.

Extensions: **Double** DQN (online net selects, target net evaluates → less overestimation), **Dueling** (separate heads, $Q=V+A-\bar A$, so the state value is learned even when actions do not matter), **Prioritized** replay (replay surprising transitions with large $|\delta|$ more often), **Rainbow** (combines these and more).

Why all the tricks? Combining **function approximation + bootstrapping + off-policy** learning (the "deadly triad") can diverge. Replay and target networks keep it stable in practice.

## Policy-based

Parameterise the policy directly, $\pi_\theta(a\mid s)$ (e.g. a softmax over network outputs), and do gradient *ascent* on the expected return $J(\theta)$.

**REINFORCE** (the policy-gradient theorem):
$$\nabla_\theta J=\mathbb E\big[\nabla_\theta\log\pi_\theta(a\mid s)\,G_t\big]$$

Deriving it in small steps (for one decision, to see the trick):

1. $J(\theta)=\sum_a\pi_\theta(a)\,G(a)$.
2. $\nabla J=\sum_a\nabla\pi_\theta(a)\,G(a)$.
3. Log-derivative trick: $\nabla\pi=\pi\,\nabla\log\pi$, so $\nabla J=\sum_a\pi_\theta(a)\,\nabla\log\pi_\theta(a)\,G(a)=\mathbb E_{a\sim\pi}[\nabla\log\pi_\theta(a)\,G]$.
4. An expectation can be estimated by sampling: play, observe $G_t$, and step along $\nabla\log\pi_\theta(a_t\mid s_t)\,G_t$.

In words: $\nabla\log\pi(a\mid s)$ is the direction that makes the taken action more likely; scale it by how good the outcome was.

For a softmax policy with logits $\theta$, $\nabla_\theta\log\pi(a)=e_a-\pi$ (one-hot of the taken action minus the probability vector): raise the taken action's logit, lower the others in proportion to their probability.

**Baseline:** subtract a baseline to reduce variance: use $(G_t-b(s))$ instead of $G_t$. It does not change the expected gradient, because
$$\mathbb E_a[\nabla\log\pi_\theta(a\mid s)\,b(s)]=b(s)\sum_a\nabla\pi_\theta(a\mid s)=b(s)\,\nabla\!\sum_a\pi_\theta(a\mid s)=b(s)\nabla1=0.$$
Intuition: without a baseline, if all returns are positive, *every* sampled action gets pushed up and only the relative sizes sort things out, which is noisy. With $b\approx$ average return, better-than-average actions go up and worse-than-average go down.

![REINFORCE with a baseline shifting probability towards the best action](../../Attachments/ML%20Animations/Q-Learning%20and%20Policy%20Gradients%20-%20REINFORCE%20update.gif)

*Watch the sign of $G-b$: a green (positive) advantage grows the sampled bar, a red one shrinks it, and mass flows to $a_2$, the action whose return beats the baseline.*

## Actor–critic

A **critic** estimates $V$/$Q$, and the **actor** updates the policy using the critic's judgement instead of the raw, noisy return. Typically the actor uses the advantage $A(s,a)=Q(s,a)-V(s)$, estimated by the TD error $\delta=r+\gamma V(s')-V(s)$.

- **A2C/A3C**: synchronous / asynchronous advantage actor–critic with many parallel workers.
- **PPO** (clipped objective, workhorse): with ratio $\rho=\pi_\theta(a\mid s)/\pi_{\theta_\text{old}}(a\mid s)$, maximise
  $$L^{\text{CLIP}}=\mathbb E\big[\min\big(\rho A,\ \mathrm{clip}(\rho,1-\epsilon,1+\epsilon)A\big)\big].$$
  In words: improve the policy, but once the new policy has moved more than $\pm\epsilon$ (e.g. 20 %) away from the old one on a sample, stop getting credit for moving further. This allows several gradient steps per batch of data without wrecking the policy. Simple, robust, the default in many libraries and in RLHF.
- **TRPO**: the predecessor; enforces a hard KL-divergence trust region (more complex second-order optimisation).
- **SAC/TD3** (continuous control): off-policy actor–critics for continuous actions (robot torques). SAC adds an entropy bonus for exploration; TD3 uses twin critics (taking the minimum, like Double Q) and delayed actor updates.

## Worked example

**One TD(0) update.** $V(s)=1$, $V(s')=4$, $r=0$, $\alpha=0.5$, $\gamma=0.9$.
Target $=0+0.9\cdot4=3.6$; TD error $\delta=3.6-1=2.6$; new $V(s)=1+0.5\cdot2.6=2.3$.

**SARSA vs Q-learning on the same transition.** $Q(s,a)=1$, $r=1$, $\gamma=0.9$, $\alpha=0.5$, and in $s'$ the two actions have $Q(s',\cdot)=(2,5)$. The ε-greedy agent happens to explore and pick the action worth 2.
- SARSA target: $1+0.9\cdot2=2.8$ → $Q=1+0.5(2.8-1)=1.9$.
- Q-learning target: $1+0.9\cdot5=5.5$ → $Q=1+0.5(5.5-1)=3.25$.

Q-learning ignores the exploratory move; SARSA "pays" for it.

**One REINFORCE step.** Three actions, logits $\theta=(0,0,0)$, so $\pi=(\tfrac13,\tfrac13,\tfrac13)$. We sample $a_2$, observe $G=3$, baseline $b=1$, step size $0.3$.
$\nabla\log\pi(a_2)=e_2-\pi=(-\tfrac13,\tfrac23,-\tfrac13)$, so $\theta\leftarrow0.3\cdot(3-1)\cdot(-\tfrac13,\tfrac23,-\tfrac13)=(-0.2,0.4,-0.2)$.
New probabilities: $e^{-0.2}=0.819$, $e^{0.4}=1.492$, so $\pi\approx(0.26,0.48,0.26)$. The sampled, better-than-baseline action went from 0.33 to 0.48.

**PPO clipping** with $\epsilon=0.2$:
- $A=+2$, $\rho=1.5$: $\min(3,\ 1.2\cdot2)=2.4$ → clipped, no gradient to push $\rho$ further up.
- $A=-1$, $\rho=0.5$: $\min(-0.5,\ 0.8\cdot(-1))=-0.8$ → clipped, no gradient to push $\rho$ further down.
- $A=+2$, $\rho=0.9$: $\min(1.8,\ 1.8)=1.8$ → inside the trust region, normal gradient.

## Choosing an algorithm

| Setting | Good default | Why |
|---|---|---|
| Discrete actions, cheap simulator (Atari) | DQN family | off-policy, sample reuse via replay |
| Continuous actions, expensive real-world samples | SAC / TD3 | off-policy, sample-efficient, continuous |
| General purpose, parallel simulation, stability matters | PPO | robust, few hyperparameters |
| Tiny problems, teaching | tabular Q-learning, REINFORCE | transparent |

## Applications

Games (AlphaGo: policy and value networks plus tree search), robotics (locomotion, manipulation), RLHF for language models ([[Transformers]]): a reward model trained on human preferences scores the model's answers and PPO-style updates fine-tune the policy (the language model).

Foundations: [[RL Basics and MDPs]].

## Common confusions

- **"Off-policy means it does not use a policy."** → It means the policy being *learned* (greedy) differs from the one *generating data* (ε-greedy, old policies, demonstrations).
- **"Q-learning is always better than SARSA because it learns the optimal policy."** → It learns the optimal *greedy* values, but the agent's *online* performance while still exploring can be worse (cliff walking). SARSA is safer when exploration mistakes are costly.
- **"A baseline biases the policy gradient."** → Any baseline that does not depend on the action leaves the expected gradient unchanged (proof above); it only reduces variance.
- **"TD is just a cheaper Monte Carlo."** → They make a different trade-off: MC is unbiased with high variance; TD is biased (bootstraps) with lower variance and can learn online and in never-ending tasks.
- **"PPO's clip limits the step size of $\theta$."** → It limits how much the *policy's probabilities* change per sample (the ratio $\rho$), not the parameter step directly.

## Check yourself

> [!question]- What is the only difference between the SARSA and Q-learning updates, and what does it change?
> SARSA uses $Q(s',a')$ for the action actually taken next; Q-learning uses $\max_{a'}Q(s',a')$. SARSA therefore learns the value of its exploratory policy (on-policy); Q-learning learns the optimal greedy values (off-policy).

> [!question]- Why can DQN use a replay buffer but on-policy methods like SARSA or vanilla REINFORCE cannot (without corrections)?
> Q-learning's target needs only $(s,a,r,s')$ and assumes greedy behaviour afterwards, so data from any old policy is valid. On-policy methods need data from the *current* policy; old data comes from a different policy.

> [!question]- What does the target network in DQN fix?
> The moving-target problem: without it, every update changes the targets you regress to, which can cause oscillation or divergence. A frozen copy keeps targets fixed for $C$ steps.

> [!question]- All returns in your environment are between 100 and 110. Why is REINFORCE without a baseline slow here?
> Every sampled action is pushed up strongly (returns ≈ 100), and only the small differences (0–10) carry information, so the gradient estimate is dominated by noise. Subtracting $b\approx105$ leaves the informative part.

> [!question]- Which family would you try first for a 7-joint robot arm with costly real-world data?
> An off-policy continuous-control actor–critic such as SAC or TD3: continuous actions and sample reuse matter more than simplicity.

## Practice

[Q-Learning and Policy Gradients - Exercises](Q-Learning%20and%20Policy%20Gradients%20-%20Exercises.ipynb): TD(0) on a random walk, SARSA vs Q-learning on the cliff, maximisation bias and Double Q-learning, REINFORCE on a bandit with and without a baseline, and the PPO clipped objective by hand.

## Learn more
- [Sutton & Barto (free)](http://incompleteideas.net/book/the-book-2nd.html) ch. 6 & 13
- [OpenAI Spinning Up](https://spinningup.openai.com/)
- [DQN](https://arxiv.org/abs/1312.5602)
- [PPO](https://arxiv.org/abs/1707.06347)
- [Spinning Up: Intro to Policy Optimization](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html) — the policy-gradient derivation step by step
- [Lilian Weng – Policy Gradient Algorithms](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) — survey from REINFORCE to PPO and SAC
