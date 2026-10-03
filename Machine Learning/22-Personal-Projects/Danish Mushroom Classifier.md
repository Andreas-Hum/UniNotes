---
tags: [ml, project, computer-vision, transfer-learning]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Danish Mushroom Classifier

> [!summary] In one sentence
> Classify six common Danish mushrooms from 360 citizen-science photos taken in Denmark (or your own photos) by borrowing an ImageNet-trained ResNet-18. A frozen backbone plus logistic regression gets 87 %, where a CNN trained from scratch on the same photos gets 38 %.

> [!warning] Never eat a mushroom because a model said so
> The model confuses the deadly **grøn fluesvamp** (death cap) with the edible **Karl Johan**. Get wild mushrooms checked by a *svampekontrollant*.

**Notebook:** [Danish Mushroom Classifier - Notebook](Danish%20Mushroom%20Classifier%20-%20Notebook.ipynb) · part of [[Personal Projects]]

## Intuition first
A network trained on 1.2M ImageNet photos already "sees" edges, textures, colours and shapes, and those features transfer to caps, gills and stems. With 42 photos per class you can't learn vision from scratch, but you *can* learn which combination of existing features means "chanterelle".

## What you build (3 TODOs)
1. `extract_features`: run photos through ResNet-18 with its last layer removed → 512-d vectors.
2. `linear_probe`: logistic regression on those vectors.
3. `top_confusions`: the biggest mistakes in the confusion matrix (which mistakes matter, not just how many).

Plus a from-scratch CNN baseline, a gallery of the most confident mistakes, optional fine-tuning of the last ResNet stage, and per-photo licence credits.

## Reference results (6 classes, 252 train / 108 test photos)
| model | test accuracy |
|---|---|
| chance | 17 % |
| small CNN from scratch (30 epochs) | 38 % |
| **ResNet-18 features + logistic regression** | **87 %** |
| fine-tuned `layer4` (3 epochs, ~15 s) | 89 % |

The photos are fetched live from iNaturalist (research grade, CC0/CC-BY/CC-BY-NC, observed in Denmark, top-voted first), so your numbers can drift a few points as new observations arrive. Attribution for every photo is saved in `data/mushrooms/credits.csv`.

## Your data
- Put 20–50 photos per class in `22-Personal-Projects/data/my_photos/<class>/` and rerun: the notebook switches automatically.
- Or change `SPECIES` to other iNaturalist taxa: Danish birds (solsort, musvit, gråspurv…), trees, insects.
- Danish fungal records: [Danmarks Svampeatlas](https://svampe.databasen.org/).

## Common confusions
- **Accuracy is the wrong metric here**: 87 % sounds good until one of the 13 % is "death cap → edible". Look at the confusion matrix, and consider abstaining when unsure.
- **Test photos from the same observation**: one observation can have several photos. We take one photo per observation, so near-duplicates can't leak between train and test.
- **Shortcut learning**: the model might learn "forest floor" or "basket" instead of the mushroom. Grad-CAM (stretch goal) shows where it looks.

## Check yourself
> [!question]- Why freeze the backbone instead of training all 11M parameters?
> 252 photos can't constrain 11M parameters, so the network would overfit and wreck its useful pre-trained features. Training only a 512×6 linear layer (3k parameters) is well-posed with this much data.

> [!question]- Fine-tuning gave 89 % vs 87 % on 108 test photos. Is fine-tuning better?
> Not conclusively: 2 points = ~2 photos. The standard error of an accuracy near 0.88 on 108 samples is about $\sqrt{0.88 \cdot 0.12 / 108} \approx 3$ points. You'd need cross-validation or a bigger test set.

## Learn more
- [iNaturalist](https://www.inaturalist.org/): where the photos come from (add your own observations!)
- Vault: [[CNN]] · [[CNN Architectures]] · [[Computer Vision Overview]] · [[Explainability and Fairness]]
