---
tags: [ml, vision, segmentation]
---
# Image Segmentation

> [!summary] In one sentence
> Segmentation labels **every pixel**: semantic segmentation gives each pixel a class, instance segmentation separates individual objects, and panoptic does both – typically with encoder–decoder networks such as U-Net, scored with IoU/Dice.

## Intuition first
Detection draws a box around the cat. Segmentation colours in exactly the cat's pixels. That matters when shape matters: tumours in medical scans, road vs pavement for self-driving cars, cutting a person out of a photo.

| Task | Output | "Two cats" becomes |
|---|---|---|
| **Semantic** | class per pixel | one "cat" region |
| **Instance** | mask per object (countable "things") | cat #1, cat #2 |
| **Panoptic** | semantic for "stuff" (sky, road) + instances for "things" | sky, road, cat #1, cat #2 |

## Architectures
### Encoder–decoder idea
A classification CNN shrinks the image ($224\to7$) to capture *what*; segmentation also needs *where*. So:
- **Encoder:** a backbone that downsamples and builds semantic features.
- **Decoder:** upsamples back to full resolution (bilinear upsampling or **transposed convolutions**).
- **Skip connections:** pass high-resolution encoder features to the decoder so edges stay sharp.

| Model | Idea |
|---|---|
| **FCN** (2015) | replace FC layers with convs → a dense prediction map; upsample + skip connections |
| **U-Net** (2015) | symmetric encoder–decoder, skip connections **concatenate** features at every scale; works with few images (medical) |
| **DeepLab v3+** | **atrous (dilated) convolutions** enlarge the receptive field without downsampling; ASPP = parallel dilations for multi-scale context |
| **Mask R-CNN** (2017) | Faster R-CNN + a small mask head per detected box → instance segmentation; **RoIAlign** avoids misalignment |
| **Mask2Former** | Transformer with mask queries; one model for semantic, instance and panoptic |
| **SAM** (Segment Anything, 2023) | promptable foundation model: give a point/box/text, get a mask, zero-shot |

### Dilated convolution
A $3\times3$ filter with dilation rate $r$ samples pixels $r$ apart, covering a $(2r+1)\times(2r+1)$ area with the same 9 weights. Stacking dilations 1, 2, 4 grows the receptive field exponentially without pooling.

### Transposed convolution
The "reverse" of a strided conv: each input value scatters a weighted filter onto a larger output. Output size $=(W-1)S-2P+F$. Can produce checkerboard artefacts; bilinear upsampling + conv is a common alternative.

## Losses and metrics
- **Pixel-wise cross-entropy** – standard, but dominated by large classes (background).
- **IoU / Jaccard** per class: $\dfrac{|P\cap G|}{|P\cup G|}$; **mIoU** = mean over classes.
- **Dice coefficient:** $\dfrac{2|P\cap G|}{|P|+|G|}$ (equals F1 on pixels). **Dice loss** $=1-\text{Dice}$ (soft version uses probabilities) handles class imbalance well – popular in medical imaging. Relation: $\text{Dice}=\dfrac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}$.
- Often combined: CE + Dice.
- Instance/panoptic: mask AP (COCO), Panoptic Quality (PQ).

## Worked example: IoU vs Dice
Prediction covers 80 pixels, ground truth 100, overlap 60.
IoU $=60/(80+100-60)=0.5$. Dice $=2\cdot60/(80+100)=0.667$. Check: $2\cdot0.5/1.5=0.667$. ✓

## Practical notes
- Annotating masks is expensive → use SAM to speed up labelling, weak labels (boxes, scribbles), or pretrained backbones.
- Augment image **and mask identically** (Albumentations does this).
- Libraries: `segmentation_models_pytorch`, Detectron2, MMSegmentation, Hugging Face `transformers` (Mask2Former, SegFormer, SAM).

## Common confusions
- **"Pixel accuracy is a good metric."** → 95 % of pixels may be background; predict "all background" and get 95 %. Use mIoU/Dice.
- **"Dice and IoU rank models differently."** → They are monotonically related for a single prediction, so they rank single predictions the same; averages over images can differ slightly.
- **"Semantic segmentation can count objects."** → Touching objects of one class merge; you need instance segmentation.

## Check yourself
> [!question]- Why does U-Net need skip connections?
> The encoder throws away spatial detail while downsampling; skip connections give the decoder the high-resolution features needed for precise boundaries.

> [!question]- A $3\times3$ conv with dilation 2 – what area does it cover and how many weights does it have?
> $5\times5$ area, still 9 weights.

> [!question]- IoU is 0.6. What is Dice?
> $2\cdot0.6/1.6=0.75$.

## Learn more
- [U-Net — Ronneberger et al. 2015](https://arxiv.org/abs/1505.04597)
- [Mask R-CNN — He et al. 2017](https://arxiv.org/abs/1703.06870)
- [Segment Anything — Kirillov et al. 2023](https://arxiv.org/abs/2304.02643)
- [Stanford CS231n](https://cs231n.stanford.edu/)

See [[Computer Vision Overview]], [[Object Detection]], [[CNN Architectures]].
