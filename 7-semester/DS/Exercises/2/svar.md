# Distributed Systems: Exercises Solutions

## Exercise 1: Fail-Recovery vs. Fail-Silent Models
**Question:** Under which assumptions are the fail-recovery and fail-silent models similar?

**Answer:** The **fail-silent** model assumes a process crashes and remains in that state indefinitely. The **fail-recovery** model assumes a process can crash and later resume execution, often losing its volatile state but retaining data in stable storage.
These models are similar under the following assumptions:
* **Permanent Crashes:** If we assume that in the fail-recovery model, a process that crashes never actually recovers (or the protocol treats it as "dead" forever), it behaves identically to a fail-silent process.
* **Indistinguishable Omissions:** In both models, any process can commit **omission faults** (dropping messages). A crashed process that is currently down is indistinguishable from a "correct" process that is simply omitting all its send and receive actions.
* **Infinite Time Bounds:** In asynchronous systems, because there is no bound on how long a process can be "silent," a process that has crashed and is waiting to recover is indistinguishable from one that has crashed permanently.

---

## Exercise 2: Implementing a Stubborn Link
**Question:** Show how to make a stubborn point-to-point link using a fair-loss link API.

**Answer:**
A **fair-loss link** guarantees that if a message is sent infinitely often, it will be delivered infinitely often. A **stubborn link** ensures that a message sent once is repeatedly transmitted until delivered.

**Algorithm:**
1. **Sender-side:**
   - Upon a request to `send(m)`, the process starts a timer.
   - Every time the timer expires, it calls the `fair-loss-send(m)` API.
   - This continues indefinitely (or until an acknowledgment is received in higher-level protocols).
2. **Receiver-side:**
   - Upon `fair-loss-receive(m)`, the receiver checks if $m$ has already been delivered.
   - If not, it delivers $m$ and stores its identifier to filter future duplicates.

---

## Exercise 3: Perfect Failure Detector in Synchronous Systems
**Question:** Describe the implementation of a perfect failure detector ($P$).

**Answer:**
In a **synchronous system**, we have a known upper bound $L$ for message latency and $D$ for processing time. A perfect failure detector ($P$) satisfies **Strong Completeness** (eventually detects all crashes) and **Strong Accuracy** (never suspects a correct process).

**Implementation:**
* **Heartbeat Mechanism:** Every process $p$ sends a "heartbeat" message to all other processes every $T$ seconds.
* **Timeout:** A process $q$ suspects $p$ has crashed if it does not receive a heartbeat within a timeout period of $T + L + D$.
* **Why it's Perfect:** Because the bounds $L$ and $D$ are guaranteed, any message arriving after the timeout implies the sender has truly crashed or the system's synchronous assumptions were violated.

---

## Exercise 4: Synchronous Computation Assumption
**Question:** Does "no request ever takes more than 1 week to be processed" satisfy the synchronous-computation assumption?

**Answer:**
**Yes.** The synchronous-computation assumption requires that there is a **known, finite upper bound** on the time taken to execute a step or process a request. While "one week" is practically very slow, theoretically, as long as the bound is constant and known, it fulfills the requirement for a synchronous model.

---

## Exercise 5: Perfect Failure Detector for Byzantine Faults
**Question:** Is it possible to design a perfect failure detector for Byzantine faults?

**Answer:**
**No.** A perfect failure detector must have **Strong Accuracy**, meaning it never suspects a correct process. In a Byzantine model, a faulty process can behave perfectly (sending correct heartbeats) while internally lying or sending malicious data to other nodes. Since a "correct" node and a "malicious but currently silent" Byzantine node are indistinguishable by looking at timing alone, you cannot perfectly detect all Byzantine faults with a standard failure detector.

---

## Exercise 6: SLA and Uptime Calculations
**Question:** Calculate downtime for 90%, 99%, and 99.9% uptime. How many crashes for 99% SLA?

**Answer:**
Using a standard 30-day billing month (43,200 minutes):

| SLA % | Allowed Downtime (Monthly) | Calculation |
| :--- | :--- | :--- |
| **90%** | **4,320 mins** (72 hours) | $43200 \times 0.10$ |
| **99%** | **432 mins** (7.2 hours) | $43200 \times 0.01$ |
| **99.9%** | **43.2 mins** | $43200 \times 0.001$ |

**For a 99% SLA:**
* **Expected Crashes:** If a typical recovery takes 30 minutes, you could tolerate **~14 crashes** per month ($432 / 30$).
* **Resolution Speed:** All issues must be resolved within a cumulative total of **7 hours and 12 minutes** to avoid violating the SLA.

---

## Exercise 7: MS Azure SLA for VMs
**Question:** How much time does Azure get to fix issues, and what is their sampling frequency?

**Answer:**
* **Fix Time:** Azure SLAs do not guarantee a "time to fix." Instead, they guarantee a "Monthly Uptime Percentage" (e.g., 99.9% to 99.99%). If they fail, they provide **Service Credits** (10% to 100% of the bill) rather than guaranteeing a repair window.
* **Sampling Frequency:** Azure typically monitors "Virtual Machine Connectivity" at **1-minute intervals**. Downtime is calculated based on the number of minutes the instance was unreachable.

---

## Exercise 8: Network Graph Analysis
**Question:** What minimum percent of messages from node 1 to node 2 go through node 6?

**Answer:**
**100%**. 
Looking at the network graph, node **8** is the only gateway to node **2** (a leaf node). In turn, node **6** is the only node connected to node **8**. Therefore, every possible path from node 1 to node 2 (e.g., $1 \to 3 \to 6 \to 8 \to 2$ or $1 \to 4 \to 6 \to 8 \to 2$) must pass through node 6.

---

## Exercise 8.1: Tolerating Two Node Crashes
**Question:** Which links would you add to tolerate any two node crashes without partitions?

**Answer:**
To tolerate two node crashes, the graph must be **3-connected** (every node must have at least degree 3, and there must be 3 node-disjoint paths between any two nodes). 
**Recommended Additions:**
1. **Link (2, 7) and (2, 13):** This gives the leaf node 2 a degree of 3 and alternative paths.
2. **Link (8, 4) and (8, 12):** This bypasses the bottleneck at node 6.
3. **Link (5, 1) and (5, 11):** This ensures node 5 is not isolated if 6 and 7 crash.