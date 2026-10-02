---
tags: [ml, nlp, index]
---
# NLP Overview

> [!summary] In one sentence
> Natural language processing turns messy human text into numbers a model can learn from (normalise → tokenise → represent → model → task head), and then measures how good the resulting labels, spans or generated text are.

## Intuition first
A computer cannot "read" the string `"The movie was UNBELIEVABLE!!"`. All it can do is arithmetic on vectors. So every NLP system, from a 1990s spam filter to GPT, solves the same problem in the same order:

1. **Clean up** the text so irrelevant variation (capital letters, repeated punctuation, odd Unicode) does not create fake differences.
2. **Cut it into units** (tokens) from a fixed vocabulary, so each unit can get an ID.
3. **Turn IDs into vectors** that carry meaning ([[Text Representations]]).
4. **Run a model** over the sequence of vectors.
5. **Put a task head on top**: one label for the whole text, one label per token, a span, or a newly generated sequence.

An everyday analogy: translating a recipe for a robot chef. You first standardise the spelling ("tbsp" vs "tablespoon"), split it into steps, look each ingredient up in a catalogue (IDs), describe each ingredient by its properties (vectors), and finally the chef decides what to do (model + head).

Why does tokenisation deserve its own step? A word-level vocabulary cannot contain every word: "unbelievable", "unfollowable", typos, names. **Subword tokenisers** (BPE, WordPiece, SentencePiece) solve this by keeping frequent words whole and splitting rare words into frequent pieces (`un` + `believ` + `able`), so nothing is ever truly out-of-vocabulary.

![The NLP pipeline turning a sentence into a sentiment prediction](../../Attachments/ML%20Animations/NLP%20Overview%20-%20pipeline.gif)
*Watch the rare word "unbelievable" become three common subword pieces, each piece get an ID, and each ID get a vector before the model sees anything.*

## Pipeline
Text → normalisation → **tokenisation** (word, subword BPE/WordPiece/SentencePiece) → representation ([[Text Representations]]) → model → task head.

- **Normalisation** choices depend on the task. Lower-casing usually helps sentiment but hurts NER ("Apple" the company vs "apple" the fruit). Removing stop-words is dangerous for sentiment because standard lists contain *not*, *no*, *never*. Stemming merges "running/runs" but can also merge unrelated words.
- **Tokenisation**: *word* tokenisers split on whitespace/punctuation; *subword* tokenisers learn a vocabulary from data. BPE (byte-pair encoding) starts from characters and repeatedly merges the most frequent adjacent pair; WordPiece (BERT) picks merges by likelihood gain; SentencePiece works on raw text including spaces, so it needs no language-specific pre-tokeniser.
- **Representation**: sparse counts (bag-of-words, TF-IDF) or dense learned vectors (word2vec, contextual embeddings). See [[Text Representations]].
- **Model**: from [[Logistic Regression]] on TF-IDF, through [[RNN and LSTM]], to [[Transformers]].
- **Task head**: the small final layer that maps hidden states to the output type (see the table below).

## Tasks
| Task | Typical model |
|---|---|
| Text classification / sentiment | TF-IDF + [[Logistic Regression]] → fine-tuned BERT |
| Named entity recognition, POS tagging | CRF / BiLSTM-CRF → token classification transformer |
| Machine translation, summarisation | encoder–decoder [[Transformers]] (T5, BART) |
| Question answering | extractive (span) or generative ([[LLMs Overview]]) |
| Semantic search | sentence embeddings + ANN ([[RAG and Agents]]) |
| Language modelling | n-grams → [[RNN and LSTM]] → GPT |

A useful way to remember which architecture fits which task is to ask **what shape the output has**:
- one label per **sequence** (sentiment, topic) → encoder (BERT) + classification head on the pooled/[CLS] vector;
- one label per **token** (NER, POS) → encoder + a classifier on every token, often with BIO tags (`B-PER`, `I-PER`, `O`);
- a **span** of the input (extractive QA) → encoder + two heads predicting start and end positions;
- a **generated sequence** (translation, summarisation, chat) → encoder–decoder (T5, BART) or decoder-only (GPT).

## History in one line
n-gram LMs → word2vec/GloVe → seq2seq + attention → Transformer (2017) → BERT/GPT pretraining → instruction-tuned LLMs.

The story behind the line:
- **n-gram LMs** estimate $P(w_i\mid w_{i-n+1},\dots,w_{i-1})$ by counting. They are fast but cannot generalise to unseen word combinations.
- **word2vec/GloVe** (2013–14) gave every word a dense vector so that similar words get similar vectors.
- **seq2seq** RNNs compress the whole input into one fixed vector before decoding: a **bottleneck** for long sentences. **Attention** lets the decoder look back at every encoder state, weighting the relevant ones.
- The **Transformer** (2017) keeps only attention, so it trains in parallel and scales.
- **Pretraining** (BERT: masked LM; GPT: next-token prediction) on huge corpora, then fine-tuning, became the default. **Instruction tuning** and alignment turned GPT-style models into assistants ([[LLMs Overview]]).

## The math, step by step

**Language model.** A language model assigns a probability to a token sequence with the chain rule:
$$P(w_1,\dots,w_N)=\prod_{i=1}^{N}P(w_i\mid w_1,\dots,w_{i-1}).$$
An **n-gram** model approximates the history by the last $n-1$ tokens. For a **bigram** model the maximum-likelihood estimate is a ratio of counts:
$$P(w_i\mid w_{i-1})=\frac{c(w_{i-1},w_i)}{c(w_{i-1})}.$$
In words: of all the times we saw $w_{i-1}$, what fraction were followed by $w_i$?

**Smoothing.** Any unseen bigram gets probability 0, which makes a whole sentence impossible. **Add-one (Laplace)** smoothing pretends every bigram was seen once more:
$$P_{\text{Laplace}}(w_i\mid w_{i-1})=\frac{c(w_{i-1},w_i)+1}{c(w_{i-1})+V},$$
where $V$ is the vocabulary size (adding $V$ to the denominator keeps the probabilities summing to 1).

**Perplexity.** For a test sequence of $N$ predicted tokens,
$$\mathrm{PP}=\exp\Big(-\frac1N\sum_{i=1}^{N}\log P(w_i\mid w_{<i})\Big)=\Big(\prod_{i=1}^{N}P(w_i\mid w_{<i})\Big)^{-1/N}.$$
It is the exponentiated average negative log-likelihood (cross-entropy). Intuition: a perplexity of 20 means the model is, on average, as unsure as if it were choosing uniformly among 20 tokens. Lower is better, but **only comparable across models with the same tokeniser**, because the number of tokens $N$ differs (a BPE model predicts more, easier tokens than a word-level model on the same text).

**Classification metrics.** With true positives $TP$, false positives $FP$ and false negatives $FN$:
$$\text{precision}=\frac{TP}{TP+FP},\qquad \text{recall}=\frac{TP}{TP+FN},\qquad F_1=\frac{2\,\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}.$$
For NER these are computed at the **entity** level: a predicted entity counts only if both its span and type match exactly.

**BLEU** (translation) measures n-gram **precision** of the candidate against references. Each n-gram count is **clipped** at the maximum count in the reference (so "the the the" cannot farm credit), giving $p_n$. Then
$$\text{BLEU}=\text{BP}\cdot\exp\Big(\sum_{n=1}^{4}w_n\log p_n\Big),\qquad \text{BP}=\min\big(1,\,e^{1-r/c}\big),$$
with $w_n=\tfrac14$, reference length $r$ and candidate length $c$. The **brevity penalty** BP punishes candidates that are too short (precision alone would reward saying very little).

**ROUGE** (summarisation) is recall-oriented: ROUGE-1 recall = overlapping unigrams / unigrams in the reference. ROUGE-L uses the longest common subsequence.

**Word error rate** (speech recognition): $\text{WER}=\frac{S+D+I}{N}$, substitutions + deletions + insertions (the edit distance between hypothesis and reference) divided by the reference length $N$.

## Worked example
**A bigram LM by hand.** Corpus (each sentence wrapped in `<s> … </s>`):
`<s> we like tea </s>`, `<s> we like jam </s>`, `<s> they like tea </s>`.

Counts: $c(\text{<s>})=3$, $c(\text{<s> we})=2$, $c(\text{we})=2$, $c(\text{we like})=2$, $c(\text{like})=3$, $c(\text{like tea})=2$, $c(\text{tea})=2$, $c(\text{tea </s>})=2$.

Score the sentence "we like tea":
$$P=\underbrace{\tfrac23}_{P(\text{we}\mid\text{<s>})}\cdot\underbrace{\tfrac22}_{P(\text{like}\mid\text{we})}\cdot\underbrace{\tfrac23}_{P(\text{tea}\mid\text{like})}\cdot\underbrace{\tfrac22}_{P(\text{</s>}\mid\text{tea})}=\tfrac49.$$
Perplexity over the $N=4$ predicted tokens: $\mathrm{PP}=(4/9)^{-1/4}=2.25^{1/4}\approx1.22$. The model is barely "confused" on this sentence because it saw it in training.

**One BPE merge step.** Word counts: `l o w` ×5, `l o w e r` ×2, `n e w e s t` ×6, `w i d e s t` ×3. Count adjacent pairs, weighted by word frequency: `e s` appears $6+3=9$ times, `s t` 9, `l o` 7, `o w` 7, … The most frequent pair `e s` is merged into a new symbol `es`; recount; now `es t` (9) is merged into `est`. Repeating this a few thousand times produces a vocabulary where common words are single tokens and rare words decompose into familiar pieces.

## Evaluation
Accuracy/F1, BLEU, ROUGE, METEOR, BERTScore, perplexity, human evaluation, LLM-as-judge.

- **Accuracy / F1** for classification and tagging (use macro-F1 when classes are imbalanced).
- **BLEU** (precision-oriented, translation), **ROUGE** (recall-oriented, summarisation), **METEOR** (adds stemming and synonym matching) all reward surface n-gram overlap.
- **BERTScore** compares contextual embeddings token-by-token, so paraphrases get credit.
- **Perplexity** for language models (intrinsic, same-tokeniser comparisons only).
- **Human evaluation** is the gold standard for fluency, faithfulness and helpfulness but is slow and expensive; **LLM-as-judge** approximates it cheaply but inherits the judge model's biases (position, verbosity, self-preference).

Why overlap metrics can mislead: a perfect paraphrase ("the feline rested on the rug") gets low BLEU against "the cat sat on the mat", while a fluent output that negates the meaning ("the cat never sat on the mat") can still score high.

## Common confusions
- **"Removing stop-words always helps."** → For sentiment it can delete *not*, flipping "not good" into "good". Normalisation must match the task.
- **"Lower perplexity means a better model, full stop."** → Only with the same tokeniser and test set; changing vocabulary changes $N$ and the per-token difficulty.
- **"Subword tokenisation is just a speed trick."** → It is what removes out-of-vocabulary words and lets a model handle typos, morphology and new words.
- **"High BLEU = good translation."** → BLEU measures n-gram overlap, not meaning; always look at examples and, when it matters, use human or embedding-based evaluation.
- **"Attention was invented with the Transformer."** → Attention was added to RNN seq2seq models first (to fix the fixed-vector bottleneck); the Transformer's novelty was using *only* attention.

## Check yourself
> [!question]- Why does a plain RNN encoder–decoder struggle with long sentences, and how does attention help?
> The encoder must squeeze the entire input into one fixed-size vector, an information bottleneck that loses detail as length grows. Attention lets the decoder compute, at every output step, a weighted average over *all* encoder states, so it can look directly at the relevant input words.

> [!question]- A language model gives the tokens of a test sentence probabilities 0.5 and 0.5. What is its perplexity?
> $\mathrm{PP}=(0.5\cdot0.5)^{-1/2}=0.25^{-1/2}=2$. It is as uncertain as a fair coin flip at each step.

> [!question]- Which output shape and architecture fit named entity recognition?
> One label per **token** (BIO tags), so an encoder such as BERT with a token-classification head (historically a BiLSTM-CRF).

> [!question]- Why does BLEU need a brevity penalty?
> BLEU is precision-based. A one-word candidate that matches a reference word has precision 1. The penalty $\text{BP}=\min(1,e^{1-r/c})$ shrinks the score when the candidate is shorter than the reference.

> [!question]- What does add-one smoothing fix, and what does it cost?
> It stops unseen bigrams having probability 0 (which would make any sentence containing them impossible). The cost is that it moves a lot of probability mass to unseen events, which hurts when the vocabulary is large; better smoothers (Kneser–Ney, back-off) exist.

## Practice
[NLP Overview - Exercises](NLP%20Overview%20-%20Exercises.ipynb): normalisation choices, task heads, bigram LMs and smoothing, perplexity, entity-level F1, BLEU/ROUGE by hand, a regex tokeniser, BPE from scratch, WER via edit distance and sampling text from your own bigram model.

## Learn more
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
- [Jurafsky & Martin — *Speech and Language Processing* (free draft)](https://web.stanford.edu/~jurafsky/slp3/)
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Word2vec paper — Mikolov et al. 2013](https://arxiv.org/abs/1301.3781) · [BERT](https://arxiv.org/abs/1810.04805) · [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [BPE for NLP — Sennrich et al. 2016](https://arxiv.org/abs/1508.07909) · [BLEU — Papineni et al. 2002](https://aclanthology.org/P02-1040/)
- [3Blue1Brown — Neural networks series (incl. transformers and attention)](https://www.3blue1brown.com/topics/neural-networks)
