---
tags: [ml, masters, research]
---
# Research Skills

## Reading papers
- **Three-pass method:** (1) title, abstract, figures and conclusion in 10 minutes; (2) the method in detail, skipping proofs; (3) re-derive or re-implement.
- Keep notes with [[Paper Reading Template]] and link papers to each other in this vault.
- Find papers on [arXiv](https://arxiv.org/), [Hugging Face Papers](https://huggingface.co/papers) and [Semantic Scholar](https://www.semanticscholar.org/). For a new sub-field, start with a survey (e.g. the [multimodal recommender survey](https://arxiv.org/abs/2302.03883)).

## Running experiments
- **Baselines first**, and tune them as carefully as your own method (common critique: tuned MF often matches "new" recommenders, see [[Deep Learning Recommenders]]).
- **Multiple seeds** (≥3–5); report mean ± std.
- **Ablations**: remove one component at a time to show what matters.
- **Statistical tests** when comparing models: paired t-test or Wilcoxon over seeds/folds; corrected resampled t-test for CV; Friedman + Nemenyi for many datasets (Demšar, JMLR 2006).
- **No test-set tuning**, no leakage ([[Common Pitfalls]], [[Cross-Validation and Model Selection]]).
- **Track everything**: config, git commit, seed, metrics (W&B / MLflow, [[MLOps Overview]]).
- Training recipe: [Karpathy — A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) · [Google Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook)
- Structuring projects: [Andrew Ng — Machine Learning Yearning](https://info.deeplearning.ai/machine-learning-yearning-book)

## Writing (thesis / papers)
- Structure: problem → why it matters → gap → contribution (as bullet points) → method → experiments that answer explicit research questions → limitations.
- Every figure should make one point; the caption should state that point.
- Write the related-work section as a comparison ("unlike X, we…"), not a list.
- Use the same notation throughout; define it once in a table.
- Tools: LaTeX/Overleaf, Zotero (reference manager) + Better BibTeX, Excalidraw for figures.

## Presenting
State the one-sentence takeaway at the start and at the end. Put backup slides with derivations in an appendix.
