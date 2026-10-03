---
tags: [ml, vision, detection]
---
# Object Detection

> [!summary] In one sentence
> Object detection predicts **what** is in an image **and where**, as a set of class-labelled bounding boxes, using either two-stage (propose regions, then classify) or one-stage (predict boxes densely in one pass) detectors, cleaned up with non-maximum suppression and scored with mAP.

## Intuition first
Classification answers "is there a dog?". Detection answers "there is a dog at (x, y, w, h) and a cat over there". The difficulty: the number of objects is unknown, they come in all sizes and they overlap. Every detector has three parts:
1. a **backbone** ([[CNN Architectures|ResNet, EfficientNet, ViT]]) that turns the image into feature maps,
2. a **neck** (often a Feature Pyramid Network) that combines fine and coarse feature maps so small and large objects can both be found,
3. a **head** that outputs boxes + class scores.

## Boxes and IoU
A box is $(x_1,y_1,x_2,y_2)$ or $(c_x,c_y,w,h)$. Overlap is measured by **Intersection over Union**:
$$\mathrm{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}\in[0,1]$$
A prediction usually counts as correct (a true positive) if IoU with a ground-truth box of the same class is $\ge0.5$.

**Box regression** does not predict raw coordinates but offsets relative to an anchor/proposal $(a_x,a_y,a_w,a_h)$:
$$t_x=\frac{x-a_x}{a_w},\quad t_y=\frac{y-a_y}{a_h},\quad t_w=\log\frac{w}{a_w},\quad t_h=\log\frac{h}{a_h}$$
trained with a smooth-L1 loss (or IoU-based losses such as GIoU).

## Non-maximum suppression (NMS)
Detectors produce many overlapping boxes for the same object. NMS:
1. sort boxes by confidence,
2. keep the top box, remove every other box of the same class with IoU > threshold (e.g. 0.5),
3. repeat with the remaining boxes.

## Detector families
| Family | Examples | How it works | Trade-off |
|---|---|---|---|
| **Two-stage** | R-CNN → Fast R-CNN → **Faster R-CNN** | a Region Proposal Network suggests ~2,000 candidate boxes; RoI pooling crops features; a head classifies and refines each | accurate, slower |
| **One-stage, anchor-based** | SSD, **YOLO** (v1–v5), RetinaNet | predict class + offsets for every anchor at every grid cell in one pass | fast; RetinaNet's **focal loss** fixes the huge background/foreground imbalance |
| **Anchor-free** | FCOS, CenterNet, YOLOv8+ | predict object centres/points and distances to box edges | simpler, no anchor tuning |
| **Transformer** | **DETR**, Deformable DETR, RT-DETR | object queries + set prediction with Hungarian matching → no anchors, no NMS | elegant; DETR was slow to train, later variants fix it |
| **Open-vocabulary** | OWL-ViT, Grounding DINO | match boxes to text embeddings (CLIP-style) | detect classes never seen in training |

### Focal loss
With cross-entropy, the thousands of easy background anchors dominate the loss. Focal loss down-weights well-classified examples:
$$\mathrm{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t$$
where $p_t$ is the predicted probability of the true class; $\gamma=2$ is typical. When $p_t=0.9$, the factor $(1-p_t)^2=0.01$ shrinks that example's loss 100×.

## Evaluation: mAP
1. For one class, sort all predictions by confidence; mark each TP (IoU ≥ threshold with an unmatched ground-truth box) or FP.
2. Compute precision and recall at each rank → **precision–recall curve**.
3. **AP** = area under that curve (interpolated).
4. **mAP** = mean AP over classes. **COCO mAP@[.5:.95]** also averages over IoU thresholds 0.50, 0.55, …, 0.95, rewarding tight boxes. **mAP@0.5** (Pascal VOC) is more lenient.

## Worked example: IoU
Ground truth $(0,0,4,4)$, prediction $(2,2,6,6)$. Intersection $(2,2,4,4)$ → area 4. Union $=16+16-4=28$. IoU $=4/28\approx0.14$ → a **false positive** at threshold 0.5, even though the boxes overlap.

## Practical notes
- Libraries: Ultralytics YOLO, Detectron2, MMDetection, torchvision.
- Data formats: COCO JSON, Pascal VOC XML, YOLO txt. Label quality (tight, consistent boxes) matters a lot.
- Small objects: higher input resolution, FPN, tiling.
- Speed vs accuracy: report latency on the target hardware, not just mAP.

## Common confusions
- **"High mAP@0.5 means precise boxes."** → It only requires 50 % overlap; look at mAP@[.5:.95].
- **"NMS is part of training."** → It is post-processing; DETR-style models remove the need for it.
- **"Accuracy is a fine metric for detection."** → There is no fixed number of predictions; use precision/recall/AP.

## Check yourself
> [!question]- Two boxes of 10×10 overlap in a 5×10 strip. What is the IoU?
> $50/(100+100-50)=50/150=0.33$.

> [!question]- Why does a one-stage detector need focal loss (or hard-negative mining) more than a two-stage one?
> It scores tens of thousands of anchors per image, almost all background; the RPN in a two-stage detector already filters most easy negatives.

> [!question]- What does DETR use instead of NMS to avoid duplicate predictions?
> A fixed set of object queries trained with bipartite (Hungarian) matching to the ground truth, so each object is matched to exactly one prediction.

## Learn more
- [Faster R-CNN — Ren et al. 2015](https://arxiv.org/abs/1506.01497)
- [YOLO — Redmon et al. 2015](https://arxiv.org/abs/1506.02640)
- [Focal Loss (RetinaNet) — Lin et al. 2017](https://arxiv.org/abs/1708.02002)
- [DETR — Carion et al. 2020](https://arxiv.org/abs/2005.12872)
- [Stanford CS231n — detection lecture](https://cs231n.stanford.edu/)

See [[Computer Vision Overview]], [[CNN Architectures]], [[Image Segmentation]].
