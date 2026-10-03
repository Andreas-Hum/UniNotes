---
tags: [ml, play, interactive]
status: not-started
level:
reviewed:
---
# Playgrounds

> [!summary] In one sentence
> Five interactive mini-apps in one page – drag points, move sliders and watch an SVM, k-means, gradient descent, attention and a tiny neural network react in real time.

**Open:** [ML Playgrounds.html](ML%20Playgrounds.html) – opens in your browser (no install, works offline, light and dark mode). In Obsidian, click the link or right-click the file → *Open in default app*.

| Tab | What you do | What you should notice | Theory |
|---|---|---|---|
| **SVM margin** | add/drag blue and orange points, slide C | only the circled support vectors move the boundary; small C = wide street that tolerates violations | [[Support Vector Machines]] |
| **k-means** | add points or random blobs, Step / Run, new centroids | SSE never increases; different starts → different (local) solutions; elongated clusters get cut wrongly | [[Clustering]] |
| **Gradient descent** | click a start point, pick surface, optimiser and learning rate | zig-zag in narrow valleys, divergence at high learning rates, momentum/Adam smoothing, start-dependent minima | [[Gradient Descent]] · [[Optimizers]] |
| **Attention** | drag the query ★ and the keys, change temperature, toggle √d | the closest key dominates; low temperature → one-hot, high → uniform; scaling prevents saturation | [[Attention Mechanism]] |
| **Neural net (XOR)** | change hidden units, learning rate, dataset | 1 hidden unit cannot solve XOR; 2 sometimes gets stuck; the loss curve reacts to the learning rate | [[Neural Networks]] · [[Backpropagation]] |

## Mini-missions
- [ ] SVM: build a dataset where moving **one** point flips the boundary by 90°.
- [ ] k-means: find a dataset and k where two runs give clearly different SSE.
- [ ] Gradient descent: find the largest learning rate that still converges on the bowl. Compare with theory: for $f=x^2+10y^2$ the steepest direction has curvature 20, so stability needs lr < 2/20 = 0.1.
- [ ] Attention: place the keys so the query gives exactly 50/50 weight to two of them.
- [ ] XOR: what is the smallest H that solves the *circle* dataset reliably? Why?

Next: [[Break the Model]] · [[Guess the Output]] · [[Weekly Challenges]]
