---
tags: [ml, mlops, data]
---
# Data and Feature Management

> [!summary] In one sentence
> Most production ML problems are data problems, so treat data like code: validate it with explicit expectations, compute features once and serve them consistently (feature stores, point-in-time joins), and keep labels, lineage and privacy under control.

## Intuition first
A model is a function of its training data. If a column silently changes from euros to cents, a join duplicates rows, or a feature is computed one way in training and another way online, the model degrades – often **without any error message**. Data management is about catching those problems before the model does.

## Data validation
Write **expectations** about each dataset and check them in the pipeline before training and before scoring:
- **Schema:** columns, types, allowed categories.
- **Values:** ranges (age in 0–120), not-null rates, uniqueness of keys.
- **Distributions:** mean/quantiles within bounds; compare to a reference with PSI/KS ([[MLOps Overview]]).
- **Volume and freshness:** row count roughly as expected, latest timestamp recent.
- **Label sanity:** class balance, label delay.
Tools: Great Expectations, Pandera, TFX Data Validation, Soda, dbt tests.

```python
import pandera as pa
schema = pa.DataFrameSchema({
    "age": pa.Column(int, pa.Check.in_range(0, 120)),
    "country": pa.Column(str, pa.Check.isin(["DK", "SE", "NO"])),
    "amount": pa.Column(float, pa.Check.ge(0), nullable=False),
})
schema.validate(df)        # raises with a report if violated
```

## Feature stores
A **feature store** (Feast, Tecton, Databricks, SageMaker, Vertex AI) gives one definition per feature, computed once, and serves it in two places:
- **Offline store** (warehouse/lake): historical feature values for training.
- **Online store** (Redis/DynamoDB): latest values with millisecond lookup for serving.
Benefits: no training–serving skew, reuse across teams, discoverability, monitoring.

### Point-in-time correctness
When building training data, each label at time $t$ must be joined with feature values **as they were at $t$**, not today's values. Otherwise future information leaks in.

| user | label time | label (churned) | "orders last 30 days" – correct (as of label time) | wrong (as of today) |
|---|---|---|---|---|
| u1 | 2026-03-01 | 1 | 4 | 0 (they already left) |
The wrong version makes "0 orders" look like a perfect churn predictor – but at prediction time you never know that yet. Feature stores do these **as-of joins** for you (`pandas.merge_asof` by hand).

## Labels
- **Sources:** human annotation, implicit feedback (clicks, purchases), heuristics/weak supervision (Snorkel), LLM-assisted labelling.
- **Quality:** inter-annotator agreement (Cohen's κ), clear guidelines, audit samples; find label errors with confident learning (cleanlab).
- **Label delay:** fraud labels may arrive weeks later → monitoring and retraining must wait for them.
- **Active learning:** label the examples the model is least sure about first.

## Lineage, governance and privacy
- **Lineage:** which raw sources and transformations produced each feature and model (OpenLineage, dbt docs).
- **Data contracts:** producers promise a schema and semantics; breaking changes are versioned.
- **Privacy:** minimise personal data, pseudonymise, control access, define retention/deletion (GDPR – see the [[9-semester/IT-lov/Noter/Lektion 2 - Aktører og behandlingsprincipper|IT-ret notes]] on purpose limitation and data minimisation); deleting a user may require retraining or "machine unlearning".
- **Documentation:** *Datasheets for Datasets* and *Model Cards* record origin, intended use and limitations.

## Common confusions
- **"More data fixes everything."** → More wrong or leaky data makes things worse; quality beats quantity.
- **"Validation is a one-off notebook check."** → It must run automatically on every new batch.
- **"Joining on user id is enough."** → Without time, you leak the future; use point-in-time joins.
- **"Feature stores are only for big companies."** → The idea – one feature definition used in training and serving – matters at any size.

## Check yourself
> [!question]- Why is "number of support tickets in the 30 days after the label date" leakage in a churn model?
> It uses information from after the prediction time, which will not exist when the model is used.

> [!question]- What are the offline and online stores of a feature store for?
> Offline: historical values for building training sets (point-in-time joins). Online: low-latency latest values for real-time inference.

> [!question]- Give three expectations you would write for a transactions table.
> E.g. `amount >= 0` and not null; `currency` in an allowed set; transaction id unique; daily row count within ±30 % of the last week's average; latest timestamp less than a day old.

## Learn more
- [Feast docs](https://docs.feast.dev/) · [Great Expectations](https://docs.greatexpectations.io/) · [Pandera](https://pandera.readthedocs.io/)
- [Datasheets for Datasets — Gebru et al. 2018](https://arxiv.org/abs/1803.09010) · [Model Cards — Mitchell et al. 2018](https://arxiv.org/abs/1810.03993)
- [Confident Learning (cleanlab) — Northcutt et al. 2019](https://arxiv.org/abs/1911.00068)

See [[MLOps Overview]], [[Data Preprocessing]], [[Common Pitfalls]], [[Model Deployment and Serving]].
