---
tags: [ml, project, distillation, compression]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Knowledge Distillation

> [!summary] In one sentence
> Distill a 420k-parameter CNN teacher into a 17× smaller MLP student on Fashion-MNIST: implement the temperature-scaled KD loss, look at the teacher's dark knowledge, and find out when distillation helps a little (same labelled data) and when it helps a lot (teacher-labelled unlabelled data).

**Notebook:** [Project - Knowledge Distillation](Project%20-%20Knowledge%20Distillation.ipynb) · topic: [[Model Deployment and Serving]] · all projects: [[Projects Overview]]

## What you build
1. `kd_loss`: $T^2\,\mathrm{KL}(\text{softmax}(z_t/T)\,\|\,\text{softmax}(z_s/T))$.
2. `distill_loss`: $(1-\alpha)\,\mathrm{CE}+\alpha\,\mathcal L_{KD}$.

Given: the teacher (CNN trained on all 60k images, 89.3 % test accuracy), the student (784 → 32 → 10, 25k parameters) and the experiments.

## Reference results (solution, laptop CPU)
Student test accuracy (mean of 3 seeds where noted):

| student training | accuracy |
|---|---|
| hard labels, 2k labelled images | 80.8 % |
| KD T = 1, same 2k images | **82.1 %** |
| KD T = 4, α = 0.7 | 81.1 % |
| KD T = 8 | 79.1 % (worse than hard labels) |
| **KD on 2k + 30k unlabelled images, teacher soft labels** | **85.0 %** |
| upper bound: 60k true labels | 86.1 % |

Two lessons: on the same data the gain is modest and high temperatures hurt a student this small; the big win is letting the teacher label data you have no labels for.

## Check yourself
> [!question]- Why does a very small student prefer a low temperature here?
> High T asks the student to match the teacher's tiny probabilities on unlikely classes, detail a 25k-parameter MLP can't represent, so capacity is wasted on noise. Hinton et al. observed that much smaller students do best at intermediate/low temperatures.

> [!question]- Why multiply the KD loss by T²?
> The gradient of the softened cross-entropy w.r.t. the logits scales as 1/T²; multiplying by T² keeps the soft and hard terms balanced when you change T.

> [!question]- What does "distillation" mean for LLMs?
> Usually generating answers with a large model and fine-tuning a small one on them (sequence-level distillation), sometimes also matching token probabilities.

## Learn more
- [Hinton, Vinyals, Dean – Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)
- Theory: [[Fine-tuning and Alignment]] (Distillation section) · [[ML Formula Sheet]] §13

---
Back to [[00 - Machine Learning Index]].
