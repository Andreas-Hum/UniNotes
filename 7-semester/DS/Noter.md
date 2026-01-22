
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

# Lecture 4 
## Group Communication and Multicast

### 1. Group Communication Overview
Group communication allows a process to send a single message to a group of processes without needing to know the individual identities of the members (**Space Uncoupling**).
- **Closed Group:** Only members can send to the group.
- **Open Group:** Non-members can send to the group.
- **Use Cases:** Replicated services (fault tolerance), service discovery, and event dissemination (e.g., social media updates).

### 2. Multicast Ordering Guarantees
Distributed systems often require specific delivery orders to maintain consistency.
- **FIFO Ordering:** If a process multicasts $m_1$ and then $m_2$, any process that delivers $m_2$ must have already delivered $m_1$. (Focuses on the **sender's** order).
- **Causal Ordering:** If a multicast $m_1$ "happens-before" a multicast $m_2$, then any process delivering $m_2$ must deliver $m_1$ first. (Focuses on **causal relationships**).
- **Total Ordering:** If any two correct processes deliver messages $m_1$ and $m_2$, they must deliver them in the same order. (Ensures **all nodes** see the same sequence).

---

### 3. Reliable Multicast Properties
To be considered "Reliable" ($R$-Multicast), the protocol must satisfy:
1. **Integrity:** A correct process delivers a message at most once.
2. **Validity:** If a correct process multicasts $m$, it will eventually deliver $m$ to itself.
3. **Agreement:** If any correct process delivers $m$, then all other correct processes in the group will eventually deliver $m$.

---

### 4. Vector Clocks in Causal Multicast
Vector clocks are used to track causal dependencies between messages. Each process $P_i$ maintains a vector $V_i$ of length $N$ (the number of processes).

**The Delivery Rule for Causal Ordering:**
When $P_j$ receives a message $m$ from $P_i$ with timestamp $V_m$, it only delivers $m$ when:
1. $V_m[i] = V_j[i] + 1$ 
   - *This ensures $m$ is the next message $P_j$ expects from $P_i$.*
2. $V_m[k] \leq V_j[k]$ for all $k \neq i$
   - *This ensures $P_j$ has already delivered all messages from other processes that $P_i$ had seen before sending $m$.*


---

### 5. Convergecast
Convergecast is the inverse of a broadcast; it is the process of collecting and aggregating information from all nodes in a network to a single "root" or initiator.

**Basic Algorithm:**
- Requires a **Spanning Tree** (often built via a preceding flooding/broadcast phase).
- **Leaf Nodes:** Send their data to their parent immediately.
- **Internal Nodes:** Wait until they have received a message from **all** their children, aggregate that data with their own, and then send the result to their parent.
- **Termination:** The algorithm completes when the root receives messages from all its immediate children.

**Performance:**
- **Message Complexity:** $n - 1$ messages (one per edge in the spanning tree, moving upward).
- **Time Complexity:** $O(h)$ where $h$ is the height of the tree.

# Lecture 5

## 1. Repetition: The Two Generals Problem
The Two Generals problem is the foundational "impossibility" result in distributed consensus.
- **Scenario:** Two generals on opposite hills must agree on a time to attack an enemy in the valley. They only communicate via messengers who might be captured (unreliable channel).
- **Result:** It is **impossible** to reach guaranteed agreement.
- **The Proof (Induction):**
	- Suppose a protocol exists that requires $n$ messages.
	- The sender of the $n$-th message can never be sure it arrived.
	- If the protocol must work even if the $n$-th message is lost, then the $n$-th message was unnecessary.
	- By repeating this logic, you reduce the required messages to zero, proving no protocol works.

---

## 2. The Consensus Problem
Consensus is the ability of a group of processes to agree on a single value. Formally, a consensus algorithm must satisfy three properties:

1.  **Termination:** Eventually, every correct process sets its decision variable (Liveness).
2.  **Agreement:** The decision value of all correct processes must be the same (Safety).
3.  **Integrity (Validity):** If all correct processes propose the same value $v$, then any correct process must decide $v$.

**The FLP Impossibility Result:**
In a **fully asynchronous** system, there is no deterministic consensus algorithm that is guaranteed to terminate if even one process can fail by crashing.

---

## 3. Paxos Algorithm
Paxos is the "gold standard" for consensus in asynchronous systems with crash failures. It prioritizes **Safety** (Agreement) over **Liveness** (it might not terminate if proposers conflict forever).

**Roles in Paxos:**
- **Proposers:** Suggest values to be agreed upon.
- **Acceptors:** Act as the "parliament" and vote to accept or reject proposals.
- **Learners:** Detect when a value has been accepted by a majority.

**The Two Phases:**
1.  **Phase 1 (Prepare/Promise):**
    - **Proposer** selects a unique proposal number $n$ and sends a `Prepare(n)` request to a majority of Acceptors.
    - **Acceptor** receives `Prepare(n)`. If $n$ is greater than any number it has seen, it responds with a `Promise` never to accept a lower $n$ and sends back the value of the highest-numbered proposal it has already accepted (if any).
2.  **Phase 2 (Accept/Accepted):**
    - If the **Proposer** receives a majority of `Promises`, it sends an `Accept(n, v)` request.
    - **The Value $v$:** If any Acceptor reported a previously accepted value, the Proposer **must** pick the value from the highest-numbered proposal. Otherwise, it picks its own value.
    - **Acceptor** receives `Accept(n, v)`. If it hasn't promised a higher number since Phase 1, it accepts the value and notifies Learners.

---

## 4. Raft and Leader Election
Raft is a more "understandable" alternative to Paxos, commonly used for log replication.

**Leader Election & Heartbeats:**
- Raft uses a **Leader-based** approach. All changes must go through the Leader.
- **Terms:** Time is divided into terms of arbitrary length. Each term begins with an election.
- **Heartbeats:** The Leader sends periodic "heartbeats" (Empty `AppendEntries` RPCs) to all followers to maintain its authority.
- **Election Trigger:** Followers have a **randomized timeout**. If they do not hear a heartbeat before the timeout expires, they assume the leader has failed, increment their term, and start a new election.

**Formally:** Consensus (Paxos/Raft) and **Total Order Broadcast** are equivalent; if you can solve one, you can solve the other.

---

## 5. Failure Detectors (Recap)
To get around the FLP impossibility, we use "Failure Detectors" to provide hints about crashes.
- **Synchronous Systems:** Use a timeout $T + D$ (where $D$ is the known max delay). If no "heartbeat" is seen, the node is definitely dead.
- **Asynchronous Systems:** We "guess" a delay $D$. If no heartbeat is seen, we **suspect** the node is dead. If it later responds, we stop suspecting and increase our guess for $D$.


# Lecture 6 

## Mutual Exclusion and Shared Memory

### 1. The Mutual Exclusion (Mutex) Problem
In a distributed system, mutual exclusion ensures that only one process can access a shared resource (the **Critical Section**) at any given time.

**Requirements for a Mutex Algorithm:**
- **Safety (Mutual Exclusion):** At most one process can be in the critical section at a time.
- **Liveness (Progress):** If no process is in the critical section and some processes want to enter, one must eventually be allowed to enter.
- **Fairness (Starvation Freedom):** A process that requests entry will eventually be allowed to enter (often implemented using "First-Come-First-Served" via logical clocks).

### 2. Shared Memory Model
Unlike the message-passing model where nodes send packets, the shared memory model assumes processes communicate by reading and writing to shared variables called **registers**. 

- **Asynchronous Shared Memory:** Processes run at different speeds, and there is no bound on how long a read or write operation takes.
- **Wait-freedom:** A property where every process can complete its operation in a finite number of its own steps, regardless of the speed or failure of other processes.

### 3. Types of Shared Registers
Registers are classified by their access patterns and the "strength" of their consistency.

**Access Patterns:**
- **SWMR (Single-Writer Multi-Reader):** Only one specific process can write; many can read.
- **MWMR (Multi-Writer Multi-Reader):** Multiple processes can both read and write.

**Consistency Levels:**
- **Safe Registers:** A read that does not overlap with a write returns the current value. If it overlaps, it can return *any* value in the register's range.
- **Regular Registers:** Similar to safe, but a read overlapping a write must return either the old value or the new value.
- **Atomic (Linearizable) Registers:** Every operation appears to take effect instantaneously at some point between its start and end. This is the strongest and most commonly assumed model.

**Special Operations (RMW - Read-Modify-Write):**
These allow for more complex atomic actions than simple reads/writes:
- **Test-and-Set:** Reads a value and sets it to 1 atomically.
- **Compare-and-Swap (CAS):** Updates a value only if it currently matches an expected "old" value.

### 4. Popular Mutex Algorithms

#### Shared Memory Algorithms
- **Peterson’s Algorithm:** A classic 2-process solution using flags and a "turn" variable to break ties.
- **Lamport’s Bakery Algorithm:** Designed for $N$ processes. Each process takes a "ticket" number. The process with the lowest ticket enters first. If tickets are equal, the process with the lower ID wins.

#### Message-Passing Algorithms
- **Centralized:** A coordinator grants permission. Simple but represents a single point of failure and a bottleneck.
- **Ricart-Agrawala:** A distributed algorithm that uses **Lamport Timestamps**. To enter, a process multicasts a request with a timestamp. Others reply only if they don't want to enter or have a higher timestamp (later request).
- **Token Ring:** Processes are organized in a logical ring. A "token" is passed around; you can only enter the critical section if you hold the token.

### 5. Synchronization and Time
**Synchronous vs. Asynchronous:** In synchronous systems, we can use timeouts to detect if a process holding a lock has crashed. In asynchronous systems, we cannot distinguish a crashed process from a slow one, making mutex much harder to solve without specific failure detectors.

**The Role of Logical Time:**
As seen in Section 14.4, **Lamport Clocks** are essential for Mutex. They provide a total ordering of requests. When two processes try to enter a critical section simultaneously, the "Happens-Before" relation (based on the logical timestamp) determines who was "first" in the eyes of the system, preventing deadlocks and ensuring fairness.



---

### Performance Measures
- **Bandwidth:** The number of messages required per entry/exit.
- **Client Delay:** The time a process waits to enter the critical section when no one else is in it.
- **Synchronization Delay:** The time between one process leaving the critical section and the next one entering.

# Lecture 7 

## Replication and High Availability

### 1. Goals of Replication
Replication is the process of maintaining multiple copies of data on different nodes.
- **Fault Tolerance:** The system continues to function even if some nodes fail.
- **Availability:** Data is accessible even during network partitions or node maintenance.
- **Performance:** Placing data geographically closer to users (Latency) and spreading the load across multiple servers (Throughput).

### 2. Reliability Math
**Dependent Components (Serial):**
If the system fails when any one component fails.
$$Uptime = (1-p)^N$$
- $Uptime$: Probability the system is functional.
- $p$: Probability of failure for a single node.
- $N$: Number of nodes.

**Independent Components (Redundant):**
The system only fails if **all** components fail simultaneously.
$$Uptime = 1 - p^N$$
- $p^N$: The probability that all $N$ nodes are down at the same time.



### 3. Replication Models
- **Passive Replication (Primary-Backup):** One "Primary" RM handles all requests and propagates updates to "Backups." If the Primary fails, a Backup is elected as the new Primary.
- **Active Replication:** Every RM is an equal peer. Requests are multicasted to all RMs using **Total Order Broadcast** to ensure every replica processes the same operations in the same order.

---

## Gossip Architecture
Gossip is a framework for implementing highly available services with **Eventual Consistency**.

### 1. The Components
- **Front Ends (FE):** Handle user requests and communicate with Replica Managers.
- **Replica Managers (RM):** Store data and exchange "gossip" messages to stay synchronized.



### 2. Operation Flow
1. **Query/Update:** The FE sends a request to any available RM.
2. **Gossip:** RMs periodically send messages to one another containing updates they haven't seen yet.
3. **Eventual Consistency:** While different RMs might have different data at a specific moment, they will eventually converge to the same state if updates stop.

---

## Distributed Transactions
A transaction is a sequence of operations that must be treated as a single unit (Atomic).

### 1. ACID Properties
- **Atomicity:** All or nothing.
- **Consistency:** Transitions the database from one valid state to another.
- **Isolation:** Transactions do not interfere with each other.
- **Durability:** Once committed, changes are permanent.

### 2. Two-Phase Commit (2PC)
A protocol used to ensure all participants in a distributed transaction either all commit or all abort.
- **Phase 1 (Voting):** The coordinator asks all participants if they are ready to commit. Participants reply "Yes" or "No."
- **Phase 2 (Completion):** If **everyone** said "Yes," the coordinator sends a "Commit" message. If **anyone** said "No" or timed out, the coordinator sends an "Abort" message.



---

## Leader Election
Leader election is the process of designating a single process as the coordinator for a specific task.

### 1. The Bully Algorithm
Assumes every process has a unique ID and can communicate with every other process.
- **Process:** A process $P$ notices the leader is down. It sends an "Election" message to all processes with higher IDs.
- **Response:** If no one higher responds, $P$ becomes the leader and "bullies" everyone else into subjection by announcing its victory. If a higher process responds, $P$ waits for that process to finish the election.


### 2. Ring-Based Election (Chang-Roberts)
Processes are organized in a logical ring.
- **Process:** A process $P$ initiates an election by sending its ID to its neighbor.
- **Flow:** Each neighbor compares the received ID with its own, forwarding the larger one.
- **Victory:** When a process receives its own ID back, it knows it has the highest ID in the ring and announces itself as the leader.

### 3. Election Properties
- **Safety:** At most one process is in the "elected" state at any time.
- **Liveness:** An election eventually terminates and a leader is chosen.

# lecture 8

## Google Infrastructure: GFS, Chubby, and Bigtable

### 1. Google Cluster Architecture & Design Philosophy

#### Core Principles
* **Commodity Hardware:** The system is built using thousands of inexpensive, commodity-class PCs rather than high-end, expensive servers. The goal is to maximize the **price-performance ratio**.
* **Fault-Tolerant Software:** Because hardware failure is considered the "norm" at this scale, the software layer is responsible for monitoring, error detection, and automatic recovery.
* **Extensive Parallelization:** Applications (like Web Search) are designed to be partitioned across many processors and clusters to handle high throughput.

#### Physical Organization
* **Racks:** 40–80 servers connected via an Ethernet switch.
* **Clusters:** Groups of 30 or more racks (thousands of machines) managed as a single unit.
* **Data Centers:** Globally distributed facilities that house multiple clusters for redundancy and low-latency access.

---

### 2. The Google File System (GFS)

GFS is a scalable distributed file system designed for large-scale, data-intensive applications.



#### Key Design Assumptions
* **Large Files:** Files are typically multi-GB; managing billions of KB-sized files is considered inefficient.
* **Append-Dominant Workload:** Most files are mutated by appending new data rather than overwriting existing data.
* **Throughput over Latency:** High sustained bandwidth for bulk data processing is prioritized over the low latency of individual reads/writes.

#### Architecture
* **Single Master:** Manages all metadata (namespace, access control, mapping from files to chunks).
* **Chunkservers:** Store the actual data. Files are divided into fixed-size **Chunks (64 MB)**.
* **Replication:** Each chunk is replicated (default 3x) across different chunkservers and racks to ensure availability.

#### The Record Append Operation
* GFS provides an **atomic record append** operation. 
* Multiple clients can append to the same file concurrently. 
* GFS guarantees that data is written **atomically at least once**, though the specific offset is chosen by the system, not the client.

---

### 3. Chubby Lock Service

Chubby provides a "coarse-grained" lock service and storage for small files.

#### Functions and Features
* **Distributed Locking:** Used to synchronize activities and prevent multiple nodes from performing the same task (e.g., electing a master).
* **Small Data Storage:** Used to store configuration information and metadata (e.g., the location of the GFS master).
* **High Availability:** Uses the **Paxos consensus algorithm** across a "cell" of replicas (typically 5) to ensure the service remains available even if some nodes fail.

#### Usage in Infrastructure
* **GFS:** Uses Chubby to elect the master and store its location.
* **Bigtable:** Uses Chubby to discover tablet servers and track the schema.

---

### 4. Bigtable

Bigtable is a distributed, structured storage system designed to scale to petabytes of data across thousands of servers.

#### Data Model
Bigtable is a **sparse, distributed, multi-dimensional sorted map**. Data is indexed by:
1. **Row Key:** An arbitrary string; data is sorted lexicographically by row.
2. **Column Key:** Grouped into **Column Families** (the unit of access control and memory management).
3. **Timestamp:** 64-bit integers used to store multiple versions of the same data (e.g., historical versions of a web page).

#### Implementation & Storage
* **Tablets:** Tables are split horizontally into row ranges called **Tablets** (typically 100-200 MB each).
* **Tablet Servers:** Each server manages a set of tablets and handles read/write requests.
* **Dependencies:** Bigtable uses **GFS** to store its data files (SSTables) and logs, and **Chubby** for coordination and metadata management.

---

### 5. Summary of System Interdependence

Google's services are layered to provide a cohesive infrastructure:
* **Bigtable** sits on top of **GFS** (for storage) and **Chubby** (for coordination).
* **MapReduce** is used to process data stored in GFS or Bigtable.
* **Chubby** serves as the root of trust for all system-wide coordination and master elections.



# lecture 9

## Peer-to-Peer Systems and Overlay Networks

### 1. Overlay Networks Overview
An **Overlay Network** is a virtual network consisting of nodes and virtual links that sits on top of an existing network (like the Internet). 
- **Network Virtualization:** It allows the construction of multiple virtual networks over a single physical infrastructure, each tailored for specific applications (e.g., Skype vs. BitTorrent).
- **Addressing and Routing:** Overlays use their own application-level addressing (e.g., GUIDs) and routing algorithms, which are independent of the underlying IP routing.
- **Decoupling:** By building logic into the application layer, developers can implement features like multicast, enhanced security, or specialized search without modifying the Internet's core protocols.

---

### 2. Peer-to-Peer (P2P) Fundamentals
The P2P paradigm shifts distributed systems from centralized servers to a model where all participants (peers) contribute resources.
- **Decentralization:** There is no requirement for separately managed central servers; every node has the same functional capabilities.
- **Self-Organization:** The system automatically handles nodes joining and leaving (**Churn**) and dynamically balances storage and processing loads.
- **Resource Edge:** P2P exploits resources available at the "edges" of the Internet—storage, CPU cycles, and content—provided by ordinary user machines.
- **Scalability:** As the number of users increases, the total resources available to the system (bandwidth and storage) also grow.

---

### 3. First Generation: Napster
Napster was the pioneer of P2P file sharing, though it was not "purely" decentralized.
- **Hybrid Architecture:** It utilized **centralized index servers** to maintain a directory of files and the IP addresses of the peers hosting them.
- **Operation:** 1. A peer registers its files with the central server.
    2. A client queries the server to find a specific file.
    3. The server returns a list of peer addresses.
    4. The client downloads the file directly from another peer via **Direct P2P Transfer**.
- **Legacy:** It proved the feasibility of large-scale sharing but demonstrated the vulnerability of centralized components (legal and technical).

---

### 4. Second Generation: Gnutella (Unstructured P2P)
Gnutella was designed to be fully decentralized, removing the need for a central index.
- **Unstructured Overlay:** There is no strict mapping between data location and the network topology; the connections between peers are essentially random.
- **Flooding Mechanism:** To find a file, a node sends a query to its neighbors, who "flood" the request to their own neighbors up to a certain **Time-to-Live (TTL)**.
- **Pros/Cons:** It is highly resilient and provides anonymity, but it is inefficient. Flooding creates massive network traffic and does not guarantee that a file will be found even if it exists.

---

### 5. Third Generation: Chord (Structured P2P)
Chord represents a **Structured Overlay** that uses a **Distributed Hash Table (DHT)** to provide deterministic routing.
- **GUIDs:** Nodes and data objects are assigned 160-bit **Globally Unique Identifiers (GUIDs)** using a hash function like SHA-1.
- **Identifier Circle:** Identifiers are arranged in a logical ring (modulo $2^m$). A data key $k$ is stored at the first node whose ID is equal to or follows $k$ (**Successor**).
- **Finger Tables:** Each node $n$ maintains a routing table (finger table) containing the IDs of nodes halfway around the ring, a quarter way, etc.
- **Performance:** Chord can locate any data object in **$O(\log N)$** hops, making it highly efficient for massive global systems.
- **Consistency:** When a node joins or leaves, only a small fraction of keys need to be moved to maintain the structure.


# Lecture 10

## IoT Routing: Directed Diffusion, DSR, and AODV

### 1. Introduction to IoT and WSN Routing
Routing in the Internet of Things (IoT) and Wireless Sensor Networks (WSN) differs from traditional IP routing due to severe resource constraints (power, memory, and processing).
- **Ubiquitous Computing:** Integration of computation into the environment requires seamless, often ad-hoc, networking.
- **Resource Constraints:** Protocols must minimize message overhead to preserve battery life and handle frequent topology changes (Churn).
- **Multi-hop Communication:** Devices often cannot reach a gateway directly and must rely on intermediate nodes to relay data.

---

### 2. Directed Diffusion (Data-Centric Routing)
Directed Diffusion is a reactive, data-centric routing paradigm where nodes are addressed by the data they provide rather than their IP addresses.

- **Interest Propagation:** A "sink" (data requester) broadcasts an **Interest** (e.g., "send temperature data from area X") to its neighbors.
- **Gradients:** As the Interest spreads through the network, nodes set up **Gradients**—state information that points back toward the neighbor who sent the Interest.
- **Data Delivery:** When a source has data matching an Interest, it sends the data along the gradient paths.
- **Reinforcement:** The sink "reinforces" the best-performing path (e.g., the one with the lowest latency), causing that path to be used for higher-rate data transmission.



---

### 3. Dynamic Source Routing (DSR)
DSR is a reactive (on-demand) routing protocol designed for multi-hop wireless ad hoc networks.

- **Source Routing:** The sender determines the **complete sequence of nodes** through which a packet must pass. This entire path is stored in the packet header.
- **Route Discovery:**
    1. A node broadcasts a **Route Request (RREQ)** if it doesn't have a route in its cache.
    2. Each intermediate node adds its own ID to the RREQ and rebroadcasts it.
    3. The destination sends a **Route Reply (RREP)** back to the source containing the full accumulated path.
- **Route Cache:** Nodes store previously discovered routes to reduce the frequency of new RREQ broadcasts.
- **No Periodic Updates:** Unlike proactive protocols, DSR does not send "Hello" messages or periodic table updates, saving significant energy.

---

### 4. Ad Hoc On-Demand Distance Vector (AODV)
AODV is a reactive protocol that combines the on-demand mechanism of DSR with the hop-by-hop routing style of distance vector protocols.

- **Hop-by-Hop Routing:** Unlike DSR, packets in AODV do not carry the full path. Instead, each node only knows the **next hop** to a destination.
- **Sequence Numbers:** AODV uses destination sequence numbers to ensure that routes are loop-free and that nodes always choose the most recent (freshest) route.
- **Routing Phases:**
    - **Route Request (RREQ):** Broadcasted when a node needs a route.
    - **Route Reply (RREP):** Unicast back to the source to establish the forward path.
    - **Route Error (RERR):** Sent to notify other nodes when a link in an active route breaks.
- **Hard State vs. Soft State:** Routing table entries are purged after a timeout (active_route_timeout) if they are not used, keeping the tables lean.



---

### 5. Tree-Based Routing
Tree topology is a hierarchical structure where a "root" node connects to multiple levels of "child" nodes.

- **Structure:** Often used in WSNs where a Sink/Gateway acts as the root. Data typically flows from the leaves (sensors) up to the root.
- **Address Assignment:** In many IoT trees (like ZigBee), addresses are assigned hierarchically, allowing a node to determine if a destination is in its subtree simply by looking at the address range.
- **Strengths:** Simple to implement and requires very little memory for routing tables.
- **Weaknesses:** Vulnerable to "single points of failure"—if a parent node fails, its entire subtree is disconnected from the root.



# Lecture 11

## Blockchain and Cryptographic Fundamentals

### 1. Cryptographic Building Blocks
Blockchains rely on several key cryptographic primitives to ensure data integrity, security, and authentication.

- **Cryptographic Hash Functions:** A function $H(x)$ that maps an input of any size to a fixed-length string. 
    - **Pre-image Resistance:** Given $h$, it is hard to find $x$ such that $H(x) = h$.
    - **Collision Resistance:** It is computationally infeasible to find two different inputs $x$ and $y$ such that $H(x) = H(y)$.
- **Hash Pointers:** A pointer to where data is stored along with a cryptographic hash of that data. This allows for the creation of tamper-evident data structures.
- **Digital Signatures:** Uses asymmetric cryptography (public/private keys). A user signs a transaction with their **private key**, and anyone can verify it using the user's **public key**, ensuring non-repudiation.

---

### 2. Blockchain Structure
A blockchain is a distributed ledger consisting of a sequence of blocks linked by hash pointers.

- **Block Anatomy:** Each block contains a header (including the hash of the previous block, a timestamp, and a nonce) and a list of transactions.
- **Merkle Trees:** Transactions within a block are organized into a binary tree of hashes. The **Merkle Root** (the top hash) is stored in the block header.
    - **Efficiency:** This allows a node to verify if a specific transaction is included in a block without downloading the entire block ($O(\log n)$ complexity).
- **Immutability:** Because each block contains the hash of the previous one, changing a single bit in an old block would require recomputing every subsequent block in the chain.



---

### 3. Consensus and Proof of Work (PoW)
Consensus protocols allow a distributed network of untrusted participants to agree on a single version of the ledger.

- **The Double-Spending Problem:** The primary challenge in digital cash is preventing a user from spending the same token twice. Bitcoin solves this via a public ledger and consensus.
- **Proof of Work (Mining):** To add a block, a "miner" must find a **nonce** such that the hash of the block header starts with a specific number of zero bits (the **Difficulty Target**).
- **The Longest Chain Rule:** Nodes always consider the longest chain (the one with the most cumulative proof of work) as the valid version of history.
- **51% Attack:** If a single entity controls more than 50% of the network's hashing power, they could theoretically roll back transactions or prevent new ones from being confirmed.



---

### 4. Smart Contracts and Ethereum
While Bitcoin is primarily for value transfer, platforms like Ethereum introduced programmable transactions.

- **Smart Contracts:** Self-executing pieces of code stored on the blockchain. They automatically enforce the terms of an agreement when predefined conditions are met.
- **Ethereum Virtual Machine (EVM):** The runtime environment that executes smart contract code across the global network of nodes.
- **Gas:** To prevent infinite loops and resource abuse, every operation in a smart contract costs "Gas," paid for by the user initiating the transaction.

---

### 5. Development with Solidity and Remix
Solidity is the primary high-level language used for writing smart contracts on Ethereum-compatible blockchains.

- **Contract Structure:** Includes state variables, functions, and modifiers.
- **Remix IDE:** A browser-based integrated development environment (IDE) used for writing, compiling, and deploying Solidity contracts.
- **Key Concepts:**
    - **Visibility:** `public`, `private`, `internal`, `external`.
    - **State Mutability:** `view` (reads state but doesn't change it), `pure` (doesn't read or change state).

---

### 6. The "Blockchain Test"
Blockchains are not always the optimal solution. A system typically benefits from a blockchain only if:
1. There are **multiple parties** involved.
2. Establishing **trust** between parties is an issue.
3. A **tamper-proof**, permanent record is critical.
4. There is a need to manage a **finite resource** (preventing double-counting).
5. The ecosystem benefits from **transparency**.



# Lecture 12

## Distributed Algorithms

### 1. Fundamental Concepts and UIDs
In distributed systems, algorithms often depend on the ability of nodes to distinguish themselves from one another.
- **Symmetry Breaking:** Many problems (like leader election) cannot be solved in an "anonymous" network where all nodes are identical.
- **Unique Identifiers (UIDs):** Nodes are typically assigned UIDs (e.g., from a large namespace) which are used to break symmetry.
- **Complexity Measures:**
    - **Message Complexity:** Total number of messages sent.
    - **Time Complexity:** Number of rounds (synchronous) or time until the last event (asynchronous).

---

### 2. Leader Election
Leader election is the process of designating a single node as the coordinator for some task.
- **Ring-Based Election:** In a logical ring, nodes pass their UIDs. The node with the highest (or lowest) UID becomes the leader.
- **LCR Algorithm:** A node sends its UID clockwise. If it receives a UID greater than its own, it discards it. If it receives its own UID back, it knows it is the highest and declares itself the leader.
- **Symmetry Breaking with Randomization:** In anonymous networks without UIDs, nodes can pick random numbers to act as temporary IDs to break symmetry.

---

### 3. Spanning Tree Construction
A spanning tree is a subgraph that includes all nodes of the original graph and has no cycles. It is essential for efficient broadcasting and convergecast.

**Breadth-First Search (BFS) Trees:**
- **Synchronous Construction:** The root sends a "discovery" message in round 1. In each subsequent round, newly discovered nodes send the message to their neighbors.
- **Asynchronous Construction:** More complex because messages can arrive out of order.
    - **Strategy:** Nodes keep track of their distance from the root. If a node receives a "shorter" path from a neighbor, it updates its parent and propagates the new distance to its children.
    - **Anomaly:** Without distance tracking, asynchronous paths can become much longer than the shortest path.



---

### 4. Graph Coloring and Maximal Independent Set (MIS)
These algorithms are used for resource allocation and scheduling.

**Graph Coloring:**
- **Goal:** Assign a "color" to each node such that no two adjacent nodes have the same color.
- **Algorithm:** Nodes use their UIDs to decide colors. A simple approach is for each node to pick a color different from its neighbors with higher UIDs.

**Maximal Independent Set (MIS):**
- **Definition:** A subset of nodes such that:
    1. **Independence:** No two nodes in the set are adjacent.
    2. **Maximality:** No additional node can be added to the set without violating independence (every node not in the MIS is adjacent to at least one node in the MIS).
- **Use Case:** Electing a set of "cluster heads" to manage local groups of nodes.

---

### 5. Randomized Algorithms (Luby’s Algorithm)
When deterministic algorithms are too slow or impossible, randomization provides a powerful alternative.

**Luby’s MIS Algorithm (Randomized):**
1. Each node $u$ picks a random value $r(u)$.
2. If $r(u)$ is strictly greater than all its neighbors' values, $u$ enters the MIS.
3. If $u$ enters the MIS, it notifies its neighbors; both $u$ and its neighbors are removed from the graph.
4. Repeat until the graph is empty.
- **Performance:** This typically converges in $O(\log n)$ rounds with high probability.

---

### 6. Shortest Paths (Optional)
Finding the shortest path from a source to all other nodes in a distributed environment.
- **Distributed Bellman-Ford:** Each node maintains a table of distances to the source. It periodically updates its distance based on the minimum distance reported by its neighbors plus the edge cost.
- **Self-Stabilization:** These algorithms are often designed to be self-stabilizing, meaning they can recover from arbitrary state changes (like edge failures or cost changes) and converge to the correct shortest path.