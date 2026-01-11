
# Math
## Serial Reliability (Dependent Components)
Used when the components are in a chain; if one fails, the whole system fails.

$$P(\text{Success}) = (1-p)^n$$
- $P(\text{Success})$: The probability the entire system remains functional.
- $p$: The probability of failure for a **single** component.
- $n$: The total number of components in the series.

## Parallel Reliability (Redundant Components)
Used when you have backups (redundancy); the system only fails if **every** component fails.
$$P(\text{Success}) = 1 - p^n$$
- $P(\text{Success})$: The probability the entire system remains functional.
- $p$: The probability of failure for a **single** component.
- $n$: The number of redundant components/backups.
- $p^n$: The mathematical probability that all $n$ components fail simultaneously.

## Amdahl's Law
Calculates the maximum theoretical speedup of a task when only a portion of it can be improved/parallelized.
$$Speedup = \frac{1}{(1-f) + \frac{f}{n}}$$
- **Speedup**: The ratio of the time taken by the old system vs. the new system.
- $f$: The **parallel fraction**—the percentage of the task that can benefit from more processors (e.g., 0.75 for 75%).
- $(1-f)$: The **sequential portion**—the part of the task that cannot be sped up and must be done by one processor.
- $n$: The number of processors or nodes added to the system.
# Lecture 1
A distributed system is one in which components located at networked computers
communicate and coordinate their actions only by passing messages
## Chapter 1: Characterization of Distributed Systems

### 1. Core Definition
A distributed system consists of hardware/software components on networked computers that communicate and coordinate **only by passing messages**.
- **The "Smart Pet Feeder" Lesson:** As noted in your slides, distribution means your local system can fail because of a remote computer you didn't even know existed.
### 2. Key Characteristics
- **Concurrency:** Multiple processes execute simultaneously. Coordination is required to manage shared resources.
- **No Global Clock:** There is no single "correct" time across the network; synchronization is a major challenge.
- **Independent Failures:** Components fail individually. A system must be able to handle a partial crash without failing entirely.
### 3. Design Challenges
- **Heterogeneity:** The system must work across different hardware, OS, and programming languages.
- **Scalability:** The system remains effective as the number of users and resources grows.
- **Transparency:** Making the "distributed" nature invisible to the user so the system feels like a single local entity.

---
## Chapter 2: System Models

### 1. Architectural Models
- **Client-Server:** The most common model; clients request, and passive servers respond.
- **Peer-to-Peer (P2P):** All nodes are equal and share the workload, offering better scalability.
- **Middleware:** A software layer (like Java RMI) that sits between the OS and the application to hide complexity.
- **3-Tier Architecture:** 1. **Presentation:** The User Interface.
    2. **Application Logic:** Where the actual processing happens.
    3. **Data Logic:** The database/storage layer.
### 2. Fundamental Models
Abstract ways to view system behavior:
- **Interaction Model:** - **Synchronous:** There are strict, known time limits for message delivery and processing.
    - **Asynchronous:** There are no time limits; messages can take any amount of time to arrive.
- **Failure Model:**
    - **Omission Failures:** A message is dropped or a process simply stops responding.
    - **Arbitrary (Byzantine) Failures:** The worst-case scenario where a process acts maliciously or sends "garbage" data.
- **Security Model:** Focuses on protecting the system via **Confidentiality** (secrets stay secret), **Integrity** (data isn't altered), and **Availability** (the system stays reachable).



# Lecture 2
## Fundamental Models of Distributed Systems

### 1. Model Definitions
A model is an abstraction that defines the rules of a system.
- **Message Passing:** Processes communicate solely by sending/receiving messages over channels. No shared memory exists.
- **Shared Memory:** Processes communicate by reading/writing to a common address space.
- **Interleaving Model:** We view concurrent executions as a linear sequence of events. Even if things happen at the same time, we model them as a specific "schedule" of steps.

### 2. Synchronous vs. Asynchronous Systems
This distinction is based on **Time**.

- **Synchronous System:** There are known, strict upper and lower bounds on:
	1. The time to execute a processing step.
	2. The time to deliver a message.
	3. The clock drift rate of each node.
- **Asynchronous System:** There are **no bounds** on how long a process takes to compute or how long a message takes to arrive. This is the model of the Internet.

---

### 3. Failure Models
Failures describe how a system departs from its expected behavior.

#### Node (Process) Failures
1. **Crash-Failure:** The process stops and does nothing else. It is "fail-silent."
2. **Omission Failure:** The process "skips" an action (e.g., fails to send a message or fails to process a received one).
3. **Arbitrary (Byzantine) Failure:** The worst case. The process can behave in any way, including sending conflicting or malicious data to different nodes.



#### Communication Failures
- **Omission:** Messages are dropped by the network.
- **Arbitrary:** Message contents are corrupted or "ghost" messages appear.
- **Timing:** (Only in synchronous systems) A message arrives, but it arrives outside the guaranteed time bound.

---

### 4. The Two Generals Problem
A classic problem proving that **agreement is impossible** over an unreliable communication channel.

- **The Scenario:** Two generals must agree to attack at the same time. If only one attacks, they lose. They communicate via messengers who can be captured (Omission failure).
- **The "Small Proof" (Induction on Message Chain):**
	- Suppose there is a protocol that requires $n$ messages to reach agreement.
	- Let $m_n$ be the last message. Since the channel is unreliable, the sender of $m_n$ never knows if it arrived.
	- If the protocol works even if $m_n$ is lost, then $m_n$ wasn't necessary.
	- If $m_n$ wasn't necessary, then we only needed $n-1$ messages.
	- By induction, we can reduce the required messages to zero, proving that no finite number of messages can ever guarantee agreement.



---

### 5. Common Knowledge & Muddy Children
Knowledge is the foundation of agreement. 
- **Individual Knowledge:** "I know $X$."
- **Common Knowledge:** "Everyone knows $X$, and everyone knows that everyone knows $X$ (to infinity)."

**The Muddy Children Puzzle:**
- $k$ children have mud on their faces. They can see everyone's face but their own.
- The father says: *"At least one of you has a muddy face."*
- This creates **Common Knowledge**. Before he spoke, every child might have known there was a muddy face (because they saw others), but they didn't know that *everyone else* knew it.
- **The Result:** Through rounds of silence, the children use the fact that "no one stepped forward" to deduce their own state. It proves that some tasks require a public announcement to become common knowledge before they can be solved.

---

### 6. Failure Detectors
In asynchronous systems, you cannot distinguish a "crashed" process from a "very slow" one. Failure detectors provide a "hint" about which processes have failed.

They are defined by two properties:
1. **Completeness:** Does the detector eventually suspect all crashed processes?
	- *Strong:* Every crashed process is suspected by **all** correct processes.
2. **Accuracy:** Does the detector avoid suspecting healthy processes?
	- *Strong:* No correct process is **ever** suspected.
	- *Eventual ($\diamond$):* The detector might make mistakes initially but eventually stops suspecting correct processes.

---

### 7. Performance Measures
How we quantify the efficiency of a distributed system.

- **Latency:** The time delay between the start of an operation and its completion.
- **Bandwidth:** The total amount of information that can be transmitted over the network in a given time.
- **Throughput:** The rate at which the system completes requests (e.g., requests per second).
- **Message Complexity:** The total number of messages sent to complete an algorithm.
- **Space/Time Complexity:** The amount of memory or the number of steps required per node.

**Service Levels:**
- **SLI (Service Level Indicator):** What we measure (e.g., "95th percentile latency").
- **SLO (Service Level Objective):** The target value (e.g., "Latency must be < 200ms").
- **SLA (Service Level Agreement):** The contract: SLO + consequences of failing to meet it.


# Lecture 3 
## Time and Global States in Distributed Systems

### 1. Counting Time Locally and Remotely
In a distributed system, time is a tool for ordering events and measuring intervals, but it is inherently problematic.
- **Local Time:** Each computer has a physical hardware clock (typically a quartz crystal oscillator) that counts oscillations and stores them in a register. The OS scales this to a software clock $C_i(t)$.
- **The Remote Problem:** There is no "global clock." Because messages take time to travel and network delays are unpredictable, we cannot perfectly synchronize clocks across different machines.
- **Clock Drift:** Hardware clocks naturally lose or gain time at different rates. Most quartz clocks have a drift rate of about $10^{-6}$ seconds per second (1 second every 11.6 days).
- **Clock Skew:** The instantaneous difference between the readings of any two clocks.

### 2. Dealing with Time Disagreement (Synchronization)
We synchronize clocks either to an external source (External Sync) or with each other (Internal Sync).

**Cristian's Algorithm (External)**
A client requests time from a centralized time server $S$.
$$T_{\text{new}} = T_{\text{server}} + \frac{T_{\text{round}}}{2}$$
- $T_{\text{new}}$: The time set on the client's clock.
- $T_{\text{server}}$: The timestamp returned by the server.
- $T_{\text{round}}$: The total round-trip time measured by the client.
- **Accuracy:** The error is $\pm (\frac{T_{\text{round}}}{2} - \text{min})$, where $\text{min}$ is the minimum possible message delay.

**The Berkeley Algorithm (Internal)**
A coordinator polls all "slaves" for their times, calculates a fault-tolerant average (discarding outliers), and sends back an offset (e.g., "slow down by 2s") to each node.

**Network Time Protocol (NTP)**
A hierarchical system (Strata) designed to synchronize the Internet. It uses statistical filtering to handle high network jitter.

---

### 3. The Happens-Before Relation ($\to$)
Defined by Leslie Lamport, this relation provides a partial ordering of events based on "causal" flow rather than physical time.

**Definition Rules:**
1. **Local Order:** If $a$ and $b$ are events in the same process, and $a$ comes before $b$, then $a \to b$.
2. **Message Flow:** If $a$ is the sending of a message and $b$ is the receipt of that same message, then $a \to b$.
3. **Transitivity:** If $a \to b$ and $b \to c$, then $a \to c$.

**Concurrent Events ($\parallel$):**
If $a \nrightarrow b$ and $b \nrightarrow a$, the events are **concurrent**. They have no causal relationship.


---

### 4. Logical Time and Clocks
Logical clocks assign a number $L(e)$ to an event $e$ such that if $a \to b$, then $L(a) < L(b)$.

**Lamport Logical Clocks**
Each process $P_i$ maintains a counter $L_i$.
- **Local Update:** Before each event, $L_i = L_i + 1$.
- **Sending:** Attach current $L_i$ to the message.
- **Receiving:** When receiving a message with timestamp $L_{\text{msg}}$, set $L_i = \max(L_i, L_{\text{msg}}) + 1$.
- **Variables:** - $L_i$: Local logical clock value.
	- $L_{\text{msg}}$: Timestamp attached to an incoming message.

**Vector Clocks**
Lamport clocks have a weakness: $L(a) < L(b)$ does **not** guarantee that $a \to b$. Vector clocks fix this by keeping a vector of size $N$ (number of processes).
- **Update Rule:** Each process increments its own entry in its vector $V_i[i]$ for every local event. When receiving a vector $V_{\text{msg}}$, the process updates its local vector to the element-wise maximum: $V_i[j] = \max(V_i[j], V_{\text{msg}}[j])$.
- **Causality Guarantee:** $V(a) < V(b) \iff a \to b$.

---

### 5. Timing Issues and Lamport Diagrams
- **Timing Issue Example:** In a distributed database, two users might update the same row. Without logical ordering, different replicas might apply the updates in different orders, leading to inconsistency.
- **Lamport Diagrams:** These visualize distributed executions using vertical lines for processes and slanted arrows for messages. They allow us to trace "causal paths" to see if one event could have influenced another.