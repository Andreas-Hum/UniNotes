# Distributed Systems: Mutual Exclusion and Shared Memory Solutions

### Q1: Centralized Algorithm and Ordering
**Example of failure to satisfy ME3 (Happened-before ordering):**
The centralized algorithm handles requests based on the order they arrive at the server, not the order they were sent. Consider two processes $P_1$ and $P_2$. $P_1$ sends a request $r_1$ and then sends a message to $P_2$ saying "I've requested the token." $P_2$, upon receiving this, sends its own request $r_2$. By Lamport’s happens-before relation, $r_1 \to r_2$. However, due to network congestion, $r_2$ might arrive at the central server before $r_1$. The server will grant the token to $P_2$ first, violating the ordering property.

**Mechanism to fix this:**
The leader (server) could use **Lamport Timestamps**. Each client attaches a logical timestamp to its request. The leader would then queue requests and grant the token based on the lowest timestamp rather than the arrival time.

---

### Q2: Comparison of Mutual Exclusion Algorithms

| Algorithm | Client Delay | Sync. Delay | Bandwidth (per entry) | Major Problem |
| :--- | :--- | :--- | :--- | :--- |
| **Centralized** | 2 messages | 2 messages | 3 messages | Single point of failure & bottleneck at server. |
| **Token Ring** | 0 to $N$ msgs | 1 to $N-1$ msgs | Constant (token passing) | High bandwidth consumption even when no one wants entry. |
| **Maekawa** | 2 messages | 2 messages | $3\sqrt{N}$ messages | Prone to deadlock if not carefully managed. |
| **Ricart & Agrawala**| 2 messages | 1 message | $2(N-1)$ messages | High message overhead for large $N$. |

**Is Token Ring "more" fault tolerant?**
Not necessarily. In a **Leader-Token** system, if a client crashes, the server can just ignore it. If the server crashes, the system stops. In a **Token Ring**, if a single process crashes, the ring is broken and the token is lost. While a new ring can be formed and a new token generated, the recovery process is complex. In a **crash-recover** scenario, the Token Ring is highly sensitive because every time a node disappears or reappears, the logical ring must be completely restructured, which is often more disruptive than a central server simply reissuing a token.

---

### Q3: Synchronous Systems and Ordering
In a fully synchronous, single-threaded system where each process executes one step at a time and message delays are bounded, the **Happens-before order (ME3)** is technically less "critical" because physical time and logical time are closely aligned. However, it is still relevant if the application logic requires causality to be preserved. 
It can be mitigated without changing the algorithm by using **Physical Timestamps**. Since the system is synchronous, clocks can be synchronized with a known bound. By adding a small "wait time" equal to the maximum network delay ($D$) before processing a request, the server can ensure that no request sent later (physically) can be processed before one sent earlier.

---

### Q4: Maximum Throughput Formula
Throughput is the number of critical section entries per unit of time. If we assume the time spent inside the critical section is $E$ and the synchronization delay is $SD$, the maximum throughput ($T$) is:
$$T = \frac{1}{SD + E}$$
If $SD$ is the time between one process exiting and the next one being able to enter, the system can complete one full cycle every $SD + E$ units of time.

---

### Q5: Central Server with Client Crash Handling
**Adaptation:**
The server uses a **heartbeat-based failure detector** for the client currently holding the token. If the detector suspects the client has crashed, the server unilaterally "revokes" the token and grants it to the next process in the queue.
**Fault Tolerance:** The resultant system is **fault-tolerant for client failures** but remains vulnerable to server failures.
**Wrong Suspicion:** If a client holding the token is wrongly suspected (e.g., due to network delay), the server will issue a second token. This violates the **Safety (Mutual Exclusion)** property, as two processes could now enter the Critical Section simultaneously.

---

### Q6: Pseudocode Concepts

**Centralized:**
- **Requestor:** `send(REQUEST) to server; wait(GRANT); CS; send(RELEASE) to server;`
- **Server:** `if (busy) queue(request); else send(GRANT) to requestor;`

**Token Ring:**
- **Process:** `wait(TOKEN) from neighbor; if (wants_entry) { CS; } send(TOKEN) to next_neighbor;`

**Ricart-Agrawala:**
- **Requestor:** `timestamp = ++counter; multicast(REQUEST, timestamp); wait(N-1 ACKs); CS; reply_to_deferred_requests();`

**Maekawa:**
- **Requestor:** `multicast(REQUEST) to Voting Set; wait(ACKs from all in Set); CS; multicast(RELEASE) to Set;`

---

### Q7: Ricart-Agrawala Efficiency
**Why inefficient?**
If a process uses the CS many times in a row, it must multicast and wait for $N-1$ replies for *every single entry*, even if no one else is competing for it.
**Improvement:**
Adopt a **"Token-based"** or **"Lazy"** approach. After a process leaves the CS, it "holds" the permissions (token) it received. If it needs to enter again, it does so immediately without messaging. It only gives up the permissions when it receives a request from another process.
**Liveness (ME2):** Yes, this satisfies ME2 because a process is only allowed to "hold" the token until another process requests it, at which point it must eventually release it.

---

### Q8: Dekker’s Algorithm (2 Processes)
Each process $i$ has a `wants_to_enter[i]` flag and there is a shared `turn` variable.
1. Process $P_0$ sets `wants_to_enter[0] = true`.
2. It checks `wants_to_enter[1]`. If false, it enters the CS.
3. If `wants_to_enter[1]` is true, it checks `turn`.
4. If `turn == 1`, $P_0$ sets its flag to `false` (yielding) and waits until `turn == 0`.
5. Once `turn == 0`, it sets its flag back to `true` and attempts to enter.
6. Upon exit, it sets `turn = 1` and `wants_to_enter[0] = false`.

**Q8.1 (N Processes):**
In a fair version of Dekker's/Bakery for $N$ processes, if process $j$ is "faster" and requests multiple times, it is typically granted entrance **only once** before process $i$ if $i$ had already started its request. Specifically, if $j < i$ and $j$ is already in the queue, it will go before $i$. However, once $i$ has its "ticket" or "turn," $j$ cannot jump ahead of $i$ a second time. So, $j$ can be granted entrance **at most once** before $i$ is allowed in.

---

### Q9: TSO Memory Model Execution
**Possible Values:**
Under **Total Store Ordering (TSO)**, writes can be buffered. This means the read ($a := y$ or $b := x$) can happen before the write ($x := 1$ or $y := 1$) is visible to other processors.
- P1 reads $a$: Could be **0** or **1**.
- P2 reads $b$: Could be **0** or **1**.

**Can both enter CS?**
**Yes.** If both $a$ and $b$ read 0 (because the writes were still in the local buffers and not yet flushed to main memory), both processes will satisfy their `if` conditions and enter the Critical Section simultaneously. This is a classic example of why basic software mutex algorithms like Dekker's fail on modern CPUs without **Memory Barriers**.

**Replacing line 5 with `if x=1`:**
This would act as a local check. However, in TSO, P1 "sees" its own write ($x:=1$) immediately even if P2 doesn't. So $P_1$ would still enter the CS. Since the fundamental issue is $P_1$ not seeing $P_2$'s write and vice versa, changing the check on $x$ doesn't prevent both from entering.