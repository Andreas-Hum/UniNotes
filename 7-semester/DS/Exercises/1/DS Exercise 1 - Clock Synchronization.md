### Q: How might two computers on a local network synchronize without an external time source? What limits accuracy? How is it done on the Internet?
**Internal Synchronization (Local Network):**
Without an external source, computers use **Internal Synchronization**, such as the **Berkeley Algorithm**. One computer acts as a coordinator, polls the others for their times, averages them (including its own), and tells each computer how much to adjust its clock.

**Limiting Factors:**
* **Network Jitter:** Variability in the time it takes to send/receive messages.
* **Clock Drift:** The hardware rate at which a clock "ticks" varies between machines.
* **Processing Latency:** The time the operating system takes to process the time-sync message.

**Internet-Wide Synchronization:**
This is done using the **Network Time Protocol (NTP)**. It uses a hierarchy of "Strata" where Stratum 1 servers are linked to atomic clocks and Stratum 2/3 servers sync with them over the Internet.

**Accuracy:** On the public Internet, accuracy is usually within **10-50 milliseconds** due to the unpredictable nature of network congestion and routing delays.

---

### Q: What is the main disadvantage of distributed systems using the Internet? How is it overcome?
**Main Disadvantage:**
The lack of **Quality of Service (QoS) guarantees**. The Internet is a "best-effort" network, meaning it does not guarantee bandwidth, latency, or reliability. This leads to unpredictable performance.

**How to Overcome:**
* **Replication and Caching:** Storing data closer to the user to reduce dependence on long-distance network hops.
* **Middleware:** Using software layers that automatically handle retries, timeouts, and data recovery.
* **Redundancy:** Routing data through multiple paths to ensure arrival.

---

### Q: What are the implications of using home desktops in P2P systems for availability and security?
**Implications:**
* **Availability:** Home computers have high **"churn"**—users turn them off or disconnect them frequently, making data often unavailable.
* **Security:** These hosts are not in "hardened" data centers. They are susceptible to local user tampering, malware, and physical theft of data.

**Role of Replication:**
* **Availability:** Highly effective. By spreading copies of data across many nodes, the object remains reachable even if a large percentage of nodes go offline.
* **Security:** Less effective. While it prevents data loss, it increases the **attack surface** because there are now more copies of the data that could potentially be compromised.

---

### Q: Why does NTP provide no guaranteed bound for the difference between two clocks?
Even with NTP, no guaranteed bound can be given because the Internet is an **Asynchronous Network**. 
* In such networks, there is **no maximum upper bound** on how long a message takes to travel between two points.
* Because the receiver cannot know exactly how long a timestamp message was "in flight," it cannot calculate the exact error, only an estimate.

---

### Q: Speedup Calculation (Amdahl's Law)
*Program: 60% parallel ($f=0.6$), 40% sequential ($1-f=0.4$).*

**a) 2 processors ($n=2$):**
$$Speedup = \frac{1}{0.4 + \frac{0.6}{2}} = \frac{1}{0.4 + 0.3} = \frac{1}{0.7} \approx 1.43$$

**b) 4 processors ($n=4$):**
$$Speedup = \frac{1}{0.4 + \frac{0.6}{4}} = \frac{1}{0.4 + 0.15} = \frac{1}{0.55} \approx 1.82$$

**c) Infinite processors ($n=\infty$):**
$$Speedup = \frac{1}{0.4 + 0} = 2.5$$
*Note: The speedup can never exceed 2.5, regardless of how many processors you add.*

---

### Q: Finding the Parallel Fraction
*Scenario: Speedup ($S$) of 5 on 8 processors ($n=8$).*

We use the formula: $S = \frac{1}{(1-f) + \frac{f}{n}}$
$$5 = \frac{1}{(1-f) + \frac{f}{8}}$$
$$5(1 - f + 0.125f) = 1$$
$$5(1 - 0.875f) = 1$$
$$5 - 4.375f = 1$$
$$4 = 4.375f$$
$$f = \frac{4}{4.375} \approx 0.914$$

**Result:** The parallelized fraction ($f$) of the program is approximately **91.4%**.