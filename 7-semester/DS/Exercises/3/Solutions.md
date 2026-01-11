# Lecture 3 - Exercises: Solutions

## Exercise 1: Unix Time vs ISO 8601
**Unix Time:** An integer representing the number of seconds that have elapsed since the **Unix Epoch** (January 1, 1970, 00:00:00 UTC), not counting leap seconds.
**ISO 8601:** A string-based international standard for representing dates and times (e.g., `2026-01-11T03:31:00Z`).

**Conversion Logic:**
- **Unix to ISO 8601:** Take the Unix timestamp, add it to the Epoch date, and format as a string.
- **ISO 8601 to Unix:** Parse the string to a date object and calculate the offset from the Epoch in seconds.

---

## Exercise 2: Why not use ISO 8601 everywhere?
While ISO 8601 is human-readable, it is less efficient for computers because:
1. **Computational Overhead:** Comparing two strings (ISO 8601) is significantly slower than comparing two 64-bit integers (Unix time).
2. **Storage Space:** A Unix timestamp typically takes 8 bytes, while an ISO 8601 string can take 20+ bytes.
3. **Arithmetic:** Calculating the duration between two events is trivial with integers ($T_2 - T_1$) but complex with formatted strings.

---

## Exercise 3: Bounds on `elapsedTime`
**Scenario:** `fun()` takes 50ms. Time is measured using `System.currentTime()`, which syncs with NTP.
**Answer:** There are **no strict bounds** on `elapsedTime`.
- **Reasoning:** If an NTP update occurs during the execution of `fun()`, the system clock could be adjusted forward or backward.
- **Lower Bound:** Could be **negative**. If the NTP sync sets the clock back by more than 50ms, `endTime < startTime`.
- **Upper Bound:** Could be **much larger than 50ms**. If the NTP sync jumps the clock forward.
*Note: This is why `System.nanoTime()` is preferred for measuring duration, as it is monotonic and unaffected by clock jumps.*

---

## Exercise 4: Happens-Before Pairs
*Note: Since the slides are not provided here, the methodology for finding these pairs (from Lamport's definition) is used:*
1. **Local Order:** Every pair of events $(e_1, e_2)$ in the same process where $e_1$ is before $e_2$ is a pair.
2. **Message Flow:** Every pair $(s, r)$ where $s$ is the sending of a message and $r$ is the receipt of that message is a pair.
3. **Transitive Closure:** If $a \to b$ and $b \to c$, then $(a, c)$ is a pair.

---

## Exercise 5: Proof of Trichotomy
**Question:** Prove that for any two events $a$ and $b$, either $a \to b$, $b \to a$, or $a \parallel b$.
**Proof:**
By the definition of the **Happens-Before** relation ($\to$):
1. If there is a causal path (local steps or messages) from $a$ to $b$, then **$a \to b$**.
2. If there is a causal path from $b$ to $a$, then **$b \to a$**.
3. If no such path exists in either direction, the events are **concurrent**, denoted as **$a \parallel b$**.
Because a path either exists in one direction, the other, or neither, these three cases are mutually exclusive and collectively exhaustive.

---

## Exercise 6: Proof of Strict Partial Order
A strict partial order must be **irreflexive** and **transitive**.

1. **Transitivity:** Follows directly from the definition. If $a$ causally affects $b$, and $b$ causally affects $c$, then $a$ causally affects $c$.
2. **Irreflexivity:** An event cannot happen before itself ($a \nrightarrow a$).
   - **Proof by Physics:** In a distributed system, for $a \to a$ to be true, there would have to be a cycle of messages/events. Since information cannot travel faster than the speed of light and nodes are at non-zero distances, any message sent from $P_i$ and returning to $P_i$ must arrive at a strictly later physical time. Thus, a causal loop is physically impossible.

---

## Exercise 7: NTP Calculation
**Given:**
- $t_1 = 3:31$ (Client sends request)
- $t_2 = 3:30$ (Server receives)
- $t_3 = 3:31$ (Server sends response)
- $t_4 = 3:34$ (Client receives)

**1. Estimated Network Delay ($d$):**
$$d = \frac{(t_4 - t_1) - (t_3 - t_2)}{2} = \frac{(3 \text{ min}) - (1 \text{ min})}{2} = 1 \text{ minute}$$

**2. Estimated Clock Skew ($o$):**
$$o = \frac{(t_2 - t_1) + (t_3 - t_4)}{2} = \frac{(-1 \text{ min}) + (-3 \text{ min})}{2} = -2 \text{ minutes}$$
*Interpretation: The client's clock is 2 minutes **ahead** of the server's clock.*

**Clock Correction:**
The client should adjust its clock back by 2 minutes. In production, this is usually done by **slewing** (slightly slowing down the clock rate) rather than **stepping** (jumping the time) to avoid breaking applications that rely on monotonic time.

---

## Exercise 8: Safety Properties
Safety properties state that "a bad thing never happens." They can be falsified by a finite execution prefix.

1. **Eventually detected:** **Liveness** (something good eventually happens).
2. **No process detected before it crashes:** **Safety** (the "bad thing" of false detection never happens).
3. **No two processes decide differently:** **Safety** (Agreement—the "bad thing" of disagreement never happens).
4. **No two correct processes decide differently:** **Safety**.
5. **Every correct process decides before time $t$:** **Safety**. If a process hasn't decided by $t$, the property is violated at that specific moment.
6. **If some correct process decides then...:** **Liveness** (part of Termination/Validity).