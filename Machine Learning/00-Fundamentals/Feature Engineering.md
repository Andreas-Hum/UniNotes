---
tags: [ml, fundamentals, features]
---
# Feature Engineering

- **Numeric**: scaling, log/Box–Cox for skew, binning, polynomial and interaction terms.
- **Categorical**: one-hot, ordinal, target/mean encoding (beware leakage), hashing, learned embeddings.
- **Text**: bag-of-words, TF-IDF, n-grams, word/sentence embeddings, [[Transformers]].
- **Time**: lags, rolling statistics, cyclic sin/cos encoding of hour/month.
- **Missing values**: indicator flags + imputation (see [[Data Preprocessing]]).
- **Selection**: filter (correlation, mutual information), wrapper (RFE), embedded (L1, tree importances).
- **Extraction**: [[PCA]], autoencoders, [[Kernel Methods]] (implicit feature maps).

Non-linear feature maps $\phi(x)$ turn linear models into non-linear ones; see [[Linear Models for Classification]].
