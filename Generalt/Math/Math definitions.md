
# Set operations

## Powerset ($\mathcal{P}(X)$)      
The powerset of a set $X$ is the set of all possible subsets of $X$, including the empty set. 
For example, if $X = \{1, 2\}$, then $\mathcal{P}(X) = \{\emptyset, \{1\}, \{2\}, \{1, 2\}\}$.
### $$\mathcal{P}(X) = \{S|S\subseteq X\}$$

## Subset ($A\subseteq B$)

The subset means that one set is contained within another set.
For instance, if $A=\{1,2\}$ and $B=\{1,2,3\}$ then $A\subseteq B$

### $$A\subseteq B \Leftrightarrow \forall a \in A. a\in B $$

## Intersection ($A \cap B$)        
The intersection of two sets $A$ and $B$ is the set of elements that are common to both sets. 
For instance, if $A = \{1, 2, 3\}$ and $B = \{2, 3, 4\}$, then $A \cap B = \{2, 3\}$.

### $$A\cap B =\{x| x \in A \land x \in B \}$$
## Union ($A \cup U$)

The union of two sets $A$ and $B$ is the set containing all elements that are in $A$, $B$, or both. For example, if $A = \{1, 2, 3\}$ and $B = \{3, 4, 5\}$, then $A \cup B = \{1, 2, 3, 4, 5\}$.

### $$A\cup B =\{x| x \in A \lor x \in B \}$$
## Cartesian Product ($A \times B$) 
The Cartesian product of sets $A$ and $B$ is the set of all possible ordered pairs $(a, b)$ where $a$ is from $A$ and $b$ is from $B$. 
For example, if $A = \{1, 2\}$ and $B = \{x, y\}$, then $A \times B = \{(1, x), (1, y), (2, x), (2, y)\}$.
### $$A\times B =\{(a,b)| a \in A \land b \in B \}$$
## Complement ($A^c$)               
The complement of a set $A$ with respect to the universe $U$ is the set of all elements in $U$ that are not in $A$. For instance, if $U = \{1, 2, 3, 4\}$ and $A = \{2, 3\}$, then $A^c = \{1, 4\}$.
### $$A^c = U \backslash A = \{x| x \in U \land x \notin A \}$$

## Relations

We will often be interested in relations having the following properties $R \subseteq A \times A$.

We will often be interested in relations having the following properties:
###  Reflexive: $$\forall a \in A, (a,a) \in R$$
### Symmetric: $$\forall a, b \in A, (a,b) \in R \Rightarrow (b,a) \in R$$

### Antisymmetric: $$\forall a, b \in A, (a,b) \in R \land (b,a) \in R \Rightarrow a = b$$
### Transitive: $$\forall a, b, c \in A, (a,b) \in R \land (b,c) \in R \Rightarrow (a,c) \in R$$

# Quantifiers


## For all ($\forall$)
The symbol $\forall$ denotes the universal quantifier, indicating that a statement holds for all elements in a set.$\forall x$ is read as "for all $x$" or "for every $x$". 
$\forall x \in X$, where $X$ is the set under consideration.
$\forall x \in \mathbb{N}, x > 0$, which reads as "for all natural numbers $x$, $x$ is greater than 0.
## There Exists Quantifier ($\exists$)
The symbol $\exists$ denotes the existential quantifier, indicating that there exists at least one element in a set for which a statement holds true.
$\exists x$ is read as "there exists an $x$".
$\exists x \in X$, where $X$ is the set under consideration.
$\exists x \in \mathbb{R}, x^2 = 4$, which reads as "there exists a real number $x$ such that $x^2 = 4$."

# Functions

A function (or mapping) describes an input-output assignment. 
The set of possible inputs to the function is called the domain of $f$, denoted as $\text{dom}(f)$. The outputs are the elements of a set called the range of $f$, denoted as $\text{range}(f)$.

An $A$-ary function is a function of type $f : A_1 \times \ldots \times A_k \rightarrow B$. 
We call $a_i \in A_i$. the arguments of $f$, 
$k$ is called the arity of $f$, 
if $k=1$ the function is called unary; if $k=2$ it is called binary

Technically a function $f : A \rightarrow  B$ is just a binary relation between A, B such that 
for every element $a\in A$ there exists a unique element $f(a) \in B$ 

It is also important to node that if every input in the domain does not have a corresponding output in the range, then the function is called a partial function.

# Proofs

### Proof by construction (direct proof) 

In a constructive proof, one attempts to demonstrate $P \Rightarrow Q$ directly. This is the simplest and easiest method of proof available to us. There is only one step to a direct proof (the second part being the tricky one):

#### Logical definition

1. Assume that $P$ is true 
2. use $P$ to show that $Q$ must be true.

#### Example
**Theorem 1.** If $a$ and $b$ are consecutive integers, then the sum $a+b$ is odd.
##### **Proof.**
Assume that $a$ and $b$ are consecutive integers. Because $a$ and $b$ are consecutive, we know that $b = a+1$. Thus, the sum $a+b$ may be rewritten as $2a+1$. Thus, there exists a number $k$ such that $a+b = 2k+1$, so the sum $a+b$ is odd.
### Proof by Contradiction

The proof by contradiction is grounded in the fact that any proposition must be either true or false, but not both true and false at the same time. We arrive at a contradiction when we are able to demonstrate that a statement is both simultaneously true and false, showing that our assumptions are inconsistent. We can use this to demonstrate $P \Rightarrow Q$ by assuming both $P$ and $\neg Q$ are simultaneously true and deriving a contradiction. When we derive this contradiction, it means that one of our assumptions was untenable. Presumably, we have either assumed or already proved $P$ to be true so that finding a contradiction implies that $\neg Q$ must be false. The method of proof by contradiction:

#### Logical definition

1. Assume that $P$ is true.
2. Assume that $\neg Q$ is true.
3. Use $P$ and $\neg Q$ to demonstrate a contradiction.

#### Example

**Theorem 2.** If $a$ and $b$ are consecutive integers, then the sum $a+b$ is odd.

##### **Proof.**
Assume that $a$ and $b$ are consecutive integers. Assume also that the sum $a +b$ is not odd. Because the sum $a+b$ is not odd, there exists no number $k$ such that $a +b = 2k+1$. However, the integers $a$ and $b$ are consecutive, so we may write the sum $a+b$ as $2a+1$. Thus, we have derived that $a+b= 2k +1$ for any integer $k$ and also that $a + b = 2a + 1$. This is a contradiction. If we hold that $a$ and $b$ are consecutive, then we know that the sum $a + b$ must be odd.


A proof by contradiction assumes the negation of the proposition to be proven and derives a contradiction.

### Proof by Mathematical Induction

#### Logical definition

To demonstrate $P \Rightarrow Q$ by induction, we require that the truth of $P$ and $Q$ be expressed as a function of some ordered set $S$.

1. (Basis) Show that $P \Rightarrow Q$ is valid for a specific element $k$ in $S$.
2. (Inductive Hypothesis) Assume that $P \Rightarrow Q$ for some element $n$ in $S$.
3. Demonstrate that $P \Rightarrow Q$ for the element $n+1$ in $S$.
4. Conclude that $P \Rightarrow Q$ for all elements greater than or equal to $k$ in $S$.

#### Example
**Theorem 8.** Show that the summation formula $\sum_{i=1}^{n} i$ is valid for all integers $n$. $i = \frac{n(n+1)}{2}$

##### **Proof.**
(Basis case) We demonstrate that the formula is valid for $n = 1$. By substituting $1$ for $n$, the formula gives us $1 = \frac{1(2)}{2}$, which is true.

(Inductive Hypothesis) Suppose that the formula is valid for some integer $n$. 

To demonstrate that the formula is valid for $n + 1$, we must use the inductive hypothesis to show that the formula still holds. By assumption, the formula is valid for $n$. Using basic algebra, we add $n+1$ to both sides of the equation to demonstrate that the formula is still valid for $n+1$. We begin with the left-hand side:
$$\sum_{i=1}^{n+1} i + (n+1) = \sum_{i=1}^{n} i + (n+1)$$
We now demonstrate adding $n + 1$ to the right-hand side. We perform fraction addition and factor out an $(n + 1)$.
$$\frac{n(n +1)}{2} + (n+1) = \frac{n(n+1)+2(n+1)}{2} = \frac{(n+1)(n+2)}{2}$$
Combining the right-hand sides of equations two and three yields:
$$\sum_{i=1}^{n+1} i = \frac{(n+1)(n+2)}{2}$$
Which is exactly what we require. Thus, if the formula is valid for $n$, then the formula must be valid for $n +1$ as we have shown above. Thus, by mathematical induction over the integers, the summation formula is valid for all integers greater than or equal to one.


### Proof by Contrapositive

Proof by contraposition is a method of proof which is not a method all its own per se. From first-order logic we know that the implication $P \Rightarrow Q$ is equivalent to $\neg Q \Rightarrow \neg P$. The second proposition is called the contrapositive of the first proposition. By saying that the two propositions are equivalent we mean that if one can prove $P \Rightarrow Q$ then they have also proved $\neg Q \Rightarrow \neg P$, and vice versa. Proof by contraposition can be an effective approach when a traditional direct proof is tricky, or it can be a different way to think about the substance of a problem.

#### Logical definition

Recall that first-order logic shows that the statement  $P \Rightarrow Q$ is equivalent to  $\neg Q \Rightarrow \neg P$

1. Assume $\neg Q$ is true. 
2. Show that $\neg P$ must be true. 
3. Observe that  $P \Rightarrow Q$by contraposition.

#### Example

**Theorem 4.** If the sum $a + b$ is not odd, then $a$ and $b$ are not consecutive integers.

It is important to be extremely pedantic when interpreting a contraposition. It would be tempting to claim that the above theorem claims that the sum of two numbers is odd only when those two numbers are consecutive. However, this is nonsense.

##### **Proof.**
Assume that the sum of the integers $a$ and $b$ is not odd. Then, there exists no integer $k$ such that $a + b = 2k +1$. Thus, $a+b= k +(k +1)$ for all integers $k$. Because $k +1$ is the successor of $k$, this implies that $a$ and $b$ cannot be consecutive integers.


## Proof techniques other

## Pumping lemma for regular languages

The pumping lemma state that for any given string in a regular [[Automata and Languages Definitions#Language of an automata|language]] the strings can be "pumped" if they are at least as long as a certain special value, called the *pumping length*. That means that each such string contains a section that can be repeated any number of times with the resulting string remaining in the language.

### Formal definition
If $A$ is a [[Automata and Languages Definitions#Regular language|regular language]], then there is a number $\mathcal{p}$ (the pumping length) where if $s$ is any string in $A$ of length at least $\mathcal{p}$, then $s$ may be divided into three pieces, $s=xyz$, satisfying the following conditions

1. $\forall i \geq 0. (xy^iz\in A)$ 
2. $|y| >0$
3. $|xy|\leq \mathcal{p}$

Recall the notation where $|s|$ represents the length of string $s$, $y^i$ means that $i$ copies of $y$ are concatenated together and $y^0=\epsilon$. When $s$ is divided into $xyz$ either $x$ or $z$ may be $\epsilon$ but condition 2 says $y\neq \epsilon$. Condition 3 states that the pieces $xy$ together have length at most $\mathcal{p}$, this is an extra technical condition that sometimes becomes useful when proving certain languages to be non regular

#### [[Math definitions#Proof by Contrapositive|Contrapositive]] form

Let $A$ be a language. Suppose that the following holds:

For all $p\geq0$ there exits a string $s\in A$ with $|w|\geq p$ such that, for all $x,y,z$ with $w=xyz$, $y\neq \epsilon$ and $|xy|\leq p$ there exist $i\geq 0$ such that $xy^iz\notin A$
Then $A$ is not regular

## Game form

1. The demon picks $p$
2. You pick $s\in A$ such that $|s|\geq p$
3. The demon picks $x,y,z$ s.t. $s=xyz,y\neq \epsilon$ and $|xy|\leq p$
4. You pick $i\geq 0$
you win if $xy^iz\notin A$; the demon wins if $xy^iz\in A$ 
# Definitions

## Pidgeon hole principle

the **pigeonhole principle** states that if n items are put into m containers, with _n_ > _m_, then at least one container must contain more than one item. In state terms this means,

For example, the following image shows an FSA.

[![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/An_automat_accepting_the_language_a%28bc%29%2Ad.svg/170px-An_automat_accepting_the_language_a%28bc%29%2Ad.svg.png)](https://en.wikipedia.org/wiki/File:An_automat_accepting_the_language_a(bc)*d.svg)

The FSA accepts the string: **abcd**. Since this string has a length at least as large as the number of states, which is four (so the total number of states that the machine passes through to scan **abcd** would be 5), the [pigeonhole principle](https://en.wikipedia.org/wiki/Pigeonhole_principle "Pigeonhole principle") indicates that there must be at least one repeated state among the start state and the next four visited states.