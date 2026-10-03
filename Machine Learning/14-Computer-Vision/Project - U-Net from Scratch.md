---
tags: [ml, project, segmentation, unet]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - U-Net from Scratch

> [!summary] In one sentence
> Build a U-Net (encoder, decoder, skip connections), train it with cross-entropy + soft Dice to segment circles, squares and triangles in noisy images, and measure what the skip connections buy: sharper boundaries.

**Notebook:** [Project - U-Net from Scratch](Project%20-%20U-Net%20from%20Scratch.ipynb) · topic: [[Image Segmentation]] · all projects: [[Projects Overview]]

## What you build
1. `dice_loss`: multi-class soft Dice over the foreground classes.
2. `UNet.forward`: two down stages, bottleneck, two up stages with `torch.cat` skip connections (or without, for the ablation).
3. `mean_iou`: per-class IoU averaged over the foreground classes.

## Reference results (solution, laptop CPU)
800 synthetic 64×64 training images, 20 epochs each (≈ 1.5 min CPU). 87.8 % of pixels are background, so pixel accuracy is nearly useless.

| model | mIoU | pixel acc | boundary acc (±2 px) |
|---|---|---|---|
| **U-Net (skips)** | **0.905** | 0.993 | **0.960** |
| same net, no skips | 0.896 | 0.991 | 0.942 |

The skip connections cut boundary errors from 5.8 % to 4.0 %: the decoder gets back the fine detail that pooling threw away.

## Check yourself
> [!question]- Why is the mIoU gap small while the boundary gap is large?
> Most of a shape's pixels are in its interior, which the coarse bottleneck features already classify well. Skip connections mainly fix the thin band of pixels at the edges, which mIoU dilutes.

> [!question]- Why combine cross-entropy with Dice?
> Cross-entropy gives smooth per-pixel gradients from the start; Dice directly optimises overlap and ignores the huge number of easy background pixels.

## Learn more
- [Ronneberger, Fischer, Brox – U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

---
Back to [[00 - Machine Learning Index]].
