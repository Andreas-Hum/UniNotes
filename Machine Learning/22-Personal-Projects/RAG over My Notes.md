---
tags: [ml, project, llm, rag]
status: not-started
notebook: not-started
level: I
reviewed:
---
# RAG over My Notes

> [!summary] In one sentence
> Turn this vault into a study chatbot: split notes by heading, find the right sections with keyword + multilingual embedding search, check retrieval on your own question set, and let Claude answer only from those sections, with clickable links back to the note.

**Notebook:** [RAG over My Notes - Notebook](RAG%20over%20My%20Notes%20-%20Notebook.ipynb) · part of [[Personal Projects]]

## Do I have enough notes?
**Yes.** RAG doesn't *train* on your notes, it *searches* them, so 10 notes already work. Today the corpus is 128 notes (ML + IT-ret) → 1,560 sections. The index is rebuilt every run and embeddings are cached by content hash, so a new lecture costs a few seconds. The one real limit is that it can only answer what's in your notes, and for exam prep that's a feature: a "the sources don't cover this" answer shows you a gap.

## Intuition first
An LLM alone answers from memory and can make things up. RAG is an open-book exam: first **retrieve** the relevant pages, then let the model **read and cite** them. Retrieval quality is everything: the model can't cite what it never sees.

## What you build (4 TODOs)
1. `chunk_markdown`: one chunk per heading, with a breadcrumb (`Note > Heading > Subheading`).
2. `rrf`: reciprocal rank fusion of TF-IDF and embedding rankings.
3. `build_prompt`: numbered sources + "answer only from these, cite [n], same language as the question".
4. `hit_at_k`: evaluate retrieval on a hand-made question set (Danish GDPR + English ML).

## Reference results (20 questions, 128 notes)
| retriever | hit@1 | hit@3 |
|---|---|---|
| TF-IDF (keywords) | 0.55 | 0.80 |
| multilingual-e5-small (embeddings) | 0.90 | 0.95 |
| hybrid (RRF) | 0.85 | 0.95 |

The one miss: *"What is the difference between a data controller and a data processor?"*, an **English** GDPR question that lands on English ML notes about data. The Danish version of the question works. Numbers shift as the vault grows: this very note now comes back for that English question, because it quotes it! Fixes to try are listed in the notebook (query translation, folder filters).

## Answers with an LLM
Set `ANTHROPIC_API_KEY` and `ask("Hvornår skal man udpege en DPO?")` returns an answer citing `[1]`, `[2]`… plus `obsidian://` links that open the exact note, and `[[Note#Heading]]` links to paste into your notes. Without a key you still get the ranked sources. The generation call was tested with a stand-in client; run it once with your key to see real answers.

## Common confusions
- **"Fine-tune the LLM on my notes instead"**: fine-tuning teaches style, not reliable facts, and you'd have to redo it for every new lecture. Retrieval is cheaper, updatable and citable.
- **Bigger chunks = better context**: too big and the embedding blurs many topics into one vector, so retrieval gets worse. Measure with hit@k.
- **Similarity ≠ answer**: the top chunk can be *about* the topic without answering the question. Check faithfulness, not just retrieval.

## Check yourself
> [!question]- Why fuse by rank (RRF) instead of adding the two similarity scores?
> TF-IDF cosine and embedding cosine live on different scales and distributions; adding them lets one dominate. Ranks are comparable, and RRF rewards documents that both retrievers place high.

> [!question]- Why does every chunk start with its breadcrumb?
> A section like "Undtagelser" means nothing on its own. The breadcrumb ("Lektion 3 > Art. 9 > Undtagelser") puts the context into both the TF-IDF terms and the embedding.

## Learn more
- [Wang et al. – Text Embeddings by Weakly-Supervised Contrastive Pre-training (E5)](https://arxiv.org/abs/2212.03533) · [model card](https://huggingface.co/intfloat/multilingual-e5-small)
- [IBM Technology – What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M)
- Vault: [[RAG and Agents]] · [[Text Representations]] · [[LLMs Overview]] · [[00 - IT-ret Oversigt]]
