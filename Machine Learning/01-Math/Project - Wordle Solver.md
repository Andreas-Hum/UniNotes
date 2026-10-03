---
tags: [ml, project, information-theory]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Wordle Solver

> [!summary] In one sentence
> Build a Wordle bot that picks every guess to maximise expected information (entropy), the same quantity behind decision-tree splits, then play IT-ret Wordle with the 5-letter words from your own Danish notes.

**Notebook:** [Project - Wordle Solver](Project%20-%20Wordle%20Solver.ipynb) · topic: [[Information Theory]] · all projects: [[Projects Overview]]

## What you build
1. `feedback`: the green/yellow/grey rule with duplicate letters (the classic bug).
2. `entropy`: expected bits of a guess, $H=-\sum_k p_k\log_2p_k$ over feedback patterns.
3. `pick_guess`: the max-entropy guess over the answers still possible.

## Reference results (solution, laptop CPU)
| solver (200 secret words, 1,500-word answer list from text8) | avg. guesses | solved ≤ 6 |
|---|---|---|
| random consistent guess | 3.83 | 99 % |
| **max entropy** | **3.23** | **100 %** |

Best openers: *aires*, *rates*, *tales* (≈ 6.1 bits of a possible 10.55). Best Danish opener from the IT-ret words: *taler*.

## Check yourself
> [!question]- Why is the maximum first-guess information log2(1500) bits, and why can't a real guess reach it?
> A guess can at most split 1,500 answers into 1,500 single-answer groups (log2 1500 = 10.55 bits). There are only 243 feedback patterns, so at most log2 243 = 7.9 bits, and real words land far lower (≈ 6.1).

> [!question]- How is this the same as choosing a decision-tree split?
> Both pick the question whose answer reduces uncertainty the most: information gain = entropy before − expected entropy after.

## Learn more
- [3Blue1Brown – Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)

---
Back to [[00 - Machine Learning Index]].
