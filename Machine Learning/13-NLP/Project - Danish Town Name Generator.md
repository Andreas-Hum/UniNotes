---
tags: [ml, project, language-models]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Danish Town Name Generator

> [!summary] In one sentence
> Train character-level language models (bigram counts, then a makemore-style MLP) on Denmark's ~1,500 urban areas from Statistics Denmark and invent towns like Skallesennerup, Guldby and Herbollystrup.

**Notebook:** [Project - Danish Town Name Generator](Project%20-%20Danish%20Town%20Name%20Generator.ipynb) · topic: [[NLP Overview]] · all projects: [[Projects Overview]]

## What you build
1. `bigram_model`: smoothed character-pair counts → probabilities.
2. `nll`: average negative log-likelihood per character, the metric for language models.

Then a given 3-character-context MLP to beat the bigram.

## Reference results (solution, laptop CPU)
| model | validation NLL (nats/char) |
|---|---|
| uniform (31 symbols) | 3.43 |
| bigram | 2.38 |
| **MLP, 3 characters of context** | **1.98** |

## Check yourself
> [!question]- Why do bigram names come out too long or too short?
> The bigram only knows the previous character, not how long the name already is, so the stop decision ignores length.

> [!question]- What does an NLL of 1.98 nats mean?
> $e^{1.98}\approx7.2$: on average the model is as uncertain as a uniform choice among ~7 characters, down from 31.

## Learn more
- [Statistics Denmark API (statbank.dk)](https://api.statbank.dk/v1/tableinfo/BY1?lang=da&format=JSON) · related: [[Mini-GPT on Danish]]

---
Back to [[00 - Machine Learning Index]].
