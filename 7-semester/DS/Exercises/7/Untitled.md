# Replication, Consistency, and Election Solutions

## 1. Consensus vs. Consistency
Consensus is the process of a group of nodes agreeing on a single value. Consistency is a property of the system's state across multiple replicas.
- **Implementation:** You can implement consistency by using **Total Order Broadcast** (which is equivalent to consensus) to order all update operations. If every replica manager receives and applies the exact same sequence of updates in the same order, the replicas stay synchronized.
- **Kind of Consistency:** This implements **Strong Consistency** (specifically **Linearizability** or **Sequential Consistency**), as every node transitions through the exact same states at the same logical time.

## 2. Non-Partition Tolerant Systems (CA)
According to the CAP theorem, a system cannot be simultaneously Consistent, Available, and Partition Tolerant.
- **Argument:** A system that chooses **Consistency and Availability (CA)** but is not **Partition Tolerant (P)** can still be considered a distributed system. It functions perfectly across multiple networked nodes under normal conditions. However, the definition of a distributed system includes the reality of network failures. A CA system simply "stops" or loses its properties during a partition. It is a distributed system that is not robust to network failures.

## 3. Interleavings (Slide 21)
- **Not Linearizable but Sequentially Consistent:** Imagine Process A writes `x=1` and finishes at time $t=10$. Process B starts a read at time $t=15$ and gets the old value `x=0`. 
  - This is **not linearizable** because the read started strictly after the write finished. 
  - It **is sequentially consistent** because we can logically "reorder" the events such that the read happened before the write without violating the program order of either individual process.
- **Not Sequentially Consistent:** Process A writes `x=1` then `x=2`. Process B reads `x=2` then `x=1`. This violates A's program order; no single global linear sequence can explain why B saw 2 before 1 if A wrote 1 then 2.
- **Minimum Clients for Non-Sequential Consistency:** **Two clients.** You need at least one process to perform multiple operations to establish a "program order" that another process can then observe in a contradictory way.

## 4. Passive Replication (Primary-Backup)
- **Message Complexity:** $O(n)$. For a write, the client sends 1 message to the primary, the primary sends $(n-1)$ messages to backups, receives $(n-1)$ ACKs, and sends 1 ACK back to the client. Total messages are $2n$.
- **Delay:** 2 round-trips ($Client \leftrightarrow Primary$ and $Primary \leftrightarrow Backups$).

## 5. Sacrificing Linearizability
"Sacrifice linearizability => offload reads to backups" means that instead of making every client go to the Primary for a "perfect" up-to-date value, you allow them to read from any Backup. 
- **Meaning:** This reduces the load on the Primary and improves read performance.
- **Consistency Result:** You end up with **Eventual Consistency** or **Causal Consistency**. Clients might read "stale" (old) data because the backup hasn't received the latest update from the primary yet.

## 6. Active Replication
- **Message Complexity:** Usually $O(n^2)$ or $O(n \log n)$ depending on the underlying Total Order Broadcast protocol (e.g., Paxos or Raft). Every node must communicate with a majority or every other node to agree on the sequence.
- **Delay:** High. You must wait for the consensus/Total Order protocol to reach agreement before the message can be delivered and executed.

## 7. Why use Active Replication?
Despite the high delay and complexity, Active Replication is used because:
1. **No Failover Delay:** Since all nodes are equal and active, there is no "primary" to elect if one node fails.
2. **Byzantine Fault Tolerance:** It is easier to handle nodes that send "garbage" data (Byzantine failures) by using a voting mechanism among all active replicas.
3. **Symmetry:** There is no bottleneck at a single primary node for execution.

## 8. Gossip Architecture Complexity/Delay
- **Message Complexity:** Update is $O(1)$ (send to one RM). The Gossip phase is background noise, typically $O(n)$ total per cycle.
- **Delay:** Very low for the client (immediate response from one RM), but **very high** for "global" consistency, as it takes time for the gossip to spread to all nodes.

## 9. Gossip: Read Operations
- **Outdated Replica:** If your first read was from RM1 (Vector Clock [1,0,0]) and your second read is from RM2 (Vector Clock [0,0,0]), you would see a "version" of the world that is older than what you already know.
- **Resolution:** The Front End (FE) keeps its own Vector Clock. It will refuse to read from a replica unless that replica's clock is $\ge$ the FE's clock.

## 10. Gossip: Write Operations
- **Apply all updates in log?** No, you only apply updates that haven't been executed yet.
- **Why keep updates forever?** You cannot delete updates from the log because you don't know if **all** other replicas have received them. If a replica crashes and comes back a week later, it needs those old updates to catch up. Deleting them would prevent new or recovering replicas from reaching a consistent state.

## 11. Chang-Roberts (Ring Election)
To overcome a crash after detection, the process that detects the crash (because its neighbor didn't respond) must modify the logical ring. It bypasses the crashed node and sends the election message to the **next** node in the sequence. This requires the nodes to have a list of all members, not just their immediate neighbor.

## 12. Bully Algorithm: Broken Safety
Safety is broken (meaning multiple leaders are elected) in these cases:
- **Too tight deadline:** A process assumes a higher-ID process is dead because it didn't respond fast enough, even though it's just slow. Both will then claim to be the leader.
- **Process ID reappears:** If a high-ID process recovers and starts an election while another election is finishing, the messages can cross in a way that leads both to believe they won.
- **Asynchronous System:** Since the Bully algorithm relies on timeouts to "prove" a node is dead, and asynchronous systems have no upper bound on delays, a timeout can never truly prove a node has crashed. This leads to "split-brain" scenarios where multiple leaders exist.