


# lec 2

Variable X has domain(X), it can be discreet, continuious a binary and so forth

Given a set of variables, an assignment on the set of variables is a function from the variables into the domains of the variables. We write an assignment on {X1, X2,..., Xk} as {X1 = v1, X2 = v2,..., Xk = vk}, where vi is in domain(Xi). This assignment specifies that, for each i, variable Xi is assigned value vi. A variable can only be assigned one value in an assignment. A total assignment assigns a value to every variable.

If there are n variables, each with domain size d, there are d^n total assignments.

A unary constraint is a constraint on a single variable (e.g., B ≤ 3). A binary constraint is a constraint over a pair of variables (e.g., A ≤ B). In general, a k-ary constraint has a scope of size k. For example, A + B = C is a 3-ary (ternary) constraint. A constraint can be evaluated in an assignment that assigns a superset of the variables in the scope. The extra variables are ignored. For example, A ≤ B is true of the assignment {A = 3, B = 7,C = 5}. Assignment A satisfies constraint c if A assigns the variables in the scope of c and the condition of c evaluates to true for A restricted to the scope of c. Assignment A violates constraint c if A assigns the variables in the scope of c and the condition of c evaluates to false for that assignment. If an assignment A satisfies a constraint, then any assignment that is a superset of A also satisfies the constraint.


A constraint satisfaction problem (CSP) consists of:
• a set of variables
• a domain for each variable
• a set of constraints.
A solution is a total assignment that satisfies all of the constraints

• There is a node (drawn as a circle or an oval) for each variable.
• There is a node (drawn as a rectangle) for each constraint.
• For every constraint c, and for every variable X in the scope of c, there is
an arc X, c	. The constraint network is thus a bipartite graph, with the
two parts consisting of the variable nodes and the constraint nodes; each
arc goes from a variable node to a constraint node.
• There is also a dictionary dom with the variables as keys, where dom[X] is
a set of possible values for variable X. dom[X] is initially the domain of X

Suppose constraint c has scope {X,Y1,...,Yk}. Arc X, c	 is arc consistent
if, for each value x ∈ dom[X], there are values y1,..., yk where yi ∈ dom[Yi],
such that the assignment {X = x,Y1 = y1,...,Yk = yk} satisfies c. A network is
arc consistent if all its arcs are arc consistent.

we can do better by domain splitting, a form of case analysis that interleaves search and arc consistency. The idea is to split a problem into a number of disjoint cases and solve each case separately.