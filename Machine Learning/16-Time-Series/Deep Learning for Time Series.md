---
tags: [ml, time-series, deep-learning]
---
# Deep Learning for Time Series

> [!summary] In one sentence
> Neural forecasters (RNNs, TCNs, N-BEATS, Temporal Fusion Transformer, PatchTST, foundation models) shine when you have **many related series** and rich covariates, learning one global model across all of them – but on a single short series a tuned ETS/ARIMA or gradient boosting model often still wins.

## Intuition first
Classical models fit **one model per series**. A retailer with 50,000 products × 1,000 stores has 50 million series, many short and noisy. A **global** neural model trained on all of them can share patterns ("products with a Christmas spike", "weekend effects") and forecast new series with little history. That is where deep learning pays off.

## Framing the problem
- **Window:** input the last $L$ steps (lookback) → output the next $H$ steps (horizon).
- **Covariates:** *past* (only known up to now: past sales), *future-known* (calendar, holidays, planned promotions), *static* (store, category).
- **Multi-step strategy:** *recursive* (predict one step, feed it back – errors compound) vs *direct/multi-output* (predict all $H$ at once – usual for neural models).
- **Scaling:** normalise each series (e.g. divide by its mean, or **RevIN**: instance normalisation removed after prediction) so the model sees comparable shapes.
- **Probabilistic output:** predict quantiles (pinball loss) or distribution parameters (DeepAR) instead of a single number.

## Model families
| Model | Year | Idea |
|---|---|---|
| **LSTM/GRU seq2seq** | – | encoder reads the past, decoder emits the future ([[RNN and LSTM]]) |
| **DeepAR** (Amazon) | 2017 | autoregressive RNN, global over many series, outputs a likelihood (Gaussian, negative binomial) → probabilistic forecasts |
| **TCN** | 2018 | causal, **dilated** 1-D convolutions; receptive field grows exponentially; parallel training |
| **N-BEATS** | 2019 | stacks of fully connected blocks with **backward/forward residuals**; interpretable trend/season basis option; won on M4 |
| **N-HiTS** | 2022 | N-BEATS with multi-rate sampling – better long horizons, cheaper |
| **Temporal Fusion Transformer (TFT)** | 2019 | LSTM + attention + gating + variable selection; handles static/past/future covariates; interpretable |
| **Informer / Autoformer / FEDformer** | 2021–22 | efficient attention for long horizons |
| **DLinear** | 2022 | a single linear layer on decomposed series beat many Transformers – a sanity check |
| **PatchTST** | 2023 | split each series into **patches** as tokens (like ViT), channel-independent → strong long-horizon results |
| **Foundation models** (TimesFM, Chronos, Moirai, Lag-Llama) | 2023–24 | pretrained on huge corpora of series; **zero-shot** forecasts for new series |

### Causal dilated convolution (TCN)
Output at time $t$ only uses inputs $\le t$: $y_t=\sum_{i=0}^{k-1}w_i\,x_{t-d\cdot i}$ with dilation $d$. With kernel $k$ and dilations $1,2,4,\dots,2^{L-1}$, the receptive field is $1+(k-1)(2^L-1)$: kernel 2 and 10 layers see 1,024 steps.

### N-BEATS block
Each block takes the residual input $x_\ell$, outputs a **backcast** $\hat x_\ell$ and a **forecast** $\hat y_\ell$; the next block gets $x_{\ell+1}=x_\ell-\hat x_\ell$ (what is still unexplained). The final forecast is $\sum_\ell\hat y_\ell$. Like boosting inside one network.

### Pinball (quantile) loss
For quantile $\tau\in(0,1)$ and error $u=y-\hat y_\tau$:
$$\rho_\tau(u)=\max(\tau u,\,(\tau-1)u)$$
For $\tau=0.9$, under-forecasting costs 9× more than over-forecasting, so the model learns the 90th percentile.

## When does deep learning win?
| Situation | Usually best |
|---|---|
| one or few short series | ETS/ARIMA, Theta, seasonal naive ([[Classical Forecasting Models]]) |
| many series + tabular covariates | **gradient boosting (LightGBM) with lag features** – won M5 ([[Time Series Validation and Features]]) |
| many long series, complex covariates, need for probabilistic output | DeepAR, TFT, N-HiTS, PatchTST |
| new series, no time to train | foundation models (zero-shot), then fine-tune |
Ensembles of statistical + ML models are hard to beat (M4/M5 competitions).

## Common confusions
- **"Transformers must be best because they win in NLP."** → DLinear showed many long-horizon Transformers were beaten by a linear model; patching and channel independence were what made PatchTST work.
- **"Randomly shuffle windows into train/validation."** → Overlapping windows leak the future; split by time ([[Time Series Validation and Features]]).
- **"Recursive forecasting is free."** → Errors compound over the horizon.
- **"Global model = loses per-series detail."** → Static embeddings and per-series scaling let it adapt.

## Check yourself
> [!question]- A TCN with kernel size 3 and dilations 1, 2, 4, 8. What is its receptive field?
> $1+(3-1)(1+2+4+8)=31$ steps.

> [!question]- What is the pinball loss for $\tau=0.9$ when the truth is 100 and the prediction 80? And when the prediction is 120?
> Under-forecast: $u=20$ → $0.9\cdot20=18$. Over-forecast: $u=-20$ → $(0.9-1)(-20)=2$.

> [!question]- Why does a global model help with the "cold start" of a new product?
> It has learned patterns shared across many similar series and can use static features (category, store) even when the new series has little history.

## Learn more
- [DeepAR — Salinas et al. 2017](https://arxiv.org/abs/1704.04110)
- [N-BEATS — Oreshkin et al. 2019](https://arxiv.org/abs/1905.10437)
- [Temporal Fusion Transformer — Lim et al. 2019](https://arxiv.org/abs/1912.09363)
- [Are Transformers Effective for Time Series Forecasting? (DLinear) — Zeng et al. 2022](https://arxiv.org/abs/2205.13504)
- [PatchTST — Nie et al. 2022](https://arxiv.org/abs/2211.14730)
- Libraries: Nixtla `neuralforecast`, Darts, GluonTS, PyTorch Forecasting

See [[Time Series Forecasting]], [[Classical Forecasting Models]], [[Transformers]].
