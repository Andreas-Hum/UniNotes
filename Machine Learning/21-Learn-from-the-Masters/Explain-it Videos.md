---
tags: [ml, masters, teaching, manim]
status: not-started
level: I
reviewed:
---
# Explain-it Videos

> [!summary] In one sentence
> Pick one concept and explain it in a 3-minute animated video made with Manim, the Python library behind 3Blue1Brown. If you can't animate it step by step, you don't understand it yet. Teaching is the hardest test of understanding.

**The example below:** a working scene, *Gradient descent and the learning rate* ([explain_it_gradient_descent.py](explain_it_gradient_descent.py), ≈ 55 s). Copy it as your starting point.

![[Explain-it - Gradient Descent.mp4]]

## The recipe: 5 beats in 3 minutes

| Beat | Time | Job | In the example |
|---|---|---|---|
| 1. **Hook** | 0:00–0:15 | Ask the question the video answers | "How does a neural network actually learn?" |
| 2. **Intuition** | 0:15–1:00 | One picture, no symbols | the loss as a landscape, the weights as a ball on it |
| 3. **The rule / math** | 1:00–1:45 | Introduce the formula *by animating it* | tangent line + `new w = w − lr × slope`, 6 steps |
| 4. **What can go wrong** | 1:45–2:30 | The failure mode or the common confusion | three learning rates side by side |
| 5. **Recap** | 2:30–3:00 | 3–4 bullets + a teaser for the next idea | "the slope becomes a gradient vector" |

The example runs about 55 s. To stretch it to 3 minutes, add the beats *you* think are missing, for example momentum, a 2-D contour plot, or stochastic mini-batch noise. Choosing what to add is part of the exercise.

## Storyboard template (fill in before writing any code)
```markdown
**Concept:** 
**The one sentence the viewer should remember:** 
**Who is the viewer?** (e.g. a 3rd-semester student who knows derivatives)
1. Hook (15 s) – question: 
2. Intuition (45 s) – picture: 
3. Math (45 s) – formula, and what moves on screen while I say it: 
4. Pitfall (45 s) – the confusion from the note's "Common confusions" section: 
5. Recap (30 s) – bullets: 
```
Good beat-4 material is already in each topic note's **Common confusions** section.

## Setup
```bash
pip install manim          # needs Cairo + Pango; on Ubuntu: sudo apt install libcairo2-dev libpango1.0-dev pkg-config python3-dev ffmpeg
manim -pql explain_it_gradient_descent.py GradientDescent   # 480p preview, opens when done
manim -qh  explain_it_gradient_descent.py GradientDescent   # 1080p final
manim -ql --format=gif explain_it_gradient_descent.py GradientDescent   # GIF, like the ones in Attachments/ML Animations
```
- Use `Text(...)` for labels. `MathTex` needs a LaTeX install (TeX Live/MiKTeX). Add it once your formulas get serious.
- Output goes to `media/` next to the script (ignored by git). Copy the final video or GIF to `Attachments/ML Animations/` and embed it in the topic note.
- Animation building blocks you will reuse: `ValueTracker` + `always_redraw` (anything that follows a moving number), `Axes.plot`, `Transform`/`ReplacementTransform`, `Indicate`, `FadeIn(..., shift=UP)`.

## Ideas for videos (one per month, alternating with [[Paper-to-Code Months]])
- **Attention in 3 minutes:** queries looking up keys, the softmax as a spotlight, why divide by $\sqrt{d_k}$ ([[Attention Mechanism]]).
- **Why residual connections work:** a block that can do nothing is a block that can't hurt. Pair it with the ResNet month ([[CNN Architectures]]).
- **Bias–variance:** polynomials of increasing degree fitted to the same noisy points ([[Bias-Variance Tradeoff]]).
- **Backprop as passing blame backwards** through a 3-node graph ([[Backpropagation]]).
- **Diffusion:** two moons dissolving into noise and back. Pair it with the DDPM month ([[Generative Models]]).

## Check yourself
> [!question]- Why does the example use a 1-D bowl instead of a real network's loss?
> One weight means you can *see* the whole landscape and every step. A good explainer strips the idea down to the smallest case that still shows the mechanism, and only then says "the same thing happens in a million dimensions".

> [!question]- In the "too large" panel the ball oscillates and drifts outward. What learning rate is the boundary for $L(w)=\tfrac12 w^2$?
> Each step multiplies $w$ by $(1-\eta)$. It converges when $|1-\eta|<1$, i.e. $0<\eta<2$. At $\eta = 2.05$ the factor is $-1.05$: the ball flips side every step and moves 5 % further out each time.

## Learn more
- [Manim Community – installation](https://docs.manim.community/en/stable/installation.html) · [quickstart tutorial](https://docs.manim.community/en/stable/tutorials/quickstart.html)
- [3Blue1Brown – Neural networks series](https://www.3blue1brown.com/topics/neural-networks), the gold standard for this style

---
Back to [[00 - Machine Learning Index]].
