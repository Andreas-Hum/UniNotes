---
tags: [ml, project, graphs, pagerank]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - PageRank of My Vault

> [!summary] In one sentence
> Turn this Obsidian vault into a graph of wikilinks, implement PageRank (checked against NetworkX), find the hub notes and the orphans, and get Adamic–Adar link suggestions.

**Notebook:** [Project - PageRank of My Vault](Project%20-%20PageRank%20of%20My%20Vault.ipynb) · topic: [[Graph ML Overview]] · all projects: [[Projects Overview]]

## What you build
1. `wikilinks`: parse `[[Note]]`, `[[Note|alias]]`, `[[Note#Heading]]`, `[[folder/Note]]`.
2. `pagerank`: power iteration with teleportation and dangling nodes.

## Reference results (solution, laptop CPU)
133 notes, 1,044 links (ML + IT-ret). Top PageRank: **Transformers** (0.049), Common Pitfalls, Cross-Validation and Model Selection, Backpropagation, Optimizers. Only 2 notes had no incoming links (the exercise list and the IT-lov index). The numbers change as you write.

## Check yourself
> [!question]- Why does PageRank need teleportation?
> Without it the surfer gets trapped in groups of notes with no way out (rank sinks), and the iteration may not converge to a unique answer. Teleportation makes the Markov chain irreducible and aperiodic.

> [!question]- Why isn't PageRank just the number of in-links?
> A link from an important note counts more than one from an obscure note, and a note that links to 50 others passes on only 1/50 of its rank per link.

---
Back to [[00 - Machine Learning Index]].
