---
tags: [ml, recsys, evaluation]
status: not-started
notebook: not-started
level:
reviewed:
---
# Evaluating Recommenders

> [!summary] In one sentence
> Evaluating a recommender means checking whether the items users actually went on to like appear **near the top** of its ranked lists, using a split that never lets the model peek into the future, and finally confirming offline gains with online experiments.

## Intuition first

A recommender shows a short list, and people mostly look at the top. So "is the model good?" really means: *when we hide some things a user later did, does the model put them high in its list?* That leads to three separate questions:

1. **What to measure.** Accuracy of star predictions (RMSE) matters only if you display stars. For lists you need **ranking metrics** that reward putting relevant items early: Precision/Recall@K, HitRate, MRR, MAP, NDCG, AUC. And beyond accuracy: is the list diverse, does it cover the catalogue, does it surprise?
2. **How to hold out data.** If you hide a random click from March but train on the user's clicks from April, the model has seen the future. Offline scores then look great and mean nothing. The split must respect time.
3. **Does it hold online?** Offline logs only contain reactions to what the *old* system showed. The final judge is an A/B test (or interleaving), or a careful off-policy estimate from logged data.

## Offline metrics
| Metric | Formula / idea |
|---|---|
| RMSE / MAE | rating prediction error |
| Precision@K / Recall@K | relevant items in top K |
| HitRate@K | ≥1 relevant in top K |
| **MRR** | $\frac1{|U|}\sum\frac1{\text{rank}_u}$ of first relevant |
| **MAP@K** | mean of average precision |
| **NDCG@K** | $\frac{DCG}{IDCG}$, $DCG=\sum_{k}\frac{2^{rel_k}-1}{\log_2(k+1)}$ |
| AUC | pairwise ranking correctness |
| Coverage, diversity, novelty, serendipity | beyond accuracy |

![A ranked list of five items with relevance, position discounts and gains; moving a relevant item to the top raises NDCG](../../Attachments/ML%20Animations/Evaluating%20Recommenders%20-%20NDCG%20discount.gif)

*Watch the blue discount bars shrink with rank, then see NDCG jump from 0.65 to 0.92 when the model moves relevant item D from rank 4 to rank 1.*

## The math, step by step

For one user: the model's ranked list, the set $\mathrm{rel}$ of held-out relevant items, and $\mathrm{rel}_k\in\{0,1\}$ (or a grade) for the item at rank $k$.

- **Precision@K** $=\frac{|\mathrm{rel}\cap\text{top}K|}{K}$: what fraction of the shown items were good.
- **Recall@K** $=\frac{|\mathrm{rel}\cap\text{top}K|}{|\mathrm{rel}|}$: what fraction of the good items were shown. If $|\mathrm{rel}|>K$, recall can never reach 1.
- **HitRate@K** $=\mathbb 1[|\mathrm{rel}\cap\text{top}K|\ge1]$: natural with leave-one-out (exactly one held-out item).
- **MRR**: $\frac1{|U|}\sum_u\frac1{\text{rank}_u}$, with $\text{rank}_u$ the position of the first relevant item (contributes 0 if it is outside the cut-off). Rank 1 → 1, rank 2 → 0.5, rank 10 → 0.1: steep reward for the very top.
- **AP@K** $=\frac{1}{\min(K,|\mathrm{rel}|)}\sum_{k=1}^K P@k\cdot\mathrm{rel}_k$: average the precision at each position where a relevant item appears. **MAP@K** is its mean over users.
- **DCG@K** $=\sum_{k=1}^K\frac{2^{rel_k}-1}{\log_2(k+1)}$: each relevant item contributes a *gain* $2^{rel_k}-1$ (with graded relevance, a "3" is worth much more than a "1"), *discounted* by $\log_2(k+1)$: rank 1 counts fully, rank 3 half, rank 7 a third. **IDCG@K** is the DCG of the best possible ordering, so **NDCG@K** $=\frac{DCG@K}{IDCG@K}\in[0,1]$ is comparable across users with different numbers of relevant items.
- **AUC** (per user): the fraction of (positive, negative) pairs where the positive scores higher (ties count ½). Equivalently, via ranks (Mann–Whitney U): $\mathrm{AUC}=\frac{\sum_{i\in+}\mathrm{rank}_i-n_+(n_++1)/2}{n_+n_-}$. AUC weights a swap at rank 900 the same as a swap at rank 1, which is why NDCG@10 fits a 10-item feed better.

**Beyond accuracy**, each catching a failure accuracy cannot see:
- **coverage**: share of the catalogue that appears in anyone's top-K (popularity models score near zero: everyone sees the same 10 items);
- **diversity**: dissimilarity within one list (ten near-identical phone cases);
- **novelty**: how unpopular / unknown the recommended items are (recommending the Beatles to everybody is accurate but useless);
- **serendipity**: relevant *and* unexpected (the only thing a user could not have found alone).

## Worked example

A model ranks $[A,B,C,D,E]$; the user's relevant held-out items are $\{B,D,G\}$ (G was not retrieved).
- Precision@3 $=1/3$ (B), Recall@3 $=1/3$. Precision@5 $=2/5$, Recall@5 $=2/3$ (G is missing, so recall@5 cannot reach 1).
- First relevant at rank 2 → reciprocal rank $=0.5$. HitRate@1 $=0$, HitRate@3 $=1$.
- AP@5: relevant at ranks 2 and 4, with $P@2=1/2$ and $P@4=2/4$, so $\mathrm{AP@5}=\frac{1}{\min(5,3)}(0.5+0.5)=\frac13$.
- NDCG@5 (binary): $DCG=\frac{1}{\log_23}+\frac{1}{\log_25}\approx0.63+0.43=1.06$. Ideal: three relevant items at ranks 1–3, $IDCG=1+0.63+0.5=2.13$, so $NDCG\approx0.50$. (In the animation only two items are relevant, so $IDCG=1.63$ and $NDCG=0.65$.)

**AUC by counting pairs.** Positives score $0.8, 0.5$; negatives $0.6, 0.2, 0.1$. Of the 6 pairs, $0.8$ beats all three negatives and $0.5$ beats two: $\mathrm{AUC}=5/6\approx0.83$.

## Splitting

![Three users' interaction timelines; a random split leaves future items in training, leave-last-out holds out each user's most recent item](../../Attachments/ML%20Animations/Evaluating%20Recommenders%20-%20random%20vs%20temporal%20split.gif)

*Watch the orange brace: under a random split the training data contains what this user did after the test item. Leave-last-out moves every red test dot to the end of its timeline.*

- **Temporal / leave-last-out**: hold out each user's most recent interaction(s) — avoids future leakage ([[Common Pitfalls]]).
- Random splits overestimate performance.
- **Sampled metrics** (rank among 100 random negatives) can mis-rank models — prefer full ranking (Krichene & Rendle 2020).

Why random splits overestimate, two ways: (1) **the user's own future**: the model trains on interactions that happened *after* the test one, e.g. the sequel the user watched next; (2) **global trends**: items that become popular later are already popular in the training data, so the model "knows" tomorrow's hits. Leave-last-out fixes (1) but can still leak (2), since another user's last item may be later than this user's test item. A **global time cut** (train before date $T$, test after) fixes both and mimics deployment best.

**Why sampled metrics mislead.** Ranking the held-out item against only $n$ random negatives instead of the whole catalogue makes the task far easier, and *not uniformly* easier for all models. Example: the held-out item has 100 items scoring above it among 5,000 candidates (true rank 101, a miss for HR@10). With 50 sampled negatives, the expected number above it is $50\cdot\frac{100}{5000}=1$, so the expected sampled rank is about 2: a "hit". Sampled metrics compress differences between models and can even reverse their order. Prefer full ranking.

## Online
A/B tests (CTR, conversion, retention, watch time), interleaving, counterfactual / off-policy evaluation (IPS) from logged data.

- **A/B test**: split users randomly into control and treatment, compare business metrics. The gold standard, but slow and needs many users because of user-to-user variance.
- **Interleaving**: merge both rankers' lists into one list (e.g. team-draft), show it to the **same** user, and credit clicks to the ranker that contributed the clicked item. Each user compares both systems directly, which removes between-user variance; it needs far fewer users than an A/B test to detect which ranker is better.
- **Off-policy evaluation with IPS.** Logs were produced by a logging policy $\pi_0$. To estimate the click rate of a new policy $\pi$ without deploying it, reweight each logged reward by how much more (or less) likely $\pi$ would have taken the same action:
$$\hat V_{\text{IPS}}(\pi)=\frac1n\sum_{t=1}^n\frac{\pi(a_t)}{\pi_0(a_t)}\,r_t.$$
Unbiased if $\pi_0(a)>0$ wherever $\pi(a)>0$, but high-variance when $\pi_0$ rarely took the actions $\pi$ likes (huge weights). **SNIPS** divides by $\sum_tw_t$ instead of $n$, trading a little bias for much lower variance. Example: $\pi_0$ shows A or B with probability $0.5$ each; logs (A, click), (B, no click), (B, click), (A, no click). For "always B": weights are 2 on B rows, 0 on A rows, $\hat V=\frac{0+0+2\cdot1+0}{4}=0.5$.

Why offline and online can disagree: the offline gain is on items the old system chose to show (biased logs); the metric does not match the business goal (NDCG vs retention); novelty effects; feedback loops; and the offline improvement may sit in positions users never look at.

General metrics: [[Model Evaluation and Metrics]].

## Common confusions

- **"Lower RMSE means better recommendations."** → RMSE measures star prediction on items the user chose to rate. Top-K quality is about ranking the whole catalogue; use ranking metrics.
- **"Random train/test splits are fine, like in normal ML."** → Interaction data has time order and trends; random splits leak the future and inflate scores.
- **"Sampling 100 negatives is just a faster version of full ranking."** → It changes the metric and can reverse model comparisons.
- **"AUC is a top-K metric."** → AUC treats all pair swaps equally, regardless of position; NDCG/Recall@K focus on the visible top.
- **"A metric close to 1 is good."** → Compare against popularity and a tuned MF baseline under the same protocol; absolute numbers depend heavily on the split and candidate set.
- **"IPS works for any new policy."** → Only if the logging policy gave non-zero probability to the actions the new policy takes, and with enough data to tame the variance.

## Check yourself

> [!question]- Three users have their single held-out item at ranks 1, 4 and 20. What are HitRate@5 and MRR@10?
> HitRate@5 $=2/3$ (ranks 1 and 4 are in the top 5). MRR@10 $=\frac13(1+\frac14+0)\approx0.42$.

> [!question]- Why does NDCG divide by IDCG?
> To normalise to $[0,1]$: users with many relevant items would otherwise get larger DCG values regardless of model quality, and averages across users would be dominated by them.

> [!question]- What does leave-last-out still leak?
> Global trends: other users' interactions after this user's test time can be in the training set, so popularity that emerged later is visible. A global time cut removes this.

> [!question]- Which metric fits a "next song" autoplay with one correct answer?
> HitRate@K or MRR (single relevant item, position of that item matters most).

> [!question]- Why does interleaving need fewer users than an A/B test?
> Each user sees both rankers' items in one list and implicitly compares them, so the big differences between users cancel out.

## Practice

[Evaluating Recommenders - Exercises](Evaluating%20Recommenders%20-%20Exercises.ipynb): precision/recall, HitRate, MRR, AP, NDCG with graded relevance, AUC, sampled metrics and IPS by hand; split leakage, beyond-accuracy metrics, offline vs online and metric choice; then top-K metrics, NDCG checked against sklearn, AUC by counting pairs, a leave-last-out split, measuring the random-split leak, sampled vs full HitRate and IPS/SNIPS in code.

**Project:** [[Project - Sampled vs Full Ranking Metrics]] – sampled vs. full-ranking hit@10 on MovieLens

## Learn more

- Krichene & Rendle, *On Sampled Metrics for Item Recommendation* (KDD 2020).
- [scikit-learn `ndcg_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html) (note: uses linear gain, not $2^{rel}-1$).
- [[Recommender Systems Overview]] · [[Recommender Systems Resources]] · [[Model Evaluation and Metrics]]
