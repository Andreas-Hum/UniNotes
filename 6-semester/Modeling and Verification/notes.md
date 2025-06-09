# Small common things

## The meaning of programs
An algorithm is specified as a collection of legal inputs and, for each legal input it is associated an output. 

The samantics is a function mapping states to states $[ \text{States}\mapsto \text{States}]$
it can also be a partial function if a state is undefined $[ \text{States}\rightharpoonup \text{States}]$

## Semantics
- Each input is associated with an output value
- Non-termination = undefined output (the partial function)  
- In case of termination the result is unique
## Reactive system
it is a computing system that reacts to stimuli from its environment



<div style="page-break-after: always;"></div>
# Labelled Transition Systems

A **Labelled Transition System** (LTS) is a tuple:

$$ ( \text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \mid \alpha \in \text{Act} \} ) $$

where:
- $\text{Proc}$ is a set of **states** (or **processes**),
- $\text{Act}$ is a set of **actions** (or **labels**),
- for each $\alpha \in \text{Act}$, $\xrightarrow{\alpha} \subseteq \text{Proc} \times \text{Proc}$ is a **binary relation** called the **transition relation** $\xrightarrow{\alpha}$.

Sometimes we distinguish an **initial** (or **start**) state.

---

## Recap of Binary Relations

A **binary relation** $R$ on a set $A$ is a subset:

$$ R \subseteq A \times A. $$

Sometimes we write:

$$ a \ R \ a' $$

instead of:

$$ (a, a') \in R. $$

---
## Properties of Relations and Their Closures

### Reflexive

**Definition**: $R$ is **reflexive** if:

$$ (a, a) \in R \quad \text{for all} \ a \in A. $$

**Reflexive closure**: If $R$ is not already reflexive, we can make it reflexive by **adding** all pairs $(a,a)$ for every $a \in A$.

---
### Symmetric

**Definition**: $R$ is **symmetric** if:

$$ (a, b) \in R \ \Rightarrow \ (b, a) \in R, \quad \text{for all} \ a, b \in A. $$

**Symmetric closure**: If $R$ is not symmetric, we can make it symmetric by **adding the reverse** of every existing pair.

---
### Transitive

**Definition**: $R$ is **transitive** if:

$$ (a, b) \in R \ \text{and} \ (b, c) \in R \ \Rightarrow \ (a, c) \in R, \quad \text{for all} \ a, b, c \in A. $$

**Transitive closure**: If $R$ is not transitive, we can make it transitive by **adding shortcuts** — whenever a path $a \to b \to c$ exists, we add a direct transition $a \to c$.

---
## LTS - Notation (Extension to Words)

Let $(\text{Proc}, \text{Act}, \{\xrightarrow{\alpha} \mid \alpha \in \text{Act}\})$ be an LTS.
We can extend $\xrightarrow{\alpha}$ from single labels $\alpha \in \text{Act}$ to **words** $w \in \text{Act}^*$.
The extension $\xrightarrow{w}$ is defined inductively:
- For every $p \in \text{Proc}$:

$$p \xrightarrow{\varepsilon} p$$
where $\varepsilon$ is the **empty word**.
- For $w = \alpha \cdot w'$, and $p, p' \in \text{Proc}$:
$$p \xrightarrow{w} p' \quad \text{if there exists}\ p'' \in \text{Proc}\ \text{such that}\ p \xrightarrow{\alpha} p''\ \text{and}\ p'' \xrightarrow{w'} p'.$$
**Intuition**: The path:
$$p = p_0 \xrightarrow{\alpha_1} p_1 \xrightarrow{\alpha_2} p_2 \xrightarrow{\alpha_3} \dots \xrightarrow{\alpha_n} p_n = p'$$
corresponds to:
$$p \xrightarrow{w} p' \quad \text{where}\ w = \alpha_1 \alpha_2 \dots \alpha_n.$$

---
## LTS - Notation (Derived Relations)

Let $(\text{Proc}, \text{Act}, \{\xrightarrow{\alpha} \mid \alpha \in \text{Act}\})$ be an LTS.
We define:
- **Unlabelled transition relation**:
$$\xrightarrow{} \ =\ \{(p, p') \mid p \xrightarrow{\alpha} p'\ \text{for some}\ \alpha \in \text{Act}\}$$
- **Reflexive and transitive closure** of $\xrightarrow{}$:
$$\xrightarrow{*}$$
so that:
$$p \xrightarrow{*} p'$$

means that $p$ can reach $p'$ via **zero or more transitions**.

---
### Useful Notation

- $p \xrightarrow{}$ means there exists $p' \in \text{Proc}$ such that:
$$p \xrightarrow{} p'.$$

- $p \nrightarrow$ means there is **no** $p' \in \text{Proc}$ such that:
$$p \xrightarrow{} p'.$$
In other words: $p$ is a **terminal** or **deadlock** state.

---
## Reachable States
A state $p'$ is **reachable** from $p$ if:
$$p \xrightarrow{*} p'.$$

The set of **reachable states** from an initial state $p_0$ is:
$$\{p' \mid p_0 \xrightarrow{*} p'\}.$$
<div style="page-break-after: always;"></div>



<div style="page-break-after: always;"></div>
# CCS (Calculus of communicating systems)
Each process is characterized by:
- a **name**  
- an **interface** (also called **communication ports** or **channels**)  
- a **behavior**  

---
## Example Processes
$$
CM \overset{\text{def}}{=} \overline{coin} . coffee . CM
$$
$$
CS \overset{\text{def}}{=} \overline{pub} . \overline{coin} . coffee . CS
$$
---
## Key Concepts
### Communication Ports (Channels, Interfaces)

Processes communicate via **ports** (also called **channels** or **interfaces**).

---

### Nil Process
The **Nil process** represents complete **inactivity** (also called **deadlock** behavior).

---

### Prefixing
**Prefixing** is the operation that takes a process $P$ to:
$$
a.P
$$

This means the process first performs the action $a$, and then behaves like $P$.

---
### Names & Definitions
Giving names to processes allows us to **define process behaviors**, including **recursive definitions**.

---
### Choice Operator

The **choice operator** expresses **non-determinism**:
$$
P + Q
$$

The process $P + Q$ can behave as either $P$ or $Q$ — the choice is made **non-deterministically**.

![[Pasted image 20250607213834.png]]

---

### Parallel Composition

**Parallel composition** allows processes to run **concurrently**, with the possibility of **synchronous communication**:
$$
P \; | \; Q
$$

Processes $P$ and $Q$ can interact via matching input/output actions.

![[Pasted image 20250607213945.png]]

---

### Restriction Operator
The **restriction operator** limits the **visibility** of certain communication ports:
$$
(P \; | \; Q) \setminus \{a, b, \dots \}
$$

This makes ports **private** (unobservable externally), enabling **synchronization** without exposing the channels.

![[Pasted image 20250607214015.png]]

---

### Relabelling
**Relabelling** allows you to **rename ports**, enabling the definition of **generic process procedures**.
![[Pasted image 20250607214101.png]]

---

## Example & Explanation

Given:
$$
CS \overset{\text{def}}{=} \overline{pub} . \overline{coin} . coffee . CS
$$
Now consider the composition:
$$
(CM \; | \; CS) \setminus \{coin, coffee\} \; | \; CS
$$

### What happens here?
1. **Parallel composition**:  
   $CM$ and $CS$ run in parallel, and can synchronize on the actions `coin` and `coffee`.
2. **Restriction** $\setminus \{coin, coffee\}$:  
   The ports `coin` and `coffee` are made **private** to the composition $(CM \; | \; CS)$.  
   This forces `coin` and `coffee` to be used **only for synchronization between $CM$ and $CS$**, and **not observable from outside**.
3. The outer $| \; CS$ adds another $CS$ process in parallel.

### Why restrict?
With restriction, **only the internal processes** ($CM$ and $CS$) can interact over these ports — this ensures **synchronization** is controlled and encapsulated.
## Syntax and Semantics

### CCS Expressions (Syntax)

---
#### Labels vs Actions
- Let $\mathbb{A}$ be a set of **channel names**.
- Let $\overline{\mathbb{A}} = \{ \overline{a} \mid a \in \mathbb{A} \}$ be the set of **co-names**.
- Define:
  - $\mathbb{L} = \mathbb{A} \cup \overline{\mathbb{A}}$ = set of **labels**
  - $Act = \mathbb{L} \cup \{ \tau \}$ = set of **actions**, where $\tau$ is the **internal (silent) action**.

---

#### Relabelling Function
By convention, for all $a$:
$$
\overline{a} = \overline{a}
$$

A **relabelling function** is a function:

$$
f : Act \rightarrow Act
$$

such that:

$$
f(\tau) = \tau, \quad f(a) = f(a)
$$

---

#### Grammar of CCS Expressions

$$
\begin{aligned}
P &::= K \quad & \text{constant} \ (K \in \mathbb{K}) \\
P &::= \alpha . P \quad & \text{prefixing} \ (\alpha \in Act) \\
P &::= \sum_{i \in I} P_i \quad & \text{summation} \\
P &::= P \; | \; Q \quad & \text{parallel composition} \\
P &::= P \setminus L \quad & \text{restriction} \ (L \subseteq \mathbb{A}) \\
P &::= P[f] \quad & \text{relabelling} \ (f : Act \rightarrow Act) \\
\end{aligned}
$$

---

### Conventions

- The set of all CCS expressions is denoted $\mathcal{P}$.

#### Operator Precedence (from tightest to loosest):

1. **Restriction** and **Relabelling** (tightest binding)
2. **Action prefixing**
3. **Parallel composition**
4. **Summation**

---

### Notation

- $P_1 + P_2 = \sum_{i \in \{1, 2\}} P_i$
- $0 = \sum_{i \in \emptyset} P_i$

---

### CCS Programs

A **CCS program** is a set of **defining equations** of the form:

$$
K = P
$$

where:

- $K \in \mathbb{K}$ is a **process constant**
- $P \in \mathcal{P}$ is a **CCS process expression**

---

## Semantics of CCS

---
The behavior of CCS processes is **intuitively clear**.  
However, intuition alone can be misleading — and it **cannot be fed into computers**!

---
### Formal Semantics
The **formal semantics** of processes is given in terms of a **Labeled Transition System (LTS)**:
$$
(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \mid \alpha \in Act \} )
$$

Where:
- **States**: $\text{Proc} = \mathcal{P}$
- **Actions**: $Act = \mathbb{L} \cup \{ \tau \}$
- **Transitions**: defined by **Structural Operational Semantics (SOS) rules**

---

![[Pasted image 20250608000356.png]]

<div style="page-break-after: always;"></div>




# Strong Bisimilarity
In pure CCS, communication is just synchronization, with no exchange of data. In many applications, processes exchange data. To model this, CCS is extended with:
### Data-Passing Prefixes
- Input Prefix: $a(x).P$ ($x$ is a variable)  
- Output Prefix: $a(e).P$ ($e$ is an expression)

### Example: Defining Equations

$$
\begin{aligned}
Bank(total) &\overset{def}{=} save(y).Bank(total + y) \\
Job(amount) &\overset{def}{=} pay(amount).0 \\
Worker &\overset{def}{=} pay(x).save(x/2).Worker
\end{aligned}
$$
### Example System Execution
$$
Job(6) \; | \; Worker \; | \; Bank(100)
$$
Trace:
$$
\to 0 \; | \; Worker \; | \; Bank(103) \to 0 \; | \; save(3).Worker \; | \; Bank(100) \xrightarrow{\tau} \xrightarrow{\tau}
$$
## Formal Semantics

![[Pasted image 20250608131028.png]]

## Encoding into Pure CCS
Per Milner (1989), value-passing CCS can be encoded in pure CCS.
Value-passing CCS:
$$
\begin{aligned}
P &= in(x).Q(x) \\
Q(x) &= out(x).P
\end{aligned}
$$
Pure CCS encoding:
$$
\begin{aligned}
Q_i &= out_i.P \\
P &= \sum in_i.Q_i
\end{aligned}
$$
## Behavioral Equivalences

### Implementation vs Specification
Implementation:

$$
\begin{aligned}
CS &\overset{def}{=} pub.coin.coffee.CS \\
CM &\overset{def}{=} coin.coffee.CM \\
Sys &\overset{def}{=} (CM \; | \; CS) \setminus \{coin, coffee\}
\end{aligned}
$$
Specification:
$$
Spec \overset{def}{=} pub.Spec
$$

## Implementation Verification
A good behavioral equivalence should: (1) be based on observable behavior, (2) abstract from nondeterminism, (3) ignore internal behavior, (4) be at least a preorder, (5) be a congruence.

### Congruence
A relation $R \subseteq \mathcal{P} \times \mathcal{P}$ is a congruence if:
$$
\forall C[\ ], \ P \ R \ Q \implies C[P] \ R \ C[Q]
$$
### Trace Equivalence

Given LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \mid \alpha \in Act \})$, for $s \in \text{Proc}$:
$$
\text{Trace}(s) = \{ w \in Act^* \mid \exists s' \in \text{Proc}, \ s \xrightarrow{w} s' \}
$$
Trace equivalence:
$$
s \equiv_t s' \iff \text{Trace}(s) = \text{Trace}(s')
$$
## Strong Bisimilarity
**Idea**: No external observer can distinguish between two bisimilar processes.
### Definition (Strong Bisimulation)

A binary relation $R \subseteq \text{Proc} \times \text{Proc}$ is a strong bisimulation iff:
$$
\forall s, t, \ s R t \implies \forall \alpha \in Act:
$$
- If $s \xrightarrow{\alpha} s'$, then $\exists t'$ s.t. $t \xrightarrow{\alpha} t'$ and $s' R t'$.
- If $t \xrightarrow{\alpha} t'$, then $\exists s'$ s.t. $s \xrightarrow{\alpha} s'$ and $s' R t'$.
### Strong Bisimilarity
$$
s \sim t \iff \exists R \text{ strong bisimulation with } s R t
$$
Equivalently:

$$
\sim = ⊔ \{ R \mid R \text{ is a strong bisimulation} \}
$$
### Bisimilarity & CCS Laws
For all CCS processes $P, Q, R$:
- $P + Q \sim Q + P$  
- $P \; | \; Q \sim Q \; | \; P$  
- $P + 0 \sim P$  
- $P \; | \; 0 \sim P$  
- $(P + Q) + R \sim P + (Q + R)$  
- $(P \; | \; Q) \; | \; R \sim P \; | \; (Q \; | \; R)$

### Proving Non-Bisimilarity

Options:
- Exhaustive: enumerate all relations (impractical).  
- Observations to rule out candidates.  
- **Game characterization**.

### Game Characterization
- $s \sim t$ iff the **defender** has a universal winning strategy from $(s,t)$.  
- $s \not\sim t$ iff the **attacker** has a universal winning strategy from $(s,t)$.  

**Theorem**: A universal strategy = a set of moves (possibly conditional) describing player behavior in each configuration. EXPLORE THE STATES SO IF YOU FIND (s1,q1) and add it then explore from those states REMEMBER TO SEE ALL TRANSITIONS FROM EACH STATE SO BOTH s1 AND q1 if q1 can go by c to some state q' but s1 cant match it NOT STRONLY BISIMILAR

<div style="page-break-after: always;"></div>
# Weak Bisimilarity
## Buffer
### Buffer of Capacity n (CCS Implementation)
A buffer of capacity $n \geq 1$ should satisfy:
- If full: no input capability  
- If empty: no output capability  
- Otherwise: able to input or output

### Theorem: n-times
For all $n \geq 1$:
$$
B_{0,n} \sim B_{0,1} \ | \ B_{0,1} \ | \ \dots \ | \ B_{0,1}
$$
Construct the binary relation $R$:
$$
R = \{ (B_{i,n}, B_{i,1} \ | \ \dots \ | \ B_{i,1}) \mid i_1 + \dots + i_n = i \}, \quad i_1, \dots, i_n \in \{0,1\}
$$
In particular:
$$
(B_{0,n}, B_{0,1} \ | \ B_{0,1} \ | \ \dots \ | \ B_{0,1}) \in R
$$
$R$ is a strong bisimulation. (Proof →)
![[Pasted image 20250608155935.png]]

### Summary of Properties
- $\sim$ is an equivalence relation  
- $\sim$ is the largest strong bisimulation  
- $\sim$ is a congruence  
- Sufficient to prove natural equivalences: $P \ | \ 0 \sim P$, $P \ | \ Q \sim Q \ | \ P$, etc.
## Weak Bisimilarity
### Weak Transition Relation
Given LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \mid \alpha \in \text{Act} \})$, with $\tau \in \text{Act}$, define:
$$
\begin{aligned}
\Rightarrow_\alpha &= (\xrightarrow{\ })^* \text{ if } \alpha = \tau \\
\Rightarrow_\alpha &= (\xrightarrow{\ })^* \circ \xrightarrow{\alpha} \circ (\xrightarrow{\ })^* \text{ if } \alpha \neq \tau
\end{aligned}
$$
- If $\alpha \neq \tau$, $s \Rightarrow t$ means: from $s$, zero or more $\tau$ actions, then $\alpha$, then zero or more $\tau$ actions.  
- If $\alpha = \tau$, $s \Rightarrow t$ means: from $s$, zero or more $\tau$ actions.
### Definition: Weak Bisimilarity
Two states $s, t \in \text{Proc}$ are **weakly bisimilar**, written $s \approx t$, iff:
$$
\exists R \text{ weak bisimulation such that } s \ R \ t
$$
Equivalently:
$$
\approx = ⊔ \{ R \mid R \text{ is a weak bisimulation} \}
$$
### Definition: Weak Bisimulation
A binary relation $R \subseteq \text{Proc} \times \text{Proc}$ is a weak bisimulation iff:
$$
\forall s, t \in \text{Proc}, \ s \ R \ t \implies \forall \alpha \in \text{Act}:
$$
- If $s \xrightarrow{\alpha} s'$, then $\exists t'$ such that $t \Rightarrow_\alpha t'$ and $s' \ R \ t'$
- If $t \xrightarrow{\alpha} t'$, then $\exists s'$ such that $s \Rightarrow_\alpha s'$ and $s' \ R \ t'$
## The Game Characterisation
$s \approx t$ iff the **defender** has a universal winning strategy from configuration $(s, t)$.  
$s \not\approx t$ iff the **attacker** has a universal winning strategy from $(s, t)$.  
**Theorem**: The weak bisimulation game is defined like for strong bisimulation, except:
- **Defender** uses $\Rightarrow$-moves  
- **Attacker** uses $\xrightarrow{\alpha}$-moves
## Is it a Congruence?

Let $P, Q$ be CCS processes such that $P \approx Q$. Then:
- $\alpha.P \approx \alpha.Q$, for each $\alpha \in \text{Act}$
- $P \ | \ R \approx Q \ | \ R$ and $R \ | \ P \approx R \ | \ Q$, for any CCS process $R$
- $P[f] \approx Q[f]$, for any relabelling function $f$
- $P \setminus L \approx Q \setminus L$, for any $L \subseteq \mathbb{A}$
### What About Nondeterministic Choice?
Example:

$$
\tau.a.0 \approx a.0 \text{ but } \tau.a.0 + b.0 \not\approx a.0 + b.0
$$
**Conclusion**: Weak bisimilarity is **not** a congruence for CCS!

<div style="page-break-after: always;"></div>

# Hennessy-Milner Logic
## Verifying Correctness
Impl $\equiv$ Spec. $\equiv$ is an abstract equivalence (e.g., $\sim$, $\approx$). Spec and Impl often expressed in same language; Spec defines expected behavior.
### Approaches
**Equivalence Checking**: Impl $\vDash$ Property  
**Model Checking**: Impl $\vDash$ Property (Property in logic, describes behavior)
## Modal Logic
We need connectives to relate current and next states: "can drink coffee now", "cannot drink coffee now", "always can publish after drinking coffee". Modal connectives: possibility vs necessity.
## Hennessy-Milner Logic (HML)
### Syntax
$$
\varphi ::= tt \ | \ ff \ | \ \varphi \land \varphi \ | \ \varphi \lor \varphi \ | \ \langle a \rangle \varphi \ | \ [a] \varphi
$$
$tt$: true; $ff$: false  
$\land$, $\lor$: Boolean AND, OR  
$\langle a \rangle \varphi$: some $a$-successor satisfies $\varphi$  
$[a] \varphi$: all $a$-successors satisfy $\varphi$  
$\mathcal{M}$ = set of HML formulas.
## Semantics of HML
Given LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \})$, define:
$p \vDash tt$ always  
$p \vDash ff$ never  
$p \vDash \varphi \land \psi \iff p \vDash \varphi$ and $p \vDash \psi$  
$p \vDash \varphi \lor \psi \iff p \vDash \varphi$ or $p \vDash \psi$  
$p \vDash \langle a \rangle \varphi \iff \exists p'.\ p \xrightarrow{a} p' \text{ and } p' \vDash \varphi$  
$p \vDash [a] \varphi \iff \forall p'.\ p \xrightarrow{a} p' \implies p' \vDash \varphi$  
We write $p \nvDash \varphi$ if $p$ does not satisfy $\varphi$.
## Expressing Negation
Define complement $\varphi^c$:

$$
\begin{aligned}
tt^c &= ff \\
ff^c &= tt \\
(\varphi \land \psi)^c &= \varphi^c \lor \psi^c \\
(\varphi \lor \psi)^c &= \varphi^c \land \psi^c \\
\langle a \rangle \varphi^c &= [a] \varphi^c \\
[a] \varphi^c &= \langle a \rangle \varphi^c
\end{aligned}
$$
$$p \nvDash \varphi \iff p \vDash \varphi^c$$

**Example**: "cannot drink coffee now": $(\langle coffee \rangle tt)^c = [coffee] ff$
## Denotational Semantics
For formula $\varphi$, define $\langle\langle \varphi \rangle\rangle \subseteq \text{Proc}$ = states satisfying $\varphi$.
$$
\begin{aligned}
\langle\langle \langle a \rangle \varphi \rangle\rangle &= \{ p \mid \exists p'.\ p \xrightarrow{a} p' \text{ and } p' \in \langle\langle \varphi \rangle\rangle \} \\
\langle\langle [a] \varphi \rangle\rangle &= \{ p \mid \forall p'.\ p \xrightarrow{a} p' \implies p' \in \langle\langle \varphi \rangle\rangle \} \\
\langle\langle tt \rangle\rangle &= \text{Proc} \\
\langle\langle ff \rangle\rangle &= \emptyset \\
\langle\langle \varphi \land \psi \rangle\rangle &= \langle\langle \varphi \rangle\rangle \cap \langle\langle \psi \rangle\rangle \\
\langle\langle \varphi \lor \psi \rangle\rangle &= \langle\langle \varphi \rangle\rangle \cup \langle\langle \psi \rangle\rangle
\end{aligned}
$$
## Equivalence of Semantics
**Theorem**: For any $p \in \text{Proc}$ and $\varphi \in \mathcal{M}$:

$$
p \vDash \varphi \iff p \in \langle\langle \varphi \rangle\rangle
$$

Proof: by induction on $\varphi$ (Exercise 5.6).
## Hennessy-Milner Theorem
For image-finite LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \})$ and $p, q \in \text{Proc}$:
$$
p \sim q \iff \forall \varphi \in \mathcal{M}.\ (p \vDash \varphi \iff q \vDash \varphi)
$$

**Conclusion**: If $p \nsim q$, there exists a distinguishing HML formula!
## Image-finite LTS
An LTS is image-finite if:
$$
\forall p \in \text{Proc},\ \forall \alpha \in \text{Act},\ \{ p' \mid p \xrightarrow{\alpha} p' \} \text{ is finite}.
$$
Example of not image-finite:
$$
\begin{aligned}
Rep &\overset{def}{=} a.0 \ | \ Rep \\
P &\overset{def}{=} \sum_{i \geq 0} a.0
\end{aligned}
$$

<div style="page-break-after: always;"></div>
# Tarski's Fixed Point Theorem

## Verifying Correctness
Equivalence Checking: Impl $\equiv$ Spec.  
Model Checking:  Impl $\vDash$ Property.  

Given image-finite LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \})$, for $p, q \in \text{Proc}$:
$$
p \sim q \iff \forall \varphi \in \mathcal{M}.\ (p \vDash \varphi \iff q \vDash \varphi)
$$
(Hennessy-Milner Theorem)
## Can we detect deadlocks?
Let $A = \{ a_1, \dots, a_n \} \subseteq \text{Act}$:
$$
[A] \varphi = [a_1] \varphi \land \dots \land [a_n] \varphi \\
\langle A \rangle \varphi = \langle a_1 \rangle \varphi \lor \dots \lor \langle a_n \rangle \varphi
$$
"Cannot perform any move": $s \vDash \langle \text{Act} \rangle [\text{Act}] ff$  
"Reaches deadlock": $d \vDash [\text{Act}] ff$
Define:

$$
\begin{aligned}
D_0 &= [\text{Act}] ff \\
D_{n+1} &= \langle \text{Act} \rangle D_n \\
D &= \bigvee_{n \geq 0} D_n
\end{aligned}
$$
## Typical Temporal Properties (Not Expressible in HML)
Let $A = \{ a_1, \dots, a_n \} \subseteq \text{Act}$:
$$
[A] \varphi = [a_1] \varphi \land \dots \land [a_n] \varphi \\
\langle A \rangle \varphi = \langle a_1 \rangle \varphi \lor \dots \lor \langle a_n \rangle \varphi
$$
Possibility:
$$
\begin{aligned}
\text{Pos}_0(\varphi) &= \varphi \\
\text{Pos}_{n+1}(\varphi) &= \langle \text{Act} \rangle \text{Pos}_n(\varphi) \\
\text{Pos}(\varphi) &= \bigvee_{n \geq 0} \text{Pos}_n(\varphi)
\end{aligned}
$$

Invariance:
$$
\begin{aligned}
\text{Inv}_0(\varphi) &= \varphi \\
\text{Inv}_{n+1}(\varphi) &= [\text{Act}] \text{Inv}_n(\varphi) \\
\text{Inv}(\varphi) &= \bigwedge_{n \geq 0} \text{Inv}_n(\varphi)
\end{aligned}
$$
Infinite $\vee$, $\wedge$ not expressible in HML!
## Solutions of Equations
Given $\varphi, \psi \in \mathcal{M}$, write $\varphi \equiv \psi$ if:
$$
\langle\langle \varphi \rangle\rangle = \langle\langle \psi \rangle\rangle
$$
Equations:
$$
\begin{aligned}
\text{Pos}(\varphi) &\equiv \varphi \lor \langle \text{Act} \rangle \text{Pos}(\varphi) \\
\text{Inv}(\varphi) &\equiv \varphi \land [\text{Act}] \text{Inv}(\varphi)
\end{aligned}
$$
## Recursion vs Infinite $\lor$ / $\land$
Properties like Pos, Inv useful (safety, liveness). Two options:
- Extend HML with infinitary $\lor$, $\land$  
- Extend HML with recursion.
## Fixed Points
Given set $D$ and $f : D \to D$, a **fixed point** is $d \in D$ such that $d = f(d)$.
Examples:
- $D = \mathbb{N},\ f(n) = 2n$, fixed point: $0$  
- $D = 2^{\mathbb{N}},\ f(M) = M \cup N$, fixed point: $N$
## Lattice Theory
### Partial Order
A **partial order** is $(D, \sqsubseteq)$:
- Reflexive: $\forall d.\ d \sqsubseteq d$  
- Antisymmetric: $d \sqsubseteq e \land e \sqsubseteq d \Rightarrow d = e$  
- Transitive: $d \sqsubseteq e \land e \sqsubseteq f \Rightarrow d \sqsubseteq f$

Examples: $(\mathbb{N}, \leq)$, $(2^{\mathbb{N}}, \subseteq)$.
### Infimum & Supremum
Given $F \subseteq D$:
- $d$ is **lower bound** $\iff d \sqsubseteq f$ for all $f \in F$  
- $d$ is **upper bound** $\iff f \sqsubseteq d$ for all $f \in F$
**Infimum** $⊓ F$: greatest lower bound.  
**Supremum** $⊔ F$: least upper bound.
## Tarski's Fixed Point Theorem
### Complete Lattice
A partial order $(D, \sqsubseteq)$ is a **complete lattice** if $⊓ F$, $⊔ F$ exist for all $F \subseteq D$.
Example: $(2^{\mathbb{N}}, \subseteq)$ is complete; $(\mathbb{N}, \leq)$ is not.
Always has:
- Top element $\top = ⊔ D$  
- Bottom element $\bot = ⊓ D$
### Monotonic Functions
$f : D \to D$ is **monotonic** if:

$$
\forall d, e \in D,\ d \sqsubseteq e \Rightarrow f(d) \sqsubseteq f(e)
$$

Examples:
- $f(n) = 2n$ monotonic on $\mathbb{N}$  
- $F(M) = \mathbb{N} \setminus M$ not monotonic on $2^{\mathbb{N}}$
### Tarski’s Theorem
Let $(D, \sqsubseteq)$ be complete lattice, $f : D \to D$ monotonic. Then:
1. Fixed points of $f$ form a complete lattice  
2. Least and greatest fixed points exist:
$$
\begin{aligned}
\text{lfp}(f) &= ⊓ \{ d \in D \mid f(d) \sqsubseteq d \} \\
\text{gfp}(f) &= ⊔ \{ d \in D \mid d \sqsubseteq f(d) \}
\end{aligned}
$$

**Basis of many CS results!**
## Computing by Iterations
Given finite complete lattice $(D, \sqsubseteq)$, $f : D \to D$ monotonic:
Define:

$$
\begin{aligned}
f^0(d) &= d \\
f^{n+1}(d) &= f(f^n(d))
\end{aligned}
$$
Then exist $M, m \geq 0$ such that:
$$
\text{lfp}(f) = f^m(\bot), \quad \text{gfp}(f) = f^M(\top)
$$
**Sequence stabilizes in finite steps → terminating algorithm!**
Example:

$$
\bot \sqsubseteq f^1(\bot) \sqsubseteq \dots \sqsubseteq f^{m-1}(\bot) \sqsubseteq f^m(\bot) = f^{m+1}(\bot)
$$
Similarly for greatest fixed point:
$$
f^{M+1}(\top) = f^M(\top) \sqsubseteq f^{M-1}(\top) \sqsubseteq \dots \sqsubseteq f^1(\top) \sqsubseteq \top
$$



<div style="page-break-after: always;"></div>
# Hennessy-Milner Logic with Recursion

## Tarski’s Fixed Point Theorem
Let $(D, \sqsubseteq)$ be a complete lattice and $f : D \to D$ a monotonic function.
1. The set of fixed points of $f$ forms a complete lattice.  
2. The least and greatest fixed points exist:

$$
\begin{aligned}
\text{lfp}(f) &= \bigcap \{ d \in D \mid f(d) \sqsubseteq d \} \\
\text{gfp}(f) &= \bigcup \{ d \in D \mid d \sqsubseteq f(d) \}
\end{aligned}
$$
## Strong Bisimilarity
Given LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{\alpha} \})$:
A relation $R \subseteq \text{Proc} \times \text{Proc}$ is a **strong bisimulation** iff:
- If $s \xrightarrow{\alpha} s'$, then $t \xrightarrow{\alpha} t'$ with $(s', t') \in R$.  
- If $t \xrightarrow{\alpha} t'$, then $s \xrightarrow{\alpha} s'$ with $(s', t') \in R$.
$s \sim t$ iff there exists $R$ such that $s R t$.
## Fixed Point Operator
Define $\mathcal{B}(R)$:
$$(s, t) \in \mathcal{B}(R) \iff \text{bisimulation conditions hold w.r.t } R.$$
Thus:
$$
\mathcal{B} : 2^{\text{Proc} \times \text{Proc}} \to 2^{\text{Proc} \times \text{Proc}}
$$
## Bisimilarity as Fixed Point
Strong bisimilarity is the **greatest fixed point** of $\mathcal{B}$:
$$
\sim = \bigcup \{ R \mid R \subseteq \mathcal{B}(R) \} = \text{gfp}(\mathcal{B})
$$
Observations:
- $(2^{\text{Proc} \times \text{Proc}}, \subseteq)$ is a complete lattice.  
- $\mathcal{B}$ is monotonic.  
- $R$ is a strong bisimulation iff $R \subseteq \mathcal{B}(R)$.
## HML with Recursion
### Syntax

$$
\varphi ::= X \mid tt \mid ff \mid \varphi \land \varphi \mid \varphi \lor \varphi \mid \langle a \rangle \varphi \mid [a] \varphi
$$

$X \in \mathbb{X}$ is a **recursive variable**.

Each $X$ is associated with a unique equation:
- $\min X = \varphi_X$ → least fixed point  
- $\max X = \varphi_X$ → greatest fixed point
## Semantics of Variables
If $X \equiv \varphi_X$, this means:

$$
\langle\langle X \rangle\rangle = \langle\langle \varphi_X \rangle\rangle
$$
This induces an operator:
$$
\mathcal{O}_\varphi : 2^{\text{Proc}} \to 2^{\text{Proc}}
$$
Example:
$$
\varphi_X = [a] ff \lor \langle a \rangle X
$$
Then:
$$
\langle\langle X \rangle\rangle = \mathcal{O}(\langle\langle X \rangle\rangle)
$$
## Definition of $\mathcal{O}_\varphi$
For $S \subseteq \text{Proc}$:

$$
\begin{aligned}
\mathcal{O}_X(S) &= S \\
\mathcal{O}_{tt}(S) &= \text{Proc} \\
\mathcal{O}_{ff}(S) &= \emptyset \\
\mathcal{O}_{\varphi \land \psi}(S) &= \mathcal{O}_\varphi(S) \cap \mathcal{O}_\psi(S) \\
\mathcal{O}_{\varphi \lor \psi}(S) &= \mathcal{O}_\varphi(S) \cup \mathcal{O}_\psi(S) \\
\mathcal{O}_{\langle a \rangle \varphi}(S) &= \{ p \mid \exists p'.\ p \xrightarrow{a} p' \land p' \in \mathcal{O}_\varphi(S) \} \\
\mathcal{O}_{[a] \varphi}(S) &= \{ p \mid \forall p'.\ p \xrightarrow{a} p' \Rightarrow p' \in \mathcal{O}_\varphi(S) \}
\end{aligned}
$$
$\mathcal{O}_\varphi$ is monotonic.
## Semantics of Variables (via Fixed Points)

$(2^{\text{Proc}}, \subseteq)$ is a complete lattice. $\mathcal{O}_\varphi$ is monotonic. By Tarski:
- If $X = \min X$, then:
$$
\langle\langle X \rangle\rangle = \bigcap \{ S \subseteq \text{Proc} \mid \mathcal{O}_\varphi(S) \subseteq S \}
$$
- If $X = \max X$, then:
$$
\langle\langle X \rangle\rangle = \bigcup \{ S \subseteq \text{Proc} \mid S \subseteq \mathcal{O}_\varphi(S) \}
$$
## Recursive Properties
Examples:
- $\text{Pos}(\varphi): X = \varphi \lor \langle \text{Act} \rangle X$ (**possible φ**), max
- $\text{Inv}(\varphi): X = \varphi \land [\text{Act}] X$ (**invariant φ**), min
- $\text{Even}(\varphi): X = \varphi \lor (\langle \text{Act} \rangle tt \land [\text{Act}] X)$
- $\text{Safe}(\varphi): X = \varphi \land ([\text{Act}] ff \lor \langle \text{Act} \rangle X)$
Dualities:
$$
\text{Inv}(\varphi^c) = \text{Pos}(\varphi)^c \\
\text{Safe}(\varphi^c) = \text{Even}(\varphi)^c
$$
## Strong & Weak Until
- Weak Until:
$$
\varphi \mathcal{U}_w \psi: X = \psi \lor (\varphi \land [\text{Act}] X)
$$
- Strong Until:
$$
\varphi \mathcal{U}_s \psi: X = \psi \lor (\varphi \land \langle \text{Act} \rangle tt \land [\text{Act}] X)
$$
**Intuition**: φ must hold **until** ψ is reached.
## Game Characterisation
Intuition:
- **Attacker** tries to show $s \nvDash \varphi$  
- **Defender** tries to show $s \vDash \varphi$
Configurations: pairs $(s, \varphi)$.

Rules:
- $(s, tt)$ and $(s, ff)$: no successor.  
- $(s, \varphi \land \psi)$, $(s, \varphi \lor \psi)$: successors $(s, \varphi)$, $(s, \psi)$.  
- $(s, \langle a \rangle \varphi)$, $(s, [a] \varphi)$: successors $(s', \varphi)$ where $s \xrightarrow{a} s'$.  
- $(s, X)$: successor $(s, \varphi_X)$.

Moves:
- **Attacker** chooses in $(s, \varphi \land \psi)$, $(s, [a] \varphi)$.  
- **Defender** chooses in $(s, \varphi \lor \psi)$, $(s, \langle a \rangle \varphi)$.

Winning:
- **Attacker wins** if defender gets stuck or reaches $(s, ff)$.  
- **Defender wins** if attacker gets stuck or reaches $(s, tt)$.

**Semantics via game**:
$$
s \vDash \varphi \iff \text{defender has a universal winning strategy from } (s, \varphi)
$$
## More than One Variable
Example:
$$
\begin{aligned}
X &= Y \lor \langle \text{Act} \rangle X \\
Y &= \langle a \rangle tt \land \langle \text{Act} \rangle Y
\end{aligned}
$$
Compute $\langle\langle Y \rangle\rangle$ first, then $\langle\langle X \rangle\rangle$.
## Nested Definitions
Example:
$$
\begin{aligned}
X &= [a] Y \\
Y &= \langle a \rangle X
\end{aligned}
$$
Now we must work in lattice $(2^{\text{Proc}} \times 2^{\text{Proc}}, \sqsubseteq)$:
$$(S, S') \sqsubseteq (Q, Q') \iff S \subseteq Q \land S' \subseteq Q'$$
## Mutual Recursion
In general:
$$
\begin{aligned}
X_1 &= \varphi_1 \\
\vdots \\
X_n &= \varphi_n
\end{aligned}
$$
Define:
$$
\mathcal{O}_D(S_1, \dots, S_n) = (\mathcal{O}_{\varphi_1}(S_1, \dots, S_n), \dots, \mathcal{O}_{\varphi_n}(S_1, \dots, S_n))
$$
## Characteristic Property
Once we have recursion and mutual recursion, we can express **characteristic formulas**:
For finite LTS $(\text{Proc}, \text{Act}, \{ \xrightarrow{a} \})$ and $s \in \text{Proc}$:
$$
X_s = \langle a \rangle X_t \land [a] X_t
$$

This is the **characteristic formula** for $s$:
$$
t \vDash X_s \iff t \sim s
$$
(Theorem: **Characteristic Formula**.)
<div style="page-break-after: always;"></div>

# Peterson's algorithm

## Overview
Goal: Verify a CCS model of a **mutual exclusion** algorithm.
Techniques:
- Verification using **HML with recursion**  
- Verification using **behavioral equivalences**  
- Model checking (with tools like CAAL)
- 

---

## Peterson’s Mutual Exclusion Algorithm
Pseudocode for process $i$:

```
while true do
  non-critical section
  b_i := true
  k := j
  while b_j ∧ k = j do skip
  critical section
  b_i := false
end while
```

- $b_1$, $b_2$, $k$ are **shared variables**  
- $b_i = true$ means process $i$ is trying to enter critical section  
- Initially: $b_1 = b_2 = false$  
- $k$ is the ID of the process in critical section  

---
## CCS Modeling
### Modeling Strategy
1. **Processes**: $P_1$ and $P_2$  
2. **Variables**: modeled as **passive agents** with read/write actions  
3. **Communication**: through reads/writes on variables (no direct P1–P2 communication)  
4. **Composition**: parallel composition + restriction

---
### Boolean Variables
For each $b_i$:

$$
\begin{aligned}
B_i^f &\overset{def}{=} b_irf.B_i^f + b_iwf.B_i^f + b_iwt.B_i^t \\
B_i^t &\overset{def}{=} b_irt.B_i^t + b_iwf.B_i^f + b_iwt.B_i^t
\end{aligned}
$$

- $rf$: read false  
- $rt$: read true  
- $wf$: write false  
- $wt$: write true

---
### The Turn Variable $k$
Possible values: $1$ and $2$ → modeled as $K_1$, $K_2$:

$$
\begin{aligned}
K_1 &\overset{def}{=} kr1.K_1 + kw1.K_1 + kw2.K_2 \\
K_2 &\overset{def}{=} kr2.K_2 + kw1.K_1 + kw2.K_2
\end{aligned}
$$

---
### Process 1 ($P_1$)

$$
\begin{aligned}
P_1 &\overset{def}{=} b1wt.kw2.P_{11} \\
P_{11} &\overset{def}{=} b2rf.P_{12} + b2rt.(kr2.P_{11} + kr1.P_{12}) \\
P_{12} &\overset{def}{=} enter1.exit1.b1wf.P_1
\end{aligned}
$$

---


$$
\begin{aligned}
P_2 &\overset{def}{=} b2wt.kw1.P_{21} \\
P_{21} &\overset{def}{=} b1rf.P_{22} + b1rt.(kr1.P_{21} + kr2.P_{22}) \\
P_{22} &\overset{def}{=} enter2.exit2.b2wf.P_2
\end{aligned}
$$

---

## Full System: Peterson
$$
\text{Peterson} \overset{def}{=} (B1^f \ | \ B2^f \ | \ K_1 \ | \ P_1 \ | \ P_2) \setminus L
$$

Where:
$$
L = \{ b1rf, b1rt, b1wf, b1wt, b2rf, b2rt, b2wf, b2wt, kr1, kw1, kr2, kw2 \}
$$
---
## Verification Goals
### Informal Safety Property
**Mutual exclusion**: $P_1$ and $P_2$ should **never be in critical sections at the same time**.

---
### HML with Recursion
Define invariant:
$$
\text{Inv} \overset{max}{=} F \land [\text{Act}] \ \text{Inv}
$$

Where:
$$
F = [exit1]ff \lor [exit2]ff
$$
**Interpretation**: one of the exits must be reachable — both cannot stay in critical section.
Result: **Peterson $\vDash$ Inv**.

---
### Verification via Behavioral Equivalences

---
#### Strong Bisimulation
Candidate spec:
$$
\text{MutexSpec} \overset{def}{=} enter1.exit1.\text{MutexSpec} + enter2.exit2.\text{MutexSpec}
$$
Question: Is $\text{Peterson} \sim \text{MutexSpec}$?
**Result**: No — attacker can show mismatch using game characterisation.

---

#### Weak Bisimulation
Same spec:
$$
\text{MutexSpec} \overset{def}{=} enter1.exit1.\text{MutexSpec} + enter2.exit2.\text{MutexSpec}
$$

Is $\text{Peterson} \approx \text{MutexSpec}$?
**Result**: No — again a mismatch exists.

---
#### Trace Equivalence
**Result**:
- **Peterson is NOT strongly trace equivalent** to MutexSpec.  
- But **Peterson IS weakly trace equivalent** to MutexSpec.
---
## Summary of Findings

| Method                 | Result |
| ---------------------- | ------ |
| HML with recursion     | Pass   |
| Strong bisimulation    | Fail   |
| Weak bisimulation      | Fail   |
| Weak trace equivalence | Pass   |

---
**Conclusion**: Using **HML with recursion**, we can verify the core safety property of Peterson’s algorithm, even though bisimilarity does not hold.
<div style="page-break-after: always;"></div>

# Timed Automata
## 1. Timed Labelled Transition Systems (TLTS)

A **TLTS** is a triple:
$$
(\text{Proc}, \text{Act}, \{ \xrightarrow{a} \mid a \in \text{Act} \})
$$
where:
- $\text{Proc}$ = set of **states**  
- $\text{Act} = \mathbb{N} \cup \mathbb{R}^{\geq 0}$ = set of **actions**:
    - $\mathbb{N}$ = labels (discrete actions)  
    - $\mathbb{R}^{\geq 0}$ = **time-elapsing steps**
- For each $a \in \text{Act}$:  
    $\xrightarrow{a} \subseteq \text{Proc} \times \text{Proc}$ = **transition relation**
### Notation:
- $s \xrightarrow{a} s'$ if $a \in \mathbb{N}$  
- $s \xrightarrow{d} s'$ if $d \in \mathbb{R}^{\geq 0}$
### TLTS Requirements:
- **Time determinism**  
- **Maximal progress**  
- **Time additivity**  
- **Non-zenoness** (no infinite $\tau$-loops w/o time passing)

---
## 2. Timed CCS (TCCS)
### Idea:
- **CCS + delays**  
- Adds **delay prefix** $\epsilon . P$
### Syntax:
$$
P ::= 0 \mid a.P \mid \epsilon . P \mid P + Q \mid P \ | \ Q \mid P \setminus L \mid P[f]
$$
### Semantics (SOS):
- **Action transitions**: $s \xrightarrow{a} s'$  
- **Delay transitions**: $s \xrightarrow{d} s'$  
    - Time can pass **only if no urgent actions enabled**  
    - Parallel delay: both components must allow same delay


![[Pasted image 20250609160738.png]]

---
## 3. Parallel Composition in TCCS
### Delay rule:
$$
\text{If} \quad P \xrightarrow{d} P' \ \text{and} \ Q \xrightarrow{d} Q' \quad \Rightarrow \quad P \ | \ Q \xrightarrow{d} P' \ | \ Q'
$$
- **Synchronization of delays** in parallel.



---
## 4. Timed Automata (TA)
### Key idea:
- Finite automata + **clocks** $\{x, y, ...\}$  
- Clocks are **real-valued** and increase with time.
### Components:
- **Locations**  
- **Transitions**: $(\ell, g, a, r, \ell')$:
    - $g$ = **guard** (clock constraint)
    - $r$ = **reset set** (which clocks reset)  
- **Invariants** on locations
### State = $(\ell, v)$:
- $\ell$ = location  
- $v$ = clock valuation
### Semantics:
- **Delay transitions**: time passes (clocks advance)  
- **Action transitions**: guard satisfied $\Rightarrow$ take transition + reset clocks.

---
## 5. Light Switch Example (TCCS)
$$
\text{Switch} = \epsilon . on . \text{Switch} + \epsilon . off . \text{Switch}
$$

---
## 6. Dumb Light Controller (TA)
- Turns **on/off** with timeouts.
- Simple **TA** model.

---
## 7. Intelligent Light Controller (TA)
- **User activity** resets a clock.
- Light turns **off** after **timeout** if no activity.

---
## 8. Tool Support: UPPAAL
- **UPPAAL** supports:
    - **modeling** TA  
    - **simulation**  
    - **model checking** (safety, liveness)  

---
## 9. Summary: CCS vs TCCS vs TA

| Concept  | CCS | TCCS          | TA                    |
|----------|-----|---------------|----------------------|
| Time     | No  | Delays ($\epsilon . P$) | Clocks + constraints |
| Parallel Time | N/A | Synchronized delays | Yes |
| Tool     | CAAL | UPPAAL-TIGA | UPPAAL |

---

## 10. For Exam: What to Remember

### TLTS:
- $(\text{Proc}, \text{Act}, \xrightarrow{a})$  
- $\text{Act} = \mathbb{N} \cup \mathbb{R}^{\geq 0}$  
- Time transitions + action transitions
### TCCS:
- **Adds $\epsilon . P$**  
- **Time cannot bypass urgent actions**  
- Delays **synchronize** in parallel
### TA:
- **Clocks**  
- **Guards**, **resets**, **invariants**  
- Real-time model  
- **Verification with UPPAAL**

<div style="page-break-after: always;"></div>

# Train-Gate and Gossiping Girls Protocol

---

## 1️⃣ Train-Gate (Exercise 3)

---

### Model Overview

- **Processes**: $N$ trains ($N=6$), 1 gate.
- **Goal**: Only 1 train on crossing at any time (mutual exclusion).
- **Communication**:
    - `appr[id]! / appr[id]?` — Train approaches.
    - `stop[id]! / stop[id]?` — Gate stops a train.
    - `go[id]! / go[id]?` — Gate allows a train to go.
    - `leave[id]! / leave[id]?` — Train leaves crossing.

---

### Train Template

- **Locations**:
    - `Safe` → `Appr` (approaching)
    - `Appr` → `Cross` (crossing) OR → `Stop`
    - `Stop` → `Start` → `Cross`
    - `Cross` → `Safe`
- **Clock $x$** used for timing:
    - Max approach time: $x \leq 20$
    - Crossing invariant: $x \leq 5$
    - Other guards: $x \geq 10$, $x \geq 3$, etc.

---

### Gate Template

- **Queue** of trains implemented via `list[N+1]`, `len`.
- **Locations**: `Free`, `Occ`, `Committed`
- **Queue operations**:
    - `enqueue(e)`  
    - `dequeue()`
    - `front()`, `tail()`

- **Behavior**:
    - On `appr[e]?` → enqueue.
    - On `leave[e]?` → dequeue.
    - If `len > 0` → send `go[front()]!`
    - If occupied → send `stop[tail()]!`

---

### Errors (Part a)

Using UPPAAL (simulation or verification):

- **Problem**: Potential mismatch between Gate queue and train state:
    - Gate may send **`go`** to train not currently stopped → wrong transition.
    - Gate may send **`stop`** when not needed → extra waiting.

- **Cause**: Misaligned use of `tail()` in `stop`, vs `front()` in `go`.

---

### Corrected Behavior

- Align `stop` and `go` logic with queue ordering.
- Ensure gate does not send `stop` when `len == 0`.
- Synchronize correctly when first train leaves.

---

### Timing Questions

**(b) Min time from request → crossing**:

- Fastest path: `Safe → Appr → Cross`:
    - Appr: guard `x \geq 10`
    - Cross: after `x=0` → can enter Cross.

**Answer**: ~10 time units minimum.

---

**(c) Min waiting time (Stop → permission to go)**:

- After Stop → Start:
    - Transition on `go[id]?` resets $x=0$.
    - Guard allows immediate transition when Gate sends `go`.

**Answer**: 0 time units (if Gate responds immediately).

---

### 2️⃣ Gossiping Girls Protocol

---

## Problem

- **N=4 girls** initially each know 1 secret.
- **Calls** between pairs exchange all known secrets.
- **Scenarios**:
    - 1: Chain topology (neighbors only).
    - 2: Full topology (any girl can call any other).

---

### Model (UPPAAL)

- **Global**:
    - `N=4`
    - `broadcast chan call[N]`
    - `bool tmp[N]`, `clock time`

- **Girl Template**:

    - Local:
        - `bool secrets[N]` — which secrets the girl knows.
        - Clock `x`.

    - Functions:
        - `start()`: initialize girl’s own secret.
        - `talk()`: copy secrets to `tmp`.
        - `exchange()`: update `tmp` with new secrets.
        - `listen()`: receive updated `tmp`.

---

### Girl Behavior

- **Locations**:
    - `Idle` (waiting, $x \leq 60$)
    - `Ready` (can initiate call)
    - `Listen` (receive secrets)
    - Init → `Idle` (via `start()`)

- **Transitions**:

    - Ready → Idle (after call received)
    - Ready → Listen → Idle
    - After $x \geq 60$ → Ready
    - Calls last **exactly 60 seconds**.

---

## Scenarios

**Scenario 1**: Linear chain  
**Scenario 2**: Full graph  
(Optional: Circular, Single-call-at-a-time)

---

### Minimal Number of Calls

### Scenario 1:

- Min calls = $2(N - 1) = 6$ for $N=4$

### Scenario 2:

- Min calls = $\lceil \log_2 N \rceil + 1 = 3$

---

### Minimum Time (calls take 60 sec)

### Scenario 1:

- Sequential → $6 \times 60 = 360$ sec

### Scenario 2:

- Parallel → can finish in **180 sec** (if calls are parallelized optimally).

---

### Search Options (Part of Experiment)

- Tried: BFS, DFS, random DFS
- Diagnostic trace: fastest / shortest
- For $N=5$: more complex, but feasible with BFS + optimized topology.

---

### Message Sequence Chart (MSC)

- MSC clearly shows **who calls whom**, in which order.

---

### Summary of Experience

- **Modeling**: Easy to represent as UPPAAL **network of automata**.
- **Key challenge**: Encoding **topology** (adjacency).
- **Observation**: Parallelism in Scenario 2 greatly reduces total time.
- UPPAAL **trace visualization** (MSC) very helpful for understanding.

---

### Final Summary

| Problem            | Key Concept                        |
| ------------------ | ---------------------------------- |
| Train-Gate         | Mutual exclusion via queue; timing |
| Gossiping Girls    | Knowledge propagation; parallelism |
| Region Graph       | Finite abstraction of TA           |
| Clock Valuation    | Tracks delays & guards             |
| Timed Bisimilarity | Match actions & exact delays       |
|                    |                                    |
<div style="page-break-after: always;"></div>

# 1️⃣ Transition Systems and CCS
*(Exam Question 1)*

### 4 bullets:
1. Labelled Transition System (LTS)
2. CCS Syntax and Semantics
3. Parallel Composition and Restriction
4. Example: Coffee Machine & Server

---

### 1️⃣ Labelled Transition System (LTS)

An LTS models behavior using states and actions.

**Definition**:  
An LTS is a triple $(\text{Proc}, \text{Act}, \{ \xrightarrow{a} \})$, where:
- $\text{Proc}$ is the set of states (or processes).
- $\text{Act}$ is the set of actions (e.g., $a$, $\tau$, $\text{coin}$).
- $\xrightarrow{a} \subseteq \text{Proc} \times \text{Proc}$ is the transition relation.

Extended notation: $p \xrightarrow{w} p'$ means $p$ can reach $p'$ through a sequence $w$ of actions.

---

### 2️⃣ CCS Syntax and Semantics

CCS models concurrent systems using algebraic process expressions.

**Syntax**:
$$
P ::= a.P \mid P + Q \mid P \mid Q \mid P \setminus L \mid P[f] \mid 0
$$

- $a.P$: do action $a$, then behave like $P$.
- $P + Q$: nondeterministic choice.
- $P \mid Q$: parallel composition.
- $P \setminus L$: restrict $L$ (actions become internal).
- $P[f]$: relabel actions via function $f$.
- $0$: the nil process (does nothing).

Semantics is defined using Structural Operational Semantics (SOS rules).

---

### 3️⃣ Parallel Composition and Restriction

- $P \mid Q$: processes run concurrently. If $P$ does $a$ and $Q$ does $\overline{a}$, they synchronize into $\tau$.
- $P \setminus \{a\}$: hides action $a$ from the environment; it becomes internal.

---

### 4️⃣ Example: Coffee Machine & Server

Let:
$$
CM = \overline{coin}.coffee.CM \\
CS = \overline{pub}.\overline{coin}.coffee.CS
$$

System:
$$
(CM \mid CS) \setminus \{coin, coffee\}
$$

- Only action $\text{pub}$ is visible externally.
- Synchronization happens on $\text{coin}$ and $\text{coffee}$ internally.

---
<div style="page-break-after: always;"></div>
# 2️⃣ Strong & Weak Bisimilarity, Bisimulation Games
*(Exam Question 2)*

### 4 bullets:
1. Strong Bisimilarity
2. Weak Bisimilarity
3. Bisimulation Games
4. Practical Example: Buffers

---

### 1️⃣ Strong Bisimilarity

Processes $p$ and $q$ are **strongly bisimilar** if they can match each other's transitions **exactly**.

Let $R \subseteq \text{Proc} \times \text{Proc}$ be a relation.

**$R$ is a strong bisimulation** iff:
- If $(p, q) \in R$ and $p \xrightarrow{a} p'$, then $\exists q'$ such that $q \xrightarrow{a} q'$ and $(p', q') \in R$, and vice versa.

**Notation**: $p \sim q$ means they are strongly bisimilar.

---

### 2️⃣ Weak Bisimilarity

We allow abstraction over $\tau$ (silent) actions.

Define the **weak transition**:
- $p \Rightarrow_a p'$ means $p$ can reach $p'$ via zero or more $\tau$, then $a$, then more $\tau$.

A relation $R$ is a **weak bisimulation** iff:
- $(p, q) \in R \Rightarrow$ for all $a$, transitions in $p$ can be weakly matched in $q$, and vice versa.

---

### 3️⃣ Bisimulation Games

Two players:
- **Attacker** chooses a transition in one process.
- **Defender** must match it in the other.

Defender **loses** if they can't match → processes not bisimilar.

This provides a **proof method** for non-bisimilarity.

---

### 4️⃣ Example: Buffers

Example: show that a 2-slot buffer $B_{0,2}$ is not bisimilar to $B_{0,1} \mid B_{0,1}$.

- Use a game: force a transition that one system can't match.

---
<div style="page-break-after: always;"></div>
# 3️⃣ Hennessy-Milner Logic and Bisimulation
*(Exam Question 3)*
### 4 bullets:
1. Syntax & Semantics
2. Hennessy-Milner Theorem
3. Expressing Properties
4. Characteristic Formulas

---

### 1️⃣ Syntax & Semantics

Formulas:
$$
\varphi ::= tt \mid ff \mid \varphi \land \psi \mid \varphi \lor \psi \mid \langle a \rangle \varphi \mid [a]\varphi
$$

- $\langle a \rangle \varphi$: there exists an $a$-successor satisfying $\varphi$.
- $[a] \varphi$: all $a$-successors satisfy $\varphi$.

Negation is expressed via complements: $\varphi^c$.

---

### 2️⃣ Hennessy-Milner Theorem

For **image-finite LTS**:

$$
p \sim q \iff \forall \varphi.\ p \models \varphi \iff q \models \varphi
$$

That is, **logical equivalence = strong bisimilarity**.

---

### 3️⃣ Expressing Properties

Examples:
- **Deadlock**: $[Act]\ ff$
- **Possibility (some action)**: $\langle Act \rangle tt$
- **Invariance**: $[Act]\varphi$

---

### 4️⃣ Characteristic Formulas

For any state $p$, we can construct $\varphi_p$ such that:

$$
q \models \varphi_p \iff q \sim p
$$

Used in model checking to decide bisimilarity logically.

---

<div style="page-break-after: always;"></div>
# 4️⃣ Tarski's Theorem & Recursion in HML
*(Exam Question 4)*

### 4 bullets:
1. Complete Lattices and Monotonicity
2. Tarski’s Theorem
3. Recursion in HML
4. Fixed Point Examples (Pos, Inv, Until)

---

### 1️⃣ Complete Lattices and Monotonicity

- A **partial order** $(D, \sqsubseteq)$ has:
  - Reflexivity, Antisymmetry, Transitivity.
- A **complete lattice** means:
  - Every subset $S \subseteq D$ has:
    - Least upper bound $\bigsqcup S$
    - Greatest lower bound $⊓ S$

A function $f: D \to D$ is **monotonic** if:
$$
d \sqsubseteq e \Rightarrow f(d) \sqsubseteq f(e)
$$

---

### 2️⃣ Tarski’s Fixed Point Theorem

Let $(D, \sqsubseteq)$ be a complete lattice and $f: D \to D$ monotonic.

Then:
- The set of fixed points of $f$ is a complete lattice.
- The **least fixed point** is:
$$
lfp(f) = ⊓ \{ d \in D \mid f(d) \sqsubseteq d \}
$$
- The **greatest fixed point** is:
$$
gfp(f) = \bigsqcup \{ d \in D \mid d \sqsubseteq f(d) \}
$$

---

### 3️⃣ Recursion in HML

We add recursion via fixed-point variables:
- $\min X = \varphi_X$ means $X$ is defined by least fixed point of $\varphi_X$
- $\max X = \varphi_X$ means greatest fixed point.

Define the **operator** $\mathcal{O}_\varphi: 2^{Proc} \to 2^{Proc}$ recursively:

$$
\mathcal{O}_X(S) = S \\
\mathcal{O}_{tt}(S) = Proc \\
\mathcal{O}_{ff}(S) = \emptyset
$$

And for modal operators:
$$
\mathcal{O}_{\langle a \rangle \varphi}(S) = \{ p \mid \exists p'.\ p \xrightarrow{a} p' \land p' \in \mathcal{O}_\varphi(S) \} \\
$$
 $$\mathcal{O}_{[a] \varphi}(S) = \{ p \mid \forall p'.\ p \xrightarrow{a} p' \Rightarrow p' \in \mathcal{O}_\varphi(S) \}$$

---

### 4️⃣ Fixed Point Examples

- **Eventually (Possibility)**:
$$
Pos(\varphi) = \max X. \varphi \lor \langle Act \rangle X
$$

- **Always (Invariance)**:
$$
Inv(\varphi) = \min X. \varphi \land [Act]X
$$

- **Until (Strong)**:
$$
X = \psi \lor (\varphi \land \langle Act \rangle tt \land [Act]X)
$$

- **Until (Weak)**:
$$
X = \psi \lor (\varphi \land [Act]X)
$$

<div style="page-break-after: always;"></div>
# 5️⃣ Peterson’s Algorithm and HML Verification
*(Exam Question 5)*

### 4 bullets:
1. Mutual Exclusion Problem
2. Modeling Variables and Processes in CCS
3. HML Verification
4. Summary of Results

---

### 1️⃣ Mutual Exclusion Problem

Goal: Ensure two processes never enter the **critical section** at the same time.

Uses:
- Boolean flags $b_1$, $b_2$
- Shared variable $k$ (whose turn is it?)

Each process sets its flag, sets $k$ to the other process, then waits.

---

### 2️⃣ Modeling in CCS

**Boolean variables and turn** are modeled as **independent processes**.

Example:
$$
B_1^f = b1rf.B_1^f + b1wf.B_1^f + b1wt.B_1^t
$$

- $b1rf$: read flag as false.
- $b1wt$: write flag true.

Processes:
$$
P_1 = b1wt.kwt2.b2rf.krt1.enter1.exit1.P_1
$$

Full system:
$$
Peterson = (B_1^f \mid B_2^f \mid K_1 \mid P_1 \mid P_2) \setminus L
$$

where $L$ includes all shared variable actions.

---

### 3️⃣ HML Verification

Goal: verify **mutual exclusion** using HML.

Property: "Never both in critical section":
$$
A[]\ \neg (P_1\ in\ CS \land P_2\ in\ CS)
$$

HML formulation:
$$
Inv = \max X. F \land [Act]X
$$

Where $F$ encodes: **at least one exit is enabled**.

Use fixed-point logic because **invariance = gfp**.

---

### 4️⃣ Summary of Results

| Method               | Result |
|----------------------|--------|
| HML with recursion   | ✅     |
| Strong bisimilarity  | ❌     |
| Weak bisimilarity    | ❌     |
| Trace equivalence    | ✅     |

Conclusion: algorithm is **correct**, but **not strongly bisimilar** to ideal.

---
<div style="page-break-after: always;"></div>
# 6️⃣ Timed CCS and Timed Bisimilarity
*(Exam Question 6)*

### 4 bullets:
1. Timed LTS (TLTS)
2. Timed CCS (TCCS)
3. Timed Bisimilarity
4. Example: Timed Light

---

### 1️⃣ Timed LTS (TLTS)

A **Timed LTS** extends LTS with **real-valued time**.

Let:
$$
\text{Act} = \Sigma \cup \mathbb{R}_{\geq 0}
$$

- Actions: $\Sigma$ are discrete events.
- Time delays: $d \in \mathbb{R}_{\geq 0}$.

Properties:
- **Time determinism**: time always passes the same.
- **Maximal progress**: urgent actions happen before time passes.
- **Non-zenoness**: time must eventually progress.

---

### 2️⃣ Timed CCS (TCCS)

Add **delay prefix** to CCS:
$$
\epsilon . P
$$

This means: "wait $d$ units, then behave as $P$".

Delay synchronization:
If $P \xrightarrow{d} P'$ and $Q \xrightarrow{d} Q'$, then:
$$
P \mid Q \xrightarrow{d} P' \mid Q'
$$

---

### 3️⃣ Timed Bisimilarity

Processes $P$ and $Q$ are **timed bisimilar** if:
- $P \xrightarrow{a} P'$ implies $Q \xrightarrow{a} Q'$ and vice versa.
- $P \xrightarrow{d} P'$ implies $Q \xrightarrow{d} Q'$ and vice versa.

So: both **actions** and **delays** must be matched **quantitatively**.

---

### 4️⃣ Example: Timed Light Switch

$$
Light = \epsilon . on . Light + \epsilon . off . Light
$$

Also models:
- **Timeout**: $\epsilon^{10}.off$
- **User activity** resets clock.

**Timed bisimilarity** ensures **behavior + time** is identical.

--- 
<div style="page-break-after: always;"></div>
# 7️⃣ Timed Automata, Clock Valuations & Region Graph
*(Exam Question 7)*

### 4 bullets:
1. Timed Automata (TA)
2. Clock Valuations
3. Region Graph Abstraction
4. Timed Bisimilarity

---

### 1️⃣ Timed Automata (TA)

Timed automata = finite automata + clocks.

Transition:
$$
(\ell, g, a, r, \ell')
$$

- $\ell$ = location (state)
- $g$ = guard (clock constraint)
- $a$ = action
- $r$ = reset set (clocks to reset)
- $\ell'$ = target location

Locations may have **invariants** (e.g., $x \leq 10$).

---

### 2️⃣ Clock Valuations

Clocks map to time:
$$
v: C \to \mathbb{R}_{\geq 0}
$$

- Time delay: $v + d$ increases all clocks by $d$.
- After a transition, clocks in reset set $r$ are set to 0.

Guards: boolean constraints like $x \leq 5$, $x \geq 2$.

---

### 3️⃣ Region Graph Abstraction

Infinite time space → **finite** abstraction.

A **region** groups all clock valuations that:
- Satisfy the same set of guards.
- Have the same integer/fractional relationship.

**Region graph**:
- Finite quotient of state space.
- Enables model checking of TAs.

---

### 4️⃣ Timed Bisimilarity

Two states are **timed bisimilar** if:
- They can match actions.
- And match exact **delays**.

Useful for:
- Checking if two TAs behave the same.
- Formal reasoning about timing.

---
<div style="page-break-after: always;"></div>
# 8️⃣ UPPAAL: Modeling & Verification
*(Exam Question 8)*

### 4 bullets:
1. UPPAAL Basics
2. Train-Gate Example
3. Gossiping Girls Problem
4. Analysis Techniques

---

### 1️⃣ UPPAAL Basics

UPPAAL = model checker for **Timed Automata Networks**.

Features:
- **Clocks**: real-valued time.
- **Synchronization**: via channels (urgent, broadcast).
- **Variables**: like C.
- Queries:
    - Safety: $A[]\ \text{not deadlock}$
    - Liveness: $E<>\ \text{goal}$

---

### 2️⃣ Train-Gate Example

Goal: only **one train on bridge** at a time.

- Each **Train** process:
    - Safe → Appr → Cross → Safe
    - Has a local clock $x$
    - Invariants like $x \leq 20$ in Appr

- **Gate** process:
    - Maintains queue of arriving trains.
    - Uses `enqueue()` and `dequeue()` in C-code.
    - Sends `go[id]!` to let train cross.

Verified:
- Mutual exclusion: one train on bridge.
- Liveness: trains eventually cross.
- Timing bounds: minimum/maximum wait times.

---

### 3️⃣ Gossiping Girls Problem

Goal: all girls eventually know all secrets.

- Each **Girl** has:
    - Local secrets array.
    - `call[id]!` and `call[id]?` to synchronize.
    - 60s duration per call.

Topologies:
- Scenario 1: linear chain.
- Scenario 2: full graph.
- Scenario 3: circle.
- Scenario 4: single call allowed at once.

Verified:
- Number of calls.
- Time needed.
- Liveness.

---

### 4️⃣ Analysis Techniques

Used:
- **Search strategies**: BFS, DFS, Random DFS.
- **Diagnostic traces**: fastest vs shortest.
- **Message Sequence Charts (MSC)** to visualize communication.

Takeaways:
- Topology has **huge impact**.
- Traces help understand bugs.
- UPPAAL scales to ~5 participants in real-time models.

---

<div style="page-break-after: always;"></div>
# Practice Text 1️⃣ Transition Systems and CCS

I will talk about Labelled Transition Systems and CCS.

A Labelled Transition System, or LTS, consists of a set of states, a set of actions, and a transition relation for each action. The transitions describe how the system can move between states by performing actions. We can also define paths as sequences of actions, and use reflexive-transitive closure to describe reachability.

CCS, or Calculus of Communicating Systems, is a language to model processes that interact. Each process has a name, an interface, and a behavior. The main operators are:
- prefixing: $a.P$ performs $a$, then behaves as $P$,
- choice: $P + Q$ behaves as either $P$ or $Q$,
- parallel composition: $P | Q$ allows $P$ and $Q$ to interact,
- restriction: $(P | Q) \setminus L$ hides actions,
- relabelling: $P[f]$ renames actions.

Using CCS we can model concurrent systems with synchronous communication. The semantics of CCS is given by an LTS where states are CCS processes and transitions are defined by structural operational semantics.

---

# Practice Text 2️⃣ Strong and Weak Bisimilarity

I will explain strong and weak bisimilarity and bisimulation games.

Strong bisimilarity compares processes step-by-step. Two processes are strongly bisimilar if they can match each other’s actions exactly, including internal actions. A relation $R$ is a strong bisimulation if for every action, both processes can simulate each other, staying within $R$.

Weak bisimilarity abstracts from internal actions (τ). In weak bisimulation, we allow matching sequences of τ-actions with a single τ-step. The matching condition uses weak transitions $\Rightarrow$. This allows us to compare processes while ignoring internal computation.

Bisimulation games help prove or disprove bisimilarity. The attacker tries to find a mismatch, while the defender tries to match every move. If the defender always has a strategy to match moves, the processes are bisimilar.

---

# Practice Text 3️⃣ Hennessy-Milner Logic and Bisimulation

I will present Hennessy-Milner Logic and its relation to bisimulation.

Hennessy-Milner Logic, or HML, is a modal logic to express properties of processes. The formulas include:
- $\langle a \rangle \varphi$: there exists an $a$-transition to a state satisfying $\varphi$,
- $[a] \varphi$: all $a$-transitions lead to states satisfying $\varphi$.

The semantics of HML is defined over an LTS. A key result is the Hennessy-Milner theorem: for image-finite LTS, two states are strongly bisimilar if and only if they satisfy the same HML formulas.

Thus, HML provides a logical characterization of bisimilarity. If we can find a formula that distinguishes two states, they are not bisimilar.

---

# Practice Text 4️⃣ Tarski’s Fixed-Point Theorem and HML with Recursion

I will explain Tarski’s Fixed Point Theorem and its application to HML with recursion.

Tarski’s theorem says that for any monotonic function on a complete lattice, least and greatest fixed points exist. In process verification, this lets us define properties as fixed points.

HML with recursion introduces variables with recursive definitions, such as:
$$
X = \varphi \lor \langle Act \rangle X
$$
This defines the property "eventually $\varphi$ holds."

The semantics is defined using Tarski’s theorem: the interpretation of $X$ is the least or greatest fixed point of the corresponding operator.

This enables us to express properties like safety, liveness, and until properties, which require recursion to define.

---

# Practice Text 5️⃣ Peterson’s Algorithm

I will talk about verifying Peterson’s mutual exclusion algorithm.

Peterson’s algorithm ensures that two processes cannot be in their critical section at the same time. It uses shared flags and a turn variable.

In CCS, we model each flag and turn as passive agents, with read and write actions. Each process performs reads and writes to coordinate entry to its critical section.

We verify the model using HML with recursion:
$$
Inv = \max X. F \land [Act] X
$$
which expresses mutual exclusion.

Using bisimilarity, Peterson’s system is not strongly bisimilar to an ideal specification but does satisfy the safety property. Trace equivalence also holds weakly.

---

# Practice Text 6️⃣ Timed CCS and Timed Bisimilarity

I will present Timed CCS and Timed Bisimilarity.

Timed CCS extends CCS with delays. We add the prefix $\epsilon . P$, meaning after some time delay, the process behaves as $P$.

The semantics is given by a Timed LTS, where actions include discrete actions and real-valued time delays.

Timed bisimilarity requires that two processes match both discrete actions and exact time delays. This is stricter than weak bisimilarity, since delays must match quantitatively.

For example, a light controller can be modeled in TCCS to turn off after a timeout. Timed bisimilarity ensures that two versions of the controller behave the same in terms of both actions and timing.

---

# Practice Text 7️⃣ Timed Automata

I will explain Timed Automata.

A Timed Automaton is a finite automaton with real-valued clocks. Clocks increase with time and can be reset on transitions.

Transitions are labeled with guards and resets:
$$
(\ell, g, a, r, \ell')
$$
Guards restrict when a transition is enabled, based on clock values.

The semantics uses clock valuations: functions mapping each clock to its current value. Time can pass if location invariants allow it.

To verify Timed Automata, we use region graphs, a finite abstraction of the infinite state space. Regions group valuations that behave equivalently.

Timed bisimilarity in TA matches both discrete actions and precise time delays, ensuring exact quantitative equivalence between automata.

---

# Practice Text 8️⃣ UPPAAL Train-Gate and Gossiping Girls

I will present two UPPAAL models: Train-Gate and Gossiping Girls.

In Train-Gate, multiple trains want to cross a bridge. The gate controls access to ensure mutual exclusion. Trains synchronize with the gate using channels like `appr`, `stop`, `go`, and `leave`.

The Train automaton uses a clock to model timing of approach and crossing. The Gate uses a queue to manage waiting trains.

We verify mutual exclusion, liveness, and absence of deadlocks.

In Gossiping Girls, each girl initially knows one secret. When two girls call each other, they exchange all known secrets.

The Girl automaton uses a clock to model call duration. Calls last exactly 60 seconds.

In Scenario 1 (chain), only neighbors can call. In Scenario 2 (full graph), any pair can call. We analyze the minimum number of calls and time needed for all secrets to spread.

UPPAAL provides powerful tools: simulation, trace visualization, and model checking to verify such systems.

---
---

## Practice Text 5️⃣: Peterson’s Algorithm and Its Verification

Peterson’s algorithm is a classical solution to the **mutual exclusion problem** for two processes.

It ensures:
1. **Safety**: At most one process is in the critical section (CS).
2. **Liveness**: If a process wants to enter CS, it eventually does.

Each process has:
- A boolean flag $b_i$ indicating interest in the CS.
- A shared variable `turn` that gives priority to the other process.

Process $P_i$:
1. Sets $b_i := true$.
2. Sets `turn := j`.
3. Waits until either $b_j = false$ or `turn = i`.

In **CCS**, we model:
- Variables as **passive agents** that respond to reads and writes.
  - For example:
    $$
    B_1^f = b1rf.B_1^f + b1wf.B_1^f + b1wt.B_1^t
    $$
- The process sequence:
    $$
    enter1.exit1.P_1
    $$
- The full system:
    $$
    Peterson = (B1^f \mid B2^f \mid K \mid P_1 \mid P_2) \setminus L
    $$

We verify using **HML with recursion**.

For **safety**, we define an invariant formula:
$$
Inv = \max X. F \land [Act]X
$$
Where $F$ expresses that **both processes cannot be in CS**.

Verification shows:
- **HML with recursion**: ✅
- **Strong bisimilarity to ideal spec**: ❌ (too strict)
- **Trace equivalence**: ✅ (behavioral correctness)

Thus, Peterson is functionally correct but not identical in structure.

---

## Practice Text 6️⃣: Timed CCS and Timed Bisimilarity

Timed CCS (TCCS) extends CCS with time.

Processes can delay using:
$$
\epsilon . P
$$
This means: wait for some real-valued time $d \geq 0$ before continuing as $P$.

We model this using a **Timed Labelled Transition System (TLTS)**:
- Set of states (processes).
- Set of actions $\text{Act} = \mathbb{N} \cup \mathbb{R}_{\geq 0}$.
- Transitions:
    - Discrete: $P \xrightarrow{a} P'$
    - Time: $P \xrightarrow{d} P'$ (wait $d$ time units)

**Properties**:
- **Time determinism**: Time evolves deterministically.
- **Maximal progress**: If a discrete transition is enabled, time cannot progress.
- **Non-zenoness**: No infinite internal activity without time passage.

**Timed bisimilarity**:
- $P \sim_t Q$ if:
  - For every $P \xrightarrow{a} P'$, $Q \xrightarrow{a} Q'$ and $P' \sim_t Q'$.
  - For every $P \xrightarrow{d} P'$, $Q \xrightarrow{d} Q'$ and $P' \sim_t Q'$.

Delays must match **exactly**, which makes it more strict than weak bisimilarity.

**Example**: Light Controller
- Waits 30s in `on` mode unless user resets it.
- Turns off after timeout.
- Timed bisimilarity ensures that both versions respond the same way over time and behavior.

---

## Practice Text 7️⃣: Timed Automata and Region Graphs

A **Timed Automaton** (TA) is a finite state machine extended with **real-valued clocks**.

Clocks:
- Increase uniformly with time.
- Can be **reset** on transitions.

Transitions:
$$
(\ell, g, a, r, \ell')
$$
- $\ell$: source location.
- $g$: guard on clocks (e.g., $x \leq 5$).
- $a$: action.
- $r$: set of clocks to reset.
- $\ell'$: target location.

Each location may have **invariants** (e.g., $x \leq 10$) restricting how long time can be spent there.

**Clock valuation**:
- $v: C \to \mathbb{R}_{\geq 0}$
- $v + d$: time passes $d$.
- Reset: $v[x := 0]$

To analyze TAs, we use a **region graph**:
- Partition clock valuations into **equivalence classes** called **regions**.
- Two valuations are in the same region if they **enable the same transitions**.
- The region graph is **finite**, enabling **model checking**.

**Timed bisimilarity** compares TAs:
- Both must perform the **same discrete actions**.
- Both must delay by the **same time**.

Example: A timed safety controller must delay before entry into critical state — region abstraction lets us verify this.

---

## Practice Text 8️⃣: UPPAAL – Train-Gate and Gossiping Girls

Let me present two case studies modeled and verified in UPPAAL.

### 🛤️ Train-Gate System

Goal: Only **one train** on the bridge at a time.

**Train automaton**:
- States: Safe → Appr → Cross → Safe
- Clock $x$ controls timing of transitions.
- Guards and invariants ensure timing constraints (e.g., must wait 10 seconds before crossing).

**Gate automaton**:
- Maintains a **queue** of trains.
- Handles signals:
  - `appr[id]!`, `stop[id]?`, `go[id]!`, `leave[id]!`

Verification goals:
- **Safety**: No two trains in Cross simultaneously.
- **Liveness**: Every train eventually crosses.
- **No deadlocks**.

Correct model ensures:
- Mutual exclusion,
- Fairness,
- Finite waiting time.

### 📞 Gossiping Girls

Goal: All girls know all secrets.

Each **Girl automaton**:
- Initially knows one secret.
- Can call others using `call[i]!` and `call[i]?`
- When two talk: they share all known secrets.

Calls take **exactly 60 seconds**, modeled using clock $x$.

**Scenarios**:
1. Chain: Only neighbors can call.
2. Full graph: Any girl can call any other.

Optional:
- Circular topology.
- Only one call at a time.

Verification tasks:
- **Minimum number of calls**.
- **Minimum time** to spread all secrets.
- **Deadlock freedom**.
- Use **search strategies**: BFS, DFS, shortest/fastest path.
- Use **Message Sequence Charts (MSC)** to visualize communication.

Result: Efficient models spread secrets in ~170 seconds for 4 girls.

---

