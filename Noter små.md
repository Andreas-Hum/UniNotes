# Author
**Andreas Hummelmose**  
*Computer Science Student, 5th Semester, Aalborg University*  
[LinkedIn: Andreas Hummelmose](https://www.linkedin.com/in/andreas-hummelmose-77580a252/)

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

## GAC Example

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

When we work with a **Bayesian Network** (BN) and want to compute a probability distribution—such as $P(Q \mid E=e)$—we often have:

- **Query** variable(s): The variable(s) $Q$ whose probability we want to find.
- **Evidence** variable(s): The observed variable(s) $E$ set to particular values $e$.
- **Hidden (Latent) Variables**: Variables that are not observed (no evidence for them) and are not the direct target of the query.

A general strategy is:
1. **Identify** which variables are **query**, **evidence**, and **hidden**.
2. **Express** the joint probability for the BN in **factorized** form according to its structure.
3. **Marginalize (sum) over all possible values** of the hidden variables.

#### Example: General Formula

Suppose we want $P(Q \mid E = e)$ in a BN with hidden variables $H$. Then:

$$
P(Q \mid E = e)
\;=\;
\frac{P(Q, E = e)}{P(E = e)}
\;=\;
\frac{\sum_H P(Q, H, E = e)}{\sum_{Q'} \sum_H P(Q', H, E = e)}.
$$

- The numerator $\sum_H P(Q, H, E = e)$ **sums** over all possible assignments of the hidden variables $H$.
- The denominator is $P(E = e)$, which you can similarly expand by summing over **all** possible values of both $Q$ and $H$.

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


# Working with the Full Joint Probability Distribution

### Example: Toothache and Cavity Joint Distribution
|            | Toothache   | ¬Toothache |
|------------|-------------|------------|
| **Cavity** | 0.12        | 0.08       |
| **¬Cavity**| 0.08        | 0.72       |

---

### How to Compute Probabilities from the Joint Distribution:
1. **$P(\text{cavity})$**:  
   Sum across the row:

   $$
   P(\text{cavity}) = P(\text{cavity} \land \text{toothache}) + P(\text{cavity} \land \lnot \text{toothache})
   $$

2. **$P(\text{cavity} \lor \text{toothache})$**:  
   Sum across atomic events:

   $$
   P(\text{cavity} \lor \text{toothache}) = P(\text{cavity} \land \text{toothache}) + P(\lnot \text{cavity} \land \text{toothache}) + P(\text{cavity} \land \lnot \text{toothache})
   $$

3. **$P(\text{cavity} \mid \text{toothache})$**:

   $$
   P(\text{cavity} \mid \text{toothache}) = \frac{P(\text{cavity} \land \text{toothache})}{P(\text{toothache})}
   $$

---

## **Bayes' Rule**

**Proposition**: Given propositions $A$ and $B$ where $P(A) > 0$ and $P(B) > 0$, we have:

$$
P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}
$$

**Proof**:  
By definition:

$$
P(A \mid B) = \frac{P(A \land B)}{P(B)}
$$

And by the product rule:

$$
P(A \land B) = P(B \mid A) P(A)
$$

Therefore:

$$
P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}
$$

**Notation** (System of equations):

$$
P(X \mid Y) = \frac{P(Y \mid X) P(X)}{P(Y)}
$$

---

### Example: Toothache and Cavity

Given:

- $P(\text{toothache} \mid \text{cavity}) = 0.6$
- $P(\text{cavity}) = 0.2$
- $P(\text{toothache}) = 0.2$

Using Bayes' Rule:

$$
P(\text{cavity} \mid \text{toothache}) = \frac{P(\text{toothache} \mid \text{cavity}) P(\text{cavity})}{P(\text{toothache})}
$$

Substitute values:

$$
P(\text{cavity} \mid \text{toothache}) = \frac{0.6 \times 0.2}{0.2} = 0.6
$$

---

### **Why Not Directly Assess $P(\text{cavity} \mid \text{toothache})$?**

- $P(\text{toothache} \mid \text{cavity})$ is **causal**.
- $P(\text{cavity} \mid \text{toothache})$ is **diagnostic**.

**Causal dependencies** are more robust across different situations (e.g., changes in frequency of causes).  
For example:

- If there is a **cavity epidemic**, $P(\text{cavity} \mid \text{toothache})$ increases, but $P(\text{toothache} \mid \text{cavity})$ remains the same.
- **Causal dependencies** are often easier to assess.

---

## **Definition of Independence**

Two events $A$ and $B$ are **independent** if:

$$
P(A \land B) = P(A) P(B)
$$

---

### **Proposition**:  
Given independent events $A$ and $B$ where $P(B) > 0$, we have:

$$
P(A \mid B) = P(A)
$$

**Proof**:  
By definition:

$$
P(A \mid B) = \frac{P(A \land B)}{P(B)}
$$

By independence:

$$
P(A \land B) = P(A) P(B)
$$

Therefore:

$$
P(A \mid B) = P(A)
$$

Similarly, if $P(A) > 0$, we have:

$$
P(B \mid A) = P(B)
$$

---

### **Examples of Independence:**

- $P(\text{Dice1} = 6 \land \text{Dice2} = 6) = \frac{1}{36}$
- $P(W = \text{sunny} \mid \text{headache}) = P(W = \text{sunny})$ (unless you're weather-sensitive).

However, **toothache** and **cavity** are **NOT independent**:

- $P(\text{toothache}) = 0.2$
- $P(\text{cavity}) = 0.2$
- $P(\text{toothache} \land \text{cavity}) = 0.12 > 0.04$

This shows that **the fraction of cavities is higher within toothaches than without toothaches**.

---

## **Definition: Random Variable Independence**

Two random variables $X$ and $Y$ are independent if:

$$
P(X, Y) = P(X) P(Y)
$$

---

### **Definition: Independence of Multiple Variables**

The variables $A_1, \dots, A_k$ and $B_1, \dots, B_m$ are independent if:

$$
P(A_1, \dots, A_k \mid B_1, \dots, B_m) = P(A_1, \dots, A_k)
$$

This is equivalent to:

$$
P(B_1, \dots, B_m \mid A_1, \dots, A_k) = P(B_1, \dots, B_m)
$$

And also to:

$$
P(A_1, \dots, A_k, B_1, \dots, B_m) = P(A_1, \dots, A_k) \cdot P(B_1, \dots, B_m)
$$



# Lecture 05: Supervised Learning and Decision Trees

Learning is the ability of an agent to improve its behavior based on experience.
This could mean the following:
• The range of behaviors is expanded; the agent can do more.
• The accuracy on tasks is improved; the agent can do things better.
• The speed is improved; the agent can do things faster.


## Learning Task Overview

- **Task:** The behavior or task being improved through learning.
- **Data:** Experiences used to improve performance, either as a set (bag) or sequence of examples. A bag allows repeated elements, where order doesn't convey information.
- **Measure of Improvement:** How the improvement is measured, such as new skills, increased accuracy, or improved speed.
- **Learning Techniques:** Include tasks like supervised learning (classification, regression), unsupervised learning, reinforcement learning, graph learning, and inductive programming.
- **Feedback:** Characterized by feedback types (supervised, unsupervised, reinforcement learning).
- **Measuring Success:** Success is measured by performance on new data, not just training data. Success depends on generalizing beyond seen examples.
- **Bias:** The tendency to prefer one hypothesis over another, known as inductive bias, influences generalization.
- **Representation:** The internal model or representation that an agent uses for solving tasks. A richer representation is more useful but harder to learn.
- **Learning as Search:** Learning is seen as a search through possible models, with search bias affecting model selection.
- **Imperfect Data:** Handling noise, missing data, and errors in the data is crucial for a learning algorithm.
- **Interpolation and Extrapolation:** Interpolation predicts within known data, while extrapolation predicts beyond it, typically with lower accuracy.
- **Curse of Dimensionality:** As the dimensionality of data increases, the number of examples grows exponentially, making data sparse and increasing prediction difficulty.
- **Online and Offline Learning:** In offline learning, all training examples are available before acting. In online learning, examples arrive during actions and the agent must adapt continuously.
- **Active Learning:** A form of online learning where the agent actively selects which examples are most useful to learn from.
## Supervised learning  Overview

In a supervised learning task, the learner is given  
- a set of input features, $X_1, \dots, X_m$  
- a set of target features, $Y_1, \dots, Y_k$  
- a bag (multiset) of training examples, where each example $e$ is a pair  
  $(x_e, y_e)$  where  $x_e = (X_1(e), \dots, X_m(e))$  is a tuple of a value for each input feature, and  $y_e = (Y_1(e), \dots, Y_k(e))$ is a tuple of a value for each target feature.  
  
The output is a predictor, a function that predicts $Y_s$ from $X_s$.

Supervised learning is called regression when the domain of the target is (a subset of) the real numbers. It is called classification when the domain of the target is a fixed finite set

## Evaluating predictions

A predictor for target feature Y is a function from the domains of the input
features into the domain of Y. A predictor for Y is written as $\hat{Y}$, so $\hat{Y}(e)$ is the
predicted value for target feature Y on example e


The loss for example $e$ on feature $Y$ is a measure of how close the prediction $\hat{Y}(e)$ is to the actual value $Y(e)$. The measures below define a nonnegative real-valued function $\text{loss}(p, a)$ that gives the loss for prediction $p$ on an example when the actual value is $a$.

A common error function on a dataset is the mean loss, which for predictor $\hat{Y}$ on a dataset $E_s$ is
$$
\frac{1}{|E_s|} \sum_{e \in E_s} \text{loss}(\hat{Y}(e), Y(e))
$$
where $|E_s|$ is the number of examples in $E_s$.

An alternative error is the sum of losses (without $\frac{1}{|E_s|}$):
$$
\sum_{e \in E_s} \text{loss}(\hat{Y}(e), Y(e))
$$
For regression, when the target feature $Y$ is real-valued, the following losses are common:

- **0–1 loss** ($L_0$ loss):
  $$
  \text{loss}(p, a) = \begin{cases} 
  1 & \text{if } p \neq a \\
  0 & \text{if } p = a
  \end{cases}
  $$  
  The mean 0–1 loss is the fraction of wrong predictions. Accuracy is $1$ minus the mean 0–1 loss. This loss is suitable for mode or median predictions but unreliable for real-valued predictions due to floating-point inaccuracies.

- **Absolute loss** ($L_1$ loss):
  $$
  \text{loss}(p, a) = |p - a|
  $$  
  The mean absolute loss is zero only when predictions exactly match the observed values. Close predictions are better than far-away predictions.

- **Squared loss** ($L_2$ loss):
  $$
  \text{loss}(p, a) = (p - a)^2
  $$  
  This loss penalizes large errors more heavily than small ones. Minimizing mean squared loss is equivalent to minimizing root-mean-square error (RMS error). Sometimes written as $\frac{1}{2}(p - a)^2$ for easier derivative calculations.

- **Worst-case loss** ($L_\infty$ loss) on examples $E_s$:
  $$
  \max_{e \in E_s} | \hat{Y}(e) - Y(e) |
  $$  
  This evaluates the learner by its worst prediction and is the only loss that is not based on a mean or sum.

The real-valued prediction $p$ for variable $Y$ is equivalent to the categorical prediction where the prediction for 1 is $p$ and the prediction for 0 is $1 - p$.

The binary log loss, or binary cross-entropy loss, for prediction $p$ and actual value $a$ is defined by
$$
\text{logloss}(p, a) = -a \log p - (1 - a) \log(1 - p)
$$

$\textbf{Entropy for Binary Classes}$. For a probability distribution $(p, 1 - p)$ of a two-valued class label, define the entropy as:
$$
\text{Entropy}(p, 1 - p) = -p \cdot \log_2(p) - (1 - p) \cdot \log_2(1 - p).
$$

and by convention,  the purethe the distution the smaller the entropy
$$
\text{logloss}(1, 1) = \text{logloss}(0, 0) = 0.
$$
$\textbf{Definition (Expected Entropy)}$. For feature $X$ with domain $v_1, \dots, v_n$, let:
- $E_i$ be the set of examples with $X = v_i$,
- $q_i = \frac{|E_i|}{|E|}$,
- $h_i$ the entropy of the class label distribution in $E_i$.

The expected entropy from splitting on $X$ is:
$$
\text{Entropy(Class | X)} = \sum_{i=1}^{n} q_i \cdot h_i.
$$

$\textbf{Definition (Information Gain)}$. Let $\text{Entropy(Class)}$ be the entropy of the class label distribution before splitting. The information gain from splitting on $X$ is:
$$
\text{Information Gain} = \text{Entropy(Class)} - \text{Entropy(Class | X)}.
$$
The following measures are often used:
$$
\text{Recall} = \frac{tp}{tp + fn}
$$

The proportion of actual positives that are predicted to be positive.

$$
\text{Precision} = \frac{tp}{tp + fp}
$$

The proportion of predicted positives that are actually positive.

$$
\text{Accuracy} = \frac{tp + tn}{tp + tn + fp + fn}
$$

The proportion of all predictions (both positive and negative) that are correct.

$$
\text{False Positive Rate} = \frac{fp}{fp + tn}
$$
 
the proportion of actual negatives predicted to be positive.

An agent should try to maximize the true-positive rate and minimize the false-positive rate; however, these goals are incompatible. An agent can maximize the true-positive rate by making positive predictions about all cases it is sure about (assuming it is correct about these). However, this choice maximizes the false-positive rate because more of the positives will be wrong.

The information gain measure favors attributes with many values: For example, the attribute Date (with the possible dates as states) will have a very high information gain but is unable to generalize! One approach for avoiding this problem is to select attributes ($X$) based on the Gain Ratio (for a given set of examples $S$):
$$
\text{GainRatio}(X) = \frac{\text{InformationGain}(X)}{\text{SplitInformation}(S, X)}.
$$
The Split Information is defined as:
$$
\text{SplitInformation}(S, X) = - \sum_{i=1}^{c} \frac{|S_i|}{|S|} \log_2 \left( \frac{|S_i|}{|S|} \right),
$$
where $S_i$ is the subset of $S$ for which attribute $X$ takes the $i$-th value, and $c$ is the number of distinct values of attribute $X$.


## Basic models for supervised learning

### Decision tree

A decision tree is a simple representation for classifying examples. Decision tree learning is one of the simplest useful techniques for supervised classification learning.

A decision tree is a tree in which:
- each internal (non-leaf) node is labeled with a condition, a Boolean function of examples,
- each internal node has two branches, one labeled true and the other false,
- each leaf of the tree is labeled with a point estimate 

Decision trees are also called $\textit{classification trees}$ when the target (leaf) is a classification, and $\textit{regression trees}$ when the target is real-valued.

### Linear regression and classification

Linear regression is the problem of fitting a linear function to a set of training examples, in which the input and target features are real numbers. Suppose the input features, $X_1, \dots, X_m$, are all real numbers (which includes the $\{0, 1\}$ case) and there is a single target feature $Y$. A linear function of the input features is a function of the form
$$
\hat{Y}_w(e) = w_0 + w_1 \cdot X_1(e) + \cdots + w_m \cdot X_m(e)
$$
or equivalently,
$$
\hat{Y}_w(e) = \sum_{i=0}^{m} w_i \cdot X_i(e)
$$
where $w = (w_0, w_1, \dots, w_m)$ is a vector (tuple) of weights, and $X_0$ is a special feature whose value is always 1.

Suppose $E_s$ is a set of examples. The mean squared loss on examples $E_s$ for target $Y$ is the error
$$
\text{error}(E_s, w) = \frac{1}{|E_s|} \sum_{e \in E_s} (\hat{Y}_w(e) - Y(e))^2
$$
or equivalently,
$$
\text{error}(E_s, w) = \frac{1}{|E_s|} \sum_{e \in E_s} \left( \sum_{i=0}^{m} w_i \cdot X_i(e) - Y(e) \right)^2 \quad \text{(7.1)}
$$

Consider minimizing the mean squared loss. There is a unique minimum, which occurs when the partial derivatives with respect to the weights are all zero. The partial derivative of the error in Equation (7.1) with respect to weight $w_i$ is
$$
\frac{\partial}{\partial w_i} \text{error}(E_s, w) = \frac{1}{|E_s|} \sum_{e \in E_s} 2 \cdot \delta(e) \cdot X_i(e) \quad \text{(7.2)}
$$
where $\delta(e) = \hat{Y}_w(e) - Y(e)$, a linear function of the weights.


Consider binary classification, where the target variable is in the domain $\{0, 1\}$. A linear function does not work well for such tasks, as predictions could be outside the range [0, 1]. For example, a linear model might predict a value like 3 to fit other examples better.

A squashed linear function is of the form
$$
\hat{Y}_w(e) = \phi\left(w_0 + w_1 \cdot X_1(e) + \cdots + w_m \cdot X_m(e)\right)
$$
or equivalently,
$$
\hat{Y}_w(e) = \phi\left(\sum_i w_i \cdot X_i(e)\right),
$$
where $\phi$ is an activation function that maps the real line $(-\infty, \infty)$ into a subset of the real line, such as $[0, 1]$. A prediction based on a squashed linear function is a linear classifier.

One common differentiable activation function is the **sigmoid** function:
$$
\text{sigmoid}(x) = \frac{1}{1 + \exp(-x)},
$$
where $\exp(v) = e^v$, with $e$ being Euler’s number (approximately 2.718). The sigmoid function squashes the real line into the interval $(0, 1)$, making it appropriate for classification. It is also differentiable, with the derivative:
$$
\frac{d}{dx} \text{sigmoid}(x) = \text{sigmoid}(x) \cdot (1 - \text{sigmoid}(x)).
$$
Suppose the target $Y$ is categorical with domain represented by the tuple of values $(v_1, \dots, v_k)$. The softmax function takes a vector (tuple) of real numbers $(\alpha_1, \dots, \alpha_k)$ and returns a vector of the same size, where the $i$-th component of the result is
$$
\text{softmax}((\alpha_1, \dots, \alpha_k))_i = \frac{\exp(\alpha_i)}{\sum_{j=1}^{k} \exp(\alpha_j)}.
$$
This ensures that the resulting values are all positive and sum to 1, so they can be considered as a probability distribution.





# Lecture 06: Neural networks

A linear function takes a vector $\textbf{in}$ of values for the inputs to the layer (and, as in linear regression, an extra constant input that has value “1”), and returns a vector $\textbf{out}$ of output values, so that: $$ \text{out}[j] = \phi\left(\sum_{k} \text{in}[k] \cdot w[k, j]\right) $$ where $w$ is a two-dimensional array of weights. The weight associated with the extra constant input $1$ is the bias. There is a weight $w[i, j]$ for each input–output pair of the layer, plus a bias for each output. The outputs of one layer become the inputs to the next layer.

A common activation function for hidden layers is the rectified linear unit (ReLU), defined by: $$ \phi(x) = \max(0, x) $$ That is: $$ \phi(x) = \begin{cases} 0 & \text{if } x < 0 \\ x & \text{if } x \geq 0 \end{cases} $$ The function $\phi$ has a derivative of $0$ for $x < 0$ and $1$ for $x > 0$. Although it does not have a derivative at $x = 0$, assume the derivative is $0$ at that point. If all the hidden layers use ReLU activation, the network implements a piecewise linear function.


We want to find the value of the parameters $w$ that minimize the sum of squared errors (SSE): $$ \text{SSE} = \sum_{i=1}^{M} \left( y_i - o_i \right)^2 = \sum_{i=1}^{M} \left( y_i - \sum_{j=1}^{N} x_{i,j} w_j \right)^2 $$ We define the error function as: $$ E(w) = \frac{1}{2} \sum_{i=1}^{M} \left( y_i - \sum_{j=1}^{N} x_{i,j} w_j \right)^2 $$
Notes: 1. We multiply by $\frac{1}{2}$ because it simplifies the derivative. This is fine because the minimum remains the same.

Intuition to Update the Weights

- If $\nabla E > 0$: The output $o$ should be **increased**, so $x \cdot w$ goes **up**.  
  The weight update rule is:

  $$
  w := w + \alpha \nabla E x
  $$

- If $\nabla E < 0$: The output $o$ should be **decreased**, so $x \cdot w$ goes **down**.  
  The weight update rule is:

  $$
  w := w + \alpha \nabla E x
  $$

Hyperparameter: Learning Rate $\alpha$
The parameter $\alpha$ is called the **learning rate**:

- $\alpha$ controls how much the parameters are updated at each iteration.


![[Pasted image 20250111171641.png]]

Two-Step Computation in Neural Networks 1. **Combine inputs as a weighted sum**: $$ a_j = \sum_i x_i \cdot w_{i,j} $$ 2. **Compute the output by applying an activation function to the combined inputs**: $$ o_j = \phi(a_j) $$ 
Key Points to Remember: - The input $x_0$ is always the constant value $1$ (bias term). 
Summary: 1. Each neuron applies a **linear function** (like in linear regression) and then applies an **activation function**. 2. The results from **multiple neurons** are combined, with each neuron having its own set of weights.


The gradient of the sum of squared errors (SSE) with respect to the weights is defined as: $$ \nabla \text{SSE}(w) = \left( \frac{\partial \text{SSE}}{\partial w_0}, \dots, \frac{\partial \text{SSE}}{\partial w_n} \right) $$It specifies the **direction of steepest increase** in SSE. ### Weight Update Rule: To minimize the SSE, our new training rule becomes: $$ w_i := w_i + \Delta w_i $$ where: $$ \Delta w_i = -\alpha \frac{\partial \text{SSE}}{\partial w_i} $$ Explanation: - $\nabla \text{SSE}(w)$ represents the gradient of the error function. - $\alpha$ is the **learning rate**, which controls the size of the weight updates. - The term $-\alpha \frac{\partial \text{SSE}}{\partial w_i}$ ensures we move in the direction of **steepest decrease** in SSE.

#  Lecture 07: Other Supervised Learning Approaches and Evaluation of Supervised Learning

We can use **Bayesian Networks** as a machine learning model. 
### Example: Spam Classification Classify an email as **spam** if:
$$ P(\text{Spam} = \text{yes} \mid X = x) > \text{threshold} $$ where: - $X = (\text{abacus}, \dots, \text{zytogenic})$ represents a set of features (words in the email). - $x$ is the corresponding set of **yes/no values** indicating the presence or absence of each feature. 
### Assumption: We will assume the **simplest structural assumption** for the Bayesian Network.

### Input Features:
The input features are based on the **word occurrence** in emails, where each feature corresponds to a possible word. Here is an example of the data format:

| Email ID | abacus | ... | informatics | ... | pills | ... | watch | ... | zytogenic | Spam |
|----------|--------|-----|-------------|-----|-------|-----|-------|-----|-----------|------|
| m1       | n      | ... | y           | ... | n     | ... | n     | ... | n         | yes  |
| m2       | n      | ... | n           | ... | n     | ... | n     | ... | n         | yes  |
| m3       | n      | ... | n           | ... | n     | ... | y     | ... | n         | yes  |
| m4       | n      | ... | n           | ... | n     | ... | n     | ... | y         | no   |
| m5       | n      | ... | n           | ... | y     | ... | n     | ... | yes       | yes  |
| m6       | n      | ... | n           | ... | n     | ... | n     | ... | yes       | yes  |
| m7       | n      | ... | n           | ... | n     | ... | n     | ... | yes       | no   |
| m8       | n      | ... | n           | ... | n     | ... | n     | ... | yes       | yes  |
| m9       | n      | ... | y           | ... | y     | ... | n     | ... | yes       | yes  |

---

### Bayesian Network for Spam Classification:

We can use **Bayesian Networks** as a machine learning model to classify emails as spam.

In this example:

- Classify an email as **spam** if:

$$
P(\text{Spam} = \text{yes} \mid X = x) > \text{threshold}
$$

where:

- $X = (\text{abacus}, \dots, \text{zytogenic})$ represents the word occurrences in the email (binary values: yes/no for each word).
- $x$ is the corresponding set of **yes/no values** indicating the presence or absence of each word.

### Assumption:
We assume the simplest structural assumption for the Bayesian Network:

$$
P(a_1, \dots, a_n, \text{Spam}) = P(a_1 \mid \text{Spam}) \cdot P(a_2 \mid \text{Spam}) \cdot \dots \cdot P(a_n \mid \text{Spam}) \cdot P(\text{Spam})
$$

This representation captures the relationship between each word ($a_1, a_2, \dots, a_n$) and the class label **Spam**.

Noise in data may lead to a bad classifier. In particular, if the **decision tree** fits the data perfectly, this is called **overfitting**.

### Definition:
A hypothesis $h$ is said to **overfit** the training data if there exists an alternative hypothesis $h'$ such that:

- $h'$ has a smaller error than $h$ over the training data.
- However, $h$ has a smaller error than $h'$ over the entire distribution of instances.



# Lecture 8. Unsupervised Learning: Clustering

## K-Means Clustering

We consider the scenario where the number $k$ of clusters is known. We have a distance measure $d(x_i, x_j)$ between pairs of data points (feature vectors). We can calculate a **centroid** for a collection of data points $S = \{x_1, \dots, x_n\}$.

### K-Means Algorithm:
1. **Initialize**: Randomly pick $k$ data points as initial cluster centers $c = \{c_1, \dots, c_k\}$ from $S$.
2. **Repeat**:
   - Form $k$ clusters by assigning each point in $S$ to its closest centroid.
   - Recompute the centroid for each cluster.
3. **Until**: Centroids do not change.

---

## K-Means as an Optimization Problem

Assume that we use the **Euclidean distance** $d$ as a proximity measure and that the quality of the clustering is measured by the **sum of squared errors** (SSE):

$$
\text{SSE}_k = \sum_{x \in C_i} d(c_i, x)^2
$$

where:

- $c_i$ is the $i$'th centroid.
- $C_i \subseteq S$ is the set of points closest to $c_i$ according to $d$.

In principle, we could minimize the SSE by looking at all possible partitionings. However, this is **not feasible**! Instead, the centroid that minimizes the SSE is the mean of the data points in that cluster:

$$
c_i = \frac{1}{|C_i|} \sum_{x \in C_i} x
$$

---

## Clustering Evaluation

A clustering algorithm applied to a dataset will return a clustering, even if there is **no meaningful structure** in the data.

### Questions:
- **Do the clusters actually correspond to meaningful groups** of data instances?
- **Are all the clusters relevant**, or are there some real and some meaningless clusters?

### Two Types of Evaluation:
1. **Supervised Evaluation**
2. **Unsupervised Evaluation**


# Lecture 9: search 


### Definition: Admissibility
Let $\Pi$ be a problem with state space $\Theta$ and states $S$, and let $h$ be a heuristic function for $\Pi$. We say that $h$ is **admissible** if, for every state $s \in S$, we have:

$$
h(s) \leq h^*(s)
$$

- **What does this mean?**  
  An admissible heuristic **never overestimates** the true cost to reach the goal from any state. It gives a **lower bound** on the cost to the goal, meaning it’s always an estimate that’s equal to or less than the actual cost.

- **Example**:  
  Imagine you're on a road trip, trying to get from City A to City B. The straight-line (or "as-the-crow-flies") distance from City A to City B is 100 miles, but you can’t drive directly. The actual driving distance is 120 miles.

  - The **straight-line distance** is the heuristic, $h(s) = 100$ miles.
  - The **actual driving distance** is $h^*(s) = 120$ miles.

  Since the heuristic never overestimates the real cost, $h(s) = 100 \leq h^*(s) = 120$, it is admissible.

---

### Definition: Consistency
We say that $h$ is **consistent** (or **monotonic**) if, for any two states $s$ and $s'$ connected by an action $a$, the following holds:

$$
h(s) - h(s') \leq c(a)
$$

where $c(a)$ is the cost of the action $a$ that moves from $s$ to $s'$.

- **What does this mean?**  
  A consistent heuristic ensures that the value of the heuristic never decreases by more than the cost of taking an action. In other words, when you move from one state to another, the heuristic value can only drop by an amount that is less than or equal to the cost of that action.

- **Example**:  
  Suppose you're moving from City A to City B, and the straight-line distance (heuristic) is 100 miles. You drive from City A to City C, which is 50 miles away, and then from City C to City B, which is 70 miles away.

  - The heuristic at City A is $h(\text{City A}) = 100$ miles.
  - The heuristic at City C is $h(\text{City C}) = 50$ miles.
  - The cost of the action (driving from City A to City C) is $c(a) = 50$ miles.

  After moving from City A to City C, the heuristic dropped from 100 to 50 miles. The decrease in the heuristic is:

  $$
  h(\text{City A}) - h(\text{City C}) = 100 - 50 = 50 \text{ miles}
  $$

  Since the cost of the action was also 50 miles, we have:

  $$
  50 \leq 50
  $$

  This satisfies the consistency condition, so the heuristic is consistent.

---

### Key Differences:
- **Admissibility**: The heuristic is safe and doesn’t overestimate the cost to the goal.
- **Consistency**: The heuristic behaves smoothly, meaning its value only changes in a way that makes sense with the costs of the actions.

If a heuristic is consistent, it’s also admissible. But not all admissible heuristics are consistent.


# Lecture: 10. Classical Planning


# Lecture: 11. Multi-Agent Systems: Adversarial Search and Game Theory
## 2-Player Zero-Sum Game

A **2-player zero-sum game** is a game where two players compete, and one player's gain is exactly equal to the other player's loss. The sum of their payoffs is always zero. In other words, if one player wins points, the other player loses the same amount.

Mathematically:
$$
P_1 + P_2 = 0
$$
Where:
- $P_1$ is Player 1's payoff.
- $P_2$ is Player 2's payoff.

In these games, players make decisions to maximize their own payoffs while minimizing the opponent's payoff.

---

# Minimax Strategy
The **minimax strategy** is a decision-making rule used to minimize the possible loss for a worst-case scenario. In zero-sum games, it involves:

1. **Player 1 (Maximizer)**: Wants to maximize their minimum possible payoff.
2. **Player 2 (Minimizer)**: Wants to minimize Player 1's maximum possible payoff.

### Minimax Process:
1. Evaluate the payoffs for each possible combination of strategies.
2. Find the worst-case scenario for each player.
3. Choose the strategy that results in the best of the worst-case payoffs.

---

# Decision Tree Example
A **decision tree** visually represents the possible decisions and their corresponding outcomes. Here's a general idea of what a decision tree might look like for a 2-player zero-sum game:

             Player 1
            /      \
       A          B
    /   \      /   \
  Player 2  Player 2  Player 2  Player 2
   /   \    /   \    /   \    /   \
  X     Y  X     Y  X     Y  X     Y
 (3,-3) (-2,2) (-1,1) (4,-4)

In this tree:
- **Player 1** can choose **A** or **B**.
- **Player 2** can choose **X** or **Y** in response.
- The payoffs are shown in parentheses, where the first number is Player 1's payoff and the second is Player 2's payoff.

---

# Payoff Table
Below is the payoff table for a 2x2 zero-sum game between Player 1 and Player 2. The first number in each cell is Player 1's payoff, and the second number is Player 2's payoff (the negative of Player 1's payoff).

table  

|           | Player 2: X | Player 2: Y |  
|-----------|-------------|-------------|  
| Player 1: A | (3, -3)     | (-2, 2)     |  
| Player 1: B | (-1, 1)     | (4, -4)     |

---

# Nash Equilibrium
The two strategies are in **Nash Equilibrium** when no player can improve their utility by switching their strategy while the other player keeps theirs unchanged.

This means:
- An **agent will stick to a strategy** when it knows the other player's strategy.
- **No player has an incentive to deviate** from their chosen strategy once they know what the other player is doing.

### Key Properties of Nash Equilibrium:
1. If every player maximizes their own utility, the game will tend to a Nash Equilibrium.
2. **The Nash Equilibrium is not always unique.** There may be multiple Nash Equilibriums in a game.

---

# Example of Nash Equilibrium
Consider the following payoff table for a 2-player game:

table  

|           | Player 2: X | Player 2: Y |  
|-----------|-------------|-------------|  
| Player 1: A | (2, -2)     | (0, 0)      |  
| Player 1: B | (1, -1)     | (3, -3)     |

In this game:
- If **Player 1 chooses A** and **Player 2 chooses X**, the payoff is **(2, -2)**. If Player 1 switches to B, their payoff will drop to 1. Therefore, Player 1 has no incentive to switch from A.
- If **Player 2 chooses X** and **Player 1 chooses A**, the payoff is **(-2)** for Player 2. If Player 2 switches to Y, their payoff will drop to **0**. Therefore, Player 2 has no incentive to switch from X.

Thus, **(A, X)** is a Nash Equilibrium because neither player can improve their payoff by unilaterally changing their strategy.

---

# Summary
- **Zero-sum game**: One player's gain equals the other player's loss.
- **Minimax strategy**: Each player chooses a strategy to minimize their worst-case loss.
- **Decision tree**: A visual representation of the game decisions and outcomes.
- **Payoff table**: A structured way to represent the possible payoffs for both players based on their choices.
- **Nash Equilibrium**: A situation where no player can improve their utility by changing their strategy unilaterally.


# Lecture: 12. Planning under Uncertainty: Markov Decision Processes

## Problem:
Sum of rewards over an infinite horizon is often infinite, no matter how much you wait to start gaining reward.

### Two solutions:
- Finite Horizon
- Discounted Rewards

### Finite-Horizon MDP
Consider only the rewards obtained in the first $k$ states:
$$
U(s_0, s_1, s_2, \dots) = R(s_0) + R(s_1) + \dots + R(s_k) < \infty.
$$
But how do we choose $k$?
- For $k = 0$, we only care about the immediate reward, hence we pursue a very greedy strategy.
- For $k = 5$, we only care about maximizing the reward for the next 5 time steps (but we may end in a really bad state for the future).

**Finite horizon MDPs** = Live your life as if there were not tomorrow.

Weigh rewards in the immediate future higher than rewards in the distant future:
$$
U(s_0, s_1, s_2, \dots) = R(s_0) + \gamma R(s_1) + \gamma^2 R(s_2) + \dots,
$$
where $0 \leq \gamma \leq 1$.

Possible interpretations of the discounting factor $\gamma$:
- In economics, $\gamma$ may be thought of as inflation or an interest rate.
- The decision process may terminate with probability $(1 - \gamma)$ at any point in time (e.g., the robot breaking down).

Thanks to increasing the exponent in $\gamma$ after every step, the sum of rewards is always finite!

With $\gamma < 1$, we have:
$$
U(s_0, s_1, s_2, \dots) = \sum_{i=0}^{\infty} \gamma^i R(s_i).
$$
For $\gamma = 0$, we have a greedy strategy:
$$
\sum_{i=0}^{\infty} \gamma^i R(s_i) \leq \sum_{i=0}^{\infty} \gamma^i R(s_i).
$$
For $\gamma = 1$, we have normal additive rewards:
$$
\gamma \max R = \max R \cdot \frac{1}{1 - \gamma} < \infty.
$$
So, expected discounted reward is a good metric to compare policies. Typically, we want values $\gamma < 1$ but $\gamma \approx 1$, such as $\gamma = 0.99$.

### Given a discounted MDP $(S, A, r, P, I, ST, \gamma)$, $s \in S$, and a policy $\pi$ closed in $s$, the value of $s$ under $\pi$ is:
$$
V^\pi(s) = \mathbb{E}[r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \dots] = \mathbb{E} \left[\sum_{i \geq 0} \gamma^i r_{t+i}\right],
$$
where $r_{t+i} = R(s_{t+i})$, given a state sequence $s_t, s_{t+1}, \dots$ induced by $\pi$ and $T$ starting from $s = s_t$, and the expectation is over these sequences.

### Definition (V$^*$): 
Given a discounted MDP $(S, A, r, P, I, ST, \gamma)$, the optimal value function $V^*$ is defined as:
$$
V^*(s) = \max_\pi V^\pi(s).
$$

### Theorem (The Bellman Equation):
Given a discounted MDP $(S, A, r, P, I, ST, \gamma)$, for every $s \in S$, it holds that:
$$
V^*(s) = R(s) + \max_{a \in A} \gamma \sum_{s' \in S} P(s'|s,a)V^*(s').
$$
Optimal state value = immediate reward + best action’s (discounted) expected successor state value.

**Uses of the Bellman equation:**
- Bellman state update: given value function $V$, set:
$$
V(s) \leftarrow R(s) + \max_{a \in A} \gamma \sum_{s' \in S} P(s'|s,a)V(s').
$$
Such updates (starting from any $V$) converge to $V^*$. Compute an optimal policy:
$$
\pi^*(s) = \arg\max_{a \in A} \gamma \sum_{s' \in S} P(s'|s,a)V^*(s').
$$

- Bellman operator: given value function $V$, the function $BV$ is defined by:
$$
BV(s) = R(s) + \max_{a \in A} \gamma \sum_{s' \in S} P(s'|s,a)V(s')
$$
for all $s$. Applies Bellman state update to all states in parallel.

### In general, in a Markov decision process:
- The world is fully observable, i.e., the agent can observe the true state of the world at any point in time.
- The uncertainty in the system is a result of the consequences of the actions being non-deterministic (when performing an action, we make a state transition with a certain probability, but independent of the time step).
- For each decision, we get a reward (which may be negative) that may depend on the current world state but is independent of the time step.

### Instead of updating the utility function, make an initial guess at the optimal policy and perform an iterative refinement of this guess:
- The updating function:
$$
\pi_{i+1}(s) := \arg\max_{a \in S} P(s'|a,s) U_{\pi_i}(s').
$$
- The evaluation function:
$$
U_{\pi_i}(s) = R(s) + \gamma \sum_{s' \in S} P(s'|\pi_i(s),s) U_{\pi_i}(s'),
$$
which defines a system of linear equalities; the solution is $U_{\pi_i}$.


# Lecture: 13 Reinforcement learning

## Model-free Reinforcement Learning
We do not need to learn how the environment works. It may be enough to learn what to do in each state.

In the previous lecture, we considered:

- Value function $V^*(s)$: expected utility starting in $s$ and afterwards acting optimally.
$$
V^*(s) = R(s) + \max_{a \in A} \gamma.
$$

Here, we consider instead:
$$
P(s'|s,a)V^*(s').
$$

- Q-value $Q^*(s,a)$: expected utility starting in $s$, applying action $a$, and afterwards acting optimally.
$$
Q^*(s,a) = R(s) + \gamma \sum_{s'|s,a} P(s'|s,a)V^*(s').
$$

We can still get $V$ from $Q$:
$$
V^*(s) = \max_a Q^*(s,a).
$$

### So, what is the advantage of considering Q-values?
We know what the best action is without knowing the transition relation:
$$
\arg\max_a Q^*(s,a).
$$

### Q-learning
Learn an approximate model of $Q^*(s,a)$ directly. Update current estimate $Q$ of $Q^*$ after each experience $\langle s_t, a_t, r_t, s_{t+1} \rangle$.

**Q-learning update**: After $\langle s, a, r, s' \rangle$, update $Q(s,a)$:
$$
Q(s,a) \leftarrow (1-\alpha) \cdot Q(s,a) + \alpha \left(r + \gamma \max_{a'} Q(s',a')\right).
$$

We do not need to know the transition probabilities or the reward function, because we get $s'$ and $r$ directly by sampling the environment.

- $\alpha$ is the learning rate. It is a parameter in $[0,1]$ that controls how much we weight our previous experiences and the new one.
