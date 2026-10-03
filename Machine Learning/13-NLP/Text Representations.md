---
tags: [ml, nlp]
status: not-started
notebook: not-started
level:
reviewed:
---
# Text Representations

> [!summary] In one sentence
> A text representation maps words, sentences or documents to vectors, from sparse counts (bag-of-words, TF-IDF) to dense learned embeddings (word2vec, contextual BERT vectors, sentence embeddings), so that geometric closeness (usually cosine similarity) means closeness in meaning.

## Intuition first
Models need numbers, so we must decide **what each coordinate of a text vector means**.

- The simplest answer: one coordinate per vocabulary word, holding how often that word occurs. That is **bag-of-words**. It is like describing a recipe only by its shopping list: you know the ingredients but not the order of the steps. "dog bites man" and "man bites dog" get the *same* vector.
- **TF-IDF** improves the shopping list by down-weighting ingredients that are in every recipe (salt, water). A word that appears in every document tells you nothing about which document you are looking at.
- **Dense embeddings** take a different view: *"you shall know a word by the company it keeps"* (the distributional hypothesis). Words that appear in similar contexts ("coffee"/"tea") should get similar vectors. Coordinates no longer mean single words; they are learned features, and **directions** in the space start to carry meaning (a "gender" direction, a "plural" direction).
- **Contextual embeddings** go one step further: the vector for "bank" depends on whether the sentence is about rivers or money.

![Word vectors where king − man + woman lands near queen, then cosine similarity](../../Attachments/ML%20Animations/Text%20Representations%20-%20word%20analogy.gif)
*Watch the yellow "woman − man" arrow get copied onto "king" and land next to "queen"; then compare the small angle between king and queen with the large angle between king and apple.*

## The representations at a glance
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

## The math, step by step

**Bag-of-words.** With vocabulary $\{t_1,\dots,t_V\}$, document $d$ becomes $x_d\in\mathbb N^V$ with $x_{d,j}=$ number of times $t_j$ occurs in $d$. Almost every entry is 0 (sparse), and word order is lost (also punctuation, negation scope and which word modifies which).

**TF-IDF.**
$$\text{tfidf}(t,d)=tf(t,d)\cdot\log\frac{N}{df(t)}$$
- $tf(t,d)$: count of term $t$ in document $d$ ("how much does this document talk about $t$?").
- $N$: number of documents; $df(t)$: number of documents containing $t$.
- $\log\frac{N}{df(t)}$ (inverse document frequency): 0 if $t$ is in every document ($\log 1=0$), large if $t$ is rare. So frequent-everywhere words like "the" vanish, and distinctive words dominate.

scikit-learn's `TfidfVectorizer` uses a **smoothed** IDF, $\ln\frac{1+N}{1+df(t)}+1$ (never zero, no division by zero), and then **L2-normalises** each document vector.

**n-grams** add features for word pairs/triples ("not good" becomes its own feature), recovering some local order at the cost of a much larger vocabulary.

**Cosine similarity.**
$$\cos(a,b)=\frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}\in[-1,1].$$
It measures the **angle**, not the length. A long document that repeats the same words has a longer vector but the same direction, so it is not penalised for length.

**word2vec, skip-gram.** Each word has two vectors: $v_w$ when it is the centre word and $u_w$ when it is a context word. For every centre word $c$ and each context word $o$ within a window of $\pm m$ positions, skip-gram wants $u_o^\top v_c$ to be large. The full softmax over the vocabulary is too expensive, so **negative sampling** turns it into $K+1$ binary classification problems: "is $(c,o)$ a real pair or a random one?"
$$J=-\log\sigma(u_o^\top v_c)-\sum_{k=1}^{K}\log\sigma(-u_k^\top v_c),$$
where $u_1,\dots,u_K$ are random "negative" words and $\sigma$ is the sigmoid. Pull the true pair together, push the random ones apart. Its gradient with respect to the centre vector is
$$\frac{\partial J}{\partial v_c}=\big(\sigma(u_o^\top v_c)-1\big)u_o+\sum_{k}\sigma(u_k^\top v_c)\,u_k.$$
Negatives are drawn from $P_n(w)\propto c(w)^{3/4}$; the $3/4$ power flattens the unigram distribution so rare words are sampled a bit more often than their raw frequency. **CBOW** is the mirror image: predict the centre word from the average of its context vectors.

**Count-based view.** Build the word–context co-occurrence matrix, convert it to positive pointwise mutual information
$$\text{PPMI}(w,c)=\max\Big(0,\ \log\frac{P(w,c)}{P(w)P(c)}\Big),$$
and take a truncated SVD. This gives embeddings very similar to word2vec (which implicitly factorises a shifted PMI matrix). **GloVe** makes this explicit by fitting $u_i^\top v_j+b_i+b_j\approx\log X_{ij}$ on co-occurrence counts $X_{ij}$.

**fastText** represents a word as the sum of vectors of its character n-grams, with boundary markers: "where" with $n=3$ gives `<wh, whe, her, ere, re>` (plus the whole word `<where>`). An unseen word like "unfollowable" or a typo like "recieve" still gets a sensible vector from its pieces, whereas word2vec has no vector at all for them.

**Analogies.** If a relation is a consistent direction, then $v_{king}-v_{man}+v_{woman}$ should land near $v_{queen}$. We find the nearest word by cosine, **excluding the three query words** (otherwise "king" itself often wins).

**Contextual embeddings** (ELMo, BERT) compute each token's vector from the whole sentence, so "river bank" and "bank account" get different vectors (polysemy handled). **Sentence embeddings** (SBERT, E5, BGE) produce one vector per sentence, trained contrastively: pull paraphrases/question–answer pairs together and push unrelated sentences apart. A cheap baseline is **mean pooling**, the average of the word vectors.

## Worked example
**TF-IDF by hand.** $N=3$ documents: $d_1$ = "red apple", $d_2$ = "green apple apple", $d_3$ = "green pear". Using natural log:

| term | $df$ | idf $=\ln(3/df)$ | tfidf in $d_2$ |
|---|---|---|---|
| apple | 2 | $\ln 1.5=0.405$ | $2\times0.405=0.81$ |
| green | 2 | $0.405$ | $1\times0.405=0.41$ |
| red | 1 | $\ln 3=1.099$ | 0 |
| pear | 1 | $1.099$ | 0 |

"red" scores higher in $d_1$ (1.10) than "apple" (0.41): it is what makes $d_1$ distinctive.

**Cosine by hand.** $a=(2,0,1)$, $b=(1,1,1)$: $a^\top b=3$, $\lVert a\rVert=\sqrt5$, $\lVert b\rVert=\sqrt3$, so $\cos=3/\sqrt{15}\approx0.77$. Doubling $a$ to $(4,0,2)$ leaves the cosine unchanged; that is exactly why cosine is preferred for documents of different lengths.

**Analogy by hand** (the toy vectors from the animation): $\text{king}-\text{man}+\text{woman}=(4,0.5)-(1,0)+(1,2)=(4,2.5)$, and the closest remaining word is queen $(4.2,2.4)$.

## Choosing a representation
- **Small labelled dataset, keyword-driven task** (spam, topic): TF-IDF (+ bigrams) and a linear model. Fast, strong, interpretable.
- **Need similarity between words, little compute**: pretrained static embeddings (word2vec/GloVe), fastText if typos or rich morphology.
- **Meaning depends on context** (QA, NER, sentiment with negation): contextual transformer embeddings.
- **Search, clustering, retrieval for [[RAG and Agents]]**: sentence embeddings + an approximate nearest-neighbour index.
- **Visualising** embeddings: project with PCA/t-SNE/UMAP ([[Dimensionality Reduction]]), remembering that 2-D pictures distort distances.

## Common confusions
- **"word2vec gives a vector per meaning."** → It gives one vector per *word type*; "bank" is a blend of all its senses. Contextual models give one per *occurrence*.
- **"IDF makes common words important."** → The opposite: a word in every document gets IDF $\log 1=0$.
- **"Cosine similarity and Euclidean distance always disagree."** → For L2-normalised vectors they are monotonically related: $\lVert a-b\rVert^2=2-2\cos(a,b)$.
- **"Bigger embedding dimension is always better."** → More dimensions need more data; 100–300 is typical for static embeddings.
- **"Analogies prove the model understands."** → They work for some relations and fail for many; and the query words must be excluded from the search, or the answer is often trivial.

## Check yourself
> [!question]- "dog bites man" vs "man bites dog": what does bag-of-words lose, and what partially recovers it?
> Word order (who did what to whom), plus syntax and negation scope. Adding n-grams ("dog bites" vs "man bites") recovers local order; contextual models recover it fully.

> [!question]- What TF-IDF weight does a word that occurs in every document get, and why is that sensible?
> $\log(N/N)=0$. A word present everywhere cannot help distinguish documents, so it should not influence similarity or classification.

> [!question]- Why does word2vec use negative sampling instead of a full softmax?
> The softmax normaliser sums over the entire vocabulary (often $10^5$+ words) for every training pair. Negative sampling replaces it with $K$ (≈5–20) binary logistic losses on random words, which is far cheaper and works well in practice.

> [!question]- How does fastText handle the misspelling "recieve"?
> It sums the vectors of the word's character n-grams (`<re`, `rec`, `eci`, …), most of which also occur in "receive", so the typo gets a vector close to the correct word.

> [!question]- Compute the cosine similarity of $(1,0)$ and $(1,1)$.
> $\frac{1}{1\cdot\sqrt2}\approx0.71$, an angle of 45°.

## Practice
[Text Representations - Exercises](Text%20Representations%20-%20Exercises.ipynb): BoW and TF-IDF by hand and in code (matching scikit-learn), cosine similarity, analogies, skip-gram pair counting, the negative-sampling gradient, the $3/4$-power noise distribution, fastText n-grams, PPMI + SVD embeddings, skip-gram training and mean-pooled sentence embeddings.

## Learn more
- [Jay Alammar — The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/)
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/) (lectures 1–2 cover word vectors)
- [Jurafsky & Martin — Vector Semantics and Embeddings chapter](https://web.stanford.edu/~jurafsky/slp3/)
- Papers: [word2vec](https://arxiv.org/abs/1301.3781) · [GloVe](https://nlp.stanford.edu/projects/glove/) · [fastText subword vectors](https://arxiv.org/abs/1607.04606) · [Sentence-BERT](https://arxiv.org/abs/1908.10084)
