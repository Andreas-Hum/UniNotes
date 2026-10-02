---
tags: [ml, nlp]
---
# Text Representations

| Representation | Idea | Pros / cons |
|---|---|---|
| One-hot / bag-of-words | count vector over vocabulary | simple, sparse, no order |
| **TF-IDF** | $tf(t,d)\cdot\log\frac{N}{df(t)}$ | strong baseline for classification/search |
| n-grams | include word sequences | some local order |
| **word2vec** (CBOW / skip-gram) | predict context words; negative sampling | dense, analogies ($king-man+woman\approx queen$) |
| GloVe | factorise co-occurrence matrix | similar to word2vec |
| fastText | subword character n-grams | handles rare/misspelled words |
| **Contextual** (ELMo, BERT) | vector depends on sentence | polysemy handled |
| **Sentence embeddings** (SBERT, E5, BGE) | one vector per sentence, contrastive training | semantic search, clustering, [[RAG and Agents]] |

Cosine similarity is the default comparison. Dimensionality reduction for plots: [[Dimensionality Reduction]].
Used in [[Content-Based and Hybrid Recommenders]] and [[NLP Overview]].
