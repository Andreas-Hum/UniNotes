---
tags: [ml, project, object-detection]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - IoU and Non-Max Suppression

> [!summary] In one sentence
> Implement intersection-over-union and greedy non-max suppression, match torchvision exactly, and turn 51 noisy detections into one box per object.

**Notebook:** [Project - IoU and Non-Max Suppression](Project%20-%20IoU%20and%20Non-Max%20Suppression.ipynb) · topic: [[Object Detection]] · all projects: [[Projects Overview]]

## What you build
1. `iou`: one box vs. many.
2. `nms`: greedy suppression above an IoU threshold.

## Reference results (solution, laptop CPU)
| | boxes | precision | recall |
|---|---|---|---|
| raw detections | 51 | 0.06 | 1.00 |
| after NMS (IoU 0.5) | 9 | 0.33 | 1.00 |
| **after NMS + score > 0.5** | **3** | **1.00** | **1.00** |

Your NMS returns exactly the same indices as `torchvision.ops.nms`.

## Check yourself
> [!question]- What goes wrong with NMS in crowds?
> Two real people standing close produce boxes with IoU > threshold, so the lower-scoring true detection gets suppressed. Soft-NMS lowers its score instead of deleting it.

> [!question]- Why is IoU better than distance between box centres?
> It's scale-invariant and accounts for size and shape: a tiny box at the right centre still has low IoU with a large object.

---
Back to [[00 - Machine Learning Index]].
