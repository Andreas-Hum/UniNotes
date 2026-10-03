---
tags: [ml, mlops, reproducibility]
status: not-started
level:
reviewed:
---
# Experiment Tracking and Reproducibility

> [!summary] In one sentence
> A result is only trustworthy if you can say exactly which **code, data, configuration, environment and random seed** produced it and rerun it – so log every run automatically, version data alongside code, and automate training as a pipeline.

## Intuition first
Three weeks after a great result, someone asks "which settings gave 0.91?" and nobody knows: the notebook was edited, the data was re-exported, a library was upgraded. Reproducibility is insurance: it makes results **comparable** (did the change help, or did the data change?), **auditable** (why did the model make that decision?) and **recoverable** (roll back to last month's model).

## The five things that define a run
| Ingredient | How to pin it |
|---|---|
| **Code** | git commit hash (and refuse to run with uncommitted changes) |
| **Data** | dataset version/hash (DVC, lakeFS, Delta Lake time travel, or a content hash of the files) |
| **Config** | all hyperparameters in a file (YAML/Hydra), logged with the run |
| **Environment** | lock file (`uv.lock`, `poetry.lock`, `requirements.txt` with versions), Docker image, CUDA version |
| **Randomness** | seeds for Python, NumPy, PyTorch; deterministic algorithms where needed |

```python
import random, numpy as np, torch
def seed_everything(seed=42):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```
Even with seeds, some GPU operations are non-deterministic; report **mean ± std over several seeds** rather than one lucky run.

## Experiment tracking
Tools: **MLflow**, **Weights & Biases**, Neptune, Comet, TensorBoard, Aim.
Log per run: config, git hash, data version, metrics over time (loss curves), final metrics, system info, artefacts (model, plots, confusion matrix), and notes ("tried label smoothing").

```python
import mlflow
with mlflow.start_run():
    mlflow.log_params(cfg)                  # hyperparameters
    mlflow.set_tag("git_commit", commit)
    mlflow.log_metric("val_auc", auc)       # call per epoch for curves
    mlflow.sklearn.log_model(model, "model")
```
Benefits: compare runs side by side, sweep hyperparameters (W&B Sweeps, Optuna), and promote the chosen model to a **registry**.

## Data versioning
- **DVC:** git-like commands for large files; git stores small pointer files, the data lives in S3/GCS/a drive.
- **Lakehouse tables** (Delta Lake, Iceberg): query a table "as of" a timestamp or version.
- At minimum: write data snapshots to immutable, dated paths and log the path + hash.

## Pipelines and automation
Turn notebook steps into a **pipeline** of steps: ingest → validate → featurise → train → evaluate → register.
- Orchestrators: Airflow, Prefect, Dagster, Kubeflow Pipelines, ZenML, Metaflow.
- Each step is cached and re-runs only when its inputs change.
- **CI/CD for ML:** on every commit run unit tests (feature code), data-validation tests and a small training smoke test; **continuous training** retrains on a schedule or trigger, with an automatic evaluation gate against the current production model before promotion.
- **Lineage:** link each deployed model to the run, data version and code that produced it.

## MLOps maturity (Google's levels)
| Level | Description |
|---|---|
| 0 – manual | notebooks, manual hand-off of a model file |
| 1 – ML pipeline automation | automated, reproducible training pipeline; continuous training |
| 2 – CI/CD pipeline automation | the pipeline itself is tested and deployed automatically |

## Worked example: why seeds and repeats matter
Model A scores 0.842, model B 0.848 on one run each. Repeating five seeds gives A $=0.843\pm0.004$, B $=0.845\pm0.005$. The difference (0.002) is smaller than the seed noise – there is no evidence B is better. A paired test over the same seeds/folds is the right comparison ([[Research Skills]]).

## Common confusions
- **"Saving the model file = reproducible."** → Without the data version, code and environment you cannot retrain or explain it.
- **"Notebook outputs are my experiment log."** → They are overwritten and not searchable; use a tracker.
- **"Setting a seed guarantees identical results."** → Not across hardware, library versions or some GPU kernels.
- **"Tracking is only for big teams."** → It saves a solo student the most time (thesis!).

## Check yourself
> [!question]- Name the five things you need to pin to reproduce a training run.
> Code (commit), data (version/hash), config (hyperparameters), environment (dependencies/container), random seeds.

> [!question]- How does DVC store a 20 GB dataset alongside a git repo?
> Git tracks small `.dvc` pointer files with hashes; the data itself lives in remote storage and is fetched with `dvc pull`.

> [!question]- What is "continuous training"?
> A pipeline that retrains the model automatically (on a schedule or trigger such as drift) and promotes it only if it passes evaluation gates.

## Learn more
- [MLflow docs](https://mlflow.org/docs/latest/index.html) · [Weights & Biases docs](https://docs.wandb.ai/) · [DVC](https://dvc.org/doc)
- Google Cloud, *MLOps: Continuous delivery and automation pipelines in machine learning* (source of the maturity levels)
- Sculley et al. (2015), *Hidden Technical Debt in Machine Learning Systems*, NeurIPS

See [[MLOps Overview]], [[Model Deployment and Serving]], [[Data and Feature Management]], [[Research Skills]].
