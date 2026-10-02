---
tags: [ml, deep-learning, practice]
---
# Training Tricks

> [!summary] In one sentence
> Getting a deep network to actually train is mostly about keeping signals at a sane scale (initialization, normalization), keeping the model from memorising (regularization), keeping updates stable and affordable (schedules, clipping, precision tricks), and debugging systematically when it still goes wrong.

## Intuition first

A deep network is a long chain of layers. Anything that slightly shrinks or slightly amplifies the signal at each layer gets *compounded*: $0.7^{20}\approx 0.0008$ and $1.3^{20}\approx 190$. Most "tricks" are ways to keep this chain balanced:

- **Initialization** sets the starting scale so that activations and gradients neither die out nor blow up.
- **Normalization** re-centres and re-scales activations *during* training, so they stay balanced even as weights change.
- **Regularization** stops the model from memorising the training set ([[Overfitting and Regularization]]).
- **Optimization tricks** keep the updates stable and let you train bigger models on limited hardware ([[Optimizers]]).
- **The debug checklist** is how you find out which of these is broken.

Think of tuning a long line of guitar amplifiers: if each one has gain slightly below 1 you hear silence at the end, slightly above 1 and you get screeching feedback. You want each stage at gain $\approx1$.

![Activation scale through a 10-layer ReLU network for four initializations: too small vanishes, too large explodes, Xavier fades, He stays flat](../../Attachments/ML%20Animations/Training%20Tricks%20-%20initialization%20and%20depth.gif)

*Note the log scale: each wrong init loses or gains a constant factor per layer, so its line is straight; only He's variance $2/n_{in}$ keeps ReLU activations at a constant scale.*

## Initialization

Xavier/Glorot (tanh), He/Kaiming (ReLU). Never all zeros.

**Why not zeros (or any constant)?** If all hidden units in a layer start with identical weights, they compute identical outputs, receive identical gradients, and get identical updates, forever. The layer behaves like a single unit (the **symmetry** is never broken). With all-zero weights in a ReLU or tanh net it is even worse: the hidden activations or the backpropagated signal $W^\top\delta$ is zero, so most gradients are exactly zero. Random weights break symmetry. Biases *can* start at zero, because the random weights already make units different.

**Deriving the right scale.** For $z_j=\sum_{i=1}^{n}W_{ji}h_i$ with independent zero-mean weights of variance $s^2$:
$$\mathrm{Var}(z_j)=n\,s^2\,\mathbb E[h_i^2].$$
- With a ReLU in front, $h=\max(0,z_{\text{prev}})$ and $z_{\text{prev}}$ symmetric around 0, half the mass is zeroed, so $\mathbb E[h^2]=\tfrac12\mathrm{Var}(z_{\text{prev}})$.
- To keep $\mathrm{Var}(z)$ constant from layer to layer we need $n\,s^2\cdot\tfrac12=1$, i.e. **He/Kaiming**: $s^2=2/n_{in}$.
- For tanh (roughly linear around 0, no halving) the same argument gives $s^2=1/n_{in}$; **Xavier/Glorot** averages forward and backward requirements: $s^2=2/(n_{in}+n_{out})$, or uniform on $\pm\sqrt{6/(n_{in}+n_{out})}$.

Using Xavier with ReLU loses a factor $\sqrt{1/2}$ in standard deviation per layer, which is the slowly fading blue line in the animation.

## Normalization

BatchNorm (CNN), LayerNorm ([[Transformers]]), GroupNorm (small batches), RMSNorm.

All of them do the same two steps on some group of numbers: standardise, then let the network re-scale and re-shift with learned parameters $\gamma,\beta$:
$$\hat x=\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}},\qquad y=\gamma\hat x+\beta.$$
They differ only in **which numbers** $\mu,\sigma^2$ are computed over (for activations of shape $N\times C\times H\times W$):

| Layer | Statistics over | Good for | Why |
|---|---|---|---|
| BatchNorm | the batch and spatial dims ($N,H,W$), per channel | CNNs with decent batch sizes | uses batch statistics, so it needs a big enough batch |
| LayerNorm | all features of *one* example ($C,H,W$ / the hidden vector) | [[Transformers]], RNNs | independent of batch size and sequence length |
| GroupNorm | groups of channels within one example | small batches (detection, segmentation) | batch-independent, but keeps some channel structure |
| RMSNorm | like LayerNorm, but no mean subtraction: $x/\sqrt{\overline{x^2}+\epsilon}\cdot\gamma$ | large language models | cheaper, works as well in practice |

**BatchNorm's train/test difference:** during training it uses the current batch's mean and variance and updates running averages; at test time it uses those running averages (a single test example has no meaningful batch statistics). Forgetting `model.eval()` makes predictions depend on whatever else is in the batch. For fine-tuning with tiny batches, freeze the BatchNorm statistics or switch to GroupNorm.

## Regularization

Dropout, weight decay, label smoothing, mixup/cutmix, augmentation, early stopping ([[Overfitting and Regularization]]).

- **Dropout**: during training, zero each activation with probability $p$. **Inverted dropout** scales the survivors by $1/(1-p)$ so that $\mathbb E[\tilde h]=h$, and does nothing at test time. Each step trains a random thinned sub-network, so units cannot rely on specific partners (an implicit ensemble).
- **Weight decay**: shrink weights a little each step ($w\leftarrow(1-\eta\lambda)w$, decoupled in AdamW). Prefers simpler, smaller-weight solutions.
- **Label smoothing**: replace the one-hot target by $y^{LS}=(1-\varepsilon)\,y+\varepsilon/K$. The model can no longer push one logit to infinity to reach zero loss, which reduces over-confidence and improves calibration.
- **Mixup / CutMix**: train on blends of two examples, $\tilde x=\lambda x_i+(1-\lambda)x_j$ with $\tilde y=\lambda y_i+(1-\lambda)y_j$, $\lambda\sim\mathrm{Beta}(\alpha,\alpha)$ (CutMix pastes a patch of one image into another and mixes labels by area). Encourages linear behaviour between classes.
- **Augmentation**: random crops, flips, colour jitter, etc., i.e. free extra data that encodes invariances you know the task has.
- **Early stopping**: monitor validation loss and stop (keeping the best checkpoint) once it has not improved for `patience` epochs.

## Optimization

Warm-up + decay schedules, gradient clipping, mixed precision (bf16), gradient accumulation, gradient checkpointing ([[Optimizers]]).

- **Warm-up + decay**: small learning rate at first (unstable early statistics and gradients), larger in the middle, decaying (cosine/linear) at the end to settle into a minimum.
- **Gradient clipping** by global norm: if $\|g\|=\sqrt{\sum_i\|g_i\|^2}$ over *all* parameter tensors exceeds a threshold $c$, rescale every gradient by $c/\|g\|$. Unlike clipping each element to $[-c,c]$, this keeps the gradient's direction.
- **Mixed precision (bf16)**: do most arithmetic in 16-bit floats (about 2× faster, half the memory) while keeping a 32-bit master copy of the weights; bf16 has the same exponent range as fp32, so it rarely overflows.
- **Gradient accumulation**: run several micro-batches, add up their gradients, then take one optimizer step. Effective batch $=$ (#devices) × (micro-batch) × (accumulation steps). Divide each micro-batch loss by the number of accumulation steps so the sum equals the mean over the effective batch.
- **Gradient checkpointing**: store only some activations and recompute the rest in the backward pass: trades about one extra forward pass for much less memory ([[Backpropagation]]).

## Debug checklist
1. Overfit 10 examples to ~0 loss.
2. Initial loss ≈ $\log K$ for $K$ classes.
3. Check data/labels visually and shapes.
4. Turn off augmentation/regularization first, add back later.
5. Watch gradient norms, activation statistics, learning-rate sweep.
6. Fix seeds; log with TensorBoard / Weights & Biases.

Why each step:
1. A network that cannot memorise 10 examples has a bug (wrong loss, labels misaligned, learning rate far off, gradients not flowing); no amount of data will fix it.
2. With small final-layer weights, logits are $\approx0$, softmax is uniform $1/K$, so cross-entropy is $-\log(1/K)=\log K$. A much larger starting loss means the output layer is badly scaled; a loss stuck *exactly* at $\log K$ means the network outputs a constant.
3. Most "model" bugs are data bugs: wrong label mapping, wrong channel order, broadcasting on the wrong axis.
4. Regularization makes the first sanity checks harder to pass; get a model that fits first, then make it generalise.
5. Exploding/vanishing gradients and dead units are visible in these statistics long before the loss tells you. A learning-rate sweep finds the range between "nothing happens" and "diverges".
6. Reproducibility lets you tell a real improvement from noise, and logs let you compare runs.

Typical symptoms: loss becomes `nan` mid-training → learning rate too high or a numerical problem (clip gradients, check $\log(0)$); training accuracy ≫ validation → overfitting (more regularization/data); validation better than training throughout → regularization such as dropout/augmentation is only active during training (normal) or the split leaks.

## Transfer learning

Freeze backbone → train head → unfreeze with small LR.

1. Load a model pretrained on a big dataset; replace the final layer by a new head for your classes.
2. **Freeze the backbone** and train only the head: the randomly initialised head would otherwise send large, noisy gradients into good pretrained features and wreck them.
3. **Unfreeze** (all or the top layers) and fine-tune with a **small learning rate** (e.g. 10× smaller), so the features adapt gently instead of being overwritten.

With a lot of target data you can unfreeze earlier and train more layers; with very little, keep more frozen.
Pitfalls: [[Common Pitfalls]]. Code: [[PyTorch Recipes]].

## Worked example

- **Initial loss check**, 5-class problem: expect $\log 5\approx1.61$. If you see 15, the logits are far too large at init.
- **He init** for a layer with $n_{in}=256$: $s=\sqrt{2/256}\approx0.088$.
- **Inverted dropout** with $p=0.5$: survivors are multiplied by $1/(1-0.5)=2$. An activation $h=3$ becomes $0$ or $6$ with equal probability: mean $3$, as intended.
- **Label smoothing** with $K=4$, $\varepsilon=0.2$, true class 0: $y^{LS}=(0.8+0.05,\ 0.05,\ 0.05,\ 0.05)=(0.85,0.05,0.05,0.05)$.
- **Gradient accumulation**: 2 GPUs × micro-batch 16 × 8 accumulation steps = effective batch 256; scale each micro-batch loss by $1/8$.

## Common confusions

- **"Zero init is fine because training will fix it."** Identical units get identical updates, so symmetry is never broken.
- **"Dropout is applied at test time too."** With inverted dropout, test time uses the full network with no scaling; the scaling was done during training.
- **"BatchNorm works the same in train and eval mode."** Train mode uses batch statistics, eval mode uses running averages; mixing them up silently changes predictions.
- **"A lower training loss is always better."** Regularization deliberately raises training loss to lower validation loss; judge by validation.
- **"Gradient accumulation is free."** It matches the gradient of a larger batch, but BatchNorm still only sees the micro-batch, and it costs proportionally more time per step.

## Check yourself

> [!question]- What is the expected initial cross-entropy loss for a 100-class classifier?
> $\log 100\approx4.61$.

> [!question]- Why does He initialization use variance $2/n_{in}$ rather than $1/n_{in}$?
> ReLU zeroes about half of its inputs, so $\mathbb E[h^2]=\tfrac12\mathrm{Var}(z)$; the factor 2 compensates to keep the variance constant across layers.

> [!question]- You train a Transformer on variable-length text. BatchNorm or LayerNorm, and why?
> LayerNorm: it normalises each token's features independently of the batch and of sequence length.

> [!question]- Why is global-norm clipping preferred over clipping each gradient element?
> It rescales all gradients by the same factor, preserving the update direction; element-wise clipping distorts the direction.

> [!question]- Your model cannot drive the loss on 10 training examples near zero. What does that tell you?
> There is a bug or a gross misconfiguration (loss, labels, learning rate, gradient flow); fix that before training on the full dataset.

## Practice

[Training Tricks - Exercises](Training%20Tricks%20-%20Exercises.ipynb): zero init, choosing a normalization layer, debugging from symptoms, transfer learning, $\log K$, deriving He init, dropout, label smoothing, gradient accumulation and mixup by hand, then coding activation statistics, BatchNorm forward/backward, LayerNorm/RMSNorm, dropout, global-norm clipping, overfitting 10 examples, and early stopping.

## Learn more
- [Karpathy – Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- [Stanford CS231n](https://cs231n.stanford.edu/) · [notes](https://cs231n.github.io/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/)
- [Karpathy – A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)
- [He et al. – Delving Deep into Rectifiers (He initialization)](https://arxiv.org/abs/1502.01852)
