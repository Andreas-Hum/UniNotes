# Lecture 2: Constraint Satisfaction Problems (CSPs)

### Key Concepts

1. **Variable and Domain**:
   - A **variable** $X$ has a **domain** $dom[X]$, which can be:
     - Discrete (e.g., integers),
     - Continuous (e.g., real numbers),
     - Binary (e.g., $\{0, 1\}$).
2. **Assignments**:
   - An **assignment** maps variables to values in their domains:
     - Example: $\{X_1 = v_1, X_2 = v_2, ..., X_k = v_k\}$, where $v_i \in dom[X_i]$.
   - **Total assignment**: Every variable is assigned a value.
   - If there are $n$ variables and each has a domain of size $d$, there are $d^n$ total assignments.
3. **Constraints**:
   - A **constraint** specifies conditions on variable assignments:
     - **Unary constraint**: On a single variable (e.g., $B \leq 3$).
     - **Binary constraint**: Between two variables (e.g., $A \leq B$).
     - **k-ary constraint**: Involves $k$ variables (e.g., $A + B = C$ is ternary).
   - An assignment **satisfies** a constraint if the condition evaluates to true. It **violates** a constraint if it evaluates to false.

4. **Constraint Satisfaction Problem (CSP)**:
   - A CSP consists of:
     - A set of variables.
     - A domain for each variable.
     - A set of constraints.
   - A **solution** is a total assignment that satisfies all constraints.

---

### Representation of CSPs

1. **Constraint Graph**:
   - Nodes:
     - Circles/ovals represent **variables**.
     - Rectangles represent **constraints**.
   - Arcs:
     - Connect variable nodes to constraint nodes in their scope.
   - The constraint network is a **bipartite graph**.

2. **Domain Representation**:
   - Use a dictionary $dom$ where $dom[X]$ is the set of possible values for variable $X$.

---

### Arc Consistency

- **Arc Consistency**:
  - Suppose a constraint $c$ has scope $\{X, Y_1, ..., Y_k\}$.
  - Arc $(X, c)$ is **arc consistent** if, for every value $x \in dom[X]$, there exist values $y_1 \in dom[Y_1], ..., y_k \in dom[Y_k]$ such that the assignment $\{X = x, Y_1 = y_1, ..., Y_k = y_k\}$ satisfies $c$.
  - A network is **arc consistent** if all arcs are arc consistent.

- **Improving Efficiency**:
  - Use **domain splitting** (case analysis + search):
    - Split a problem into disjoint cases (e.g., partition the domain).
    - Apply arc consistency to simplify each case.

---

### Generalized Arc Consistency (GAC) Algorithm

The **Generalized Arc Consistency (GAC) algorithm** is given in Figure 4.4. It takes in a CSP with:
- **Variables**: $Vs$,
- **Constraints**: $Cs$,
- (Possibly reduced) **domains** specified by the dictionary $dom$, and
- A **set of potentially inconsistent arcs**: $to\_do$.

#### Initialization:
- The set $to\_do$ initially consists of all arcs in the graph:
  $$
  \{\langle X, c \rangle \mid c \in Cs \text{ and } X \in scope(c)\}.
  $$
- The goal of the algorithm is to modify $dom$ to make the network arc consistent.

#### Procedure:
1. **While $to\_do$ is not empty**:
   - Remove an arc $\langle X, c \rangle$ from $to\_do$.
   - If the arc $\langle X, c \rangle$ is **not arc consistent**:
     - Prune the domain of $X$ to make it arc consistent.
     - Add all previously consistent arcs that could now be inconsistent to $to\_do$:
       $$
       \{\langle Z, c' \rangle \mid c' \neq c, X \in scope(c'), Z \neq X\}.
       $$
       These arcs involve:
       - A different constraint $c'$ that involves $X$.
       - A variable $Z$ in the scope of $c'$ other than $X$.
2. **When $to\_do$ is empty**, the constraint graph is arc consistent.

---

### Explanation of Key Steps

#### **What does pruning mean?**
- When an arc $\langle X, c \rangle$ is **not arc consistent**, this means there is at least one value $x \in dom[X]$ that cannot satisfy the constraint $c$ with any valid assignment for the other variables in the scope of $c$. 
- **Pruning** removes these invalid values from $dom[X]$, ensuring that $dom[X]$ only contains values that can satisfy $c$.

#### **What does it mean to add arcs to $to\_do$?**
- After pruning $dom[X]$, the domains of other variables connected to $X$ through different constraints may become invalid. 
- To handle this:
  - Arcs $\langle Z, c' \rangle$ are added back to $to\_do$, where:
    - $c'$ is a constraint that involves $X$ (but is not the current constraint $c$ being processed).
    - $Z$ is another variable in the scope of $c'$ (other than $X$).
  - This ensures that all potentially inconsistent arcs caused by the domain changes of $X$ are rechecked for consistency.

#### **When is the graph arc consistent?**
- When $to\_do$ is empty, it means that:
  - All arcs have been processed.
  - The domains of all variables are pruned so that every value in a variable's domain satisfies all relevant constraints with some valid assignments for the other variables.

---

### Summary of GAC Algorithm:
- **Input**: A CSP with variables, constraints, and domains.
- **Output**: A pruned domain dictionary $dom$ such that the CSP is arc consistent.
- **Key Idea**:
  - Iteratively make arcs consistent by pruning domains and rechecking affected arcs until no further pruning is required.

# GAC Example

We have three variables $A$, $B$, and $C$.  
Their **initial domains** are $\{1,2,3\}$ for each of $A$, $B$, $C$.

We have **two constraints**:
- $A < B$
- $B < C$

## Arcs
Since each constraint has two variables, we list the arcs as:
- $\langle A,\, A<B\rangle$
- $\langle B,\, A<B\rangle$
- $\langle B,\, B<C\rangle$
- $\langle C,\, B<C\rangle$

We start with  
$to\_do = \{\langle A,\, A<B\rangle,\; \langle B,\, A<B\rangle,\; \langle B,\, B<C\rangle,\; \langle C,\, B<C\rangle\}$.

---

## Step-by-Step GAC

### Step 1: Process $\langle A,\, A<B\rangle$
- Current domains: $dom(A) = \{1,2,3\}$, $dom(B) = \{1,2,3\}$.
- For each $a \in dom(A)$, check if there is some $b \in dom(B)$ with $a < b$:
  - $a = 1$: needs $1 < b$. In $\{1,2,3\}$, $b$ can be $2$ or $3$. Valid.
  - $a = 2$: needs $2 < b$. In $\{1,2,3\}$, $b = 3$ works. Valid.
  - $a = 3$: needs $3 < b$. No $b \in \{1,2,3\}$ satisfies this. Invalid.
- **Prune** $3$ from $dom(A)$, so $dom(A) = \{1,2\}$.
- Add back any arcs involving $A$ if there are other constraints with $A$ (not needed here aside from the current one).

### Step 2: Process $\langle B,\, A<B\rangle$
- Now $dom(A) = \{1,2\}$, $dom(B) = \{1,2,3\}$.
- For each $b \in dom(B)$, check if there is some $a \in dom(A)$ with $a < b$:
  - $b = 1$: needs $a < 1$. No $a \in \{1,2\}$ works. Invalid.
  - $b = 2$: needs $a < 2$. $a=1$ is valid.
  - $b = 3$: needs $a < 3$. $a=1$ or $2$ is valid.
- **Prune** $1$ from $dom(B)$, so $dom(B) = \{2,3\}$.
- Since $dom(B)$ changed, we must recheck any constraints involving $B$ (like $B<C$).

### Step 3: Process $\langle B,\, B<C\rangle$
- Now $dom(B) = \{2,3\}$, $dom(C) = \{1,2,3\}$.
- For each $b \in \{2,3\}$, check if there is some $c \in \{1,2,3\}$ with $b < c$:
  - $b = 2$: needs $c > 2$. Then $c = 3$. Valid.
  - $b = 3$: needs $c > 3$. None in $\{1,2,3\}$. Invalid.
- **Prune** $3$ from $dom(B)$, so $dom(B) = \{2\}$.
- Add arcs involving $B$ (like $\langle A,\, A<B\rangle$) back to be rechecked.

### Step 4: Process $\langle C,\, B<C\rangle$
- $dom(B) = \{2\}$, $dom(C) = \{1,2,3\}$.
- For each $c \in \{1,2,3\}$, we need $2 < c$:
  - $c=1$: $2 < 1$ is false.
  - $c=2$: $2 < 2$ is false.
  - $c=3$: $2 < 3$ is true. Valid.
- **Prune** $1$ and $2$ from $dom(C)$, so $dom(C) = \{3\}$.

### Step 5: Re-check Affected Arcs
#### (a) $\langle A,\, A<B\rangle$
- $dom(A) = \{1,2\}$, $dom(B) = \{2\}$.
- For each $a \in \{1,2\}$, check $a < 2$:
  - $a=1$ is valid.
  - $a=2$ fails ($2 < 2$ is false).
- **Prune** $2$ from $dom(A)$, leaving $dom(A) = \{1\}$.

#### (b) $\langle B,\, A<B\rangle$
- Now $dom(A)=\{1\}$, $dom(B)=\{2\}$.
- We need $a < b$ for $a=1$ and $b=2$. This is true, so no pruning.

No more arcs require changes. The queue is empty.

---

## Final Domains
- $dom(A) = \{1\}$
- $dom(B) = \{2\}$
- $dom(C) = \{3\}$

These single-value domains are **arc consistent** for $A < B$ and $B < C$.

  
# Lecture 03: Reasoning under Uncertainty and Bayesian Networks

### 4.1.3 Probability of an Event

**Definition**: The probability of an event $E$, denoted as $P(E)$, is a measure of the likelihood that $E$ will occur. It quantifies how "likely" an event is, given the defined sample space.

**Formula**: $P(E) = \frac{|E|}{|S|}$, where $|E|$ is the number of favorable outcomes, and $|S|$ is the total number of possible outcomes in the sample space.

**Example**: For a fair six-sided die, the probability of rolling an even number (event $E = \{2, 4, 6\}$) is calculated as:

$$
P(E) = \frac{|E|}{|S|} = \frac{3}{6} = 0.5
$$

**Properties**:
- $0 \leq P(E) \leq 1$: The probability of any event is between 0 and 1.
- $P(S) = 1$: The probability of the sample space itself is 1, meaning that something in the sample space must occur.
- $P(\emptyset) = 0$: The probability of the empty set (an impossible event) is 0.
- **Total Probability**: The sum of the probabilities of all simple events (outcomes) in the sample space is 1.

## 4.2 Conditional Probability and Independence

### 4.2.1 Conditional Probability

**Definition**: The probability of an event $A$ given that another event $B$ has occurred is called conditional probability, denoted $P(A|B)$. This measures how the probability of $A$ is affected by knowing that $B$ has happened.

**Formula**: $P(A|B) = \frac{P(A \cap B)}{P(B)}$, assuming $P(B) > 0$. This formula tells us how to adjust the probability of $A$ when $B$ is known to have occurred.

**Example**: Consider a deck of 52 cards. If we know a card drawn is a face card (event $B$), the probability of it being an ace (event $A$) changes. Normally, there are 4 aces in a deck, so $P(A) = \frac{4}{52}$. But given that the card is a face card (which includes 12 cards: 4 Jacks, 4 Queens, 4 Kings), the conditional probability is:

$$
P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0}{12} = 0
$$

Thus, if a card is known to be a face card, the probability that it is an ace is 0.

### 4.2.2 Independent Events

**Definition**: Two events $A$ and $B$ are independent if the occurrence of one does not affect the probability of the other. This is a key concept when events do not influence each other.

**Formula**: $P(A \cap B) = P(A) \cdot P(B)$ if $A$ and $B$ are independent.

**Example**: Suppose you roll two fair six-sided dice. Let $A$ be the event that the first die shows a 4, and $B$ be the event that the second die shows a 4. The probability of each event is $P(A) = \frac{1}{6}$ and $P(B) = \frac{1}{6}$. Since the outcome of one die does not affect the other, the probability that both dice show a 4 is:

$$
P(A \cap B) = P(A) \cdot P(B) = \frac{1}{6} \cdot \frac{1}{6} = \frac{1}{36} \approx 0.0278
$$

### 4.2.3 Bayes' Rule

**Definition**: Bayes' Rule, also known as Bayes' Theorem, is a fundamental result in probability theory that describes how to update the probability of a hypothesis based on new evidence. It relates the conditional probability of a hypothesis given observed data to the likelihood of the data under the hypothesis and the prior probability of the hypothesis.

**Formula**:

$$
P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)} = \frac{P(E|H)\cdot P(H)}{P(E|H) \cdot P(H) + P(E|\neg H) \cdot P(\neg H)}
$$

where:
- $P(H|E)$ is the **posterior probability**, or the probability of the hypothesis $H$ given the evidence $E$.
- $P(E|H)$ is the **likelihood**, or the probability of observing the evidence $E$ given that the hypothesis $H$ is true.
- $P(H)$ is the **prior probability** of the hypothesis before observing the evidence.
- $P(E)$ is the **marginal likelihood** or the total probability of observing the evidence under all possible hypotheses.

**Example**: Suppose a doctor is trying to diagnose a rare disease that affects 1 in 1000 people. There is a test for this disease that is 99% accurate, meaning that the probability of a positive test result given that a person has the disease is 0.99, and the probability of a positive test result given that a person does not have the disease is 0.01.

- Let $H$ represent the event that a person has the disease.
- Let $E$ represent the event that the test result is positive.

We want to find the probability that a person has the disease given that their test result is positive, i.e., $P(H|E)$.

First, we identify the components of Bayes' Rule:
- The prior probability $P(H)$ is 0.001 (since the disease is rare).
- The likelihood $P(E|H)$ is 0.99 (the test correctly identifies the disease).
- The marginal likelihood $P(E)$ can be calculated as:

$$
P(E) = P(E|H) \cdot P(H) + P(E|\neg H) \cdot P(\neg H)
$$

where $P(\neg H)$ is the probability that the person does not have the disease (0.999) and $P(E|\neg H)$ is the probability of a positive test result given the person does not have the disease (0.01). Therefore:

$$
P(E) = (0.99 \cdot 0.001) + (0.01 \cdot 0.999) = 0.00099 + 0.00999 = 0.01098
$$

Now, applying Bayes' Rule:

$$
P(H|E) = \frac{0.99 \cdot 0.001}{0.01098} \approx 0.0902
$$

So, even with a positive test result, the probability that the person actually has the disease is approximately 9.02%. This example illustrates how a rare condition combined with a positive test result still leads to a relatively low probability due to the rarity of the disease, demonstrating the importance of considering prior probabilities.

**Applications of Bayes' Rule**:
- **Medical Diagnosis**: Updating the probability of a disease based on symptoms and test results.
- **Spam Filtering**: Determining whether an email is spam based on the presence of certain words.
- **Machine Learning**: Naive Bayes classifiers use Bayes' Rule for classification tasks.
- **Decision-Making Under Uncertainty**: Making informed decisions by continuously updating the likelihood of outcomes based on new data.

**Importance in AI**: Bayes' Rule is fundamental in many AI systems, especially in areas like natural language processing, predictive analytics, and decision-making systems. It allows these systems to make better decisions by incorporating new data in a principled way.

## 4.3 Joint Probability and Joint Probability Distributions

### 4.3.1 Joint Probability

**Definition**: Joint probability refers to the probability of two (or more) events occurring simultaneously. If $A$ and $B$ are two events, the joint probability of $A$ and $B$ is denoted by $P(A \cap B)$ or simply $P(A, B)$.

**Formula**:

- For **independent** events $A$ and $B$, the joint probability is:
  $$
  P(A \cap B) = P(A) \cdot P(B).
  $$

- For **dependent** events, where the occurrence of one affects the probability of the other, the joint probability is:
  $$
  P(A \cap B) = P(A \mid B) \cdot P(B) = P(B \mid A) \cdot P(A).
  $$

**Example**: Consider two events: $A$ is the event that a randomly chosen person is female, and $B$ is the event that the person has brown hair. Suppose $P(A) = 0.51$ (51% of the population is female), and $P(B \mid A) = 0.4$ (40% of females have brown hair). The joint probability that a person is both female and has brown hair is:

$$
P(A \cap B) = P(A) \cdot P(B \mid A) = 0.51 \cdot 0.4 = 0.204.
$$

Thus, there is a 20.4% chance that a randomly selected person is both female and has brown hair.

---

### 4.3.2 Joint Probability Distribution

**Definition**: A joint probability distribution represents the probabilities of all possible combinations of outcomes for two or more random variables. For two **discrete** random variables $X$ and $Y$, the joint probability distribution is typically presented in the form of a table, where each cell contains the probability $P(X = x_i, Y = y_j)$.

For **continuous** random variables, the joint distribution is described by a joint probability density function (PDF), denoted as $f_{X,Y}(x, y)$, which gives the likelihood that $X$ is near $x$ and $Y$ is near $y$.

**Properties**:  
1. **Non-negativity**: $P(X = x_i, Y = y_j) \ge 0$ for all $x_i$ and $y_j$.  
2. **Normalization**: The sum (for discrete variables) or the integral (for continuous variables) of all joint probabilities must equal 1:

   - **Discrete case**:
     $$
     \sum_i \sum_j P(X = x_i, Y = y_j) = 1.
     $$

   - **Continuous case**:
     $$
     \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f_{X,Y}(x, y)\,dx\,dy = 1.
     $$

**Example (Discrete)**: Consider two discrete random variables, $X$ (representing the outcome of a fair die roll) and $Y$ (representing the outcome of flipping a fair coin, where 0 is tails and 1 is heads). The joint probability distribution could be represented in a table as follows:

|       | $Y=0$ (Tails) | $Y=1$ (Heads) |
|:-----:|:-------------:|:-------------:|
| $X=1$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |
| $X=2$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |
| $X=3$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |
| $X=4$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |
| $X=5$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |
| $X=6$ | $\tfrac{1}{12}$ | $\tfrac{1}{12}$ |

Since the die roll and coin flip are independent, each of the 12 possible outcomes has probability $\tfrac{1}{12}$.

**Example (Continuous)**: For two continuous random variables $X$ and $Y$, their joint probability distribution could be given by a joint PDF, such as:

$$
f_{X,Y}(x, y) = \frac{1}{2\pi \sigma_X \sigma_Y \sqrt{1-\rho^2}} 
\exp\Bigg(-\frac{1}{2(1-\rho^2)}\Big[\Big(\frac{x-\mu_X}{\sigma_X}\Big)^2 
- 2\rho\Big(\frac{x-\mu_X}{\sigma_X}\Big)\Big(\frac{y-\mu_Y}{\sigma_Y}\Big) 
+ \Big(\frac{y-\mu_Y}{\sigma_Y}\Big)^2\Big]\Bigg),
$$

which represents the joint PDF of two normally distributed variables $X$ and $Y$ with means $\mu_X$ and $\mu_Y$, standard deviations $\sigma_X$ and $\sigma_Y$, and correlation $\rho$.

---

### 4.3.3 Working with a Full Joint Probability Distribution

A *full joint probability distribution* specifies the probability of *every* combination of events in the sample space. As an example, consider two binary variables:

- **Toothache (T)**: whether a patient has a toothache ($\text{toothache}$ or $\neg\text{toothache}$).  
- **Cavity (C)**: whether a patient has a cavity ($\text{cavity}$ or $\neg\text{cavity}$).

Suppose the full joint probability distribution is given by the following table:

|                          | $\text{toothache}$ | $\neg\text{toothache}$ |
|:------------------------:|:------------------:|:-----------------------:|
| **$\text{cavity}$**      | 0.12               | 0.08                   |
| **$\neg\text{cavity}$**  | 0.08               | 0.72                   |

1. **How to compute $P(\text{cavity})$?**  
   We **sum** all joint probabilities where $\text{cavity}$ is true:
   $$
   P(\text{cavity}) 
   = P(\text{cavity} \wedge \text{toothache}) 
   + P(\text{cavity} \wedge \neg\text{toothache}) 
   = 0.12 + 0.08 = 0.20.
   $$

2. **How to compute $P(\text{cavity} \vee \text{toothache})$?**  
   We **sum** all joint probabilities where either $\text{cavity}$ or $\text{toothache}$ (or both) is true:
   $$
   P(\text{cavity} \vee \text{toothache}) 
   = P(\text{cavity} \wedge \text{toothache})
   + P(\neg\text{cavity} \wedge \text{toothache})
   + P(\text{cavity} \wedge \neg\text{toothache}).
   $$
   From the table:
   $$
   = 0.12 + 0.08 + 0.08 = 0.28.
   $$

3. **How to compute $P(\text{cavity} \mid \text{toothache})$?**  
   Using the definition of conditional probability:
   $$
   P(\text{cavity} \mid \text{toothache}) 
   = \frac{P(\text{cavity} \wedge \text{toothache})}{P(\text{toothache})}.
   $$
   First, find $P(\text{toothache})$ by summing the relevant row:
   $$
   P(\text{toothache}) 
   = P(\text{cavity} \wedge \text{toothache}) 
   + P(\neg\text{cavity} \wedge \text{toothache}) 
   = 0.12 + 0.08 = 0.20.
   $$
   Then,
   $$
   P(\text{cavity} \mid \text{toothache}) 
   = \frac{0.12}{0.20} = 0.60.
   $$
### **Marginalization Rule**  
To remove (marginalize out) a variable $X$ from a joint probability distribution $P(X, Y, \dots)$, **sum** the probabilities over **all** possible values of $X$. Formally:

$$
P(Y, \dots) = \sum_{x} \; P(X = x, Y, \dots).
$$

---

#### Mini Example

Suppose you have a table for two variables, $X$ and $Y$, showing $P(X, Y)$:

|       | $Y=1$ | $Y=2$ |
|:-----:|:-----:|:-----:|
| $X=1$ | 0.10   | 0.15  |
| $X=2$ | 0.25   | 0.50  |

To **remove $X$** and get the marginal $P(Y)$:

1. **For $Y=1$**, sum over $X$:
   $$
   P(Y=1) = P(X=1, Y=1) + P(X=2, Y=1) = 0.10 + 0.25 = 0.35.
   $$

2. **For $Y=2$**, sum over $X$:
   $$
   P(Y=2) = P(X=1, Y=2) + P(X=2, Y=2) = 0.15 + 0.50 = 0.65.
   $$

Hence,

|  $Y$  | $P(Y)$ |
|:-----:|:------:|
| **1** | 0.35   |
| **2** | 0.65   |

and $0.35 + 0.65 = 1$. 

### General Conditional Probability with Multiple Variables

When you have several variables and want to compute probabilities such as:

1. **$P(X \mid Y_1, \dots, Y_n)$** 
2. **$P(X, Y \mid Z)$**

the standard rule is **always**:

$$
P(\text{(variables)} \mid \text{(other variables)}) 
\;=\; 
\frac{P(\text{all variables together})}{P(\text{the conditioning variables alone})}.
$$

#### Case 1: $P(X \mid Y_1, Y_2, \dots, Y_n)$

- **Definition**:

  $$
  P\bigl(X \mid Y_1, Y_2, \dots, Y_n\bigr)
  \;=\;
  \frac{P\bigl(X, Y_1, Y_2, \dots, Y_n\bigr)}{P\bigl(Y_1, Y_2, \dots, Y_n\bigr)}.
  $$

- **Marginalizing out $X$** in the denominator:

  $$
  P\bigl(Y_1, Y_2, \dots, Y_n\bigr)
  \;=\;
  \sum_{x'} \;
  P\bigl(x', Y_1, Y_2, \dots, Y_n\bigr).
  $$

#### Case 2: $P(X, Y \mid Z)$

- **Definition**:

  $$
  P(X, Y \mid Z)
  \;=\;
  \frac{P(X, Y, Z)}{P(Z)}.
  $$

- **Marginalizing out $(X, Y)$** in the denominator**?**  
  Actually, for $P(Z)$, you **sum over all** possible values of **both** $X$ and $Y$:

  $$
  P(Z)
  \;=\;
  \sum_{x'} \sum_{y'} P(x',\, y',\, Z).
  $$

---

### Example with Three Variables: $X$, $Y$, and $Z$

#### Joint Distribution Table

Let's say each of $X$, $Y$, and $Z$ can take two values:
- $X \in \{x_1, x_2\}$,
- $Y \in \{y_1, y_2\}$,
- $Z \in \{z_1, z_2\}$.

Below is a possible joint distribution $P(X, Y, Z)$ (just as an example):

| $X$   | $Y$   | $Z$   | $P(X, Y, Z)$ |
|:-----:|:-----:|:-----:|:------------:|
| $x_1$ | $y_1$ | $z_1$ | 0.10         |
| $x_1$ | $y_1$ | $z_2$ | 0.05         |
| $x_1$ | $y_2$ | $z_1$ | 0.15         |
| $x_1$ | $y_2$ | $z_2$ | 0.10         |
| $x_2$ | $y_1$ | $z_1$ | 0.20         |
| $x_2$ | $y_1$ | $z_2$ | 0.05         |
| $x_2$ | $y_2$ | $z_1$ | 0.25         |
| $x_2$ | $y_2$ | $z_2$ | 0.10         |

> **Check**: Summing all cells gives 1.00 (0.10 + 0.05 + 0.15 + 0.10 + 0.20 + 0.05 + 0.25 + 0.10 = 1.00).

#### 1. Compute $P(Z)$ by Marginalizing Out $X$ and $Y$

To get $P(Z)$, **add all** rows for each value of $Z$.

- **$P(Z=z_1)$**: sum all rows where $Z=z_1$
  
  $$
  0.10 + 0.15 + 0.20 + 0.25 = 0.70.
  $$

- **$P(Z=z_2)$**: sum all rows where $Z=z_2$
  
  $$
  0.05 + 0.10 + 0.05 + 0.10 = 0.30.
  $$

Indeed, $0.70 + 0.30 = 1.00$.

#### 2. Example: $P(X=x_1 \mid Z=z_1)$

Use the rule

$$
P(X=x_1 \mid Z=z_1)
= \frac{P(X=x_1, Z=z_1)}{P(Z=z_1)}.
$$

First, **find** $P(X=x_1, Z=z_1)$ by summing over all values of $Y$ while keeping $X=x_1$ and $Z=z_1$:

- $P(x_1, y_1, z_1) = 0.10$
- $P(x_1, y_2, z_1) = 0.15$

So,

$$
P(x_1, Z=z_1) = 0.10 + 0.15 = 0.25.
$$

We already have $P(Z=z_1) = 0.70$ (from above).

Hence,

$$
P(x_1 \mid z_1)
= \frac{0.25}{0.70}
\approx 0.357.
$$

### 3. Example: $P(X=x_2, Y=y_2 \mid Z=z_1)$

Use

$$
P(X=x_2, Y=y_2 \mid Z=z_1)
= \frac{P(X=x_2, Y=y_2, Z=z_1)}{P(Z=z_1)}.
$$

From the table, $P(x_2, y_2, z_1) = 0.25$, and $P(z_1) = 0.70$. So:

$$
P(x_2, y_2 \mid z_1)
= \frac{0.25}{0.70}
\approx 0.357.
$$

#### 4. Example: $P(X, Y \mid Z)$ in Full Table Form

If you want the entire table for $P(X, Y \mid Z=z_1)$, do the above for **each** pair $(X, Y)$ while $Z=z_1$, and confirm they sum to 1. For instance:

- $P(x_1, y_1 \mid z_1) = \frac{0.10}{0.70} \approx 0.143$
- $P(x_1, y_2 \mid z_1) = \frac{0.15}{0.70} \approx 0.214$
- $P(x_2, y_1 \mid z_1) = \frac{0.20}{0.70} \approx 0.286$
- $P(x_2, y_2 \mid z_1) = \frac{0.25}{0.70} \approx 0.357$

Check sum: $0.143 + 0.214 + 0.286 + 0.357 = 1.00$.

---

### Summary of the General Formulas

1. **Conditional Probability with Multiple Conditions**  
   For any set of variables $X, Y_1, Y_2, \dots, Y_n$:
   $$
   P\bigl(X \mid Y_1, Y_2, \dots, Y_n\bigr)
   \;=\;
   \frac{P\bigl(X, Y_1, Y_2, \dots, Y_n\bigr)}{
         \sum_{x'}\,P\bigl(x', Y_1, Y_2, \dots, Y_n\bigr)
       }.
   $$

2. **Conditional Probability of a Pair**  
   For $P(X, Y \mid Z)$:
   $$
   P(X, Y \mid Z)
   = \frac{P(X, Y, Z)}{P(Z)}
   \quad \text{where} \quad
   P(Z) = \sum_{x'} \sum_{y'} P(x',\,y',\,Z).
   $$

Use these rules any time you want to “condition on” some variables and keep others. The key is **marginalizing out** (summing over) the variables you *don’t* want in your final expression.


### Summation Over Hidden Variables in Bayesian Networks

When we work with a **Bayesian Network** (BN) and want to compute a probability distribution—such as $ P(Q \mid E=e) $—we often have:

- **Query** variable(s): The variable(s) $Q$ whose probability we want to find.
- **Evidence** variable(s): The observed variable(s) $E$ set to particular values $e$.
- **Hidden (Latent) Variables**: Variables that are not observed (no evidence for them) and are not the direct target of the query.

A general strategy is:
1. **Identify** which variables are **query**, **evidence**, and **hidden**.
2. **Express** the joint probability for the BN in **factorized** form according to its structure.
3. **Marginalize (sum) over all possible values** of the hidden variables.

#### Example: General Formula

Suppose we want $ P(Q \mid E = e) $ in a BN with hidden variables $H$. Then:

$$
P(Q \mid E = e)
\;=\;
\frac{P(Q, E = e)}{P(E = e)}
\;=\;
\frac{\sum_H P(Q, H, E = e)}{\sum_{Q'} \sum_H P(Q', H, E = e)}.
$$

- The numerator $\sum_H P(Q, H, E = e)$ **sums** over all possible assignments of the hidden variables $H$.
- The denominator is $ P(E = e) $, which you can similarly expand by summing over **all** possible values of both $Q$ and $H$.

#### Factorizing the Joint

If our BN has a set of variables $\{X_1, X_2, \ldots, X_n\}$ with parent sets $\mathrm{Parents}(X_i)$, then:

$$
P(X_1, X_2, \dots, X_n)
\;=\;
\prod_{i=1}^{n} P(X_i \mid \mathrm{Parents}(X_i)).
$$

Each factor depends only on $X_i$ and its parents.

#### Handling Hidden Variables

- If a variable is **not** observed (no evidence) and **not** part of the query, it is **hidden**.
- To compute $ P(\text{anything involving the hidden variable}) $, we must **sum** (or, if continuous, **integrate**) over **all** possible values of that hidden variable.

Formally, if we want $ P(A, B) $ but $C$ is unobserved (hidden), then:

$$
P(A, B)
\;=\;
\sum_{c \in \text{Values}(C)} P(A, B, C=c).
$$

#### Example Computation

Imagine a BN with variables $$A, B, C$$. You know $$A = a$$ (evidence), want $P(B)$ (query), and $C$ is hidden. Then:

$$
P(B \mid A=a)
\;=\;
\frac{P(B, A=a)}{P(A=a)}
\;=\;
\frac{\sum_{c} P(B, A=a, C=c)}{\sum_{B'} \sum_{c} P(B', A=a, C=c)}.
$$

Each term $P(B, A=a, C=c)$ is factorized according to the structure of your BN.  

---

#### Key Points

1. **Query**: The variable or set of variables you want a probability for.
2. **Evidence**: Variables you have observed data for.
3. **Hidden**: Variables neither observed nor queried—must be summed out (marginalized).
4. **Factorization**: Use the **parents** structure in the BN to write the joint probability product.
5. **Summation**: Carefully sum (or integrate) over **all** values of the hidden variables.

### **Topological Ordering in the Network**

Given the directed edges:

- $A \to B$
- $A \to C$
- $C \to D$

A valid **topological ordering** must ensure:

1. $A$ appears before $B$ and $C$.
2. $C$ appears before $D$.

There is no constraint between $B$ and $C$ directly, so both of the following are valid topological orderings:

- **$A, B, C, D$**
- **$A, C, B, D$**

Any sequence where $A$ comes first (before $B$ and $C$) and $C$ comes before $D$ will be acceptable.
