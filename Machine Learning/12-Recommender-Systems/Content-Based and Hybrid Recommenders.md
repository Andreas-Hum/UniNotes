---
tags: [ml, recsys]
---
# Content-Based and Hybrid Recommenders

## Content-based
1. Represent items with features: genre, tags, TF-IDF of text, image/text embeddings ([[Text Representations]]).
2. Build a user profile: weighted average of liked item vectors, or train a per-user classifier ([[Logistic Regression]], [[Naive Bayes]]).
3. Score by similarity (cosine).

+ no cold-start for new items, explainable ("because you liked X")
− over-specialisation (filter bubble), needs good features, new users still cold

## Knowledge-based / constraint-based
Explicit requirements (budget, size) — cars, real estate.

## Hybrids
| Type | Example |
|---|---|
| Weighted | blend CF and content scores |
| Switching | content for new items, CF otherwise |
| Feature augmentation | CF output as a feature for a ranker |
| Model-level | LightFM, factorization machines, two-tower with side features ([[Deep Learning Recommenders]]) |

## Cold-start strategies
Onboarding questionnaires, popularity by segment, content/meta features, bandit exploration ([[Q-Learning and Policy Gradients]]), transfer from other domains.

See [[Recommender Systems Overview]].
