---
tags: [ml, vision, index]
---
# Computer Vision Overview

> [!summary] In one sentence
> Computer vision tasks differ mainly in *what the output looks like* (one label, a set of boxes, a label per pixel, a mask per object, keypoints, a new image, text), and each output type comes with its own model family, its own augmentation rules and its own metric such as top-k accuracy, IoU, mAP, Dice or FID.

## Intuition first

Show a photo of a street to a person and ask different questions:

1. "What is this a picture of?" → *a street* (**classification**: one label per image).
2. "Where are the cars?" → draw a rectangle around each (**object detection**: boxes + labels).
3. "Colour every road pixel grey and every car pixel red" (**semantic segmentation**: a class per pixel, all cars share one colour).
4. "Colour each car differently" (**instance segmentation**: a separate mask per object).
5. "Where are the pedestrian's elbows and knees?" (**keypoints / pose**).

Same image, increasingly detailed outputs. Most modern systems share the same backbone (a [[CNN]] or a Vision Transformer that turns the image into feature maps or tokens) and differ in the **head** that turns features into the required output, and in how the result is scored.

Scoring needs care because outputs are geometric. A predicted box is never pixel-perfect, so "is this detection correct?" becomes "does it overlap the true box enough?". That overlap measure, **IoU**, is the backbone of detection and segmentation metrics.

![A predicted box sliding onto a ground-truth box while IoU and the true/false-positive verdict update](../../Attachments/ML%20Animations/Computer%20Vision%20Overview%20-%20IoU.gif)

*Watch the yellow intersection grow while the union shrinks: a box that looks "pretty close" still scores only $0.49$ and counts as a false positive at the usual $0.5$ threshold; a perfect match gives $1.00$.*

## Tasks at a glance

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

### What is behind each row

- **Classification**: backbone → global pooling → linear layer → softmax over classes. **ViT** instead cuts the image into $P\times P$ patches, flattens and linearly embeds each one as a token (a $224\times224$ image with $16\times16$ patches gives $14\times14=196$ tokens) and runs a [[Transformers|Transformer]] encoder.
- **Detection, two-stage** (Faster R-CNN): stage 1, a region proposal network suggests a few hundred candidate boxes; stage 2 classifies each candidate and refines its coordinates. Accurate but slower.
- **Detection, one-stage** (YOLO, SSD): predict class scores and box offsets densely, for every cell of a grid (and several anchor shapes), in one forward pass. Fast enough for video. Dense prediction produces many overlapping boxes for the same object, so they need **non-maximum suppression (NMS)**: keep the highest-scoring box, delete all remaining boxes that overlap it with IoU above a threshold, repeat.
- **DETR** treats detection as set prediction with a Transformer: a fixed number of learned queries each output one box or "no object", matched one-to-one to ground truth, so no NMS is needed.
- **Semantic segmentation**: an encoder–decoder. **U-Net** downsamples to capture context, upsamples back to full resolution, and uses skip connections to copy fine detail from encoder to decoder. **DeepLab** uses dilated (atrous) convolutions to grow the receptive field without losing resolution.
- **Instance segmentation**: **Mask R-CNN** = Faster R-CNN + a small mask head per detected box. **SAM** (Segment Anything) is a promptable model: given a point or a box, it returns a mask for whatever object is there.
- **Keypoints**: predict one heatmap per joint and take its peak (HRNet keeps high-resolution features throughout; OpenPose also links joints into skeletons for many people).
- **Vision–language**: **CLIP** trains image and text encoders contrastively so matching pairs embed close together, which enables zero-shot classification ("a photo of a {class}") and retrieval; VLMs feed image tokens into an LLM.
- **Self-supervised pretraining**: learn features from unlabelled images, see [[Self-Supervised and Contrastive Learning]].

## The math, step by step: metrics

Metrics: Top-1/Top-5 accuracy, IoU, mAP@[.5:.95], Dice, FID.

**Top-1 / Top-5 accuracy.** Top-1: the highest-scoring class is correct. Top-5: the correct class is among the five highest. Top-5 is forgiving on datasets with 1000 fine-grained classes (several dog breeds look alike). Random guessing on 1000 classes gives top-1 $0.1\%$ and top-5 $0.5\%$.

**IoU (Intersection over Union)** of two boxes or masks $A,B$:

$$\mathrm{IoU}=\frac{|A\cap B|}{|A\cup B|},\qquad |A\cup B|=|A|+|B|-|A\cap B|$$

For boxes $(x_1,y_1,x_2,y_2)$ the intersection is $\max(0,\min(x_2^A,x_2^B)-\max(x_1^A,x_1^B))$ times the same expression in $y$. IoU is 1 for a perfect match, 0 for no overlap, and it is scale-invariant: a 5-pixel error matters more on a small object than on a large one.

**Dice** (common in medical segmentation):

$$\mathrm{Dice}=\frac{2|A\cap B|}{|A|+|B|}=\frac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}$$

It is a monotone transform of IoU (same ranking of models) but always at least as large, and it equals the F1 score of pixel classification.

**Precision, recall and AP for detection.**

1. Sort all detections of one class by confidence.
2. Walk down the list. A detection is a **TP** if it matches a not-yet-matched ground-truth object with IoU $\ge$ threshold, otherwise an **FP**.
3. After each detection compute precision $=\frac{\text{TP so far}}{\text{detections so far}}$ and recall $=\frac{\text{TP so far}}{\#\text{ground truth}}$.
4. **AP** is the area under the precision–recall curve (after making precision non-increasing, the "envelope").
5. **mAP** averages AP over classes.

**mAP@[.5:.95]** (the COCO metric) also averages over 10 IoU thresholds $0.50,0.55,\dots,0.95$, so it rewards precise localisation, not just finding the object. PASCAL VOC's older mAP@0.5 uses only the first threshold.

**FID** compares the feature statistics of generated and real images; lower is better (see [[Generative Models]]).

**Segmentation metrics** come from a pixel confusion matrix $M$ (rows: true class, columns: predicted): IoU of class $c$ is $\frac{M_{cc}}{\sum_j M_{cj}+\sum_i M_{ic}-M_{cc}}$, and mIoU averages over classes. Pixel accuracy alone is misleading when one class (background, road) dominates.

## Worked example

**IoU and Dice.** $A=(1,1,5,5)$, $B=(3,2,7,6)$, both $4\times4$ (area 16).

- Intersection: $x$ from 3 to 5 (width 2), $y$ from 2 to 5 (height 3), area $6$.
- Union: $16+16-6=26$. IoU $=6/26=0.23$, a miss at threshold 0.5.
- Dice: $2\cdot6/32=0.375$; check: $2(0.23)/(1.23)=0.375$.

**AP by hand.** 3 ground-truth objects; detections sorted by score are **TP, TP, FP, TP**.

| rank | result | precision | recall |
|---|---|---|---|
| 1 | TP | 1/1 = 1.00 | 1/3 |
| 2 | TP | 2/2 = 1.00 | 2/3 |
| 3 | FP | 2/3 = 0.67 | 2/3 |
| 4 | TP | 3/4 = 0.75 | 3/3 |

The envelope precision is 1.00 up to recall 2/3 and 0.75 for the last third, so AP $=\tfrac13(1+1+0.75)=0.92$.

**COCO thresholds.** A detection with IoU 0.72 is a TP at thresholds $0.50,\dots,0.70$ (5 of the 10) and an FP at $0.75,\dots,0.95$, so it earns only half credit in mAP@[.5:.95].

## Practical toolbox

Data augmentation (flip, crop, colour jitter, mixup/cutmix), transfer learning from pretrained weights, mixed precision ([[Training Tricks]]). Libraries: torchvision, timm, Ultralytics, OpenCV, Albumentations.

- **Augmentation must transform the labels too.** Flip an image horizontally and every box becomes $x_1'=W-x_2$, $x_2'=W-x_1$; crop and the boxes must be clipped; for segmentation the mask gets exactly the same geometric transform. Colour jitter changes no labels.
- **Choose augmentations the task allows.** Flipping is fine for cats, wrong for reading text or for left/right anatomy.
- **Mixup / CutMix**: mixup blends two images and their one-hot labels; CutMix pastes a rectangle of image $b$ into image $a$ and mixes the labels by area, $\tilde y=\lambda y_a+(1-\lambda)y_b$ with $\lambda=1-\frac{\text{patch area}}{HW}$. Both regularise classifiers.
- **Transfer learning** is the default: start from ImageNet (or self-supervised) weights, swap the head, fine-tune with a small learning rate. With little data, freeze the early layers.
- **Libraries**: torchvision (datasets, classic models, box ops such as NMS), timm (hundreds of pretrained backbones), Ultralytics (YOLO training and inference), OpenCV (classic image processing, video I/O), Albumentations (fast augmentations that also transform boxes, masks and keypoints).

## Common confusions

- "Semantic and instance segmentation are the same." → Semantic gives one class per pixel (all cars share a label); instance separates individual objects.
- "A detection that overlaps the object is correct." → Only if IoU exceeds the threshold, and each ground-truth object can be matched once; duplicates count as FPs (hence NMS).
- "Dice and IoU can rank two models differently." → $\mathrm{Dice}=2\,\mathrm{IoU}/(1+\mathrm{IoU})$ is monotone, so per image they agree; only averages over images can differ slightly.
- "High pixel accuracy means good segmentation." → With dominant background classes, predicting background everywhere scores high; use per-class IoU / mIoU.
- "mAP@0.5 and COCO mAP are the same number." → COCO averages over IoU thresholds 0.5–0.95 and is much stricter.

## Check yourself

> [!question]- Two $2\times2$ boxes overlap in a $1\times2$ strip. What is their IoU?
> Intersection 2, union $4+4-2=6$, IoU $=1/3$.

> [!question]- Why do YOLO-style detectors need non-maximum suppression?
> They predict boxes densely, so one object triggers many overlapping high-scoring boxes; NMS keeps the best and removes the overlapping duplicates.

> [!question]- Convert IoU $=0.5$ to Dice.
> $2(0.5)/(1.5)=0.667$.

> [!question]- How many tokens does ViT produce for a $224\times224$ image with $16\times16$ patches, and how long is each flattened patch?
> $196$ tokens; each patch has $16\cdot16\cdot3=768$ numbers before the linear embedding.

> [!question]- You horizontally flip a $W=100$ image with a box $(10,20,30,60)$. What is the new box?
> $(100-30,\,20,\,100-10,\,60)=(70,20,90,60)$.

## Practice

[Computer Vision Overview - Exercises](Computer%20Vision%20Overview%20-%20Exercises.ipynb): matching applications to tasks, one-stage vs two-stage vs DETR, augmentation and transfer learning per task, IoU, Dice, AP, ViT tokens and COCO thresholds by hand, then code for vectorised IoU, NMS, top-k accuracy, segmentation metrics, average precision, flipping images with their boxes, CutMix and patchify for a ViT.

## Resources

- [Stanford CS231n](https://cs231n.stanford.edu/) · [CS231n course notes](https://cs231n.github.io/)
- [Dive into Deep Learning — CV chapters](https://d2l.ai/)
- Papers: [ResNet](https://arxiv.org/abs/1512.03385) · [ViT](https://arxiv.org/abs/2010.11929) · [U-Net](https://arxiv.org/abs/1505.04597) · [YOLO](https://arxiv.org/abs/1506.02640) · [CLIP](https://arxiv.org/abs/2103.00020)
- More papers: [Faster R-CNN](https://arxiv.org/abs/1506.01497) · [Mask R-CNN](https://arxiv.org/abs/1703.06870) · [DETR](https://arxiv.org/abs/2005.12872) · [Segment Anything](https://arxiv.org/abs/2304.02643)
