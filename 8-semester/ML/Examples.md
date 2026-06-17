## Example 1: Conceptual Tasks (Classification vs. Regression)

This example contrasts classification and regression tasks based on whether the target space is discrete or continuous.

### Classification (Discrete Target Space)
* **Weather Prediction:** Inputting meteorological variables to predict a binary class label $y \in \{\text{Sunny}, \text{Rainy}\}$.
* **Medical Diagnosis:** Processing patient symptoms to predict a specific disease class label $y \in \{\mathcal{C}_1, \mathcal{C}_2, \mathcal{C}_3\}$ where each represents a unique medical condition.

### Regression (Continuous Target Space)
* **Ad Click-Through Rate (CTR):** Predicting a continuous value $y \in [0, 1]$ representing the precise probability of a user clicking an online advertisement.
* **Patient Survival Estimation:** Predicting a continuous lifespan target $y \in \mathbb{R}^+$ measured in fractional years (e.g., $y = 4.25$ years).

---

## Example 2: The XOR Problem (Linear Inseparability)

This classic example shows why simple linear classifiers fail when dealing with non-linearly separable functions.

### The Dataset
Consider four points in a two-dimensional feature space $x = (x_1, x_2) \in \mathbb{R}^2$ defining an exclusive-OR (XOR) relationship:
* Instance 1: $x^{(1)} = (0, 0)^T \implies \text{Class } y = -1$
* Instance 2: $x^{(2)} = (1, 0)^T \implies \text{Class } y = 1$
* Instance 3: $x^{(3)} = (0, 1)^T \implies \text{Class } y = 1$
* Instance 4: $x^{(4)} = (1, 1)^T \implies \text{Class } y = -1$

### The Geometric Failure
A linear classifier attempts to construct a decision boundary defined by the hyperplane equation:

$$w_1x_1 + w_2x_2 + w_0 = 0$$

Plotting these points reveals that the positive instances $(1,0)$ and $(0,1)$ lie diagonally across from the negative instances $(0,0)$ and $(1,1)$. It is geometrically impossible to choose weights $w_1, w_2$ and a bias $w_0$ such that a single straight line isolates both positive points on one side ($> 0$) and both negative points on the other side ($\le 0$). 

---

## Example 3: KNN Model Complexity and Overfitting

This example illustrates how shifting the complexity parameter $K$ alters a model's bias-variance tradeoff and its susceptibility to overfitting.

### Scenario
* **Training Set:** $N_{\text{train}} = 20$ points.
* **Test Set:** $N_{\text{test}} = 9$ points.

### Case A: $K = 1$ (Maximum Complexity Boundary)
* **Training Performance:** 100% accuracy. Because the closest point to any training sample is itself, the distance $d(x_i, x_i) = 0$, guaranteeing a perfect classification on seen data.
* **Test Performance:** $\sim 66\%$ accuracy ($\frac{6}{9}$ correct classifications).
* **Analysis:** The decision boundary forms tightly around local noise and individual training anomalies, failing to capture the underlying data distribution (High variance/Overfitting).

### Case B: $K = 5$ (Smoothed, Simpler Boundary)
* **Training Performance:** $\sim 75\%$ accuracy ($\frac{15}{20}$ correct classifications). Outliers are ignored in favor of regional majorities.
* **Test Performance:** $\sim 77\%$ accuracy ($\frac{7}{9}$ correct classifications).
* **Analysis:** The decision boundary smooths out local irregularities. By allowing a small amount of training error, the model generalizes significantly better to unseen test data.

---

## Example 4: Geometry of a Decision Boundary

This mathematical example breaks down the structural components of a linear decision boundary in a two-dimensional feature space ($D = 2$).

### Given Parameter Values
* Bias parameter: $w_0 = 2.5$
* Weight vector: $w = (w_1, w_2)^T = (1.3, 1.3)^T$

### Discriminant Equation
The linear function is defined as:

$$y(x) = w_0 + w \cdot x = 2.5 + 1.3x_1 + 1.3x_2$$

### Geometric Breakdown
* **The Decision Surface:** Calculated by solving for $y(x) = 0$:
  $$2.5 + 1.3x_1 + 1.3x_2 = 0$$
  This simplifies to the linear equation $x_2 = -x_1 - \frac{2.5}{1.3}$.
* **Orientation:** The weight vector $w = (1.3, 1.3)^T$ acts as a normal vector pointing perpendicularly away from the decision surface into positive decision region $\mathcal{R}_1$.
* **Perpendicular Distance to Origin:** The absolute spatial distance from the origin $(0,0)^T$ to the decision line is calculated as:
  $$\text{Distance} = \frac{|w_0|}{\|w\|} = \frac{2.5}{\sqrt{1.3^2 + 1.3^2}} = \frac{2.5}{\sqrt{1.69 + 1.69}} = \frac{2.5}{\sqrt{3.38}} \approx 1.36$$

---

## Example 5: The Failure of Least Squares for Classification

This numerical example demonstrates why minimizing a sum-of-squares objective function can distort decision boundaries and cause misclassifications, even on datasets that are completely linearly separable.

### Setup
* $N = 3$ training points in $D = 2$ dimensional space with $K = 2$ target classes.
* Target vectors use one-hot encoding: Class 1 is represented as $t = (1, 0)^T$ and Class 2 is represented as $t = (0, 1)^T$.

### Training Dataset
* Instance 1: $x_1 = (1, 1)^T \implies \text{Class } 1 \implies t_1 = (1, 0)^T$
* Instance 2: $x_2 = (1, 5)^T \implies \text{Class } 1 \implies t_2 = (1, 0)^T$ (Sits deep inside Class 1 territory)
* Instance 3: $x_3 = (0, 1)^T \implies \text{Class } 2 \implies t_3 = (0, 1)^T$

### Model Evaluation
We compare two competing weight matrices, $W_1$ and $W_2$, using the discriminant calculation $y(x) = W^T x$.

#### Candidate Model 1 (100% Classification Accuracy, High Least-Squares Error)
* Predictions:
  * $y(x_1) = (10, 0)^T \implies \arg\max \implies \text{Class } 1$ (Correct)
  * $y(x_2) = (10, 4)^T \implies \arg\max \implies \text{Class } 1$ (Correct)
  * $y(x_3) = (0, 1)^T \implies \arg\max \implies \text{Class } 2$ (Correct)
* **Classification Error:** 0% misclassifications.
* **Sum-of-Squares Objective Value ($E_D$):**
  $$E_D = \frac{1}{2} \sum_{n=1}^{3} \|y(x_n) - t_n\|^2$$
  Evaluating the first component for $x_1$: $\|(10,0)^T - (1,0)^T\|^2 = (10-1)^2 + (0-0)^2 = 81$.
  Because the prediction magnitudes are far from the strict binary values of $1$ and $0$, this perfectly accurate classifier yields a massive overall squared error: $E_D = 89.0$.

#### Candidate Model 2 (66.6% Classification Accuracy, Low Least-Squares Error)
* Predictions:
  * $y(x_1) = (2, 0)^T \implies \arg\max \implies \text{Class } 1$ (Correct)
  * $y(x_2) = (6, -4)^T \implies \arg\max \implies \text{Class } 1$ (Correct)
  * $y(x_3) = (1, -1)^T \implies \arg\max \implies \text{Class } 1$ (Incorrect, target was Class 2)
* **Classification Error:** 33.3% misclassifications (misclassifies $x_3$).
* **Sum-of-Squares Objective Value ($E_D$):**
  Because the values computed by this model stay closer to the nominal targets of $1$ and $0$, calculating the squared differences across the points yields a small error value: $E_D = 23.5$.

### Core Takeaway for Oral Exam
If trained via a least-squares regression algorithm, the system will select **Candidate Model 2** because it minimizes the error metric ($23.5 < 89.0$). However, Model 2 introduces a critical misclassification on $x_3$. 

Least squares fails here because its quadratic penalty forces the decision boundary to swing out of position to try and reduce the squared distance to outlier $x_2$ (which is "too correct" with a prediction value of $10$). This demonstrates that minimizing a sum-of-squares metric does not directly optimize for classification accuracy.

## Example 1: Generative vs. Discriminative Paradigms

This example highlights how the two paradigms process a dataset differently to make predictions.

### Scenario
Classifying whether a text message is Spam ($Y = 1$) or Not Spam ($Y = 0$) based on a single binary feature: whether it contains the word "Winner" ($X = 1$ or $X = 0$).

### 1. Generative Approach (e.g., Naive Bayes)
A generative model learns the class priors $P(Y)$ and the class-conditional distributions $P(X \mid Y)$ from the training history.

* **Learned Estimates:**
  * Prior probabilities: $P(Y = 1) = 0.20$, $P(Y = 0) = 0.80$
  * Likelihood of feature given class: $P(X = 1 \mid Y = 1) = 0.70$, $P(X = 1 \mid Y = 0) = 0.05$

* **Classification Decision:** A new message arrives containing the word "Winner" ($X = 1$). We calculate the joint probability $P(X, Y) = P(X \mid Y)P(Y)$ for each class:
  $$P(X = 1, Y = 1) = 0.70 \times 0.20 = 0.14$$
  $$P(X = 1, Y = 0) = 0.05 \times 0.80 = 0.04$$

* **Posterior Probability Calculation:** Using Bayes' theorem to normalize the results:
  $$P(Y = 1 \mid X = 1) = \frac{0.14}{0.14 + 0.04} = \frac{0.14}{0.18} \approx 0.778$$
  Since $0.778 > 0.50$, the system classifies the message as Spam.

### 2. Discriminative Approach (e.g., Logistic Regression)
A discriminative model ignores how often the word "Winner" appears within each class. It directly optimizes a functional mapping from the input feature $X$ to the posterior probability $P(Y \mid X)$.

* **Learned Functional Rule:** Through optimization, it directly determines the conditional probability parameters:
  $$P(Y = 1 \mid X = 1) = 0.778$$
  $$P(Y = 1 \mid X = 0) = 0.070$$
* **Classification Decision:** For an input where $X = 1$, it looks up or computes $P(Y = 1 \mid X = 1) = 0.778$ and immediately routes it to the Spam class without evaluation of intermediate joint distributions.

---

## Example 2: Linear Discriminant Analysis (LDA) Assumption Failure

This example demonstrates how the foundational assumption of LDA (shared covariance across all classes) can cause it to misclassify data, even when the underlying dataset is linearly separable.

### Scenario
We have a two-dimensional dataset ($D = 2$) with two classes ($K = 2$). 

### Class Statistics
* **Class 0 (Highly Concentrated):**
  $$\mu_0 = \begin{pmatrix} 0 \\ 0 \end{pmatrix}, \quad \Sigma_0 = \begin{pmatrix} 0.1 & 0 \\ 0 & 0.1 \end{pmatrix}$$
* **Class 1 (Widely Dispersed):**
  $$\mu_1 = \begin{pmatrix} 4 \\ 0 \end{pmatrix}, \quad \Sigma_1 = \begin{pmatrix} 9.0 & 0 \\ 0 & 9.0 \end{pmatrix}$$

### The Failure Mechanics
Because LDA enforces a strict shared covariance constraint, it averages the individual covariance matrices to compute a pooled covariance matrix $\Sigma$:

$$\Sigma = \frac{1}{2}(\Sigma_0 + \Sigma_1) = \frac{1}{2}\left(\begin{pmatrix} 0.1 & 0 \\ 0 & 0.1 \end{pmatrix} + \begin{pmatrix} 9.0 & 0 \\ 0 & 9.0 \end{pmatrix}\right) = \begin{pmatrix} 4.55 & 0 \\ 0 & 4.55 \end{pmatrix}$$

* **Boundary Placement:** Using this shared matrix $\Sigma$, LDA treats both classes as having identical spread. Because the priors are equal, it positions the linear decision boundary exactly midway between the means, at $x_1 = 2$.
* **The Error:** In reality, Class 1 points have high variance ($\sigma^2 = 9.0$) and frequently scatter far to the left of $x_1 = 2$. Concurrently, Class 0 points are tightly locked near the origin and never cross $x_1 = 1$. 
* **Oral Exam Conclusion:** LDA misclassifies many Class 1 points falling left of $x_1 = 2$ because its shared covariance assumption fails to model the true class-specific variances. A quadratic model (QDA) or discriminative model would be required to place the boundary correctly near $x_1 = 0.8$.

---

## Example 3: Logistic Regression Probability Computation

This example shows the explicit steps for computing a classification probability using a trained logistic regression model.

### Setup
* Feature space dimension: $D = 2$
* Input vector: $x = (x_1, x_2)^T = (2.0, 3.0)^T$
* Model parameters: Bias $w_0 = -4.5$, Weight vector $w = (w_1, w_2)^T = (1.5, 0.5)^T$

### Step 1: Compute the Linear Activation ($a$)
Using the augmented input vector $\tilde{x} = (1, x_1, x_2)^T$ and weight vector $w = (w_0, w_1, w_2)^T$:

$$a = w^T \tilde{x} = w_0 + w_1x_1 + w_2x_2$$
$$a = -4.5 + (1.5 \times 2.0) + (0.5 \times 3.0)$$
$$a = -4.5 + 3.0 + 1.5 = 0$$

### Step 2: Apply the Logistic Sigmoid Mapping
Pass the activation value $a$ through the sigmoid function $\sigma(a)$ to obtain the posterior probability for Class 1:

$$P(\mathcal{C}_1 \mid x) = \sigma(a) = \frac{1}{1 + e^{-a}}$$
$$P(\mathcal{C}_1 \mid x) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = 0.50$$

### Step 3: Shifted Input Evaluation
Let us evaluate another data point located deeper within the feature space at $x' = (4.0, 3.0)^T$:

$$a' = -4.5 + (1.5 \times 4.0) + (0.5 \times 3.0)$$
$$a' = -4.5 + 6.0 + 1.5 = 3.0$$
$$P(\mathcal{C}_1 \mid x') = \sigma(3.0) = \frac{1}{1 + e^{-3.0}} \approx \frac{1}{1 + 0.0498} \approx 0.952$$

Since $0.952 \ge 0.50$, the model assigns $x'$ to Class 1 with $95.2\%$ confidence.

---

## Example 4: Data Transformations and Feature Maps ($\phi$)

This example demonstrates how a non-linear feature map converts a dataset that cannot be separated by a straight line into a space where it is completely linearly separable.

### Dataset Structure (Concentric Rings)
Points are distributed in a two-dimensional input space $x = (x_1, x_2)^T$:
* **Class 0 (Inner Ring):** Data clusters closely around a radius of $r = 1$.
* **Class 1 (Outer Ring):** Data clusters around an outer radius of $r = 3$.

No straight line can separate an inner circle from an outer ring in this 2D input coordinates system.

### Defining the Feature Map
We apply a non-linear mapping function $\phi(x)$ to project the data into a new 2D feature space $z = (z_1, z_2)^T$:

$$\phi(x) = \begin{pmatrix} \phi_1(x) \\ \phi_2(x) \end{pmatrix} = \begin{pmatrix} x_1^2 \\ x_2^2 \end{pmatrix}$$

Let $z_1 = x_1^2$ and $z_2 = x_2^2$.

### Linear Separation in Feature Space
In this new feature space, we construct a standard linear model:

$$y(z) = w_1 z_1 + w_2 z_2 + w_0$$

By assigning parameter weights $w_1 = 1$, $w_2 = 1$, and a bias $w_0 = -4.0$, the decision boundary equation ($y(z) = 0$) becomes:

$$1 \cdot z_1 + 1 \cdot z_2 - 4.0 = 0 \implies z_1 + z_2 = 4.0$$

* **Geometry in Feature Space:** The equation $z_1 + z_2 = 4.0$ defines a straight line boundary.
* **Geometry in Input Space:** Substituting the features back shows what the model drew in the original space: $x_1^2 + x_2^2 = 4.0$. This is a circular decision boundary with a radius of $2$, perfectly separating the concentric rings.