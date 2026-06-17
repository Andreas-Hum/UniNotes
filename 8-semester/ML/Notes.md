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