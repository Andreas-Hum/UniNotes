
# Basics
## 📘 Propositional Logic – Exam Notes [[Noter Og Andet#3. Propositional Logic| her for mere som hvordan man kan omskrive]]

### The sat problem 

- Propositional Logic: Satisfiability can refer to many different logics. In this course, we focus on one of the simplest! 
- Satisfiable: A formula is satisfiable if it is possible to find an interpretation (assignment) that makes the formula true.
### 🔹 Syntax

Let **Σ** be a set of **atomic propositions** (also called **atoms**, i.e., Boolean variables).

**Σ-formulas** are defined inductively:
1. **⊥** and **⊤** are Σ-formulas.  
   → ⊥ means "false", ⊤ means "true".
2. Each **P ∈ Σ** is a Σ-formula.  
   → Atomic propositions (like P, Q, R).
3. If **ϕ** is a Σ-formula, then so is **¬ϕ**.  
   → Negation: "not ϕ".
4. If **ϕ** and **ψ** are Σ-formulas, then so are:
   - **ϕ ∧ ψ** (*conjunction*)  
     → "ϕ and ψ" are both true.
   - **ϕ ∨ ψ** (*disjunction*)  
     → At least one of ϕ or ψ is true.
   - **ϕ → ψ** (*implication*)  
     → If ϕ is true, then ψ must be true.
   - **ϕ ↔ ψ** (*equivalence*)  
     → ϕ and ψ have the same truth value.

**Notation**:
- **Literals** = Atoms and negated atoms.  
  → Basic building blocks of formulas.
- **Operator precedence**: `¬ > ∧ > ∨ > → > ↔`  
  → Negation binds tightest; use parentheses to be safe.

---

### 🔹 Semantics

#### Interpretation

An **interpretation** `I` of Σ (aka a **truth assignment**) is a function:

```
I : Σ → {1, 0}
```

→ It assigns each atom either **true (1)** or **false (0)**.

Truth rules:

- `I ⊨ ⊤`  
  → "True" is always satisfied.
- `I ⊭ ⊥`  
  → "False" is never satisfied.
- `I ⊨ P` iff `I(P) = 1`  
  → Atom is true if assigned 1.
- `I ⊨ ¬ϕ` iff `I ⊭ ϕ`  
  → Negation is true if ϕ is false.
- `I ⊨ ϕ ∧ ψ` iff `I ⊨ ϕ` **and** `I ⊨ ψ`  
  → Both must be true.
- `I ⊨ ϕ ∨ ψ` iff `I ⊨ ϕ` **or** `I ⊨ ψ`  
  → At least one must be true.
- `I ⊨ ϕ → ψ` iff if `I ⊨ ϕ` then `I ⊨ ψ`  
  → No true → false allowed.
- `I ⊨ ϕ ↔ ψ` iff `I ⊨ ϕ` **iff** `I ⊨ ψ`  
  → True together or false together.

> If `I ⊨ ϕ`, we say that **I satisfies ϕ**, or that **I is a model of ϕ**.  
> The set of all models of ϕ is denoted **M(ϕ)**.  
→ A **model** is an assignment of truth values to atoms that makes the formula ϕ true.

---

### 🔹 Terminology

- **Satisfiable**: ∃`I` such that `I ⊨ ϕ`  
  → ϕ is **true in at least one model**.
- **Unsatisfiable**: ¬∃ `I` such that `I ⊨ ϕ`  
  → ϕ is **never true**.
- **Falsifiable**: ∃ `I` such that `I ⊭ ϕ`  
  → ϕ is **false in at least one model**.
- **Valid**: ∀ `I`: `I ⊨ ϕ`  
  → ϕ is **true in all models** (tautology).

---

### 🔹 Equivalence & Entailment

- **Equivalence**:  
  `ϕ ≡ ψ` ⇔ `M(ϕ) = M(ψ)`  
  → ϕ and ψ are true in **exactly the same models**.

- **Entailment**:  
  `ϕ ⊨ ψ` ⇔ `M(ψ) ⊆ M(ϕ)`  
  → **ϕ being true guarantees that ψ is also true**.

![[Noter Og Andet#3.3 Logical Equivalences]]

### Normal forms
![[Pasted image 20250529175824.png]]



## Clausal form
![[Pasted image 20250529190110.png]]![[Pasted image 20250529190137.png]]
## 🧠 DPLL Algorithm – Step-by-Step Exam Guide

Use this to determine if a CNF formula is SATISFIABLE or UNSATISFIABLE.

---

### ✅ Input
A propositional formula in **Conjunctive Normal Form (CNF)**, e.g.:
```
(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ C) ∧ (¬C)
```

---

### 🔁 DPLL Procedure

#### 🔍 Unit Propagation
   - If there's a clause with a single literal (a **unit clause**), assign the value that satisfies it.
   - Propagate this assignment (i.e., simplify other clauses).
   - Repeat until no unit clauses are left.

#### 🔍 Pure Literal Elimination (optional but helpful)
   - If a variable appears **only as A** or **only as ¬A**, assign it to satisfy all such clauses.
   - Repeat if new pure literals appear.

#### 🔨 Splitting Rule
   - If no unit clauses or pure literals are left, pick an unassigned variable.
   - Try assigning it `True` and recursively apply DPLL.
   - If that fails, backtrack and try `False`.

#### 🚫 Contradiction Check
   - If **any clause becomes false** (all literals in it are false), that path is a dead end.
   - Backtrack and try the other branch.
   - If **all branches fail**, the formula is **UNSATISFIABLE**.

#### 🎯 Success Condition
   - If **all clauses are satisfied** (i.e., simplified away), return SATISFIABLE with the assignment.

---

### 🧪 Example (UNSAT):

**Formula**:
```
(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ C) ∧ (¬C)
```

**Step-by-step**:
- Unit clause: `¬C` → `C = False`
- Substitute: `(¬A ∨ False)` → `¬A`, `(¬B ∨ False)` → `¬B`
- Unit clauses: `¬A` → `A = False`, `¬B` → `B = False`
- Check `(A ∨ B)` → `False ∨ False` = ❌ contradiction
→ **UNSAT**

---

### ✅ Example (SAT):

**Formula**:
```
(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)
```

**Step-by-step**:
- No unit clauses or pure literals
- Split on `A = True`
- `(A ∨ B)` → satisfied
- `(¬A ∨ C)` → `False ∨ C` → becomes `C` → unit clause → `C = True`
- `(¬B ∨ ¬C)` → becomes `(¬B ∨ False)` → `¬B` → unit clause → `B = False`
→ All clauses satisfied with:

Assignment:
- `A = True`, `B = False`, `C = True`

✔️ **SATISFIABLE**

---

### 🧾 Tips for Exam
- Start with unit propagation every time.
- Simplify clauses immediately after each assignment.
- If stuck, pick a variable and split (backtracking will handle the rest).
- If any clause is fully false, prune the branch.
- If all clauses disappear (all satisfied), you're done — it’s SAT!


## ⚙️ CDCL Algorithm – Step-by-Step Exam Guide (Conflict-Driven Clause Learning)

Use this to determine if a CNF formula is **SATISFIABLE** or **UNSATISFIABLE** — like DPLL, but with **learning** and **non-chronological backtracking**.

---

### ✅ Input
A propositional formula in **Conjunctive Normal Form (CNF)**, e.g.:
```
(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ C) ∧ (¬C)
```

---

### 🧭 CDCL Procedure

#### 🔍 Unit Propagation (Boolean Constraint Propagation / BCP)
   - If there's a **unit clause**, assign its value.
   - Propagate this assignment (simplify other clauses).
   - Continue until:
     - No unit clauses are left, or
     - **A conflict is detected** (clause becomes false).

#### 🚨 Conflict Detection
   - If a clause is **false** under current assignments → **conflict**!

#### 📈 Implication Graph
   - A directed graph showing how each assignment was derived.
   - **Nodes** = variable assignments (with decision level).
   - **Edges** = cause → effect (which clause caused this assignment).
   - **Conflict** = a node where all incoming literals are false.

#### 🧠 Conflict Analysis
   - Use the implication graph to analyze the conflict.
   - Identify the **First UIP (Unique Implication Point)** — key node to cut the conflict.
   - From this, **learn a new clause** (called a learned clause or conflict clause):
     - This clause **prevents this exact conflict** in the future.

#### 🏃 Non-Chronological Backtracking (Backjumping)
   - Backtrack to the **decision level** where the learned clause becomes unit.
   - Do NOT just go back step-by-step — jump over irrelevant decisions.

#### 🔄 Continue
   - Add the learned clause to the formula.
   - Repeat:
     - Unit propagation
     - Conflict detection
     - Learning + backjumping
   - Until either:
     - All clauses satisfied → **SATISFIABLE**
     - Conflict at level 0 → **UNSATISFIABLE**

---

### 🧪 Example Flow (Abstract):

**Formula** (with **named clauses** — this helps a LOT!):
```
C1: (A ∨ B)  
C2: (¬A ∨ C)  
C3: (¬B ∨ C)  
C4: (¬C)
```

**Steps**:
1️⃣ Decide `A = True` (Decision level 1)  
2️⃣ Propagate using `C2`:  
   - `C2` → `C = True`
3️⃣ Propagate using `C4`:  
   - `C4` conflicts with `C = True` → CONFLICT!

**Implication Graph**:
```
[A=True] --(C2)--> [C=True] --(C4)--> CONFLICT
```

**Learned Clause**: `(¬A)`  
**Backjump** to level 0, assign `A=False` → continue search.

---

### 🎯 Success Condition
- If all clauses satisfied → **SATISFIABLE** + assignment.
- If conflict at level 0 and cannot learn any useful clause → **UNSATISFIABLE**.

---

### 📝 Why Naming Clauses Helps
- **Always number or name clauses** (C1, C2, ...), e.g. on paper or in exam.
- This makes it MUCH easier to:
  - Build the **implication graph**.
  - Write cause → effect edges.
  - Trace where each assignment came from.
  - Perform **conflict analysis** clearly.
- Without names, it's easy to get lost in the graph!

---

### 🧾 Tips for Exam
- CDCL = DPLL + learning + backjumping!
- Always:
  - Propagate (BCP).
  - Detect conflicts.
  - Build implication graph.
  - Learn clause.
  - Backjump.
- **Implication graph = key to learning** — visualize cause → effect.
- Non-chronological backtracking avoids useless work!
- If conflict at level 0 → UNSAT.
- **Name your clauses!** (C1, C2, ...) — it will save you time.

---

### ⚠️ Difference vs. DPLL
| DPLL                 | CDCL                       |
|----------------------|----------------------------|
| No clause learning   | Learns clauses dynamically |
| Chronological backtrack | Non-chronological backjump |
| Simpler, can be slow  | Faster, modern SAT solvers |

---
# ⚙️ BDD Model Counting – Step-by-Step Guide  
### (For $mc(f) = 2^{j-i-1} \cdot mc(f_0) + 2^{k-i-1} \cdot mc(f_1)$)

---

### ✅ What is $MC(f)$?

$MC(f)$ = number of total assignments that make $f = \text{True}$.  
You compute it by **walking the BDD recursively** using this formula.

---

### 🧭 Procedure

#### 1️⃣ Build BDD (with variable order)

Each node = $f = (x_i, f_0, f_1)$:

| Term | Meaning |
|------|---------|
| $x_i$ | current variable at this node |
| $f_0$ | LOW branch ($x_i = 0$) |
| $f_1$ | HIGH branch ($x_i = 1$) |

---

#### 2️⃣ Label each node with $v(f)$

| Term | Meaning |
|------|---------|
| $v(f)$ | index of first variable appearing in the subtree under node $f$ |
| $v(\text{True}), v(\text{False})$ | defined as $n+1$ (one level after last variable) |

---

#### 3️⃣ Use this formula:

$$
mc(f) = 2^{v(f_0)-i-1} \cdot mc(f_0) + 2^{v(f_1)-i-1} \cdot mc(f_1)
$$

Where:

| Term                               | Meaning |
| ---------------------------------- | ------- |
| $j = v(f_0)$                       |         |
| $k = v(f_1)$                       |         |
| $i$ = current variable at node $f$ |         |

---

#### 4️⃣ Base cases (terminals):

$$
mc(\text{True}) = 1 \\
mc(\text{False}) = 0
$$

---

### 🚦 Why the $2^{j-i-1}$?

Because if there are **skipped variables** between $x_i$ and child,  
each skipped variable gives $2$ options → multiply accordingly.

---

## 🎓 Worked Example:  
$f(x_1, x_2, x_3) = (x_1 \lor x_3)$  
Variable order: $x_1 \rightarrow x_2 \rightarrow x_3$

---

## 🚀 BDD Structure:

```
               [x₁]
             /      \
          0 /        \ 1
           /          \
        [x₂]         [True]
       /    \
    0 /      \ 1
     /        \
  [x₃]       [x₃]
  /   \      /   \
F     T     F     T
```

---

## 🚀 Step-by-step labeling:

| Node | Variable | $v(f)$ |
|------|----------|--------|
| Root $[x_1]$ | $x_1$ | $1$ |
| $f_0 = [x_2]$ | $x_2$ | $2$ |
| $f_1 = [\text{True}]$ | terminal $\rightarrow 4$ |
| $[x_2]$ | $x_2$ | $2$ |
| $f_0 = [x_3]$ | $x_3$ | $3$ |
| $f_1 = [x_3]$ | $x_3$ | $3$ |
| $[x_3]$ | $x_3$ | $3$ |
| $f_0 = [\text{False}]$ | terminal $\rightarrow 4$ |
| $f_1 = [\text{True}]$ | terminal $\rightarrow 4$ |

---

## 🚀 Apply $mc(f)$ formula step by step:

### Step 1: Terminals

$$
mc(\text{True}) = 1 \\
mc(\text{False}) = 0
$$

---

### Step 2: $mc([x_3])$

$$
mc([x_3]) = 2^{4 - 3 - 1} \cdot mc(\text{False}) + 2^{4 - 3 - 1} \cdot mc(\text{True})
$$

Exponent: $4 - 3 - 1 = 0$ → $2^0 = 1$

$$
mc([x_3]) = 1 \cdot 0 + 1 \cdot 1 = 1
$$

---

### Step 3: $mc([x_2])$

$$
mc([x_2]) = 2^{3 - 2 - 1} \cdot mc([x_3]) + 2^{3 - 2 - 1} \cdot mc([x_3])
$$

Exponent: $3 - 2 - 1 = 0$ → $2^0 = 1$

$$
mc([x_2]) = 1 \cdot 1 + 1 \cdot 1 = 2
$$

---

### Step 4: $mc([x_1])$ → ROOT

$$
mc([x_1]) = 2^{2 - 1 - 1} \cdot mc([x_2]) + 2^{4 - 1 - 1} \cdot mc(\text{True})
$$

Exponents:

$2 - 1 - 1 = 0$ → $2^0 = 1$  
$4 - 1 - 1 = 2$ → $2^2 = 4$

$$
mc([x_1]) = 1 \cdot 2 + 4 \cdot 1 = 2 + 4 = 6
$$

---

## 🎉 FINAL RESULT:

$$
MC(f) = 6
$$

---

## 🚀 Does it match truth table?

YES! ✅

6 models where $f = 1$ → matches perfectly!

---

## 🚀 Summary of steps

1️⃣ Build BDD with variable order  
2️⃣ Label $v(f)$ for each node  
3️⃣ Apply:

$$
mc(f) = 2^{v(f_0)-i-1} \cdot mc(f_0) + 2^{v(f_1)-i-1} \cdot mc(f_1)
$$

4️⃣ Terminals:

$$
mc(\text{True}) = 1 
$$
$$mc(\text{False}) = 0$$

5️⃣ Work from leaves up to root  
6️⃣ Result at root = total model count

---

## 📝 Why $2^{j-i-1}$ ?

Because **BDD skips variables** (ROBDD is reduced).  
Skipped variables are free → each skipped variable gives 2 possibilities.  
So we multiply by $2^{\# \text{ skipped variables}}$ → this is exactly what $2^{j-i-1}$ is computing!

---

## 🚀 Final Mini Cheat Sheet

At each node $f = (x_i, f_0, f_1)$:

$$
mc(f) = 2^{v(f_0)-i-1} \cdot mc(f_0) + 2^{v(f_1)-i-1} \cdot mc(f_1)
$$

---

Terminals:

$$
mc(\text{True}) = 1 
$$
$$mc(\text{False}) = 0$$

---

$v(f)$:

$v(f)$ = index of first variable in subtree rooted at $f$

---

$v(\text{True}), v(\text{False})$:

$v(\text{True}) = n+1$  
$v(\text{False}) = n+1$

---
# ⚙️ APPLY – Full Step-by-Step Guide  
### Example: (x2 ∨ x1 ∨ x3) ∧ (x2 ∨ x3 ∨ x4)  
### Operation: AND

---

### ✅ Goal: 

We want to compute a BDD for:  
(x2 ∨ x1 ∨ x3) ∧ (x2 ∨ x3 ∨ x4)  

We will do this using:  

APPLY(AND, B_f, B_g)  

where:  

- B_f = BDD for (x2 ∨ x1 ∨ x3)  
- B_g = BDD for (x2 ∨ x3 ∨ x4)

---

### ✅ Variable order:

We need a variable order.  
**IMPORTANT**: Both BDDs must use the SAME variable order (this is called "compatible")  

We choose:  

x1 → x2 → x3 → x4

---

### ✅ Step 1: Build B_f and B_g

---

#### B_f = BDD for (x2 ∨ x1 ∨ x3)

This is a big OR → TRUE as soon as **any one** of these variables is TRUE.  

```
[x1]
 / \
[x2] T
 / \
[x3] T
 / \
F   T
```

---

#### B_g = BDD for (x2 ∨ x3 ∨ x4)

Same idea → TRUE as soon as **x2, x3, or x4** is TRUE.  

```
[x2]
 / \
[x3] T
 / \
[x4] T
 / \
F   T
```

---

### ✅ Step 2: What does APPLY do?

---

We call:  

APPLY(AND, B_f, B_g)

---

**How does APPLY work?**

At each step, APPLY looks at:  
- current node of B_f  
- current node of B_g  

and applies these rules:

---

### CASES:

---

#### CASE 1: Both are terminals (True or False)

Then:  
APPLY(AND, u_f, u_g) = u_f AND u_g  

Examples:  
APPLY(AND, True, True) = True  
APPLY(AND, True, False) = False  
APPLY(AND, False, False) = False  

---

#### CASE 2: Same variable

If: var(u_f) == var(u_g) == x_i  

Then:  
APPLY(AND, u_f, u_g) = new node for x_i with:  
- low branch = APPLY(AND, low(u_f), low(u_g))  
- high branch = APPLY(AND, high(u_f), high(u_g))  

---

#### CASE 3: var(u_f) < var(u_g)

Then:  
APPLY(AND, u_f, u_g) = new node for var(u_f) with:  
- low branch = APPLY(AND, low(u_f), u_g)  
- high branch = APPLY(AND, high(u_f), u_g)  

---

#### CASE 4: var(u_g) < var(u_f)

Then:  
APPLY(AND, u_f, u_g) = new node for var(u_g) with:  
- low branch = APPLY(AND, u_f, low(u_g))  
- high branch = APPLY(AND, u_f, high(u_g))  

---

### ✅ Step 3: APPLY on this example

---

**We start at roots**:
- B_f root = x1  
- B_g root = x2  

---

**Compare variables**:

var(x1) < var(x2)  
→ This is CASE 3.

---

### Step 4: First recursion

We build:  
```
[x1]  
/   \  
low  high
```

---

#### Left branch:

APPLY(AND, low(x1 of B_f), B_g)

This is: APPLY(AND, x2 (in B_f), x2 (in B_g))  

Now: variables SAME → CASE 2.

---

### Step 5: Recurse CASE 2 at x2

We now build:  
```
[x2]  
/   \  
low  high
```

---

#### Left branch:

APPLY(AND, low(x2 of B_f), low(x2 of B_g))  

This is: x3 (in B_f), x3 (in B_g) → SAME → CASE 2 again.

---

Keep going like this → the recursion will eventually reach:

- x4 vs terminal  
- terminal vs terminal → CASE 1 → return value.

---

### ✅ What is happening?

---

APPLY walks both BDDs:

- When variables are same → match up branches.  
- When variables are different → "delay" the one with higher variable.

---

### ✅ Final result:

The BDD you get represents:  

(x2 ∨ x1 ∨ x3) ∧ (x2 ∨ x3 ∨ x4)

---

### ✅ Why does this work?

- Because BDDs are **trees of decisions**.
- APPLY builds the **combined decision tree** for the new function.
- It does this by **zipping** the two BDDs together → walking both at the same time.

---

## ✅ Summary of APPLY:

---

| Rule   | Meaning                                    |
| ------ | ------------------------------------------ |
| CASE 1 | Both terminals → compute result directly   |
| CASE 2 | Same variable → recurse on both branches   |
| CASE 3 | var(u_f) < var(u_g) → recurse on u_f first |
| CASE 4 | var(u_g) < var(u_f) → recurse on u_g first |

---

**APPLY works for ANY binary operator**:  

- AND  
- OR  
- XOR  
- IMPLIES  
- EQUIVALENT  

---

**Unary operator**:  
- NEGATION: ¬f = f ⊕ 1

---

# ⚙️ How to Encode Problems as SAT – Step-by-Step Guide (with Examples)

---

### ✅ What is SAT solving?

SAT solving = finding an assignment of **Boolean variables** that makes a **Boolean formula** true.

The formula must be in **Conjunctive Normal Form (CNF)**:

$$
\text{CNF} = (clause_1) \land (clause_2) \land \dots \land (clause_n)
$$

Each clause is:

$$
(literal_1 \lor literal_2 \lor \dots)
$$

---

### 🎯 Goal:

**Encode your problem as a SAT formula**:

- If **satisfiable** → gives a solution.
- If **unsatisfiable** → proves no solution exists.

---

## 🧭 Step-by-step procedure (with examples):

---

### Step 1️⃣ What are your decision variables?

---

**Decision variables** = variables whose assignment **represents a solution**.

---

#### Examples:

- **Graph coloring:** $x_{v,c} =$ "node $v$ has color $c$"
- **Scheduling:** $x_{task,slot} =$ "task is in time slot"
- **Sudoku:** $x_{cell,value} =$ "cell contains value"

---

#### Auxiliary variables:

You can introduce **helper variables**:

Example:

$$
y = (x_1 \land x_2)
$$

Then encode:

$$
(y \rightarrow x_1) \land (y \rightarrow x_2) \land ((x_1 \land x_2) \rightarrow y)
$$

---

### 🚩 Rule of thumb:

👉 First think about what the solution looks like → define variables.

---

### Step 2️⃣ Build the CNF formula

---

### 🧱 Common Encoding Patterns

---

#### ✅ **Exactly one of (x₁ ... xₙ) is true**

##### Formula:

- **At least one true**:

$$
(x_1 \lor x_2 \lor \dots \lor x_n)
$$

- **At most one true**:

$$
(\neg x_i \lor \neg x_j) \quad \text{for all pairs } (i < j)
$$

---

#### ✅ **At least one true**

$$
(x_1 \lor x_2 \lor \dots \lor x_n)
$$

---

#### ✅ **At most one true**

$$
(\neg x_i \lor \neg x_j) \quad \text{for all pairs } (i < j)
$$

---

#### ✅ **If-then (implication)**

$$
x \rightarrow y \quad \equiv \quad (\neg x \lor y)
$$

---

#### ✅ **If-then-not**

$$
x \rightarrow \neg y \quad \equiv \quad (\neg x \lor \neg y)
$$

---

#### ✅ **Equivalence (iff)**

##### For **single variable** equivalence:

$$
x \leftrightarrow y
$$

Encode as:

$$
(\neg x \lor y) \land (x \lor \neg y)
$$

---

#### ✅ **AND equivalence**

##### $y \leftrightarrow (x_1 \land x_2)$

Encode as:

$$
(\neg y \lor x_1) \land (\neg y \lor x_2) \land (y \lor \neg x_1 \lor \neg x_2)
$$

---

#### ✅ **OR equivalence**

##### $y \leftrightarrow (x_1 \lor x_2)$

Encode as:

$$
(\neg x_1 \lor y) \land (\neg x_2 \lor y) \land (x_1 \lor x_2 \lor \neg y)
$$

---

#### ✅ **NOR equivalence**

##### $y \leftrightarrow \neg(x_1 \lor x_2)$

Encode as:

$$
(x_1 \lor x_2 \lor \neg y) \land (\neg x_1 \lor y) \land (\neg x_2 \lor y)
$$

---

#### ✅ **XOR equivalence**

##### $y \leftrightarrow (x_1 \oplus x_2)$

Encode as:

$$
(\neg x_1 \lor \neg x_2 \lor \neg y) \land (x_1 \lor x_2 \lor \neg y) \land (x_1 \lor \neg x_2 \lor y) \land (\neg x_1 \lor x_2 \lor y)
$$

---

#### ✅ **At most k true**

You can use **pairwise clauses**, or more efficiently:

- **Sequential counters**  
- **Cardinality networks**  
- **Totalizer encoding**

👉 (Advanced techniques — for now, know you can Google “SAT at-most-k encoding” for efficient versions!)

---

#### ✅ **Mutual exclusion (mutex)**

For variables $x_1, x_2, ..., x_n$, only **one** is allowed true:

$$
(\neg x_i \lor \neg x_j) \quad \forall i < j
$$

---

## 🚩 Rule of thumb:

👉 For **every constraint**, write CNF clauses.  
👉 All parts of the problem must be represented!

---

### Step 3️⃣ Solve and interpret result

---

#### Case 1: SAT → solution exists!

Example:

$$
x_{task_1,slot_3} = \text{True} \Rightarrow \text{Task 1 is in slot 3}
$$

---

#### Case 2: UNSAT → impossible!

Example:

- Sudoku: if **UNSAT**, puzzle is invalid (no solution).

---

### 🚩 Rule of thumb:

👉 Always know: **What does SAT mean? What does UNSAT mean?**  
👉 Be ready to **read the solution** from variable assignments.

---

## ✅ Final Summary

---

| Step | What to do |
|------|------------|
| Step 1 | Define decision variables (and auxiliary variables if needed) |
| Step 2 | Write CNF formula capturing the whole problem |
| Step 3 | Interpret SAT/UNSAT result |

---

## 🚦 Library of Common Encodings

---

| Pattern                        | Encoding                                                                      |
| ------------------------------ | ----------------------------------------------------------------------------- |
| **x → y**                      | $(\neg x \lor y)$                                                             |
| **x → ¬y**                     | $(\neg x \lor \neg y)$                                                        |
| **x ↔ y**                      | $(\neg x \lor y) \land (x \lor \neg y)$                                       |
| **y ↔ (x₁ ∧ x₂)**              | $(\neg y \lor x₁) \land (\neg y \lor x₂) \land (y \lor \neg x₁ \lor \neg x₂)$ |
| **y ↔ (x₁ ∨ x₂)**              | $(\neg x₁ \lor y) \land (\neg x₂ \lor y) \land (x₁ \lor x₂ \lor \neg y)$      |
| **y ↔ NOR(x₁, x₂)**            | $(x₁ \lor x₂ \lor \neg y) \land (\neg x₁ \lor y) \land (\neg x₂ \lor y)$      |
| **y ↔ XOR(x₁, x₂)**            | See detailed 4-clause form above                                              |
| **Exactly one of {x₁ ... xₙ}** | $(x₁ \lor \dots \lor xₙ) \land$ all pairwise $(\neg x_i \lor \neg x_j)$       |
| **At least one**               | $(x₁ \lor \dots \lor xₙ)$                                                     |
| **At most one**                | All pairwise $(\neg x_i \lor \neg x_j)$                                       |
| **Mutual exclusion**           | Same as at-most-one                                                           |
| **At most k true**             | Advanced: sequential counter, cardinality network                             |

---

## 🚦 Example applications:

- **Scheduling** → assign tasks to time slots
- **Graph coloring** → color nodes with constraints
- **Sudoku** → fill digits respecting puzzle rules
- **Puzzles and games** → encode valid solutions
- **Verification** → check if system meets specification
- **Circuit design** → check logic correctness
- **Resource allocation** → distribute resources legally
- **AI planning** → encode action sequences

---

### Final tips:

✅ Define variables so **you can read the solution**.  
✅ Break complex constraints into **small building blocks** (AND, OR, NOR, XOR, mutex, etc).  
✅ Practice with **small problems** → build intuition!


## ⚙️ Tseitin Encoding Guide – Systematic Way to Encode Any Circuit to CNF

---

### ✅ What is Tseitin encoding?

👉 Tseitin encoding = systematic way to turn **any circuit / formula** into **CNF**.

Why use it?

✅ Works for **any Boolean circuit**  
✅ Keeps the CNF formula **small and efficient**  
✅ Guarantees **equivalence** to the original circuit

---

### ⚙️ Idea:

- For every **gate** (AND, OR, NOR, XOR, etc):
    - Introduce a new variable to represent the gate's output
    - Write **CNF clauses** for that variable = "the gate is working correctly"
- The final **goal of the circuit** becomes **one variable** → assert that variable = true (or false)

---

### 🚀 Algorithm (Step-by-step):

---

### Step 1️⃣ Label all **internal nodes** of the circuit

- Each input → variable (example: x₁, x₂, ...)
- Each gate → introduce a **fresh variable** to represent the output of the gate
    - Example: y₁ = output of first AND gate
    - Example: y₂ = output of an OR gate
    - etc.

---

### Step 2️⃣ For each gate, write its **CNF clauses**

- Use the **standard encodings** (see table below!)

---

### Step 3️⃣ Add the **goal clause**

- If your circuit's output is variable y_goal:
    - To assert "output is True" → add clause: **(y_goal)**
    - To assert "output is False" → add clause: **(¬y_goal)**

---

### 🚦 Example: Small Circuit

```
x₁ ---\
        AND ---> y₁ ---\
x₂ ---/               OR ---> y₂ ---\
x₃ -----------------/             NOR ---> y_goal
x₄ --------------------------------/
```

---

#### Variables:

```
x₁, x₂, x₃, x₄ → inputs  
y₁ = x₁ ∧ x₂  
y₂ = y₁ ∨ x₃  
y_goal = ¬(y₂ ∨ x₄)  → NOR
```

---

#### Tseitin encoding:

**AND gate:** y₁ ↔ (x₁ ∧ x₂)

```
(¬y₁ ∨ x₁)
(¬y₁ ∨ x₂)
(y₁ ∨ ¬x₁ ∨ ¬x₂)
```

---

**OR gate:** y₂ ↔ (y₁ ∨ x₃)

```
(¬y₁ ∨ y₂)
(¬x₃ ∨ y₂)
(y₁ ∨ x₃ ∨ ¬y₂)
```

---

**NOR gate:** y_goal ↔ ¬(y₂ ∨ x₄)

```
(y₂ ∨ x₄ ∨ ¬y_goal)
(¬y₂ ∨ y_goal)
(¬x₄ ∨ y_goal)
```

---

**Goal:** Assert y_goal = True

```
(y_goal)
```

---

### ✅ Summary of the encoding process:

---

| Gate                         | Encoding (Tseitin)                                                  |
| ---------------------------- | ------------------------------------------------------------------- |
| **y ↔ (x₁ ∧ x₂)**            | (¬y ∨ x₁) ∧ (¬y ∨ x₂) ∧ (y ∨ ¬x₁ ∨ ¬x₂)                             |
| **y ↔ (x₁ ∨ x₂)**            | (¬x₁ ∨ y) ∧ (¬x₂ ∨ y) ∧ (x₁ ∨ x₂ ∨ ¬y)                              |
| **y ↔ ¬(x₁ ∨ x₂)** (**NOR**) | (x₁ ∨ x₂ ∨ ¬y) ∧ (¬x₁ ∨ y) ∧ (¬x₂ ∨ y)                              |
| **y ↔ (x₁ ⊕ x₂)** (**XOR**)  | (¬x₁ ∨ ¬x₂ ∨ ¬y) ∧ (x₁ ∨ x₂ ∨ ¬y) ∧ (x₁ ∨ ¬x₂ ∨ y) ∧ (¬x₁ ∨ x₂ ∨ y) |
| **y ↔ ¬x₁** (**NOT**)        | (x₁ ∨ ¬y) ∧ (¬x₁ ∨ y)                                               |
| **y ↔ x₁** (**BUFFER**)      | (¬x₁ ∨ y) ∧ (x₁ ∨ ¬y)                                               |

---

### 🚩 General rule:

👉 For each gate:  
✅ Introduce a fresh variable  
✅ Encode its behavior with **local clauses**  
✅ Combine all clauses into the full CNF  
✅ Add a goal clause (assert final output true/false)

---

### 🚦 Benefits of Tseitin encoding:

✅ **Linear size** in the circuit → avoids exponential blow-up  
✅ Guarantees equivalence  
✅ Efficient for SAT solvers  
✅ Standard method for: hardware verification, bounded model checking, etc

---

### 🚀 Example Applications:

- **Circuit verification**
- **Model checking**
- **Compiling SMT to SAT**
- **Encoding transition systems**
- **AI planning (STRIPS → SAT)**

---

### 🚩 Final Tips:

✅ Always introduce **fresh variable per gate**  
✅ Use the **canonical encodings** (table above)  
✅ Don’t inline large expressions → keep things modular with fresh variables  
✅ Assert **goal variable** → output of your circuit

---



# ⚙️ Planning Tasks & Heuristics – Full Overview with Examples

---

## ✅ Satisficing vs. Optimal Planning

---

### Satisficing Planning

- Goal: **find any valid plan** that achieves the goal.
- No guarantee of optimality (may not be shortest/cheapest).
- Planner stops as soon as it finds *some* solution.

---

### Optimal Planning

- Goal: **find the best possible plan** (shortest or lowest cost).
- Guarantees optimality (with respect to plan length or cost).
- Planner must explore until it proves optimality.

---

### Example

Robot moving on a grid:

| Planner Type  | Result |
|---------------|--------|
| Satisficing   | Any path to goal (even long one). |
| Optimal       | Shortest path to goal. |

---

## ✅ STRIPS Planning Task

---

### Formal Definition

STRIPS planning task:  
**Π = (P, A, I, G)**

- **P:** finite set of boolean facts (propositions).
- **A:** finite set of actions. Each action a = (pre(a), add(a), del(a)):
  - **pre(a):** required facts to apply action.
  - **add(a):** facts made true after applying action.
  - **del(a):** facts made false after applying action.
- **I:** initial state (subset of P).
- **G:** goal (subset of P).

---

### ✅ Step-by-Step Example – Baking a Cake

---

#### Problem Setup

- **P:** {HaveIngredients, OvenPreheated, CakeBaked}
- **I:** {HaveIngredients = true, OvenPreheated = false, CakeBaked = false}
- **G:** {CakeBaked = true}
- **A:**  
  - PreheatOven:  
    - pre: {¬OvenPreheated}  
    - add: {OvenPreheated}  
  - BakeCake:  
    - pre: {HaveIngredients, OvenPreheated}  
    - add: {CakeBaked}

---

#### Goal: Bake the cake!

---

### ✅ Possible Plan

1️⃣ Apply **PreheatOven**:
- Before: {HaveIngredients = true, OvenPreheated = false, CakeBaked = false}
- After:  {HaveIngredients = true, OvenPreheated = true, CakeBaked = false}

---

2️⃣ Apply **BakeCake**:
- Before: {HaveIngredients = true, OvenPreheated = true, CakeBaked = false}
- After:  {HaveIngredients = true, OvenPreheated = true, CakeBaked = true} → Goal ✔️

---

## ✅ STRIPS State Space

---

### Definition

- **States:** subsets of P (each fact true or false).
- **Transitions:** $s \xrightarrow{a} s'$, where:
  - If pre(a) ⊆ s → action applicable.
  - $s' = (s ∪ add(a)) \setminus del(a)$
- **Goal states:** s where G ⊆ s.
- **Solvable:** if path from I to goal exists.

---

### ✅ Step-by-Step Example – State Space

1️⃣ Initial state s₀:
{HaveIngredients = true, ¬OvenPreheated, ¬CakeBaked}

---

2️⃣ Transition: PreheatOven → s₁:
{HaveIngredients = true, OvenPreheated = true, ¬CakeBaked}

---

3️⃣ Transition: BakeCake → s₂ (goal):
{HaveIngredients = true, OvenPreheated = true, CakeBaked = true}

---

## ✅ Heuristic Function

---

### What is a Heuristic?

- **h(s):** estimates how far state s is from the goal.
- Used to **guide the search**.

---

### Formal:

- $h: S → ℕ₀ ∪ {∞}$
- $h(s) = 0$ if s is a goal state.
- **Admissible:** if $h(s) ≤ h^*(s)$ (never overestimates true cost).

---

### ✅ Example Heuristics

---

1️⃣ Trivial: $h(s) = 0$ → admissible but uninformative.

---

2️⃣ Goal Count: number of unsatisfied goal facts.
- For baking cake:
  - If CakeBaked = false → $h(s) = 1$.

---

3️⃣ Puzzle heuristic:
- 8-puzzle: Manhattan distance → admissible.

---

## ✅ FDR Planning Task

---

### Formal Definition

**Π = (V, A, c, I, G)**

- **V:** state variables with finite domains.
- **A:** actions: a = (pre(a), eff(a)).
- **c:** cost function (cost of actions).
- **I:** complete initial assignment.
- **G:** partial goal assignment.

---

### ✅ Step-by-Step Example – Robot with Key

---

#### Problem Setup

- **V:**
  - RobotLoc ∈ {A, B, C}
  - HasKey ∈ {No, Yes}

---

- **I:** {RobotLoc = A, HasKey = No}

- **G:** {RobotLoc = C, HasKey = Yes}

---

- **A:**  
  - MoveAB:  
    - pre: {RobotLoc = A}  
    - eff: {RobotLoc := B}  
  - PickKey:  
    - pre: {RobotLoc = B, HasKey = No}  
    - eff: {HasKey := Yes}  
  - MoveBC:  
    - pre: {RobotLoc = B, HasKey = Yes}  
    - eff: {RobotLoc := C}

---

### ✅ Possible Plan

1️⃣ MoveAB → B  
2️⃣ PickKey → HasKey = Yes  
3️⃣ MoveBC → C + HasKey = Yes → Goal ✔️

---

## ✅ Abstraction Heuristic

---

### What is it?

A heuristic built by solving a **simplified version** of the problem.

---

### ✅ How it works – Step by Step

---

1️⃣ Define abstraction mapping:
- $\alpha: S → S_{abstract}$

---

2️⃣ Build abstract problem:
- Fewer distinctions (e.g. ignore some variables).

---

3️⃣ Solve abstract problem:
- Compute shortest distances.

---

4️⃣ Define heuristic:
- $h_\alpha(s) = distance(\alpha(s))$

---

### ✅ Example – Abstraction Heuristic (Robot with Key)

---

#### Step 1: Define abstraction

Ignore **HasKey**.  
α(s) = RobotLoc only.

---

#### Step 2: Abstract states

{A, B, C}

---

#### Step 3: Abstract actions

- MoveAB: A → B
- MoveBC: B → C

---

#### Step 4: Solve abstract problem

- A → C: 2 steps
- B → C: 1 step
- C → C: 0 steps

---

#### Step 5: Heuristic

| Concrete State s      | α(s) | hₐ(s) |
|-----------------------|------|-------|
| (A, No)               | A    | 2     |
| (B, No)               | B    | 1     |
| (B, Yes)              | B    | 1     |
| (C, No)               | C    | 0     |
| (C, Yes)              | C    | 0     |

---

## ✅ Projection & PDB Heuristic

---

### What is Projection?

A **special kind of abstraction**:  
Select a subset of variables **P ⊆ V**.

---

### ✅ How it works – Step by Step

---

1️⃣ Choose pattern P.

---

2️⃣ Define projection mapping:
- $\pi_P(s)$ = values of variables in P.

---

3️⃣ Project actions:
- Keep preconditions/effects on P.

---

4️⃣ Project goal:
- Keep goal conditions on P.

---

5️⃣ Solve projected problem:
- Build **Pattern Database (PDB)**.

---

6️⃣ Heuristic at runtime:
- $h_P(s) = PDB[\pi_P(s)]$ → admissible!

---

### ✅ Example – Projection & PDB Heuristic (Robot with Key)

---

#### Step 1: Choose pattern

P = {RobotLoc}

---

#### Step 2: Projection mapping

| Concrete State s      | π_P(s) |
|-----------------------|--------|
| (A, No)               | A      |
| (B, Yes)              | B      |
| (C, No)               | C      |

---

#### Step 3: Project actions

- MoveAB: A → B
- MoveBC: B → C

---

#### Step 4: Project goal

Goal: RobotLoc = C.

---

#### Step 5: Solve projected problem

| π_P(s) | Distance to goal |
|--------|------------------|
| A      | 2                |
| B      | 1                |
| C      | 0                |

---

#### Step 6: Runtime heuristic

| Concrete State s      | π_P(s) | hₚ(s) |
|-----------------------|--------|-------|
| (A, No)               | A      | 2     |
| (B, No)               | B      | 1     |
| (B, Yes)              | B      | 1     |
| (C, No)               | C      | 0     |
| (C, Yes)              | C      | 0     |

---

## ✅ Why is PDB Heuristic Admissible?

- Projection simplifies the problem → distances in projected space ≤ real cost.
- So: **PDB heuristic is admissible**.

---

## ✅ Summary Table

| Concept               | Meaning                                 | Example |
|-----------------------|-----------------------------------------|---------|
| Heuristic              | Estimates distance to goal               | $h(s)$ |
| Admissible heuristic   | Never overestimates                      | $h(s) ≤ h^*(s)$ |
| Abstraction heuristic  | Solve abstract problem → get $h_\alpha$  | Ignore HasKey |
| Projection             | Special abstraction: select variables   | Pattern {RobotLoc} |
| PDB heuristic          | Precomputed heuristic from projection   | PDB[π_P(s)] |

---


# 🚚 STATES AS LOGICAL FORMULAS – Step-by-Step Guide  
### Example: Logistics Domain (l1, l2, l3)  
### Truck, Packages, Locations  

---

### ✅ Goal: 

We want to represent **states** in a planning problem (Logistics) as **logical formulas** (sets of literals).  

This allows us to:  
- Define **initial state**  
- Define **goal state**  
- Define **actions** (with preconditions & effects)  
- Define **transition relation** (TR)  
- Use symbolic techniques (like **SAT**, **BDD**) to reason about the domain.  

---

### ✅ Facts:

We use **facts** (aka **predicates**) of the form:  

`at(x, l)` → object `x` is at location `l`  

`in(p, t)` → package `p` is inside the truck `t`  

---

#### Objects:  

- `t` → truck  
- `p1`, `p2` → packages  

#### Locations:  

- `l1`, `l2`, `l3`  

---

### ✅ Initial State (I):

The **initial state** is represented as a **conjunction of literals** (facts that are true):  

```
I = at(t, l1) ∧ at(p1, l1) ∧ at(p2, l1)
```

---

### ✅ Goal State (G):

The **goal state** is also a conjunction of literals:  

```
G = at(t, l1) ∧ at(p1, l3) ∧ at(p2, l3)
```

---

### ✅ Actions (A):

Each **action** is specified by:  

- **Preconditions** → must be true for the action to apply.  
- **Add effects** → facts that will become true after applying the action.  
- **Delete effects** → facts that will become false after applying the action.  

---

#### Action: `drive(x, y)`  
(only allowed if there is a **road** between x and y)  

```
Preconditions: at(t, x)  
Add effects:   at(t, y)  
Delete effects: at(t, x)  
```

---

#### Action: `load(p, x)`  

```
Preconditions: at(t, x) ∧ at(p, x)  
Add effects:   in(p, t)  
Delete effects: at(p, x)  
```

---

#### Action: `unload(p, x)`  

```
Preconditions: at(t, x) ∧ in(p, t)  
Add effects:   at(p, x)  
Delete effects: in(p, t)  
```

---

### ✅ Representing a State:

A **state** is a complete assignment of all facts → represented as a conjunction of **positive** and **negative** literals.  

**IMPORTANT**:  
In propositional logic, there is **no closed-world assumption** → we must explicitly include **negated literals** to show what is false.  

---

#### Example State S:

```
S = at(t, l1) ∧ ¬at(t, l2) ∧ ¬at(t, l3)  
  ∧ at(p1, l1) ∧ ¬at(p1, l2) ∧ ¬at(p1, l3)  
  ∧ at(p2, l1) ∧ ¬at(p2, l2) ∧ ¬at(p2, l3)  
  ∧ ¬in(p1, t) ∧ ¬in(p2, t)
```

---

### ✅ Transition Relation (TR):

The **Transition Relation** `TR_a` for an action `a` defines how applying `a` moves us from a state `s` to a new state `s'`.  

---

#### For each action `a`, we define:

```
TR_a =  
    (preconditions hold in s)  
∧   (add effects hold in s')  
∧ ¬(delete effects hold in s')  
∧   (all other facts stay unchanged → frame axioms)
```

---

#### Example: TR for `load(p1, l1)`

Action:

```
load(p1, l1):  
  Preconditions: at(t, l1) ∧ at(p1, l1)  
  Add effects:   in(p1, t)  
  Delete effects: at(p1, l1)
```

---

Then the **transition relation** is:

```
TR_load(p1, l1) =  
    at(t, l1) ∧ at(p1, l1)                # preconditions must hold in s  
∧   in'(p1, t)                            # add effect must hold in s'  
∧ ¬at'(p1, l1)                            # delete effect must NOT hold in s'  
∧ (∀ other facts f: f ↔ f')               # other facts remain unchanged
```

---

### ✅ Full Transition Relation:

To get the **full TR** for the whole domain:  

```
TR = ⋃ (TR_a)    for all actions a ∈ A
```

This means:  
- If we apply **any action** a ∈ A, it defines one part of the full TR.  
- The full TR is the **union** of all the individual TR_a relations.  

---

### ✅ BDD Image Operation:

Now suppose we have:  

- **Set of states** S(x)  
- **Transition relation** TR(x, x')  

We can compute the **successor states** by taking the image:  

```
image(S(x), TR(x, x')) = { x' | ∃x . (S(x) ∧ TR(x, x')) }
```

---

### ✅ BDD Operations Needed:

#### 1️⃣ Existential Quantification (∃x):

This operation **removes variables x** from the BDD by computing their disjunction:  

```
∃x . f(x, y) = f(true, y) ∨ f(false, y)
```

Used to "project away" the old state variables.

---

#### 2️⃣ Variable Replacement [x → x']:

This operation **renames** variables:  

```
[x1 → x1', x2 → x2', ...]
```

Used to align variable names between old state and new state.

---

### ✅ Example: Applying Action `load(p1, l1)`  

---

#### Initial state S:

```
S = at(t, l1) ∧ at(p1, l1) ∧ at(p2, l1)  
  ∧ ¬in(p1, t) ∧ ¬in(p2, t)  
  ∧ ¬at(t, l2) ∧ ¬at(t, l3)  
  ∧ ¬at(p1, l2) ∧ ¬at(p1, l3)  
  ∧ ¬at(p2, l2) ∧ ¬at(p2, l3)
```

---

#### Action: `load(p1, l1)`

```
Preconditions: at(t, l1) ∧ at(p1, l1)  
Add effects: in(p1, t)  
Delete effects: at(p1, l1)
```

---

#### TR_load(p1, l1):

```
TR_load(p1, l1) =  
    at(t, l1) ∧ at(p1, l1)  
∧   in'(p1, t)  
∧ ¬at'(p1, l1)  
∧ (∀ other facts f: f ↔ f')
```

---

### ✅ Compute image(S, TR_load):

```
image(S, TR_load) = ∃x . (S(x) ∧ TR_load(x, x'))
```

---

#### Step 1: Check preconditions

```
at(t, l1) ∈ S → TRUE  
at(p1, l1) ∈ S → TRUE  
→ action applicable
```

---

#### Step 2: Build S' (successor state)

```
S' = at(t, l1)                     # unchanged  
  ∧ in(p1, t)                      # added  
  ∧ ¬at(p1, l1)                    # deleted  
  ∧ at(p2, l1)                     # unchanged  
  ∧ ¬in(p2, t)                     # unchanged  
  ∧ ¬at(t, l2) ∧ ¬at(t, l3)        # unchanged  
  ∧ ¬at(p1, l2) ∧ ¬at(p1, l3)      # unchanged  
  ∧ ¬at(p2, l2) ∧ ¬at(p2, l3)      # unchanged
```

---

### ✅ Summary of Transition:

| Step             | Meaning                                |
| ---------------- | -------------------------------------- |
| Preconditions    | must hold in `s`                        |
| Adds             | must hold in `s'`                       |
| Deletes          | must NOT hold in `s'`                   |
| All others       | stay unchanged (frame axioms)           |

---

### ✅ Why Logical Representation?

- General → works for **any domain**  
- Declarative → easy to express actions & goals  
- Works with **symbolic planners** (SAT, BDD-based)  
- Enables automatic planning by reasoning about logical formulas.

---

### ✅ Final Recap:

**To simulate 1 step of planning**:  

```
image(S(x), TR(x, x')) = ∃x . (S(x) ∧ TR(x, x'))
```

This gives us **all possible successor states** after applying any valid action.

---



# ⚙️ DYNAMIC PROGRAMMING – Full Step-by-Step Guide  

---

### ✅ Goal:  

To understand and be able to apply:  
**Dynamic Programming (DP)** = solving problems by:  
- breaking them into subproblems  
- storing (memoizing) the answers to subproblems to avoid recomputation  
- combining subproblem answers to build up the full solution  

---

### ✅ When to use DP?

**Two signs a problem is suitable for DP:**  

1️⃣ **Optimal substructure** → the optimal solution can be built from optimal solutions of subproblems  

2️⃣ **Overlapping subproblems** → the same subproblems are solved multiple times → store their results!  

---

### ✅ Big Picture: How DP works

1️⃣ Identify the subproblem(s)  
2️⃣ Define the state  
3️⃣ Write the recurrence relation  
4️⃣ Decide base cases  
5️⃣ Implement either:  
    - top-down (recursive + memoization)  
    - bottom-up (iterative table filling)  

---

### ✅ How to turn a problem into a DP  

---

#### Step 1: Define the subproblem (state)  

Ask:  
**"What do I need to compute?"**  

Example: For EditDistance(s[1..i], t[1..j])  
→ subproblem = distance between first i characters of s and first j characters of t  

---

#### Step 2: Define recurrence relation  

Ask:  
**"How can I build this subproblem from smaller subproblems?"**  

→ Write the formula (recurrence)  

Example:  
If s[i] == t[j]:  
dist[i,j] = min(  
    dist[i-1,j-1],       // match  
    dist[i-1,j] + 1,     // delete  
    dist[i,j-1] + 1      // insert  
)  

Else:  
dist[i,j] = 1 + min(  
    dist[i-1,j-1],       // substitute  
    dist[i-1,j],         // delete  
    dist[i,j-1]          // insert  
)  

---

#### Step 3: Base cases  

Ask:  
**"What are the simplest subproblems I know the answer to?"**  

Example:  
dist[0,j] = j → need j insertions to match empty string to t[1..j]  
dist[i,0] = i → need i deletions to match s[1..i] to empty string  

---

#### Step 4: Order of computation  

Two options:  

**Top-down (recursion + memoization)**  
- Write normal recursion  
- Add a table (hashmap/array) to memoize  

**Bottom-up (iterative)**  
- Fill table in order that ensures dependencies are ready  

---

### ✅ Example: Edit Distance  

---

#### Pseudocode  

```
EditDistance(s[1..m], t[1..n])  

for i = 0 to m do  
    dist[i,0] = i  

for j = 0 to n do  
    dist[0,j] = j  

for i = 1 to m do  
    for j = 1 to n do  
        if s[i] == t[j] then  
            dist[i,j] = min(dist[i-1,j-1], dist[i-1,j] + 1, dist[i,j-1] + 1)  
        else  
            dist[i,j] = 1 + min(dist[i-1,j-1], dist[i-1,j], dist[i,j-1])  

return dist[m,n]  
```

---

#### DP Table  

A (m+1) x (n+1) table where dist[i,j] = edit distance between s[1..i] and t[1..j]  

---

### ✅ How to analyze running time  

---

#### For iterative DP:  

Usually: **#subproblems × time per subproblem**  

Example: Edit Distance:  
- #subproblems = O(m * n) → the table has m * n cells  
- time per subproblem = O(1) → constant number of min and add  

**Total = O(m * n)**  

---

#### Quick checklist to analyze any DP:  

| Step          | What to do              |
|---------------|-------------------------|
| Subproblems   | How many distinct states? |
| Work per state| How much time per state?  |
| Final runtime | Multiply the two!        |

---

### ✅ Example: Activity Selection  

---

Problem: Select max number of non-overlapping activities (each has start time s_i and finish time f_i)  

---

#### Greedy solution (not DP, but compare!)  

- Sort activities by finish time  
- Greedily select earliest finishing compatible activity  

**Runtime: O(n log n)** (for sorting)  

---

#### If DP version (Weighted Activity Selection)  

- Activities may have weights/profits → must use DP!  

---

#### Subproblem:  

Define opt(j) = max total weight of subset of first j activities ending by time f_j  

---

#### Recurrence:  

opt(j) = max(  
    opt(j-1),  
    weight_j + opt(p(j))  
)  

where p(j) = rightmost activity i < j that finishes before s_j  

---

#### Base case:  

opt(0) = 0  

---

#### Runtime:  

- #subproblems = O(n)  
- time per subproblem = O(log n) if use binary search to compute p(j)  

**Total: O(n log n)**  

---

### ✅ Summary: How to apply DP  

---

| Step | What to do |
|------|------------|
| 1    | Define state (subproblem) |
| 2    | Write recurrence relation |
| 3    | Define base cases |
| 4    | Decide order of computation |
| 5    | Implement → analyze runtime |

---

### ✅ How to quickly see running time of an algorithm  

---

#### "Classic checklist":  

| Component            | Typical Big-O   |
|----------------------|-----------------|
| Loop over n          | O(n)            |
| Nested loop n x n    | O(n²)           |
| Loop with log n      | O(log n)        |
| Divide & conquer     | O(n log n)      |
| DP table fill        | O(#states × work/state) |

---

#### Example:  

If table is size n x m → O(n * m)  
If recursion does 2^n calls → O(2^n)  
If recursion does log n depth → O(log n)  

---

### ✅ Asymptotic behavior  

**Big-O** = upper bound  

Also sometimes:  
- Θ (Theta) → tight bound  
- Ω (Omega) → lower bound  

---

### ✅ Summary table of typical complexities  

| Algorithm Type           | Time Complexity |
|--------------------------|-----------------|
| Simple loop              | O(n)            |
| Nested loop              | O(n²)           |
| Sorting                  | O(n log n)      |
| Classic DP table fill    | O(n²), O(n³), etc |
| Backtracking/Brute force | O(2^n)          |

---

### ✅ Final DP Checklist (for exam!)  

---

✅ Does problem have **optimal substructure**?  
✅ Does problem have **overlapping subproblems**?  
✅ Did you define state clearly?  
✅ Did you write recurrence relation?  
✅ Did you define base cases?  
✅ Did you choose top-down or bottom-up?  
✅ Did you analyze runtime correctly?  

---


# ⚙️ GREEDY ALGORITHMS – Full Step-by-Step Guide  

---

### ✅ Goal:  

To understand and apply **Greedy Algorithm Design**:

---

### ✅ What is a Greedy Algorithm?  

At each step:  
→ Make the **best local choice** (greedy choice)  
→ Hope that this leads to a **global optimum**  

---

### ✅ When does Greedy work?  

Greedy works when:  

1️⃣ **Greedy-choice property**:  
→ A global optimum can be arrived at by selecting local optimums  

2️⃣ **Optimal substructure**:  
→ Optimal solution contains optimal solutions to subproblems  

---

### ✅ Greedy Algorithm Template  

1️⃣ Identify greedy choice → what local choice to make  
2️⃣ Prove that greedy choice is safe → leads to optimal solution  
3️⃣ Implement → usually very fast (O(n log n) or O(n))  

---

### ✅ Greedy vs DP  

| Technique | Characteristics |
|-----------|-----------------|
| Greedy    | No backtracking; locally optimal choices |
| DP        | Explore all combinations via subproblems |

---

### ✅ Example Problems  

---

1️⃣ **Activity Selection**  
2️⃣ **Huffman Coding** ✅ explained below  
3️⃣ **Minimum Spanning Trees**  

---

# 📜 HUFFMAN CODING – Full Step-by-Step Guide  

---

### ✅ Goal:  

**Given:** Alphabet of symbols {a₁, a₂, ..., a_n} with frequencies f₁, f₂, ..., f_n  

**Compute:** A prefix-free binary code (Huffman Code) minimizing total cost:  

TotalCost = Σ (fᵢ * length(codeᵢ))  

---

### ✅ What is a Huffman Tree?  

A **binary tree**:  
- Leaves = symbols  
- Path to leaf = codeword (0 = left, 1 = right)  
- No code is prefix of another (prefix-free)  

---

### ✅ Why does greedy work here?  

**Greedy choice property:**  
→ It is optimal to combine the two lowest-frequency symbols first  

**Optimal substructure:**  
→ The optimal code for n symbols can be built from the optimal code for n-1 combined symbols  

---

### ✅ Step-by-step algorithm  

---

#### Step 1: Initialization  

- Start with **n single-node trees**, one per symbol  
- Priority queue (min-heap) ordered by frequency  

---

#### Step 2: Build Tree  

Repeat until one tree remains:  

1️⃣ Extract two trees with **smallest frequencies** f₁, f₂  
2️⃣ Create a new parent node with combined frequency f₁ + f₂  
3️⃣ Add the new node back into the priority queue  

---

#### Step 3: Assign codes  

- Traverse the final tree:  
    - Left edge = add '0'  
    - Right edge = add '1'  
- Path to each leaf = that symbol's code  

---

### ✅ Example  

---

**Given symbols and frequencies:**  

| Symbol | Frequency |
|--------|-----------|
| A      | 5         |
| B      | 9         |
| C      | 12        |
| D      | 13        |
| E      | 16        |
| F      | 45        |

---

#### Step-by-step  

---

**Priority queue:**  

{A(5), B(9), C(12), D(13), E(16), F(45)}  

---

**Iteration 1:**  

- Extract A(5), B(9) → new node (14)  
- Queue: {C(12), D(13), E(16), F(45), (14)}  

---

**Iteration 2:**  

- Extract C(12), D(13) → new node (25)  
- Queue: {E(16), F(45), (14), (25)}  

---

**Iteration 3:**  

- Extract (14), E(16) → new node (30)  
- Queue: {F(45), (25), (30)}  

---

**Iteration 4:**  

- Extract (25), (30) → new node (55)  
- Queue: {F(45), (55)}  

---

**Iteration 5:**  

- Extract F(45), (55) → new root (100)  

---

Now you have the **full tree** → assign 0/1 to edges → codes are created!  

---

### ✅ Final Codes (Example Output)  

| Symbol | Code  |
|--------|-------|
| F      | 0     |
| C      | 100   |
| D      | 101   |
| A      | 1100  |
| B      | 1101  |
| E      | 111   |

---

### ✅ Why is Huffman optimal?  

---

**Proof idea:**  

1️⃣ Greedy choice = safe  
- Combining two smallest frequencies is always optimal (proof by exchange argument)  

2️⃣ Optimal substructure  
- Remaining problem is again a smaller Huffman problem  

---

### ✅ Pseudocode  

---

```
Huffman(symbols[1..n], freq[1..n])  

PQ = priority queue ordered by frequency  

for i = 1 to n do  
    PQ.insert(new tree node with symbol[i] and freq[i])  

while PQ.size > 1 do  
    x = PQ.extractMin()  
    y = PQ.extractMin()  
    z = new node with freq = x.freq + y.freq  
    z.left = x  
    z.right = y  
    PQ.insert(z)  

return PQ.extractMin() → root of final tree  
```

---

### ✅ Runtime  

---

- n insertions into PQ → O(n log n)  
- n-1 extractMin/insert → O(n log n)  

**Total runtime: O(n log n)**  

---

### ✅ Final checklist (for exam!)  

---

✅ Greedy-choice property holds?  
✅ Optimal substructure?  
✅ What is the greedy choice?  
✅ Prove correctness (optional: exchange argument)  
✅ What is runtime?  
✅ How to implement?  

---

# ✅ Summary of Example Greedy Algorithms  

---

| Problem                           | Greedy choice                    | Runtime    |
| --------------------------------- | -------------------------------- | ---------- |
| Activity Selection                | Earliest finish time             | O(n log n) |
| Huffman Coding                    | Combine lowest freq pair         | O(n log n) |
| Minimum Spanning Tree (Prim's)    | Pick lightest edge growing tree  | O(E log V) |
| Minimum Spanning Tree (Kruskal's) | Pick lightest edge without cycle | O(E log E) |

---
# 🔄 MAXIMUM FLOW – Step-by-Step Guide  
### Weighted Directed Graph → Flow Network  
### Ford-Fulkerson → Edmonds-Karp → Max-Flow Min-Cut  

---

### ✅ What is the Maximum Flow Problem?

We are given a **directed graph** with **weights** on the edges.  
The weights represent **capacity** → maximum amount of "flow" allowed on the edge.  

---

**Examples of flow networks:**
- Pipe network → flow = liquid  
- Electric circuit → flow = electric current  
- Road network → flow = cars  

---

We are also given:
- A **source vertex** `s` → where the flow starts.  
- A **sink vertex** `t` → where the flow ends.  

---

**Goal:**  
Compute the **maximum possible flow** from `s` to `t`, subject to the edge capacities.

---

### ✅ Formal Definitions:

---

#### 1️⃣ Flow Network:

A flow network is a **directed graph** `G = (V, E)` with:
- Capacity function `c(u,v)` for each edge → max flow allowed on `(u,v)`  
- A **source** node `s` ∈ V  
- A **sink** node `t` ∈ V  

---

#### 2️⃣ Flow:

A flow is a function `f(u,v)` defined for each edge `(u,v)` with:
1. **Capacity constraint:**  
   `0 ≤ f(u,v) ≤ c(u,v)`  
2. **Flow conservation:**  
   For all nodes `v ≠ s,t`:  
   `sum_incoming_flows = sum_outgoing_flows`  
   In other words: flow is conserved in all intermediate nodes.  

---

#### 3️⃣ Value of a flow:

```
|f| = total flow sent from s = sum of flows out of s
```

---

### ✅ Example Network:

Let's say we have this graph:

```
       10        5
    s -----> a -----> t
     \        |       ^
      \       v       |
       >----> b ------>  
         15    10      10
```

**Capacities:**
```
c(s,a) = 10  
c(s,b) = 15  
c(a,t) = 5  
c(b,t) = 10  
c(a,b) = 10  
```

---

### ✅ What is a Maximum Flow?

In this example, we want to compute **how much flow we can push from `s` to `t`**.

---

### ✅ The Residual Network:

At each step of the algorithm, we build the **residual network**:

Residual capacity of edge `(u,v)`:
```
c_f(u,v) = c(u,v) - f(u,v)
```

It represents how much more flow we can push along that edge.

We also add **reverse edges** in residual network to allow flow to be "canceled" / "pushed back" if needed!

---

### ✅ Ford-Fulkerson Method:

---

**Algorithm idea:**
1️⃣ Start with **zero flow** on all edges.  
2️⃣ While there exists an **augmenting path** in the residual network:
   - Find the **minimum residual capacity** `c_f` on the path.
   - Push flow along the path.
   - Update the flow and residual capacities.

---

### ✅ Edmonds-Karp Algorithm:

Edmonds-Karp is a **specific implementation** of Ford-Fulkerson that:
- Always finds the **shortest augmenting path** (using **BFS**).
- Guarantees **polynomial runtime**:  
  `O(V * E^2)`  

---

### ✅ Worked Example: Ford-Fulkerson on the example graph

---

#### Step 0: Initial flow = 0 everywhere.

Residual capacities = original capacities.

---

#### Step 1: Find augmenting path.

Use BFS → we find:

`s → a → t`

Residual capacity of this path:

```
min(c_f(s,a), c_f(a,t)) = min(10, 5) = 5
```

→ Push flow of **5** units along this path.

---

Now:

```
f(s,a) = 5  
f(a,t) = 5
```

Updated residual capacities:

```
c_f(s,a) = 10 - 5 = 5  
c_f(a,t) = 5 - 5 = 0
```

---

#### Step 2: Find next augmenting path.

Now the path `s → a → t` is blocked (capacity 0 on a→t).

BFS finds:

`s → b → t`

Residual capacity:

```
min(c_f(s,b), c_f(b,t)) = min(15, 10) = 10
```

→ Push flow of **10** units.

Now:

```
f(s,b) = 10  
f(b,t) = 10
```

---

#### Step 3: Any more augmenting paths?

Now:

```
c_f(a,t) = 0  
c_f(b,t) = 0
```

→ No more paths from `s` to `t` with positive residual capacity.

---

#### Final result:

Total flow out of `s`:

```
|f| = f(s,a) + f(s,b) = 5 + 10 = 15
```

✅ **Maximum flow = 15 units!**

---

### ✅ Max-Flow Min-Cut Theorem:

The theorem says:

```
Maximum flow value = Minimum capacity of an s-t cut.
```

→ The Ford-Fulkerson method **provably finds the maximum flow**, because once no more augmenting paths exist, the current flow equals the capacity of some cut.

---

### ✅ Linear Programming Formulation:

We can express max-flow as a linear program:

```
Maximize: sum of flow out of s

Subject to:

1️⃣ Capacity constraints:
   0 ≤ f(u,v) ≤ c(u,v)

2️⃣ Flow conservation:
   ∑ f(v,u) = ∑ f(u,v)  for all v ≠ s,t
```

---

The **dual** of this LP corresponds to finding the **minimum cut** → mirrors the max-flow min-cut duality!

---

### ✅ Application: Maximum Bipartite Matching

---

We can **reduce bipartite matching to a max-flow problem!**

---

#### Given:

A bipartite graph `G = (L ∪ R, E)`.

We want to find a **maximum matching** → largest set of edges where no two share an endpoint.

---

#### Construction of flow network:

- Add **source** `s`  
- Add **sink** `t`  
- For each node `u` in `L`, add edge `s → u` with capacity 1  
- For each node `v` in `R`, add edge `v → t` with capacity 1  
- For each edge `(u,v)` in the original bipartite graph, add edge `u → v` with capacity 1.

---

Then:  
**Maximum matching size = value of maximum flow from s to t**!

---

#### Why does this mapping work?

- Each matching edge corresponds to 1 unit of flow.  
- Capacity 1 ensures no node is matched twice.  
- So the flow must correspond to a valid matching.  
- Maximum flow → maximum matching.

---

### ✅ Summary of the Lecture:

---

| Goal                              | Covered? |
| --------------------------------- | -------- |
| Understand flow networks & flows   | ✅       |
| Understand Ford-Fulkerson          | ✅       |
| Understand Edmonds-Karp            | ✅       |
| Analyze runtime of Edmonds-Karp    | ✅ O(V * E^2) |
| Understand LP formulation          | ✅       |
| Apply to bipartite matching        | ✅       |

---

### ✅ Key Questions to Understand:

---

**Q1:** What is a maximum flow?  
→ The greatest total flow from source `s` to sink `t` obeying capacity and conservation constraints.

---

**Q2:** What is a residual network?  
→ The graph of remaining capacities → shows how much more flow can be pushed.

---

**Q3:** What is an augmenting path?  
→ A path from `s` to `t` in the residual network → along which we can push more flow.

---

**Q4:** What is residual capacity of a path?  
→ The minimum residual capacity along the edges of the path → how much flow can be pushed along the path.

---

**Q5:** In Edmonds-Karp, what part of Ford-Fulkerson does it implement?  
→ It implements the **augmenting path selection step**, using **shortest path (BFS)**.

---

**Q6:** How is maximum bipartite matching mapped to max flow? Why does it make sense?  
→ By adding source/sink and edges of capacity 1, matching is modeled as flow.  
→ Max flow corresponds to max matching because of capacity 1 constraints.

---


# EXAM EXERCISES FROM CAUSE

## Exercise 5 – SAT Encoding Notes  



---

### ⚙️ Variables  

For each student $s \in \{A, B, C, D, E\}$ introduce one Boolean:  

$$
x_s =
\begin{cases}
0 & \text{student $s$ is in Algorithms (ALG)} \\[4pt]
1 & \text{student $s$ is in Satisfiability (SAT)}
\end{cases}
$$  

---

### ① Astrid and Clara want the **same** group  

High-level: $x_A \leftrightarrow x_C$  

CNF:  

$$
(\lnot x_A \lor x_C) \land (x_A \lor \lnot x_C)
$$  

---

### ② David and Emily want **different** groups  

High-level: $x_D \oplus x_E$  

CNF:  

$$
(x_D \lor x_E) \land (\lnot x_D \lor \lnot x_E)
$$  

---

### ③ No student may be **alone** in a group  

Quantified form (extensible to any number of students):  

$$
\forall s \in S \;\; \exists t \in S \setminus \{s\}: \; x_s \leftrightarrow x_t
$$  

For 5 students this reduces to forbidding sums $=1$ and $=4$:  

* **Forbid sum = 1** (example clauses):  

$$
(x_A \lor x_B \lor x_C), \;\; (x_A \lor x_B \lor x_D), \;\; \ldots
$$  

* **Forbid sum = 4** (example clauses):  

$$
(\lnot x_A \lor \lnot x_B \lor \lnot x_C \lor \lnot x_D), \;\; \ldots
$$  

---

### ④ Brian does **not** want SAT (so must be in ALG)  

High-level: $x_B \leftrightarrow 0$  

CNF:  

$$
\lnot x_B
$$  

---

### ⑤ Emily **wants** SAT  

High-level: $x_E \leftrightarrow 1$  

CNF:  

$$
x_E
$$  

---

### 🔗 Combined master formula  

$$
F = (x_A \leftrightarrow x_C) \land (x_D \oplus x_E) \land 
\left[ \forall s \, \exists t \neq s : x_s \leftrightarrow x_t \right] \land 
(\lnot x_B) \land (x_E)
$$  

---

### 📌 Interpreting a satisfying assignment  

* **Algorithms group**: $\{ \, s \mid x_s = 0 \, \}$  
* **Satisfiability group**: $\{ \, s \mid x_s = 1 \, \}$  

---

### 🔄 Extending to more students  

* Add a variable $x_F$ for each new student $F$  
* Add any new friendship / dislike / preference rules similarly  
* Update the **No-Alone** clauses:  

$$
\text{Forbid sum} = 1 \quad \text{and} \quad \text{sum} = n-1
$$  

→ Always adds $2n$ short clauses.


## Exercise 4 – PDDL Encoding Notes

---

### ⚙️ Predicates

```
(:predicates
    (connected ?x ?y)    ; → This models which rooms are connected (movement allowed in the ring)
    (gold_in ?x)         ; → This tracks where the gold is (which room)
    (gold_to ?x)         ; → This says which room is the goal room for the gold (target drop room)
    (has_gold)           ; → This is true if the robot is carrying the gold (possession flag)
    (at ?x)              ; → This tracks where the robot is (current room)
)
```
---

### 🏠 Objects

```
(:objects A B C D)   ; → These are the 4 rooms (the robot and gold move between these rooms)
```
---

### 🚦 Initial State

```
(:init
    (connected A B)      ; → Robot can move A → B
    (connected B C)      ; → Robot can move B → C
    (connected C D)      ; → Robot can move C → D
    (connected D A)      ; → Robot can move D → A (completes the ring)

    (at A)               ; → Robot starts in room A
    (gold_in D)          ; → Gold starts in room D
    (gold_to C)          ; → Goal is to drop the gold in room C
)
```
---

### 🎯 Goal

```
(:goal (and
    (at C)               ; → Robot must end up in room C
    (gold_in C)          ; → Gold must be in room C
    (not (has_gold))     ; → Robot must have dropped the gold (no longer carrying it)
))
```
---

### 🏃‍♂️ Actions

---

### ① move

```
(:action move
    :parameters (?x ?y)
    :precondition (and 
        (at ?x)               ; → Robot must be in current room ?x
        (connected ?x ?y)     ; → Must be allowed to move to ?y (valid connection)
    )
    :effect (and
        (at ?y)               ; → Robot is now in room ?y
        (not (at ?x))         ; → Robot is no longer in room ?x

        ;; If entering a room that contains the gold, pick it up:
        (when (gold_in ?y) (has_gold))

        ;; If already carrying the gold, move it along with the robot:
        (when (has_gold) (gold_in ?y))
        (when (has_gold) (not (gold_in ?x)))
    )
)
```
---

### ② drop

```
(:action drop
    :parameters (?x)
    :precondition (and 
        (at ?x)               ; → Robot must be in room ?x
        (has_gold)            ; → Robot must be carrying the gold
        (gold_to ?x)          ; → This must be the target room for the gold
        (gold_in ?x)          ; → Gold must be present in the current room
    )
    :effect (and
        (not (has_gold))      ; → After dropping, robot no longer carries the gold
    )
)
```
---

### 📜 Full Combined Code

---

#### DOMAIN FILE

```
(define (domain roboto)
    
    (:predicates
        (connected ?x ?y)    ; → Models valid movement connections
        (gold_in ?x)         ; → Models current gold location
        (gold_to ?x)         ; → Models target drop room
        (has_gold)           ; → Whether robot is carrying gold
        (at ?x)              ; → Robot's current room
    )
    
    (:action move
        :parameters (?x ?y)
        :precondition (and 
            (at ?x)
            (connected ?x ?y)
        )
        :effect (and
            (at ?y)
            (not (at ?x))

            ;; Pick up gold if entering the gold room
            (when (gold_in ?y) (has_gold))

            ;; If carrying gold, move it to new room
            (when (has_gold) (gold_in ?y))
            (when (has_gold) (not (gold_in ?x)))
        )
    )

    (:action drop
        :parameters (?x)
        :precondition (and 
            (at ?x)
            (has_gold)
            (gold_to ?x)
            (gold_in ?x)
        )
        :effect (and
            (not (has_gold))
        )
    )
)
```
---

#### PROBLEM FILE

```
(define (problem bw-abcde)

  (:domain roboto)

  (:objects A B C D)

  (:init
    (connected A B)
    (connected B C)
    (connected C D)
    (connected D A)

    (at A)               ; → Robot starts in A
    (gold_in D)          ; → Gold starts in D
    (gold_to C)          ; → Target room for gold is C
  )

  (:goal (and
    (at C)               ; → Robot must be in C
    (gold_in C)          ; → Gold must be in C
    (not (has_gold))     ; → Robot must have dropped the gold
  ))

)
```
---

## ✅ Summary of What I Did:

---

1️⃣ **(connected ?x ?y)**  
→ Encodes the room connections (ring structure).  
→ Matches: "The robot can only move along the ring."

---

2️⃣ **(gold_in ?x)**  
→ Tracks the location of the gold.  
→ Matches: "The robot moves into the position of the gold."

---

3️⃣ **(has_gold)**  
→ Tracks whether the robot is carrying the gold.  
→ Matches: "Whenever the robot holds the bag of gold."

---

4️⃣ **(gold_to ?x)**  
→ Defines which room is the drop goal.  
→ Matches: "The goal is to drop the gold in room C."

---

5️⃣ **move action**  
→ Moves robot along ring.  
→ Picks up gold when entering room with gold.  
→ Moves gold along if already carrying.

---

6️⃣ **drop action**  
→ Drops gold in target room, if carrying it.

---

7️⃣ **Goal**  
→ Robot is in C, gold is in C, robot has dropped the gold.

---

✅ The entire solution meets the exercise description:

- Robot moves correctly in ring  
- Picks up gold during move  
- Can drop gold  
- Reaches goal state as required.

---


# 2024 exam 

## 1 Problem Definition

Given three strings of characters: X[1..n], Y[1..m], and Z[1..n+m], a prefix of Z[1..k] (k ≤ n+m) is called an interleaved prefix if it is formed by alternatively taking some characters from X and Y without skipping any characters. 

For example, if X = "aabc", Y = "abbc", and Z = "aababccb", then "aababc" is an interleaved prefix of Z. 

We say that "XYYXXX" is a certificate corresponding to this prefix. It shows how the prefix is formed: we take a character from X ("a"), then two characters from Y ("ab"), and three from X ("abc").

---

### What does the question mean? (Explanation)

You are given three strings:

- X[1..n] → example: "aabc"
- Y[1..m] → example: "abbc"
- Z[1..n+m] → example: "aababccb"

Now, you are asked:

**Can you form a prefix of Z — for example, "aababc" — by taking letters one at a time from X and Y, without skipping any letters in X or Y?**

---

#### Rules:

✅ You can choose whether each letter of Z comes from X or Y.

✅ But you must take the characters from X and Y *in order*:

- If you take from X, you must use X[1], then X[2], then X[3], etc. — no skipping.
- Same for Y — must take Y[1], Y[2], Y[3], etc.

---

#### What is a "certificate"?

A **certificate** is a string of "X" and "Y" letters that shows which source you used for each letter of the Z prefix.

Example:

If Z_prefix = "aababc", and you took:

1. Z[1] from X → "X"
2. Z[2] from Y → "XY"
3. Z[3] from Y → "XYY"
4. Z[4] from X → "XYYX"
5. Z[5] from X → "XYYXX"
6. Z[6] from X → "XYYXXX"

Then the certificate would be:

```
XYYXXX
```

---


## 2 Problem Definition (Longest Interleaved Prefix - LIP)

Given the above mentioned three strings X, Y, and Z, we want to find the length of the longest possible interleaved prefix of Z (LIP). 

The problem can be solved with **dynamic programming**.

Assume we have already matched a prefix of Z by interleaving the first i - 1 characters of X and the first j - 1 characters of Y. 

Then we need to solve optimally the subproblem of finding the length of the longest interleaved prefix for:

```
X[i..n], Y[j..m], and Z[i+j-1 .. n+m]
```

We denote this subproblem as:

```
LIP(i, j)
```

---

### Recurrence:

To simplify the recurrence, we assume that:

```
X[n+1] = "$"
Y[m+1] = "$"
Z[n+m+1] = "#"
```

These special ending characters are not equal to any other characters used in the strings.

---

### The recurrence is:

```
LIP(i, j) = 

    0                                  if X[i] ≠ Z[i+j−1] ∧ Y[j] ≠ Z[i+j−1]
    
    1 + LIP(i+1, j)                    if X[i] = Z[i+j−1] ∧ Y[j] ≠ Z[i+j−1]
    
    1 + LIP(i, j+1)                    if X[i] ≠ Z[i+j−1] ∧ Y[j] = Z[i+j−1]
    
    1 + max(LIP(i+1, j), LIP(i, j+1))  if X[i] = Z[i+j−1] ∧ Y[j] = Z[i+j−1]
```

---

### Interpretation:

The most interesting **fourth case** of the recurrence happens when *both* X[i] and Y[j] match the next character in Z:

```
X[i] = Z[i+j−1] ∧ Y[j] = Z[i+j−1]
```

In this case, we have **two choices** — and we pick the one that gives a longer interleaved prefix:

```
1 + max(LIP(i+1, j), LIP(i, j+1))
```

---

## 3 Question: Running Time

Now, suppose we directly convert the above recurrence into a **recursive algorithm LIP** (without memoization).

What would be the **worst-case asymptotic running time** of:

```
LIP(1, 1)
```

when run on X[1..n], Y[1..m], and Z[1..n+m]?  
(Express the result in terms of **min(n, m)**.)

---

### Answer choices:

a. Logarithmic

b. Exponential

c. Linear

d. Polynomial

---

### Correct Answer:

**b. Exponential**

---

### Explanation:

👉 The recurrence can branch **twice** in the fourth case:

```
LIP(i, j) → LIP(i+1, j)  and LIP(i, j+1)
```

👉 Therefore, the recursion tree has **exponential size** in the worst case, because it explores **both options** at each step where X[i] = Y[j] = Z[i+j−1].

👉 There is no memoization in this naive version, so the same subproblems are recomputed multiple times → exponential behavior.

---

### Summary:

- The **plain recursive version** of LIP(i,j) has worst-case **exponential** running time.
- If we add memoization → we can reduce it to **polynomial** time (O(n * m)).

---
## 3 Question: Bottom-up Dynamic Programming Algorithm

Based on the recurrence above, write a pseudocode of a **bottom-up (loop-based)** dynamic programming algorithm to find the length of the longest interleaved prefix of Z. 

Assume that strings X, Y, and Z end with the special characters:

```
X[n+1] = "$"
Y[m+1] = "$"
Z[n+m+1] = "#"
```

---

### Pseudocode:

```plaintext
procedure Lip(x[1..n], y[1..m], z[1..n+m]):

    arr = initialize an array of size n by m with all zeros

    for i = n down-to 1 do
        for j = m down-to 1 do

            if (X[i] != Z[i + j - 1] and Y[j] != Z[i + j - 1]) do
                arr[i][j] = 0

            else if (X[i] == Z[i + j - 1] and Y[j] != Z[i + j - 1]) do
                arr[i][j] = 1 + arr[i + 1][j]

            else if (X[i] != Z[i + j - 1] and Y[j] == Z[i + j - 1]) do
                arr[i][j] = 1 + arr[i][j + 1]

            else
                arr[i][j] = 1 + max(arr[i + 1][j], arr[i][j + 1])

    return arr[1][1]
```

---

### Notes:

- The table `arr[i][j]` stores LIP(i, j).
- The table is filled **bottom-up** (loops go from n down to 1 and m down to 1).
- The **base case** is built naturally because we initialized everything to zero.
- Each cell takes **O(1)** time to compute.

---

## 4 Question: Running Time of the Dynamic Programming Algorithm

What is the **worst-case running time** of a dynamic programming algorithm based on the recurrence above?

---

### Answer choices:

a. Θ(n²)

b. Θ(n lg n)

c. Θ(n)

d. Θ(n³)

---

### Correct Answer:

**a. Θ(n²)**

---

### Explanation:

- The DP table has **Θ(n²)** cells (because m = Θ(n) is assumed).
- Each cell is filled in **O(1)** time.
- So the total running time is:

```
Θ(n²)
```

---

### Summary:

- The **recursive version** is exponential.
- The **bottom-up DP version** is **Θ(n²)** time and Θ(n²) space.

---
## 5 Question: Run the Dynamic Programming Algorithm

---

### Problem:

Let:

```
X = "aac$"
Y = "acb$"
Z = "aacabc#"
```

---

We run the **bottom-up dynamic programming algorithm** based on the following recurrence:

```plaintext
LIP(i, j) = 

    0                                  if X[i] ≠ Z[i + j − 1] ∧ Y[j] ≠ Z[i + j − 1]
    
    1 + LIP(i+1, j)                    if X[i] = Z[i + j − 1] ∧ Y[j] ≠ Z[i + j − 1]
    
    1 + LIP(i, j+1)                    if X[i] ≠ Z[i + j − 1] ∧ Y[j] = Z[i + j − 1]
    
    1 + max(LIP(i+1, j), LIP(i, j+1))  if X[i] = Z[i + j − 1] ∧ Y[j] = Z[i + j − 1]
```

---

### How i and j are used:

At each table cell `arr[i][j]`, we are trying to match:

```
Z[i + j - 1]
```

- `i` tells us the position in X we are currently considering → X[i].
- `j` tells us the position in Y we are currently considering → Y[j].

---

### Initial table (partially filled):

| i / j   | a (1) | c (2) | b (3) | $ (4) |
|---------|-------|-------|-------|-------|
| **1 a** | Blank 1 | Blank 2 | Blank 3 | Blank 4 |
| **2 a** | 5     | 4     | 3     | 0     |
| **3 c** | 2     | 0     | 2     | 1     |
| **4 $** | 1     | 0     | 0     | 0     |

---

### Filling in the blanks:

---

#### arr[1][1] → Blank 1:

- Matching `Z[1] = a`
- X[1] = a → match  
- Y[1] = a → match  

→ Both match → use:

```plaintext
arr[1][1] = 1 + max(arr[2][1], arr[1][2])
          = 1 + max(5, ?)
```

We must compute arr[1][2] next.

---

#### arr[1][2] → Blank 2:

- Matching `Z[2] = a`
- X[1] = a → match  
- Y[2] = c → no match  

→ Only X matches → use:

```plaintext
arr[1][2] = 1 + arr[2][2] = 1 + 4 = 5
```

---

Now we can finish arr[1][1]:

```plaintext
arr[1][1] = 1 + max(5, 5) = 6
```

---

#### arr[1][3] → Blank 3:

- Matching `Z[3] = c`
- X[1] = a → no match  
- Y[3] = b → no match  

→ Neither matches → use:

```plaintext
arr[1][3] = 0
```

---

#### arr[1][4] → Blank 4:

- Matching `Z[4] = a`
- X[1] = a → match  
- Y[4] = $ → no match  

→ Only X matches → use:

```plaintext
arr[1][4] = 1 + arr[2][4] = 1 + 0 = 1
```

---

### Final filled table:

| i / j   | a (1) | c (2) | b (3) | $ (4) |
|---------|-------|-------|-------|-------|
| **1 a** | **6** | **5** | **0** | **1** |
| **2 a** | 5     | 4     | 3     | 0     |
| **3 c** | 2     | 0     | 2     | 1     |
| **4 $** | 1     | 0     | 0     | 0     |

---

### Final answers for the blanks:

```plaintext
Blank 1 = 6
Blank 2 = 5
Blank 3 = 0
Blank 4 = 1
```

---

### Summary:

- We used the **DP recurrence** from the previous question.
- Each cell arr[i][j] depends on **Z[i + j - 1]**, X[i], and Y[j].
- The final result is stored at arr[1][1].
- This example shows how **bottom-up DP** works step by step.

---
## 6 Question: Which algorithm is faster? (Graham’s scan vs Jarvis’s march)

We are given **n points on concentric circles**.

We want to compare:

- **Graham’s scan** → O(n log n)
- **Jarvis’s march** → O(n * h), where h = number of points on the convex hull

---

### Case 1:

**Each circle contains k points (k is a constant), and there are n / k circles.**

- Total points = n
- Outermost circle has k points → h = O(1)
- Running times:

    - Graham’s scan → O(n log n)
    - Jarvis’s march → O(n * 1) = O(n)

**Blank 1 Answer:**  
Jarvis’s march is faster → **O(n)** vs O(n log n)

---

### Case 2:

**Each circle contains n / k points (k is a constant), and there are k circles.**

- Total points = n
- Outermost circle has n / k = Θ(n) points → h = Θ(n)
- Running times:

    - Graham’s scan → O(n log n)
    - Jarvis’s march → O(n * n) = O(n²)

**Blank 2 Answer:**  
Graham’s scan is faster → **O(n log n)** vs O(n²)

---

### Case 3:

**Each circle contains √n points, and there are √n circles.**

- Total points = √n * √n = n
- Outermost circle has √n points → h = O(√n)
- Running times:

    - Graham’s scan → O(n log n)
    - Jarvis’s march → O(n * √n) = O(n^(3/2))

**Blank 3 Answer:**  
Graham’s scan is faster → **O(n log n)** vs O(n^(3/2))

---

### Final summary:

| Case | Graham’s scan | Jarvis’s march | Which is faster? |
|------|---------------|----------------|------------------|
| Blank 1 | O(n log n)   | O(n)           | **Jarvis’s march** |
| Blank 2 | O(n log n)   | O(n²)          | **Graham’s scan** |
| Blank 3 | O(n log n)   | O(n^(3/2))     | **Graham’s scan** |

---
## 7 Question: Convex Layers — Algorithm and Analysis

We can break a set of 2D points into **convex layers**:

- The **1st layer** is the convex hull of all points.
- The **2nd layer** is the convex hull of the remaining points after removing the 1st layer.
- The **k-th layer** is the convex hull of points remaining after removing the first k-1 layers.
- Continue until no points remain.

---

### Simple algorithm (using Graham’s scan):

```plaintext
Input: set of n points
Output: convex layers (list of lists of points)

Algorithm:

1. Initialize: layers = empty list

2. While the set of points is not empty:

    a. Compute the convex hull of the current set of points (using Graham’s scan → O(m log m), where m is the current number of points).
    
    b. Add the convex hull as a new layer in "layers".
    
    c. Remove the convex hull points from the set of points.
    
3. Return "layers"
```

---

### Running time analysis:

Let:

- n = total number of points
- k = number of convex layers

Each time we run Graham’s scan:

- 1st layer: O(n log n)
- 2nd layer: O((n₁) log n₁), where n₁ < n
- 3rd layer: O((n₂) log n₂), etc.

---

**Worst case:**

If only **O(1)** points are removed in each layer → up to **O(n)** layers → k = O(n)

Then total time is:

```plaintext
O(n log n) + O((n-1) log (n-1)) + O((n-2) log (n-2)) + ... + O(1 log 1)

= O(n log n) + O(n log n) + ... + O(n log n)  → up to O(n) times

= O(n² log n)
```

---

**Best / typical case:**

If each convex hull removes **Θ(n / k)** points per layer:

- There are **k layers**.
- Each layer takes O(n log n) time (since points shrink geometrically).

Then total time:

```plaintext
O(k * n log n)
```

---

### Final worst-case result:

```plaintext
O(n² log n)   → worst case (if k = O(n))
O(k * n log n) → if k is small
```

---

### Summary:

- The simple algorithm is:

    → **Repeatedly run Graham’s scan**, remove each layer.

- Worst-case running time:

    → **O(n² log n)** if there are many layers.

- If k is small:

    → **O(k * n log n)**.

---
## 8 Question: Can we parallelize the for loop on lines 6-7?

```plaintext
6   for i = l to r
7      if A[i] < A[q] then q = i
```

**Answer:**  
No, we cannot parallelize this loop.

**Explanation:**  
There would be a **race condition**:

- All threads would be **reading and writing to the same variable q**.
- Since **q is being updated inside the loop**, parallel execution would lead to inconsistent updates → incorrect result.

Therefore, this loop must remain **sequential**.

---

## 9 Question: What is the span of PLAY?

**Given recurrence for span:**  
```plaintext
S(n) = S(n/2) + Θ(n)
```

**Explanation:**  

- The recursive structure of PLAY is a **divide-and-conquer**:

    - One recursive call is spawned → runs in parallel.
    - One call is run in the current thread.
    - Then there is a sequential combine phase → loop on lines 6-7 → Θ(n) span.

- The **parallel for** on line 8 has span **Θ(log n)**, but it is dominated by the Θ(n) span from lines 6-7.

---

**Solution of recurrence:**  

```plaintext
S(n) = S(n/2) + Θ(n) → solves to Θ(n)
```

---

### Correct Answer:

**d. Θ(n)**

---

## 10 Question: What is the parallelism of PLAY?

**Work W(n):**

```plaintext
W(n) = 2 W(n/2) + Θ(n)
```

This solves to:

```plaintext
W(n) = Θ(n log n)
```

---

**Span S(n):**

```plaintext
S(n) = Θ(n)
```

---

**Parallelism = Work / Span:**

```plaintext
P(n) = W(n) / S(n) = Θ(n log n) / Θ(n) = Θ(log n)
```

---

### Correct Answer:

**d. Θ(log n)**

---

### Final Summary:

| Question | Correct Answer | Reason |
|----------|----------------|--------|
| Q8       | No             | Race condition on q |
| Q9       | Θ(n)           | Span dominated by sequential loop |
| Q10      | Θ(log n)       | Parallelism = Work / Span = Θ(log n) |

---
## 11 Question: Worst-case running time of an operation from S

**Given:**

- Dynamic table with expansion & contraction factor 2.
- Load factor α ≥ 1/4.
- Random sequence S of n operations (insert/delete chosen randomly).

---

**Worst-case for a single operation:**

- If an operation triggers an expansion (or contraction), the cost is proportional to copying the entire table → Θ(n).

---

### Correct Answer:

**d. Θ(n)**

---

## 12 Question: Best-case running time of the whole sequence S

**Best case:**

- No expansion or contraction happens.
- Each operation runs in Θ(1) time.
- Total of n operations → Θ(n).

---

### Correct Answer:

**a. Θ(n)**

---

## 13 Question: Worst-case running time of the whole sequence S

**Key point:**

- Dynamic table guarantees **amortized Θ(1)** per operation, even in worst case.
- So n operations → Θ(n), even if the first few cause expansion/contraction.
- The sequence starts with n elements, but since the sequence length is also n, expensive operations are still amortized.

---

### Correct Answer:

**c. Θ(n)**

---

## 14 Question: Amortized cost of an insertion — special cases

**Blank 1:**  
If on each table expansion we ran a loop to find the current maximum element:

- The expansion already costs Θ(n).
- The loop to find the maximum is Θ(n) → does not change asymptotic cost.
- **Would not increase** amortized cost.

---

**Blank 2:**  
If we expanded not by a factor of 2 but by a factor of log₂ n:

- Expansions become even less frequent → more efficient.
- Cost would be amortized over **even more** operations.
- **Would not increase** amortized cost.

---

### Final Answers:

```
Blank 1: would not increase
Blank 2: would not increase
```

---

## Summary:

| Question | Correct Answer | Reason |
|----------|----------------|--------|
| Q11      | Θ(n)           | Expansion takes Θ(n) |
| Q12      | Θ(n)           | Best case: Θ(1) per op |
| Q13      | Θ(n)           | Amortized Θ(1) per op |
| Q14 Blank 1 | would not increase | Loop is Θ(n), same as expansion |
| Q14 Blank 2 | would not increase | Expansions less frequent |

---
## 15 Question: CDCL Trace — Learned Clauses

**Given trace:**  

```
X1   → X2  
X2   → X10  
X10  → □3

¬X3  → X4  
¬X3  → ¬X6  
X5   → ¬X6  
X5   → X7  
X5   → X8  
X5   → □2

¬X6  → □1  
¬X6  → ¬X9  
X7   → ¬X9  
X7   → □2  
X8   → □3 
```

**Splitting variables:**  
`X1`, `X3`, `X5`

---

### How to compute learned clauses:

- **Start from the conflict (□)**
- Backtrack using the implication graph
- The learned clause is: "negation of the latest assignments on each branch to the conflict"

---

### Learned Clauses:

1️⃣ From □1:

- Clause involves **¬X6**
- ¬X6 came from **¬X3** and **X5**
- So we get:

```
{x3, not x5}
```

---

2️⃣ From □2:

- Clause involves **X5 → □2** and **X7 → □2**
- So the conflict came from **X5**
- Learned clause:

```
{not x5}
```

---

3️⃣ From □3:

- Clause involves **X1 → X2 → X10 → □3**  
- And also **X8 → □3**  
- X8 came from **X5**
- Learned clause:

```
{not x1, not x5}
```

---

### Final Answer (Learned Clauses):

```plaintext
{x3, not x5}

{not x5}

{not x1, not x5}
```

---

## 16 Question: Was this clause part of the original formula?

### Clause 1: {not x2, x3}

**Answer:**  
→ Was NOT a clause in the formula.  
If it was, x3 would have been forced immediately when x2 was set — but x3 was a split variable.

---

### Clause 2: {not x1, x2}

**Answer:**  
→ Was a clause in the formula.  
X2 was unit-propagated after X1 → consistent with this clause being in the formula.

---

### Clause 3: {x1, x2}

**Answer:**  
→ Could have been in the formula or not.  
No contradiction with the trace either way.

---

### Clause 4: {not x2, x3, x4}

**Answer:**  
→ Was a clause in the formula.  
X4 was unit-propagated after ¬X3 → consistent with this clause.

---

### Summary (Q16):

```plaintext
{not x2, x3} → was not a clause in the formula

{not x1, x2} → was a clause in the formula

{x1, x2} → could have been in the formula or not

{not x2, x3, x4} → was a clause in the formula
```

---

## 17 Question: BDD Reasoning

---

### Clause 1: If |M(C1)| < |M(C2)|

**Answer:**  
→ **None of the above**.  
Number of satisfying assignments does not determine BDD size.

---

### Clause 2: If |M(C1)| = |M(C2)|

**Answer:**  
→ **None of the above**.  
Same number of models does not guarantee same BDD size.

---

### Clause 3: If M(C1) = M(C2)

**Answer:**  
→ **|B1| = |B2|**  
Same satisfying assignments → BDDs must be functionally identical → same size.

---

### Clause 4: If C1 = C2 + extra clauses

**Answer:**  
→ **None of the above**.  
Adding clauses can either shrink or grow the BDD → no guaranteed relation.

---

### How many BDD nodes:

---

1️⃣ Function that maps every assignment to true:

**Answer:**  
→ **1** (just terminal node "true")

---

2️⃣ Function that is unsatisfiable:

**Answer:**  
→ **1** (just terminal node "false")

---

3️⃣ Function "x" (true if x = T, false otherwise):

```
x
 ↘ T → 1
 ↘ F → 0
```

**Answer:**  
→ **3 nodes** (x node + true + false terminals)

---

4️⃣ Function "x and not y":

```
x
 ↘ F → 0
 ↘ T → y
      ↘ T → 0
      ↘ F → 1
```

**Answer:**  
→ **4 nodes** (x, y, true, false)

---

### Final Answers (Q17):

```plaintext
If |M(C1)| < |M(C2)| → None of the above

If |M(C1)| = |M(C2)| → None of the above

If M(C1) = M(C2) → |B1| = |B2|

If C1 = C2 + extra clauses → None of the above

---

Function "true" → 1 node

Function "unsatisfiable" → 1 node

Function "x" → 3 nodes

Function "x and not y" → 4 nodes
```

---

### Final Summary:

| Question | Correct Answer |
|----------|-----------------|
| Q15 (Learned clauses) | {x3, not x5}, {not x5}, {not x1, not x5} |
| Q16 (Was in formula?) | See above summary |
| Q17 (BDD reasoning) | See above summary |

---
## 20 Question: Planning — Action Interference, Encoding Steps

**Facts:**  
P = {a1, a2, b1, b2, c}

**Initial state:**  
I = {} (no fact is true in the initial state)

**Goal:**  
G = {c}

---

### Actions:

```plaintext
get-a1:
    pre: {}
    add: {a1}
    del: {}

get-a2:
    pre: {}
    add: {a2}
    del: {}

get-b1:
    pre: {a1}
    add: {b1}
    del: {a1}

get-b2:
    pre: {a2, b1}
    add: {b2}
    del: {a2}

get-c:
    pre: {a1, a2, b1, b2}
    add: {c}
    del: {a1, a2, b1, b2}
```

---

### Do the following pairs of actions interfere?

---

**Definition of interference:**  
Two actions interfere if **one deletes a precondition or add-effect of the other**, or if both update (add/del) the same fact in conflicting ways.

---

### Pair 1: get-a1 and get-a2

- get-a1 → add {a1}, does not delete anything.
- get-a2 → add {a2}, does not delete anything.
- No shared effects or deletes → **no interference**.

**Answer:**  
→ **not interfere**

---

### Pair 2: get-a1 and get-b1

- get-b1 requires **pre: {a1}**, and deletes {a1}.
- If get-a1 is adding {a1}, running both in parallel may interfere:
    - get-a1 tries to produce {a1}.
    - get-b1 may delete it → conflict in ordering.

**Answer:**  
→ **interfere**

---

### Pair 3: get-a1 and get-b2

- get-b2 requires pre {a2, b1} → does not depend on {a1}.
- No overlapping facts or deletes.
- They are independent.

**Answer:**  
→ **not interfere**

---

### Pair 4: get-a1 and get-c

- get-c requires pre {a1, a2, b1, b2}.
- get-c deletes {a1}.
- get-a1 adds {a1}.
- Conflict → adding and deleting {a1} at the same step.

**Answer:**  
→ **interfere**

---

### Pair 5: get-b1 and get-b2

- get-b1 → adds {b1}, deletes {a1}.
- get-b2 → requires pre {a2, b1}, deletes {a2}.
- No conflicting deletes.
- No overlap in deletes/adds.

**Answer:**  
→ **not interfere**

---

## Encoding steps:

---

### Sequential encoding:

- Actions must be scheduled **one per step**.

Plan:

1️⃣ get-a1  
2️⃣ get-a2  
3️⃣ get-b1  
4️⃣ get-b2  
5️⃣ get-c

BUT → because of deletions → in worst case, sometimes we need to **re-get** a1 or a2 if needed by get-c:

Example worst-case plan:

1️⃣ get-a1  
2️⃣ get-a2  
3️⃣ get-b1  
4️⃣ get-b2  
5️⃣ get-a1 (again, because get-b1 deleted a1)  
6️⃣ get-a2 (again, because get-b2 deleted a2)  
7️⃣ get-c

→ **7 steps**

**Answer:**  
→ **7**

---

### Parallel (forall-step) encoding:

- Actions can run in parallel **if they do not interfere**.

Plan:

- **Step 1:** get-a1 and get-a2 (parallel)
- **Step 2:** get-b1
- **Step 3:** get-b2
- **Step 4:** re-get a1 and a2 (parallel)
- **Step 5:** get-c

→ **5 steps**

**Answer:**  
→ **5**

---

## Initial state is empty:

→ No facts are true at step 0 → we must explicitly encode that **all variables are false at first layer**.

**Answer:**  
→ **we need to explicitly set all the variables in the first layer to false**

---

## Final Answers (Q20):

```plaintext
get-a1 and get-a2 → not interfere

get-a1 and get-b1 → interfere

get-a1 and get-b2 → not interfere

get-a1 and get-c → interfere

get-b1 and get-b2 → not interfere

Sequential encoding steps → 7

Parallel (forall-step) encoding steps → 5

Since initial state is empty → we need to explicitly set all variables in first layer to false
```

---

## Summary:

| Pair                      | Interfere? |
|--------------------------|------------|
| get-a1 and get-a2         | not interfere |
| get-a1 and get-b1         | interfere |
| get-a1 and get-b2         | not interfere |
| get-a1 and get-c          | interfere |
| get-b1 and get-b2         | not interfere |

| Encoding Type            | Steps |
|--------------------------|-------|
| Sequential               | 7     |
| Parallel (forall-step)   | 5     |

| Initial State | Answer |
|---------------|--------|
| Initial empty | we need to explicitly set all variables in first layer to false |

---
