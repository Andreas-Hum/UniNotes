# Lecture 4 - Exercises: Solutions

### Exercise 1: Lamport Clock Pseudocode (API Style)
This pseudocode follows the logic from Slide 30, capturing local events, sending, and receiving.

**initialization:**
  $t := 0$

**on local event do:**
  $t := t + 1$

**on request to send message $m$ do:**
  $t := t + 1$
  send $(m, t)$ to destination

**on receiving $(m, t_{msg})$ do:**
  $t := \max(t, t_{msg}) + 1$
  deliver $m$ to application

---

### Exercise 2: Slide 9 Lamport Clocks & Issue Resolution
**Calculation:**
In Slide 9, Bob sends $m_1$ ("Meet at 7?") and Alice receives it, then sends $m_2$ ("No wait Meet at 9?").
- **Bob's send event ($e_1$):** $LT(e_1) = 1$. Message $m_1$ carries $t=1$.
- **Alice's receive event ($e_2$):** $LT(e_2) = \max(0, 1) + 1 = 2$.
- **Alice's send event ($e_3$):** $LT(e_3) = 2 + 1 = 3$. Message $m_2$ carries $t=3$.

**Resolution:**
Yes, Lamport clocks can fix the issue. If Carol receives $m_2$ ($t=3$) before $m_1$ ($t=1$), she can look at the timestamps and see that $m_1$ should have preceded $m_2$. By using a **Total Order Multicast** algorithm (Slide 32), Carol would buffer $m_2$ and wait to deliver $m_1$ first, ensuring she sees the messages in the correct causal order.

---

### Exercise 3: Proof of $a \to b \implies LT(a) < LT(b)$
**Proof by Induction:**
1. **Base Case (Local):** If $a$ and $b$ are in the same process and $a$ occurs before $b$, the algorithm increments $t$ for every event. Thus, $LT(b) \ge LT(a) + 1$, so $LT(a) < LT(b)$.
2. **Base Case (Message):** If $a$ is $send(m)$ and $b$ is $receive(m)$, the receiver sets $LT(b) = \max(t_{local}, LT(a)) + 1$. This guarantees $LT(b) > LT(a)$.
3. **Transitive Step:** If $a \to c$ and $c \to b$, by the inductive hypothesis $LT(a) < LT(c)$ and $LT(c) < LT(b)$. Therefore, $LT(a) < LT(b)$.

---

### Exercise 4: Causality of $e_1$ ($LT=5$) and $e_2$ ($LT=3$)
Because $LT(e_1) \not< LT(e_2)$, we know for certain that **$e_1$ did not happen before $e_2$** ($e_1 \nrightarrow e_2$). 
However, because Lamport clocks only provide a partial order, we **cannot** conclude that $e_2 \to e_1$. The events could be **concurrent** ($e_1 \parallel e_2$).

---

### Exercise 5: Broadcast Allowed Orders
**Slide 13 (FIFO Broadcast):**
Sender A sends $a$ then $b$. Sender B sends $c$. The only constraint is $a < b$.
- Allowed: $(a, b, c)$, $(a, c, b)$, $(c, a, b)$.

**Slide 14 (Causal Broadcast):**
User A sends $a$. User B receives $a$ and then sends $c$. User A receives $c$ and then sends $b$.
Causal chain: $a \to c \to b$.
- Allowed: Only $(a, c, b)$.

---

### Exercise 6: Causal $\implies$ FIFO Proof
FIFO ordering is a specific case of causal ordering. If $m_1$ and $m_2$ are broadcast by the same process $P_i$ and $m_1$ is sent before $m_2$, then by definition $m_1 \to m_2$ (Rule 1 of happens-before). 
Since Causal Broadcast guarantees that if $m_1 \to m_2$, $m_1$ is delivered before $m_2$, it inherently ensures $m_1$ is delivered before $m_2$ for messages from the same sender, satisfying FIFO.

---

### Exercise 7: Causal Broadcast Pseudocode (Vector Clocks)
This algorithm uses the delivery rules from Slide 39.

**initialization:**
  $V_{local} := [0, 0, \dots, 0]$
  $pending := \emptyset$

**on request to broadcast $m$:**
  $V_{local}[i] := V_{local}[i] + 1$
  $RB\_broadcast(m, V_{local})$

**on $RB\_deliver(m, V_m)$ from $P_j$:**
  $pending := pending \cup \{(m, V_m, j)\}$
  while exists $(m', V', k) \in pending$ such that:
    1. $V'[k] = V_{local}[k] + 1$
    2. $\forall x \neq k: V'[x] \le V_{local}[x]$
  do:
    deliver $m'$ to application
    $V_{local}[k] := V_{local}[k] + 1$
    $pending := pending \setminus \{(m', V', k)\}$

---

### Exercise 8: Uniform Reliable Broadcast (URB) & Majority
**Answer:** No.
Uniformity requires that if a process (even a faulty one) delivers a message, all correct processes must also deliver it. In an asynchronous system, if a majority is not assumed, a partition could result in a minority delivering the message and then crashing. The remaining "correct" processes would have no way to retrieve that message. Even with an eventually perfect failure detector ($\diamond P$), the system is essentially asynchronous before the Time of Rectification ($GST$), making it impossible to guarantee uniform agreement without a majority ($f < n/2$).

---

### Exercise 9: Causal Delivery Property Comparison
The property "If a process delivers $m_1$ and $m_2$, and $m_1 \to m_2$, then the process must deliver $m_1$ before $m_2$" is the standard definition of **Causal Delivery**. It ensures that the delivery order respects the causal history of the messages, preventing effects from being seen before their causes.

---

### Exercise 10: Vector Clock Calculation (Image 1)
**Traced Vector Clocks:**
- **User A:** $a(1,0,0) \to send$; $b(2,0,0) \to send$; $receive(g) \to (2,2,0)$; $c(3,2,0)$.
- **User B:** $receive(a) \to (1,0,0)$; $f(1,1,0)$; $g(1,2,0) \to send$.
- **User C:** $receive(b) \to (2,0,0)$; $d(2,0,1)$; $e(2,0,2)$.

**Message Contents:**
1. Message $b$ (A to C) contains $VC = (2,0,0)$.
2. Message $g$ (B to A) contains $VC = (1,2,0)$.

**Concurrent Events Examples:**
1. $f(1,1,0)$ and $b(2,0,0)$ (User B vs User A).
2. $g(1,2,0)$ and $d(2,0,1)$ (User B vs User C).