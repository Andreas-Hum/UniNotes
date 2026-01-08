
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