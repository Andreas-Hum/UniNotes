---
tags: [ml, deep-learning, representation-learning]
status: not-started
notebook: not-started
level:
reviewed:
---
# Self-Supervised and Contrastive Learning

> [!summary] In one sentence
> Self-supervised learning manufactures its own labels from unlabeled data through a **pretext task** (match two augmented views, fill in masked parts, predict the next token), and the representations learned that way are then reused with a linear probe or fine-tuning on the task you actually care about.

Learn representations from unlabeled data by inventing a **pretext task**; then fine-tune or use a linear probe.

## Intuition first

Labels are expensive; raw images and text are nearly free. The question is how to learn useful features from data that has no labels. The trick is to invent a game whose answer is already hidden in the data:

- **Contrastive**: take a photo, make two randomly cropped and recoloured copies ("views"). The game: from a big batch of views, find the one that came from the *same* photo. To win, the network must ignore crop and colour and recognise what is *in* the image, which is exactly the kind of feature a classifier later needs.
- **Masked modeling**: hide some words or image patches and reconstruct them (BERT, MAE). To fill a gap you must understand the context.
- **Autoregressive**: predict the next token (GPT). Same idea, always hiding the future.

Think of how a child learns that a cup seen from the side and from above is the same object, long before anyone teaches the word "cup". Contrastive learning is that idea in code: *different views of the same thing should map to nearby points; different things should map far apart*.

The danger in the "make views agree" game is a lazy solution: map **every** image to the same point. Then all views agree perfectly and nothing has been learned. This is called **collapse**, and each family has its own way to prevent it: negatives in contrastive learning, stop-gradient and momentum tricks in the non-contrastive methods, and a reconstruction target in masked modeling.

![Eight embeddings on the unit circle: views of the same image are pulled together and different images pushed apart, then a collapse to one point](../../Attachments/ML%20Animations/Self-Supervised%20and%20Contrastive%20Learning%20-%20pull%20and%20push.gif)

*Watch the anchor's green line (its positive) and red dashed lines (negatives), then the mean InfoNCE loss falling from about 2.8 to 0.5 as same-coloured pairs meet and colours spread around the circle. In the collapsed end state the loss is stuck at $\log 7\approx1.95$, because the anchor cannot tell its positive apart from the six negatives.*

## Families

| Family | Pretext task | Examples |
|---|---|---|
| **Contrastive** | pull augmented views of the same sample together, push others apart | SimCLR, MoCo, CLIP (image–text) |
| Non-contrastive | match views without negatives (stop-gradient, momentum encoder) | BYOL, SimSiam, DINO, BM3 ([[Multimodal Recommender Systems]]) |
| Masked modeling | reconstruct masked parts | BERT ([[Transformers]]), MAE |
| Autoregressive | predict the next token | GPT ([[LLMs Overview]]) |

- **SimCLR** uses the other images in the batch as negatives, hence large batches.
- **MoCo** keeps a queue of negatives from past batches, encoded by a slowly moving **momentum (EMA) encoder** $\xi\leftarrow m\,\xi+(1-m)\,\theta$, so many negatives are possible with small batches.
- **CLIP** treats an image and its caption as the two "views": image and text encoders are trained so that matching pairs have high similarity.
- **BYOL / SimSiam / DINO** use no negatives at all. An asymmetric setup (a predictor head on one branch, stop-gradient or an EMA "teacher" on the other) prevents the trivial collapsed solution in practice.
- **MAE** masks about 75 % of image patches and reconstructs pixels; **BERT** masks about 15 % of tokens.

## The math, step by step

### Similarity

Embeddings are L2-normalised, $\hat z=z/\lVert z\rVert$, so they live on the unit sphere and $\mathrm{sim}(z_i,z_j)=\hat z_i^\top\hat z_j=\cos\angle(z_i,z_j)\in[-1,1]$. For unit vectors $\lVert u-v\rVert^2=2-2\cos(u,v)$, so "high cosine" and "small distance" mean the same thing.

### InfoNCE / NT-Xent loss

For anchor $z_i$, positive $z_j$, temperature $\tau$:
$$\ell_{i}=-\log\frac{\exp(\mathrm{sim}(z_i,z_j)/\tau)}{\sum_{k\neq i}\exp(\mathrm{sim}(z_i,z_k)/\tau)}$$

Reading it piece by piece:

- The fraction is a **softmax** over all candidates $k\ne i$ (the positive plus all negatives), evaluated at the positive. It is "the probability that the anchor picks its true partner".
- $-\log$ of that probability is a **cross-entropy**: contrastive learning is classification where the class is "which of the $2N-1$ candidates is my other view?".
- In SimCLR a batch of $N$ images gives $2N$ views; each anchor has 1 positive and $2N-2$ negatives, and the total loss averages $\ell_i$ over all $2N$ anchors. NT-Xent means "normalised temperature-scaled cross-entropy".

Same form as the in-batch softmax of two-tower recommenders ([[Deep Learning Recommenders]]).

### What the gradient does

With $s_k=\mathrm{sim}(z_i,z_k)$ and $p_k$ the softmax probabilities,

$$\frac{\partial\ell_i}{\partial s_k}=\frac1\tau\big(p_k-\mathbb 1[k=j]\big).$$

For the positive this is $\frac1\tau(p_j-1)<0$: gradient descent *increases* its similarity (pull). For a negative it is $\frac1\tau p_k>0$: its similarity is *decreased* (push), and the push is strongest for the **hard negatives**, the ones with the highest $p_k$.

### Temperature

Dividing by a small $\tau$ sharpens the softmax: the loss then focuses almost entirely on the hardest negatives. A large $\tau$ treats all negatives alike. Typical values are $0.05$–$0.5$; temperature matters as much as a learning rate.

### Collapse, in numbers

If every embedding is the same, all similarities are equal and $p_k=\frac1{2N-1}$ for every candidate, so $\ell_i=\log(2N-1)$. The loss cannot go below that without spreading the embeddings out: negatives make collapse costly.

### Two useful views of the objective

- **Mutual information**: with one positive among $N$ candidates, $I(x;y)\ge\log N-\mathcal L_{\text{InfoNCE}}$. Minimising the loss maximises a lower bound on the information shared by the two views, and more negatives allow a higher bound.
- **Alignment and uniformity** (Wang & Isola, 2020): the loss trades off *alignment*, $\mathbb E\lVert f(x)-f(x^+)\rVert^2$ small (positives close), against *uniformity*, $\log\mathbb E\,e^{-t\lVert f(x)-f(y)\rVert^2}$ small (embeddings spread over the sphere). Collapse is perfect alignment with the worst possible uniformity.

### CLIP's symmetric loss

With normalised image embeddings $\hat I$ and text embeddings $\hat T$ for $N$ pairs, logits $L=\hat I\hat T^\top/\tau$. The correct "class" of row $i$ is column $i$. CLIP averages two cross-entropies: image→text over rows and text→image over columns.

### Using the representation

- **Linear probe**: freeze the encoder and train only a linear classifier on top. It measures how *linearly separable* the learned features are; it is a fairer test of representation quality than full fine-tuning, which can repair a mediocre encoder.
- **Fine-tuning**: unfreeze everything and train on the labelled task, usually giving the best accuracy.

## Worked example

Anchor with cosine similarity $0.9$ to its positive and $0.3,\ 0.0$ to two negatives.

With $\tau=0.5$ the logits are $1.8,\ 0.6,\ 0.0$:

- $e^{1.8}=6.05$, $e^{0.6}=1.82$, $e^{0}=1$, sum $=8.87$
- $p_{\text{pos}}=6.05/8.87=0.682$, so $\ell=-\log0.682=0.383$.

With $\tau=0.1$ the logits are $9,\ 3,\ 0$: $p_{\text{pos}}=8103/(8103+20.1+1)=0.997$ and $\ell=0.003$. The same geometry looks almost solved at low temperature; at $\tau=1$ it is $\ell=0.67$. Temperature changes how hard the loss pushes.

Collapse check: SimCLR with $N=128$ images has $2N-1=255$ candidates per anchor, so a collapsed encoder sits at $\ell=\log255\approx5.54$. If your loss is stuck near this value, suspect collapse.

## Practical lessons (SimCLR)

Strong augmentation composition (crop + colour), a projection head, large batches / many negatives, temperature matters. Collapse (all embeddings equal) is the failure mode to watch for.

- **Crop + colour together**: crops alone can be solved by matching colour histograms; colour jitter removes that shortcut and forces the network to look at shapes and objects. Augmentations define what the representation will be *invariant* to, so choose them for your domain.
- **Projection head**: a small MLP $g$ after the encoder; the loss is computed on $g(h)$ but the representation used downstream is $h$. The head absorbs the invariances the loss demands (e.g. throwing away colour), so $h$ keeps more generally useful information.
- **Many negatives**: more candidates make the classification task harder (more informative) and raise the ceiling $\log N$ of the mutual-information bound, hence large batches (SimCLR) or a queue (MoCo).
- **Watch for collapse**: monitor the standard deviation of normalised embeddings across the batch; near zero means collapse.

## Common confusions

- "Self-supervised means unsupervised clustering." → It is supervised learning on labels generated from the data itself (which view matches, which word was masked).
- "The positive is excluded from the denominator." → In this InfoNCE form the denominator sums over all $k\ne i$, which includes the positive.
- "A lower contrastive loss always means better features." → The loss depends on $\tau$, batch size and augmentations; compare representations with a linear probe on a downstream task.
- "BYOL works because it has negatives hidden somewhere." → It uses none; the predictor plus stop-gradient/EMA asymmetry is what avoids collapse.
- "Use the projection-head output downstream." → Use the encoder output $h$ before the head; it transfers better.

## Check yourself

> [!question]- Why does a loss that only pulls positive pairs together fail?
> The constant map (every input to the same embedding) makes all positives agree perfectly: collapse. Something must push apart or break the symmetry (negatives, stop-gradient, EMA teacher, reconstruction).

> [!question]- What is the InfoNCE loss of a fully collapsed encoder with $2N-1$ candidates?
> All similarities are equal, so $p_{\text{pos}}=1/(2N-1)$ and $\ell=\log(2N-1)$.

> [!question]- What does lowering the temperature $\tau$ do?
> It sharpens the softmax, so the loss and gradients concentrate on the hardest negatives; too low becomes unstable, too high treats all negatives alike.

> [!question]- What is a linear probe, and why use it?
> A linear classifier trained on frozen features; it measures how linearly separable the representation is without letting fine-tuning hide a weak encoder.

> [!question]- Which family does MAE belong to, and what is its pretext task?
> Masked modeling: reconstruct the pixels of randomly masked image patches.

## Practice

[Self-Supervised and Contrastive Learning - Exercises](Self-Supervised%20and%20Contrastive%20Learning%20-%20Exercises.ipynb): naming the pretext tasks, collapse and how each family avoids it, linear probes and projection heads, InfoNCE and its gradient by hand, the collapsed loss, cosine vs Euclidean distance, the mutual-information bound, then code for cosine-similarity matrices, NT-Xent and its gradient, augmentations, temperature, alignment and uniformity, linear probing, CLIP's symmetric loss and an EMA encoder.

## Learn more

- [SimCLR — Chen et al. 2020](https://arxiv.org/abs/2002.05709)
- [CLIP — Radford et al. 2021](https://arxiv.org/abs/2103.00020)
- [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
- [MoCo — He et al. 2019](https://arxiv.org/abs/1911.05722)
- [BYOL — Grill et al. 2020](https://arxiv.org/abs/2006.07733)
- [MAE — He et al. 2021](https://arxiv.org/abs/2111.06377)
- [Wang & Isola 2020 — Alignment and Uniformity](https://arxiv.org/abs/2005.10242)
