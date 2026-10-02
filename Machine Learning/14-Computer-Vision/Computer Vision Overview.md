---
tags: [ml, vision, index]
---
# Computer Vision Overview

| Task | Output | Models |
|---|---|---|
| Classification | label | [[CNN]] (ResNet, EfficientNet, ConvNeXt), ViT |
| Object detection | boxes + labels | Faster R-CNN (two-stage), YOLO / SSD / DETR (one-stage) |
| Semantic segmentation | per-pixel class | U-Net, DeepLab |
| Instance segmentation | per-object mask | Mask R-CNN, SAM |
| Keypoints / pose | joint locations | OpenPose, HRNet |
| Image generation | image | GANs, diffusion ([[Generative Models]]) |
| Vision–language | caption / retrieval | CLIP, VLMs ([[LLMs Overview]]) |
| Self-supervised pretraining | features | SimCLR, MoCo, DINO, MAE |

## Metrics
Top-1/Top-5 accuracy, IoU, mAP@[.5:.95], Dice, FID.

## Practical toolbox
Data augmentation (flip, crop, colour jitter, mixup/cutmix), transfer learning from pretrained weights, mixed precision ([[Training Tricks]]). Libraries: torchvision, timm, Ultralytics, OpenCV, Albumentations.

## Resources
- [Stanford CS231n](https://cs231n.stanford.edu/) · [CS231n course notes](https://cs231n.github.io/)
- [Dive into Deep Learning — CV chapters](https://d2l.ai/)
- Papers: [ResNet](https://arxiv.org/abs/1512.03385) · [ViT](https://arxiv.org/abs/2010.11929) · [U-Net](https://arxiv.org/abs/1505.04597) · [YOLO](https://arxiv.org/abs/1506.02640) · [CLIP](https://arxiv.org/abs/2103.00020)
