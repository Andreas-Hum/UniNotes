---
tags: [ml, llm]
---
# RAG and Agents

## Retrieval-Augmented Generation
1. Chunk documents → embed ([[Text Representations]]) → store in a vector index (FAISS, pgvector…).
2. At query time: retrieve top-k (dense + BM25 hybrid), optionally rerank with a cross-encoder.
3. Put retrieved passages in the prompt; generate with citations.
Evaluation: retrieval recall@k, answer faithfulness/groundedness.
Paper: [Lewis et al. 2020](https://arxiv.org/abs/2005.11401).

## Agents
LLM in a loop: think → call a **tool** (search, code, API) → observe → repeat. Patterns: ReAct ([Yao et al. 2022](https://arxiv.org/abs/2210.03629)), planning, memory, multi-agent. Key concerns: reliability, cost, evaluation, prompt injection.

Back to [[LLMs Overview]]. Retrieval is closely related to two-tower recommenders ([[Deep Learning Recommenders]]).
