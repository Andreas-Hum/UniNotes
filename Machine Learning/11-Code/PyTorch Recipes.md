---
tags: [ml, code, pytorch]
---
# PyTorch Recipes

```python
import torch, torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)
dev = "cuda" if torch.cuda.is_available() else "cpu"

model = nn.Sequential(nn.Linear(d, 128), nn.ReLU(), nn.Dropout(0.1), nn.Linear(128, K)).to(dev)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
loss_fn = nn.CrossEntropyLoss()           # expects logits, not softmax
dl = DataLoader(TensorDataset(X, y), batch_size=64, shuffle=True)

for epoch in range(20):
    model.train()
    for xb, yb in dl:
        xb, yb = xb.to(dev), yb.to(dev)
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

    model.eval()
    with torch.no_grad():
        val_acc = (model(X_val.to(dev)).argmax(1).cpu() == y_val).float().mean()

# Self-attention in 6 lines
def attention(q, k, v):
    w = torch.softmax(q @ k.transpose(-2, -1) / q.size(-1) ** 0.5, dim=-1)
    return w @ v
```

Checklist: `model.train()`/`model.eval()`, `zero_grad`, `no_grad` for eval, move data and model to the same device. See [[Training Tricks]], [[Optimizers]], [[Backpropagation]], [[Transformers]].
