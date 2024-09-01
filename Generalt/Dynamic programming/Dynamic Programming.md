# Introduction to Dynamic Programming
Dynamic Programming (DP) is a powerful algorithmic paradigm that solves complex problems by breaking them down into simpler subproblems. It's particularly useful for optimization problems. This document will explore various strategies and techniques for applying DP effectively.


## How Does Dynamic Programming (DP) Work?

1. **Identify Subproblems:** Divide the main problem into smaller, independent subproblems.
2. **Store Solutions:** Solve each subproblem and store the solution in a table or array.
3. **Build Up Solutions:** Use the stored solutions to build up the solution to the main problem.
4. **Avoid Redundancy:** By storing solutions, DP ensures that each subproblem is solved only once, reducing computation time.

## The Principle of Subproblem Optimization

### Theory
The core idea of DP is to solve each subproblem once and store its solution. When the same subproblem occurs again, we can simply look up the previously computed solution, saving computation time at the expense of storage space.

### Application
When designing a DP solution:
1. Define the state clearly: What information do you need to solve a subproblem?
2. Establish state transitions/recurrence relation: How does solving one subproblem help solve larger problems?
3. Identify the base cases: What are the simplest subproblems you can solve directly?
## The Art of State Design

### Theory
Effective state design is crucial in DP. The state should capture all necessary information to solve a subproblem while being as compact as possible to optimize space and time complexity.

### Application
1. Identify the changing parameters in the problem.
2. Determine the minimum information needed to transition between states.
3. Consider using composite states (e.g., tuples) for multi-dimensional problems.

## Recurrence Relations: The Heart of DP

### Theory
Recurrence relations express the solution to a problem in terms of solutions to smaller subproblems. They are the mathematical foundation of DP algorithms.

### Application
To identify and define recurrence relations:
1. Express the problem solution in terms of smaller subproblems.
2. Identify the base cases.
3. Ensure that combining subproblem solutions leads to the optimal overall solution.

### Example
Consider the problem of finding the longest increasing subsequence (LIS):

Let `dp[i]` represent the length of the LIS ending at index `i`.
Recurrence relation: `dp[i] = max(dp[j] + 1) for all j < i where arr[j] < arr[i]`
Base case:` dp[i] = 1 for all i (minimum LIS length is 1)`

## The Optimization Principle

### Theory
The optimization principle states that in an optimal sequence of decisions, each subsequence must itself be optimal. This principle is fundamental to the correctness of DP algorithms.

### Application
When designing a DP solution:
1. Ensure that the optimal solution can be built from optimal solutions to subproblems.
2. Verify that making a locally optimal choice leads to a globally optimal solution.

## Dimensionality Reduction

### Theory
Sometimes, a problem that seems to require an n-dimensional DP solution can be solved with fewer dimensions. This technique can significantly reduce time and space complexity.

### Application
1. Analyze the problem to identify dependencies between dimensions.
2. Look for ways to express higher-dimensional states using lower-dimensional information.
3. Consider using rolling arrays or maintaining only necessary states.

### Example
In the classic "Edit Distance" problem, instead of using a 2D array, we can solve it using two 1D arrays, alternating between them for each row of the original 2D solution.

### When to Use Dynamic Programming (DP)?

The first characteristic of DP problems is that they often ask for the optimum value (maximum or minimum) of something, or the number of ways to do something. For example:

- What is the minimum cost of doing...?
- What is the maximum profit from...?
- How many ways are there to do...?
- What is the longest possible...?
- Is it possible to reach a certain point...?

The second characteristic of DP problems is that future "decisions" depend on earlier decisions. Deciding to do something at one step may affect the ability to do something in a later step. This is what makes a greedy algorithm invalid for a DP problem - we need to factor in results from previous decisions.

### Identifying DP Problems
it's crucial to recognize when a problem can be solved using DP. Look for these characteristics:
1. Optimal substructure: The optimal solution to the problem can be constructed from optimal solutions of its subproblems.
2. Overlapping subproblems: The problem can be broken down into subproblems which are reused several times.
3. Decision-making at each step: The problem requires making a choice at each step, with the goal of optimizing the overall solution.

## Bottom-up (Tabulation)

Bottom-up dynamic programming is implemented with iteration, starting at the base cases. Let's use the Fibonacci sequence as an example:


```
F = array of length (n + 1)
F[0] = 0
F[1] = 1
for i from 2 to n:
    F[i] = F[i - 1] + F[i - 2]
```

**Sliding Window Technique**

The sliding window technique is a common optimization to save space in DP algorithms. Instead of keeping an array of size `n+1`, we only keep track of the last two computed values, as those are the only ones needed to compute the next Fibonacci number.

```
a = 0
b = 1
for i from 2 to n:
    temp = a + b
    a = b
    b = temp
```

This reduces the space complexity from `O(n)` to `O(1)`, while maintaining the same time complexity of `O(n)`.

## Top-down (Memoization)

Top-down dynamic programming is implemented with recursion and memoization. Let's use the Fibonacci sequence as an example again:

```
memo = hashmap
Function F(integer i):
    if i is 0 or 1: 
        return i
    if i doesn't exist in memo:
        memo[i] = F(i - 1) + F(i - 2)
    return memo[i]
```

In this implementation, we use a dictionary `memo` to store the results of previous function calls. When we need to calculate `fib(n)`, we first check if the result is already in `memo`. If so, we return the stored value. If not, we calculate the result and store it in `memo` before returning it.

### Bottom-up vs Top-down

Both bottom-up and top-down approaches can be used to solve the same DP problems, but they have their own advantages:

- **Bottom-up (Tabulation)**: Faster runtime, as iteration does not have the overhead that recursion does.
- **Top-down (Memoization)**: Easier to write, as the ordering of subproblems does not matter with recursion.

## Steps to Solve a Dynamic Programming Problem

1. **Identify if it is a Dynamic Programming problem**:
    - Look for problems that require maximizing or minimizing certain quantities, or counting problems that ask to count the arrangements under certain conditions.
    - Observe if the problem satisfies the overlapping subproblems and optimal substructure properties.
2. **Decide a state expression with the least parameters**:
    - The state should capture all the necessary information about the current situation in the problem.
    - Try to minimize the number of parameters in the state expression.
3. **Formulate state and transition relationships**:
    - Identify the relationship between the current state and the previous states.
    - Determine how you can transition from one state to another.
4. **Do tabulation (or memoization)**:
    - Implement the DP solution using either the bottom-up (tabulation) or top-down (memoization) approach.

### Examples

Let's solve a few examples to illustrate the DP thought process.

**Example 1: Climbing Stairs**

**Problem**: You are climbing a staircase. You can take either 1 step or 2 steps at a time. Given an integer `n` representing the number of stairs, return the number of distinct ways you can climb to the top.

**Solution**:

1. **Identify the DP problem**: This is a DP problem because it asks for the number of ways to reach a certain point (the top of the stairs).
2. **Decide the state**: The state can be represented by the current step number `i`, as that captures all the necessary information about the problem.
3. **Formulate the state and transition relationships**:
    - Base cases: `f(0) = 1`, `f(1) = 1` (There is 1 way to reach the 0th and 1st steps).
    - Transition: `f(i) = f(i-1) + f(i-2)` (The number of ways to reach the ith step is the sum of the number of ways to reach the (i-1)th step and the (i-2)th step).
4. **Implement the solution using tabulation**:

```python
def climbStairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**Example 2: Coin Change**

**Problem**: Given an array of distinct integers `coins` and an integer `amount`, return the minimum number of coins required to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

**Solution**:

1. **Identify the DP problem**: This is a DP problem because it asks for the minimum number of coins required to make up a certain amount.
2. **Decide the state**: The state can be represented by the current amount `i`, as that captures all the necessary information about the problem.
3. **Formulate the state and transition relationships**:
    - Base case: `dp[0] = 0` (0 coins are required to make up 0 amount).
    - Transition: `dp[i] = min(dp[i], 1 + dp[i - coin])` (The minimum number of coins required to make up amount `i` is the minimum of the current minimum (`dp[i]`) and 1 plus the minimum number of coins required to make up `i - coin`).
4. **Implement the solution using tabulation**:

```python
def coinChange(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    return dp[amount] if dp[amount] <= amount else -1
```

In this example, we use the `min(k, n)` trick to handle the case where `i - coin < 0`, as we don't want to consider those cases.

By working through these examples, you can see how the DP thought process involves identifying the state, formulating the state and transition relationships, and then implementing the solution using either tabulation or memoization.