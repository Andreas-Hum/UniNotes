---
tags: [ml, llm]
---
# Fine-tuning and Alignment

> [!summary] In one sentence
> Fine-tuning adapts a pretrained model to a task (cheaply, with adapters such as LoRA), and alignment (SFT, then RLHF or DPO on human preference pairs) steers it toward the answers people actually prefer, while a KL anchor to a reference model stops it drifting into nonsense.

## Intuition first
A pretrained base model is like a brilliant new hire who has read the whole internet but has never worked at *your* company: it knows a lot, but it does not know your format, your tone, or what "a good answer" means here. There are two separate jobs:

1. **Teach it the job** (fine-tuning): show examples of the inputs and outputs you want. The question is how many weights to change. Changing all of them is expensive and risks **catastrophic forgetting**; methods like **LoRA** change only a tiny, low-rank "correction" on top of frozen weights.
2. **Teach it taste** (alignment): for many prompts there is no single correct answer, but people can easily say which of two answers is *better*. Preference methods (RLHF, DPO) turn those comparisons into a training signal. A leash (the KL penalty, or the reference model inside DPO) keeps the model close to its sensible starting point, so it cannot "game" the reward with weird outputs.

Why does LoRA work at all? Empirically, the weight *change* needed to adapt a big model to a new task has low "intrinsic rank": it can be written as a product of two thin matrices, without losing much.

![LoRA: a frozen d×k matrix plus a thin trainable product BA, then merged](../../Attachments/ML%20Animations/Fine-tuning%20and%20Alignment%20-%20LoRA.gif)
*Watch how small the two orange matrices are next to the frozen $W_0$ (0.39 % of the parameters for $r=8$, $d=k=4096$), and how after training they merge back into one matrix, so inference costs nothing extra.*

## Methods at a glance
| Method | What changes | Notes |
|---|---|---|
| Full fine-tuning | all weights | expensive, risk of forgetting |
| **LoRA** | low-rank update $W+BA$, $r\ll d$ | [Hu et al. 2021](https://arxiv.org/abs/2106.09685); tiny adapters |
| QLoRA | LoRA on a 4-bit quantised base | [Dettmers et al. 2023](https://arxiv.org/abs/2305.14314) |
| Prefix / prompt tuning | learned soft prompts | very few parameters |
| SFT | supervised on instruction data | first alignment step |
| **RLHF** | reward model from preferences + PPO with KL penalty | [InstructGPT](https://arxiv.org/abs/2203.02155); see [[Q-Learning and Policy Gradients]] |
| **DPO** | direct loss on preference pairs, no RL loop | [Rafailov et al. 2023](https://arxiv.org/abs/2305.18290) |
| Distillation | train small model on big model's outputs | |

## The math, step by step

### LoRA
For a frozen weight $W_0\in\mathbb R^{d\times k}$, LoRA learns
$$W=W_0+\frac{\alpha}{r}BA,\qquad B\in\mathbb R^{d\times r},\ A\in\mathbb R^{r\times k},\ r\ll\min(d,k).$$
- $r$ is the rank of the update; $\alpha$ a scaling constant (so changing $r$ does not require re-tuning the learning rate).
- **Initialisation**: $B=0$ and $A$ random. Then $BA=0$ at the start, so training begins *exactly* at the pretrained model. (If both were zero, the gradients of both would be zero and nothing would learn.)
- **Parameter count**: $r(d+k)$ instead of $dk$.
- **Forward pass**: $y=xW_0^\top+\frac{\alpha}{r}\,xA^\top B^\top$; computing the two thin products is cheap.
- **Merging**: after training, compute $W_0+\frac{\alpha}{r}BA$ once and store a single matrix: no inference latency. Or keep several adapters and swap them per task.
- Why low rank is a sensible restriction: by the Eckart–Young theorem, the best rank-$r$ approximation of an update $\Delta W$ is its truncated SVD; if $\Delta W$'s singular values decay quickly, rank $r$ captures most of it.

### QLoRA and memory
Full fine-tuning with Adam in mixed precision costs about **16 bytes per parameter** (fp16 weights 2 + fp16 gradients 2 + fp32 master weights 4 + two fp32 Adam moments 8). For a 7B model that is ~112 GB, before activations. **QLoRA** stores the frozen base in 4-bit (NF4, ≈0.5 byte/param, ~3.5 GB for 7B) and trains only LoRA adapters in higher precision, so a 7B–13B model fits on one consumer GPU.

### Prefix / prompt tuning
Prepend $m$ trainable "virtual token" vectors to the input (prompt tuning) or to every layer's keys and values (prefix tuning). Only those vectors are learned: very few parameters, but usually weaker than LoRA on small models.

### SFT
Ordinary next-token cross-entropy on (instruction, response) pairs, usually computing the loss only on the response tokens.

### RLHF (InstructGPT recipe)
1. **SFT** on demonstrations.
2. **Reward model** $r_\phi(x,y)$ trained on human comparisons with the **Bradley–Terry** model
$$P(y_w\succ y_l\mid x)=\sigma\big(r_\phi(x,y_w)-r_\phi(x,y_l)\big),\qquad \mathcal L_{RM}=-\log\sigma\big(r_\phi(x,y_w)-r_\phi(x,y_l)\big).$$
Only *differences* of rewards matter, so the reward scale is arbitrary.
3. **RL (PPO)**: maximise the reward minus a KL penalty to the reference (SFT) policy,
$$\max_\theta\ \mathbb E_{y\sim\pi_\theta}\Big[r_\phi(x,y)-\beta\log\frac{\pi_\theta(y\mid x)}{\pi_{ref}(y\mid x)}\Big].$$
Without the KL term ($\beta=0$) the policy finds outputs that exploit the reward model's blind spots (**reward hacking**): repetitive, over-long or bizarre text the reward model happens to like, and it can collapse to one output (mode collapse). PPO itself is a policy-gradient method ([[Q-Learning and Policy Gradients]]).

**Closed-form optimum.** For a fixed prompt, the distribution that maximises $\sum_y\pi(y)r(y)-\beta\,\mathrm{KL}(\pi\,\|\,\pi_{ref})$ is
$$\pi^*(y)=\frac{1}{Z}\,\pi_{ref}(y)\exp\big(r(y)/\beta\big).$$
Large $\beta$ keeps $\pi^*$ near the reference; small $\beta$ concentrates on the highest-reward answer.

### DPO
Rearranging the optimum gives $r(y)=\beta\log\frac{\pi^*(y)}{\pi_{ref}(y)}+\beta\log Z$. Plug this into Bradley–Terry: the unknown $\beta\log Z$ cancels in the difference, and the reward model disappears. What remains is a supervised loss on the policy itself:

DPO loss: $-\log\sigma\Big(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\Big)$

In words: raise the log-probability of the preferred answer $y_w$ and lower that of the rejected $y_l$, **measured relative to the reference model**, with $\beta$ controlling how far you may move. No sampling, no reward model, no PPO.

### Distillation
The student matches the teacher's softened distribution:
$$\mathcal L=\tau^2\,\mathrm{KL}\big(\text{softmax}(z_t/\tau)\,\|\,\text{softmax}(z_s/\tau)\big)\ (+\text{ordinary label loss}).$$
A temperature $\tau>1$ reveals the teacher's "dark knowledge" (which wrong answers are *almost* right). The $\tau^2$ factor keeps gradient magnitudes comparable across temperatures. For LLMs, distillation often just means SFT on the big model's generated outputs.

## Worked example
**LoRA parameter count.** $d=k=1024$, $r=4$: full fine-tuning of this matrix trains $1024^2=1{,}048{,}576$ parameters; LoRA trains $4(1024+1024)=8{,}192$, i.e. $0.78\%$.

**Bradley–Terry.** Rewards $r(x,y_w)=1.0$, $r(x,y_l)=0.0$: $P(y_w\succ y_l)=\sigma(1)=0.73$ and the reward-model loss is $-\ln0.73=0.31$.

**DPO by hand.** $\beta=0.1$. Policy log-probs: $\log\pi_\theta(y_w)=-12$, $\log\pi_\theta(y_l)=-14$; reference: $\log\pi_{ref}(y_w)=-13$, $\log\pi_{ref}(y_l)=-13$.
- Implicit reward of $y_w$: $0.1\cdot(-12+13)=0.1$; of $y_l$: $0.1\cdot(-14+13)=-0.1$.
- Margin $0.2$, loss $=-\log\sigma(0.2)=-\ln0.55=0.60$.
The gradient pushes the margin up further (loss → 0 as the margin grows), but each step is weighted by $\sigma(-\text{margin})$: pairs that are already well ranked contribute little.

## Choosing a method
- **One GPU, big model, a few thousand domain examples** → QLoRA.
- **Many tasks on one base model** → one LoRA adapter per task, swap at serving time.
- **Fixed format or tone, plenty of demonstrations** → SFT (full or LoRA).
- **Preference data available, want simplicity and stability** → DPO.
- **Online feedback, a learned reward you trust, RL expertise** → RLHF with PPO.
- **Need a small fast model** → distil from a large one.

Tools: Hugging Face `transformers`, `peft`, `trl`. Back to [[LLMs Overview]].

## Common confusions
- **"LoRA makes inference slower."** → Only if you keep the adapter separate; merged, it is a single matrix again.
- **"Initialise both LoRA matrices randomly."** → Then $BA\neq0$ and you start from a *perturbed* model. $B=0$ starts exactly at $W_0$, and $A$ random lets gradients flow into $B$.
- **"DPO needs a reward model."** → The reward is implicit ($\beta\log\pi_\theta/\pi_{ref}$); only the policy and the frozen reference are needed.
- **"The KL penalty is just regularisation you could drop."** → It is what prevents reward hacking and keeps outputs fluent; $\beta$ is a key knob.
- **"Alignment teaches the model new facts."** → Mostly it changes *behaviour and style*; knowledge comes from pretraining (use RAG for new facts).

## Check yourself
> [!question]- Why is $B$ initialised to zero in LoRA, but not $A$?
> So the update $BA$ is zero at the start and the model begins exactly at its pretrained weights. If $A$ were also zero, the gradient w.r.t. $B$ (which depends on $A$) would be zero and training could not start.

> [!question]- What goes wrong in RLHF if $\beta=0$?
> Nothing anchors the policy to the reference, so it exploits flaws in the reward model (reward hacking), drifts into unnatural text and can collapse onto a few outputs.

> [!question]- In one sentence, how does DPO get rid of the reward model?
> The optimal KL-regularised policy implies $r=\beta\log(\pi^*/\pi_{ref})+\text{const}$; substituting into the Bradley–Terry likelihood makes the constant cancel, leaving a loss that depends only on the policy and the reference.

> [!question]- How many trainable parameters does LoRA with $r=8$ add to a $4096\times4096$ matrix?
> $8(4096+4096)=65{,}536$, about $0.39\%$ of the $16.8$M in the full matrix.

> [!question]- Why does distillation use a temperature $\tau>1$?
> It softens the teacher's distribution so the relative probabilities of wrong classes (which carry information about similarity) become visible to the student.

## Practice
[Fine-tuning and Alignment - Exercises](Fine-tuning%20and%20Alignment%20-%20Exercises.ipynb): choosing a method, the alignment pipeline, why the KL penalty, LoRA initialisation, parameter counts and memory budgets, Bradley–Terry, DPO by hand and vectorised, the closed-form RLHF optimum, LoRA forward pass and training, best rank-$r$ updates via SVD, and DPO on a toy policy.

## Learn more
- [LoRA — Hu et al. 2021](https://arxiv.org/abs/2106.09685) · [QLoRA — Dettmers et al. 2023](https://arxiv.org/abs/2305.14314)
- [InstructGPT](https://arxiv.org/abs/2203.02155) · [DPO — Rafailov et al. 2023](https://arxiv.org/abs/2305.18290)
- [Distilling the Knowledge in a Neural Network — Hinton et al. 2015](https://arxiv.org/abs/1503.02531)
- [Hugging Face PEFT docs](https://huggingface.co/docs/peft) · [Hugging Face TRL docs](https://huggingface.co/docs/trl)
- [Hugging Face blog — Illustrating RLHF](https://huggingface.co/blog/rlhf)
