---
tags: [ml, fundamentals, workflow]
---
# ML Workflow

1. **Frame the problem** — task, metric, baseline, constraints.
2. **Collect & inspect data** — distributions, leakage, label quality.
3. **Split** — before looking at test data. [[Cross-Validation and Model Selection]]
4. **Preprocess & engineer features** — [[Data Preprocessing]], [[Feature Engineering]].
5. **Baseline** — dummy model, then [[Logistic Regression]] / [[Linear Regression]].
6. **Iterate models** — [[Ensemble Methods]], [[Neural Networks]].
7. **Error analysis** — where does it fail? slices, confusion matrix.
8. **Evaluate once on test** — [[Model Evaluation and Metrics]].
9. **Deploy & monitor** — drift, latency, retraining.

Checklist of mistakes: [[Common Pitfalls]]. Exam version: [[Exam Checklist]].

## Learn more
- [Made With ML](https://madewithml.com/)
- [scikit-learn – choosing an estimator](https://scikit-learn.org/stable/machine_learning_map.html)
