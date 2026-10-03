---
tags: [ml, play, challenges]
status: not-started
level:
reviewed:
---
# Weekly Challenges

> [!summary] In one sentence
> One small dataset per week, sized for one evening, Kaggle-style: a story, a baseline, a **target score to beat**, an automatic ✅/❌ check and a hidden solution walkthrough.

Each notebook has the same shape: story → fixed split → quick look → baseline → ✏️ *Your turn* (starts as a copy of the baseline) → 🏁 *Evaluate* (prints ✅/❌ against the target) → 💡 three hints → 🏆 solution walkthrough (collapsed). Make all decisions with the training data; the evaluate cell is the only thing that touches the test set.

| Week | Challenge | Type | Difficulty | Metric | Baseline | Target | Theory |
|---|---|---|---|---|---|---|---|
| 01 | [Second Opinion](Weekly%20Challenge%2001%20-%20Second%20Opinion.ipynb) – breast-cancer biopsies | tabular classification | ★☆☆☆ | accuracy ↑ | 0.924 | **≥ 0.97** | [[k-Nearest Neighbors]] · [[Data Preprocessing]] |
| 02 | [House Hunters](Weekly%20Challenge%2002%20-%20House%20Hunters.ipynb) – California house prices | tabular regression | ★★☆☆ | RMSE ↓ | 0.746 | **≤ 0.48** | [[Ensemble Methods]] · [[Feature Engineering]] |
| 03 | [Help-Desk Router](Weekly%20Challenge%2003%20-%20Help-Desk%20Router.ipynb) – 5 overlapping computer newsgroups | text classification | ★★★☆ | macro-F1 ↑ | 0.545 | **≥ 0.70** | [[Text Representations]] · [[Naive Bayes]] |
| 04 | [Flight Planner](Weekly%20Challenge%2004%20-%20Flight%20Planner.ipynb) – airline passengers, 24 months ahead | time-series forecasting | ★★★★ | MASE ↓ | 2.494 | **≤ 0.80** | [[Time Series Forecasting]] · [[Time Series Validation and Features]] |

**Data:** week 01 is bundled with scikit-learn (offline). Weeks 02–03 use scikit-learn's downloaders (≈ 400 KB and ≈ 14 MB, cached after the first run). Week 04 reads a 2 KB CSV from GitHub.

> [!tip] How to get the most out of it
> - Give yourself one evening. Write down your plan *before* coding: "what is the baseline getting wrong?"
> - Use a hint only after 20 minutes stuck. Open the solution only after you've beaten the target, or given up.
> - After the solution, write one sentence in [[Today I Learned]]: what was the key idea?
> - Every challenge has headroom past the target. Going back later and beating your old score is the point.

## My log
Add a row whenever you beat the target, or set a new personal best.

| Date | Week | Score | Approach (one line) |
|---|---|---|---|
| | | | |

## Ideas for future weeks
- Imbalanced fraud detection (PR-AUC) · image classification on `load_digits` with a small CNN · customer segmentation (silhouette score) · MovieLens top-10 recommendations · a SARIMA/Holt–Winters rematch of week 04 with rolling-origin validation.

Related: [[Break the Model]] · [[Guess the Output]] · [[Playgrounds]] · [[Common Pitfalls]]
