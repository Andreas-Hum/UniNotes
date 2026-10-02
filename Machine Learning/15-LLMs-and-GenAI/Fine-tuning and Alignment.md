---
tags: [ml, llm]
---
# Fine-tuning and Alignment

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

DPO loss: $-\log\sigma\Big(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\Big)$

Tools: Hugging Face `transformers`, `peft`, `trl`. Back to [[LLMs Overview]].
