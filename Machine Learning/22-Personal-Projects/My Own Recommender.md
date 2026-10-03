---
tags: [ml, project, recommender-systems]
status: not-started
notebook: not-started
level: I
reviewed:
---
# My Own Recommender

> [!summary] In one sentence
> Rate 15 movies, join MovieLens as a new user without retraining anything (fold-in), blend in genres and tags so Danish films get a chance, then turn your own Spotify history into artist embeddings.

**Notebook:** [My Own Recommender - Notebook](My%20Own%20Recommender%20-%20Notebook.ipynb) · part of [[Personal Projects]]

## Intuition first
Matrix factorisation gives every movie a vector of hidden "taste dimensions". Once those are learned from 100k ratings, **you** are just one small regression away: which taste vector best explains *your* 15 ratings? That's **fold-in**, and it's how real systems handle new users between nightly retrains.

## What you build (6 TODOs)
**Movies (MovieLens latest-small)**
1. `solve_ridge`: the closed-form ridge regression at the heart of ALS.
2. `fold_in`: your user bias + taste vector from your ratings, item vectors fixed.
3. `recommend`: top-N, excluding what you rated and obscure films.
4. `content_profile`: a TF-IDF profile of genres + tags, weighted by your *centred* ratings (dislikes push away).

**Music (your Spotify export)**
5. `sessionize`: split listening history into sessions (30-minute gaps).
6. `ppmi`: positive pointwise mutual information of artist co-occurrence → SVD → artist embeddings ("word2vec without a neural net").

## Reference results
| | value |
|---|---|
| test RMSE: global mean / biases / **ALS k=20** | 1.028 / 0.861 / **0.849** |
| 40 brand-new users, 20 ratings each: RMSE biases → fold-in | 0.898 → 0.894 |
| … ranking quality (Spearman) | 0.321 → 0.335 |

The honest lesson: on a dataset this small, most of the gain for a new user comes from their **bias** (harsh or generous rater). The factors add a small, real improvement in *ranking*, and ranking is what you see as a top-10.

## Your data
- **Movies:** edit `MY_RATINGS` (use `find_movie("festen")` for exact titles). The example includes Danish films: Festen, Pusher, Blinkende lygter, Adams æbler, De grønne slagtere, Hævnen.
- **Spotify:** *Account → Privacy settings → Download your data* ([what's in it](https://support.spotify.com/us/article/understanding-my-data/)). "Account data" takes ~5 days; "Extended streaming history" up to 30 days but covers all years. Unzip into `22-Personal-Projects/data/spotify/`. Both formats load automatically. Until it arrives, a clearly labelled **synthetic** demo history runs instead.
- **Recipes:** the Food.com dataset works with the same ALS + content code (link in the notebook).

## Common confusions
- **RMSE vs. what users feel**: a 0.004 RMSE gain sounds like nothing, but the *order* of the top-10 can change a lot. Evaluate ranking too ([[Evaluating Recommenders]]).
- **Content alone = filter bubble**: a pure genre profile recommends more of the same. The blend weight `ALPHA` trades familiarity vs. discovery.
- **Play counts aren't ratings**: on Spotify you never say "I dislike this". Skips and short plays are the closest thing to negative feedback (implicit feedback).

## Check yourself
> [!question]- Why does fold-in need a regulariser (λ) when you have only 15 ratings?
> With $k=20$ factors and 15 ratings the least-squares system is under-determined: infinitely many vectors fit perfectly. λ picks the smallest one and keeps you close to "average taste" until there's evidence.

> [!question]- Why centre your ratings before building the content profile?
> If all weights were positive (1–5 stars), every movie you rated would pull the profile *towards* it, even the ones you hated. Centring on *your* mean makes 1.5-star movies pull *away*.

> [!question]- How is the PPMI + SVD trick related to word2vec?
> Skip-gram with negative sampling implicitly factorises a shifted PMI matrix of word–context co-occurrences ([Levy & Goldberg 2014](https://papers.nips.cc/paper_files/paper/2014/hash/b78666971ceae55a8e87efb7cbfd9ad4-Abstract.html)). Sessions are "sentences", artists are "words".

## Learn more
- [MovieLens datasets (GroupLens)](https://grouplens.org/datasets/movielens/)
- Vault: [[Collaborative Filtering and Matrix Factorization]] · [[Content-Based and Hybrid Recommenders]] · [[Multimodal Recommender Systems]] · [[Project - MovieLens Recommender]]
