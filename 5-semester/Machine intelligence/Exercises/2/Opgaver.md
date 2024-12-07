
# 1

![[Pasted image 20241203181617.png]]
Initialize To-do-arcs as a lexicographically ordered list (i.e., (a, b) would be before (a, c), both before (b, a) etc., if any of those exist). Furthermore, use to-do-arcs as a FIFO queue, i.e., always remove the element at the front and add new elements at the back.
## 1
The arcs $\langle A, A<B\rangle,\langle B, A<B\rangle,\langle C, B<C\rangle$ are arc consistent the arc $\langle B,B<C\rangle$ is not because $B=4$ does not have a value in the domain of C where this is true.

## 2
To make the whole network arc consistent we can follow the GAC algorithm we remember that we need it in a lexographical order in the todo and done 

$\text{Domains}(X)=\{D_A=\{1,2,3\},D_B=\{2,3,4\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle A, A<B\rangle,\langle B, A<B\rangle,\langle B, B<C\rangle \langle C,B<C\rangle\}$
$\text{Done}=\{\}$

### first iteration: 

Considering $\langle A, A<B\rangle$
$\text{Domains}(X)=\{D_A=\{1,2,3\},D_B=\{2,3,4\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle A, A<B\rangle,\langle B, A<B\rangle,\langle B, B<C\rangle \langle C,B<C\rangle\}$
$\text{Done}=\{\}$


$\forall. a \in D_A\exists b\in D_B \implies a<b$ has to be true in order for the arc to be arc consistent and the fact of the matter is that the largest element of the domain of $B$ is larger than the largest element in the domain of $A$ meaning $\text{Max}(D_A)<\text{Max}(D_B)$ is true meaning that there always exists a value in $D_B$ grater than $D_A$ 

the arc $\langle A, A<B\rangle$ is therefore arc consistent and it is added to Done

### Second iteration: 

Considering $\langle B, A<B\rangle$
$\text{Domains}(X)=\{D_A=\{1,2,3\},D_B=\{2,3,4\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle B, A<B\rangle, \langle B,B<C\rangle, \langle C, B<C\rangle\}$
$\text{Done}=\{\langle A, A<B\rangle\}$

$\forall. b \in D_B\exists a\in D_A \implies a<b$ has to be true in order for the arc to be arc consistent. This is true as $\text{Min}(D_A)<\text{Min}(D_B)$ is true. Meaning there always exists a value in $D_A$ less than the any value chosen in $D_B$

the arc $\langle B, A<B\rangle$ is therefore arc consistent and its added to Done
#### Second iteration: 

Considering $\langle B, B<C\rangle$
$\text{Domains}(X)=\{D_A=\{1,2,3\},D_B=\{2,3,4\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle B, B<C\rangle \langle C,B<C\rangle\}$
$\text{Done}=\{\langle A, A<B\rangle\,\langle B, A<B\rangle\}$

$\forall. b \in D_B\exists c\in D_c \implies b<c$ has to be true in order for the arc to be arc consistent. This proposition does not hold for $b=4$ as there exists no element in the domain of $C$ where this holds. This means the arc is not arc consistent and we need to remove $4$ from the domain of $B$

so the updated domain becomes $D'_B=\{b\in D_B| \exists c\in D_C. b<c \ \} = \{2,3\}$

Since we changed a domain we now have to readd the affected acts to the domain 
   $$
       \{\langle Z, c' \rangle \mid c' \neq c, X \in scope(c'), Z \neq X\}= \{\langle A, A<B\rangle\}
       $$

The arc $\langle A, A<B\rangle$ is added back to TODO it is not the constraint $B<C$ but $B\in \text{scope}(A<B)$ and the variable domain to consider is not B

with the domain reduced the arc $\langle B, B<C\rangle$ is now arc consistent


#### Third iteration

Considering $\langle A, A<B\rangle$
$\text{Domains}(X)=\{D_A=\{1,2,3\},D_B=\{2,3\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle A, A<B\rangle, \langle C,B<C\rangle\}$
$\text{Done}=\{\langle B, A<B\rangle\,\langle B, B<C\rangle\}$

$\forall. a \in D_A\exists b\in D_B \implies a<b$ has to be true in order for the arc to be arc consistent. This is not the case as the max element of $D_A$ is equal to the max element of $D_B$. We have to therefore update the domain  $D'_A=\{a\in D_A| \exists b\in D_B. a<b \ \} = \{1,2\}$ not the proposition from earlier holds. 

Since we changed a domain we now have to readdo the affected acr to the domain 
   $$
       \{\langle Z, c' \rangle \mid c' \neq c, X \in scope(c'), Z \neq X\}
       $$
however no arc exsists where this proposition is true. Therefore none are added.
the arc $\langle A, A<B\rangle$ is now arc consistent

#### Fourth iteration

Considering $\langle C,B<C\rangle$
$\text{Domains}(X)=\{D_A=\{1,2\},D_B=\{2,3\},D_C=\{3,4\}\}$
$\text{Todo}=\{\langle C,B<C\rangle\}$
$\text{Done}=\{\langle A, A<B\rangle,\langle B, A<B\rangle\,\langle B, B<C\rangle\}$

$\forall. c \in D_C\exists b\in D_B \implies b<c$ has to be true in order for the arc to be arc consistent. This is true as the proposition $\text{Max}(D_B)<\text{Max}(D_C)$ holds the arc $\langle C, B<C\rangle$ is therefore arc consistent  


#### Done 

final values 

$\text{Domains}(X)=\{D_A=\{1,2\},D_B=\{2,3\},D_C=\{3,4\}\}$
$\text{Todo}=\{\}$
$\text{Done}=\{\langle A, A<B\rangle,\langle B, A<B\rangle,\langle B, B<C\rangle,\langle C,B<C\rangle\}$

The constrain network is now arc consistent. 

# 2