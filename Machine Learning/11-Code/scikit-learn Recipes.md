---
tags: [ml, code, sklearn]
---
# scikit-learn Recipes

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

# Pipeline avoids leakage (scaler is fit inside each CV fold)
pipe = make_pipeline(StandardScaler(), SVC(kernel="rbf"))
scores = cross_val_score(pipe, X_tr, y_tr, cv=StratifiedKFold(5, shuffle=True, random_state=0))

# Hyperparameter search
grid = GridSearchCV(pipe, {"svc__C": [0.1, 1, 10, 100], "svc__gamma": [1e-3, 1e-2, 1e-1]}, cv=5)
grid.fit(X_tr, y_tr)
print(grid.best_params_, grid.score(X_te, y_te))

print(classification_report(y_te, grid.predict(X_te)))

# Unsupervised
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
Z = PCA(n_components=2).fit_transform(StandardScaler().fit_transform(X))
labels = KMeans(n_clusters=3, n_init=10).fit_predict(Z)
```

Concepts: [[Cross-Validation and Model Selection]], [[Support Vector Machines]], [[Ensemble Methods]], [[Clustering]], [[PCA]], [[Gaussian Mixture Models and EM]].

## Learn more
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)
