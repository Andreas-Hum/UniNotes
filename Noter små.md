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


  
# Lecture 03: Reasoning under Uncertainty and Bayesian Networks

