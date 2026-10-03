---
tags: [ml, project, lora, fine-tuning]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - LoRA from Scratch

> [!summary] In one sentence
> Write a LoRA layer (frozen weight + trainable low-rank update), adapt a digit classifier pretrained on 0–4 to digits 5–9, and compare accuracy per trainable parameter with full fine-tuning and head-only training.

**Notebook:** [Project - LoRA from Scratch](Project%20-%20LoRA%20from%20Scratch.ipynb) · topic: [[Fine-tuning and Alignment]] · all projects: [[Projects Overview]]

## What you build
1. `LoRALinear.forward`: $W_0x + \frac{\alpha}{r}BAx$ with B initialised to zero.
2. `n_trainable`: count trainable parameters.

## Reference results (solution, laptop CPU)
| method | accuracy on 5–9 | trainable params |
|---|---|---|
| full fine-tune | 98.1 % | 85,002 (100 %) |
| last layer only | 73.6 % | 2,570 (3.0 %) |
| LoRA r = 1 | 85.9 % | 1,098 (1.3 %) |
| **LoRA r = 4** | **95.9 %** | **4,392 (5.2 %)** |
| LoRA r = 16 | 95.5 % | 17,568 (20.7 %) |

All adapted models forget 0–4 (the head is retrained on 5–9 only), but the LoRA base weights are untouched: remove the adapter and the original is back.

## Check yourself
> [!question]- Why initialise B to zero?
> Then BA = 0 and the adapted model starts exactly as the pretrained one; training only moves away from it as needed.

> [!question]- Why does a low-rank update work at all?
> Fine-tuning updates tend to have low intrinsic rank: adapting to a related task needs only a few new directions in weight space.

## Learn more
- [Hu et al. – LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

---
Back to [[00 - Machine Learning Index]].
