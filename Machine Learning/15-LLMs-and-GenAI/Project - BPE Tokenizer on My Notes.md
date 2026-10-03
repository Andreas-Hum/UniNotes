---
tags: [ml, project, tokenization, llms]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - BPE Tokenizer on My Notes

> [!summary] In one sentence
> Train byte-pair encoding on your Danish IT-ret notes and watch it learn tokens like behandlingsgrundlag and datatilsynet: 11 words of legalese become 17 tokens instead of 73 characters.

**Notebook:** [Project - BPE Tokenizer on My Notes](Project%20-%20BPE%20Tokenizer%20on%20My%20Notes.ipynb) · topic: [[LLMs Overview]] · all projects: [[Projects Overview]]

## What you build
1. `pair_counts`: frequency-weighted adjacent symbol pairs.
2. `merge`: replace a pair by one symbol everywhere.

Then 500 merges and an encoder.

## Reference results (solution, laptop CPU)
First merges: *er, e</w>, t</w>, en, er</w>…*; learned whole words include *behandlingsgrundlag, databehandler, datatilsynet, hacking*. The test sentence: 11 words → **17 tokens** vs 73 characters, e.g. `dataansvar` + `lige</w>`, `person` + `oplysninger</w>`.

## Check yourself
> [!question]- Why does an English sentence cost many more tokens with this tokenizer?
> The merges were learned from Danish, so English words are split into small, rare pieces. LLM tokenizers are trained mostly on English, which makes Danish more expensive per word.

> [!question]- What is the `</w>` marker for?
> It separates word-final pieces from word-internal ones ("er" at the end of *behandler* vs. inside *personer*) so words can be reassembled with spaces.

## Learn more
- [Sennrich, Haddow, Birch – Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)

---
Back to [[00 - Machine Learning Index]].
