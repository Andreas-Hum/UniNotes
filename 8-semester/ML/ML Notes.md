# Lecture 1
## Introduction to Linear Models for Classification

Linear models use linear functions to define decision boundaries between classes. They represent one of the most fundamental concepts in machine learning.

* **Standalone Value:** Highly useful, robust, and well-understood baseline models.
* **Building Blocks:** They form the essential final component or layer of more complex, non-linear models like deep neural networks or support vector machines.

---

## Classification vs. Regression

Machine learning tasks are primarily divided based on the nature of the target variable:

### Classification
* **Goal:** Learn to predict a discrete class label.
* **Examples:**
  * Predicting whether the sun will shine tomorrow (Yes/No).
  * Medical diagnosis based on observed symptoms.
* **Data Properties:** All data points possess known feature values (predictors/attributes) and a known or unknown class label.

### Regression
* **Goal:** Learn to predict a continuous target value.
* **Examples:**
  * Predicting the click-through rate (CTR) for an online ad.
  * Stock price prediction for the next day.
  * Estimating patient survival time in years.

---

## K-Nearest Neighbor (KNN) Classifier

### Core Principle
KNN operates on the assumption that near neighbors in the feature space tend to share the same class label.

### Algorithm Mechanics
1. **Data Requirement:** Requires a set of labeled training instances $(x_1, y_1), \dots, (x_N, y_N)$ in a $D$-dimensional input space, where $x_i \in \mathbb{R}^D$ and $y_i$ is the class label.
2. **Distance Metric:** A distance function $d(x, x')$ (typically Euclidean distance) is required to evaluate proximity.
3. **Classification Step:** To classify an unlabelled instance $x$:
   * Find the $K$ training instances closest to $x$.
   * Assign $x$ the class label that occurs most frequently among those $K$ neighbors (majority voting).

### Decision Regions
A classifier partitions the instance space into distinct decision regions. Each class label defines a region where any incoming point will be assigned that specific label.
* **1-Nearest Neighbor:** Yields highly complex, granular decision boundaries that fit tightly around individual training data points.
* **5-Nearest Neighbor:** Smooths out the decision boundaries, resulting in larger, more continuous regions.

---

## Baseline Linear Classifiers: Perceptron and Naive Bayes

Despite having different underlying philosophies, both models share the exact same capacity: they represent identical linear classification rules but optimize different objective functions.

### 1. The Perceptron
A basic neural network structure containing an input layer, no hidden layers, and a single output neuron utilizing a sign activation function.

* **Function Computed:**
  $$O(x_1, \dots, x_n) = \begin{cases} 1 & \text{if } w_0 + w_1x_1 + \dots + w_nx_n > 0 \\ -1 & \text{otherwise} \end{cases}$$
* **Objective:** Minimizes a classification error function.
* **Geometry:** The resulting decision regions are strictly separated by a linear hyperplane.

### 2. Naive Bayes Model
A probabilistic classifier built on the assumption that all input features $X_i$ are conditionally independent given the class label $Y$.

* **Prediction (Binary Class/Attributes):** An instance is classified by comparing probabilities:
  $$\log P(\oplus | X_1, \dots, X_n) \ge \log P(\ominus | X_1, \dots, X_n)$$
* **Linear Connection:** Through algebraic rewriting via Bayes' rule, this probabilistic comparison simplifies directly into a linear function of the input attributes:
  $$\sum_{i=1}^{n} \log \left( \frac{P(X_i=1|\oplus)P(X_i=0|\ominus)}{P(X_i=0|\oplus)P(X_i=1|\ominus)} \right) X_i + \sum_{i=1}^{n} \log \frac{P(X_i=0|\oplus)}{P(X_i=0|\ominus)} + \log \frac{P(\oplus)}{P(\ominus)} \ge 0$$
* **Objective:** Maximizes a likelihood function.

### Fundamental Limitations
* **The XOR Problem:** Simple linear classifiers like the Perceptron and Naive Bayes are fundamentally limited because they cannot learn non-linearly separable functions such as the XOR logical operation.
* **Solutions:** Overcoming this requires advanced architectures like Support Vector Machines (SVMs), multi-layer neural networks with hidden layers, or generalized Bayesian Networks.

---

## Overfitting and Model Complexity

### Definition
A model $h$ is said to overfit the training data if there is an alternative model $h'$ such that $h$ achieves a smaller error than $h'$ on the training set, but $h'$ achieves a smaller error than $h$ over the entire true distribution of instances.

### Complexity Parameters
Model spaces are usually structured by parameters that dictate the complexity of their decision boundaries:
* **KNN:** The parameter is $K$. A small $K$ (e.g., $K=1$) leads to complex decision regions and a high risk of overfitting (100% training accuracy but lower test accuracy). Larger $K$ values decrease complexity.
* **Neural Networks:** Controlled by the number of hidden units and layers.
* **Bayesian Networks:** Controlled by the structural complexity of the network graph.

> **Exam Note:** Linear models are highly favored because their limited capacity makes them inherently unlikely to overfit, though explicit regularisation techniques are still used as a safeguard.

---

## Geometry of Linear Functions

A linear function of a $D$-dimensional numeric attribute vector $x = (x_1, \dots, x_D)$ with coefficients $w_0, w_1, \dots, w_D \in \mathbb{R}$ is defined as:

$$y(x) = w_0 + w_1x_1 + \dots + w_Dx_D = w_0 + w \cdot x$$

* **Vector Notation:** $w = (w_1, \dots, w_D)$ represents the weight vector, and $w \cdot x$ denotes the standard dot product.
* **Bias Component:** $w_0$ represents the bias. Technically, these are affine functions; they are strictly linear only when $w_0 = 0$.

### Geometric Properties of the Decision Boundary ($y(x) = 0$)
* **Orientation:** The weight vector $w$ determines the spatial orientation of the decision boundary. It acts normal (perpendicular) to the hyperplane.
* **Spatial Distance:** The perpendicular distance from the origin to the decision boundary is given by:
  $$\frac{|w_0|}{\|w\|}$$
  Where $\|w\| = \sqrt{w \cdot w}$ represents the Euclidean length of the weight vector.
* **Region Allocation:** The boundary splits the input space into two clear halves:
  * $\mathcal{R}_1 = \{x \mid y(x) \ge 0\}$
  * $\mathcal{R}_2 = \{x \mid y(x) < 0\}$

---

## Multi-Class Classification Approaches

When dealing with more than two distinct class labels ($K > 2$), linear functions can be adapted using three primary frameworks:

### 1. One-Against-All
* **Concept:** Train $K$ independent binary classifiers, where each classifier separates class $\mathcal{C}_k$ from all remaining classes combined.
* **Issue:** Can create ambiguous, unclassified regions in the input space where multiple classifiers claim or reject membership.

### 2. One-Against-One
* **Concept:** Train $K(K-1)/2$ binary classifiers covering every possible pair of classes.
* **Issue:** Can also lead to ambiguous regions where voting ties occur.

### 3. Linear Discriminant Functions
* **Concept:** Construct exactly one linear discriminant function $y_k(x)$ for each class label $k$:
  $$y_k(x) = w_{k,0} + w_k \cdot x$$
* **Classification Rule:** Assign the input vector $x$ to the specific class $k$ that maximizes the function value:
  $$\arg\max_k y_k(x)$$
* **Advantage:** Guarantees that all decision regions are fully contiguous and convex, avoiding any ambiguous zones.

### Matrix Representation
To group all $K$ linear discriminant functions compactly, vector-matrix notation is used:

$$y(x) = w_0 + W^T x$$

Where $w_0$ is a $K$-dimensional bias vector, and $W$ is a $D \times K$ weight matrix. 

By augmenting the vectors to include the bias directly, we can write this in an ultra-short format:
$$\tilde{x} = \begin{pmatrix} 1 \\ x_1 \\ \vdots \\ x_D \end{pmatrix}, \quad \tilde{W} = \begin{pmatrix} w_{1,0} & w_{2,0} & \dots & w_{K,0} \\ w_{1,1} & w_{2,1} & \dots & w_{K,1} \\ \vdots & \vdots & \dots & \vdots \\ w_{1,D} & w_{2,D} & \dots & w_{K,D} \end{pmatrix}$$

$$y(x) = \tilde{W}^T \tilde{x}$$

---

## Classification by Least Squares Regression

### Target Formulation (One-Hot Encoding)
For a training instance $x_n$ belonging to a class $y_n \in \{1, \dots, K\}$, we define a $K$-dimensional target vector $t_n$:
$$t_n = (0, \dots, 0, 1, 0, \dots, 0)^T$$
The value $1$ is placed strictly at the index of the true class $y_n$.

### Objective: Sum-of-Squares Error
We seek a weight matrix $\tilde{W}$ that minimizes the total sum-of-squares error across all $N$ instances:
$$E_D(\tilde{W}) = \frac{1}{2} \sum_{n=1}^{N} \|\tilde{W}^T \tilde{x}_n - t_n\|^2$$

In global matrix notation, this is expressed using the trace operator ($Tr$):
$$E_D(\tilde{W}) = \frac{1}{2} Tr \{ (\tilde{X}\tilde{W} - T)^T (\tilde{X}\tilde{W} - T) \}$$

### Analytical Solution
Taking the derivative with respect to $\tilde{W}$, setting it to zero, and isolating the weight matrix yields the normal equation:
$$\tilde{X}^T \tilde{X} \tilde{W} = \tilde{X}^T T$$

Solving for $\tilde{W}$ gives the exact analytical closed-form solution:
$$\tilde{W} = (\tilde{X}^T \tilde{X})^{-1} \tilde{X}^T T$$

### Critical Vulnerabilities of Least Squares for Classification
* **Sensitivity to Outliers:** Least squares penalizes predictions that are "too correct." If a data point sits deep within the correct side of the decision boundary, its target value far exceeds $1$. The quadratic penalty forces the decision line to shift to reduce this specific error, which can ruin the boundary and misclassify points closer to the center.
* **Mismatched Objectives:** Sum-of-squares error minimization optimizes for continuous target proximity rather than directly minimizing classification error rate. Consequently, a model with higher classification accuracy can sometimes be rejected by the least squares criterion in favor of a less accurate one that scores better on squared variance.

# Lecture 2
## Probabilistic Classification Frameworks

Probabilistic classifiers assign an input vector $x$ to the class $k$ for which the posterior probability $P(Y = k \mid x)$ is maximal. There are two primary paradigms used to find this probability:

### 1. Generative Approach
* **Core Concept:** Models how the data is generated by learning the joint probability distribution $P(Y, X)$.
* **Factorization:** Uses Bayes' theorem to decompose the target conditional probability:
  $$P(Y = k \mid X = x) = \frac{P(X = x \mid Y = k)P(Y = k)}{P(X = x)}$$
* **Key Components:**
  * **Class Prior $P(Y = k)$:** The overall probability of encountering class $k$.
  * **Class-Conditional Density $P(X = x \mid Y = k)$:** The probability distribution of the input features within class $k$.
* **Examples:** Linear Discriminant Analysis (LDA), Naive Bayes models.

### 2. Discriminative Approach
* **Core Concept:** Skips modeling the input distribution entirely and learns the conditional distribution $P(Y \mid X)$ directly from the data.
* **Philosophy:** Focuses strictly on discovering the optimal decision boundaries between classes.
* **Examples:** Logistic Regression, Support Vector Machines (SVMs), Feedforward Neural Networks.

### Operational Comparison
* **Predicting $Y$ given $X$:** Supported by both Generative and Discriminative models.
* **Predicting an input feature $X_i$:** Supported only by Generative models.
* **Generating new data points $(x, y)$:** Supported only by Generative models.

---

## Linear Discriminant Analysis (LDA)

LDA is a probabilistic generative classifier that models class-conditional densities using multivariate normal distributions.

### Structural Assumptions
1. **Gaussian Distribution:** Within each class $k$, the features follow a multivariate Gaussian probability density function:
  $$P(X = x \mid Y = k) = \frac{1}{(2\pi)^{D/2} |\Sigma_k|^{1/2}} \exp \left( -\frac{1}{2}(x - \mu_k)^T \Sigma_k^{-1} (x - \mu_k) \right)$$
2. **Shared Covariance:** Every class shares the exact same covariance matrix across the feature space:
  $$\Sigma_k = \Sigma \quad \forall k$$

### Derivation of the Linear Decision Boundary
When computing the log-odds ratio to compare two classes $\mathcal{C}_i$ and $\mathcal{C}_j$, the quadratic terms containing $x^T \Sigma^{-1} x$ cancel out precisely because the covariance matrix $\Sigma$ is identical across classes. 

$$\log \left( \frac{P(\mathcal{C}_i \mid x)}{P(\mathcal{C}_j \mid x)} \right) = \log \left( \frac{P(x \mid \mathcal{C}_i)}{P(x \mid \mathcal{C}_j)} \right) + \log \left( \frac{P(\mathcal{C}_i)}{P(\mathcal{C}_j)} \right)$$

Substituting the Gaussian densities into the expression simplifies the log-odds directly into a linear function of $x$:

$$\log \left( \frac{P(\mathcal{C}_i \mid x)}{P(\mathcal{C}_j \mid x)} \right) = w^T x + w_0$$

Where:
* $w = \Sigma^{-1}(\mu_i - \mu_j)$
* $w_0 = -\frac{1}{2}\mu_i^T \Sigma^{-1} \mu_i + \frac{1}{2}\mu_j^T \Sigma^{-1} \mu_j + \log \frac{P(\mathcal{C}_i)}{P(\mathcal{C}_j)}$

---

# Logistic Regression

Logistic Regression is a probabilistic discriminative model that models the posterior probabilities of classes using explicit functional mappings.

## Functional Form

For a two-class problem, the posterior probability for class $\mathcal{C}_1$ is defined via the logistic sigmoid function:

$$P(\mathcal{C}_1 \mid x) = \sigma(w^T \tilde{x}) = \frac{1}{1 + e^{-w^T \tilde{x}}}$$

Where $\sigma(a)$ represents the logistic sigmoid mapping:

$$\sigma(a) = \frac{1}{1 + e^{-a}}$$

### Essential Mathematical Properties of the Sigmoid

- **Symmetry:** $\sigma(-a) = 1 - \sigma(a)$
    
- **Derivative:** $\frac{d\sigma}{da} = \sigma(a)(1 - \sigma(a))$
    
- **Logit Function:** The inverse of the sigmoid reveals a linear relationship for the log-odds:
    
    $$\log \left( \frac{P(\mathcal{C}_1 \mid x)}{1 - P(\mathcal{C}_1 \mid x)} \right) = w^T \tilde{x}$$
    

## Maximum Likelihood Estimation (The Objective)

To find the optimal weights $w$, we use **Maximum Likelihood Estimation (MLE)**. We want to maximize the probability that our model correctly guesses the training data labels.

Let the true label be $y_i = 1$ if the datapoint belongs to $\mathcal{C}_1$, and $y_i = 0$ if it belongs to $\mathcal{C}_2$. Let our model's prediction be $p_i = \sigma(w^T \tilde{x}_i)$.

1. **The Likelihood:** For the entire dataset, we multiply the individual probabilities together:
    
    $$L(w) = \prod_{i=1}^{N} p_i^{y_i}(1 - p_i)^{1 - y_i}$$
    
2. **The Error Function (Cross-Entropy Loss):** To make the math easier for computers, we take the negative natural log of the likelihood. This turns multiplication into a clean addition problem that we want to **minimize**:
    
    $$J(w) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \right]$$
    

## The Gradient (How the Model Learns)

To minimize the error using Gradient Descent, we need to find how a tiny change in a specific weight $w_j$ affects our total loss $J(w)$. We do this using the **chain rule** by breaking the process into three simple steps:

$$\frac{\partial J}{\partial w_j} = \frac{\partial J}{\partial p_i} \cdot \frac{\partial p_i}{\partial a_i} \cdot \frac{\partial a_i}{\partial w_j}$$

Where $a_i = w^T \tilde{x}_i$ is the raw score before the sigmoid.

### The 3-Step Chain Rule Breakdown

- **Step 1: How the Loss changes with our Prediction ($\frac{\partial J}{\partial p_i}$)**
    
    Differentiating the log formulas gives us our raw scaling factor:
    
    $$\frac{\partial J}{\partial p_i} = \frac{p_i - y_i}{p_i(1-p_i)}$$
    
- **Step 2: How the Prediction changes with the Raw Score ($\frac{\partial p_i}{\partial a_i}$)**
    
    Using the essential property of the sigmoid derivative:
    
    $$\frac{\partial p_i}{\partial a_i} = p_i(1 - p_i)$$
    
    > **The Elegant Cancelation:** Notice that multiplying Step 1 and Step 2 together completely removes the complex fractional denominators:
    > 
    > $$\frac{\partial J}{\partial p_i} \cdot \frac{\partial p_i}{\partial a_i} = \frac{p_i - y_i}{\cancel{p_i(1-p_i)}} \cdot \cancel{p_i(1-p_i)} = (p_i - y_i)$$
    > 
    > This represents the simple **prediction error** (Predicted value minus True value).
    
- **Step 3: How the Raw Score changes with a Weight ($\frac{\partial a_i}{\partial w_j}$)**
    
    The raw score is a linear combination: $a_i = w_0 + w_1 x_{i1} + \dots + w_j x_{ij} + \dots$. If we take the derivative with respect to only $w_j$, all other terms are treated as constants ($0$), and the target weight $w_j$ drops out, leaving only its accompanying feature value:
    
    $$\frac{\partial a_i}{\partial w_j} = \tilde{x}_{ij}$$
    

### The Final Gradient Formula

Multiplying the terms back together and averaging them over all $N$ datapoints yields an incredibly clean, intuitive result:

$$\frac{\partial J}{\partial w_j} = \frac{1}{N} \sum_{i=1}^{N} (p_i - y_i) \tilde{x}_{ij}$$

> **Intuition:** The steepness of the error landscape for any weight is simply the **average prediction error multiplied by the input feature value**. If a prediction is perfectly correct ($p_i - y_i = 0$), the gradient step is zero, meaning the model changes nothing.

### Example  
To see how MLE handles real-valued, continuous data instead of binary classifications, let's look at weather measurements. Suppose we measure rainfall over 3 days and get the following data points (in mm):

$$x_1 = 3, \quad x_2 = 2, \quad x_3 = 6$$

We want to fit a single continuous Gaussian bell curve to this data. This time, we do not know the center (**mean** $\mu$) **nor** the width (**standard deviation** $\sigma$). Both are unknown parameters bundled inside our parameter vector $\theta = (\mu, \sigma)$.

### 1. The Continuous Likelihood Function

For continuous variables, the probability density of a single observation $x_i$ given a Normal distribution is:

$$Q(x_i; \mu, \sigma) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x_i - \mu)^2}{2\sigma^2}}$$

To find the total likelihood $L(\mu, \sigma)$ for our independent rainy days, we multiply their individual densities together:

$$L(\mu, \sigma) = \prod_{i=1}^{3} \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x_i - \mu)^2}{2\sigma^2}}$$

$$L(\mu, \sigma) = \left( \frac{1}{\sqrt{2\pi\sigma^2}} \right)^3 e^{-\frac{1}{2\sigma^2} \sum_{i=1}^{3} (x_i - \mu)^2}$$

### 2. The Log-Likelihood Function

Taking the natural logarithm ($\ln$) converts this product into a highly manageable sum:

$$\ln L(\mu, \sigma) = \ln \left[ \left(2\pi\sigma^2\right)^{-\frac{3}{2}} \right] - \frac{1}{2\sigma^2} \sum_{i=1}^{3} (x_i - \mu)^2$$

$$\ln L(\mu, \sigma) = -\frac{3}{2}\ln(2\pi) - 3\ln(\sigma) - \frac{1}{2\sigma^2} \left[ (3-\mu)^2 + (2-\mu)^2 + (6-\mu)^2 \right]$$

### 3. Solving for the Optimal Mean ($\mu$)

To find the peak along the $\mu$ axis, we take the partial derivative with respect to $\mu$ while treating $\sigma$ as a constant, and set it to $0$:

$$\frac{\partial \ln L}{\partial \mu} = 0 - 0 - \frac{1}{2\sigma^2} \left[ 2(3-\mu)(-1) + 2(2-\mu)(-1) + 2(6-\mu)(-1) \right]$$

$$\frac{\partial \ln L}{\partial \mu} = \frac{1}{\sigma^2} \left[ (3-\mu) + (2-\mu) + (6-\mu) \right] = 0$$

Since $\sigma^2 \neq 0$, we can multiply it out:

$$(3 + 2 + 6) - 3\mu = 0 \implies 3\mu = 11 \implies \mu_{\text{MLE}} = \frac{11}{3} \approx 3.67\text{ mm}$$

> **Moment Matching Intuition:** Just like in the Forward KL framework, the calculus automatically forces the optimal model center $\mu$ to match the **exact sample average** of the data points.

### 4. Solving for the Optimal Spread ($\sigma$)

Now we take the partial derivative with respect to $\sigma$, treating our newly found $\mu$ as given, and set it to $0$:

$$\frac{\partial \ln L}{\partial \sigma} = -\frac{3}{\sigma} - \left( \sum_{i=1}^{3} (x_i - \mu)^2 \right) \cdot \frac{\partial}{\partial \sigma}\left( \frac{1}{2}\sigma^{-2} \right)$$

$$\frac{\partial \ln L}{\partial \sigma} = -\frac{3}{\sigma} + \frac{1}{\sigma^3}\sum_{i=1}^{3} (x_i - \mu)^2 = 0$$

Multiply the entire equation by $\sigma^3$ to clear the denominators:

$$-3\sigma^2 + \sum_{i=1}^{3} (x_i - \mu)^2 = 0 \implies 3\sigma^2 = \sum_{i=1}^{3} (x_i - \mu)^2$$

$$\sigma^2_{\text{MLE}} = \frac{1}{3} \sum_{i=1}^{3} (x_i - \mu)^2$$

Substituting our data numbers and our optimal mean ($\mu = \frac{11}{3}$):

$$\sigma^2_{\text{MLE}} = \frac{1}{3} \left[ \left(3 - \frac{11}{3}\right)^2 + \left(2 - \frac{11}{3}\right)^2 + \left(6 - \frac{11}{3}\right)^2 \right]$$

$$\sigma^2_{\text{MLE}} = \frac{1}{3} \left[ \left(-\frac{2}{3}\right)^2 + \left(-\frac{5}{3}\right)^2 + \left(\frac{7}{3}\right)^2 \right] = \frac{1}{3} \left[ \frac{4}{9} + \frac{25}{9} + \frac{49}{9} \right] = \frac{78}{27} = \frac{26}{9} \approx 2.89$$

Taking the square root gives our optimal standard deviation (spread):

$$\sigma_{\text{MLE}} = \sqrt{\frac{26}{9}} \approx 1.70\text{ mm}$$

### Final Summary

When MLE optimizes a continuous model with _all_ parameters open:

- It sets the center knob ($\mu$) to the **mean of all the data** ($3.67\text{ mm}$).
    
- It sets the width knob ($\sigma$) to the **standard deviation of all the data** ($1.70\text{ mm}$).
    

This perfectly mirrors how **Forward KL** behaves. It checks the entire system's spread and variance simultaneously to ensure the approximating model matches the true dataset's footprint perfectly, leaving no data point uncovered.

---

## Support Vector Machines (SVM) - Foundations

Support Vector Machines are non-probabilistic discriminative models designed to find an optimal decision hyperplane based on geometric margin maximization.

### Mathematical Framework
We define a binary classification setting where target labels are encoded as $y_n \in \{-1, 1\}$. The separating hyperplane is written as:

$$w^T x + b = 0$$

The classification decision rule for any input instance $x$ is:
$$\hat{y} = \text{sign}(w^T x + b)$$

### Geometric Margin Maximization
To maximize the separation gap between the boundaries of both classes, we want to maximize the margin distance, defined as $\frac{1}{\|w\|}$. This geometric objective is formulated as a constrained minimization problem:

$$\min_{w, b} \frac{1}{2} \|w\|^2$$

Subject to the strict linear inequality constraints for all $N$ training samples:
$$y_n (w^T x_n + b) \ge 1 \quad \forall n \in \{1, \dots, N\}$$

### Support Vectors and Dual Representation
Using Lagrange multipliers $\lambda_n \ge 0$, this primal formulation is transformed into its dual optimization problem.
* **Active Constraints:** The optimal solution satisfies KKT complementarity conditions, which force either $\lambda_n = 0$ or $y_n(w^T x_n + b) = 1$.
* **Support Vectors:** The points located directly on the margins where the constraint is active ($\lambda_n > 0$) are called the Support Vectors.
* **Weight Composition:** The final weight vector is a linear combination of these support vectors:
  $$w = \sum_{n: \lambda_n > 0} \lambda_n y_n x_n$$
  Points that fall deep inside their correct class boundaries have $\lambda_n = 0$ and have no influence on the location of the decision boundary.
* **Dot Product Operational Rule:** In its dual form, both optimization and test instance evaluation depend solely on evaluating standard vector dot products ($x_n^T x_m$ or $x_n^T z$).

---

## Data Transformations and Feature Spaces

When a dataset cannot be separated linearly in its original input space, it can be projected into a higher-dimensional feature space where a linear boundary becomes viable.

### The Mapping Vector Function ($\phi$)
A non-linear mapping function transforms a $D$-dimensional input vector $x$ into a $D'$-dimensional feature space:

$$\phi: \mathbb{R}^D \rightarrow \mathbb{R}^{D'}$$

The linear models are then calculated directly using these transformed attributes:
$$y(x) = w^T \phi(x) + w_0$$

### Key Architectural Principle
While $\phi(x)$ introduces non-linear attributes with respect to the input space $x$, the decision function remains strictly linear *with respect to the weight parameters $w$*. This allows the model to draw highly complex, non-linear decision boundaries in the original coordinates while retaining simple, convex optimization properties during training.


## 1. Data Transformations & Feature Spaces

When data is not linearly separable in its original space, we can map it to a higher-dimensional space where a linear boundary can separate the classes.

- **Feature Mapping Function**: Any mapping $\phi:\mathbb{R}^{D}\rightarrow\mathbb{R}^{D^{\prime}}$ transforms an original data instance $x$ into a transformed instance $\phi(x)=(\phi_{1}(x),...,\phi_{D^{\prime}}(x))$.
    
- **Terminology**: The components $\phi_{i}(x)$ are known as **features** or **basis functions**, and the target space $\mathbb{R}^{D^{\prime}}$ is called the **feature space**.
    
- **Dimensionality**: Typically, the feature space has a higher dimensionality than the input space ($D^{\prime}>D$), and the mapping functions $\phi_{i}$ are non-linear.
    
- **Decision Boundaries**: Linear models can be applied directly to this transformed data. A linear decision boundary established in the feature space maps back to a **non-linear decision boundary** in the original input space.
    

## 2. The Kernel Trick

### The High-Dimensional Problem

To learn a non-linear SVM, a naive approach would be to embed the data into the higher-dimensional space and then train a standard linear SVM. However, suitable feature spaces often need to be exceptionally high-dimensional, making the explicit construction and computation of the transformed vectors $\phi(x)$ computationally prohibitive.

### The Core Insight

The SVM optimization problem is solved using the method of **Lagrange multipliers**. In this formulation:

- To determine the support vectors $x_i$, coefficients $\lambda_i$, and bias $b$, the **only** operation required on the data vectors is the dot product $x_{i}\cdot x_{j}$.
    
- For classifying a new unseen instance $z$, the algorithm similarly only needs to compute the dot product $x_{i}\cdot z$.
    

### Definition of a Kernel

Because data interactions occur solely via dot products, we can compute the dot product $\phi(x)\cdot\phi(x^{\prime})$ in a high-dimensional space **without ever explicitly constructing** the high-dimensional vectors $\phi(x)$ and $\phi(x^{\prime})$.

A **kernel function** $K(x,x^{\prime})$ directly calculates this inner product:

$$K(x,x^{\prime}) = \phi(x)\cdot\phi(x^{\prime})$$

> **Example**: For the mapping $\phi:(x_{1},x_{2})\rightarrow(x_{1}^{2},x_{2}^{2},\sqrt{2}x_{1},\sqrt{2}x_{2},\sqrt{2}x_{1}x_{2},1)$ , the dot product simplifies algebraically to $\phi(x)\cdot\phi(x^{\prime}) = (x\cdot x^{\prime}+1)^{2}$. Thus, $K(x,x^{\prime})=(x\cdot x^{\prime}+1)^{2}$ serves as a valid kernel function that acts as a measure of similarity.

### Mercer's Theorem & Positive Semi-Definiteness

How do we know if a symmetric similarity function $K(x,z)$ corresponds to a dot product in _some_ valid feature space?

- **Continuous Form**: $K(x,x^{\prime})$ must satisfy $\int K(x,x^{\prime})g(x)g(x^{\prime})dxdx^{\prime}\ge0$ for all functions where $\int g(x)^{2}dx<\infty$. Such a kernel is called **positive semi-definite**.
    
- **Matrix Form (Gram Matrix)**: For any finite set of data points $x_1, ..., x_n$, the resulting $n \times n$ symmetric matrix of inner products—the **Kernel Matrix** or **Gram Matrix** —must be positive semi-definite.
    
- **Characterization**: A matrix is positive semi-definite if all of its eigenvalues are non-negative , or equivalently, if $x^{T}Mx\ge0$ for all vectors $x\in\mathbb{R}^{n}$.
    

## 3. Practical Kernel Construction

### Popular Base Kernels

Standard options available in libraries like `scikit-learn` include:

- **Polynomial Kernel** (`poly`): $K(x,z) = (x\cdot z+1)^{\rho}$
    
- **Gaussian / Radial Basis Function Kernel** (`rbf`): $K(x,z) = e^{-||x-z||^2/2\sigma^{2}}$
    
- **Hyperbolic Tangent Kernel** (`sigmoid`): $K(x,z) = \tanh(\kappa\cdot x\cdot z-\delta)$
    

### Kernel Building Rules

If $K(x,x^{\prime})$ and $K^{\prime}(x,x^{\prime})$ are valid positive semi-definite kernels, you can construct new valid kernels using these operations:

- **Polynomial combination**: $q(K(x,x^{\prime}))$, where $q()$ is a polynomial with nonnegative coefficients.
    
- **Exponentiation**: $e^{K(x,x^{\prime})}$.
    
- **Product**: $K(x,x^{\prime})K^{\prime}(x,x^{\prime})$.
    
- **Normalization**: $\frac{K(x,x^{\prime})}{\sqrt{K(x,x)K(x^{\prime},x^{\prime})}}$.
    

## 4. Handling Non-Linearly Separable Data (Soft Margins)

In real-world applications, data is rarely perfectly separable even after a non-linear transformation. To resolve this, we relax the strict optimization constraints by introducing **slack variables** $\zeta_{n} \ge 0$:

|**Hard Margin SVM (Original) PDF**|**Soft Margin SVM (Relaxed) PDF**|
|---|---|
|**Objective**: Minimize $\frac{1}{2}\\|w\\|^{$|**Objective**: Minimize $\frac{1}{2}\\|w\\|^{2}+\mathcal{C}\sum_{n=1}^{N}\zeta_{$|
|**Subject to**: $y_{n}(w\cdot x_{n}+b)\ge1$|**Subject to**: $y_{n}(w\cdot x_{n}+b)\ge1-\zeta_{n}$|

- **The Hyperparameter $\mathcal{C}$**: This parameter controls the trade-off penalty between maximizing the margin and allowing constraint violations where $\zeta_{n}>0$.
    
- **Separable Risks**: If $\mathcal{C}$ is set too small on linearly separable data, the optimization may yield a solution that fails to separate the classes cleanly.
    

## 5. Kernels for Non-Standard (Structured) Data

One of the greatest strengths of the kernel trick is that it allows SVMs to process non-numeric, structured objects (like text, shapes, biological strings, or graphs) directly, provided we can construct a valid positive semi-definite kernel matrix.

### A. Text Data & Cosine Similarity

- **Bag of Words Representation**: Text documents are tokenized and preprocessed (lowercasing, punctuation removal, stemming) into terms from a fixed vocabulary of size $n$. A text $t$ is represented as an $n$-dimensional vector $tf(t)$ containing term counts. Because these vectors are mostly zero, sparse structures are preferred.
    
- **Cosine Similarity Formula**: Measures the directional alignment between two term-frequency vectors:
    
    $$\text{cos-sim}(t_{1},t_{2}) = \frac{tf(t_{1})\cdot tf(t_{2})}{||tf(t_{1})||\cdot||tf(t_{2})||}$$
    
- **Kernel Validity**: Cosine similarity is a valid positive semi-definite kernel because it represents a normalized plain dot product.
    
- _Note_: This specific case does not leverage the "kernel trick" to bypass explicit expansion since the $tf(t)$ feature vectors are physically constructed.
    

### B. String Data Features

For data instances consisting of strings $s_n \in \Sigma^*$ , we can extract structural sub-features based on a target sequence $u$:

- $\phi_{u}(s)$: The number of occurrences of $u$ as a continuous **substring** of $s$.
    
- $\phi_{u}^{+}(s)$: The number of occurrences of $u$ as a **subsequence** (gaps allowed) of $s$.
    

> **Example**: For the string $s = \text{"statistics"}$: * For $u = \text{"ti"}$, the substring count $\phi_{u}(s) = 2$, while the subsequence count $\phi_{u}^{+}(s) = 5$.

### C. Advanced String Kernels

- **$p$-Spectrum Kernel**: The feature space is defined by the substring counts of all possible combinations of length $p$ ($\{\phi_{u}|u\in\Sigma^{p}\}$).
    
- **All-Subsequences Kernel**: Tracks the frequency of all possible subsequences of any length ($\{\phi_{u}^{+}|u\in\Sigma^{*}\}$).
    
- **The Computation Challenge**: Evaluating the explicit feature vector for all subsequences is impossible because the feature space is infinite , and calculating just the non-zero features scales exponentially with string length.
    
- **The Dynamic Programming Solution**: By utilizing a dynamic programming approach to recursively match shared sub-structures , the kernel matrix entry $K(s,t)$ can be computed efficiently in $O(|s|\cdot|t|)$ time.
    

## 6. Summary: Pros and Cons of Kernelized SVMs

### Pros (+)

- Extremely powerful and robust framework for complex classification tasks.
    
- Highly successful across practical domains, such as bioinformatics.
    
- Provides uniform generalization: vastly different structured data types are easily mapped into the exact same optimization problem.
    

### Cons (-)

- Inherent binary classifiers; expanding to multi-class problems requires training and combining a collection of multiple binary classifiers (e.g., One-vs-Rest).
    
- Training complexity scales quadratically relative to the number of training instances ($O(N^2)$), making it slow on very large datasets.
    
- Selecting, designing, and optimizing the "right" domain-specific kernel requires massive engineering effort and domain expertise.



## Feature Scaling & Standardization Cheat Sheet

| Model / Algorithm                                        | Recommended Scaling                                    | Mathematical Formula                                                                                                   | Why / Lecture Insight                                                                                                                                                                            |
| :------------------------------------------------------- | :----------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Distance-Based** <br>(KNN)                             | `StandardScaler`                                       | $x_{\text{scaled}} = \frac{x - \mu}{\sigma}$                                                                           | Operates on Euclidean distance $d(x, x')$. Unscaled features with large raw ranges will completely dominate distance calculations, rendering smaller attributes useless.                         |
| **Margin-Based** <br>(SVM)                               | `StandardScaler`                                       | $\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2$                                                                    | Geometric margin width is defined by $\frac{2}{\|\mathbf{w}\|}$. Large-scale features dominate the weight vector $\mathbf{w}$, forcing the hyperplane to ignore smaller variables.               |
| **Gradient-Based** <br>(Logistic Regression, Perceptron) | `StandardScaler`                                       | $\frac{\partial J}{\partial w_j} = \frac{1}{N} \sum_{i=1}^{N} (p_i - y_i) \tilde{x}_{ij}$                              | Prevents highly elongated error valleys. Zero-centering ensures features scale evenly, allowing gradient descent optimization to converge much faster without wild oscillations.                 |
| **Matrix / Probabilistic** <br>(LDA, Least Squares)      | `StandardScaler`                                       | $\tilde{W} = (\tilde{X}^T \tilde{X})^{-1} \tilde{X}^T T$ <br><br> $X \mid Y \sim \mathcal{N}(\mu_k, \Sigma)$           | Protects matrix inversions from floating-point numerical instability ("ill-conditioned" matrices). For LDA, it ensures stable estimation of the shared covariance matrix $\Sigma$.               |
| **Bounded Inputs** <br>(Images / MNIST)                  | `MinMaxScaler`                                         | $x_{\text{scaled}} = \frac{x - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}}$                                       | Pixels naturally live in a fixed architecture $[0, 255]$. Squeezing them to $[0, 1]$ preserves the exact contrast boundaries and structural zero-value backgrounds without warping spatial data. |
| **Sparse Structures** <br>(Text / Bag of Words)          | **Length Normalization** <br>(e.g., Cosine Similarity) | $\text{cos-sim}(t_1, t_2) = \frac{\mathbf{tf}(t_1) \cdot \mathbf{tf}(t_2)}{\|\mathbf{tf}(t_1)\| \|\mathbf{tf}(t_2)\|}$ | **NEVER use StandardScaler.** Subtracting the mean $\mu$ converts structural zeros into non-zero values, completely destroying matrix sparsity and crashing system memory (RAM).                 |

---

### Quick Selection Rule-of-Thumb

* **Use `StandardScaler`** when algorithms compute geometric distances, assume underlying Gaussian distributions, or optimize parameters via raw gradient steps.
* **Use `MinMaxScaler`** when data has clear, natural physical boundaries (like image pixels or explicit bounded percentages) where zero-centering shifts distort the baseline meaning.
* **Use Vector Normalization (Cosine / TF-IDF)** when dealing with highly sparse token matrices (like text documents) to keep your structural zero entries fully intact.

# Lecture Notes: Neural Networks & Backpropagation

## 1. Deep Feedforward Networks & The Basic Unit

A feedforward neural network describes a composite mathematical architecture designed to map continuous inputs to target spaces.

### The Neural Building Unit

At its core, a single neuron evaluates a two-step computation to transform input data:

1. **Linear Combination**: It aggregates incoming inputs $i_j$ by multiplying them by their respective weights $w_j$, forming a single weighted sum vector representation: $I = \sum_{j} i_j \cdot w_j = w^\top i$.
    
2. **Non-linear Activation**: It passes this linear sum through a specialized activation function ($af$) to produce the node's final output: $out = af(I)$.
    

### Common Activation Functions

Activation functions introduce non-linearity, allowing networks to learn complex decision boundaries. The standard primitives are:

- **Sigmoid**: Defined as $af(x) = \frac{1}{1 + e^{-x}}$. It maps values into a smooth curve bounded between 0 and 1, and is often referred to as a "squashed linear function".
    
- **Hyperbolic Tangent ($\tanh$)**: Defined as $af(x) = \tanh(x)$, centering the activation curves around zero.
    
- **Rectified Linear Unit (ReLU)**: Defined as $af(x) = \max(0, x)$, which thresholds negative values directly to zero.
    
- **Identity**: Defined as $af(x) = id(x) = x$, which outputs the combined input value unchanged and is frequently used at the final output layer.
    

### Network Semantics

When stacked together into layers (comprising an **input layer**, **hidden layers**, and an **output layer**), the system models structural mappings. For instance, a continuous mapping function from 4 inputs to 3 outputs ($f: \mathbb{R}^4 \rightarrow \mathbb{R}^3$) can be mathematically unwrapped as a sequential composition:

$$\begin{aligned} h &= f_1(W_1^\top x + b_1) \\ y &= f_2(W_2^\top h + b_2) [cite_start]\end{aligned}$$

## 2. The Learning Framework & Loss Fundamentals

### The Task of Learning

Given a fixed network structure, specified activation functions, and a collection of training examples, the objective is optimization . We seek a parameter state for the weights $w$ that minimizes the global average empirical loss across all $N$ training examples:

$$Loss = \frac{1}{N}\sum_{i=1}^{N}loss(t_i, o_i(w))$$

where $t_i$ represents the target truth values and $o_i(w)$ represents the network's generated outputs given weights $w$.

### Loss/Error Paradigms

The operational form of the loss function depends heavily on the machine learning task:

- **Squared Error**: Calculated as $loss(t,o) = \sum_{i=1}^{m}(t_i - o_i)^2$. If there is only a single output neuron ($m=1$), this simplifies directly to standard regression error metrics.
    
- **Log-Loss**: Formulated directly from negative log-likelihood as $loss(t,o) = -\log p(t|x)$. If we assume the conditional probability follows a Gaussian distribution ($p(t|x) \sim \mathcal{N}(f(x|w), I)$), optimizing the log-loss becomes mathematically equivalent to minimizing the squared error.
    
- **Cross-Entropy**: Formulated as $loss(t,o) = -\sum_{i=1}^{m}t_i \cdot \log(o_i)$. This is used for classification tasks, where network outputs must sit within the interval $[0, 1]$ to be interpreted as categorical class probabilities.
    

## 3. Optimization via Gradient Descent

### Simple Gradient Descent

Gradient descent updates network weights iteratively by calculating the total empirical loss surface gradient and stepping in the exact opposite direction:

$$w' = w - \eta \nabla_{w} Loss(w)$$

where $\eta$ represents the optimization **learning rate**.

The general process follows a straightforward loop:

- Initialize weights $w$ at a random starting coordinate on the cost landscape.
    
- Calculate the loss gradient/derivative vector $\nabla Loss(w)$.
    
- Shift the weight parameters in the opposite direction of the gradient and repeat until convergence.

### Optimization Pitfalls in Deep Landscapes

- **Cliffs and Exploding Gradients**: Deep multi-layered networks often form steep regions ("cliffs") within their cost landscapes. Standard updates can cause parameters to jump excessively far, ruining local progress. To fix this, apply **Gradient Clipping**: if the norm of the gradient exceeds a set threshold $v$ ($\|g\| > v$), normalize it: $g \leftarrow \frac{g v}{\|g\|}$.
    
- **Vanishing Gradients**: When weights are initialized to excessively large values, the inputs to functions like the sigmoid push activations into saturated regions where outputs are close to either 0 or 1. Because the derivative of the sigmoid is $\frac{\partial}{\partial x}\sigma(x) = \sigma(x)(1 - \sigma(x))$, its gradient drops close to 0. Due to the sequential multiplications of the chain rule, this causes gradients in earlier layers to vanish entirely, halting learning.
    

## 4. Stochastic & Mini-Batch Gradient Descent (SGD)

When evaluating loss over large datasets, computing the true gradient requires calculating derivatives across every training instance, yielding a costly $O(N)$ runtime that scales poorly.

### Approximating Expectations

Because the true loss gradient is an empirical expectation, we can approximate it using a small, randomly sampled batch of data instances $B$ while keeping the batch size fixed as the total dataset grows:

$$g = \frac{1}{B}\sum_{i=1}^{B}\nabla_{w}loss(x^{(i)},y^{(i)}|w)$$

Weight updates are then performed using this noisy approximation: $w' = w - \eta g$.

- **Stochastic Gradient Descent (SGD)** refers specifically to a batch size of $B = 1$.
    
- **Mini-Batch Gradient Descent** describes optimization when $B > 1$.
    

### Statistical Returns and Properties

- **Diminishing Statistical Returns**: The standard error of the mean drops at a rate of $\frac{\sigma}{\sqrt{N}}$. This means that increasing sample sizes yields a less-than-linear return on performance. For example, estimating a gradient using 10,000 samples takes 100 times longer than using 100 samples, but only reduces the standard error of your estimate by a factor of 10.
    
- **Unbiased Constraints**: To keep the mini-batch gradient estimate statistically unbiased, samples must be chosen randomly and remain independent. This condition is technically only met during the first pass (epoch) over the dataset. Because of this setup, SGD is highly effective for streaming data environments.
    

### Learning Rate Schedules

Because stochastic approximations introduce noise, the learning rate $\eta$ must decrease over time to guarantee absolute convergence.

- **Sufficient Conditions**: Theoretical convergence requires that $\sum_{i=0}^{\infty}\eta_i = \infty$ and $\sum_{i=0}^{\infty}\eta_i^2 < \infty$.
    
- **In Practice**: This is achieved by systematically lowering the learning rate during training using predefined schedules or by employing adaptive learning algorithms (such as **AdaGrad** or **Adam**) that automatically compute distinct learning rates for individual parameters.
    

## 5. Advanced Optimization: Momentum Techniques

### Momentum

Standard gradient descent struggles in regions of high curvature, fine valleys, or noisy conditions. To fix this, **Momentum** introduces a velocity variable $v$ that tracks an exponentially decaying average of historical negative gradients:

$$\begin{aligned} v &\leftarrow \alpha v - \eta \nabla_{w}\left(\frac{1}{N}\sum_{i=1}^{N}loss(x^{(i)},y^{(i)}|w)\right) \\ w &\leftarrow w + v \end{aligned}$$

- **Terminal Velocity**: If gradients point consistently in the same direction, the system accelerates up to a maximum speed cap of $\frac{\eta\|g\|}{1 - \alpha}$. For example, choosing a momentum hyperparameter of $\alpha = 0.9$ amplifies your maximum velocity by a factor of 10 relative to standard gradient descent.
    

### Nesterov Momentum

An optimized variation where the gradient of the loss surface is evaluated _after_ applying the current velocity step. This gives the optimizer a "look-ahead" capability before computing final parameter shifts:

$$v \leftarrow \alpha v - \eta \nabla_{w}\left(\frac{1}{N}\sum_{i=1}^{N}loss(x^{(i)},y^{(i)}|w + \alpha v)\right)$$

## 6. The Backpropagation Algorithm

### The Core Challenge

Training datasets only provide target annotations ($t$) for output nodes. No target values are available to show the error or guide corrections for internal hidden units.

### Solution: The Chain Rule & Dynamic Programming

Backpropagation solves this by applying the mathematical **chain rule** combined with **dynamic programming**. It computes local error terms for hidden units recursively from the output layer backward, allowing us to find the partial derivatives needed for weight adjustments.

- **Scalar Derivation**: $\frac{\partial f(g(x))}{\partial x} = \frac{\partial f(g(x))}{\partial g(x)} \cdot \frac{\partial g(x)}{\partial x}$.
    
- **Multiple Component Pathways**: If an input branches to affect multiple components, their gradients sum up:
    
    $$\frac{\partial f(g_1(x), g_2(x))}{\partial x} = \frac{\partial f}{\partial g_1}\frac{\partial g_1}{\partial x} + \frac{\partial f}{\partial g_2}\frac{\partial g_2}{\partial x}$$
    
- **Vector-Valued Mappings**: For high-dimensional parameters ($x \in \mathbb{R}^m, y \in \mathbb{R}^n$), the individual scalar component partial derivative is $\frac{\partial z}{\partial x_i} = \sum_{j}\frac{\partial z}{\partial y_j}\frac{\partial y_j}{\partial x_i}$. In vector notation, this is expressed as:
    
    $$\nabla_{x}z = \left(\frac{\partial y}{\partial x}\right)^\top \nabla_{y}z$$
    
    where $\frac{\partial y}{\partial x}$ represents an $n \times m$ **Jacobian Matrix**.
    

Modern machine learning deep frameworks handle this by modeling equations as **Computational Graphs**. To run backpropagation automatically, the framework only needs the explicit structural layout of the network and the local partial derivative formulas for each primitive block (e.g., Matrix Multiplication, Vector Addition, ReLU).


## 6. The Backpropagation Algorithm: An Algorithmic Deep Dive

### 6.1 The Core Intuition: The Backward Flow of "Blame"

While the forward pass computes predictions to determine how _wrong_ the network is, the backward pass acts as a system of **recursive blame assignment**.

Because hidden layers do not have explicit target annotations ($t$), backpropagation uses the calculus chain rule to calculate exactly how much every individual weight and bias contributed to the final loss.

### 6.2 The Computational Graph View

Modern deep learning frameworks (like PyTorch) do not see neural networks as static equations. Instead, they compile them into a **Computational Graph**, where:

- **Nodes** represent primitive mathematical operators (e.g., $+$, $\times$, $\exp$, $\text{ReLU}$).
    
- **Edges** represent the data tensors flowing between operations.
    

During training, this graph executes in two distinct phases:

#### 1. The Forward Pass (Left-to-Right)

Data flows forward through the nodes. Each node takes its inputs, executes its specific mathematical operation, and caches the resulting output values. These cached values are mandatory because they are required later to compute the backward derivatives.

#### 2. The Backward Pass (Right-to-Left)

The loss gradient travels in reverse. Each node receives an **upstream gradient** ($\frac{\partial L}{\partial \text{output}}$) from its right side. It multiplies this upstream gradient by its own **local gradient** ($\frac{\partial \text{output}}{\partial \text{input}}$) to compute the **downstream gradient** ($\frac{\partial L}{\partial \text{input}}$), which it passes along to the left.

### 6.3 Local Gradient Patches: The Primitive Operator Cheat Sheet

By breaking down complex layer equations into simple graph nodes, backpropagation becomes modular. The table below outlines how standard mathematical gates handle incoming gradients:

|**Operator Gate**|**Forward Function**|**Local Gradient (∂x∂z​,∂y∂z​)**|**Gradient Behavior (Intuition)**|
|---|---|---|---|
|**Add Gate**|$z = x + y$|$\frac{\partial z}{\partial x} = 1, \quad \frac{\partial z}{\partial y} = 1$|**Gradient Distributor:** Acts as a traffic splitter. It takes the upstream gradient and passes it along to all inputs completely unaltered.|
|**Multiply Gate**|$z = x \cdot y$|$\frac{\partial z}{\partial x} = y, \quad \frac{\partial z}{\partial y} = x$|**Switch & Scale:** It takes the upstream gradient, multiplies it by the _opposite_ input value, and passes it back.|
|**Max Gate (ReLU)**|$z = \max(0, x)$|$\frac{\partial z}{\partial x} = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{otherwise} \end{cases}$|**Gradient Route Switch:** Acts like an on/off gate. If the path was active forward, the gradient passes intact. If inactive, the gradient dies (0).|
|**Sigmoid Gate**|$z = \sigma(x)$|$\frac{\partial z}{\partial x} = z(1 - z)$|**Squashing Scaler:** Scales the upstream gradient by a decimal factor of at most $0.25$, depending on how saturated the node is.|

### 6.4 Mathematical Anatomy of a Single Layer Chain

Let's unwrap the exact chain rule mechanics for a standard fully-connected layer node. Suppose a hidden node computes a linear combination followed by an activation function:

$$z = w \cdot x + b$$

$$a = \text{af}(z)$$

If the upstream gradient arriving at this node's output is $\frac{\partial L}{\partial a}$, the backward engine evaluates three interconnected partial derivatives:

#### Step 1: Push through the Activation Function

To move back past the activation barrier into the raw linear sum $z$, multiply the upstream gradient by the slope of the activation function evaluated at $z$:

$$\delta = \frac{\partial L}{\partial z} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z} = \frac{\partial L}{\partial a} \cdot \text{af}'(z)$$

This intermediate error term, $\delta$ (delta), represents the sensitivity of the entire loss landscape to changes in that specific neuron's raw input.

#### Step 2: Compute the Parameter Gradients

Now, distribute $\delta$ back to the parameters ($w$ and $b$) to get the final update vectors for your optimizer:

- **Weight Gradient:** Since $\frac{\partial z}{\partial w} = x$, we have:
    
    $$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial w} = \delta \cdot x$$
    
- **Bias Gradient:** Since $\frac{\partial z}{\partial b} = 1$, we have:
    
    $$\frac{\partial L}{\partial b} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial b} = \delta$$
    

#### Step 3: Pass the Signal Deeper (Downstream Gradient)

Finally, to allow earlier layers to continue their learning steps, calculate the gradient for the incoming input features $x$. Since $\frac{\partial z}{\partial x} = w$, we have:

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial x} = \delta \cdot w$$

This value now becomes the fresh upstream gradient for whichever layer sits directly to its left.

### 6.5 Vectorized Backpropagation: The Dimension-Matching Trick

When writing custom neural implementations (such as in NumPy), handling scalar values is trivial, but real networks run on high-dimensional data matrices.

For a vectorized layer where:

- $X$ is a batch input matrix of shape $(B \times D_{\text{in}})$
    
- $W$ is a weight matrix of shape $(D_{\text{in}} \times D_{\text{out}})$
    
- $b$ is a bias vector of shape $(1 \times D_{\text{out}})$
    
- $Z$ is the linear activation matrix of shape $(B \times D_{\text{out}})$
    

The forward pass is:

$$Z = XW + b$$

During backpropagation, calculating explicit multi-dimensional Jacobian matrices is computationally inefficient. Instead, you can rely on the **Dimension-Matching Principle**: the gradient matrix of any parameter must share the exact same matrix dimensions as the parameter itself.

By tracking matrix transpositions, the vectorized matrix equations simplify beautifully into these three standard operations:

$$\delta = \frac{\partial L}{\partial Z} = \frac{\partial L}{\partial A} \odot \text{af}'(Z) \quad \text{[Shape: } B \times D_{\text{out}}\text{]}$$

$$\frac{\partial L}{\partial W} = X^\top \delta \quad \text{[Shape: } D_{\text{in}} \times D_{\text{out}}\text{]}$$

$$\frac{\partial L}{\partial b} = \sum_{\text{rows}} \delta \quad \text{[Shape: } 1 \times D_{\text{out}}\text{]}$$

$$\frac{\partial L}{\partial X} = \delta W^\top \quad \text{[Shape: } B \times D_{\text{in}}\text{]}$$

> **Key Takeaway:** Notice how $X^\top$ and $W^\top$ are arranged. Their positioning is completely forced by matrix multiplication rules so that the resulting shapes perfectly match the dimensions of $W$ and $X$.

### 6.6 The Structural Link to the Vanishing Gradient Problem

Looking at the downstream gradient formula $\frac{\partial L}{\partial X} = \delta W^\top$, you can see precisely why deep networks stall.

If you chain 5 hidden layers together using Sigmoid activations, the overall gradient for the very first layer's weights ($W_1$) expands into an unbroken sequence of matrix multiplications:

$$\frac{\partial L}{\partial W_1} \propto \delta_{\text{out}} \cdot W_5^\top \cdot \sigma'(Z_4) \cdot W_4^\top \cdot \sigma'(Z_3) \cdot W_3^\top \cdot \sigma'(Z_2) \cdot W_2^\top \cdot \sigma'(Z_1) \cdot X^\top$$

Because every single $\sigma'(Z)$ matrix scales elements down by a maximum factor of $0.25$, the backward learning signal is repeatedly crushed layer after layer.

By the time it arrives at $W_1$, the values are mathematically insignificant, causing the earliest feature extractors of your network to remain frozen at their initial random states.

Would you like to complement this backpropagation section by adding a step-by-step mathematical derivation of the Cross-Entropy Loss gradient coupled with a Softmax output layer?



# MOC - Probabilistic Graphical Models

Tags: #machine-learning #probabilistic-models #computational-logic #exam-prep

References: Murphy [PML] Sections 2.3, 2.4, 2.7.4, 3.6, 4.0-4.2, 4.6

## 1. Core Foundations: Bayes' Rule

The structural bedrock for updating a **degree of certainty** fluidly based on new, incoming evidence.

$$p(H \mid Y) = \frac{p(Y \mid H) \cdot p(H)}{p(Y)}$$

### Component Glossary

- **Prior ($p(H)$):** Your baseline, historical belief state before observing the current data.
    
- **Likelihood ($p(Y \mid H)$):** The reliability profile of the evidence. It evaluates how likely the observation $Y$ is under a specific hypothesis $h$. _Note:_ This is a function of $h$, not a probability distribution over it (it does not sum to 1).
    
- **Marginal Likelihood / Denominator ($p(Y)$):** The total probability of observing the evidence across _all_ conceivable timelines. Used as a normalizing constant.
    
- **Posterior ($p(H \mid Y)$):** Your updated belief state.
    

$$\text{Posterior} \propto \text{Prior} \times \text{Likelihood}$$

## 2. Bayesian Belief Networks (BBNs)

A compact factorized representation of a joint probability distribution over a set of random variables.

### Core Motivation

A full joint probability distribution table over $n$ binary variables scales exponentially ($2^n$). BBNs exploit local conditional independence to break a massive, computationally intractable global table down into standalone, modular mini-tables.

### Architectural Layout

- **Topology:** Formally modeled as a **Directed Acyclic Graph (DAG)**.
    
    - **Nodes ($X_i$):** Represent random variables.
        
    - **Directed Edges ($X_i \rightarrow X_j$):** Represent direct causal dependencies.
        
- **Conditional Probability Tables (CPTs):** Every single node holds its own local table. If a node has parents, its CPT defines its probability distribution conditioned exclusively on its parents: $p(X_i \mid \text{pa}(X_i))$.
    

### The Factorization Rule (The Product Loop)

The full joint probability distribution equals the sequential product of every node's local conditional probabilities:

$$p_N(X_1, \dots, X_n) = \prod_{i=1}^{n} p(X_i \mid \text{pa}(X_i))$$

> [!TIP]
> 
> **Directional Construction Rule:** When explicitly writing out the factorization equation, always evaluate nodes **Top-to-Bottom** (from root nodes down to leaves) to maintain natural causal lineages.

## 3. Structural Phenomena & Topological Dependencies

### V-Structures (Colliders)

Occurs when two completely independent parent nodes point directly to a single shared child node ($A \rightarrow C \leftarrow B$).

Plaintext

```
A (Independent Parent 1) ───┐
                            ▼
                          C (Shared Child/Collider)
                            ▲
B (Independent Parent 2) ───┘
```

### Explaining Away (Berkson's Paradox)

- **Unobserved Child:** If $C$ is unknown, $A$ and $B$ are completely independent. Knowing $A$ occurred tells you nothing about the probability of $B$.
    
- **Observed Child:** If $C$ is observed/instantiated ($C = c$), $A$ and $B$ instantly become conditionally dependent. If you discover $A$ happened, it provides a valid root cause for $C$, drastically lowering the structural probability of $B$. The verification of one suspect **explains away** the mystery.
    

## 4. Probabilistic Inference Queries

Using a fully trained network to make active predictions or run downstream diagnostic queries.

$$\text{Query Structure: } p(X_Q \mid X_E = x_e)$$

### Variable Classifications

1. **Query Variables ($X_Q$):** The hidden targets you want to calculate.
    
2. **Evidence Variables ($X_E$):** The variables locked/instantiated to fixed, static observed states ($x_e$).
    
3. **Hidden Variables ($X_H$):** Nuisance parameters that are neither query nor evidence, but must be mathematically handled.
    

### The Inference Pipeline

1. **Restriction:** Slice away all rows across the node tables that do not match the static, real-world observed states ($x_e$).
    
2. **Combination:** Multiply the localized matching slices together using the product rule.
    
3. **Marginalization:** Sum out (erase) all unobserved hidden variables ($X_H$) to isolate the target query variable.
    

$$p(X_Q, x_e) = \sum_{x_h \in X_H} p(X_Q, x_e, x_h)$$

## 5. Parameter Learning Paradigms

### Paradigm A: Learning from Complete Data (MLE)

Used when your training log contains zero missing entries.

#### Maximum Likelihood Estimation (MLE)

MLE treats parameter estimation purely as a frequency counting exercise. To find the optimal parameter $\hat{p}(A \mid B, C)$, filter your database down to rows matching the condition and compute:

$$\hat{p}(A = a \mid B = b, C = c) = \frac{N(A = a, B = b, C = c)}{N(B = b, C = c)}$$

#### Overfitting & Laplace Smoothing

- **The Vulnerability:** If a safe, plausible event simply didn't occur in a small training log, MLE sets its parameter to absolute **0%**, breaking the model if it encounters that state during deployment.
    
- **The Countermeasure:** Inject uniform pseudo-counts (e.g., adding $+1$ to all absolute counts before division) to gracefully spread baseline probability mass to unobserved states.
    

### Paradigm B: Learning from Incomplete Data (EM)

Used when data is Missing at Random (MAR) due to missing fields or unobserved latent variables.

#### The Expectation-Maximization (EM) Algorithm

An iterative optimization method that oscillates between two foundational steps until convergence:

Plaintext

```
┌────────────────────────────────────────────────────────┐
│                                                        │
▼                                                        │
[ E-Step (Expectation) ] ──► Use current parameters to    │
                             compute fractional expected │
                             counts over missing data.   │
                                                         │ (Loop until
                                                         │  convergence)
[ M-Step (Maximization) ] ─► Treat those fractional      │
                             expected counts as true     │
                             counts; run standard MLE    │
                             normalization to update.    │
                                                         │
└────────────────────────────────────────────────────────┘
```

- **Limitation Warning:** EM is highly susceptible to getting trapped in **local maxima**. Guard against this by initializing the algorithm across multiple random parameter seeds.
    

### Paradigm C: Fully Bayesian Learning

Instead of extracting a single best point estimate for a parameter (like MLE/EM), the Fully Bayesian approach treats the parameters ($\theta$) themselves as continuous random variables.

- **Beta Priors:** We model our initial parameter uncertainty using a continuous $\text{Beta}(a, b)$ distribution.
    
- **Conjugacy:** The Beta distribution shares a mathematical _conjugate_ profile with binary variables. If you hold a $\text{Beta}(a, b)$ prior and observe $N_1$ successes and $N_0$ failures, the exact analytic posterior updates effortlessly to:
    

$$\text{Beta}(a + N_1, \, b + N_0)$$

- **Maximum A Posteriori (MAP):** A compromise point-estimate that computes the peak of the posterior distribution, running traditional MLE calculations while factoring in the structural weight of your prior beliefs.

# Master Notes: Probabilistic Graphical Models & Learning Paradigms

Tags: #machine-learning #probabilistic-models #bayesian-networks #parameter-learning #exam-master-note

References: Lecture Slides (Explosion & Pr/Bt/Ut Networks) + Murphy [PML] Sections 2.3, 2.4, 2.7.4, 3.6, 4.1–4.2.5, 4.6–4.6.2.9

## 1. Bayesian Network Foundations & Factorization

A Bayesian Network (Directed Graphical Model) represents a joint probability distribution over a set of random variables by tracking localized causal dependencies.

### 1.1 The Factorization Theorem (The Product Rule)

Instead of maintaining an exponentially large joint probability table ($2^n$ rows for $n$ binary variables), the topology of a Directed Acyclic Graph (DAG) allows the joint distribution to be factorized into a product of local conditional distributions:

$$p_N(X_1, \dots, X_n) = \prod_{i=1}^{n} p(X_i \mid \text{pa}(X_i))$$

Where $\text{pa}(X_i)$ represents the immediate structural parents of node $X_i$.

> [!TIP]
> 
> **Factorization Execution Order:** When mapping a DAG to an algebraic formula, always proceed **Top-to-Bottom** (from root nodes down to leaves). This ensures every parent condition is established before evaluating its dependent children.

### 1.2 The Lecture Slide Blueprint: The "Explosion" Network

To ground the factorization theorem, the lecture introduces a 5-node risk-assessment network:

- **Variables:** Environment ($E$), Leak ($L$), Gas Detector Failed ($G$), Explosion ($X$), Casualties ($C$).
    
- **Topological Parents:** * $\text{pa}(E) = \emptyset$ (Root)
    
    - $\text{pa}(L) = \{E\}$
        
    - $\text{pa}(G) = \{E\}$
        
    - $\text{pa}(X) = \{L, G\}$ (V-structure / Collider node)
        
    - $\text{pa}(C) = \{X\}$
        

Applying the top-to-bottom product rule yields the exact joint probability factorization equation:

$$p(E, L, G, X, C) = p(E) \cdot p(L \mid E) \cdot p(G \mid E) \cdot p(X \mid L, G) \cdot p(C \mid X)$$

## 2. Probabilistic Inference Queries

A Bayesian query computes a specific probability distribution of interest once real-world evidence is introduced into the system.

$$\text{Query Expression: } p(X_Q \mid X_E = x_e)$$

### 2.1 The Three-Way Variable Partition

When executing a query, all network nodes are dynamically categorized into three distinct roles:

1. **Query Variables ($X_Q$):** The target hidden states you want to predict or diagnose.
    
2. **Evidence Variables ($X_E$):** Variables locked to static, hardcoded observations ($x_e$) from real-world data logs (e.g., $G = 1$).
    
3. **Hidden/Nuisance Variables ($X_H$):** Unobserved background variables that are irrelevant to the current question but remain embedded within the system.
    

### 2.2 The Three Fundamental Inference Operations

To compute the distribution for a query, the network runs a localized pipeline using three core probabilistic primitives:

1. **Restriction:** Instantiate the evidence variables. Slices away all rows within the local Conditional Probability Tables (CPTs) that do not match the static observed value $x_e$.
    
2. **Combination:** Multiply the remaining valid sections of the local tables together using the product rule to construct an unified joint view of the active timeline.
    
3. **Marginalisation (Summing Out):** Eliminate the nuisance variables ($X_H$) by summing over all their possible states, leaving only the query targets intact.
    

$$\text{Numerator Calculation: } p(X_Q, x_e) = \sum_{x_h \in X_H} p(X_Q, x_e, x_h)$$

## 3. Parameter Learning: Complete Data (MLE)

Parameter learning is the task of filling the network's empty conditional probability tables with real percentages derived from historical data logs.

### 3.1 Maximum Likelihood Estimation (MLE) Counting

When the dataset $\mathcal{D}$ is **complete** (fully observed with zero missing values), MLE simplifies entirely into a localized row-counting assignment. To find the optimal parameter value $\hat{p}(A \mid B, C)$, filter the spreadsheet to isolate the rows matching the parent conditions and compute the empirical frequency:

$$\hat{p}(A = a \mid B = b, C = c) = \frac{N(A = a, B = b, C = c)}{N(B = b, C = c)}$$

### 3.2 The Zero-Frequency Trap & Laplace Smoothing

- **The Overfitting Problem:** If a particular combination of states is physically possible but simply never appeared within a small training set, MLE sets its parameter to an absolute **0%**. If that state occurs during production deployment, the product rule multiplies by zero, causing the entire joint probability network to crash.
    
- **The Solution (Pseudo-Counts / Smoothing):** Initialize the counting tables by pretending every conceivable state combination has already been observed a baseline number of times (adding a virtual $\alpha$ pseudo-count, typically $+1$, to both the numerator and denominator before normalization).
    

## 4. Parameter Learning: Incomplete Data (EM)

In real-world settings, data logs frequently suffer from missing sensor inputs or contain deliberately unobserved hidden variables.

### 4.1 Missing Data Taxonomy

1. **Missing Completely at Random (MCAR):** Data loss is completely accidental and independent of any variable value (e.g., a hardware sensor briefly loses electrical power).
    
2. **Missing at Random (MAR):** The missing status depends systematically on an alternative variable that _was_ successfully observed (e.g., a backup diagnostic test is omitted if the primary diagnostic test returns negative).
    
3. **Non-ignorable (MNAR):** The omission depends directly on the value of the missing variable itself (e.g., low-income individuals refusing to state their earnings on a financial questionnaire).
    

### 4.2 The Expectation-Maximization (EM) Algorithm

If data is missing at random (MAR), raw counting is impossible. The EM algorithm bypasses this by executing an iterative optimization loop that alters between calculating expectations and maximizing parameters.

#### Phase 0: Initialization

Initialize all network parameters to an initial baseline guess, $P_0$ (such as a uniform uniform distribution).

#### Phase 1: The E-Step (Expectation)

Instead of counting discrete rows, use the **current best-guess parameters** ($P_t$) to run standard Bayesian inference queries over the missing fields (`?`). This replaces missing entries with **fractional expected counts**:

$$\mathbb{E}[N(Pr = \text{yes})] = \sum_{\text{cases}} P_t(Pr = \text{yes} \mid \text{Observed Evidence in Case})$$

#### Phase 2: The M-Step (Maximization)

Treat those fractional expected counts as if they were actual, complete data logs. Run a standard **MLE normalization** (summing and dividing) to update the parameters, generating an upgraded parameter baseline ($P_{t+1}$).

$$\hat{P}_{t+1}(Pr = \text{yes}) = \frac{\mathbb{E}[N(Pr = \text{yes})]}{N_{\text{total}}}$$

#### Phase 3: Loop and Converge

Feed the upgraded $P_{t+1}$ parameters back into Phase 1. Recalculate the expectations for the missing entries (the weights will shift away from the uniform guess and toward the newly discovered patterns). Repeat until the parameters stabilize (**converge**).

> [!WARNING]
> 
> **Local Maxima Risk:** The EM algorithm is mathematically guaranteed to improve parameters at each step, but it is prone to getting trapped in a **local maximum** (a decent configuration that isn't the absolute best global model). To mitigate this, run the EM algorithm multiple times across different random initialization seeds.

## 5. Fully Bayesian Parameter Learning

Instead of finding a single "best" point percentage for a table (like MLE and EM do), the fully Bayesian paradigm treats the parameters ($\theta$) themselves as continuous random variables governed by a **Probability Density Function (PDF)**.

### 5.1 The Beta-Binomial Model

#### The Likelihood

For a series of independent binary trials yielding $N_1$ successes and $N_0$ failures, the data likelihood is represented by:

$$p(\mathcal{D} \mid \theta) \propto \theta^{N_1}(1-\theta)^{N_0}$$

#### The Beta Prior

We model our uncertainty regarding parameter $\theta$ using a continuous $\text{Beta}(a,b)$ distribution, where hyperparameters $a$ and $b$ act as prior virtual counts:

$$p(\theta) \propto \theta^{a-1}(1-\theta)^{b-1}$$

#### The Conjugate Posterior Update

Because the Beta prior is _conjugate_ to the binomial likelihood, the updated posterior distribution stays within the same family. It is computed analytically by adding real-world counts directly to the prior hyperparameters:

$$p(\theta \mid \mathcal{D}) \propto p(\mathcal{D} \mid \theta) \cdot p(\theta) = \text{Beta}(a + N_1, \, b + N_0)$$

### 5.2 Maximum A Posteriori (MAP) vs. Posterior Predictive

- **MAP Point Estimate:** Calculates the absolute peak (mode) of the posterior distribution curve. It balances raw counts with prior weights:
    
    $$\hat{\theta}_{\text{MAP}} = \frac{a + N_1 - 1}{a + b + N_1 + N_0 - 2}$$
    
- **The Posterior Predictive Distribution:** Instead of picking one single parameter estimate, a fully Bayesian prediction **marginalizes (integrates) out** the parameter entirely. It evaluates the probability of the next unseen event ($\tilde{x}$) by weighting every possible parameter value by its posterior plausibility:
    
    $$p(\tilde{x}=1 \mid \mathcal{D}) = \int_{0}^{1} p(\tilde{x}=1 \mid \theta) \, p(\theta \mid \mathcal{D}) \, d\theta = \mathbb{E}[\theta \mid \mathcal{D}] = \frac{a + N_1}{a + b + N_1 + N_0}$$
    

## 6. The Machine Learning Lifecycle: Box's Loop

The lecture concludes by contextualizing the entire parametric learning pipeline within **Box's Loop**, a continuous four-stage engineering cycle for developing and refining probabilistic graphical models:

1. **Build Model (Formulate):** Translate domain expert knowledge into structural nodes and directed causal arrows. Define initial continuous prior choices.
    
2. **Infer Hidden Quantities (Fit):** Run parameter learning algorithms (MLE for complete logs, EM for incomplete logs, or conjugate Bayesian updates) to populate the network's local CPTs.
    
3. **Criticize Model (Evaluate):** Expose the trained network to fresh, out-of-sample data. Identify systematic structural failures, poor predictive scaling, or over-fitted parameters.
    
4. **Revise and Repeat:** Adjust the graph layout based on the evaluation failures (e.g., adding hidden nodes, breaking incorrect independence assumptions) and re-run the loop.

![[Pasted image 20260620213043.png]]


# Lecture 3: Probabilistic Graphical Models & Probabilistic Programming

## 1. Bayesian Network Recap

A Bayesian network provides a compact, factorized representation of a joint probability distribution over a collection of random variables.

### Syntax & Semantics

- **Network Topology**: Structured as a directed acyclic graph (DAG) $\mathcal{G} = \{\mathcal{V}, \mathcal{E}\}$, where the set of vertices $\mathcal{V}$ maps directly to the random variables $X_1, \dots, X_n$.
    
- **Local Conditional Distributions**: The network contains a set of localized conditional tables $\mathcal{P} = \{p(X_i \mid pa(X_i))\}$, where $pa(X_i)$ designates the immediate structural parents of node $X_i$ defined by the edges $\mathcal{E}$.
    
- **Factorization Rule**: The global network semantics dictate that the full joint probability distribution scales as the sequential product of these local conditional distributions:
    
    $$p_{\mathcal{N}}(X_{1}, \dots, X_{n}) = \prod_{i=1}^{n} p(X_{i} \mid pa(X_{i})) \quad \text{[cite: 16]}$$
    

## 2. Plate Notation (Syntactic Sugar)

When dealing with repeated structural subsets in a graph—such as multiple independent trials—drawing every node manually becomes impossible. **Plate notation** serves as visual shorthand to compact these repeating structures cleanly.

|**Notation Style**|**Visual Presentation**|**Mathematical Mechanics**|
|---|---|---|
|**Unfolded Notation**|Draws every independent trial node ($X_1, \dots, X_N$) explicitly, with individual arrows branching from a shared parameter node $\theta$.|$p(\theta, X_1, \dots, X_N) = p(\theta) \prod_{i=1}^N p(X_i \mid \theta)$|
|**Plate Notation**|Collapses the duplicates into a single generic node $X_i$ enclosed inside a rounded box (a **plate**).|The index bound at the corner ($i = 1 : N$) indicates a loop repeating the internal structure $N$ times.|

### Concrete Example: Independent Thumbtack Tosses

- **The Global Parent**: The hidden parameter node $\theta$ sits _outside_ the plate boundary, meaning it remains a single global variable. It follows a Beta prior distribution: $\theta \sim \text{Beta}(2, 5)$.
    
- **The Repeated Child**: The observed coin toss result $X_i$ sits _inside_ the plate box. Each individual trial samples from a conditional Bernoulli likelihood model managed by the parent: $p(X_i = 1 \mid \theta) = \theta$.
    

## 3. Bayesian Linear Regression

Unlike standard ordinary least squares (OLS) regression which yields a single static line, Bayesian linear regression treats parameters as hidden random variables to model full distribution profiles.

### Graphical Model Architecture

- **Global Parameters**: The weights vector $\mathbf{w}$ sits outside the plate as the global latent variable to be inferred.
    
- **Local Data Ingestion**: The input features vector $\mathbf{x}_i$ and target variables $Y_i$ sit inside the plate bounding box, looping across the $N$ samples in the dataset.
    

### Foundational Math

Applying Bayes' rule to this network defines how we update our line coefficients given our training logs:

$$\text{Posterior} \rightarrow p(\mathbf{w} \mid \mathbf{y}, \mathbf{x}) = \frac{p(\mathbf{y} \mid \mathbf{x}, \mathbf{w}) \cdot p(\mathbf{w})}{\int p(\mathbf{y}, \mathbf{x}, \mathbf{w}) d\mathbf{w}} \quad \text{[cite: 55]}$$

- **Likelihood Component ($p(\mathbf{y} \mid \mathbf{x}, \mathbf{w})$)**: Models the continuous target data as a Gaussian distribution centered directly on our linear equation prediction, corrupted by random data noise $\sigma^2$. Note that input attributes are systematically padded with a leading $1$ to capture the intercept bias vector cleanly: $\mathbf{x}_i = [1, x_i]^\top$.
    
    $$Y_i \mid \{\mathbf{w}, \mathbf{x}_i\} \sim \mathcal{N}(\mathbf{w}^\top \mathbf{x}_i, \sigma^2) \quad \text{[cite: 62]}$$
    
- **Prior Component ($p(\mathbf{w})$)**: Captures baseline weight assumptions using a zero-centered multivariate Gaussian distribution scaled by a standard identity matrix covariance:
    
    $$\mathbf{w} \sim \mathcal{N}(\boldsymbol{\mu}_0 = \mathbf{0}, \boldsymbol{\Sigma}_0 = \mathbf{I}_{2\times2}) \quad \text{[cite: 63]}$$
    
- **Denominator**: The marginal integration yields the **marginal likelihood or model evidence**.
    

### Epistemic vs. Aleatoric Uncertainty

A primary advantage of moving to a Bayesian linear approach is that it splits our system errors into two distinct categories:

1. **Aleatoric Uncertainty (Data Noise)**: Captures the intrinsic, irreducible variance in the physical system ($\sigma^2$).
    
2. **Epistemic Uncertainty (Model/Coefficient Uncertainty)**: Captures our lingering doubt regarding the true underlying linear coefficients ($\mathbf{w}$) due to sparse data. As more data points flow into the plate, this uncertainty compresses, causing the group of plausible regression lines to tightly converge.
    

> ### 📊 Real-World Application Study: Topographic Heterogeneity vs. GDP
> 
> The slides highlight this optimization using a real-world macroeconomic dataset comparing country terrain ruggedness against log GDP per capita. * **Outside Africa**: Terrain ruggedness correlates with poor economic performance, yielding a distinct **negative slope** regression line. * **Inside Africa**: Rugged landscapes exhibit a **reverse, positive effect** on overall income levels.
> 
> Bayesian regression models these diverging trends as distinct coefficient distributions, displaying high epistemic uncertainty (wide prediction bands) where localized national data logs are thin.

## 4. Probabilistic Programming Languages (PPLs)

### The Abstraction Analogy

Fifty years ago, software engineering forced practitioners to write applications in low-level languages, requiring deep manual expertise in managing physical hardware configurations rather than focusing on application logic. High-level compiled languages fundamentally democratized development: programmers focused purely on application execution while hardware experts optimized separate automated compilers, driving massive gains in baseline productivity.

Modern machine learning platforms (like NumPy, PyTorch, or TensorFlow) mirror this historical evolution. They isolate lower-level optimization details underneath high-quality, open-source high-level abstractions to democratize technology adoption. **Probabilistic Programming Languages (PPLs)** take this further by treating _probabilistic inference engines_ as the automated compiler.

### Stacked PPL System Architecture

PPLs deploy as a modular, stacked technical architecture to separate concerns between modeling and inference implementation:

```
┌──────────────────────────────────────────────────────────┐
│ Technical Area 1: Domain Experts                         │
│ (Build NLP, Defense, or Cyber Models in Code)            │ [cite: 258, 260, 262, 263]
└───────────────┬──────────────────────────┬───────────────┘
                ▼                          ▼
┌──────────────────────────────────────────────────────────┐
│ Technical Area 2: PPL & Representation Experts           │
│ (Maintain PPL Syntax, Compilers, & High-Level Tools)     │ [cite: 264, 265, 267]
└───────────────┬──────────────────────────┬───────────────┘
                ▼                          ▼
┌──────────────────────────────────────────────────────────┐
│ Technical Area 3: Machine Learning Solver Experts        │
│ (Develop & Integrate Global Math Solvers/Algorithms)      │ [cite: 268, 269, 271, 272]
└───────────────┬──────────────────────────┬───────────────┘
                ▼                          ▼
┌──────────────────────────────────────────────────────────┐
│ Technical Area 4: Inference Engine / Hardware Compilers  │
│ (Optimize Code across CPU, GPU, Cloud, & TPUs)           │ [cite: 273, 274, 277, 278]
└──────────────────────────────────────────────────────────┘
```

- This decoupling ensures that distinct **domain experts** can program complex, customized graphical models using a unified language interface without needing to write manual inference scripts.
    
- Concurrently, **ML experts** concentrate on inventing mathematical solvers while **compiler experts** fine-tune execution speeds across specialized compute architectures.
    

## 5. PPL Lifecycle & 3rd Generation Ecosystems

### Box's Loop in PPL Development

PPL software architectures accelerate model iteration by automating the execution pipeline of **Box's Loop**:

1. **Build Model**: Program the structural graph, mapping causal relationships and entering parametric continuous prior profiles.
    
2. **Infer Hidden Quantities**: Execute the automated PPL compiler to compute parameter values via backend mathematical engines.
    
3. **Criticize Model**: Check real performance metrics against out-of-sample datasets using validation tools.
    
4. **Revise & Repeat**: Quickly adjust code structures based on error trends to rerun the loop rapidly.
    

By abstracting away manual integration proofs, PPLs simplify codebase structures, drastically slash engineering time/costs, and lower the baseline entry barrier for developing probabilistic machine learning frameworks.

### 3rd Generation PPL Capabilities

Modern production frameworks—such as **TensorFlow Probability, Pyro, and PyMC3**—represent the third generation of probabilistic programming tools. They are distinct from historical precursors due to several key features:

- **High-Dimensional Scaling**: Engineered to scale seamlessly to massive real-world data samples and high-dimensional parameter spaces.
    
- **Turing-Complete Structures**: PPL scripts support flexible execution logic, including dynamic conditioning loops and branching control statements.
    
- **Deep Learning Framework Foundations**: Build directly on top of major modern deep learning libraries (like PyTorch or TensorFlow) to leverage their underlying optimization features.
    
- **Automatic Differentiation**: Automatically calculate partial derivative gradients across arbitrary model configurations without analytical code entry.
    
- **Advanced Backend Solvers**: Bypasses slow conjugate math by relying on automated, scalable inference algorithms:
    
    - **Black Box Variational Inference (BBVI)**
        
    - **Hamiltonian Monte Carlo (HMC)**
        
- **Specialized Hardware Acceleration**: Compiles code to run natively on accelerated execution hardware, including GPUs and TPUs.
    

### Deep Framework Profile: Uber's Pyro

- **Development Background**: Maintained by Uber to optimize advanced deep generative models.
    
- **Backend Pipeline**: Relies completely on **PyTorch** as its core deep learning engine.
    
- **Operational Strengths**: Dynamically optimizes modern neural network components, enabling automatic GPU acceleration and distributed multi-node learning configurations.

# Obsidian Notes: Structural Similarity & Link Prediction


## 1. Graph Fundamentals & Network Representations

Social media analysis and biological systems are modeled as standard graph theoretic formulations where actors map to nodes and social relationships map to edges.

### Graph Topologies

- **Directed Graphs:** Edges have a specific orientation; well-suited for modeling asymmetric relationships like Twitter follower mechanics.
    
- **Undirected Graphs:** Edges represent reciprocal or bidirectional relationships, such as Facebook friendships.
    
- **Enhanced Formulations:** Graphs can be weighted (intensity of connection), labeled (type of relationship), or signed (denoting friends vs. foes or positive/negative sentiments).
    

### Computational Formats

Graphs are mathematically defined as $G = (V, E)$ or $G = (V, E, W)$. Because visual configurations do not scale computationally , algorithms process networks using three core discrete tracking layouts:

|**Format**|**Mathematical Structure**|**Best Use Case**|**Efficiency Impact**|
|---|---|---|---|
|**Adjacency Matrix**|An $n \times n$ grid where $A_{i,j} \in \{0, 1\}$ or matches weights.|Dense networks with dense cross-connections.|Highly memory-inefficient; social networks yield highly sparse arrays.|
|**Adjacency List**|An array of linked lists where each node tracks an active register of neighbors.|Sparse networks (behaves like an inverted index layout).|Memory-optimized for large, real-world systems.|
|**Edge List**|An unorganized array of pairs $(u, v)$ denoting individual directional linkages.|Basic serialization or batch storage.|Less effective for localized neighbor structural lookups.|

## 2. Graph Analytic Tasks & Link Prediction

### Core Structural Tasks

1. **Node Classification:** Predicting an individual vertex's missing characteristic (e.g., voting tendencies, hardware sensor breakdown, malicious account hijacking).
    
2. **Link Prediction:** inferring whether a structural connection exists or will form between two isolated vertices.
    
3. **Network/Graph Classification:** Determining a characteristic for an entire unified subgraph topology (e.g., identifying mutagenic molecules).
    

### Link Prediction Paradigm

Link prediction states that if two independent nodes display structural equivalence or high proximity inside the topology, they possess a strong likelihood of creating a local path bridge.

## 3. Vertex Proximity & Local Metric Formulations

### Degree Distributing Dynamics

- **In-Degree ($d_i^{in}$):** Count of directional vectors pointing directly inside node $v_i$.
    
- **Out-Degree ($d_i^{out}$):** Count of directional vectors pointing outward away from node $v_i$.
    
- **Power-Law Distributions:** Real-world interaction networks scale heavily according to popularity behaviors , conforming to a power-law distribution:
    

$$p_d = \beta d^{-\alpha}$$

$$\log(p_d) = \log(\beta) - \alpha \log(d)$$

This configuration implies that localized minor connections are extremely common, while massive, high-degree hubs (e.g., celebrity profiles) are exceptionally rare. The scaling exponent $\alpha$ typically falls in the range $[2, 3]$.

### Local Structural Equivalence Measures

Let $N(v_i)$ denote the immediate neighborhood set of vertex $v_i$. Local structural similarity metrics compute the overlap between these neighborhood sets:

### Absolute Common Neighbors (Vertex Similarity)

Measures the intersection size of the two node neighborhoods.

$$Sim_{\text{vertex}}(v_i, v_j) = |N(v_i) \cap N(v_j)|$$

### Jaccard Similarity

Normalizes the intersection by the total union size of the neighborhoods.

$$Sim_{\text{jaccard}}(v_i, v_j) = \frac{|N(v_i) \cap N(v_j)|}{|N(v_i) \cup N(v_j)|}$$

### Cosine Similarity

Computes proximity normalized by the geometric mean of node degrees.

$$Sim_{\text{cosine}}(v_i, v_j) = \frac{|N(v_i) \cap N(v_j)|}{\sqrt{|N(v_i)| \cdot |N(v_j)|}}$$

> ⚠️ **Exam Warning:** Local similarity values are **not** directly comparable across different metrics. They are only meaningful when ranking elements extracted using the exact same measure.
> 
> Local measures are simple to compute but highly vulnerable to **link spamming maneuvers** and suffer from restricted network coverage.

## 4. Global Prestige: PageRank & Markov Chain Foundations

To bypass localized link spamming manipulation, global prestige tracking analyzes structural characteristics across the entire network topology.

### The Random Web Surfer Framework

PageRank models user movement across a web network as an infinite random walk:

- At any step, a surfer jumps to a completely random web page across the entire network configuration with a baseline probability $\alpha$.
    
- Alternatively, with probability $1 - \alpha$, the surfer chooses an available outbound link from the current page uniformly at random.
    

The PageRank of a node is the limiting fraction of steps the surfer spends at that page.

### Markov Chain Abstraction

A random walk is formally treated as a first-order Markov Chain. Let $q^{(t)}$ represent the state probability distribution array across $n$ nodes at step $t$. The system state updates via matrix multiplication:

$$q^{(t)} = q^{(t-1)}P$$

The transition probability matrix $P$ contains entries defined by out-degree steps:

$$P_{i,j} = \begin{cases} \frac{1}{\text{out-degree}(i)} & \text{if a directed edge } (i \rightarrow j) \text{ exists} \\ 0 & \text{otherwise} \end{cases}$$

### Stationary Distributions & Ergodicity

A probability distribution vector is stationary if it is invariant under the transition step:

$$q^* = q^* P$$

Mathematically, $q^*$ represents the **principal eigenvector** of the transition matrix $P$ corresponding to eigenvalue $1$. In production systems, this vector is recovered via **Power Iteration calculations**.

To guarantee that power iterations converge to a unique stationary state $q^*$, the underlying Markov chain must be **ergodic**:

- **Irreducible:** Every vertex is reachable from every other vertex in the graph.
    
- **Aperiodic:** The network state transitions cannot cycle deterministically across isolated structural sets.
    

A sufficient condition for ergodicity is a strictly positive probability of passing between any two states in a single step.

### The Dangling Page Defect & Teleporting Solutions

Real networks contain **Dangling Pages**—nodes with an out-degree of 0. These act as sinks that trap random surfers, causing the transition rows to sum to zero and breaking the stochastic integrity of the matrix $P$.

To resolve this and enforce ergodicity, the system integrates a **Teleportation Vector Matrix ($U$)**, where every entry equals $1/n$. This modifies the transition matrix into the unified **Google PageRank Matrix**:

$$P_{\text{PageRank}} = (1 - \alpha)P + \alpha U$$

This formulation guarantees that the surfer can always teleport out of local sinks , yielding a stable, unique, and mathematically consistent global prestige score for each node.

## 5. Recursive Similarity: SimRank

### The SimRank Philosophy

SimRank is a structural context measure based on a recursive premise: **"Similar objects are related to other similar objects."**. Two distinct entities are structurally similar if their incoming parent neighbors are themselves similar.

Plaintext

```
       [ Parent Node c ] ───► [ Target Node a ]
              │
      ( Are they similar? )
              ▼
       [ Parent Node d ] ───► [ Target Node b ]
```

### The Analytical Formula

Let $I(a)$ represent the complete set of in-neighbors for node $a$. The structural SimRank equation for any node pair is defined as:

$$s(a, b) = \begin{cases} 1 & \text{if } a = b \\ 0 & \text{if } I(a) = \emptyset \text{ or } I(b) = \emptyset \\ \frac{C}{|I(a)||I(b)|} \sum_{i=1}^{|I(a)|} \sum_{j=1}^{|I(b)|} s(I_i(a), I_j(b)) & \text{if } a \neq b \end{cases}$$

Where:

- $C \in (0, 1)$ acts as a **decay factor or confidence constraint step**. It ensures that similarity decreases as it flows across edges. A standard empirical baseline choice is $C = 0.8$.
    

### Fixed-Point Iterative Computation

To compute this across an entire network graph, we define an iterative calculation loop that tracks updates toward a stable fixed-point:

1. **Initialization ($k=0$):** Nodes are perfectly similar only to themselves.
    
    $$R_0(a, b) = \begin{cases} 1 & \text{if } a = b \\ 0 & \text{if } a \neq b \end{cases}$$
    
2. **Iterative Update Rule:** Compute the step-$k$ similarity using the values from step $k-1$:
    
    $$R_{k+1}(a, b) = \frac{C}{|I(a)||I(b)|} \sum_{i=1}^{|I(a)|} \sum_{j=1}^{|I(b)|} R_k(I_i(a), I_j(b)) \quad (\text{for } a \neq b)$$
    

The values $R_k$ are non-decreasing with respect to $k$. Relative rankings stabilize quickly, typically requiring only around $K \approx 5$ iterations.

## 6. Evaluation Frameworks for Link Prediction

Once a structural similarity matrix $S(v, w)$ is computed, it can be used to rank unconnected node pairs. Higher ranks indicate a greater predicted likelihood of a link forming. To evaluate the quality of these predicted rankings, we use three core verification metrics:

Plaintext

```
Ranked Prediction List:  [ Node X,  Node Y*,  Node Z,  Node W* ]  ( * = True hidden link )
                              │         │        │         │
      Metric Evaluation:   Position 1  Pos 2    Pos 3     Pos 4
```

### HIT Rate

Measures the proportion of prediction lists where a true hidden link appears anywhere within the retrieved results.

$$\text{HIT} = \frac{|\text{Link Prediction Lists where a True Node Appeared}|}{|\text{All Link Prediction Lists}|}$$

- **Limitation:** It treats all positions equally and does not penalize true links that appear low in the ranking.
    

### Mean Reciprocal Rank (MRR)

Evaluates the position of the first successfully predicted link, penalizing errors that occur lower down the ranking list.

$$\text{MRR} = \frac{1}{|\text{All Lists}|} \sum_{L=1}^{|\text{All Lists}|} \frac{1}{\text{rank}(i)}$$

Where $\text{rank}(i)$ is the specific 1-indexed position of the first correct hit in that list.

### Normalized Discounted Cumulative Gain (NDCG)

An alternative ranking metric that accounts for the relative position of all true positive instances across the entire predicted list.

# Obsidian Notes: Link Prediction with Node Embedding Models

**

## 1. Paradigm Shift: Geometric Embeddings vs. Non-Learning Metrics

Traditional graph link prediction tasks compute explicit topological overlaps (e.g., Jaccard, Cosine, or recursive random walks like SimRank). While intuitive, these classic methodologies suffer from significant performance barriers:

- **Computational Bottlenecks:** Tracking pairwise structural similarity calculations or running global random walks to convergence scales poorly on massive, real-world network graphs.
    
- **Topological Sensitivity:** Results are highly susceptible to data noise and structural manipulation (e.g., link spamming).
    
- **Coverage Deficits:** Local proximity tracking exhibits poor topological coverage across detached or multi-hop neighborhoods.
    

### The Embedding Solution

Node embedding methods map raw discrete vertices down into a continuous, low-dimensional vector space: $\mathbb{R}^d$. This framework **trades complex offline model building for fast, parallelized online prediction execution**.

## 2. The Generalized Encoder-Decoder Framework

Graph representation learning treats representation extraction as an entry-to-exit reconstruction optimization problem.

### A. The Encoder ($\text{ENC}$)

The encoder maps an individual discrete node vertex $v \in \mathcal{V}$ into a dense coordinates vector $z_v \in \mathbb{R}^d$. In shallow embedding models, this is implemented as a simple embedding dictionary lookup matrix:

$$\text{ENC}(v) = \mathbf{Z}[v]$$

Where $\mathbf{Z} \in \mathbb{R}^{|\mathcal{V}| [cite_start]\times d}$ represents the entire parameter matrix containing every optimized coordinate feature.

### B. The Decoder ($\text{DEC}$)

The decoder accepts a pair of low-dimensional coordinate profiles $(z_u, z_v)$ and reconstructs their structural relationship value:

$$\text{DEC}(z_u, z_v) \approx S[u, v]$$

Where $S[u, v]$ is the target graph-defined proximity metric (e.g., adjacency or multi-hop overlap).

### C. The Learning Objective

To compress a graph topology accurately, the encoder and decoder parameters are trained to minimize a global reconstruction loss ($\mathcal{L}$) across training node sets ($\mathcal{D}$):

$$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} l\left(\text{DEC}(z_u, z_v), \; S[u,v]\right)$$

> 💡 **Core Thesis:** Predicting missing graph lines occurs naturally as a direct **predictive generalization side effect** of minimizing this global reconstruction loss.

## 3. Matrix Factorization & Inner Product Formulations

The most direct way to execute the encoder-decoder loop is via dot-product matrix decompositions.

### The Formulation

- **Decoder Strategy:** Evaluates the dot product / projection alignment between latent arrays:
    
    $$\text{DEC}(z_u, z_v) = z_u^T z_v$$
    
- **Reconstruction Objective:** Minimizes the squared Frobenius norm between the inner product space and target graph targets:
    
    $$\mathcal{L} \approx \|\mathbf{Z}\mathbf{Z}^T - \mathbf{S}\|_2^2$$
    

### Global Matrix Decompositions (SVD)

By selecting the standard binary adjacency matrix as the target matrix ($\mathbf{S} \triangleq \mathbf{A}$), the system can compute optimal coordinates analytically using **Singular Value Decomposition (SVD)**:

$$\mathbf{R} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$$

SVD isolates hidden relational dimensions by filtering out structural tracking noise, retaining only the top $k$ columns corresponding to the largest singular values.

## 4. Large-Scale Optimization: Funk-SVD & SGD

In real-world networks or user-item bipartite graphs (like the Netflix Prize data layout), the target matrix is **highly sparse** (often $>99\%$ empty). Analytical SVD breaks down here because missing values are unknown rather than zero.

### Funk-SVD Objective

To address this, Simon Funk introduced an optimization framework that evaluates the error function **strictly over observed ratings/links**, ignoring unobserved elements during the optimization step:

$$\text{Error} = \sum_{R_{mu} \in \mathcal{D}_{\text{obs}}} \left( R_{mu} - \sum_{k=1}^{K} A_{mk}B_{ku} \right)^2$$

### Stochastic Gradient Descent (SGD) Updates

Calculating exact gradients over all pairs is computationally prohibitive. Instead, **Stochastic Gradient Descent (SGD)** samples an individual observed link element $R_{mu}$ at random and performs immediate parameters updates:

$$A_{mk} \leftarrow A_{mk} + \eta \left(R_{mu} - \sum_{i=1}^{K} A_{mi}B_{iu}\right) B_{ku}$$

$$B_{ku} \leftarrow B_{ku} + \eta A_{mk} \left(R_{mu} - \sum_{i=1}^{K} A_{mi}B_{iu}\right)$$

Where $\eta$ represents the optimization learning rate step (e.g., Funk's empirical baseline $\eta = 0.001$). Because SGD "dances" around the true global minimum rather than converging smoothly, the step size must be gradually decayed as training progresses.

### Optimization Regularization (Weight Decay)

To prevent embedding values from scaling uncontrollably and overfitting to training configurations, an $L_2$ penalty parameter ($\lambda$) is added to penalize large weights:

$$\mathcal{L}_{\text{reg}} = \sum_{R_{mu} \in \mathcal{D}_{\text{obs}}} \left( R_{mu} - \sum_{k=1}^{K} A_{mk}B_{ku} \right)^2 + \lambda \left( \|\mathbf{A}\|_2^2 + \|\mathbf{B}\|_2^2 \right)$$

### Pre-Processing Residual Adjustments

To accelerate learning, models strip out obvious baseline biases (e.g., a node's baseline connectivity or a user's average rating scale) prior to factorization:

$$R_{mu} \leftarrow R_{mu} - \mu_m - \mu_u + \mu_{\text{global}}$$

Factorization is then performed strictly on the remaining **residual signals**. For inference predictions, these base averages are added back to reconstitute the final prediction scale.

## 5. Geometric Proximity: Laplacian Eigenmaps

An alternative paradigm leverages physical distance minimization instead of inner product alignment.

- **Decoder Strategy (Squared Euclidean Distance):**
    
    $$\text{DEC}(z_u, z_v) = \|z_u - z_v\|_2^2$$
    
- **Loss Function Constraint:** Minimizes distance penalized by local edge weights:
    
    $$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} \|z_u - z_v\|_2^2 \cdot S[u,v]$$
    

This framework shifts coordinates closer together if their connectivity weights are strong. This optimization can be solved analytically using the **unnormalized Graph Laplacian Matrix ($\mathbf{L}$)**:

$$\mathbf{L} = \mathbf{D} - \mathbf{A}$$

Where $\mathbf{D}$ is the diagonal node degree matrix ($D_{ii} = \sum_j W_{ij}$) and $\mathbf{A}$ is the adjacency/weights matrix. This optimization directly satisfies the quadratic vector identity:

$$\mathbf{x}^T \mathbf{L} \mathbf{x} = \frac{1}{2} \sum_{u \in \mathcal{V}}\sum_{v \in \mathcal{V}} A[u,v](x[u] - x[v])^2$$

Evaluating this objective reduces to an **Eigendecomposition problem** ($\mathbf{L}\mathbf{v} = \lambda \mathbf{v}$). The lowest non-zero eigenvectors define the coordinates that preserve the graph's intrinsic manifold structure.

## 6. Stochastic Random Walk Approaches (DeepWalk & Node2Vec)

Random walk approaches define target similarities based on local co-occurrence frequencies along short, simulated paths across the graph topology.

### The Strategy

1. **Target Metric:** Compute $P_R(v \mid u)$, representing the probability that node $v$ appears on a short random walk sequence initialized from node $u$.
    
2. **Inner Product Objective:** Optimize vectors such that their dot product is proportional to this co-occurrence probability:
    
    $$z_u^T z_v \propto P_R(v \mid u)$$
    

### Maximum Likelihood Learning & Softmax

Using a Maximum Likelihood framework, models optimize parameters to maximize neighborhood probabilities:

$$\mathcal{L} = \sum_{u \in \mathcal{V}} \sum_{v \in N_R(u)} -\log\left(P(v \mid z_u)\right)$$

Where the multi-class conditional probability is evaluated using a **Softmax transformation**:

$$P(v \mid z_u) = \frac{\exp(z_u^T z_v)}{\sum_{n \in \mathcal{V}} \exp(z_u^T z_n)}$$

### The Computational Bottleneck & Negative Sampling

Evaluating the Softmax denominator requires computing a nested summation over **every single vertex ($|\mathcal{V}|$) in the graph** for every step, which is computationally prohibitive.

To scale up, models implement **Negative Sampling**. This bypasses the full summation by approximating the denominator with $k$ randomly sampled non-neighbor nodes ("negative samples"), transforming the task into a binary logistic regression objective:

$$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}_{\text{obs}}} -\log\left(\sigma(z_u^T z_v)\right) - \gamma \sum_{l=1}^{k} \log\left(\sigma(-z_u^T z_l)\right)$$

Where $\sigma(x) = \frac{1}{1 + e^{-x}}$, and $k$ typically ranges from $5 \text{ to } 20$ to balance stability and performance.

## 7. Neighborhood Walk Strategies: DeepWalk vs. Node2Vec

The choice of random walk strategy determines the structural properties captured by the embeddings.

|**Strategy**|**Path Mechanics**|**Structural View captured**|**Focus**|
|---|---|---|---|
|**DeepWalk**|Uniform Random Step.|Unbiased, isotropic neighborhood exploration.|General community connectivity.|
|**Node2Vec**|Biased Second-Order Random Step.|Interpolates dynamically between local proximity and global structural roles.|Flexible structural profiling.|

Node2Vec parameterizes this structural trade-off using two search hyperparameters, $p$ and $q$, which bias the walk transitions after arriving at node $v$ from node $t$:

- **Return Parameter ($p$):** Controls the likelihood of immediately backtracking to the previous node ($t$). A low $p$ encourages localized **Breadth-First Search (BFS)** behavior, emphasizing local microscopic neighborhood structures.
    
- **In-Out Parameter ($q$):** Controls the likelihood of moving outward to nodes structurally further from $t$. A low $q$ encourages macro-level **Depth-First Search (DFS)** behavior, driving exploration outward to capture broader structural roles and communities.
    

## 🧠 Oral Exam Blueprint: Shallow Embedding Limitations

If a professor asks you to critically evaluate these shallow embedding techniques on a whiteboard, focus on these three core structural limitations:

1. **Parameter Scaling Inefficiency ($O(|\mathcal{V}|)$ Memory Scaling):** Shallow embedding models maintain a strict 1-to-1 dictionary look-up array. No parameters are shared across individual node encodings. As a result, the parameter footprint scales linearly with graph size, making them unfeasible for billions-scale industrial webs.
    
2. **Feature Isolation (No Node Attributes Integration):** The encoder optimization loop relies entirely on the discrete graph structure matrix. It cannot leverage or inject rich external text, image, or categorical features associated with the nodes.
    
3. **The Transductive Bottleneck (Inductive Failure):** These models cannot generalize to unseen data. If a new node joins the network post-training, the model cannot infer its embedding without re-running the optimization process across the entire graph.


# Obsidian Notes: Link Prediction with Graph Neural Networks

## 1. Topological & Parameter Limitations of Prior Paradigms

To understand the necessity of Graph Neural Networks (GNNs), we must first evaluate the architectural bottlenecks of previous Link Prediction methodologies:

### A. Non-Learning Heuristics (Lecture 8 Recap)

- Local structural similarity metrics (Jaccard, Cosine) and global recursive models (SimRank) contain **zero learnable parameters**.
    
- They compute static topological metrics over localized neighborhoods, which yields **poor neighborhood coverage** across distant regions of the graph.
    
- Highly sensitive to minor structural mutations and vulnerable to targeted structural manipulation (**link spamming**).
    

### B. Shallow Representation Embeddings (Lecture 9 Recap)

- Methods like Matrix Factorization, DeepWalk, and Node2Vec learn vector mappings, but they rely on a strict 1-to-1 look-up table ($\mathbf{Z} \in \mathbb{R}^{|\mathcal{V}| \times d}$).
    
- **No parameter sharing:** Vertices do not share optimization weights during encoding loops.
    
- **Feature Isolation:** Structural models depend entirely on adjacency matrices and cannot integrate raw node attributes or contextual features ($\mathbf{X}$) into the encoding space.
    
- **The Transductive Bottleneck:** These models cannot generalize inductively to unseen data or handle node additions post-training.
    

### The GNN Solution

GNNs replace rigid dictionary look-ups with a generalized, differentiable deep learning encoder. By applying neural message-passing layers, GNNs jointly optimize across **both the graph topology and the local node features**, enabling inductive generalization.

## 2. The Core Neural Message-Passing Framework

The encoder-decoder architecture operates by mapping graph subgraphs down into continuous hidden states, which the decoder then utilizes to predict potential relationships.

### The General Formalization

At layer $k$, each individual vertex $u \in \mathcal{V}$ collects localized incoming signals ("messages") from its immediate open neighborhood $\mathcal{N}(u)$ using a permutation-invariant aggregation function. This aggregated state is then combined with the node's previous hidden state via an update function:

$$m_{\mathcal{N}(u)}^{(k)} = \text{AGGREGATE}^{(k)}\left(\{h_v^{(k)}, \; \forall v \in \mathcal{N}(u)\}\right)$$

$$h_u^{(k+1)} = \text{UPDATE}^{(k)}\left(h_u^{(k)}, \; m_{\mathcal{N}(u)}^{(k)}\right)$$

Where:

- **$\text{UPDATE}$ and $\text{AGGREGATE}$** can be any arbitrary, differentiable neural network components.
    
- **Input Initialization ($k=0$):** The initial hidden state is directly mapped to the raw input feature vector:
    
    $$h_u^{(0)} = x_u, \quad \forall u \in \mathcal{V}$$
    
- **Encoder Termination ($k=K$):** After a fixed execution budget $K$, the final layer output defines the latent node embedding:
    
    $$\text{ENC}(u) = z_u = h_u^{(K)}$$
    

### Input Feature Variations ($\mathbf{X}$)

Depending on the task setting, input features $x_u$ can take several forms:

1. _Exogenous Attributes:_ Rich external text embeddings, images, or categorical records describing the node.
    
2. _Local Topological Statistics:_ Structural metrics like node degree or prestige scores.
    
3. _Identity Tensors (Transductive Mode):_ A standard one-hot identifier index mapping individual nodes, constraining the network to transductive operations.
    

### Graph Unfolding & CNN Analogy

A GNN layer functions similarly to a Convolutional Neural Network (CNN) kernel sliding across a grid. Unfolding a $K$-layer message-passing pipeline around target vertex $u$ creates a localized tree structure. This process ensures that after $K$ operational cycles, the final vector $h_u^{(K)}$ encapsulates both structural and attribute information spanning across the node's complete **$K$-hop neighborhood**.

## 3. Basic GNN Layer Mathematics

### Spatial Node-Level Formulation

In a basic GNN configuration, the aggregation step is implemented as a simple summation of neighbor states, while the update step applies a linear transformation followed by an element-wise activation function:

$$h_u^{(k+1)} = \sigma \left( \mathbf{W}_{\text{self}}^{(k)} h_u^{(k)} + \mathbf{W}_{\text{neigh}}^{(k)} \sum_{v \in \mathcal{N}(u)} h_v^{(k)} + b^{(k)} \right)$$

Where:

- $\mathbf{W}_{\text{self}}^{(k)}, \mathbf{W}_{\text{neigh}}^{(k)} \in \mathbb{R}^{d^{(k)} \times d^{(k-1)}}$ are the learnable parameter matrices shared universally across all graph nodes.
    
- $\sigma$ represents a non-linear activation gate (e.g., Sigmoid, Tanh, or ReLU).
    
- $b^{(k)}$ is an optional structural bias parameter tensor.
    

### Global Graph-Level Matrix Formulation (Self-Loops)

To streamline computation across massive graphs, we can rewrite the node-level operation in an equivalent matrix form. By introducing an Identity Matrix $\mathbf{I}$ to form explicit **Self-Loops**, we can integrate the node's own state directly into the adjacency matrix $\mathbf{A}$, combining the self-update and neighborhood aggregation steps into a single matrix multiplication:

$$\mathbf{H}^{(t)} = \sigma \left( (\mathbf{A} + \mathbf{I})\mathbf{H}^{(t-1)}\mathbf{W}^{(t)} \right)$$

### Link Prediction Decodation

Once the node vectors are generated, the link prediction decoder evaluates the probability of an edge forming between two vertices by computing the dot product of their final layer embeddings:

$$\text{DEC}\left(h_u^{(K)}, h_v^{(K)}\right) = h_u^{(K)T}h_v^{(K)}$$

## 4. Advanced Neighborhood Aggregation Methods

Relying on a simple sum aggregator introduces architectural vulnerabilities. If a graph exhibits a highly skewed degree distribution, high-degree hubs will generate massive message vectors, leading to **numerical instability and optimization failures**.

To stabilize gradient training, several advanced aggregation techniques are used:

### A. Neighborhood Normalization (GCN Style)

To mitigate degree-induced scale imbalances, messages can be normalized using the node's local degree properties:

- _Mean Aggregation:_ Computes a simple localized average:
    
    $$m_{\mathcal{N}(u)} = \frac{\sum_{v \in \mathcal{N}(u)} h_v}{|\mathcal{N}(u)|}$$
    
- _Symmetric Normalization:_ Accounts for the degrees of both the source and target nodes; this formulation serves as the baseline for **Graph Convolutional Networks (GCNs)**:
    
    $$m_{\mathcal{N}(u)} = \sum_{v \in \mathcal{N}(u)} \frac{h_v}{\sqrt{|\mathcal{N}(u)| \cdot |\mathcal{N}(v)|}}$$
    

> 💡 **Design Choice Rule:** Normalization dampens structural degree signals. It is most effective when **node features are significantly more informative** than the raw structural scale or when the graph exhibits extreme degree variations.

### B. Generalized Set Pooling (Deep Sets)

Because neighborhood aggregation operates over an unordered set of variable size, the aggregator must be a **permutation-invariant set function**. Applying a Multi-Layer Perceptron (MLP) mapping before and after a symmetric pooling operation allows the network to function as a universal set function approximator:

$$m_{\mathcal{N}(u)} = \text{MLP}_{\theta} \left( \sum_{v \in \mathcal{N}(u)} \text{MLP}_{\phi}(h_v) \right)$$

_The summation operation can be substituted with alternate reduction operators like element-wise $\min$ or $\max$ pooling blocks._

### C. Janossy Pooling

To leverage sequence models (e.g., LSTMs) while maintaining permutation invariance over unordered neighbor sets, Janossy Pooling evaluates the sequence model over all possible structural permutations $\Pi$ of the neighborhood list and computes the average:

$$m_{\mathcal{N}(u)} = \text{MLP}_{\theta} \left( \frac{1}{|\Pi|} \sum_{\pi \in \Pi} \rho_{\phi}\left(h_{v_1}, h_{v_2}, \dots, h_{v_{|\mathcal{N}(u)|}}\right)_{\pi} \right)$$

_To manage the computational cost of evaluating all permutations, practical implementations sample a random subset of permutations or enforce a canonical sorting criterion based on node degrees._

### D. Neighborhood Attention (GAT)

Rather than treating all neighbors equally, **Graph Attention Networks (GATs)** dynamically assign a learnable importance weight $\alpha_{u,v}$ to each incoming edge:

$$m_{\mathcal{N}(u)} = \sum_{v \in \mathcal{N}(u)} \alpha_{u,v}h_v$$

The attention coefficients are computed by applying a Softmax normalization over localized structural features:

|**Attention Mechanism**|**Formula for αu,v​ Coefficient Computation**|**Characteristics**|
|---|---|---|
|**Concatenation Head**|$$\frac{\exp\left(\mathbf{a}^T [\mathbf{W}h_u \oplus \mathbf{W}h_v]\right)}{\sum_{v' \in \mathcal{N}(u)} \exp\left(\mathbf{a}^T [\mathbf{W}h_u \oplus \mathbf{W}h_{v'}]\right)}$$|Standard GAT setup; projects nodes linearly before concatenating ($\oplus$) and multiplying by an attention vector $\mathbf{a}$.|
|**Bilinear / Inner-Product**|$$\frac{\exp\left(h_u^T \mathbf{W} h_v\right)}{\sum_{v' \in \mathcal{N}(u)} \exp\left(h_u^T \mathbf{W} h_{v'}\right)}$$|Computes similarity via a direct parametric matrix dot product projection.|
|**MLP Head**|$$\frac{\exp\left(\text{MLP}(h_u, h_v)\right)}{\sum_{v' \in \mathcal{N}(u)} \exp\left(\text{MLP}(h_u, h_{v'})\right)}$$|Employs a dedicated feed-forward layer to extract non-linear relational dependencies.|

## 5. Advanced Update architectures

### The Over-Smoothing Trap

As the depth of a GNN ($K$) increases, the network risks running into **Over-Smoothing**. Because message-passing repeatedly mixes features across neighborhoods, the latent vectors of all nodes begin to converge after multiple updates. This causes distinct node-specific information to wash out, leaving the embeddings dominated by uniform neighborhood averages.

[Image illustrating over-smoothing in deep GNN layouts where node states become homogeneous]

To combat over-smoothing and preserve a node's distinct features across deep layers, models can use advanced update architectures:

### Concatenation Updates

Instead of sum-aggregating the current state and neighbor messages, this approach explicitly isolates the node's prior characteristics by concatenating ($\oplus$) the history vector directly alongside the newly computed message space:

$$\text{UPDATE}_{\text{concat}}\left(h_u, m_{\mathcal{N}(u)}\right) = \left[\text{UPDATE}_{\text{base}}\left(h_u, m_{\mathcal{N}(u)}\right) \;\oplus\; h_u \right]$$

### Gated Linear Interpolation

This method uses an explicit gating mechanism to regulate the information flow, balancing the preservation of the node's current state with the integration of new incoming neighborhood messages:

$$\text{UPDATE}_{\text{interpolate}}\left(h_u, m_{\mathcal{N}(u)}\right) = \mathbf{\alpha}_1 \circ \text{UPDATE}_{\text{base}}\left(h_u, m_{\mathcal{N}(u)}\right) + \mathbf{\alpha}_2 \circ h_u$$

Where:

- $\circ$ denotes element-wise vector multiplication.
    
- $\mathbf{\alpha}_1, \mathbf{\alpha}_2 \in [0, 1]^d$ act as learnable gating vectors constrained such that $\mathbf{\alpha}_2 = 1 - \mathbf{\alpha}_1$. These gates are typically optimized using an auxiliary MLP or GNN sub-layer block.