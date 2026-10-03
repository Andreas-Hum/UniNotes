---
tags: [ml, project, llm, transformers]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Mini-GPT on Danish

> [!summary] In one sentence
> Write every line of a GPT yourself (tokenizer, causal attention, transformer block, sampling), train it for two minutes on your own Danish IT-ret notes, and watch it go from random symbols to fluent-sounding nonsense like *"Kun ikke nødvendighed – straffring, på hvor det"*.

**Notebook:** [Mini-GPT on Danish - Notebook](Mini-GPT%20on%20Danish%20-%20Notebook.ipynb) · part of [[Personal Projects]]

## Intuition first
A language model only ever answers one question: *given the text so far, what comes next?* Train that on enough text and grammar, spelling and style come for free. With ~100k characters of your notes the model learns Danish spelling, legal phrases ("art. 6, stk. 1", "den registrerede") and the *shape* of your notes (bullet lists, checkboxes), but not meaning.

## What you build (4 TODOs)
1. **Character tokenizer**: æ, ø, å for free; 103 symbols.
2. **Causal self-attention**: $\text{softmax}(QK^\top/\sqrt d + \text{mask})V$, checked against PyTorch's built-in and for "no peeking at the future".
3. **Transformer block**: pre-LayerNorm + residuals (GPT-2 layout).
4. **Sampling** with temperature and top-k.

Then: train 0.83M parameters for 1,500 steps (~2 min CPU) with early stopping, and measure how much it **copies** from your notes (`longest_copy`).

## Reference results (corpus ≈ 103k characters)
| | val loss (nats/char) |
|---|---|
| uniform guessing (103 symbols) | 4.63 |
| bigram counts | 2.65 |
| **mini-GPT, best step** | **1.66** |

Training loss keeps dropping (1.12 at step 1,500) while validation loss flattens. That gap is **memorisation**: with this little text the model starts learning your notes by heart. At temperature 0.5 the longest verbatim copy was ~28 characters; at 0.8 around 20. It composes new "sentences" from memorised fragments.

## Is ~100k characters enough?
For *nonsense Danish*: yes, and it's a great lesson in overfitting. For anything coherent you'd need 10–100× more text. Every lecture you add helps, and you can drop **song lyrics**, a public-domain Danish book or your own writing into `data/my_text/*.txt`. Plot best val loss against corpus size; that curve is the scaling law in miniature.

## Common confusions
- **"Loss 1.66 is bad, it's above 1"**: it's cross-entropy in nats per *character*. $e^{1.66} \approx 5.3$: the model is as unsure as choosing between ~5 characters, down from 103.
- **Random validation split**: if you shuffle characters into train/val, overlapping 64-character windows leak the validation text into training. Use a *contiguous* last 10 %.
- **Temperature isn't creativity**: it rescales logits. Below 1 = sharper and repetitive; above 1 = flatter and more spelling errors.

## Check yourself
> [!question]- Why does the causal mask use $-\infty$ and not 0?
> The mask is applied *before* softmax. $e^{-\infty} = 0$ gives future positions exactly zero weight; a 0 score would give them weight $e^0 = 1$.

> [!question]- Your model has 0.83M parameters and the corpus 93k training characters. What do you expect, and how do you detect it?
> More parameters than training tokens → it can memorise. Detect it by the train/val gap growing and by long verbatim copies in samples. Fixes: more data, more dropout, smaller model, early stopping.

> [!question]- Why is the bigram baseline 2.65 and not much lower?
> A bigram only sees one previous character. "Den dataansvarli_" is obvious to the GPT (64 characters of context) but "i_" alone could continue in dozens of ways.

## Learn more
- [Karpathy – Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY): the video this project follows
- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html): the full course
- Vault: [[Transformers]] · [[Attention Mechanism]] · [[LLMs Overview]]
