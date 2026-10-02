---
tags: [ml, nlp, index]
---
# NLP Overview

## Pipeline
Text → normalisation → **tokenisation** (word, subword BPE/WordPiece/SentencePiece) → representation ([[Text Representations]]) → model → task head.

## Tasks
| Task | Typical model |
|---|---|
| Text classification / sentiment | TF-IDF + [[Logistic Regression]] → fine-tuned BERT |
| Named entity recognition, POS tagging | CRF / BiLSTM-CRF → token classification transformer |
| Machine translation, summarisation | encoder–decoder [[Transformers]] (T5, BART) |
| Question answering | extractive (span) or generative ([[LLMs Overview]]) |
| Semantic search | sentence embeddings + ANN ([[RAG and Agents]]) |
| Language modelling | n-grams → [[RNN and LSTM]] → GPT |

## History in one line
n-gram LMs → word2vec/GloVe → seq2seq + attention → Transformer (2017) → BERT/GPT pretraining → instruction-tuned LLMs.

## Evaluation
Accuracy/F1, BLEU, ROUGE, METEOR, BERTScore, perplexity, human evaluation, LLM-as-judge.

## Resources
- [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
- [Jurafsky & Martin — *Speech and Language Processing* (free draft)](https://web.stanford.edu/~jurafsky/slp3/)
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Word2vec paper — Mikolov et al. 2013](https://arxiv.org/abs/1301.3781) · [BERT](https://arxiv.org/abs/1810.04805) · [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
