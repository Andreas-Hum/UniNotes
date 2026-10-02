---
tags: [ml, llm, index]
---
# LLMs Overview

> [!summary] In one sentence
> Large language models are decoder-only [[Transformers]] trained to predict the next token on trillions of tokens, then fine-tuned and aligned to follow instructions, and finally sampled one token at a time at inference.

## Intuition first
Large language models are decoder-only [[Transformers]] trained on next-token prediction at scale.

That one sentence hides a surprisingly powerful idea. To guess the next word of *"The capital of France is …"* you need facts; for *"2 + 3 × 4 = …"* you need arithmetic; for *"…and so the detective realised the butler was…"* you need to follow a story. **Next-token prediction is a task that rewards learning almost everything about text**, and it needs no human labels: every position of every document is a free training example (self-supervision).

A useful picture is **autocomplete on a phone, scaled up a millionfold**. The model reads the text so far, outputs a probability for every token in its vocabulary, one token is picked, appended, and the loop repeats. Everything people call "chatting", "reasoning" or "writing code" is this loop. What makes it useful as an assistant is the later training stages (fine-tuning and alignment), which change *which* continuations the model prefers.

![Next-token probabilities reshaped by temperature, then one token is sampled and appended](../../Attachments/ML%20Animations/LLMs%20Overview%20-%20temperature%20sampling.gif)
*Watch the bars sharpen as $T$ drops (almost always "mat") and flatten as $T$ rises (even "moon" gets a real chance); then one token is sampled and appended to the prompt.*

## Lifecycle
1. **Pretraining** — trillions of tokens, causal LM loss $-\sum_t\log p(x_t\mid x_{<t})$.
2. **Supervised fine-tuning (SFT)** — instruction/response pairs.
3. **Preference alignment** — RLHF (reward model + PPO), DPO, constitutional/RLAIF ([[Fine-tuning and Alignment]]).
4. **Inference** — decoding (greedy, beam, temperature, top-k, top-p), KV cache, quantisation, speculative decoding.
5. **Applications** — prompting, [[RAG and Agents]], tool use, coding assistants.

What each stage contributes:
- **Pretraining** gives knowledge and language skill; it is by far the most expensive stage. The result is a *base model* that continues text but does not reliably follow instructions.
- **SFT** teaches the format "instruction → helpful answer" from (tens of) thousands of demonstrations.
- **Preference alignment** uses comparisons ("answer A is better than B") to push the model toward helpful, honest, harmless answers ([[Fine-tuning and Alignment]]).
- **Inference** engineering makes generation affordable: caching, quantisation (8/4-bit weights), and **speculative decoding** (a small draft model proposes several tokens, the big model verifies them in one pass).

## The math, step by step

**Causal LM loss.** For a token sequence $x_1,\dots,x_T$:
$$\mathcal L=-\sum_{t=1}^{T}\log p_\theta(x_t\mid x_{<t}).$$
Each term is the cross-entropy between the model's predicted distribution and the true next token. The **causal mask** in self-attention guarantees position $t$ only sees $x_{<t}$, so all $T$ predictions are computed in one parallel forward pass during training. The **perplexity** is $\exp(\mathcal L/T)$.

**Causal self-attention.** With queries $Q$, keys $K$, values $V$ (one row per position):
$$\text{Attn}(Q,K,V)=\text{softmax}\Big(\frac{QK^\top}{\sqrt{d_k}}+M\Big)V,\qquad M_{ij}=\begin{cases}0 & j\le i\\-\infty & j>i\end{cases}$$
The mask $M$ sets attention to future positions to zero after the softmax.

**From logits to a token.** The last layer outputs logits $z\in\mathbb R^{V}$. Sampling uses
$$p_i=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}.$$
- **Temperature** $T$: $T\to0$ approaches greedy (all mass on the arg-max); $T=1$ is the model's own distribution; $T>1$ flattens it (more diverse, more mistakes).
- **Greedy**: always take the arg-max. Deterministic, can be repetitive.
- **Beam search**: keep the $b$ best partial sequences by total log-probability. Good for translation where there is one "right" answer; bland for open-ended text.
- **Top-k**: keep only the $k$ most likely tokens, renormalise, sample.
- **Top-p (nucleus)**: keep the smallest set of tokens whose cumulative probability is $\ge p$, renormalise, sample. Unlike top-k, the set adapts: small when the model is confident, large when it is unsure.

**KV cache.** During generation, the keys and values of past tokens never change, so they are cached and only the new token's query/key/value are computed. The cache costs, per token,
$$2\ (\text{K and V})\times L\ (\text{layers})\times d\ (\text{model width})\times\text{bytes per number}.$$

**Parameter count.** Each decoder block has $W_Q,W_K,W_V,W_O\in\mathbb R^{d\times d}$ ($4d^2$) and an FFN $d\to4d\to d$ ($8d^2$), so about $12d^2$ parameters per block, $\approx12Ld^2$ in total plus the embedding matrix ($Vd$).

**Scaling laws.**
- Kaplan's form for model size: $L(N)=(N_c/N)^{\alpha_N}$, a straight line on a log–log plot.
- Training compute is approximately $C\approx6ND$ FLOPs ($N$ parameters, $D$ tokens; 2 for the forward pass, 4 for the backward pass). Chinchilla's finding: for a fixed $C$, grow $N$ and $D$ together, with $D\approx20N$. Many earlier models (e.g. GPT-3) were too big for their data.

## Worked example
**Loss and perplexity.** A model gives the true next tokens probabilities $0.5$ and $0.125$. Loss $=-\ln0.5-\ln0.125=0.693+2.079=2.77$ nats; mean $1.386$; perplexity $e^{1.386}=4$ (the geometric mean of $1/0.5=2$ and $1/0.125=8$).

**Temperature.** Logits $z=(1,0)$. At $T=1$: $p_1=e/(e+1)=0.73$. At $T=0.5$ the logits become $(2,0)$: $p_1=e^2/(e^2+1)=0.88$. At $T=2$ they become $(0.5,0)$: $p_1=0.62$. Lower $T$ sharpens, higher $T$ flattens.

**Top-p.** Sorted probabilities $(0.6,0.25,0.1,0.05)$ with $p=0.8$: cumulative sums $0.6, 0.85, \dots$, so the nucleus is the first two tokens, renormalised to $(0.71,0.29)$.

**Chinchilla budget.** A 1B-parameter model should see $D\approx20\times10^9=2\times10^{10}$ tokens, costing $C\approx6\cdot10^9\cdot2\cdot10^{10}=1.2\times10^{20}$ FLOPs.

**KV cache.** $L=24$ layers, $d=2048$, fp16 (2 bytes): $2\cdot24\cdot2048\cdot2=196{,}608$ bytes ≈ 192 KiB per token, so a 4096-token context needs ≈ 0.75 GiB *per sequence*. This is why long contexts and big batches are memory-bound.

## Key ideas
- **Scaling laws** (Kaplan 2020; Chinchilla, Hoffmann 2022): loss falls as a power law in parameters, data and compute; balance tokens ≈ 20 × parameters.
- **In-context learning**: few-shot examples in the prompt; chain-of-thought prompting. The weights do **not** change: the examples only condition the forward pass. Chain-of-thought ("let's think step by step") makes the model write intermediate steps, which gives it more computation per answer.
- **Tokenisation** (BPE) shapes what the model sees. Letters inside a token are invisible to it, which is why counting characters or reversing words can be surprisingly hard; numbers split into odd chunks hurt arithmetic. See [[NLP Overview]].
- **Mixture of experts**: sparse activation for bigger capacity. Each dense FFN is replaced by several expert FFNs plus a router that sends each token to the top-$k$ experts. With 8 experts and top-2 routing, FFN parameters grow 8× but compute per token only ~2×.
- **Multimodality**: image/audio encoders feeding the LM. An image encoder turns patches into vectors that are projected into the LM's token-embedding space, so the LM "reads" them like tokens.

## Evaluation
Perplexity, benchmarks (MMLU, GSM8K, HumanEval…), human preference, LLM-as-judge; beware contamination.

- **MMLU**: multiple-choice knowledge across 57 subjects. **GSM8K**: grade-school maths word problems. **HumanEval**: write Python functions that pass unit tests (pass@k).
- **Human preference** (pairwise comparisons, Elo-style leaderboards) captures helpfulness that benchmarks miss.
- **Contamination**: if benchmark questions leaked into the pretraining data, scores measure memorisation, not ability. Mitigations: held-out or freshly written test sets, n-gram overlap checks, canary strings.

## Common confusions
- **"The model looks things up in a database."** → A plain LLM only has what is stored in its weights; for fresh or private facts you add retrieval ([[RAG and Agents]]).
- **"Few-shot prompting is a kind of training."** → No gradient step happens; it is conditioning. Fine-tuning changes the weights.
- **"Temperature 0 makes the model correct."** → It makes it *deterministic* (greedy). Greedy can still be wrong, and can loop.
- **"Bigger is always better."** → For a fixed compute budget, a smaller model trained on more tokens (Chinchilla) beats a bigger under-trained one, and is cheaper to serve.
- **"MoE with 8 experts costs 8× compute."** → Only the routed experts run per token, so compute grows with $k$, not with the number of experts; memory still grows with all of them.

## Check yourself
> [!question]- Why can a transformer compute the loss for all positions of a training sequence in one pass, but must generate one token at a time?
> During training the whole sequence is known, and the causal mask stops each position from seeing the future, so all next-token predictions are made in parallel. At generation time token $t+1$ does not exist until token $t$ has been sampled.

> [!question]- What is the difference between top-k and top-p sampling?
> Top-k always keeps a fixed number $k$ of tokens. Top-p keeps the smallest set whose cumulative probability reaches $p$, so the number of candidates adapts to the model's confidence.

> [!question]- Roughly how many tokens should a 7B-parameter model be trained on under the Chinchilla rule?
> $D\approx20N=140$B tokens. (Modern models often train far longer than this because inference cost, not training cost, dominates.)

> [!question]- What does the KV cache save, and what does it cost?
> It avoids recomputing keys and values of all previous tokens at every generation step (turning quadratic recomputation into linear work per step). It costs memory: $2\cdot L\cdot d\cdot$ bytes per token per sequence.

> [!question]- What is benchmark contamination and why does it matter?
> Test questions (or their answers) appearing in the training data. Scores then overestimate generalisation, so comparisons between models become misleading.

## Practice
[LLMs Overview - Exercises](LLMs%20Overview%20-%20Exercises.ipynb): next-token loss and perplexity, temperature, top-k/top-p by hand and in code, Chinchilla budgets, counting transformer parameters, KV-cache memory, causal attention, incremental decoding with a KV cache, greedy vs beam search and fitting a scaling law.

## Learn more
- [Karpathy — Neural Networks: Zero to Hero (build GPT)](https://karpathy.ai/zero-to-hero.html)
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
- [Lilian Weng's blog](https://lilianweng.github.io/)
- [Jurafsky & Martin — LLM chapters](https://web.stanford.edu/~jurafsky/slp3/)
- Papers: [GPT-3](https://arxiv.org/abs/2005.14165) · [Scaling laws](https://arxiv.org/abs/2001.08361) · [Chinchilla](https://arxiv.org/abs/2203.15556) · [InstructGPT/RLHF](https://arxiv.org/abs/2203.02155)
- [3Blue1Brown — Neural networks series (GPT and attention chapters)](https://www.3blue1brown.com/topics/neural-networks)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
