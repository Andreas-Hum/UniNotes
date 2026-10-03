---
tags: [ml, mlops, deployment]
---
# Model Deployment and Serving

> [!summary] In one sentence
> Deployment turns a trained model into a reliable service: choose batch, online, streaming or on-device serving; package the model and its preprocessing together; meet latency and cost budgets with batching, compression and hardware; and roll out gradually with shadow, canary and A/B releases plus a rollback plan.

## Intuition first
A notebook model answers one question when you press Shift+Enter. A production model answers thousands of questions per second, around the clock, with the *same* preprocessing as in training, within a latency budget, and must be replaceable without downtime. Most ML failures in production are **engineering** failures, not modelling failures.

## Serving patterns
| Pattern | How | Latency | Example | Watch out for |
|---|---|---|---|---|
| **Batch (offline)** | score everything on a schedule, store results in a table | hours | nightly churn scores, recommendations precomputed per user | stale predictions; wasted work for inactive users |
| **Online (real-time)** | request → model → response via REST/gRPC | ms | fraud check at payment, search ranking | latency, availability, scaling |
| **Streaming** | consume events (Kafka), update features/predictions continuously | seconds | anomaly detection on sensor streams | ordering, exactly-once processing |
| **Edge / on-device** | model runs on phone/browser/IoT | ms, offline | keyboard prediction, camera filters | model size, battery, updating devices |
**Rule of thumb:** if a prediction can be a day old, use batch – it is simpler, cheaper and easier to monitor.

## Packaging
- **Serialise** the model *with* its preprocessing (a scikit-learn `Pipeline`, or exported graph) so training and serving code cannot diverge (**training–serving skew**).
- **Formats:** pickle/joblib (Python only, never load untrusted files), **ONNX** (framework-neutral), TorchScript / `torch.export`, TensorFlow SavedModel, GGUF for LLMs.
- **Containers:** Docker image with pinned dependencies → runs the same everywhere; Kubernetes for scaling.
- **Servers:** FastAPI (simple), TorchServe, NVIDIA **Triton**, BentoML, Ray Serve, KServe; **vLLM / TGI** for LLMs.
- **Model registry** (MLflow, W&B): versioned artefacts with stage labels (staging → production) and lineage to the data and code.

## Latency, throughput and cost
- **Latency budget:** e.g. p99 < 100 ms end-to-end. Measure **percentiles** (p50, p95, p99), not averages – the slow tail is what users notice.
- **Little's law:** concurrent requests $L=\lambda W$ (arrival rate × time in system) → how many workers you need.
- **Dynamic batching:** group requests arriving within a few ms into one GPU call – much higher throughput, slightly higher latency.
- **Caching:** identical inputs (popular queries) → reuse results.
- **Model compression:**
  - **Quantisation:** float32 → int8 (4× smaller, 2–4× faster on CPU); post-training or quantisation-aware training. 4-bit for LLMs (GPTQ, AWQ).
  - **Pruning:** remove small weights/channels.
  - **Knowledge distillation:** train a small *student* to match a large *teacher*'s soft outputs: $L=(1-\alpha)\,\mathrm{CE}(y,p_s)+\alpha T^2\,\mathrm{KL}(p_t^{(T)}\Vert p_s^{(T)})$ with temperature $T$.
- **Hardware:** CPU for small tabular models; GPU for deep nets; autoscale on queue length/latency, scale to zero when idle.

## Releasing safely
| Strategy | What happens | Answers |
|---|---|---|
| **Shadow** | new model gets a copy of live traffic; its outputs are logged, not used | Does it run correctly, how do its predictions differ? Zero user risk |
| **Canary** | 1–5 % of traffic goes to the new model, increased if metrics hold | Does it break anything for real users? |
| **A/B test** | random split, compare business metrics with a significance test | Is it actually better? |
| **Blue–green** | two full environments; switch traffic at once, switch back to roll back | Instant rollback |
| **Interleaving / bandits** | mix rankings, or shift traffic adaptively to the winner | Faster comparisons for ranking/recommendation |
Always keep the previous model deployable and define **rollback triggers** (error rate, latency, prediction distribution).

## Worked example: capacity
Peak load 600 requests/s, each takes 40 ms on one worker that handles one request at a time. Concurrency $L=600\times0.04=24$ → at least 24 workers, plus headroom (e.g. 30–35) for spikes and p99 latency. With dynamic batching of 8 requests in 60 ms per batch, one GPU worker handles $8/0.06\approx133$ req/s → about 5 workers.

## Common confusions
- **"The model file is the deliverable."** → The deliverable is model + preprocessing + environment + API + monitoring.
- **"Average latency is fine, so users are happy."** → p99 can be 10× the mean.
- **"Online inference is more advanced, so better."** → It costs more and fails in more ways; choose by freshness requirements.
- **"Quantisation always hurts accuracy a lot."** → int8 typically loses < 1 point; measure on your validation set.

## Check yourself
> [!question]- Which release strategy tests a new fraud model on real traffic with zero risk to customers?
> Shadow deployment.

> [!question]- Why export preprocessing inside the model artefact?
> To prevent training–serving skew: the exact same transformations run in both places.

> [!question]- 200 req/s at 50 ms each – how many single-request workers at minimum?
> $L=200\times0.05=10$ (plus headroom).

## Learn more
- [Made With ML — serving](https://madewithml.com/)
- [Stanford CS329S — ML Systems Design](https://stanford-cs329s.github.io/)
- [Distilling the Knowledge in a Neural Network — Hinton et al. 2015](https://arxiv.org/abs/1503.02531)
- Book: *Designing Machine Learning Systems* — Chip Huyen, ch. 7

See [[MLOps Overview]], [[Experiment Tracking and Reproducibility]], [[Data and Feature Management]].
