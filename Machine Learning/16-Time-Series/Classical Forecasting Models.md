---
tags: [ml, time-series, statistics]
status: not-started
level:
reviewed:
---
# Classical Forecasting Models

> [!summary] In one sentence
> Exponential smoothing (ETS) forecasts by updating level, trend and season with weighted averages that forget the past exponentially, while ARIMA models the series as a linear function of its own past values and past errors after differencing it to stationarity – and both remain hard-to-beat baselines.

## Intuition first
- **Exponential smoothing:** "tomorrow is like today, adjusted a bit by how wrong I was." Recent observations get more weight, old ones fade.
- **ARIMA:** "today's value is a linear combination of the last few values (AR) and the last few surprises (MA)", applied to the series after removing trend by differencing (I).
- **Baselines first.** Always compare with **naive** ($\hat y_{t+h}=y_t$), **seasonal naive** ($\hat y_{t+h}=y_{t+h-m}$) and the mean. A fancy model that loses to seasonal naive is useless.

## Decomposition
$$y_t=T_t+S_t+R_t\ (\text{additive})\qquad y_t=T_t\cdot S_t\cdot R_t\ (\text{multiplicative})$$
Trend $T$, seasonality $S$ (period $m$: 12 for monthly, 7 for daily with weekly pattern, 24 for hourly), remainder $R$. Use multiplicative (or log-transform) when the seasonal swings grow with the level. **STL** is a robust decomposition method.

## Exponential smoothing (ETS)
### Simple exponential smoothing (level only)
$$\ell_t=\alpha y_t+(1-\alpha)\ell_{t-1},\qquad \hat y_{t+h|t}=\ell_t,\qquad 0<\alpha<1$$
Unrolled: $\ell_t=\alpha y_t+\alpha(1-\alpha)y_{t-1}+\alpha(1-\alpha)^2y_{t-2}+\dots$ – exponentially decaying weights. Large $\alpha$ reacts fast; small $\alpha$ smooths.

### Holt (level + trend)
$$\ell_t=\alpha y_t+(1-\alpha)(\ell_{t-1}+b_{t-1}),\quad b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1},\quad \hat y_{t+h}=\ell_t+hb_t$$
A **damped trend** ($\hat y_{t+h}=\ell_t+(\phi+\phi^2+\dots+\phi^h)b_t$, $0<\phi<1$) usually forecasts better over long horizons.

### Holt–Winters (level + trend + season)
Additive version, season length $m$:
$$\ell_t=\alpha(y_t-s_{t-m})+(1-\alpha)(\ell_{t-1}+b_{t-1})$$
$$b_t=\beta(\ell_t-\ell_{t-1})+(1-\beta)b_{t-1}$$
$$s_t=\gamma(y_t-\ell_{t-1}-b_{t-1})+(1-\gamma)s_{t-m}$$
$$\hat y_{t+h}=\ell_t+hb_t+s_{t+h-m(k+1)},\qquad k=\lfloor (h-1)/m\rfloor$$
(i.e. use the most recent estimate of the matching season).
ETS(Error, Trend, Season) is the state-space family: each component None/Additive/Multiplicative (+damped), fitted by maximum likelihood and selected by AICc.

## ARIMA
### Stationarity and differencing
ARIMA needs a **stationary** series (constant mean/variance, autocovariance depends only on the lag). Remove trend with first differences $y'_t=y_t-y_{t-1}$, seasonality with seasonal differences $y_t-y_{t-m}$. Test with **ADF** (null: unit root = non-stationary) or **KPSS** (null: stationary).

### The parts
With the backshift operator $By_t=y_{t-1}$:
- **AR(p):** $y_t=c+\phi_1y_{t-1}+\dots+\phi_py_{t-p}+\varepsilon_t$
- **MA(q):** $y_t=c+\varepsilon_t+\theta_1\varepsilon_{t-1}+\dots+\theta_q\varepsilon_{t-q}$
- **ARIMA(p,d,q):** $(1-\phi_1B-\dots-\phi_pB^p)(1-B)^dy_t=c+(1+\theta_1B+\dots+\theta_qB^q)\varepsilon_t$
- **SARIMA(p,d,q)(P,D,Q)$_m$** adds the same terms at seasonal lags; **ARIMAX/SARIMAX** add external regressors (holidays, price, weather).

### Choosing orders with ACF/PACF
| Pattern | ACF | PACF |
|---|---|---|
| AR(p) | decays gradually | **cuts off after lag p** |
| MA(q) | **cuts off after lag q** | decays gradually |
| ARMA | both decay | both decay |
In practice: `auto_arima` / `AutoARIMA` searches orders by AICc; check that residuals look like white noise (**Ljung–Box test**).

### AR(1) intuition
$y_t=\phi y_{t-1}+\varepsilon_t$ is stationary iff $|\phi|<1$; then forecasts decay geometrically to the mean: $\hat y_{t+h}=\phi^hy_t$ (for $c=0$). $\phi=1$ is a random walk: the best forecast is the last value (naive).

## Prediction intervals
A point forecast is not enough. For a random walk the $h$-step forecast variance is $h\sigma^2$, so intervals widen like $\sqrt h$: $\hat y_{t+h}\pm1.96\,\sigma\sqrt h$. ETS and ARIMA give analytic intervals; check their **coverage** on backtests.

## Other classical tools
- **Prophet:** trend + Fourier seasonality + holidays, robust and easy for business data.
- **Croston / TSB:** intermittent demand (many zeros).
- **Hierarchical reconciliation:** make store-level forecasts add up to region and total.
- **VAR:** several series that influence each other.

## Worked example: simple exponential smoothing
$\alpha=0.5$, $\ell_0=10$, observations $12, 11, 15$.
$\ell_1=0.5\cdot12+0.5\cdot10=11$; $\ell_2=0.5\cdot11+0.5\cdot11=11$; $\ell_3=0.5\cdot15+0.5\cdot11=13$. Forecast for every future step: **13** (SES forecasts are flat).

## Common confusions
- **"ARIMA works on any series."** → It needs stationarity after differencing; strong multiple seasonalities (hourly data) suit TBATS, Prophet, MSTL or ML models better.
- **"Lower in-sample error = better model."** → Compare on **out-of-sample** backtests; use AICc only within one model family.
- **"Over-differencing is harmless."** → It adds artificial negative autocorrelation and inflates variance.
- **"Exponential smoothing is just a moving average."** → Weights decay exponentially rather than being equal over a window.

## Check yourself
> [!question]- The ACF cuts off after lag 2 and the PACF decays slowly. Which model is suggested?
> MA(2).

> [!question]- Monthly sales with a yearly pattern whose amplitude grows with the level – additive or multiplicative seasonality?
> Multiplicative (or log-transform and use additive).

> [!question]- Why must every forecasting model be compared with seasonal naive?
> It costs nothing and is often surprisingly good; if a model cannot beat it, its complexity is not justified.

## Practice
**Project:** [[Project - Forecasting Aalborg Temperature]] – forecast Aalborg's temperature with climatology + an AR(1) anomaly

## Learn more
- [Hyndman & Athanasopoulos — *Forecasting: Principles and Practice* (free)](https://otexts.com/fpp3/) – chapters 8 (ETS) and 9 (ARIMA)
- `statsmodels`, Nixtla `statsforecast`, `pmdarima`

See [[Time Series Forecasting]], [[Time Series Validation and Features]], [[Deep Learning for Time Series]].
