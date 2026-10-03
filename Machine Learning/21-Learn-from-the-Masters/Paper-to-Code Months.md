---
tags: [ml, masters, papers]
status: not-started
level: I
reviewed:
---
# Paper-to-Code Months

> [!summary] In one sentence
> Once a month, reproduce the main result of one classic paper in a small notebook. Then write half a page on what held up, what didn't, and what the paper left out. Re-deriving a famous result yourself is the quickest cure for "I only know this from slides".

**Why this works:** reading a paper tells you *what* the authors claim. Re-implementing it tells you *why* each design choice is there. Every notebook below reproduces one headline claim at laptop scale (1–3 min on a CPU), so the whole loop fits in a weekend.

## The four months

| Month | Paper | Claim you reproduce | Notebook | Background |
|---|---|---|---|---|
| 1 | **ResNet** – He et al. 2015 ([arXiv](https://arxiv.org/abs/1512.03385)) | deeper plain nets train *worse*; identity shortcuts fix it | [Paper-to-Code 1 - ResNet](Paper-to-Code%201%20-%20ResNet.ipynb) | [[CNN Architectures]], [[Backpropagation]] |
| 2 | **word2vec** – Mikolov et al. 2013 ([arXiv](https://arxiv.org/abs/1301.3781), [neg. sampling](https://arxiv.org/abs/1310.4546)) | predicting neighbours gives vectors where analogies are directions | [Paper-to-Code 2 - word2vec](Paper-to-Code%202%20-%20word2vec.ipynb) | [[Text Representations]] |
| 3 | **LightGCN** – He et al. 2020 ([arXiv](https://arxiv.org/abs/2002.02126)) | a GCN with no weights and no nonlinearity beats MF for recommendation | [Paper-to-Code 3 - LightGCN](Paper-to-Code%203%20-%20LightGCN.ipynb) | [[Graph Neural Networks]], [[Collaborative Filtering and Matrix Factorization]] |
| 4 | **DDPM** – Ho et al. 2020 ([arXiv](https://arxiv.org/abs/2006.11239)) | predicting noise with an MSE loss gives a working generative model | [Paper-to-Code 4 - DDPM](Paper-to-Code%204%20-%20DDPM.ipynb) | [[Generative Models]] |

The order runs from vision to NLP to recommender systems to generative models, and each one connects to a course you have taken. After month 4, choose the next paper yourself (see *Picking the next paper* below).

### What each notebook contains
- The paper's claim in one quote-box, plus exactly what was scaled down and why.
- 2–4 **TODO** functions (the heart of the paper, never boilerplate), each with a ✅ check that tests it on a tiny hand-computable case.
- Experiment cells that unlock once the checks pass. They reproduce the claim and end in a ✅/❌ verdict.
- Hidden ▶ solutions, a *Scale it up* list for when you have a GPU, and a **write-up** cell.

### Reference results (what the solution gets on a CPU)

| Notebook | Result with the reference solution |
|---|---|
| ResNet | after 5 epochs, training loss: plain-8 **1.55**, plain-32 **1.98** (degradation), ResNet-32 **1.81**; first-layer gradient at init is 3,900× larger at depth 56 than at depth 8 for the plain net vs 36× for the ResNet |
| word2vec | neighbours of *three* = four, two, six, five, seven, eight; **5/12** analogies right after 1 epoch on 4M tokens |
| LightGCN | test NDCG@10 (sampled, same split as [[Project - MovieLens Recommender]]): MF-BPR **0.472** → LightGCN K=3 **0.504** |
| DDPM | sample→data distance **0.032**, data→sample **0.024** (pure noise: 0.246) |

Your numbers can differ a little if your implementation differs, because random draws happen in a different order. The checks have slack for that.

## The monthly rhythm (≈ 4 evenings)
1. **Read** (week 1): fill in a [[Paper Reading Template]]. Find the *one* figure or table that carries the claim.
2. **Implement** (week 2): do the TODOs without looking at the solution. Get every ✅.
3. **Poke** (week 3): run one item from *Scale it up*, or one ablation you came up with yourself. This is where you learn the most.
4. **Write up** (week 4): fill in the write-up cell and paste it into the log below. Keep it to half a page.

## Write-up template
```markdown
### <Paper> – <month>
- **Claim:** 
- **What I implemented / scaled down:** 
- **Result:** | setting | metric | paper | me |
- **Did it hold? Why / why not?** 
- **What the paper glossed over:** 
- **Next, with a GPU:** 
```

## Results log
*(Append one entry per month.)*

## Picking the next paper
Good candidates have one clear, checkable claim and a small-scale version that runs in minutes:
- **Attention Is All You Need** ([arXiv:1706.03762](https://arxiv.org/abs/1706.03762)): a 2-layer transformer on a copy/reverse task ([[Transformers]]).
- **Batch Normalization** ([arXiv:1502.03167](https://arxiv.org/abs/1502.03167)): faster training with higher learning rates on a small CNN ([[Training Tricks]]).
- **Dropout** ([JMLR 2014](https://jmlr.org/papers/v15/srivastava14a.html)): less overfitting on a small MLP.
- **SimCLR** ([arXiv:2002.05709](https://arxiv.org/abs/2002.05709)): contrastive pre-training on CIFAR-10 subsets ([[Self-Supervised and Contrastive Learning]]).
- **DQN** ([arXiv:1312.5602](https://arxiv.org/abs/1312.5602)): Atari from pixels, scaled down to a small grid game ([[Q-Learning and Policy Gradients]]).

See also [[Implement From Scratch]] for more build-it-yourself ideas, and [[Explain-it Videos]] for the teaching half of *Learn from the masters*.

---
Back to [[00 - Machine Learning Index]].
