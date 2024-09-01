# Strings and Languages 

## Alphabet

An alphabet is a finite nonempty set.

### Properties

#### Lexicographically order

If the alphabet $\Sigma$ is ordered then the set of strings over $\Sigma$ can be ordered lexicographically: 
$$w\preceq w' \Leftrightarrow\ (w\ \ \text{prefix of} \ \ w') \ \ \text{or} \ \ \exists a\leq b \in \Sigma. \begin{cases} ua & \text{prefix of } w  \\ ub & \text{prefix of } w' \end{cases}$$

### Examples:

**The binary alphabet**: $\Sigma =\{1,0\}$
**The Danish alphabet:** $\Sigma = \{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,x,y,z,æ,ø,å\}$


## String

A string (or word) over an alphabet is a finite sequence of symbols.

### Properties

#### Length 
The length of a string $w$, written $|w|$ is the number of symbols it contains
#### Reverse
The reverse of a string $w$ written $w^R$ is the string obtained by writing $w$ in the opposite order
### Examples: 

The string Hello is a string over the Danish alphabet and has the length 5.
The binary string 0101 is a string over the binary alphabet and has the length 4


## Substring

1. A string is a substring of $s$ if it appears consecutively within $s$; 
	1. Examples: Let $s = \text{"abracadabra"}$, $\text{"ab"}$, $\text{"cad"}$, $\text{"d"}$, $\text{"a"}$, ...
2. A string is a prefix of $s$ if it appears at the beginning of $s$; 
	1. Examples: $\text{"a"}$, $\text{"ab"}$, $\text{"abra"}$, ...
3. A string is a suffix of $s$ if it appears at the end of $s$; 
	1. Examples: $\text{"a"}$, $\text{"ra"}$, $\text{"bra"}$, ...


## The empty string

The empty string, written $\epsilon$ is the string that contains no symbols
## Language

A language over the alphabet $\Sigma$ is a set of strings over $\Sigma$. We denote by $\Sigma^*$ the language of all strings over $\Sigma$ 




## Nonregular language

While Automata has a lot of power it also has some limitations, some languages can't be recognized by any meaning that they are nonregular languages.  An example of a nonregular language is $$B=\{0^n1^n|n\geq0\}$$When trying to create a automata from this language one will quicky notice since you need to keep track of how many 0 there are before the 1 and that it is unbounded one will have to keep track of an infinite amount of 0s and you also need to remember how many zeros there where. 



# String operations

## String concatenation 

Given strings $w$ and $w'$ over the same alphabet, the concatenation of $w$ and $w'$, written $ww'$, is the string obtained by appending $w'$ to the end of $w$.

Examples: For $w = \text{"ab"}$ and $w' = \text{"cd"}$, 
$\begin{align*} ww' &= \text{"abcd"}, \\ w'w &= \text{"cdab"}, \\ w^3 &= \text{"ababab"}. \end{align*}$

### Note that
- The empty string is the identity element: $\epsilon w = w = w\epsilon$.
- If $w$ is a prefix of $x$, then $x = w'w$ for some $w'$.
- If $w$ is a suffix of $y$, then $y = ww'$ for some $w'$.
- If $z$ is a substring of $w$, then $w = xzw'$ for some $x, w'$.

# Language operations

**All capital letters are languages**

## Union

### $$A\cup B = \{x| x\in A \lor B\}$$
The class of [[Automata and Languages Definitions#Regular language|regular languages]] is closed under the union operation. Meaning that if $A$ and $B$ are both regular languages then $A\cup B$ is also. 

## Concatenation

### $$A\circ B = \{xy| x\in A \land y\in B\}$$
The class of [[Automata and Languages Definitions#Regular language|regular languages]] is closed under the concatenation operation. Meaning that if $A$ and $B$ are both regular languages then $A\circ B$ is also. 

## Star

### $$A^* = \{x_1x_2\dots x_k| k\geq0 \ \ \text{and each} \ \ x_i \in A\}$$
The class of [[Automata and Languages Definitions#Regular language|regular languages]] is closed under the concatenation operation. Meaning that if $A$ is a regular language then $A^*$ also is. 
# Automata

## Language of an automata

If $A$ is the set of [[Automata and Languages Definitions#Strings and Languages#String|strings]] that a machine $M$ accepts, we say that $A$ is the [[Automata and Languages Definitions#Strings and Languages#Language|language]] of machine $M$ and write $L(M)=A$. We say that $M$ recognizes $A$ or $M$ accepts $A$

### Regular language

A [[Automata and Languages Definitions#Strings and Languages#Language|language]] is said to be regular  if some finite automata recognizes it. 

## Definite Finite Automata

### Definition

A Definite Finite Automaton is a 5-tuple $(Q, \Sigma,\delta, q_0,F)$

Being a definite finite automata means that for each input symbol in $\Sigma$ a state must have a transition function for that symbol and ONLY ONE. So in layman's terms, every state must have only one  outgoing arrow with that symbol


Example of a DFA:

![[Pasted image 20240316164951.png]]

#### $Q$ is a finite set of states

Q is the set of states in the automata, if the automata $M$ has two states $q_1,q_2$ then $Q=\{q_1,q_2\}$

#### $\Sigma$  is a finite set called the [[Automata and Languages Definitions#Alphabet|Alphabet]]

![[Automata and Languages Definitions#Alphabet]]
#### $\delta: Q \times \Sigma \rightarrow Q$ Is the transition function 

The transition [[Math definitions#Functions|function]] is the function that defines the rules for moving withing the DFA. It maps a state to a symbol and outputs a new state. The domain is the [[Math definitions#Cartesian Product ($A times B$)|cartesian product]] of $Q$ and $\Sigma$. And the range is $Q$
It is a binary function as it takes 2 arguments 

**A DFA**: must have exactly one transition exiting every state for each possible input symbol.  meaning the function must cant be partial
#### $q_0 \in Q$ is the start state
 
$q_0$ is the start state of the automata, meaning the state from which the input first enters. **There must be at least one start state **

#### $F\subseteq Q$ is the set of accept states 

The set of accept states $F$  is a [[Math definitions#Subset ($A subseteq B$)|subset|]] of $Q$ and are the states in the automata that if the input ends there the automata accepts the input. More formal if input ends at a state $q$ and $q\in F$ then the automata accepts the input





## Nondeterministic Finite Automata 

### Definition
A Non-Deterministic Finite Automaton (NFA) is characterized by a 5-tuple $(Q, \Sigma, \delta, q_0, F)$, where:

In the context of NFAs, the transition function $\delta$ is non-deterministic, implying that for a given state and input symbol, multiple possible next states may exist. This non-deterministic behavior reflects the automaton's capability to have various choices of paths for a given input symbol.

In simpler terms, an NFA allows multiple arrows to leave a state, all labeled with the same input symbol. Consequently, upon encountering that input symbol, the automaton can potentially transition to multiple states simultaneously or non-deterministically, resulting in branching computation paths.

Regarding the function's nature, an NFA can represent both partial and total functions:

- **Partial Function**: If for any state and input symbol, there exist transitions that are undefined or lead to no state (i.e., a transition maps to an empty set of states), the NFA represents a partial function. In this case, certain inputs may not lead to any valid computation path.
    
- **Total Function**: If for every state and input symbol, there exists at least one valid transition leading to a non-empty set of states, the NFA represents a total function. This implies that for any input, there is at least one valid computation path within the automaton.
#### $Q$ is a finite set of states

Q is the set of states in the automata, if the automata $M$ has two states $q_1,q_2$ then $Q=\{q_1,q_2\}$

#### $\Sigma$  is a finite set called the [[Automata and Languages Definitions#Alphabet|Alphabet]]
![[Automata and Languages Definitions#Alphabet]]


#### $\delta: Q \times \Sigma_\epsilon \rightarrow \mathcal{P}(Q)$ Is the transition function 

The transition [[Math definitions#Functions|function]] is the function that defines the rules for moving withing the NFA. It maps a state to a symbol and outputs a new state. The domain is the [[Math definitions#Cartesian Product ($A times B$)|cartesian product]] of $Q$ and $\Sigma_\epsilon$. And the range is [[Math definitions#Powerset ($ mathcal{P}(X)$)|powerset]] of $Q$
It is a binary function as it takes 2 arguments 

Unlike a DFA, an NFA can have transitions that are not defined, and have multiple transitions for each input symbol. This means that the function can be partial.
#### $q_0 \in Q$ is the start state
 
$q_0$ is the start state of the automata, meaning the state from which the input first enters. **There must be at least one start state **

#### $F\subseteq Q$ is the set of accept states 

The set of accept states $F$  is a [[Math definitions#Subset ($A subseteq B$)|subset|]] of $Q$ and are the states in the automata that if the input ends there the automata accepts the input. More formal if input ends at a state $q$ and $q\in F$ then the automata accepts the input




### DFA and NFA equivalence 

Every NFA has an equivalent DFA

If k is the number of states in the NFA then it has has a powerset of length $2^k$. Each of these ,according to the definition of the [[Automata and Languages Definitions#$ delta Q times Sigma_ epsilon rightarrow mathcal{P}(Q)$ Is the transition function|transition function]] for an NFA, it must mean that the equivalent DFA must have to remember all of these possibilities meaning it will have $2^k$ states.

Note til Andreas lav transition function tables for NFA og brug den :) du klare den godt :D

#### Proof:

Let $N=(Q,\Sigma,\delta,q_0,F)$ be the NFA recognizing some [[Automata and Languages Definitions#Strings and Languages#Language|language]] A. We construct a DFA $M=(Q',\Sigma,\delta',q_0',F')$ recognizing A. 
##### Without $\epsilon$-transitions
 
Before doing the full construction let us consider the simpler case where there are no $\epsilon$-transitions.

1. $Q'=\mathcal{P}(Q)$
   This is saying that every state of M is a set of states from N. Or every state of M is a subset of the powerset of N
2. For $R\in Q'$ and $a\in \Sigma$, let $\delta'(R,a)=\{q\in |q\in \delta(r,a)\:\text{for some} \: r\in R\}$
   If $R$ is a state of M, it is also a set of states of N. When M reads a symbol $a$ in states $R$, it shows where $a$ takes each state in $R$. Because each state may go to a set of states, we take the union of these sets. In math terms $$\delta'(R,a)=\bigcup_{r\in R}\delta(r,a)$$
3. $q_0'=\{q_0\}$
   The DFA M starts in the state corresponding to the set containing just the start state of the NFA N.
4. $F=\{R\in Q' | R \: \text{contains an accept state of N}\}$
   The DFA M accepts if one of the possible states that N could be in at this point is an accept state
   
##### With $\epsilon$-transitions

To construct an equivalent DFA when there are $\epsilon$-transitions, we now add a new notation known as the epsilon closure of a state R. We define $E(R)$ to be the epsilon closure of the state R, meaning that we get out a collection of states that we can reach by going along epsilon transitions from R.
Formally for $R\subseteq Q$ let $$E(Q)=\{q | q\: \text{can be reached by going along 0 or more epsilon transitions} $$
Then we modify the transition function of M by this $E(\delta(r,a))$ thus $$\delta'(R,a) = \{q\in Q|q\in E(\delta(r,a))\: \text{for some} \: r \in R \}$$
In the other term
$$\delta'(R,a) = \bigcup_{r\in R} E(\delta(r,a))$$
the start state of the DFA M is now $q_0=E({q_0})$

## Generalized Nondeterministic Finite Automaton 

### Definition

A GNFA is a way to convert a DFA into its equivalent regular expression and it is characterized by  a 5-tuple $(Q, \Sigma, \delta, q_{start}, q_{accept})$

A GNFA accepts a string $w$ in $\Sigma^*$ if $w=w_1w_2\dots w_k$ where each $w_i$ is in $\Sigma^*$ and sequence of states $q_0q_1\dots q_k$, exists such that 

1. $q_0=q_{start}$ is the start state
2. $q_k=q_{accepts}$ is the accept state
3. For each i, we have $w_i\in L(R_i)$, where $R_i=\delta(q_{i-1},q_i)$ , in other words, $R_i$ is the expression on the arrow from $q_{i-1}$ to $q_i$

#### $Q$ is a finite set of states

Q is the set of states in the automata, if the automata $M$ has two states $q_1,q_2$ then $Q=\{q_1,q_2\}$

#### $\Sigma$  is a finite set called the [[Automata and Languages Definitions#Alphabet|Alphabet]]
![[Automata and Languages Definitions#Alphabet|Alphabet]]



#### $\delta: (Q-\{q_{accept}\}) \times (Q-\{q_{accept}\}) \rightarrow \mathcal{R}$ Is the transition function 

The transition [[Math definitions#Functions|function]] is the function that defines the rules for moving withing the GNFA. It maps a state to a symbol and outputs a new state. The domain is the [[Math definitions#Cartesian Product ($A times B$)|cartesian product]] of $Q$ and $\Sigma_\epsilon$. And the range is [[Math definitions#Powerset ($ mathcal{P}(X)$)|powerset]] of $Q$

It is a binary function as it takes 2 arguments 

#### $q_{start}$ the start state
#### $q_{accept}$ the accept state


#### Algorithm for converting

1. Let $k$ be the number of states of $G$
2. If $k$ = 2,  then $G$ Must consist of start state, an accept state and a single arrow connecting them and labeled with a regular expression $R$.
   Return the expression $R$
3. If $k>2$, we select any state $q_{rip}\in Q$ different from $q_{start}$ and $q_{accept}$ and let $G'$ be the GNFA $(Q', \Sigma, \delta', q_{start}, q_{accept})$ where $$Q'=Q-\{q_{rip}\}$$
   and for any $q_i \in Q'-\{q_{accept}\}$ and any $q_j\in Q'-\{q_{start}\}$ let $$\delta'(q_i,q_j)=(R_1)(R_2)^*(R_3)\cup(R_4)$$
   for for $R_1=\delta(q_i,q_{rip})$ , $R_r=\delta(q_{rip},q_{rip})$ $R_3=\delta(q_{rip},q_j)$ $R_4=\delta(q_i,q_j)$
4. Compute CONVERT(G') and return this value





## Pushdown Automata

A pushdown automata is similar to [[Automata and Languages Definitions#Nondeterministic Finite Automata|NFA]] but they contain an extra component called the stack, this stack serves as an extra memory.  A PDA can push symbols onto the stack and then pop them of the stack later to read them.

There exists to type of pushdown automata, the nondeterministic  pushdown automata and deterministic pushdown automata, but unlike [[Automata and Languages Definitions#Definite Finite Automata|DFA]] and [[Automata and Languages Definitions#Nondeterministic Finite Automata|NFA]] they are NOT [[Automata and Languages Definitions#DFA and NFA equivalence|equal]] in power, an NPDA can recognise certain languages that a DPDA cant. However a PDA and CFA are [[Automata and Languages Definitions#Context-Free Grammars|equal]] in terms of the languages that they can recognize.

A PDA does not know when it has reached the end of the stack, instead it often relies on special symbols to rely that information.

### Definition

A pushdown automata is a 6-tuple $(Q, \Sigma, \Gamma, \delta, q_0, F)$, where 

#### $Q$ is a finite set of states

Q is the set of states in the automata, if the automata $M$ has two states $q_1,q_2$ then $Q=\{q_1,q_2\}$

#### $\Sigma$  is a finite set called the [[Automata and Languages Definitions#Alphabet|alphabet]]
![[Automata and Languages Definitions#Alphabet]]

#### $\Gamma$ is the stack  [[Automata and Languages Definitions#Alphabet|alphabet]]
#### $\delta: Q \times \Sigma_\epsilon \times \Gamma_\epsilon \rightarrow \mathcal{P}(Q\times \Gamma_\epsilon)$ Is the transition function 

#### $q_0 \in Q$ is the start state
 
$q_0$ is the start state of the automata, meaning the state from which the input first enters. **There must be at least one start state**

#### $F\subseteq Q$ is the set of accept states 

The set of accept states $F$  is a [[Math definitions#Subset ($A subseteq B$)|subset|]] of $Q$ and are the states in the automata that if the input ends there the automata accepts the input. More formal if input ends at a state $q$ and $q\in F$ then the automata accepts the input

#### Formal definition of computation
Let $M = (Q, \Sigma,\Gamma,\delta, q_0,F)$ be a finite automaton and let $w=w_1w_2\dots w_n$ be a [[Automata and Languages Definitions#Strings and Languages#String|string]] where each $w_i$ is a member of the [[Automata and Languages Definitions#Alphabet|alphabet]] $\Sigma_\epsilon$. Then $M$ accepts $w$ if a sequence of states $r_0,\dots , r_n$ in $Q$ and strings $s_0\dots s_n$ in  $\Gamma^*$ exists and fulfils the three conditions:
1. $r_0 = q_0$ and  $s_0=\epsilon$ the $s_0=\epsilon$ indicates that the stack starts empty 
2. For $i=0,\dots n-1$ we have $(r_{i+1},b)\in\delta(r_i,w_{i+1},a)$, where   $s_i=at$ and $s_{i+1}=bt$, for some $a,b\in   \Gamma_\epsilon$ and $t\in\Gamma^*$
3. $r_n\in F$

We say that $M$ recognizes $A$ if $A=\{w| M \ \ \text{accepts} \ \ w\}$
## Formal definition of computation 

Let $M = (Q, \Sigma,\delta, q_0,F)$ be a finite automaton and let $w=w_1w_2\dots w_n$ be a [[Automata and Languages Definitions#Strings and Languages#String|string]] where each $w_i$ is a member of the [[Automata and Languages Definitions#Alphabet|alphabet]] $\Sigma$. Then $M$ accepts $w$ of a sequence of states $r_0,\dots , r_n$ in $Q$ exists with three conditions:
1. $r_0 = q_0$
2. $\delta(r_i,w_{i+1}) = r_{i+1}, \ \ \text{for} \ \ i = 0,\dots,n-1$
3. $r_n\in F$

We say that $M$ recognizes $A$ if $A=\{w| M \ \ \text{accepts} \ \ w\}$

### CFG and PDA equivalence


![[Pasted image 20240421184047.png]]
# Regular Expressions

A regular expression is like an athematic expression expect that the value of a regular expression is a [[Automata and Languages Definitions#Language of an automata|language]] that a automata recognizes.

example: $$(a\cup b)^*$$

## Definition

We say that $R$ is a regular expression if $R$ is 

1. $a$ for some $a$ in the alphabet $\Sigma$ 
2. $\epsilon$
3. $Ø$
4. $R_1\cup R_2$ , where $R_1$ and $R_2$ are regular expressions
5. $R_1 \circ R_2$ , where $R_1$ and $R_2$ are regular expressions
6. $R_1^*$. where $R_1$ is a regular expressions

 In terms of items 1 and 2, the regular expressions $a$ and $\epsilon$ represents the languages $\{a\}$ and $\{\epsilon\}$, respectively. In item 3, the regular expression $Ø$ represents the empty language. I items 4, 5 and 6, the expressions by taking the union, concatenation and the star of the respective regular expressions.


# Context-Free Grammars

A grammar consists of a collection of *substitution rules*, also called *productions*. Each rule appears as a line in the grammar, comprising a symbol and a string separated by an arrow. The symbol is called a *variable*. The string that consists of variables and other symbols are called *terminals*.  The variable symbols are often in capital letters while terminals are in lowercase. One variable is designated the *start variable* it usually occurs on the left hand side of the topmost rule.

example of a context free grammar
$$\begin{align*}
A&\rightarrow0A1 \\
A &\rightarrow B \\
B &\rightarrow \#
\end{align*}$$
The start variable is $A$, the variables are $A$ and $B$ and the terminals $0,1$ and $\#$. The sequence of substitutions to obtain a string is called a *derivation*.

All strings generated by a derivation is called the *language of the grammar*. Any language that can be generated by some context-free grammar is called a *context-free language

## Formal Definition

A context-free grammar is a 4-tuple $(V,\Sigma,R,S)$ where.

### $V$ is a finite set called the variables
$V$ is a finite set; each element $v\in V$ is called _a nonterminal character_ or a _variable_. Each variable represents a different type of phrase or clause in the sentence. Variables are also sometimes called syntactic categories. Each variable defines a sub-language of the language defined by G.
### $\Sigma$ is a finite set, disjoint from $V$
$\Sigma$ is a finite set of *terminals*, disjoint from $V$, which make up the actual content of the sentence. The set of terminals is the alphabet of the language defined by the grammar G.
### $R$ is a finite set of rules, with each rule being a variable and a string of variables and terminals
$R$ is a finite [[Math definitions#Relations|relation]] in $V\times (V\cup \Sigma)^*$ operation. The members of *R* are called the *(rewrite)* rules or *production* of the grammar. (also commonly symbolized by a P)
### $S\in V$ is the start variable
$S$ is the start variable (or start symbol), used to represent the whole sentence (or program). It must be an element of $V$.

## Yields and Derives

If $u,v$ and $w$ are strings of variables and terminals and $A\rightarrow w$ is a rule of the grammar, we say that $uAv$ yields $uwv$, written $uAv\Rightarrow uwv$. We say that $u$ derives $v$, written $u\overset{*}{\Rightarrow}v$ if $u=v$ or if a sequence $u_1,u_2\dots u_k$ exists for $k\geq 0$  and $$u\Rightarrow u_1\Rightarrow u_2 \Rightarrow\dots \Rightarrow u_k \Rightarrow v$$
## Language of the Grammar 

The language of the grammar is defined as $L(G)=\{w\in\Sigma^*|S\overset{*}{\Rightarrow}w\}$.
In the example grammar above $V=\{A,B\}$, $\Sigma=\{0,1,\#\},S=A$ and $R$ are the substitution rules 
## Example of a creating a grammar

We want to create a grammar for the language $L=\{0^n1^n|n\geq 0\}\cup\{1^n0^n|n\geq0\}$ first we create the grammar for $\{0^n1^n|n\geq 0\}$ this is $$S_1\rightarrow0S_11|\epsilon$$and now we create the grammar for $\{1^n0^n|n\geq0\}$ which is $$S_2\rightarrow1S_20|\epsilon$$and now to combine them we add the substitution rule $S\rightarrow S_1|S_2$. The final grammar will then be 
$$\begin{align*}
S&\rightarrow S_1|S_2 \\
S_1&\rightarrow0S_11|\epsilon\\
S_2&\rightarrow1S_20|\epsilon \\
\end{align*}$$Converting a 

## Ambiguity of a Grammar

If a grammar generates the same string in several different ways, we say that the string is [[Automata and Languages Definitions#Yields and Derives|derived]] ambiguously in that grammar.  If a Grammar generates some string ambiguously, we say that the grammar is ambiguous.

Some grammars cant be created with unambiguous languages 

### Definition

A string $w$ is derived ambiguously in context-free grammar $G$ if it has two or more different leftmost derivations. Grammar $G$ is ambiguous if it generates some string ambiguously.


## Chomsky normal form 

Chomsky normal form is useful in giving algorithms for working with [[Automata and Languages Definitions#Context-Free Grammars|context-free grammars]]  

### Definition

A context-free grammar is in Chomsky normal form if every rule is in the form$$\begin{align*}
A&\rightarrow BC \\
A &\rightarrow a \\
\end{align*}$$Where $a$ is any [[Automata and Languages Definitions#$R$ is a finite set of rules, with each rule being a variable and a string of variables and terminals |terminal]] and  $A,B$ and $C$ are any [[Automata and Languages Definitions#$V$ is a finite set called the variables|variables]]---except that $A$ and $C$ may not be the start variable. In addition, we permit the rule $S\rightarrow \epsilon$ where $S$ is the start variable 

#### Example of a conversion of Chomsky normal form
$$\begin{align*}
S&\rightarrow ASA|aB \\
A &\rightarrow B| S \\
B &\rightarrow b| \epsilon
\end{align*}$$We start by creating a new start variable $S_0$ and a new rule 
$$\begin{align*}
S_0&\rightarrow S\\
S&\rightarrow ASA|aB \\
A &\rightarrow B| S \\
B &\rightarrow b| \epsilon
\end{align*}$$We now focus on the nullable variables meaning those with an $\epsilon$ rule meaning $B\rightarrow \epsilon$ and $A\rightarrow B$ which can lead to the [[Automata and Languages Definitions#Yields and Derives|derivation]] $A\rightarrow \epsilon$. $$\begin{align*}
S_0&\rightarrow S\\
S&\rightarrow ASA|aB|AS|SA|S|a \\
A &\rightarrow B| S \\
B &\rightarrow b
\end{align*}$$We can further remove any self references if they are unit rules meaning that $S\rightarrow S$ can be removed$$\begin{align*}
S_0&\rightarrow S\\
S&\rightarrow ASA|aB|AS|SA|a \\
A &\rightarrow B| S \\
B &\rightarrow b
\end{align*}$$Now a directed graph is drawn to figure out the relations between the different unit rules 

Now we replace the unit rules with the full rules of that specific variable$$\begin{align*}
S_0&\rightarrow ASA|aB|AS|SA|a\\
S&\rightarrow ASA|aB|AS|SA|a \\
A &\rightarrow b| ASA|aB|AS|SA|a \\
B &\rightarrow b
\end{align*}$$Now we assure that all the rules follow the form $$\begin{align*}
A&\rightarrow BC \\
A &\rightarrow a \\
\end{align*}$$This can be done by creating some new rules $A_1\rightarrow a$ and $U\rightarrow SA$$$\begin{align*}
S_0&\rightarrow AU|A_1B|AS|SA|a\\
S&\rightarrow AU|A_1B|AS|SA|a \\
A &\rightarrow b| AU|A_1B|AS|SA|a \\
U &\rightarrow SA\\
B &\rightarrow b\\
A_1 &\rightarrow a
\end{align*}$$
Now the grammar is in Chomsky normal form





