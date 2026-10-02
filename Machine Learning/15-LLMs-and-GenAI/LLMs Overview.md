---
tags: [ml, llm, index]
---
# LLMs Overview

Large language models are decoder-only [[Transformers]] trained on next-token prediction at scale.

## Lifecycle
1. **Pretraining** — trillions of tokens, causal LM loss $-\sum_t\log p(x_t\mid x_{<t})$.
2. **Supervised fine-tuning (SFT)** — instruction/response pairs.
3. **Preference alignment** — RLHF (reward model + PPO), DPO, constitutional/RLAIF ([[Fine-tuning and Alignment]]).
4. **Inference** — decoding (greedy, beam, temperature, top-k, top-p), KV cache, quantisation, speculative decoding.
5. **Applications** — prompting, [[RAG and Agents]], tool use, coding assistants.

## Key ideas
- **Scaling laws** (Kaplan 2020; Chinchilla, Hoffmann 2022): loss falls as a power law in parameters, data and compute; balance tokens ≈ 20 × parameters.
- **In-context learning**: few-shot examples in the prompt; chain-of-thought prompting.
- **Tokenisation** (BPE) shapes what the model sees.
- **Mixture of experts**: sparse activation for bigger capacity.
- **Multimodality**: image/audio encoders feeding the LM.

## Evaluation
Perplexity, benchmarks (MMLU, GSM8K, HumanEval…), human preference, LLM-as-judge; beware contamination.

## Resources
- [Karpathy — Neural Networks: Zero to Hero (build GPT)](https://karpathy.ai/zero-to-hero.html)
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
- [Lilian Weng's blog](https://lilianweng.github.io/)
- [Jurafsky & Martin — LLM chapters](https://web.stanford.edu/~jurafsky/slp3/)
- Papers: [GPT-3](https://arxiv.org/abs/2005.14165) · [Scaling laws](https://arxiv.org/abs/2001.08361) · [Chinchilla](https://arxiv.org/abs/2203.15556) · [InstructGPT/RLHF](https://arxiv.org/abs/2203.02155)
