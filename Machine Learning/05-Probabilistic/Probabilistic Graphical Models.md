---
tags: [ml, probabilistic, graphical-models]
---
# Probabilistic Graphical Models

> [!summary] In one sentence
> A probabilistic graphical model draws random variables as nodes and direct dependencies as edges, so that the missing edges tell you which variables are conditionally independent, which shrinks a huge joint distribution into a product of small local pieces you can store, learn and reason with.

## Intuition first

Graph structure encodes conditional independence.

Suppose you model 30 yes/no variables about a patient (symptoms, diseases, test results). A full joint probability table has $2^{30}-1\approx10^9$ numbers: impossible to store, let alone learn. But most variables do not *directly* affect each other: a cough depends on flu and smoking, not on your blood type. A graph lets you say exactly that, and the joint collapses to a product of small tables.

**Analogy: gossip in a village.** Each person (node) only talks to their neighbours (edges). What you know about a far-away person reaches you only through the chain of people in between. If you already know what your direct neighbours think (you *condition* on them), news from further away tells you nothing new. That "screening off" is conditional independence, and the graph makes it visible.

Two flavours:
- **Directed (Bayesian networks)**: arrows mean "directly influences / generates". Natural for causal and generative stories.
- **Undirected (Markov random fields)**: links mean "are compatible with / like to agree". Natural for symmetric interactions such as neighbouring pixels.

![Explaining away in the Rain/Sprinkler/Wet-grass network](../../Attachments/ML%20Animations/Probabilistic%20Graphical%20Models%20-%20explaining%20away.gif)

*Watch the blue bar: wet grass makes rain more likely (0.20 → 0.43), but once you also learn the sprinkler was on, rain drops back to 0.22, even though rain and sprinkler are independent a priori.*

## The math, step by step

### Bayesian networks (directed)

$$p(x_1..x_n)=\prod_i p(x_i\mid\mathrm{pa}(x_i))$$

- $\mathrm{pa}(x_i)$: the parents of node $i$ (nodes with an arrow into it).
- Each factor is a **conditional probability table (CPT)** or conditional density.
- The graph must be a DAG (no directed cycles), so you can generate data by sampling parents before children (*ancestral sampling*).

**Why it saves parameters.** For binary variables, node $i$ needs $2^{|\mathrm{pa}(x_i)|}$ numbers (one probability per parent configuration). The total is $\sum_i2^{|\mathrm{pa}(x_i)|}$ instead of $2^n-1$. Rain/Sprinkler/Wet: $1+1+4=6$ numbers vs $2^3-1=7$; with 30 nodes of at most 3 parents it is at most $30\cdot8=240$ vs a billion.

### The three basic structures

**d-separation** tells which independences hold (chain, fork, collider/explaining away). Everything follows from three 3-node patterns:

| Pattern | Graph | Marginally | Given the middle node $B$ |
|---|---|---|---|
| Chain | $A\to B\to C$ | dependent | $A\perp C\mid B$ (B blocks the flow) |
| Fork (common cause) | $A\leftarrow B\to C$ | dependent | $A\perp C\mid B$ (B blocks) |
| Collider (common effect) | $A\to B\leftarrow C$ | $A\perp C$ | **dependent** (observing B, or any descendant of B, opens the path) |

The collider is the counter-intuitive one, and it is called **explaining away**: two independent causes become dependent once you observe their common effect, because evidence for one cause "uses up" the effect and lowers the need for the other.

**d-separation rule.** $X$ and $Y$ are conditionally independent given a set $Z$ if *every* undirected path between them is blocked. A path is blocked if it contains a chain or fork whose middle node is in $Z$, or a collider whose middle node is *not* in $Z$ and has no descendant in $Z$.

**Markov blanket.** A node is independent of everything else given its parents, children, and its children's other parents. This is what makes Gibbs sampling ([[MCMC]]) cheap in a graphical model.

### Markov random fields (undirected)

$$p(x)=\frac1Z\prod_c\psi_c(x_c)$$ over cliques; $Z$ intractable in general.

- $c$ ranges over cliques (fully connected subsets of nodes); $x_c$ are the variables in clique $c$.
- $\psi_c\ge0$ are **potentials**: unnormalised "compatibility scores", *not* probabilities.
- $Z=\sum_x\prod_c\psi_c(x_c)$ is the **partition function**, a sum over every joint configuration, exponential in $n$.
- Independence is simpler than in BNs: $A\perp C\mid B$ whenever every path from $A$ to $C$ passes through $B$ (graph separation).

Example: the **Ising model** on an image grid, $\psi(x_i,x_j)=\exp(Jx_ix_j)$ with $x\in\{-1,+1\}$: neighbouring pixels prefer to agree when $J>0$.

**Directed or undirected?** Use a BN when there is a natural generative or causal direction (disease → symptom). Use an MRF when interactions are symmetric and there is no "who causes whom" (pixels, spins, neighbouring words for labelling).

### Inference

Inference = computing marginals or conditionals such as $p(\text{rain}\mid\text{wet})$, or the most likely configuration.

- Exact: variable elimination, belief propagation / junction tree (exponential in treewidth).
- Approximate: [[Variational Inference]], [[MCMC]], loopy BP.

**Variable elimination** pushes sums inside products. On a chain $x_1-x_2-\dots-x_n$ with $k$ states each,
$$p(x_n)=\sum_{x_{n-1}}p(x_n\mid x_{n-1})\cdots\sum_{x_1}p(x_2\mid x_1)p(x_1),$$
computed right-to-left costs $O(nk^2)$ instead of $O(k^n)$ for brute-force enumeration. **Belief propagation** is the same idea phrased as messages passed along edges; it is exact on trees. On graphs with loops, the **junction tree** algorithm clusters nodes into a tree, at a cost exponential in the treewidth. Loopy BP just runs the messages anyway and hopes they converge.

**HMM forward algorithm** (variable elimination on a time chain). Hidden states $z_t$, transitions $A_{ij}=p(z_t=j\mid z_{t-1}=i)$, emissions $p(x_t\mid z_t)$:
$$\alpha_t(j)=p(x_t\mid z_t=j)\sum_i\alpha_{t-1}(i)A_{ij},\qquad p(x_{1:T})=\sum_j\alpha_T(j).$$
Replace $\sum$ by $\max$ (and keep back-pointers) and you get **Viterbi decoding**, the most likely hidden path.

### Learning

Parameters: MLE counts (fully observed) or [[Gaussian Mixture Models and EM|EM]] (latent). Structure: score-based or constraint-based.

- **Fully observed**: the likelihood factorises over CPTs, so each is estimated independently by counting: $\hat p(x_i=a\mid\mathrm{pa}=b)=\frac{N(x_i=a,\mathrm{pa}=b)}{N(\mathrm{pa}=b)}$. Add pseudo-counts (a Dirichlet prior, see [[Bayesian Inference]]) to avoid zeros.
- **Latent variables**: counts are unknown, so EM fills them in with expected counts (E-step) and re-counts (M-step).
- **Structure learning**: *score-based* searches over graphs maximising a score like BIC; *constraint-based* (e.g. the PC algorithm) runs conditional independence tests and builds a graph consistent with them.

## Worked example: explaining away in numbers

Rain $R$ and Sprinkler $S$ are independent with $P(R)=0.2$, $P(S)=0.3$. Wet grass: $P(W\mid R,S)=0.05,\,0.9,\,0.9,\,0.99$ for $(R,S)=(0,0),(1,0),(0,1),(1,1)$.

1. Joint terms with $W=1$:
   - $(0,0)$: $0.8\cdot0.7\cdot0.05=0.028$
   - $(1,0)$: $0.2\cdot0.7\cdot0.9=0.126$
   - $(0,1)$: $0.8\cdot0.3\cdot0.9=0.216$
   - $(1,1)$: $0.2\cdot0.3\cdot0.99=0.0594$
   - Sum: $P(W=1)=0.4294$.
2. $P(R=1\mid W=1)=\frac{0.126+0.0594}{0.4294}\approx0.43$ (up from 0.20).
3. $P(S=1\mid W=1)=\frac{0.216+0.0594}{0.4294}\approx0.64$ (up from 0.30).
4. Now also observe $S=1$: $P(R=1\mid W=1,S=1)=\frac{0.0594}{0.216+0.0594}\approx0.22$.

The sprinkler "explains" the wet grass, so rain falls back almost to its prior. This is exactly the collider rule: $R\perp S$, but $R\not\perp S\mid W$.

**A tiny MRF.** Two spins $x_1,x_2\in\{-1,+1\}$ with $\psi(x_1,x_2)=e^{x_1x_2}$. Then $Z=e+e^{-1}+e^{-1}+e=2e+2e^{-1}\approx6.17$ and $P(x_1=x_2)=2e/Z\approx0.88$.

## Examples

[[Naive Bayes]], HMM, Kalman filter, LDA topic model, PPCA, mixture models. See your AI notes in [[5-semester/Machine intelligence/Noter små|Noter små]].

- **[[Naive Bayes]]**: a class node with arrows to every feature (a fork), so features are independent given the class.
- **HMM**: a chain of discrete hidden states, each emitting an observation. **Kalman filter**: the same graph with linear-Gaussian states.
- **Mixture models / PPCA**: one latent per data point ($z\to x$), discrete for mixtures, continuous Gaussian for PPCA.
- **LDA topic model**: documents → topic proportions → per-word topic → word.

## Common confusions

- **"Arrows mean causation."** → A BN only encodes conditional independences; many different arrow directions encode the same independences. A causal reading is an extra assumption.
- **"Observing more variables can only make things more independent."** → Not at colliders: observing a common effect *creates* dependence (explaining away).
- **"MRF potentials are probabilities."** → They are arbitrary non-negative scores; only after dividing by $Z$ do you get probabilities.
- **"Exact inference is always exponential."** → Only in the treewidth. Chains and trees (HMMs, Naive Bayes) are linear time.
- **"No edge between A and C means A and C are independent."** → It means they are independent *given the right conditioning set*; they can still be dependent through other paths.

## Check yourself

> [!question]- In $A\to B\to C$, are $A$ and $C$ independent? And given $B$?
> Not marginally (information flows through $B$); yes given $B$.

> [!question]- In $A\to B\leftarrow C$, what happens to the dependence between $A$ and $C$ when $B$ (or a child of $B$) is observed?
> They become dependent (explaining away). Marginally they are independent.

> [!question]- How many parameters does a binary BN $A\to C\leftarrow B$, $C\to D$ need, versus the full joint?
> $1+1+4+2=8$ vs $2^4-1=15$.

> [!question]- Why is the partition function $Z$ of an MRF hard to compute?
> It sums the product of potentials over every joint configuration: $k^n$ terms for $n$ variables with $k$ states.

> [!question]- What changes between the HMM forward algorithm and Viterbi?
> The sum over previous states becomes a max (with back-pointers to recover the best path).

## Practice

[Probabilistic Graphical Models - Exercises](Probabilistic%20Graphical%20Models%20-%20Exercises.ipynb): chain/fork/collider, explaining away, directed vs undirected, parameter counting, d-separation queries, a tiny MRF's partition function, variable elimination and the HMM forward recursion by hand, then enumeration, variable elimination, CPT learning, the forward algorithm, Viterbi and Gibbs sampling on an Ising model in code.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 8
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [Stanford CS228 – Probabilistic Graphical Models course notes](https://ermongroup.github.io/cs228-notes/)
