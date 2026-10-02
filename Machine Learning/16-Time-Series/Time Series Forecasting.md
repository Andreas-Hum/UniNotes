---
tags: [ml, time-series]
---
# Time Series Forecasting

> [!summary] In one sentence
> Forecasting predicts future values of a sequence from its own past (and maybe other signals) by modelling trend, seasonality and the autocorrelation left over, and it must be evaluated strictly forward in time against simple baselines.

## Intuition first

A time series is a sequence of measurements in time order: daily sales, hourly electricity load, monthly airline passengers. What makes it different from ordinary tabular data is that **order matters and the rows are not independent**: today's value is strongly related to yesterday's.

A useful mental model is that a series is the sum of a few simple stories:

- **Trend**: the slow long-run drift (sales growing year on year).
- **Seasonality**: a pattern that repeats with a *fixed, known* period (more ice cream every summer, more traffic every Monday morning).
- **Cycles**: rises and falls *without* a fixed period (business cycles lasting "a few years").
- **Noise**: the irregular part you cannot predict.

Forecasting then means: extend the trend, repeat the seasonal pattern, and put honest uncertainty bands around the noise. Every model in the table below is a different way of doing that, from "tomorrow = today" to deep networks.

![A series built up from trend, seasonality and remainder](../../Attachments/ML%20Animations/Time%20Series%20Forecasting%20-%20trend%20season%20remainder.gif)

*Watch the straight trend line bend into a repeating 12-month wave, then get roughened by noise: the observed series is just these three layers added together, which is what decomposition methods (STL, Prophet) try to undo.*

The other big lesson is about **evaluation**. Because the future is unknown at prediction time, a model must never be trained on data that comes after the period it is tested on. Shuffling rows into random folds, as in normal cross-validation, lets the model peek at the future and makes it look far better than it is.

## Concepts

Trend, seasonality, cycles, noise; **stationarity** (ADF/KPSS tests, differencing); autocorrelation (ACF/PACF).

### Stationarity

A series is (weakly) **stationary** if its mean, variance and autocorrelation structure do not change over time. Many classical models (ARMA) assume it, because then the past is a reliable guide to the future's *statistical behaviour*. A trend (changing mean) or growing seasonal swings (changing variance) break it.

- **Differencing** removes trends: $\nabla y_t=y_t-y_{t-1}$. A linear trend $y_t=a+bt$ becomes the constant $b$. A random walk $y_t=y_{t-1}+\varepsilon_t$ (non-stationary: its variance grows with $t$) becomes white noise $\varepsilon_t$.
- **Seasonal differencing** removes a period-$m$ pattern: $\nabla_my_t=y_t-y_{t-m}$.
- A log transform first stabilises variance that grows with the level.
- **ADF test** (augmented Dickey–Fuller): regress $\Delta y_t=\alpha+\gamma y_{t-1}+(\text{lagged }\Delta y)+e_t$; $H_0$: unit root ($\gamma=0$, non-stationary). Reject → evidence of stationarity. Its test statistic does *not* follow a normal t-distribution, so special critical values are used.
- **KPSS test**: the opposite null, $H_0$: stationary. Using both is informative: ADF rejects and KPSS does not → stationary.

### Autocorrelation: ACF and PACF

- **ACF** at lag $k$: the correlation between $y_t$ and $y_{t-k}$. Sample version $r_k=\frac{\sum_t(y_t-\bar y)(y_{t-k}-\bar y)}{\sum_t(y_t-\bar y)^2}$. A slowly decaying ACF signals a trend (non-stationary); spikes at lags $m,2m,\dots$ signal seasonality.
- **PACF** at lag $k$: the correlation between $y_t$ and $y_{t-k}$ *after removing the effect of lags $1,\dots,k-1$*; equivalently, the last coefficient when you regress $y_t$ on $y_{t-1},\dots,y_{t-k}$.
- Reading them: an **AR($p$)** process has a PACF that cuts off after lag $p$ and an ACF that decays; an **MA($q$)** process has an ACF that cuts off after lag $q$ and a PACF that decays.

## The math, step by step

**Naive and seasonal naive** (baselines): $\hat y_{T+h\mid T}=y_T$ ("tomorrow = today"), and $\hat y_{T+h\mid T}=y_{T+h-m}$ for $h\le m$ ("this July = last July").

**Simple exponential smoothing (SES):**
$$\ell_t=\alpha y_t+(1-\alpha)\ell_{t-1},\qquad\hat y_{T+h\mid T}=\ell_T.$$
The level $\ell_t$ is a weighted average of all past observations with weights $\alpha,\alpha(1-\alpha),\alpha(1-\alpha)^2,\dots$ that decay exponentially into the past. $\alpha$ near 1 → react quickly (close to naive); $\alpha$ near 0 → very smooth (close to the long-run mean). The forecast is flat.

**Holt's linear trend** adds a slope $b_t$:
$$\ell_t=\alpha y_t+(1-\alpha)(\ell_{t-1}+b_{t-1}),\quad b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1},\quad\hat y_{T+h}=\ell_T+hb_T.$$
**Holt–Winters** adds a seasonal component as well; **ETS** (Error, Trend, Seasonal) is the state-space framework that contains all of these and gives likelihoods and prediction intervals.

**AR($p$):** $y_t=c+\phi_1y_{t-1}+\dots+\phi_py_{t-p}+\varepsilon_t$: regress the series on its own past (fit by least squares). For AR(1), $y_t=c+\phi y_{t-1}+\varepsilon_t$ with $|\phi|<1$:
- stationary mean $\mu=c/(1-\phi)$ (take expectations of both sides and set $\mathbb E y_t=\mathbb Ey_{t-1}=\mu$);
- variance $\gamma_0=\sigma^2/(1-\phi^2)$; autocorrelation $\rho_k=\phi^k$;
- forecasts decay geometrically towards $\mu$: $\hat y_{T+h}-\mu=\phi^h(y_T-\mu)$. Multi-step forecasts are made *recursively* by feeding forecasts back in.

**MA($q$):** $y_t=\mu+\varepsilon_t+\theta_1\varepsilon_{t-1}+\dots+\theta_q\varepsilon_{t-q}$: the value depends on recent *shocks*.

**ARIMA($p,d,q$):** difference $d$ times to get stationarity, then fit ARMA($p,q$). **SARIMA** adds seasonal AR/MA/differencing terms $(P,D,Q)_m$; the **X** stands for exogenous regressors (price, holidays, temperature).

## Models

| Family | Examples |
|---|---|
| Baselines | naive, seasonal naive, moving average — always compare! |
| Exponential smoothing | SES, Holt, Holt–Winters, ETS |
| ARIMA family | AR, MA, ARIMA, SARIMA(X) |
| Decomposition | STL, Prophet |
| ML with lag features | LightGBM/XGBoost on lags, rolling stats, calendar features ([[Ensemble Methods]]) |
| Deep | [[RNN and LSTM]], TCN, N-BEATS, DeepAR, Temporal Fusion Transformer, PatchTST |
| State space | Kalman filters ([[Probabilistic Graphical Models]]) |

Why each exists:
- **Baselines** are often hard to beat, and they define the scale of metrics like MASE. A complex model that loses to seasonal naive is not worth deploying.
- **Exponential smoothing** and **ARIMA** are cheap, interpretable and strong on single, regular series.
- **Decomposition**: STL splits a series into trend + seasonal + remainder with local regression; Prophet fits trend + seasonalities + holiday effects as a regression, robust to missing data and easy for analysts.
- **ML with lag features** turns forecasting into tabular regression: features such as $y_{t-1}$, $y_{t-7}$, rolling means and standard deviations, day-of-week, month and holiday flags. Gradient boosting shines when you have many related series (thousands of products) and external features. Careful: every feature must be computable at prediction time (rolling windows must end *before* the target).
- **Deep models** learn across many series: DeepAR (probabilistic RNN), N-BEATS (stacked MLP blocks), TCN (dilated convolutions), Temporal Fusion Transformer and PatchTST (attention-based).
- **State-space / Kalman filters** track a hidden state (level, slope) that evolves over time and is observed with noise, handle missing values naturally and give exact uncertainty under Gaussian assumptions.

## Evaluation

Rolling-origin / time-series CV — never shuffle ([[Cross-Validation and Model Selection]]). Metrics: MAE, RMSE, MAPE, sMAPE, MASE; probabilistic: pinball loss, CRPS.

**Rolling-origin evaluation** (also "time-series CV" or "backtesting"): pick a forecast origin, train on everything before it, forecast the next $h$ steps, record the error; move the origin forward and repeat; average the errors over folds. Each fold respects time, and the average over several origins is far more reliable than a single train/test split.

![Rolling-origin evaluation with a seasonal-naive forecaster](../../Attachments/ML%20Animations/Time%20Series%20Forecasting%20-%20rolling-origin%20evaluation.gif)

*Watch the shaded training window grow while the orange test block always sits strictly after it; each fold produces one error, and the final score is their average.*

**Point metrics** (with errors $e_t=y_t-\hat y_t$):
- **MAE** $=\frac1n\sum|e_t|$: in the units of the data, robust; optimal forecast is the median.
- **RMSE** $=\sqrt{\frac1n\sum e_t^2}$: punishes large errors more; optimal forecast is the mean. Prefer it when big misses are especially costly.
- **MAPE** $=\frac{100}{n}\sum|e_t/y_t|$: scale-free percentages, but explodes when $y_t$ is near 0 (intermittent demand) and is asymmetric (penalises over-forecasts more heavily than under-forecasts of the same size, because under-forecast errors are capped at 100 %).
- **sMAPE** $=\frac{100}{n}\sum\frac{2|e_t|}{|y_t|+|\hat y_t|}$: tries to fix the asymmetry by dividing by the average of actual and forecast; still unstable near 0.
- **MASE** $=\mathrm{MAE}/Q$, where $Q=\frac1{T-1}\sum_{t=2}^T|y_t-y_{t-1}|$ is the in-sample MAE of the one-step naive forecast (or the seasonal naive for seasonal data). Scale-free and comparable across series; **MASE < 1** means you beat the naive benchmark.

**Probabilistic metrics.** A good forecast says how uncertain it is.
- **Pinball (quantile) loss** for a quantile forecast $q$ at level $\tau$: $\rho_\tau(y,q)=\tau(y-q)$ if $y\ge q$, else $(1-\tau)(q-y)$. Its expected value is minimised when $q$ is the true $\tau$-quantile. For $\tau=0.9$, being below the truth costs 9× more than being above, which pushes $q$ up to the 90th percentile.
- **CRPS** generalises this to a whole predictive distribution (it equals twice the pinball loss integrated over all $\tau$); for a point forecast it reduces to MAE.
- **Coverage**: an 80 % prediction interval should contain about 80 % of the actual values. Too low → overconfident.

## Worked example

**SES by hand.** $\alpha=0.3$, $\ell_0=20$, observations $y=(22,18,24)$.
- $\ell_1=0.3\cdot22+0.7\cdot20=20.6$
- $\ell_2=0.3\cdot18+0.7\cdot20.6=19.82$
- $\ell_3=0.3\cdot24+0.7\cdot19.82=21.07$

Forecast for every future step: $21.07$. Weight on the latest observation: $0.3$; on the one before: $0.21$; then $0.147$.

**AR(1) forecasting.** $c=2$, $\phi=0.5$ → $\mu=2/(1-0.5)=4$. If $y_T=8$: $\hat y_{T+1}=2+0.5\cdot8=6$, $\hat y_{T+2}=2+0.5\cdot6=5$, $\hat y_{T+3}=4.5$, … halving the gap to the mean each step, since $\hat y_{T+h}-4=0.5^h(8-4)$.

**MASE.** Training data $(5,7,6,8)$: naive in-sample errors $|7-5|,|6-7|,|8-6|=2,1,2$, so $Q=5/3\approx1.67$. A model forecasts $(8,8)$; actuals are $(9,6)$: MAE $=(1+2)/2=1.5$, MASE $=1.5/1.67=0.9<1$ → slightly better than naive.

**Pinball loss.** $\tau=0.9$, $q=50$. If $y=60$: $0.9\cdot10=9$. If $y=40$: $0.1\cdot10=1$. Under-predicting a 90 % quantile is expensive.

**Differencing.** $y_t=5+3t$ gives $(5,8,11,14,\dots)$; $\nabla y_t=(3,3,3,\dots)$, constant: the trend is gone.

## Common confusions

- **"I can use normal k-fold CV."** → Shuffled folds train on the future and test on the past; autocorrelation makes the leak large. Use rolling-origin evaluation.
- **"Seasonality and cycles are the same."** → Seasonality has a fixed, known period (12 months, 7 days); cycles have irregular length and are much harder to forecast.
- **"A low MAPE is always good."** → MAPE is undefined or huge near zero and asymmetric; prefer MASE or MAE for intermittent or near-zero series.
- **"ADF and KPSS test the same null."** → ADF's null is *non-stationary* (unit root); KPSS's null is *stationary*. Failing to reject is not proof of either.
- **"Lag features are harmless."** → A rolling mean that includes the target day, or a feature only known after the fact, leaks the answer. Every feature must be available at forecast time.
- **"A deep model will beat the baselines."** → Often not, especially on a single short series. Always report the naive and seasonal-naive scores next to your model.

## Check yourself

> [!question]- The ACF of your series decays very slowly and stays high for many lags. What does that suggest, and what do you do?
> Non-stationarity (a trend or unit root). Difference the series (and check with ADF/KPSS) before fitting an ARMA model.

> [!question]- PACF has significant spikes at lags 1 and 2 and nothing after; ACF decays gradually. Which model?
> AR(2): the PACF cuts off after lag $p=2$.

> [!question]- A model's MASE on a test set is 1.3. Interpret it.
> Its MAE is 30 % worse than that of the in-sample naive forecast; it does not beat the simple benchmark.

> [!question]- With SES, what forecast do you get for 1 step ahead vs 10 steps ahead?
> The same value $\ell_T$: SES forecasts are flat. Use Holt (trend) or Holt–Winters (season) if the series has those.

> [!question]- Why must the 80 % prediction interval's empirical coverage be checked on a rolling-origin backtest rather than in-sample?
> In-sample residuals are optimistically small (the model was fitted to them), so in-sample coverage overstates reliability. Forward-in-time evaluation reflects real forecasting conditions.

## Practice

[Time Series Forecasting - Exercises](Time%20Series%20Forecasting%20-%20Exercises.ipynb): stationarity and differencing, reading ACF/PACF, naive vs seasonal naive, SES and Holt, AR(p) by least squares, a Dickey–Fuller regression, MASE and pinball loss by hand, lag features with rolling-origin evaluation, and prediction-interval coverage.

## Resources
- [Hyndman & Athanasopoulos — *Forecasting: Principles and Practice* (free)](https://otexts.com/fpp3/)
- Libraries: statsmodels, Prophet, sktime, Darts, Nixtla (statsforecast/neuralforecast), GluonTS
