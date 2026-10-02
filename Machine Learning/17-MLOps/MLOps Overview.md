---
tags: [ml, mlops]
---
# MLOps Overview

Getting models into production and keeping them healthy.

| Stage | Practices & tools |
|---|---|
| Data | versioning (DVC, lakeFS), validation (Great Expectations), feature stores (Feast) |
| Experiments | tracking (MLflow, Weights & Biases), configs (Hydra), seeds |
| Training | pipelines (Airflow, Kubeflow, Prefect), distributed training, HPO (Optuna) |
| Packaging | Docker, ONNX, model registry |
| Serving | batch vs online; FastAPI, TorchServe, Triton, BentoML; latency budgets |
| Monitoring | data drift, concept drift, prediction distribution, performance on delayed labels |
| Testing | unit tests for data/feature code, model behavioural tests, canary/shadow deployment, A/B tests |
| Governance | model cards, lineage, reproducibility, privacy |

## Resources
- [Made With ML — MLOps course](https://madewithml.com/)
- [Stanford CS329S — ML Systems Design (Chip Huyen)](https://stanford-cs329s.github.io/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/)
- Book: *Designing Machine Learning Systems* — Chip Huyen (O'Reilly 2022)

See [[ML Workflow]] and [[Common Pitfalls]].
