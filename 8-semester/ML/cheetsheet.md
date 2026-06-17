# Ultimate Linear Model & Multi-Class Classifier Cheat Sheet

## 1. Linear Algebra & Regression Layouts

| Data Layout | Matrix Dimensions | Closed-Form Solution (OLS) | Prediction Code | Connection to $y = W^T x$ or $y = w \cdot x$ |
| :--- | :--- | :--- | :--- | :--- |
| **Columns are Samples** | $X \in \mathbb{R}^{\text{Features} \times \text{Samples}}$ <br> $T \in \mathbb{R}^{\text{Targets} \times \text{Samples}}$ | $W = T X^T (X X^T)^{-1}$ | `np.matmul(W, X)` | $X$ is built of vertical feature vectors stacked sideways. Each row of $W$ holds a classifier's weights. |
| **Rows are Samples** | $X \in \mathbb{R}^{\text{Samples} \times \text{Features}}$ <br> $T \in \mathbb{R}^{\text{Samples} \times \text{Targets}}$ | $W = (X^T X)^{-1} X^T T$ | `np.matmul(X, W)` | $X$ is built of horizontal feature vectors stacked vertically. Each column of $W$ holds a classifier's weights. |

---

## 2. Multi-Class Classification Strategies ($K$ Classes)

### For Layout: Columns are Samples ($X$ is $\text{Features} \times \text{Samples}$)

| Classifier Strategy | Weight Matrix ($W$) Dimensions | Prediction / Decision Rule Code | Boundary Condition ($y_i = y_j$) | Handling of Ambiguity |
| :--- | :--- | :--- | :--- | :--- |
| **Discriminant Functions** | $W \in \mathbb{R}^{K \times \text{Features}}$ <br> *(One scoring row per class)* | `np.argmax(np.matmul(W, X), axis=0)` | $(w_i - w_j)^T x = 0$ | **None.** Space is perfectly divided; highest score always wins. |
| **One-versus-the-Rest (OvR)** | $W \in \mathbb{R}^{K \times \text{Features}}$ <br> *(One binary classifier per class)* | `np.argmax(np.matmul(W, X), axis=0)` <br> *(Using continuous confidence/distance)* | $(w_i - w_j)^T x = 0$ | Overlaps/blindspots occur **only** if using hard discrete outputs instead of continuous scores. |
| **One-against-One (OvO)** | $\frac{K(K-1)}{2}$ distinct vectors of size $\text{Features}$ | `votes = np.sign(np.matmul(W_pairwise, X))` <br> followed by a majority tally per sample. | $w_{\text{pair}}^T x = 0$ <br> *(The original pairwise lines)* | **High.** Creates deadlock zones where cycles occur (e.g., a perfect 1-1-1 tie loop). |

### For Layout: Rows are Samples ($X$ is $\text{Samples} \times \text{Features}$)

| Classifier Strategy | Weight Matrix ($W$) Dimensions | Prediction / Decision Rule Code | Boundary Condition ($y_i = y_j$) | Handling of Ambiguity |
| :--- | :--- | :--- | :--- | :--- |
| **Discriminant Functions** | $W \in \mathbb{R}^{\text{Features} \times \text{K}}$ <br> *(One scoring column per class)* | `np.argmax(np.matmul(X, W), axis=1)` | $x^T (w_i - w_j) = 0$ | **None.** Every point on the map maps cleanly to a maximum value. |
| **One-versus-the-Rest (OvR)** | $W \in \mathbb{R}^{\text{Features} \times \text{K}}$ <br> *(One binary classifier per column)* | `np.argmax(np.matmul(X, W), axis=1)` <br> *(Using continuous confidence/distance)* | $x^T (w_i - w_j) = 0$ | Avoids deadlocks by taking the maximum continuous margin. |
| **One-against-One (OvO)** | $\frac{K(K-1)}{2}$ distinct vectors of size $\text{Features}$ | `votes = np.sign(np.matmul(X, W_pairwise))` <br> followed by a majority tally per sample. | $x^T w_{\text{pair}} = 0$ | Leaves unclassified "no-man's-lands" where voting deadlocks occur. |
