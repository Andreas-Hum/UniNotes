# Lecture 1: Linear Models for Classification I

## 1. Executive Summary & Core Objectives

- **Overview:** This lecture introduces the fundamental concepts of linear models for classification, where linear combinations of input features are utilized to establish decision surfaces. While geometrically restricted to hyperplanes, linear models serve as critical standalone classifiers and form the structural foundation for more sophisticated non-linear architectures, such as deep neural networks.
    
- **Core Objectives:**
    
    - Mathematically define linear discriminant functions and analyze the underlying geometry of hyperplanes.
        
    - Evaluate multi-class classification strategies, explicitly contrasting the limitations of binary ensembles (One-Against-All, One-Against-One) with the geometric consistency of joint linear discriminant functions.
        
    - Frame classification through the lens of multi-target linear regression using least-squares parameter estimation.
        
    - Expose the fundamental theoretical flaws of the least-squares objective function when applied to classification tasks, specifically its high sensitivity to outliers and its tendency to penalize "over-correct" predictions.
        

## 2. Theoretical Foundations & Mathematical Models

### Binary Classification and Hyperplane Geometry

A linear discriminant function downmaps a $D$-dimensional input vector $\mathbf{x}$ to a scalar score $y(\mathbf{x})$ via an affine transformation:

$$y(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + w_0$$

where $\mathbf{w} \in \mathbb{R}^D$ is the weight vector (controlling orientation) and $w_0 \in \mathbb{R}$ is the bias or threshold parameter. The decision surface is defined by the locus of points where the discriminant function evaluates to zero:

$$\{ \mathbf{x} \in \mathbb{R}^D \mid y(\mathbf{x}) = 0 \}$$

This equation defines a $(D-1)$-dimensional hyperplane embedded within a $D$-dimensional feature space. Let $\mathbf{x}_1$ and $\mathbf{x}_2$ be any two arbitrary points residing strictly on this decision hyperplane. Because $y(\mathbf{x}_1) = y(\mathbf{x}_2) = 0$, it follows that:

$$\mathbf{w}^T \mathbf{x}_1 + w_0 = \mathbf{w}^T \mathbf{x}_2 + w_0 \implies \mathbf{w}^T (\mathbf{x}_1 - \mathbf{x}_2) = 0$$

Since $(\mathbf{x}_1 - \mathbf{x}_2)$ defines a vector parallel to the hyperplane, the weight vector $\mathbf{w}$ is proven to be strictly orthogonal to every vector lying within the decision surface. Thus, $\mathbf{w}$ dictates the normal orientation of the hyperplane.

The algebraic distance from an arbitrary input point $\mathbf{x}$ to the hyperplane is given by $\frac{y(\mathbf{x})}{\|\mathbf{w}\|}$. Consequently, the perpendicular distance from the origin to the hyperplane is found by setting $\mathbf{x} = \mathbf{0}$:

$$\text{Distance}_{\text{origin}} = \frac{w_0}{\|\mathbf{w}\|}$$

The hyperplane rigidly partitions the continuous input space into two disjoint decision regions:

- $\mathcal{R}_1 = \{ \mathbf{x} \mid y(\mathbf{x}) \geq 0 \}$, mapped to class $\mathcal{C}_1$.
    
- $\mathcal{R}_2 = \{ \mathbf{x} \mid y(\mathbf{x}) < 0 \}$, mapped to class $\mathcal{C}_2$.
    

### Multi-Class Generalizations

When extending classification to $K > 2$ discrete classes, binary decomposition heuristics introduce geometric ambiguities:

1. **One-Against-All (One-vs-Rest):** Constructs $K$ independent binary classifiers, each trained to distinguish class $\mathcal{C}_k$ from all remaining $K-1$ classes. This induces ambiguous regions where multiple classifiers simultaneously output positive predictions, or where no classifier claims a point.
    
2. **One-Against-One (One-vs-One):** Constructs $\frac{K(K-1)}{2}$ binary classifiers covering all unique pairs. Classification proceeds via a majority voting scheme. This approach suffers from unassigned, non-convex decision spaces where voting deadlocks occur.
    

> [!note] Ambiguity Resolution via Joint Linear Discriminants
> 
> To eliminate unassigned territories, we define a joint framework comprising $K$ distinct linear functions evaluated simultaneously:
> 
> $$y_k(\mathbf{x}) = \mathbf{w}_k^T \mathbf{x} + w_{k0}$$
> 
> An input vector $\mathbf{x}$ is assigned to class $\mathcal{C}_k$ if and only if its corresponding discriminant score is strictly greater than all other scores:
> 
> $$\mathbf{x} \in \mathcal{C}_k \quad \text{if} \quad y_k(\mathbf{x}) > y_j(\mathbf{x}) \quad \forall j \neq k$$
> 
> The decision boundary separating class $\mathcal{C}_k$ from class $\mathcal{C}_j$ occurs where their scores tie, yielding a linear decision boundary:
> 
> $$(\mathbf{w}_k - \mathbf{w}_j)^T \mathbf{x} + (w_{k0} - w_{j0}) = 0$$
> 
> Because these regions are defined as the intersection of multiple open half-spaces, the resulting decision spaces are guaranteed to be single-connected and strictly convex.

### Matrix Representation of Multi-Class Discriminants

The system of $K$ discriminant functions can be concisely formulated in vector-matrix notation as:

$$\mathbf{y}(\mathbf{x}) = \mathbf{w}_0 + \mathbf{W}^T \mathbf{x}$$

where $\mathbf{w}_0$ is a $K$-dimensional bias vector, and $\mathbf{W}$ is a $D \times K$ weight matrix whose columns correspond to the class weight vectors. By appending a dummy input coordinate $x_0 = 1$, we construct an augmented input vector $\tilde{\mathbf{x}} = (1, \mathbf{x}^T)^T \in \mathbb{R}^{D+1}$ and an augmented weight matrix $\tilde{\mathbf{W}} = (\mathbf{w}_0, \mathbf{W}^T)^T \in \mathbb{R}^{(D+1) \times K}$. This simplifies the entire system to a single linear operation:

$$\mathbf{y}(\mathbf{x}) = \tilde{\mathbf{W}}^T \tilde{\mathbf{x}}$$

### Classification by Least Squares Regression

Least-squares classification treats class assignment as a multi-target linear regression problem. Each training sample's discrete label $y_n \in \{1, \dots, K\}$ is transformed into a binary target vector $\mathbf{t}_n \in \mathbb{R}^K$ using a 1-of-$K$ (one-hot) encoding scheme.

Given a dataset of $N$ observations, let $\tilde{\mathbf{X}}$ denote the $N \times (D+1)$ design matrix where row $n$ equals $\tilde{\mathbf{x}}_n^T$, and let $\mathbf{T}$ represent the $N \times K$ target matrix where row $n$ equals $\mathbf{t}_n^T$. The global sum-of-squares objective function over the matrix parameter space is expressed as:

$$E_D(\tilde{\mathbf{W}}) = \frac{1}{2} \sum_{n=1}^N \|\tilde{\mathbf{W}}^T \tilde{\mathbf{x}}_n - \mathbf{t}_n\|^2 = \frac{1}{2} \text{Tr}\left\{ (\tilde{\mathbf{X}}\tilde{\mathbf{W}} - \mathbf{T})^T (\tilde{\mathbf{X}}\tilde{\mathbf{W}} - \mathbf{T}) \right\}$$

To minimize $E_D(\tilde{\mathbf{W}})$, we compute the matrix derivative with respect to $\tilde{\mathbf{W}}$ and equate the gradient to the zero matrix, which yields the normal equations:

$$\frac{\partial E_D}{\partial \tilde{\mathbf{W}}} = \tilde{\mathbf{X}}^T(\tilde{\mathbf{X}}\tilde{\mathbf{W}} - \mathbf{T}) = \mathbf{0} \implies \tilde{\mathbf{X}}^T \tilde{\mathbf{X}} \tilde{\mathbf{W}} = \tilde{\mathbf{X}}^T \mathbf{T}$$

Assuming $\tilde{\mathbf{X}}^T \tilde{\mathbf{X}}$ is non-singular, isolating the augmented parameter matrix yields the closed-form analytical solution:

$$\tilde{\mathbf{W}} = (\tilde{\mathbf{X}}^T \tilde{\mathbf{X}})^{-1} \tilde{\mathbf{X}}^T \mathbf{T}$$

_Note on Structural Transformations:_ If the data matrix is configured such that individual features form the rows and individual samples form the columns (i.e., $\tilde{\mathbf{X}} \in \mathbb{R}^{(D+1) \times N}$ and $\mathbf{T} \in \mathbb{R}^{K \times N}$), the algebraic order of the closed-form normal equation shifts to preserve row-column multiplication compliance:

$$\tilde{\mathbf{W}} = \mathbf{T} \tilde{\mathbf{X}}^T (\tilde{\mathbf{X}} \tilde{\mathbf{X}}^T)^{-1}$$

## 3. Practical Implementation & Self-Study Bridge

An analysis of `lecture1.ipynb` reveals the absolute alignment between the continuous mathematical geometry and its implementation in discrete array tracking frameworks.

### Experiment 1: Verifying Hyperplane Orthogonality

To analyze the binary discriminant line $y_1(x_1, x_2) = 2 - \frac{2}{3}x_1 - x_2 = 0$, the notebook isolates the vertical axis mapping to enable standard programmatic plotting:

$$x_2 = -\frac{2}{3}x_1 + 2$$

The vector normal to this boundary line is explicitly defined by the weights: $\mathbf{w} = \left(-\frac{2}{3}, -1\right)^T$. The notebook validates orthogonality numerically:

1. Identifies two arbitrary coordinate pairs situated on the line: $A = (0, 2)$ and $B = (3, 0)$.
    
2. Constructs a continuous directional vector parallel to the line boundary by subtraction:
    
    $$\mathbf{x}_{\perp} = A - B = \begin{pmatrix} 0 - 3 \\ 2 - 0 \end{pmatrix} = \begin{pmatrix} -3 \\ 2 \end{pmatrix}$$
    
3. Computes the inner dot product vector multiplication:
    
    $$\mathbf{w}^T \mathbf{x}_{\perp} = \begin{pmatrix} -\frac{2}{3} & -1 \end{pmatrix} \begin{pmatrix} -3 \\ 2 \end{pmatrix} = \left(-\frac{2}{3} \cdot -3\right) + (-1 \cdot 2) = 2 - 2 = 0$$
    

Because the dot product evaluates to $0.0$, the geometric property that the weight vector acts as a normal vector to the decision hyperplane is verified. Testing the origin $(0, 0)$ outputs $y_1(0,0) = 2 > 0$, indicating that the decision region $y_1(\mathbf{x}) > 0$ forms the open half-plane containing all points below and to the left of the hyperplane line.

### Experiment 2: The Failure Mode of Least-Squares Classification

The second notebook experiment evaluates a classification dataset containing $N=3$ samples across $D=2$ features and $K=2$ classes, organized as columns:

$$X = \begin{pmatrix} 1 & 1 & 0 \\ 1 & 5 & 1 \end{pmatrix}, \quad T = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

The notebook evaluates the global Sum-of-Squares Error (SSE) for two distinct heuristic parameter configurations using the matrix trace method:

Python

```python
# NumPy Trace Implementation of SSE Evaluation
E_D = 0.5 * np.trace(np.matmul((Y - Target).T, (Y - Target)))
```

Evaluating the models yields the following results:

- **Model 1 ($W_1$):** Achieves **100% classification accuracy** but records a high **SSE of 89.0**.
    
- **Model 2 ($W_2$):** Misclassifies a sample ($x_3$) but outputs a significantly lower **SSE of 23.5**.
    

This demonstrates that the least-squares objective function does not align directly with classification accuracy. Because it treats classification labels as continuous numerical targets, points located far on the correct side of the decision boundary generate large error penalties, forcing the line to shift and degrade classification accuracy.

By applying the column-based closed-form equation, the notebook calculates the optimal parameter matrix $W_3$:

Python

```python
# Optimal Weights Closed-Form Implementation
O = np.linalg.inv(np.matmul(X, X.T))
F = np.matmul(Target, X.T)
OW = np.matmul(F, O)  # W3 Weight Matrix
```

The resulting optimal matrix $W_3 = \begin{pmatrix} 1.0 & 0.0 \\ -0.333 & 0.111 \end{pmatrix}$ minimizes the system error to a global minimum **SSE of 0.444** while correctly classifying all three data samples.

### Experiment 3: Visualizing Ambiguity vs. Convex Decision Spaces

The final experiment maps three separate linear functions:

$$y_1(\mathbf{x}) = 2 - \frac{2}{3}x_1 - x_2, \quad y_2(\mathbf{x}) = 3 + 3x_1 - x_2, \quad y_3(\mathbf{x}) = 1 + \frac{1}{10}x_1 - \frac{1}{4}x_2$$

- **One-Against-One Setup:** When these lines act as independent pairwise boundary lines, the notebook fills the voting spaces using `fill_between`. This setup isolates a central **ambiguous zone ($\emptyset$)** where a voting deadlock occurs ($a > b$, $b > c$, and $c > a$), demonstrating that pairwise voting schemes can create regions with unassigned labels.
    
- **Joint Discriminant Setup:** When treating $y_1, y_2, y_3$ as joint discriminant models representing class scores $y_a, y_b, y_c$, the boundary lines are plotted where the scores tie (e.g., $y_a - y_b = 0$):
    

Python

```python
# Boundary line tracing via score ties
plt.contour(X1, X2, score_A - score_B, levels=[0], colors="blue")
plt.contour(X1, X2, score_A - score_C, levels=[0], colors="red")
plt.contour(X1, X2, score_B - score_C, levels=[0], colors="green")
```

This multi-class discriminant approach partitions the grid into convex, contiguous decision spaces without unassigned territories or overlap, confirming the geometric advantage of joint discriminants.

## 4. Critical Insights & Conceptual Connections

### The Outlier and Over-Confidence Penalty

The sum-of-squares error function derives from a maximum likelihood estimation framework assuming a Gaussian conditional noise distribution. While suitable for continuous regression tasks, this assumption fails for classification where the targets are discrete binary indicators ($0$ or $1$). Least squares penalizes accurate predictions that are far from the decision boundary (e.g., predicting $y_k(\mathbf{x}) = 4$ for a target of $1$) as severely as it penalizes misclassifications. This makes least-squares classification highly sensitive to outlier points, which can pull the decision boundary away from its optimal position and ruin the classification performance on linearly separable datasets.

### Geometric Enclosure and Convexity

Multi-class decision boundaries face distinct structural limitations depending on how they are composed:

- Binary classification extensions (One-vs-Rest and One-vs-One) combine separate lines independently, which can introduce geometric ambiguities like overlapping region assignments or completely unassigned zones.
    
- In contrast, joint linear discriminant functions choose class assignments based on the maximum scalar score (`argmax`). This guarantees that all decision spaces are convex and contiguous, meaning that any line segment connecting two points within the same class region stays entirely within that region.
    

### Capacity vs. Optimization Diversity

Different linear classifiers—such as the Perceptron, Naive Bayes models, and Least Squares Classification—share the exact same geometric capacity, meaning they can all represent linear decision boundaries. However, because they optimize completely different objective functions (e.g., error-correction updates vs. joint generative likelihood maximization vs. mean-squared error minimization), they converge to different parameter states and exhibit unique sensitivities to noise, outliers, and varying dataset densities.

# Lecture 2: Linear Models for Classification II

## 1. Executive Summary & Core Objectives

This lecture advances the study of linear models for classification by moving from non-probabilistic hyperplanes (such as the Perceptron and Least Squares) to advanced statistical methods. It establishes a fundamental architectural division in machine learning: **Generative** versus **Discriminative** modeling.

The core objectives of this session are:

- **Deconstruct Generative Classifiers:** Analyze how Naive Bayes, general Gaussian Mixture Models (GMMs), and Linear Discriminant Analysis (LDA) model the joint probability distribution $P(\mathbf{X}, Y)$ to compute class posteriors via Bayes' theorem.
    
- **Formulate Discriminative Learning:** Analyze **Logistic Regression** as a direct model of the conditional posterior probability $P(Y|\mathbf{X})$ through the logistic sigmoid function, and evaluate its optimization via conditional maximum likelihood.
    
- **Establish a Multi-Model Comparative Framework:** Evaluate the mathematical criteria, computational complexities, and structural limitations of Least Squares, Perceptron, LDA, and Logistic Regression.
    
- **Introduce Maximum Margin Optimality:** Formulate the foundations of **Support Vector Machines (SVMs)** using constrained quadratic optimization and Lagrange duality, demonstrating why optimal decision boundaries depend solely on data inner products.
    
- **Examine Feature Space Transformations:** Understand how non-linear mappings $\boldsymbol{\phi}(\mathbf{x})$ project non-linearly separable input data into high-dimensional spaces where linear separation becomes mathematically viable.
    

## 2. Theoretical Foundations & Mathematical Models

### A. The Generative vs. Discriminative Paradigms

A classification task requires predicting a discrete class label $Y \in \{1, \dots, K\}$ given an input feature vector $\mathbf{x} \in \mathbb{R}^D$. Probabilistic classifiers determine the optimal class by finding $\arg\max_k P(Y=k|\mathbf{x})$. The two primary paradigms approach this computation differently:

#### 1. Generative Approach

Generative models learn the joint probability distribution $P(\mathbf{X}, Y)$, typically factored as the product of the class prior $P(Y)$ and the class-conditional density $P(\mathbf{X}|Y)$:

$$P(\mathbf{X}, Y) = P(Y)P(\mathbf{X}|Y)$$

To classify a new instance $\mathbf{x}$, the model applies **Bayes' theorem** to derive the conditional posterior probability:

$$P(Y=k|\mathbf{X}=\mathbf{x}) = \frac{P(\mathbf{X}=\mathbf{x}|Y=k)P(Y=k)}{P(\mathbf{X}=\mathbf{x})} = \frac{P(\mathbf{X}=\mathbf{x}|Y=k)P(Y=k)}{\sum_{j=1}^K P(\mathbf{X}=\mathbf{x}|Y=j)P(Y=j)}$$

#### 2. Discriminative Approach

Discriminative models skip the modeling of the input feature distribution $P(\mathbf{X})$ and directly learn the conditional posterior distribution $P(Y|\mathbf{X})$ from the data.

|**Feature / Operation**|**Generative Models**|**Discriminative Models**|
|---|---|---|
|**Primary Target**|Joint Distribution $P(\mathbf{X}, Y)$|Conditional Posterior $P(Y\mid\mathbf{X})$|
|**Predicting $Y$ given $\mathbf{X}$**|**Yes**: Via Bayes' Theorem|**Yes**: Direct Functional Mapping|
|**Predicting Missing Features $X_i$**|**Yes**: Computes arbitrary conditionals $P(X_i \mid \mathbf{X}_{\setminus i})$|**No**|
|**Data Generation**|**Yes**: Can sample synthetic points $(\mathbf{x}, y) \sim P(\mathbf{X}, Y)$|**No**|
|**Optimization Criterion**|Maximize Joint Likelihood: $\prod_{n=1}^N P(\mathbf{x}_n, y_n)$|Maximize Conditional Likelihood: $\prod_{n=1}^N P(y_n \mid \mathbf{x}_n)$|
|**Data Efficiency**|Requires parametric models for both $P(Y)$ and $P(\mathbf{X}\mid Y)$|More sample-efficient for a fixed prediction task|

### B. Naive Bayes & General Gaussian Mixture Models (GMM)

When modeling the class-conditional density $P(\mathbf{X}|Y=k)$ for continuous features, different assumptions about feature independence change the complexity of the model:

#### 1. Naive Bayes Classifier

The Naive Bayes model introduces a strict conditional independence assumption: configuration of any feature $X_i$ is entirely independent of any other feature $X_j$ given the class label $Y$. Mathematically, this eliminates off-diagonal feature interactions:

$$P(\mathbf{X} = \mathbf{x} \mid Y=k) = \prod_{i=1}^D P(X_i = x_i \mid Y=k)$$

If the features $X_i$ are continuous and modeled as univariate Gaussians $\mathcal{N}(\mu_{i,k}, \sigma_{i,k}^2)$, the joint class-conditional distribution forms a multivariate normal distribution with a **strictly diagonal covariance matrix**:

$$\boldsymbol{\Sigma}_k = \text{diag}(\sigma_{1,k}^2, \sigma_{2,k}^2, \dots, \sigma_{D,k}^2)$$

#### 2. General Gaussian Mixture Models (GMM)

Without the naive independence assumption, a generative classifier models the class-conditional density using an unrestricted multivariate normal distribution for each class $k$:

$$P(\mathbf{X}=\mathbf{x} \mid Y=k) = \frac{1}{(2\pi)^{D/2}|\boldsymbol{\Sigma}_k|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_k)^T\boldsymbol{\Sigma}_k^{-1}(\mathbf{x}-\boldsymbol{\mu}_k)\right)$$

Here, $\boldsymbol{\mu}_k \in \mathbb{R}^D$ represents the class-specific mean vector, and $\boldsymbol{\Sigma}_k \in \mathbb{R}^{D \times D}$ represents the class-specific covariance matrix. Non-zero off-diagonal entries ($\sigma_{i,j,k} \neq 0$) capture the linear correlations between features $X_i$ and $X_j$ within class $k$.

### C. Linear Discriminant Analysis (LDA)

**Linear Discriminant Analysis (LDA)** is a specific variation of the generative Gaussian mixture framework. It operates under a key constraint: **all classes share the exact same covariance matrix**.

$$\boldsymbol{\Sigma}_1 = \boldsymbol{\Sigma}_2 = \dots = \boldsymbol{\Sigma}_K = \boldsymbol{\Sigma}$$

> [!note]
> 
> In literature (such as _Bishop Section 4.2.1_), this model is mathematically derived as the classification boundary for shared-covariance Gaussians, though it is not explicitly called "LDA" to avoid confusion with **Fisher's Linear Discriminant**. Fisher's method is a non-probabilistic dimensionality reduction technique that maximizes between-class variance relative to within-class variance, rather than a generative probabilistic model.

#### Mathematical Derivation of the Linear Boundary

To observe why this constraint creates a linear decision boundary, consider the log-posterior ratio between class $k$ and class $j$:

$$\ln \frac{P(Y=k \mid \mathbf{x})}{P(Y=j \mid \mathbf{x})} = \ln \frac{P(\mathbf{x} \mid Y=k)P(Y=k)}{P(\mathbf{x} \mid Y=j)P(Y=j)} = \ln P(\mathbf{x} \mid Y=k) - \ln P(\mathbf{x} \mid Y=j) + \ln \frac{P(Y=k)}{P(Y=j)}$$

Substituting the multivariate Gaussian density function into the log-conditional probability yields:

$$\ln P(\mathbf{x} \mid Y=k) = -\frac{D}{2}\ln(2\pi) - \frac{1}{2}\ln|\boldsymbol{\Sigma}| - \frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_k)^T\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}_k)$$

Expanding the quadratic form gives:

$$-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_k)^T\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}_k) = -\frac{1}{2}\mathbf{x}^T\boldsymbol{\Sigma}^{-1}\mathbf{x} + \mathbf{x}^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k - \frac{1}{2}\boldsymbol{\mu}_k^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k$$

When we subtract $\ln P(\mathbf{x} \mid Y=j)$ from $\ln P(\mathbf{x} \mid Y=k)$, the quadratic term $-\frac{1}{2}\mathbf{x}^T\boldsymbol{\Sigma}^{-1}\mathbf{x}$ cancels out completely because $\boldsymbol{\Sigma}$ is shared across both classes. This leaves:

$$\ln \frac{P(Y=k \mid \mathbf{x})}{P(Y=j \mid \mathbf{x})} = \mathbf{x}^T\boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu}_k - \boldsymbol{\mu}_j) - \frac{1}{2}\boldsymbol{\mu}_k^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k + \frac{1}{2}\boldsymbol{\mu}_j^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_j + \ln \frac{P(Y=k)}{P(Y=j)}$$

This equation is strictly linear with respect to $\mathbf{x}$. We can define this linear relation as a decision discriminant $\mathbf{w}^T\mathbf{x} + w_0$, where:

$$\mathbf{w} = \boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu}_k - \boldsymbol{\mu}_j)$$

$$w_0 = -\frac{1}{2}\boldsymbol{\mu}_k^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k + \frac{1}{2}\boldsymbol{\mu}_j^T\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_j + \ln \frac{P(Y=k)}{P(Y=j)}$$

#### Maximum Likelihood Parameter Estimation

Given a training dataset of $N$ points $(\mathbf{x}_n, y_n)$ where $N_k$ is the total count of points belonging to class $k$, the joint likelihood is maximized via closed-form solutions:

- **Class Priors:** $P(Y=k) = \frac{N_k}{N}$
    
- **Class Means:** $\boldsymbol{\mu}_k = \frac{1}{N_k} \sum_{n:y_n=k} \mathbf{x}_n$
    
- **Shared Covariance Matrix ($\boldsymbol{\Sigma}$):**
    
    $$\boldsymbol{\Sigma} = \frac{1}{N} \sum_{k=1}^K \sum_{n:y_n=k} (\mathbf{x}_n - \boldsymbol{\mu}_k)(\mathbf{x}_n - \boldsymbol{\mu}_k)^T$$
    

### D. Logistic Regression

Logistic Regression is a **discriminative** model for continuous inputs. It models the conditional posterior distribution directly via a linear combination of features passed through a non-linear activation function.

#### Binary Classification Formulation

For a binary classification problem ($Y \in \{0, 1\}$), the posterior probability of class 1 is modeled using the **logistic sigmoid function** $\sigma(z) = \frac{1}{1 + e^{-z}}$:

$$P(Y=1 \mid \mathbf{x}, \mathbf{w}) = \sigma(\mathbf{w}^T\mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T\mathbf{x} + b)}}$$

where $\mathbf{w} \in \mathbb{R}^D$ is the weight vector and $b \in \mathbb{R}$ is the bias term.

The log-odds (or logit) transformation reveals the underlying linear architecture of the model:

$$\ln \left( \frac{P(Y=1 \mid \mathbf{x})}{P(Y=0 \mid \mathbf{x})} \right) = \ln \left( \frac{\sigma(\mathbf{w}^T\mathbf{x} + b)}{1 - \sigma(\mathbf{w}^T\mathbf{x} + b)} \right) = \mathbf{w}^T\mathbf{x} + b$$

The decision boundary is defined by the plane where $P(Y=1|\mathbf{x}) = 0.5$, which matches the linear equation $\mathbf{w}^T\mathbf{x} + b = 0$.


#### Extensions: Categorical Features and Multi-Class

- **Categorical Features:** If an input feature is categorical with $h$ distinct states, it is converted into $h$ numerical binary features using **one-hot encoding**.
    
- **Multi-Class Classification:** For $K > 2$ classes, the model selects a reference class (e.g., class $K$) and sets up $K-1$ linear log-odds equations:
    
    $$\ln \left( \frac{P(Y=k \mid \mathbf{x})}{P(Y=K \mid \mathbf{x})} \right) = \mathbf{w}_k^T\mathbf{x} + b_k \quad \forall k = 1, \dots, K-1$$
    

This scales up to the **Softmax function**, which generalizes the conditional posterior distribution for any class $k$:

$$P(Y=k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T\mathbf{x} + b_k}}{\sum_{j=1}^K e^{\mathbf{w}_j^T\mathbf{x} + b_j}}$$

#### Maximum Conditional Likelihood Estimation

Unlike generative models, Logistic Regression parameters are optimized by maximizing the **conditional likelihood** function. Assuming binary targets $y_n \in \{0, 1\}$, the conditional likelihood is:

$$P(\mathbf{y} \mid \mathbf{w}, b) = \prod_{n=1}^N P(Y=1 \mid \mathbf{x}_n)^{y_n} \left(1 - P(Y=1 \mid \mathbf{x}_n)\right)^{1-y_n}$$

Taking the negative log of the conditional likelihood yields the **Cross-Entropy Error Function**:

$$E(\mathbf{w}, b) = -\ln P(\mathbf{y} \mid \mathbf{w}, b) = -\sum_{n=1}^N \left[ y_n \ln \sigma(\mathbf{w}^T\mathbf{x}_n + b) + (1 - y_n) \ln \left(1 - \sigma(\mathbf{w}^T\mathbf{x}_n + b)\right) \right]$$

To compute the gradient of the error function with respect to the weight vector $\mathbf{w}$, we apply the chain rule using the property of the sigmoid derivative $\frac{\partial \sigma(z)}{\partial z} = \sigma(z)(1 - \sigma(z))$:

$$\nabla_\mathbf{w} E(\mathbf{w}, b) = \sum_{n=1}^N \left( \sigma(\mathbf{w}^T\mathbf{x}_n + b) - y_n \right) \mathbf{x}_n$$

> [!brainstorm]
> 
> Notice that the gradient $\sum_{n=1}^N (\sigma_n - y_n)\mathbf{x}_n$ has the exact same mathematical form as the gradient derived for Least Squares linear regression. However, unlike Least Squares, setting this gradient to zero does not yield a closed-form solution. The presence of the non-linear sigmoid activation function $\sigma(\mathbf{w}^T\mathbf{x}_n + b)$ makes the optimization non-linear, requiring iterative numerical approximation methods (e.g., Newton-Raphson, Iterative Reweighted Least Squares (IRLS), or L-BFGS).

### E. Comprehensive Model Comparison Matrix

|**Property**|**Least Squares for Classification**|**Perceptron**|**Linear Discriminant Analysis (LDA)**|**Logistic Regression**|
|---|---|---|---|---|
|**Optimization Criterion**|Minimize Mean Squared Error against one-hot targets|Minimize distance of misclassified instances to hyperplane|Maximize Joint Maximum Likelihood: $P(\mathbf{X}, Y)$|Maximize Conditional Maximum Likelihood: $P(Y \mid \mathbf{X})$|
|**Probabilistic Nature**|Non-probabilistic|Non-probabilistic|Probabilistic (Generative Paradigm)|Probabilistic (Discriminative Paradigm)|
|**Native Multi-Class Handling**|**Yes**: Direct multi-output regression matrix|**No**: Requires meta-strategies (One-vs-Rest)|**Yes**: Native via multi-class Gaussian parameters|**Yes**: Via multinomial Softmax extension|
|**Computational Nature**|**One-step**: Exact closed-form matrix inversion|**Iterative**: Online stochastic updates|**One-step**: Exact closed-form empirical statistics|**Iterative**: Numerical optimization (e.g., L-BFGS)|
|**Behavior on Linearly Separable Data**|Can fail to separate due to outlier sensitivity and masking|Guaranteed to converge to a valid boundary|Separates effectively if class densities are balanced|Converges asymptotically; weights diverge to infinity without regularization|
|**Outlier Robustness**|Highly sensitive|Moderately sensitive|Robust (averages out via mean vectors)|High (bounded log-likelihood penalties)|

### F. Support Vector Machines (SVM) & Maximum Margin Hyperplanes

When data is linearly separable, there are infinitely many separating hyperplanes. Support Vector Machines resolve this ambiguity by selecting the unique hyperplane that maximizes the **margin**—the minimum geometric distance from the hyperplane to any training instance.


Using target labels $y_n \in \{-1, +1\}$, the separating hyperplane equation is $y(\mathbf{x}) = \mathbf{w}^T\mathbf{x} + b = 0$. The perpendicular geometric distance of any data point $\mathbf{x}_n$ to this hyperplane is given by:

$$\gamma_n = \frac{y_n(\mathbf{w}^T\mathbf{x}_n + b)}{\|\mathbf{w}\|}$$

The optimization objective seeks to maximize this minimum distance:

$$\max_{\mathbf{w}, b} \left\{ \frac{1}{\|\mathbf{w}\|} \min_{n} \left[ y_n (\mathbf{w}^T\mathbf{x}_n + b) \right] \right\}$$

Because scaling the parameters ($\mathbf{w} \to \kappa\mathbf{w}$, $b \to \kappa b$) does not change the geometric distance or the decision boundary, we can fix the scale such that the closest points to the hyperplane satisfy:

$$y_n(\mathbf{w}^T\mathbf{x}_n + b) = 1$$

Consequently, for all training instances, the constraint becomes $y_n(\mathbf{w}^T\mathbf{x}_n + b) \geq 1$. Maximizing the margin $\frac{1}{\|\mathbf{w}\|}$ is equivalent to minimizing the inverse quadratic term $\frac{1}{2}\|\mathbf{w}\|^2$. This yields the **Primal Constrained Optimization Problem**:

$$\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 \quad \text{subject to } y_n(\mathbf{w}^T\mathbf{x}_n + b) - 1 \geq 0, \quad \forall n = 1, \dots, N$$

To solve this constrained problem, we construct a **Lagrangian Function** introducing non-negative Lagrange multipliers $\lambda_n \geq 0$:

$$L(\mathbf{w}, b, \boldsymbol{\lambda}) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{n=1}^N \lambda_n \left\{ y_n(\mathbf{w}^T\mathbf{x}_n + b) - 1 \right\}$$

To find the optimum, we set the derivatives of $L(\mathbf{w}, b, \boldsymbol{\lambda})$ with respect to the primal variables $\mathbf{w}$ and $b$ to zero:

$$\frac{\partial L}{\partial \mathbf{w}} = 0 \implies \mathbf{w} = \sum_{n=1}^N \lambda_n y_n \mathbf{x}_n$$

$$\frac{\partial L}{\partial b} = 0 \implies \sum_{n=1}^N \lambda_n y_n = 0$$

Substituting these relations back into the primal Lagrangian eliminates $\mathbf{w}$ and $b$, producing the **Wolfe Dual Optimization Problem**:

$$\max_{\boldsymbol{\lambda}} \left\{ \sum_{n=1}^N \lambda_n - \frac{1}{2}\sum_{n=1}^N\sum_{m=1}^N \lambda_n \lambda_m y_n y_m (\mathbf{x}_n^T\mathbf{x}_m) \right\}$$

$$\text{subject to } \lambda_n \geq 0 \; \forall n, \quad \text{and } \sum_{n=1}^N \lambda_n y_n = 0$$

The optimization must satisfy the **Karush-Kuhn-Tucker (KKT)** conditions, which include the complementary slackness requirement:

$$\lambda_n \left\{ y_n(\mathbf{w}^T\mathbf{x}_n + b) - 1 \right\} = 0$$

This condition implies that for every data point $\mathbf{x}_n$:

- Either $\lambda_n = 0$, meaning the point lies strictly outside the margin and does not influence the orientation of the hyperplane.
    
- Or $\lambda_n > 0$, which forces $y_n(\mathbf{w}^T\mathbf{x}_n + b) = 1$. These points lie exactly on the margin boundary and are the **Support Vectors**.
    

The weight vector is determined entirely by this sparse subset of support vectors:

$$\mathbf{w} = \sum_{n \in \text{SV}} \lambda_n y_n \mathbf{x}_n$$

This allows the final predictive discriminant function for a new test instance $\mathbf{z}$ to be evaluated using only inner products:

$$y(\mathbf{z}) = \mathbf{w}^T\mathbf{z} + b = \sum_{n \in \text{SV}} \lambda_n y_n (\mathbf{x}_n^T\mathbf{z}) + b$$

### G. Non-linear Feature Space Projective Transformations

If a dataset cannot be separated by a linear boundary in its native input space $\mathbb{R}^D$, it can be mapped into a higher-dimensional feature space $\mathbb{R}^{D'}$ via a non-linear vector transformation $\boldsymbol{\phi}(\mathbf{x})$:

$$\boldsymbol{\phi}(\mathbf{x}) = \left[ \phi_1(\mathbf{x}), \phi_2(\mathbf{x}), \dots, \phi_{D'}(\mathbf{x}) \right]^T$$



Applying a linear classifier to the transformed features changes the predictive model to:

$$y(\mathbf{x}) = \mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}) + b$$

The linear decision boundary $\mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}) + b = 0$ in the higher-dimensional feature space $\mathbb{R}^{D'}$ maps back to a non-linear decision boundary in the original input space $\mathbb{R}^D$.

## 3. Practical Implementation & Self-Study Bridge

### A. The Role of Feature Scaling

In the companion Jupyter self-study (`MLSelfStudy2-F26.ipynb`), data normalization is executed using `StandardScaler()` prior to training:

Python

```python
scaler = StandardScaler()
features_train_norm = scaler.fit_transform(features_train)
features_test_norm = scaler.transform(features_test)
```

This normalization transforms features to have a mean of 0 and variance of 1 ($\mathbf{x}_{\text{norm}} = \frac{\mathbf{x} - \boldsymbol{\mu}}{\boldsymbol{\sigma}}$). This step affects our linear classifiers in different ways:

- **Logistic Regression:** Normalization balances the gradient updates across all feature dimensions, preventing numerical instability and accelerating gradient descent convergence.
    
- **Support Vector Machines (Linear SVC):** SVMs maximize the geometric margin based on the L2 norm $\|\mathbf{w}\|^2$. If features are on completely different scales, the unscaled dimensions will dominate the distance metric, distorting the margin maximization.
    
- **Linear Discriminant Analysis (LDA):** Because LDA calculates full empirical covariance matrices, it inherently accounts for differing feature variances and scales. However, pre-scaling can improve numerical stability during matrix factorization.
    

### B. Mapping Scikit-Learn Classifiers to Core Theory

The self-study instantiates three specific models to evaluate decision regions:

Python

```python
models = [
    ("LDA", LinearDiscriminantAnalysis()),
    ("Logistic Regression", LogisticRegression(solver='lbfgs')),
    ("Linear SVC", SVC(kernel="linear"))
]
```

#### 1. LinearDiscriminantAnalysis()

This model solves the maximum joint likelihood problem using empirical means and a shared covariance matrix.

By default, scikit-learn uses the Singular Value Decomposition (`solver='svd'`). This approach factorizes the feature matrix directly without explicitly computing and inverting the shared covariance matrix $\boldsymbol{\Sigma}$, which improves numerical stability and performance on high-dimensional data.

The class-specific mean vectors $\boldsymbol{\mu}_k$ derived by the model are stored in and accessed via the `means_` attribute:

Python

```python
print(model.means_)
```

#### 2. LogisticRegression(solver='lbfgs')

This model directly optimizes the cross-entropy loss function using conditional maximum likelihood.

The `lbfgs` solver (Limited-memory Broyden–Fletcher–Goldfarb–Shanno) is a quasi-Newton optimization method. It approximates the inverse Hessian matrix of second-order partial derivatives, allowing it to make more accurate optimization steps than standard Stochastic Gradient Descent (SGD) without the high memory cost of storing the full Hessian matrix.

The optimized parameter vector $\mathbf{w}$ is accessed via the `coef_` attribute:

Python

```python
print(model.coef_)
```

#### 3. SVC(kernel="linear")

This model maps to the Wolfe Dual optimization problem, maximizing the geometric margin under structural constraints.

The optimized weight vector `coef_` represents the explicit linear combination of the support vectors weighted by their optimal Lagrange multipliers:

$$\mathbf{w} = \sum_{n \in \text{SV}} \lambda_n y_n \mathbf{x}_n$$

Python

```python
print(model.coef_)
```

### C. Parameter & Configuration Analysis

Python

```python
# Extracting and comparing internal parameters from the self-study models
for name, model in models:
    model.fit(features_train_norm, labels_train)
    if name == "LDA":
        # Global shared covariance isn't directly exposed as a simple attribute 
        # unless store_covariance=True, but means_ are available:
        print(f"LDA Learned Class Means:\n{model.means_}")
    elif name == "Logistic Regression":
        print(f"LogReg Learned Weights (w):\n{model.coef_}")
        print(f"LogReg Learned Intercept (b): {model.intercept_}")
    elif name == "Linear SVC":
        print(f"Linear SVC Optimal Margin Weights (w):\n{model.coef_}")
        print(f"Linear SVC Intercept (b): {model.intercept_}")
```

#### Internal Parameter Interpretation

- **LDA Means:** Represent the center of gravity of the multivariate Gaussian distribution for each class. The decision boundary is placed exactly halfway between these learned means, adjusted by the class priors and the pooled covariance structure.
    
- **Logistic Regression Weights:** The coefficients reflect the change in the log-odds of the target class per unit change of that feature. A positive weight increases the posterior probability of the target class exponentially with the feature value.
    
- **Linear SVC Weights:** These weights define the orientation of the maximum margin hyperplane. They are determined exclusively by the support vectors on the margin boundary. Changing the position of any data point outside the margin will leave these weights completely unchanged.
    

## 4. Critical Insights & Conceptual Connections

### A. Core Failure Modes: When LDA Fails Completely

In `exercises.ipynb` (Exercise 1), we look at an example where a 2D dataset is perfectly linearly separable, yet Linear Discriminant Analysis (LDA) fails completely, achieving 50% accuracy.


#### The Mechanism of Failure

LDA models classes as multivariate Gaussians sharing an identical covariance matrix $\boldsymbol{\Sigma}$. If the dataset consists of classes that are highly elongated and tilted parallel to the separating line, the calculated shared covariance matrix pools this strong directional variance.

As a result, LDA assumes that each class spreads out heavily along this tilted axis. To maximize joint likelihood under this pooled covariance model, LDA rotates its decision boundary to run parallel to the direction of maximum variance, cutting directly through both clusters rather than separating them.

#### The Contrast with SVM

A Support Vector Machine (SVM) avoids this pitfall. It does not model global data distributions or assume Gaussian shapes. Instead, it relies on boundary points to maximize the margin. This allows the SVM to find the correct separating hyperplane, demonstrating its robustness against global variance distortions.

### B. Resolving Non-Linearity via Projection: The XOR Case

In `exercises.ipynb` (Exercise 4), we analyze the non-linear XOR function, which cannot be separated by a straight line in its original 2D space.

|**Input A**|**Input B**|**Target Class (Y)**|
|---|---|---|
|1|1|0 ($\ominus$)|
|1|0|1 ($\oplus$)|
|0|1|1 ($\oplus$)|
|0|0|0 ($\ominus$)|

To resolve this, we define a non-linear mapping function $\boldsymbol{\phi}: \mathbb{R}^2 \to \mathbb{R}^3$:

$$\boldsymbol{\phi}(A, B) = [A, B, A \cdot B]^T$$

This function projects our four input coordinates into a 3D space:

- $\boldsymbol{\phi}(1, 1) = [1, 1, 1]^T \implies \text{Class } 0$
    
- $\boldsymbol{\phi}(1, 0) = [1, 0, 0]^T \implies \text{Class } 1$
    
- $\boldsymbol{\phi}(0, 1) = [0, 1, 0]^T \implies \text{Class } 1$
    
- $\boldsymbol{\phi}(0, 0) = [0, 0, 0]^T \implies \text{Class } 0$
    

In this new 3D feature space, we can achieve perfect linear separation using a hyperplane defined by weights $\mathbf{w} = [1, 1, -2]^T$ and bias $b = -0.5$:

$$\mathbf{w}^T\boldsymbol{\phi}(A, B) + b = A + B - 2(A \cdot B) - 0.5$$

Evaluating this equation for each projected point confirms perfect separation:

- **Point (1,1):** $1 + 1 - 2(1) - 0.5 = -0.5 < 0 \implies \text{Class } 0$
    
- **Point (1,0):** $1 + 0 - 2(0) - 0.5 = +0.5 > 0 \implies \text{Class } 1$
    
- **Point (0,1):** $0 + 1 - 2(0) - 0.5 = +0.5 > 0 \implies \text{Class } 1$
    
- **Point (0,0):** $0 + 0 - 2(0) - 0.5 = -0.5 < 0 \implies \text{Class } 0$
    

This mapping transforms a non-linear problem into a simple linear one by expanding the feature space, illustrating the core principle behind non-linear classifiers.

# Lecture 3: Kernel Support Vector Machines

## 1. Executive Summary & Core Objectives

This lecture concludes the foundational analysis of **Support Vector Machines (SVMs)** by introducing non-linear feature space extensions via the **Kernel Trick**. It bridges the gap between linear hyperplanes and highly complex, non-linear real-world data boundaries.

The core objectives of this session are:

- **Formulate the Optimization Foundations:** Review the primal and dual Lagrangian formulations of maximum-margin hyperplanes to show that the dual optimization depends exclusively on data inner products ($\mathbf{x}_i \cdot \mathbf{x}_j$).
    
- **Deconstruct the Kernel Trick:** Understand how valid kernel functions $K(\mathbf{x}, \mathbf{x}')$ implicitly evaluate dot products in a high-dimensional feature space $\mathbb{R}^{D'}$ without requiring the explicit, computationally expensive construction of transformation vectors $\boldsymbol{\phi}(\mathbf{x})$.
    
- **Establish Mathematical Rigor for Kernels:** Analyze the criteria for valid similarity metrics via **Mercer’s Theorem** and **Gram Matrix Positive Semi-Definiteness**.
    
- **Apply Support Vector Learning to Structured Data:** Extend SVM classification to non-numeric spaces—specifically text data (via **Cosine Similarity**) and sequence data (via **$p$-Spectrum** and **All-Subsequences String Kernels**).
    
- **Analyze the Soft Margin Formulation:** Introduce slack variables ($\xi_n$) to relax constraints on non-linearly separable or noisy datasets.
    

## 2. Theoretical Foundations & Mathematical Models

### A. The Primal-to-Dual Path and Dot Product Dependence

The predictive decision function for a linear maximum-margin classifier is given by $f(\mathbf{x}) = \mathbf{w}^T\mathbf{x} + b$. In Lecture 2, this was optimized by constructing the primal Lagrangian:

$$L(\mathbf{w}, b, \boldsymbol{\lambda}) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{n=1}^N \lambda_n \left\{ y_n(\mathbf{w}^T\mathbf{x}_n + b) - 1 \right\}$$

Minimizing with respect to the primal parameters ($\mathbf{w}, b$) requires setting their partial derivatives to zero:

$$\frac{\partial L}{\partial \mathbf{w}} = \mathbf{w} - \sum_{n=1}^N \lambda_n y_n \mathbf{x}_n = 0 \implies \mathbf{w} = \sum_{n=1}^N \lambda_n y_n \mathbf{x}_n$$

$$\frac{\partial L}{\partial b} = -\sum_{n=1}^N \lambda_n y_n = 0 \implies \sum_{n=1}^N \lambda_n y_n = 0$$

Substituting these back into the primal function yields the **Wolfe Dual Problem**:

$$\max_{\boldsymbol{\lambda}} \left\{ \sum_{n=1}^N \lambda_n - \frac{1}{2}\sum_{n=1}^N\sum_{m=1}^N \lambda_n \lambda_m y_n y_m (\mathbf{x}_n \cdot \mathbf{x}_m) \right\}$$

$$\text{subject to } \lambda_n \geq 0 \quad \forall n \in \{1, \dots, N\}, \quad \text{and } \sum_{n=1}^N \lambda_n y_n = 0$$

> [!note] The dual optimization task contains no explicit reference to the weight vector $\mathbf{w}$. The data points $\mathbf{x}_n$ and $\mathbf{x}_m$ appear exclusively within an inner product (dot product) operation $(\mathbf{x}_n \cdot \mathbf{x}_m)$. Consequently, evaluating any test sample $\mathbf{z}$ at inference time relies solely on computing dot products against the sparse set of identified Support Vectors (SVs):
> 
> $$f(\mathbf{z}) = \left( \sum_{n \in \text{SV}} \lambda_n y_n \mathbf{x}_n \right)^T \mathbf{z} + b = \sum_{n \in \text{SV}} \lambda_n y_n (\mathbf{x}_n \cdot \mathbf{z}) + b$$

### B. The Kernel Trick and Feature Space Transformations

If data is non-linearly separable in its original input space $\mathbb{R}^D$, we can map it into a higher-dimensional feature space $\mathbb{R}^{D'}$ via a non-linear vector transformation $\boldsymbol{\phi}(\mathbf{x})$:

$$\boldsymbol{\phi}(\mathbf{x}) = \left[ \phi_1(\mathbf{x}), \phi_2(\mathbf{x}), \dots, \phi_{D'}(\mathbf{x}) \right]^T$$

Applying support vector learning in this high-dimensional space requires replacing every instance of the original input dot product with the transformed inner product $\boldsymbol{\phi}(\mathbf{x}_n) \cdot \boldsymbol{\phi}(\mathbf{x}_m)$. When $D'$ is massive or infinite, explicitly mapping $\boldsymbol{\phi}(\mathbf{x})$ and computing its dot product is computationally prohibitive.½

The **Kernel Trick** bypasses this explicit mapping. It defines a kernel function $K(\mathbf{x}, \mathbf{x}')$ that directly computes the value of the inner product in the target feature space:

$$K(\mathbf{x}, \mathbf{x}') = \boldsymbol{\phi}(\mathbf{x}) \cdot \boldsymbol{\phi}(\mathbf{x}')$$

#### Concrete Polynomial Kernel Transformation Example

Consider a 2D input space $\mathbf{x} = (x_1, x_2)^T$ mapped into a 6D feature space via:

$$\boldsymbol{\phi}(\mathbf{x}) = \left( x_1^2, x_2^2, \sqrt{2}x_1, \sqrt{2}x_2, \sqrt{2}x_1x_2, 1 \right)^T$$

Evaluating the dot product of two transformed vectors $\boldsymbol{\phi}(\mathbf{x})$ and $\boldsymbol{\phi}(\mathbf{x}')$ yields:

$$\boldsymbol{\phi}(\mathbf{x}) \cdot \boldsymbol{\phi}(\mathbf{x}') = x_1^2 {x_1'}^2 + x_2^2 {x_2'}^2 + 2x_1x_1' + 2x_2x_2' + 2x_1x_1'x_2x_2' + 1$$

Factoring this algebraic expression reveals that it is exactly equal to the square of the input space dot product plus one:

$$\boldsymbol{\phi}(\mathbf{x}) \cdot \boldsymbol{\phi}(\mathbf{x}') = \left( x_1 x_1' + x_2 x_2' + 1 \right)^2 = (\mathbf{x} \cdot \mathbf{x}' + 1)^2$$

Thus, we can define the valid kernel function $K(\mathbf{x}, \mathbf{x}') = (\mathbf{x} \cdot \mathbf{x}' + 1)^2$. This allows us to evaluate a 6D inner product using a simple 2D dot product and a scalar power operation, demonstrating the efficiency of the kernel trick.

### C. Mathematical Validation: Mercer's Theorem and the Gram Matrix

To ensure a symmetric function $K(\mathbf{x}, \mathbf{x}')$ implicitly represents a valid inner product in a Hilbert feature space, it must satisfy conditions of positive semi-definiteness.

#### 1. Mercer's Theorem (Continuous Formulation)

A continuous symmetric kernel function $K(\mathbf{x}, \mathbf{x}')$ can be expressed as a dot product $\boldsymbol{\phi}(\mathbf{x}) \cdot \boldsymbol{\phi}(\mathbf{x}')$ if and only if, for any square-integrable function $g(\mathbf{x})$ (such that $\int g(\mathbf{x})^2 d\mathbf{x} < \infty$), the following condition holds:

$$\int \int K(\mathbf{x}, \mathbf{x}') g(\mathbf{x}) g(\mathbf{x}') d\mathbf{x} d\mathbf{x}' \geq 0$$

#### 2. Gram Matrix Formulation (Discrete Version)

In practical machine learning applications, we validate candidate kernels using finite datasets. Given a set of training instances $\{\mathbf{x}_1, \dots, \mathbf{x}_N\}$, we construct an $N \times N$ **Gram Matrix** (or **Kernel Matrix**) $\mathbf{K}$, where each entry is defined as $\mathbf{K}_{ij} = K(\mathbf{x}_i, \mathbf{x}_j)$:

$$\mathbf{K} = \begin{pmatrix} K(\mathbf{x}_1, \mathbf{x}_1) & K(\mathbf{x}_1, \mathbf{x}_2) & \dots & K(\mathbf{x}_1, \mathbf{x}_N) \\ K(\mathbf{x}_2, \mathbf{x}_1) & K(\mathbf{x}_2, \mathbf{x}_2) & \dots & K(\mathbf{x}_2, \mathbf{x}_N) \\ \vdots & \vdots & \ddots & \vdots \\ K(\mathbf{x}_N, \mathbf{x}_1) & K(\mathbf{x}_N, \mathbf{x}_2) & \dots & K(\mathbf{x}_N, \mathbf{x}_N) \end{pmatrix}$$

A symmetric function $K(\mathbf{x}, \mathbf{x}')$ is a valid kernel if and only if its Gram matrix $\mathbf{K}$ is **Positive Semi-Definite (PSD)** for all possible finite sets of points. A matrix is verified as PSD if it satisfies either of these equivalent conditions:

- **Quadratic Form:** For any non-zero coefficient vector $\mathbf{v} \in \mathbb{R}^N$:
    
    $$\mathbf{v}^T \mathbf{K} \mathbf{v} = \sum_{i=1}^N \sum_{j=1}^N v_i v_j \mathbf{K}_{ij} \geq 0$$
    
- **Eigenvalue Spectrum:** All eigenvalues $\lambda$ of the matrix $\mathbf{K}$ are non-negative ($\lambda_i \geq 0 \quad \forall i$).
    

#### 3. Kernel Composition Algebra

We can construct complex, domain-specific valid kernels from simpler ones using algebraic composition rules. If $K_1(\mathbf{x}, \mathbf{x}')$ and $K_2(\mathbf{x}, \mathbf{x}')$ are valid positive semi-definite kernels, then the following functions are also valid kernels:

- **Scalar Multiplication & Constant Addition:** $q(K_1(\mathbf{x}, \mathbf{x}'))$, where $q(\cdot)$ is a polynomial function with non-negative coefficients.
    
- **Exponential Mapping:** $\exp(K_1(\mathbf{x}, \mathbf{x}'))$.
    
- **Tensor/Hadamard Product:** $K_1(\mathbf{x}, \mathbf{x}') K_2(\mathbf{x}, \mathbf{x}')$.
    
- **Normalization Transformation:** This normalizes the feature space vectors to unit length:
    
    $$K_{\text{norm}}(\mathbf{x}, \mathbf{x}') = \frac{K_1(\mathbf{x}, \mathbf{x}')}{\sqrt{K_1(\mathbf{x}, \mathbf{x}) K_1(\mathbf{x}', \mathbf{x}')}}$$
    

### D. The Soft Margin Formulation: Slack Variable Relaxation

Real-world datasets are rarely perfectly linearly separable, even after high-dimensional kernel projections. To handle noisy data and overlapping distributions, we introduce non-negative **Slack Variables** $\xi_n \geq 0$ to relax the strict margin constraints.


The relaxed constraints allow training instances to violate the margin boundaries:

$$y_n (\mathbf{w} \cdot \mathbf{x}_n + b) \geq 1 - \xi_n \quad \forall n \in \{1, \dots, N\}$$

The value of $\xi_n$ determines the position of the data point $\mathbf{x}_n$ relative to the margin:

- $\xi_n = 0$: The instance is correctly classified and lies outside or exactly on the margin boundary.
    
- $0 < \xi_n \leq 1$: The instance is correctly classified but lies within the margin safety zone.
    
- $\xi_n > 1$: The instance crosses the decision boundary and is misclassified.
    

To balance margin maximization with classification errors, we introduce the regularization hyperparameter $C$, yielding the **Relaxed Primal Objective Function**:

$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \left( \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{n=1}^N \xi_n \right) \quad \text{subject to } y_n(\mathbf{w} \cdot \mathbf{x}_n + b) \geq 1 - \xi_n \text{ and } \xi_n \geq 0$$

### E. Advanced Kernels for Non-Standard Structurally Complex Spaces

Because kernels measure similarity between abstract entities without requiring explicit coordinate vectors, we can apply SVMs to non-numeric data types like text, strings, and graphs.

#### 1. Text Spaces: Bag-of-Words and Cosine Similarity Kernels

A text document $t$ can be converted into a sparse numerical vector $\mathbf{tf}(t)$ over a fixed vocabulary of size $V$. Each element $\mathbf{tf}(t)[i]$ stores the count of occurrences of word $i$ in document $t$.

The similarity between two documents is measured using the **Cosine Similarity Kernel**:

$$K_{\text{cos}}(t_1, t_2) = \cos(\theta) = \frac{\mathbf{tf}(t_1) \cdot \mathbf{tf}(t_2)}{\|\mathbf{tf}(t_1)\| \|\mathbf{tf}(t_2)\|} = \frac{\mathbf{tf}(t_1) \cdot \mathbf{tf}(t_2)}{\sqrt{(\mathbf{tf}(t_1) \cdot \mathbf{tf}(t_1))(\mathbf{tf}(t_2) \cdot \mathbf{tf}(t_2))}}$$

This function satisfies Mercer's conditions because it is a normalization of the standard dot product kernel applied to the term-frequency representation.

#### 2. Sequence Spaces: Substring vs. Subsequence Character Mappings

Let $\mathbf{s}$ and $\mathbf{t}$ be sequence strings over a discrete alphabet set $\Sigma$. We define two distinct character matching strategies:

- **Substring Mapping ($\phi_u(\mathbf{s})$):** Counts the exact, contiguous occurrences of string pattern $u$ within string $\mathbf{s}$.
    
- **Subsequence Mapping ($\phi_u^+(\mathbf{s})$):** Counts the non-contiguous occurrences of string pattern $u$ within string $\mathbf{s}$, preserving character order but allowing arbitrary gaps.
    

##### Structural String Pattern Matching Example

Let the sequence string be $\mathbf{s} = \text{"statistics"}$. We evaluate the matching counts for target substrings and subsequences:

|**Target Pattern (u)**|**Substring Feature Vector ϕu​(s)**|**Subsequence Feature Vector ϕu+​(s)**|
|---|---|---|
|$u = \text{"ti"}$|**2** (sta**ti**s**ti**cs)|**5**|
|$u = \text{"tis"}$|**1** (sta**tis**tics)|**7**|
|$u = \text{"atics"}$|**0** (Not present contiguously)|**3**|

#### 3. The $p$-Spectrum Kernel

The **$p$-Spectrum Kernel** measures string similarity by counting shared contiguous substrings of a fixed length $p$. The feature transformation vector is indexed across all possible character combinations in $\Sigma^p$:

$$K_p(\mathbf{s}, \mathbf{t}) = \sum_{u \in \Sigma^p} \phi_u(\mathbf{s}) \phi_u(\mathbf{t})$$

#### 4. The All-Subsequences Kernel and Dynamic Programming Recursion

The **All-Subsequences Kernel** extends similarity evaluation by summing matching counts across all possible subsequences of any length:

$$K_{\text{all}}(\mathbf{s}, \mathbf{t}) = \sum_{u \in \Sigma^*} \phi_u^+(\mathbf{s}) \phi_u^+(\mathbf{t})$$

Because the length of $u$ is unrestricted, the explicit feature space is infinite, making direct summation impossible. We resolve this by using a **Dynamic Programming** framework that computes the kernel score recursively in $O(|\mathbf{s}| \cdot |\mathbf{t}|)$ time.

Let $\mathbf{s} = s_1 s_2 \dots s_n$ and $\mathbf{t} = t_1 t_2 \dots t_m$. The base case for an empty sequence string $\epsilon$ is defined as:

$$K(\epsilon, \mathbf{t}) = 1 \quad \forall \mathbf{t}$$

The general recursive step evaluates sequence prefixes by splitting the subsequence count into two parts: matches that exclude the trailing character $s_i$, and matches that include it:

$$K(\mathbf{s}[1:i], \mathbf{t}[1:j]) = K(\mathbf{s}[1:i-1], \mathbf{t}[1:j]) + \sum_{k \leq j : t_k = s_i} K(\mathbf{s}[1:i-1], \mathbf{t}[1:k-1])$$

## 3. Practical Implementation & Self-Study Bridge

### A. The Practical Importance of Input Data Normalization

In the practical self-study (`MLSelfStudy3-F26.ipynb`), input pixel intensities from the MNIST dataset are scaled before training the SVM classifiers:

Python

```python
# MinMax Scaling to a bounded interval
mnist_scaled = mnist.data / 255.0

# Z-score Normalization to zero mean and unit variance
mnist_scaled = (mnist_scaled - mnist_scaled.mean()) / mnist_scaled.std()
```

Normalization is essential for non-linear kernels like the **Radial Basis Function (RBF)** ($K(\mathbf{x}, \mathbf{x}') = \exp(-\gamma \|\mathbf{x}-\mathbf{x}'\|^2)$). The RBF kernel measures similarity using the squared Euclidean distance between instances. If feature scales are unbalanced, dimensions with larger magnitudes will dominate the distance metric, rendering the kernel insensitive to variations in other features.

### B. Mapping Code Implementations to Dual Optimization Theory

The self-study configures non-linear SVM models using scikit-learn's `SVC` class:

Python

```python
from sklearn.svm import SVC

# Configuring a Non-Linear Polynomial Kernel Support Vector Classifier
model = SVC(kernel="poly", degree=3, C=10)
model.fit(X_train_2d, y_train)
```

#### Code-to-Theory Mapping

```python
     Scikit-Learn Class Call                  Underlying Optimization Model
  ==============================             ==================================
   SVC(kernel="poly", degree=3)  --------->   K(x, x') = (x \cdot x' + 1)^3
                                              Evaluates 3rd degree polynomial dual inner product
  ------------------------------             ----------------------------------
   C=10 Regularization Parameter --------->  Sets upper bound constraint on multipliers:
                                              0 <= \lambda_n <= C
```

When fitting the model, scikit-learn uses the LIBSVM library to solve the Wolfe Dual quadratic programming problem. The regularization parameter `C` acts as an upper bound on the Lagrange multipliers, enforcing the constraint $0 \leq \lambda_n \leq C$.

Instances that satisfy the margin constraints have $\lambda_n = 0$. Points that lie exactly on the margin boundaries become support vectors with $0 < \lambda_n < C$. Points that violate the margin have their multipliers bounded at the maximum value, $\lambda_n = C$.

### C. The Degenerate Boundary Case: Setting $C=0$

In `exercise3 solutions.pdf` (Exercise 1), we evaluate a structural boundary case: what happens to the optimal separating hyperplane if we set the hyperparameter $C=0$?

Setting $C=0$ removes the penalty for classification errors and margin violations from the objective function, reducing the optimization task to:

$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 \quad \text{subject to } y_n(\mathbf{w} \cdot \mathbf{x}_n + b) \geq 1 - \xi_n$$

The objective function $\frac{1}{2}\|\mathbf{w}\|^2$ is minimized by setting the weight vector to zero ($\mathbf{w} = \mathbf{0}$). Substituting $\mathbf{w} = \mathbf{0}$ simplifies the constraints to:

$$y_n \cdot b \geq 1 - \xi_n$$

Because there is no penalty for margin violations, the slack variables $\xi_n$ can grow arbitrarily large to satisfy the constraints for any choice of $b$. For example, if we set $b=1$, the constraints are satisfied by choosing $\xi_n = 0$ for positive instances ($y_n = +1$) and $\xi_n = 2$ for negative instances ($y_n = -1$).

Since $\mathbf{w} = \mathbf{0}$, the discriminant function simplifies to a constant value for all inputs:

$$f(\mathbf{x}) = \mathbf{0} \cdot \mathbf{x} + b = b = 1$$

As a result, the model assigns the exact same class label to every data point regardless of its features, rendering the classifier useless. This demonstrates that $C$ must be strictly greater than zero ($C > 0$) for the optimization to produce a meaningful decision boundary.

## 4. Critical Insights & Conceptual Connections

### A. Non-Linear Separation Framework: Linear PCA Projections vs. Polynomial Kernels

In the self-study experiments, the high-dimensional MNIST dataset is processed using two different approaches to handle complex class boundaries:

Python

```python
from cuml.decomposition import PCA
from cuml.svm import SVC

# 1. Linear Dimensionality Reduction Projection Subspace
pca = PCA(n_components=2)
X_train_2d = pca.fit_transform(X_train)

# 2. Non-Linear Feature Space Projection via Dual Kernels
model = SVC(kernel="poly", degree=3, C=10)
model.fit(X_train_2d, y_train)
```

This pipeline highlights the different mechanisms used by linear projections and kernel functions:

- **Principal Component Analysis (PCA):** Performs a _linear projection_ that maps the original 784-dimensional pixel space down to a 2D plane. It chooses projection axes that maximize global variance, without considering class labels. If the classes are non-linearly distributed or interleaved, a linear projection can squash them together, causing significant overlap and making separation impossible.
    
- **Polynomial Kernel SVM:** Takes the 2D coordinates produced by PCA and applies a _non-linear transformation_ using a 3rd-degree polynomial kernel:
    
    $$K(\mathbf{x}, \mathbf{x}') = (\mathbf{x} \cdot \mathbf{x}' + 1)^3$$
    

This implicitly maps the data into a higher-dimensional feature space where the classes become linearly separable. The SVM then finds the optimal maximum-margin hyperplane in this extended space. When projected back down to the 2D PCA plane, this flat hyperplane forms a highly flexible, curved polynomial decision boundary that can wrap around complex class distributions.

### B. Computational Complexity and Multiclass Scalability Trade-offs

While Kernel SVMs offer powerful non-linear classification capabilities, they introduce specific computational trade-offs that must be managed:

#### 1. Dataset Size Scalability

Training a kernel SVM requires computing and storing the $N \times N$ Gram Matrix $\mathbf{K}$. This step has a computational complexity that scales quadratically with the number of training instances ($O(N^2)$). As a result, while SVMs are highly effective for small to medium-sized datasets with complex features, they become computationally expensive and memory-intensive when scaled to large datasets with millions of rows.

#### 2. Multiclass Extension Strategies

The maximum-margin objective is fundamentally designed for binary classification ($y_n \in \{-1, +1\}$). To handle multiclass problems like the 10-digit MNIST dataset, we must combine multiple binary classifiers using meta-strategies:

- **One-vs-Rest (OvR):** Trains $K$ independent binary classifiers, where each model learns to separate one specific class from all other classes combined.
    
- **One-vs-One (OvO):** Trains $\frac{K(K-1)}{2}$ distinct binary classifiers covering every possible pair of classes. For a 10-class problem, this requires training 45 separate models. At inference time, each classifier casts a vote, and the class with the most votes is selected as the final prediction.
    

While OvO requires training more models, each individual classifier is trained on a small subset of the data containing only two classes. Because training complexity scales quadratically with dataset size ($O(N^2)$), training many smaller models on pairs of classes is often faster than training fewer large models using the OvR strategy.
# Lecture 4: Neural Networks and Deep Learning

## 1. Executive Summary & Core Objectives

This lecture shifts the foundational framework from linear boundaries to non-linear universal function approximators through the multi-layered composition of parameters and activation functions. It bridges the gap between raw gradient calculation and highly efficient backward algorithmic scheduling via computational graphs.

The core objectives are:

- **Formulate Multilayer Perceptrons (MLPs):** Define neural network layers as chains of nested function compositions, explaining how non-linear operators prevent multi-layered networks from collapsing into basic single-layer linear systems.
    
- **Deconstruct Backpropagation:** Track exact partial derivatives step-by-step using scalar and vector versions of the generalized chain rule on top of explicit computational graphs.
    
- **Diagnose Core Training Failure Modes:** Quantify and analyze optimization blocks, focusing on the **Vanishing Gradient** problem caused by activation derivatives, and the **Exploding Gradient** challenge near landscape cliffs.
    
- **Evaluate Advanced Optimization Mechanics:** Review the sample size properties of **Stochastic Gradient Descent (SGD)**, study how standard error scales with batch choices, and analyze higher-order momentum dynamics.
    

## 2. Theoretical Foundations & Mathematical Models

### A. The Neural Network Architectural Blueprint

A standard feedforward neural network maps an input vector $\mathbf{x} \in \mathbb{R}^D$ to an output vector $\mathbf{y} \in \mathbb{R}^K$ by passing it through a series of structured layers. The fundamental building unit—the neuron—performs a two-step calculation:

1. A linear combination of its input vectors $\mathbf{i}$ scaled by a weight vector $\mathbf{w}$ plus a scalar bias $b$:
    
    $$I = \mathbf{w}^T \mathbf{i} + b = \sum_{j} i_j w_j + b$$
    
2. A non-linear transformation applied to this scalar value via an **activation function** ($af$) to produce the final output:
    
    $$out = af(I)$$
    

```
  Inputs (i_j)       Weights (w_j)         Linear Sum (I)       Activation (af)
     i_1 -------------> w_1 -------------\
     i_2 -------------> w_2 ------------->  Sum(i_j w_j) + b  -->  af(I) --> Output
     i_3 -------------> w_3 -------------/
```

When grouped into consecutive operational blocks, a neural network expresses its global mapping as a composite function:

$$\mathbf{y} = f(\mathbf{x}) = f^{(L)}\left( \mathbf{W}^{(L)T} \dots f^{(1)}\left(\mathbf{W}^{(1)T}\mathbf{x} + \mathbf{b}^{(1)}\right) \dots + \mathbf{b}^{(L)}\right)$$

> [!note]
> 
> If the non-linear activation functions $f^{(l)}$ are omitted, the entire multi-layered network collapses into a single linear layer. Mathematically, a sequence of matrix multiplications can always be compressed into a single matrix product: $\mathbf{W}_{\text{equivalent}} = \mathbf{W}^{(1)} \mathbf{W}^{(2)} \dots \mathbf{W}^{(L)}$. Consequently, non-linear activation functions are essential to allow the network to construct complex, non-linear decision boundaries.

#### Common Non-Linear Activation Functions

- **Logistic Sigmoid:** Projects continuous scalar values into a bounded probability interval:
    
    $$\sigma(z) = \frac{1}{1 + e^{-z}} \in (0, 1)$$
    
    _Derivative Analysis:_ The derivative can be expressed entirely in terms of its output value:
    
    $$\frac{d\sigma(z)}{dz} = \sigma(z)\left(1 - \sigma(z)\right)$$
    
    The maximum value of this derivative is exactly $0.25$ at the inflection point $z = 0$.
    
- **Hyperbolic Tangent ($\tanh$):** A zero-centered activation function that maps outputs across a symmetric range:
    
    $$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} \in (-1, 1)$$
    
    _Derivative Analysis:_
    
    $$\frac{d\tanh(z)}{dz} = 1 - \tanh^2(z)$$
    
    The maximum value of this derivative is $1.0$ at $z = 0$.
    
- **Rectified Linear Unit (ReLU):** A piecewise linear function that yields sparse activation maps and avoids derivative saturation for positive inputs:
    
    $$\text{ReLU}(z) = \max(0, z) = \begin{cases} z & \text{if } z > 0 \\ 0 & \text{if } z \le 0 \end{cases}$$
    
    _Derivative Analysis:_
    
    $$\frac{d\text{ReLU}(z)}{dz} = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \end{cases}$$
    

### B. Loss / Cost Function Formulations

To train the parameters of a network, we define a scalar loss function $\mathcal{L}(\mathbf{t}, \mathbf{o})$ that quantifies the error between target variables $\mathbf{t}$ and model outputs $\mathbf{o}$:

- **Squared Error (L2 Loss):** Typically used for continuous regression tasks:
    
    $$\mathcal{L}(\mathbf{t}, \mathbf{o}) = \sum_{k=1}^m (t_k - o_k)^2$$
    
- **Cross-Entropy Loss (Negative Log-Likelihood):** Used for classification tasks by interpreting output entries as discrete class probabilities:
    
    $$\mathcal{L}(\mathbf{t}, \mathbf{o}) = -\sum_{k=1}^m t_k \ln(o_k)$$
    
    For multi-class setups, this cross-entropy loss is paired with a **Softmax** activation layer to ensure the outputs form a valid probability distribution summing to one.
    

### C. The Calculus of Backpropagation on Computational Graphs

The **Backpropagation Algorithm** uses the chain rule to evaluate the gradient of the loss function with respect to every internal weight and bias in the network.

#### Mathematical Foundation

- **Scalar Chain Rule:** For nested functions $f(g(x))$:
    
    $$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial g(x)} \cdot \frac{\partial g(x)}{\partial x}$$
    
- **Multi-Variable Branching Chain Rule:** If an input node distributes its signal to multiple downstream branches $g_1(x), g_2(x)$, the local gradients from each path are summed together:
    
    $$\frac{\partial f(g_1(x), g_2(x))}{\partial x} = \frac{\partial f}{\partial g_1(x)}\frac{\partial g_1(x)}{\partial x} + \frac{\partial f}{\partial g_2(x)}\frac{\partial g_2(x)}{\partial x}$$
    
- **Vector Chain Rule (Jacobian Framework):** For vectors $\mathbf{x} \in \mathbb{R}^m$ and $\mathbf{y} \in \mathbb{R}^n$ where $\mathbf{y} = g(\mathbf{x})$ and scalar loss $z = f(\mathbf{y})$:
    
    $$\nabla_{\mathbf{x}} z = \left( \frac{\partial \mathbf{y}}{\partial \mathbf{x}} \right)^T \nabla_{\mathbf{y}} z$$
    
    Here, $\frac{\partial \mathbf{y}}{\partial \mathbf{x}} \in \mathbb{R}^{n \times m}$ represents the system's full Jacobian matrix.
    

#### Mathematical Verification of the Computational Graph Slide Example

Let's verify the complete forward and backward propagation steps from the detailed example in the slides.

```
  x_1 (1.0) --( * w_1=2.0 )--> y_1 (2.0) ---\
                                             ( + ) --> y_3 (3.5) --[ Sigmoid ]--> y_4 (0.9707) ---\
  x_2 (3.0) --( * w_2=0.5 )--> y_2 (1.5) ---/                    --[ ReLU    ]--> y_5 (3.5000) ----( * )--> y_6 (3.3975) --> Error
```

##### 1. Forward Pass Specifications

- **Initial Node Constraints:** $x_1 = 1$, $w_1 = 2$, $x_2 = 3$, $w_2 = 0.5$. Target value $o = 1$.
    
- **Linear Nodes:**
    
    $$y_1 = x_1 \cdot w_1 = 1 \cdot 2 = 2$$
    
    $$y_2 = x_2 \cdot w_2 = 3 \cdot 0.5 = 1.5$$
    
    $$y_3 = y_1 + y_2 = 2 + 1.5 = 3.5$$
    
- **Activation Layers:**
    
    $$y_4 = \sigma(y_3) = \frac{1}{1 + e^{-3.5}} \approx 0.970687$$
    
    $$y_5 = \text{ReLU}(y_3) = \max(0, 3.5) = 3.5$$
    
- **Output Node & Error Calculation:**
    
    $$y_6 = y_4 \cdot y_5 = 0.970687 \cdot 3.5 \approx 3.397405$$
    
    $$\text{err} = (o - y_6)^2 = (1 - 3.397405)^2 \approx 5.74755$$
    

##### 2. Backward Pass Gradient Computations

- **Base Case:**
    
    $$\frac{\partial \text{err}}{\partial \text{err}} = 1$$
    
- **Output Layer Derivative:**
    
    $$\frac{\partial \text{err}}{\partial y_6} = -2(o - y_6) = -2(1 - 3.397405) = 4.79481$$
    
- **Branching Layer Derivatives (Product Rule Application):**
    
    $$\frac{\partial \text{err}}{\partial y_4} = \frac{\partial \text{err}}{\partial y_6} \cdot \frac{\partial y_6}{\partial y_4} = \frac{\partial \text{err}}{\partial y_6} \cdot y_5 = 4.79481 \cdot 3.5 \approx 16.7818$$
    
    $$\frac{\partial \text{err}}{\partial y_5} = \frac{\partial \text{err}}{\partial y_6} \cdot \frac{\partial y_6}{\partial y_5} = \frac{\partial \text{err}}{\partial y_6} \cdot y_4 = 4.79481 \cdot 0.970687 \approx 4.6542$$
    
- **Activation Gradients:**
    
    $$\frac{\partial y_4}{\partial y_3} = \sigma(y_3)(1 - \sigma(y_3)) = 0.970687 \cdot (1 - 0.970687) \approx 0.028442$$
    
    $$\frac{\partial y_5}{\partial y_3} = \mathbf{1}_{(y_3 > 0)} = 1$$
    
- **Summation at the $y_3$ Branching Point:**
    
    $$\frac{\partial \text{err}}{\partial y_3} = \frac{\partial \text{err}}{\partial y_4}\frac{\partial y_4}{\partial y_3} + \frac{\partial \text{err}}{\partial y_5}\frac{\partial y_5}{\partial y_3} = (16.7818 \cdot 0.028442) + (4.6542 \cdot 1) \approx 0.47728 + 4.6542 = 5.13148$$
    
    _(Matches the slide calculation of $5.132$)_.
    
- **Summation Layer Splitting:** Since $y_3 = y_1 + y_2$, we have $\frac{\partial y_3}{\partial y_1} = 1$ and $\frac{\partial y_3}{\partial y_2} = 1$. Therefore:
    
    $$\frac{\partial \text{err}}{\partial y_1} = \frac{\partial \text{err}}{\partial y_3} \cdot 1 \approx 5.132$$
    
    $$\frac{\partial \text{err}}{\partial y_2} = \frac{\partial \text{err}}{\partial y_3} \cdot 1 \approx 5.132$$
    
- **Input and Parameter Weight Gradients:**
    
    $$\frac{\partial \text{err}}{\partial x_1} = \frac{\partial \text{err}}{\partial y_1} \cdot \frac{\partial y_1}{\partial x_1} = \frac{\partial \text{err}}{\partial y_1} \cdot w_1 = 5.13148 \cdot 2 \approx 10.263$$
    
    $$\frac{\partial \text{err}}{\partial w_1} = \frac{\partial \text{err}}{\partial y_1} \cdot \frac{\partial y_1}{\partial w_1} = \frac{\partial \text{err}}{\partial y_1} \cdot x_1 = 5.13148 \cdot 1 \approx 5.132$$
    
    $$\frac{\partial \text{err}}{\partial x_2} = \frac{\partial \text{err}}{\partial y_2} \cdot \frac{\partial y_2}{\partial x_2} = \frac{\partial \text{err}}{\partial y_2} \cdot w_2 = 5.13148 \cdot 0.5 \approx 2.566$$
    
    $$\frac{\partial \text{err}}{\partial w_2} = \frac{\partial \text{err}}{\partial y_2} \cdot \frac{\partial y_2}{\partial w_2} = \frac{\partial \text{err}}{\partial y_2} \cdot x_2 = 5.13148 \cdot 3 \approx 15.394$$
    

### D. Advanced Stochastic Gradient Descent & Statistical Variance

In deep learning, computing the true gradient over an entire dataset of size $N$ is often computationally impractical. Instead, we use **Stochastic Gradient Descent (SGD)** to approximate the global cost expectation by sampling a small, random mini-batch of size $B$:

$$\mathbf{g} = \frac{1}{B}\sum_{i=1}^B \nabla_{\mathbf{w}} \mathcal{L}\left(x^{(i)}, y^{(i)} \;\middle|\; \mathbf{w}\right)$$

#### Statistical Variance Properties

The standard error ($SE$) of an empirical mean estimated from $B$ independent samples is given by:

$$SE(\hat{\mu}) = \frac{\sigma}{\sqrt{B}}$$

where $\sigma$ represents the true standard deviation of the underlying data distribution.

This relationship explains why increasing the batch size yields sublinear returns in gradient accuracy. For example, consider two gradient estimates:

- **Estimate A:** Evaluated using $B_A = 100$ samples.
    
- **Estimate B:** Evaluated using $B_B = 10,000$ samples.
    

While Estimate B requires $100\times$ more computational steps than Estimate A, its standard error is only reduced by a factor of $\sqrt{100} = 10$. Because of this sublinear scaling, mini-batch sizes between $B=32$ and $B=256$ are typically chosen to balance computational efficiency with stable variance updates.

### E. Higher-Order Optimization: Momentum Frameworks

**Momentum** optimization mimics physical acceleration to help gradient updates navigate areas of high curvature or noisy, conflicting gradients.

#### Classical Momentum Formulation

We introduce an internal velocity vector $\mathbf{v}$ that maintains a running history of past updates, controlled by an exponential decay parameter $\alpha \in [0, 1)$:

$$\mathbf{v}_t = \alpha \mathbf{v}_{t-1} - \eta \mathbf{g}_t$$

$$\mathbf{w}_t = \mathbf{w}_{t-1} + \mathbf{v}_t$$

#### Derivation of Terminal Velocity

If the local gradients consistently point in the same directional vector $-\mathbf{g}$ across consecutive iterations, the velocity vector eventually reaches a stable equilibrium known as **terminal velocity** ($\mathbf{v}_\infty$):

$$\mathbf{v}_\infty = \alpha \mathbf{v}_\infty - \eta \mathbf{g} \implies \mathbf{v}_\infty (1 - \alpha) = - \eta \mathbf{g} \implies \mathbf{v}_\infty = -\frac{\eta \mathbf{g}}{1 - \alpha}$$

The parameter update step at terminal velocity becomes:

$$\Delta \mathbf{w} = -\frac{\eta \|\mathbf{g}\|}{1 - \alpha}$$

> [!tip] Think of the term $\frac{1}{1-\alpha}$ as an effective speed multiplier. Setting $\alpha = 0.9$ scales the steady-state velocity up by a factor of $10\times$ compared to standard gradient descent. This acceleration helps the model push through flat plateaus and shallow local minima.

#### Nesterov Accelerated Gradient (NAG)

Nesterov momentum improves upon classical momentum by evaluating the gradient _after_ applying the current velocity step, acting as a predictive look-ahead mechanism:

$$\mathbf{v}_t = \alpha \mathbf{v}_{t-1} - \eta \nabla_{\mathbf{w}} \mathcal{L}\left(\mathbf{w}_{t-1} + \alpha \mathbf{v}_{t-1}\right)$$

```
  Classical Momentum:      w_(t-1) -----------> +alpha*v_(t-1) ----------> w_t (Apply -eta*grad at start)
  
  Nesterov Momentum:       w_(t-1) ---> +alpha*v_(t-1) ---> [Look-ahead point] ---> Evaluate gradient here
```

## 3. Practical Implementation & Self-Study Bridge

### A. Architectural Structural Mapping

In the companion self-study notebook (`Self study 1.ipynb`), the conceptual building blocks of neural networks are implemented using PyTorch expressions.

Python

```python
import torch.nn as nn

# Explicit Sequential Architecture Pipeline Mapping
model = nn.Sequential(
    nn.Linear(2, 1),   # Evaluates weighted input combination: z = w^T x + b
    nn.ReLU(),         # Non-linear activation: maps values via max(0, z)
    nn.Linear(1, 1),   # Second parameter layer transformation
    nn.Sigmoid()       # Squashes output values into a probabilistic range
)
criterion = nn.BCELoss()  # Binary Cross-Entropy loss mapping
```

During the model's training loop, the optimization sequence must be executed in a specific order to manage the data flow through PyTorch's backend:

Python

```
# Standard Iterative Training Loop Steps
optimizer.zero_grad()               # 1. Reset gradient buffers from the previous loop
predictions = model(inputs)          # 2. Forward pass: compute predictions
loss = criterion(predictions, target) # 3. Compute scalar loss value
loss.backward()                     # 4. Backward pass: evaluate all partial derivatives via Autograd
optimizer.step()                     # 5. Update model weights using the optimization formula
```

> [!important]
> 
> Calling `optimizer.zero_grad()` at the start of each iteration is critical. By default, PyTorch **accumulates** gradients in its buffers during the backward pass rather than overwriting them. This accumulation behavior is useful for advanced architectures like recurrent networks or gradient checkpointing, but for standard training loops, failing to reset the gradients will corrupt the update steps.

### B. Convolutional Extension Analysis

The self-study extends this standard linear architecture to include spatial transformations for image processing tasks:

Python

```python
import torch.nn.functional as F

class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 15, kernel_size=5) # 2D spatial feature mapping
        self.fc = nn.Linear(15 * 24 * 24, 10)       # Classification projection layer

    def forward(self, xb):
        # Apply 2D convolution followed by a ReLU activation function
        xb = F.relu(self.conv1(xb))
        # Flatten the spatial feature maps into a 1D vector for the linear layer
        xb = xb.view(-1, 15 * 24 * 24)
        xb = self.fc(xb)
        return xb
```

- **Spatial Flattening (`xb.view`):** The transition from 2D convolutional feature maps to a 1D classification vector requires flattening the tensor dimensions while preserving the batch size (`-1`).
    
- **Loss Function Integration:** When using `nn.CrossEntropyLoss` in PyTorch, the network output should not include a final Softmax layer. PyTorch integrates the Softmax activation directly into the cross-entropy loss function using a log-sum-exp numerical optimization, which improves training stability and avoids underflow errors.
    

## 4. Critical Insights & Conceptual Connections

### A. The Vanishing Gradient Problem: The "Decimal Chain Reaction"

In deep networks with many layers, backpropagation can stall because gradients shrink exponentially as they travel backward toward the input layers. This behavior is analyzed in detail in `exercises.ipynb`.

Consider a deep architecture using Sigmoid activation functions. The derivative of the sigmoid function is bounded by $\sigma'(z) \le 0.25$. When computing the gradient for the earliest weight layer ($\mathbf{W}_1$) in an $L$-layer deep network, the chain rule multiplies the activation derivatives together layer by layer:

$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_1} \propto \prod_{l=1}^L \frac{\partial a^{(l)}}{\partial z^{(l)}} \le (0.25)^L$$

For a modest network of $L=5$ hidden layers, this derivative product shrinks significantly:

$$\text{Gradient Scale Factor} \le (0.25)^5 \approx 0.000976$$

This **Decimal Chain Reaction** means that as network depth increases, the learning signal reaching the earliest layers drops exponentially toward zero. As a result, the early layers train incredibly slowly or stop updating entirely, preventing the network from learning complex low-level features.

### B. Exploding Gradients and Cost Landscape Cliffs

Conversely, deep networks can also suffer from **exploding gradients**, where deep weight products cause gradient values to grow exponentially. This issue often occurs in highly complex error landscapes that feature extremely steep drop-offs, or "cliffs".

```
       Loss Error (J)
            |
            |   \
            |    \  <- High curvature landscape region
            |_____\
            |     |
            |     | <- Dangerous Cliff: produces massive gradient vectors
            |_____|____________________> Parameters (w, b)
```

When an update step lands near one of these cliffs, the massive gradient can launch the parameters completely out of the optimal training zone, causing the loss to explode or destabilizing the model entirely.

To prevent these unstable jumps, we apply **Gradient Clipping** to cap the maximum size of a gradient update before updating the parameters:

$$\text{if } \|\mathbf{g}\| > v \quad \text{then} \quad \mathbf{g} \leftarrow \frac{\mathbf{g} \cdot v}{\|\mathbf{g}\|}$$

This scaling operation caps the gradient's length to a maximum threshold $v$ while keeping its descent direction completely unchanged. This clipping mechanism stabilizes training loops, allowing models to navigate highly curved error surfaces safely.


# Lecture 5: Probabilistic Models and Learning

## 1. Executive Summary & Core Objectives

This lecture introduces **Probabilistic Graphical Models (PGMs)**, focusing on **Bayesian Networks (BNs)** and the underlying statistical principles used to learn their parameters from data. It bridges high-dimensional joint probability spaces with factored local conditional representations, establishing the mathematical foundations for modeling uncertainty.

The core objectives of this session are:

- **Formalize Bayesian Network Semantics:** Review the syntax of directed acyclic graphs (DAGs) and understand how structural d-separation determines conditional independence, enabling high-dimensional joint distributions to factor into low-dimensional components.
    
- **Master Parameter Estimation Frameworks:** Deconstruct **Maximum Likelihood Estimation (MLE)** and **Bayesian Parameter Learning** for continuous and discrete distributions under the Independent and Identically Distributed (i.i.d.) assumption.
    
- **Address Data Incompleteness:** Evaluate how missing data mechanisms—**Missing Completely at Random (MCAR)**, **Missing at Random (MAR)**, and **Non-ignorable** parameters—impact learning, and formalize the optimization mechanics of the **Expectation-Maximization (EM)** algorithm.
    
- **Mitigate Parameter Overfitting:** Analyze the failure mode of zero-probability assignment on unseen configurations and resolve it using conjugate priors, Beta-Binomial updates, and Laplace parameter smoothing.
    

## 2. Theoretical Foundations & Mathematical Models

### A. Bayesian Network Syntax and Semantics

A Bayesian Network models a joint probability distribution over a set of random variables $\mathcal{V} = \{X_1, X_2, \dots, X_n\}$ through structural decomposition.

#### 1. Structural Syntax

A Bayesian network consists of a Directed Acyclic Graph (DAG) $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where:

- The nodes $\mathcal{V}$ represent the random variables.
    
- The directed edges $\mathcal{E}$ represent direct probabilistic dependencies.
    
- For each variable $X_i \in \mathcal{V}$, its immediate parents are denoted as $pa(X_i) = \{Y \in \mathcal{V} \mid (Y \to X_i) \in \mathcal{E}\}$.
    
- The set of non-descendants of a variable $X_i$ is denoted as $nd(X_i)$.
    

#### 2. The Local Markov Property

The foundational assumption of a Bayesian network structure is the **Local Markov Property**: each random variable $X_i$ is conditionally independent of its non-descendants given its parents.

$$X_i \perp \perp nd(X_i) \mid pa(X_i)$$

#### 3. Factorisation Property

By applying the local Markov property to the general chain rule of probability, the complete joint probability distribution $P(X_1, X_2, \dots, X_n)$ decomposes into a product of local **Conditional Probability Distributions (CPDs)**:

$$P(X_1, X_2, \dots, X_n) = \prod_{i=1}^n P(X_i \mid pa(X_i))$$

### B. Probabilistic Inference Operations

Probabilistic inference computes the posterior distribution of a set of query variables $X_Q$ given observed evidence $X_E = x_e$, expressed as $P(X_Q \mid x_e)$. This process relies on three core operations on mathematical potentials:

1. **Restriction:** Modifying a probability potential to focus only on configurations that match the observed evidence values $x_e$ (e.g., transforming a general potential $P(G \mid E)$ into a restricted potential $P(g \mid E)$ given evidence $G=g$).
    
2. **Combination:** Multiplying independent or conditional potentials together to form a larger joint space over the union of their variables:
    
    $$\psi(X, Y, Z) = \phi_1(X, Y) \cdot \phi_2(Y, Z)$$
    
3. **Marginalisation:** Summing out (discrete) or integrating out (continuous) nuisance variables $X_N$ from a joint potential to simplify the distribution down to the remaining variables:
    
    $$\sum_{l} P(l \mid e) \cdot P(x \mid l, g) = P(x \mid e, g)$$
    

### C. Maximum Likelihood Parameter Learning (Complete Data)

Given a dataset $\mathcal{D} = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_N\}$ consisting of independent and identically distributed (i.i.d.) observations, Maximum Likelihood Estimation seeks parameter values $\hat{\theta}$ that maximize the probability of generating the observed data.

$$\hat{\theta} = \arg\max_{\theta} L(\theta \mid \mathcal{D}) = \arg\max_{\theta} \prod_{i=1}^N P(\mathbf{x}_i \mid \theta)$$

Because products can introduce numerical underflow issues, we maximize the monotone **Log-Likelihood** function instead:

$$\ln L(\theta \mid \mathcal{D}) = \sum_{i=1}^N \ln P(\mathbf{x}_i \mid \theta)$$

#### 1. Discrete Parameters in Bayesian Networks

When the data is complete (no missing values), the joint log-likelihood of a Bayesian network decomposes into independent local optimization problems for each node:

$$\ln L(\theta \mid \mathcal{D}) = \sum_{i=1}^N \sum_{X \in \mathcal{V}} \ln P(X \mid pa(X), \theta)(\mathbf{x}_i)$$

For discrete categorical variables, the maximum likelihood parameter $\hat{\theta}_{ijk} = P(X_i = k \mid pa(X_i) = j)$ simplifies to an intuitive counting problem:

$$\hat{\theta}_{ijk} = \frac{N(X_i = k, pa(X_i) = j)}{\sum_{k'} N(X_i = k', pa(X_i) = j)}$$

where $N(\cdot)$ represents the empirical count of instances in the dataset matching that specific variable configuration.

#### 2. Continuous Parameters: Univariate Gaussian MLE

For a continuous feature $X$ modeled as a univariate Gaussian distribution $\mathcal{N}(\mu, \sigma^2)$, the probability density function is defined as:

$$f(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left( -\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2 \right)$$

Taking the log-likelihood over $N$ observations yields:

$$\ln L(\mu, \sigma^2) = -\frac{1}{2\sigma^2} \sum_{i=1}^N (x_i - \mu)^2 - \frac{N}{2} \ln(2\pi\sigma^2)$$

Setting the partial derivatives with respect to $\mu$ and $\sigma^2$ to zero gives the closed-form maximum likelihood solutions:

$$\frac{\partial \ln L}{\partial \mu} = 0 \implies \hat{\mu} = \frac{1}{N} \sum_{i=1}^N x_i$$

$$\frac{\partial \ln L}{\partial \sigma^2} = 0 \implies \hat{\sigma}^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \hat{\mu})^2$$

### D. Learning with Incomplete Data: Missingness Mechanisms and EM

Real-world datasets often contain missing values. To handle incomplete data effectively, we must model the underlying missingness mechanism.

#### 1. Categorization of Missing Data

- **Missing Completely at Random (MCAR):** The probability that a value is missing is entirely independent of both the observed values and the unobserved hidden entries.
    
- **Missing at Random (MAR):** The probability that a value is missing depends strictly on other features that are fully observed in the dataset.
    
- **Non-ignorable (Missing Not at Random - MNAR):** The missingness depends directly on the unobserved value itself (e.g., an extreme right-wing voter refusing to answer an exit poll).
    

#### 2. The Expectation-Maximization (EM) Algorithm

When data is missing under a MAR mechanism, the log-likelihood cannot be optimized in closed form. The **Expectation-Maximization (EM)** algorithm circumvents this by iteratively maximizing the expected marginal log-likelihood using a two-step process:

```
                  +--------------------------------+
                  |  Initialize parameters \theta  |
                  +----------------+---------------+
                                   |
                                   v
                    +--------------+--------------+
                    |  E-Step: Compute expected   | <------+
                    |  sufficient statistics Q    |        |
                    +--------------+--------------+        | Loop until
                                   |                       | convergence
                                   v                       |
                    +--------------+--------------+        |
                    |  M-Step: Maximize Q to update| -------+
                    |  parameter estimates \theta  |
                    +------------------------------+
```

- **The E-step (Expectation):** Calculate the expected values of the missing sufficient statistics using the current parameter estimates $\theta^t$ and the observed data parts $\mathcal{D}_{\text{obs}}$. For a discrete variable configuration:
    
    $$\mathbb{E}[N(X_i = k, pa(X_i) = j) \mid \mathcal{D}_{\text{obs}}, \theta^t] = \sum_{d \in \mathcal{D}} P(X_i = k, pa(X_i) = j \mid d, \theta^t)$$
    
- **The M-step (Maximization):** Treat these expected statistics as actual counts to update the parameters, maximizing the expected log-likelihood:
    
    $$\hat{\theta}_{ijk}^{t+1} = \frac{\mathbb{E}[N(X_i = k, pa(X_i) = j) \mid \mathcal{D}, \theta^t]}{\sum_{k'} \mathbb{E}[N(X_i = k', pa(X_i) = j) \mid \mathcal{D}, \theta^t]}$$
    

### E. Fully Bayesian Parameter Learning

The Bayesian paradigm treats parameters $\theta$ not as fixed constants, but as latent random variables governed by prior distributions.

$$\begin{matrix} \text{Prior Distribution} & \text{Likelihood Function} & \text{Posterior Distribution} \\ P(\theta) & P(\mathcal{D} \mid \theta) & P(\theta \mid \mathcal{D}) \propto P(\theta)P(\mathcal{D} \mid \theta) \end{matrix}$$

#### Conjugate Analysis: The Beta-Bernoulli Model

For binary outcomes modeled as a Bernoulli process with parameter $\theta \in [0,1]$, the **Beta Distribution** serves as the conjugate prior:

$$P(\theta) = \text{Beta}(\theta \mid a, b) \propto \theta^{a-1}(1-\theta)^{b-1}$$

where $a$ and $b$ are hyper-parameters representing virtual pseudo-counts.

If a dataset records $N_1$ successes and $N_0$ failures, multiplying the Beta prior by the Bernoulli likelihood yields a posterior distribution that remains within the Beta family:

$$P(\theta \mid \mathcal{D}) \propto \left( \theta^{a-1}(1-\theta)^{b-1} \right) \cdot \left( \theta^{N_1}(1-\theta)^{N_0} \right) = \theta^{a + N_1 - 1}(1-\theta)^{b + N_0 - 1}$$

$$P(\theta \mid \mathcal{D}) = \text{Beta}(\theta \mid a + N_1, b + N_0)$$

#### Posterior Predictive Inference

To predict the next unobserved instance $X_{N+1}$ given the historical dataset, we integrate over the entire parameter posterior space instead of relying on a single point estimate:

$$P(X_{N+1} = 1 \mid \mathcal{D}) = \int_{0}^1 P(X_{N+1} = 1 \mid \theta) P(\theta \mid \mathcal{D}) \, d\theta = \int_{0}^1 \theta \cdot \text{Beta}(\theta \mid a + N_1, b + N_0) \, d\theta$$

This integration evaluates directly to the expected mean of the updated Beta distribution:

$$P(X_{N+1} = 1 \mid \mathcal{D}) = \frac{a + N_1}{a + b + N_1 + N_0}$$

## 3. Practical Implementation & Self-Study Bridge

### A. Univariate Gaussian Parameters

In the self-study companion notebook (`exercises_02.ipynb` Part 1), maximum likelihood estimations are performed on an empirical continuous 1D dataset:

Python

```python
import numpy as np
from scipy.stats import norm

# Continuous numeric evaluation array from self-study
data = np.array([4.04078064, -0.55665445, 3.05080334, 5.08400317, 2.72089663, 0.71922335])

# Calculate maximum likelihood estimates for parameters
mu_hat, sigma_hat = norm.fit(data)
print(f"Estimated Mu: {mu_hat:.4f}, Estimated Sigma: {sigma_hat:.4f}")
```

#### Code-to-Theory Correspondence

The function call `norm.fit(data)` maps directly to the analytical closed-form derivative roots derived for a univariate Gaussian:

- The computed value `mu_hat` ($\hat{\mu} = 2.1764$) implements the empirical sample mean equation $\frac{1}{N}\sum x_i$.
    
- The computed value `sigma_hat` ($\hat{\sigma} = 2.0836$) implements the square root of the variance equation $\sqrt{\frac{1}{N}\sum(x_i - \hat{\mu})^2}$.
    

### B. Constructing a Discrete Naive Bayes Classifier from Frequencies

Part 2 of the self-study constructs a Naive Bayes network to evaluate a poker game dataset. The task maps the best-hand outcome variable (`BH` $\in$ [op, me, draw]) against three conditional features: my hand (`MH`), first-round cards changed (`FC`), and second-round cards changed (`SC`).

Python

```python
import pandas as pd
import numpy as np

# Load observation parameters
df = pd.read_csv("poker_data.csv")
classes = ['op', 'me', 'draw']
n_total = df.shape[0]

# 1. Compute empirical global class priors P(BH)
priors = np.array([df[df.BH == c].shape[0] for c in classes]) / n_total

# Target configurations for checking posterior probability
target_MH, target_FC, target_SC = "1a", 1, 1
likelihoods = []

# 2. Iterate through discrete graph classes to isolate local counts
for c in classes:
    df_class = df[df.BH == c]
    n_class = df_class.shape[0]
    
    # Calculate empirical maximum likelihood frequencies P(Feature | Class)
    p_MH = df_class[df_class.MH == target_MH].shape[0] / n_class
    p_FC = df_class[df_class.FC == target_FC].shape[0] / n_class
    p_SC = df_class[df_class.SC == target_SC].shape[0] / n_class
    
    likelihoods.append(p_MH * p_FC * p_SC)

# 3. Apply combination via product array mapping
scores = priors * np.array(likelihoods)
posterior = scores / np.sum(scores)
```

#### Parameter Extraction Analysis

This program builds joint classification scores without utilizing external libraries, relying entirely on frequency tables. The manual calculation steps map directly to the discrete factorisation rules of Naive Bayes:

$$P(\text{Class} \mid \text{Features}) \propto P(\text{Class}) \cdot \prod_{i} P(\text{Feature}_i \mid \text{Class})$$

## 4. Critical Insights & Conceptual Connections

### A. The Zero-Probability Structural Pitfall and Laplace Smoothing

The code example in `exercises_02.ipynb` reveals a major vulnerability of vanilla Maximum Likelihood Estimation when applied to sparse datasets.

```
       Training Sample Split                   Calculated Posterior
  ===============================        =================================
   Draw occurrences in data = 0 ---------> P(BH = draw | Evidence) = 0.0000
                                          Locks prediction; ignores features
```

Because the specific outcome `draw` never appears alongside the features `MH=1a`, `FC=1`, or `SC=1` in the 20 training rows, the empirical count calculation drops to exactly zero:

$$P(\text{MH}=1\text{a} \mid \text{BH}=\text{draw}) = \frac{0}{N_{\text{draw}}} = 0$$

Since the joint score is computed as a product of terms, this single zero forces the entire posterior probability for that class to zero:

$$\text{Score}(\text{BH}=\text{draw}) = P(\text{draw}) \cdot 0 \cdot P(\text{FC}=1 \mid \text{draw}) \cdot P(\text{SC}=1 \mid \text{draw}) = 0$$

This represents a critical failure mode: the model layout asserts that a draw is completely impossible under these conditions, regardless of any encouraging evidence from other features.

#### The Laplace Smoothing Solution

To fix this, we introduce a uniform pseudo-count $\alpha$ (typically $\alpha = 1$) to all frequency tables before normalizing, ensuring that no conditional probability ever drops to zero:

$$P(X_i = k \mid pa(X_i) = j) = \frac{N(X_i = k, pa(X_i) = j) + \alpha}{\sum_{k'} \left( N(X_i = k', pa(X_i) = j) + \alpha \right)}$$

This adjustment smooths the parameter estimates, preventing extreme zero-probability assignments and improving the model's generalization on unseen test data.

### B. Iterative Optimization Landscapes: EM Multi-Modality

While Maximum Likelihood parameters can be calculated using deterministic closed-form equations when data is complete, learning from incomplete data via the EM algorithm requires iterative numerical optimization.

Because the hidden variables break the log-likelihood's algebraic symmetry, the optimization surface for incomplete data becomes non-convex, frequently featuring multiple local maxima and saddle points.

> [!brainstorm]
> 
> The EM algorithm climbs this optimization surface using coordinate accent. While it is mathematically guaranteed to increase the marginal log-likelihood at every step, it cannot guarantee convergence to the global maximum. The algorithm can easily stall in a sub-optimal local peak if initialized poorly. To mitigate this risk, real-world PGM training pipelines use **Random Restarts**—running the EM loop multiple times from different, randomly sampled parameter starting points $\theta^0$ to isolate the best global fit.

### C. Box's Loop: The Iterative PGM Development Cycle

The process of building, evaluating, and refining probabilistic graphical models follows a structured scientific framework known as **Box's Loop**:

```
                 +---------------------------------------+
                 | 1. BUILD MODEL                        |
                 | Define DAG topology and dependencies |
                 +-------------------+-------------------+
                                     |
                                     v
                 +-------------------+-------------------+
                 | 2. INFER LATENT QUANTITIES            |
                 | Compute parameters via MLE, EM, or Beta|
                 +-------------------+-------------------+
                                     |
                                     v
                 +-------------------+-------------------+
                 | 3. CRITICIZE MODEL                    |
                 | Check performance and zero anomalies |
                 +-------------------+-------------------+
                                     |
                                     v
                 +-------------------+-------------------+
                 | 4. REVISE MODEL                       |
                 | Add Laplace smoothing or adjust links |
                 +-------------------+-------------------+
                                     |
                                     +-----------------------(Loop back to Step 1)
```

1. **Build Model:** Formulate the DAG structure based on domain knowledge or causal rules.
    
2. **Infer Latent Quantities:** Learn the network parameters from data using Maximum Likelihood, Expectation-Maximization, or Bayesian updates.
    
3. **Criticize Model:** Evaluate the model's predictions against real-world test data to identify anomalies, such as severe overfitting from zero counts.
    
4. **Revise Model:** Refine the model by adding Laplace smoothing, using informative priors, or adjusting the graph structure, restarting the cycle to build a more robust system.


# Lecture 6: Probabilistic Models and Learning

## 1. Executive Summary & Core Objectives

This lecture focuses on the shift from deterministic machine learning paradigms to **Probabilistic Graphical Models (PGMs)** and **Probabilistic Programming Languages (PPLs)**, with a practical focus on the **Pyro** framework. Standard machine learning models optimize point estimates of parameters, frequently failing to quantify uncertainty or capture complex generative data structures.

The core objectives of this lecture are:

- To master **Plate Notation** as a syntactic abstraction for representing independent and identically distributed (i.i.d.) random variables and shared conditional probability distributions.
    
- To establish the theoretical framework of **Bayesian Machine Learning**, transitioning from classical Linear and Logistic Regressions to deep **Bayesian Neural Networks (BNNs)**.
    
- To bridge mathematical frameworks with code execution using Pyro, mastering **Stochastic Variational Inference (SVI)**, the **Evidence Lower Bound (ELBO)**, and variational distributions (**Guides**).
    
- To understand **Box’s Loop** as a disciplined, iterative pipeline for generating, estimating, criticizing, and refining probabilistic generative systems.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1 Bayesian Networks Semantics and Plate Notation

A Bayesian Network over a collection of random variables $\mathcal{X} = \{X_1, X_2, \dots, X_n\}$ is defined by a directed acyclic graph (DAG) $\mathcal{G} = \{\mathcal{V}, \mathcal{E}\}$. The nodes $\mathcal{V}$ correspond to the random variables, and the directed edges $\mathcal{E}$ dictate conditional independence assertions. The joint probability distribution decomposes as a product of local conditional probability distributions:

$$p_{\mathcal{N}}(X_1, X_2, \dots, X_n) = \prod_{i=1}^{n} p(X_i \mid \text{pa}(X_i))$$

where $\text{pa}(X_i)$ denotes the set of immediate parent nodes of $X_i$ within the graph $\mathcal{G}$.

When scaling models to data with $N$ independent observations, explicitly writing out the graphical structure results in large, complex graphs (unfolded notation). **Plate Notation** introduces a visual macro to encapsulate repeated substructures. A bounding box (the "plate") indexed by $i = 1 \dots N$ indicates that the sub-graph contained inside replicates $N$ times.

```
 Unfolded Notation:                     Plate Notation:
 
     [ θ ]                                  [ θ ]
    /  |  \                                   |
   v   v   v                                  v
 [X1] [X2] [X3]                          +--------+
                                         |  [Xi]  |
                                         |        |
                                         | i=1..N |
                                         +--------+
```

Parameters outside the plate are global parameters shared across all data replicates, while nodes inside the plate represent local variables unique to each observation.

### 2.2 Generative Modeling & Box's Loop

Generative modeling requires formulating a comprehensive joint distribution $p(\mathcal{X}, \mathcal{Z} \mid \theta)$ over observed data $\mathcal{X}$ and latent variables $\mathcal{Z}$. This specification defines a clear process explaining how the observed data was generated from the latent space.

Evaluating and updating these models follows **Box's Loop**, which divides data analysis into four iterative stages:

1. **Build Model:** Construct a generative joint distribution using priors, generalized linear models, or neural layers.
    
2. **Infer Hidden Quantities:** Compute the posterior distribution $p(\mathcal{Z} \mid \mathcal{X}, \theta)$ over the unobserved parameters given the data.
    
3. **Criticize Model:** Assess model performance via posterior predictive checks ($PPC$) to isolate systematic gaps between the model's simulations and real-world observations:
    
    $$p(X^{\text{new}} \mid \mathcal{X}) = \int p(X^{\text{new}} \mid \mathcal{Z}) p(\mathcal{Z} \mid \mathcal{X}) d\mathcal{Z}$$
    
4. **Apply and Revise Model:** Deploy the system for downstream prediction, or update the model graph to fix issues identified during criticism.
    

### 2.3 Bayesian Linear and Logistic Regression Models

#### Bayesian Linear Regression

Given independent pairs $(x_i, y_i)_{i=1}^N$, where $x_i \in \mathbb{R}^D$ and $y_i \in \mathbb{R}$, classical linear regression fits parameters via point estimation. In contrast, Bayesian linear regression models parameters as random variables.

$$\text{Prior:} \quad w \sim \mathcal{N}(\mu_0, \Sigma_0)$$

$$\text{Likelihood:} \quad Y_i \mid w, x_i \sim \mathcal{N}(w^T x_i, \sigma^2)$$

Here, $w \in \mathbb{R}^D$ represents the vector of regression coefficients, $\sigma^2$ captures data noise (aleatoric uncertainty), and $\Sigma_0$ reflects our initial parameter uncertainty (epistemic uncertainty).

#### Bayesian Logistic Regression

For binary targets $y_i \in \{0, 1\}$, the continuous linear combination is mapped through the sigmoid link function $\sigma(z) = (1 + e^{-z})^{-1}$ to parameterize a Bernoulli or Binomial distribution:

$$\text{Prior:} \quad w \sim \mathcal{N}(\mu_0, \Sigma_0), \quad b \sim \mathcal{N}(\mu_b, \sigma_b^2)$$

$$\text{Likelihood:} \quad Y_i \mid w, b, x_i \sim \text{Bernoulli}(\pi_i) \quad \text{where} \quad \pi_i = \sigma(w^T x_i + b)$$

### 2.4 Approximate Inference: SVI and the ELBO

Computing the true parameter posterior requires applying Bayes' theorem:

$$p(W \mid \mathcal{D}) = \frac{p(\mathcal{D} \mid W) p(W)}{p(\mathcal{D})} = \frac{p(\mathcal{D} \mid W) p(W)}{\int p(\mathcal{D} \mid W) p(W) dW}$$

The denominator—the marginal likelihood or evidence—requires calculating a complex, high-dimensional integral over the parameter space, which quickly becomes intractable for non-conjugate or deep architectures.

**Stochastic Variational Inference (SVI)** turns this integration challenge into an optimization problem. We approximate the true posterior $p(W \mid \mathcal{D})$ using a tractable family of distributions $q_\phi(W)$, parameterized by variational parameters $\phi$. We evaluate this approximation by minimizing the Kullback-Leibler (KL) divergence from $q_\phi(W)$ to $p(W \mid \mathcal{D})$:

$$D_{\text{KL}}(q_\phi(W) \parallel p(W \mid \mathcal{D})) = \int q_\phi(W) \log \frac{q_\phi(W)}{p(W \mid \mathcal{D})} dW$$

Because the true posterior $p(W \mid \mathcal{D})$ is unobservable, we maximize a mathematically equivalent alternative called the **Evidence Lower Bound (ELBO)**:

$$\text{ELBO}(\phi) = \mathbb{E}_{q_\phi(W)} [\log p(\mathcal{D}, W)] - \mathbb{E}_{q_\phi(W)} [\log q_\phi(W)]$$

Maximizing the ELBO directly minimizes the KL divergence since the log evidence is the sum of the ELBO and the KL divergence: $\log p(\mathcal{D}) = \text{ELBO}(\phi) + D_{\text{KL}}(q_\phi(W) \parallel p(W \mid \mathcal{D}))$.

In a **Mean-Field Variational Family**, we assume the variational distribution fully factorizes into independent terms:

$$q_\phi(W) = \prod_{k=1}^K q_{\phi_k}(W_k)$$

For Gaussian approximations, each parameter $W_k$ is assigned its own independent mean $\mu_k$ and variance $\sigma_k^2$, completely ignoring cross-variable correlations to keep optimization fast and scalable.

## 3. Practical Implementation & Self-Study Bridge

Probabilistic programming frameworks like Pyro separate model design from the underlying inference engine.

```
+-------------------------------------------------------------------+
|                     Technical Area 1: Domain Models               |
|            (e.g., Time-Series, BNNs, Generalized Linear Models)   |
+-------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|         Technical Area 2: Probabilistic Programming (Pyro)         |
|         Primitive Primitives: pyro.sample(), pyro.param()         |
+-------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|               Technical Area 3: Inference Solvers                 |
|             (Stochastic Variational Inference via ELBO)           |
+-------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------+
|           Technical Area 4: Execution & Acceleration Backend       |
|              (PyTorch AutoGrad, CPU / GPU Execution)              |
+-------------------------------------------------------------------+
```

### 3.1 Base Pyro Primitives and Conditioning

Pyro's core language relies on two fundamental statements that extend standard PyTorch execution graphs:

- `pyro.sample(name, fn, obs=None)`: Names a random node in the execution graph, binding it to a distribution `fn`. If the `obs` argument is supplied, the node is treated as an observed variable, fixing its value and conditioning the joint distribution directly on that data.
    
- `pyro.param(name, init_tensor, constraint)`: Registers a learnable parameter within the global parameter store (`pyro.get_param_store()`), allowing external optimizers to track and update it across SVI steps.
    

### 3.2 Parameter & Configuration Analysis

#### 1. Vectorized Observations via `pyro.plate`

Instead of using standard Python loops, which build inefficient sequential graphs, vectorization is handled via `pyro.plate`:

Python

```python
# Sequential Loop (Inefficient Engine)
for i in range(len(x_data)):
    pyro.sample(f"obs_{i}", dist.Normal(mu, sigma), obs=x_data[i])

# Vectorized Plate Architecture (Highly Optimized Engine)
with pyro.plate("data_plate", len(x_data)):
    pyro.sample("obs", dist.Normal(mu, sigma), obs=x_data)
```

Using `pyro.plate` signals to the compiler that these observations are conditionally independent given the parent parameters. This allows Pyro to parallelize log-probability evaluations into vectorized tensor operations, drastically accelerating execution.

#### 2. Automatic vs. Manual Variational Guides

An implementation can leverage automated variational guides (`AutoNormal`) or manually defined structures:

Python

```python
# Automated Mean-Field Variational Family
guide = AutoNormal(model)

# Custom Explicit Variational Architecture
def customized_guide(x_data, y_data):
    w_loc = pyro.param("weights_loc", torch.zeros(1, 2))
    w_scale = pyro.param("weights_scale", torch.ones(1, 2), constraint=torch.distributions.constraints.positive)
    pyro.sample("w", dist.Normal(w_loc, w_scale).to_event(2))
```

> [!note]
> 
> The `.to_event()` call alters how Pyro treats tensor dimensions, moving boundaries from parallel batch dimensions to dependent event dimensions. This step ensures that log-likelihood evaluations are correctly summed across the internal parameters of a single event node.

### 3.3 Advanced Code-to-Theory Synthesis: Bayesian Neural Networks

Consider the implementation of a deep Bayesian Neural Network designed to learn nonlinear regressions with heteroscedastic data noise from `ML-3-2026_BayesianNeuralNetworks.ipynb`.

Python

```python
import torch
import pyro
import pyro.distributions as dist

def model(x_data, y_data):
    # Parameter Dimension Profiles
    # x_data: [N, 1], y_data: [N, 1], NHIDDEN = 250
    
    # Layer 1 Weight and Bias Priors
    w1_prior = dist.Normal(loc=torch.zeros(1, 250), scale=torch.ones(1, 250)).to_event(2)
    b1_prior = dist.Normal(loc=torch.zeros(1, 250), scale=torch.ones(1, 250)).to_event(2)
    
    # Layer 2 (Output) Weight and Bias Priors
    w2_prior = dist.Normal(loc=torch.zeros(250, 1), scale=torch.ones(250, 1)).to_event(2)
    b2_prior = dist.Normal(loc=torch.zeros(1, 1), scale=torch.ones(1, 1)).to_event(2)
    
    # Sample weights and biases from prior distributions
    w1 = pyro.sample("w1", w1_prior)
    b1 = pyro.sample("b1", b1_prior)
    w2 = pyro.sample("w2", w2_prior)
    b2 = pyro.sample("b2", b2_prior)
    
    # Latent Noise Observation Prior
    log_sigma = pyro.sample("log_sigma", dist.Normal(0., 1.))
    
    with pyro.plate("data_predictions", len(x_data)):
        # Linear Forward Transformation with non-linear Tanh Activation
        # Layer 1 hidden state: [N, 250]
        hidden_activation = torch.tanh(torch.mm(x_data, w1) + b1)
        
        # Layer 2 prediction mapping: [N, 1]
        predictive_mean = torch.mm(hidden_activation, w2) + b2
        
        # Scale evaluation
        data_variance = torch.exp(log_sigma)
        
        # Condition Likelihood on Observational Data
        pyro.sample("obs", dist.Normal(predictive_mean, data_variance).to_event(1), obs=y_data)
```

#### Code-to-Theory Mapping and Execution Dynamics

- **Weight Sampling as Latent Variables:** Instead of treating network coefficients as fixed values optimized via backpropagation, `w1`, `b1`, `w2`, and `b2` are explicitly sampled from normal priors. This forces the optimization engine to evaluate an entire distribution over functions rather than a single point estimate.
    
- **Nonlinear Activation Logic:** The code uses `torch.tanh` to transform the first layer's output: $\mathbf{H} = \tanh(\mathbf{X}\mathbf{W}_1 + \mathbf{b}_1)$. This activation acts as a nonlinear feature mapping, allowing subsequent linear operations to approximate complex, non-monotonic data patterns like sinusoidal curves.
    
- **Exponentiated Variance Mapping:** The scale of the observational distribution is parameterized using `torch.exp(log_sigma)`. This maps the unbounded real support of the variational parameter $\log \sigma \in (-\infty, \infty)$ directly to valid strictly positive scales $\sigma \in (0, \infty)$, preventing numerical instability during gradient steps.
    

## 4. Critical Insights & Conceptual Connections

### 4.1 Epistemic vs. Aleatoric Uncertainty Profiles

- **Epistemic Uncertainty:** Refers to structural uncertainty regarding our model parameters due to a lack of data. In our Pyro networks, this is captured by the variance of the variational parameter distributions (e.g., `AutoNormal.scales.w`). Epistemic uncertainty is reducible; as the sample size grows ($N \to \infty$), the parameter posteriors narrow, collapsing toward a deterministic point estimate.
    
- **Aleatoric Uncertainty:** Captures inherent, irreducible randomness in the data generation process itself. In our BNN model, this is explicitly handled by the `data_variance` term. No matter how much data we collect, aleatoric uncertainty remains fixed because it reflects the physical limits and noise floor of our system's observations.
    

### 4.2 Structural Optimization Trade-offs in PPL Inferential Solvers

| **Solvers / Abstractions**          | **Advantages**                                                                                      | **Critical Gotchas & Gaps**                                                                                                               |
| ----------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **`AutoNormal` (Mean-Field VI)**    | Fast, scales efficiently to high dimensions; gradient steps are decoupled across latent nodes.      | Ignores cross-parameter correlations, causing it to structurally underestimate posterior variance.                                        |
| **Full-Rank Variational Families**  | Captures complex, correlated parameter posteriors; provides highly realistic uncertainty estimates. | Computational complexity scales quadratically $\mathcal{O}(D^2)$ with parameter count, causing memory bottlenecks in large deep networks. |
| **Markov Chain Monte Carlo (MCMC)** | Asymptotically guarantees convergence to the exact true posterior without structural bias.          | Prohibitively slow on large datasets; cannot leverage parallel GPU acceleration because it relies on sequential sampling chains.          |
|                                     |                                                                                                     |                                                                                                                                           |
|                                     |                                                                                                     |                                                                                                                                           |

> [!brainstorm]
> When testing a model on synthetic data featuring an intentional observation gap (such as no data between $x=0$ and $x=5$), a classical MLE network will produce highly confident but potentially flawed predictions across the missing region.
> 
> In contrast, a deep Bayesian Neural Network surfaces this issue visually: inside the training zones, the sampled alternative means align tightly, indicating low epistemic uncertainty. The moment the evaluation enters the observation gap, the sampled prediction lines diverge wildly, increasing the predictive variance. This warns practitioners that the model lacks the data needed to make reliable choices in that region.

# Lecture 7: Probabilistic Graphical Models: Inference and Learning via Variational Inference

## 1. Executive Summary & Core Objectives

- **Core Focus**: This lecture transitions from exact inference methods (analytically tractable only in highly specialized conjugate models) to **approximate inference** frameworks required for general, complex probabilistic graphical models (PGMs).
    
- **The Optimization Paradigm**: The primary objective is to demonstrate how the problem of estimating an intractable posterior distribution $p(z|x)$ can be recast as a deterministic optimization problem over a tractable family of distributions $\mathcal{Q}$.
    
- **Key Frameworks**: The material introduces **Variational Inference (VI)**, the **Evidence Lower Bound (ELBO)**, **Black Box Variational Inference (BBVI)**, and their practical implementation using the Probabilistic Programming Language (PPL) **Pyro** on top of PyTorch computational graphs.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1 Probabilistic Graphical Models (PGMs) and Intractability

A directed PGM over a collection of random variables $X_1, \dots, X_n$ consists of a directed acyclic graph (DAG) $\mathcal{G} = \{\mathcal{V}, \mathcal{E}\}$ and a set of local conditional distributions $\mathcal{P} = \{p(X_i | pa(X_i)), X_i \in \mathcal{V}\}$, where $pa(X_i)$ denotes the parent nodes of $X_i$. The joint distribution factorizes as:

$$p_N(X_1, \dots, X_n) = \prod_{i=1}^{n} p(X_i | pa(X_i))$$

In a Bayesian configuration containing observed data $x$ and latent variables (or parameters) $z$, inference proceeds via Bayes' rule:

$$p(z|x) = \frac{p(x|z)p(z)}{p(x)} = \frac{p(x|z)p(z)}{\int p(x, z) dz}$$

The denominator $p(x) = \int p(x, z) dz$ is the **marginal likelihood** or **model evidence**. Computing this integral becomes analytically and computationally intractable when $z$ resides in a high-dimensional space or when the likelihood $p(x|z)$ and prior $p(z)$ are non-conjugate.

### 2.2 Variational Inference and the Reverse KL Divergence

Instead of drawing samples from $p(z|x)$ (as in Markov Chain Monte Carlo), Variational Inference chooses a tractable family of distributions $\mathcal{Q} = \{q_\lambda(z)\}$ parameterized by variational parameters $\lambda$, and minimizes the **Kullback-Leibler (KL) divergence** between $q_\lambda(z)$ and the true posterior $p(z|x)$:

$$\hat{q}(z) = \arg\min_{\lambda} KL(q_\lambda(z) \parallel p(z|x))$$

The continuous KL divergence from $g(z)$ to $f(z)$ is formally defined as:

$$KL(f \parallel g) = \int_{z} f(z) \log\left(\frac{f(z)}{g(z)}\right) dz = \mathbb{E}_f\left[\log\left(\frac{f(z)}{g(z)}\right)\right]$$

Because $KL(f \parallel g) \neq KL(g \parallel f)$, the selection of the divergence direction alters the approximation properties:

- **Forward KL ($KL(p \parallel q)$)**: _Mean-seeking_ or zero-avoiding. It forces $q(z) > 0$ wherever $p(z) > 0$, causing $q(z)$ to average over multiple modes.
    
- **Reverse KL ($KL(q \parallel p)$)**: _Mode-seeking_ or zero-forcing. It forces $q(z) = 0$ wherever $p(z) = 0$. In Variational Inference, optimizing the reverse KL causes $q_\lambda(z)$ to lock onto a single local mode of the true posterior and underestimate its variance.
    

### 2.3 Mathematical Derivation of the Evidence Lower Bound (ELBO)

Direct minimization of $KL(q_\lambda(z) \parallel p(z|x))$ is impossible because it requires explicit access to the intractable true posterior $p(z|x)$. We expand the KL divergence definition to circumvent this constraint:

$$KL(q(z) \parallel p(z|x)) = \mathbb{E}_q\left[\log\frac{q(z)}{p(z|x)}\right]$$

Applying Bayes' rule ($p(z|x) = \frac{p(z, x)}{p(x)}$) yields:

$$KL(q(z) \parallel p(z|x)) = \mathbb{E}_q\left[\log\frac{q(z) \cdot p(x)}{p(z, x)}\right]$$

Using the linearity of expectation and separating terms:

$$KL(q(z) \parallel p(z|x)) = \mathbb{E}_q[\log p(x)] + \mathbb{E}_q\left[\log\frac{q(z)}{p(z, x)}\right]$$

Because $\log p(x)$ does not depend on the variational distribution $q(z)$, its expectation with respect to $q(z)$ is itself:

$$KL(q(z) \parallel p(z|x)) = \log p(x) - \mathbb{E}_q\left[\log\frac{p(z, x)}{q(z)}\right]$$

We define the **Evidence Lower Bound (ELBO)**, denoted as $\mathcal{L}(q)$, as:

$$\mathcal{L}(q) = \mathbb{E}_q\left[\log\frac{p(z, x)}{q(z)}\right] = \int_z q(z) \log\left(\frac{p(z, x)}{q(z)}\right) dz$$

Substituting $\mathcal{L}(q)$ back into our equation establishes the fundamental relationship:

$$\log p(x) = \mathcal{L}(q) + KL(q(z) \parallel p(z|x))$$

> [!note] Since Gibbs' Inequality states that $KL(q \parallel p) \ge 0$, it guarantees that $\log p(x) \ge \mathcal{L}(q)$. Because the marginal log-likelihood $\log p(x)$ is fixed with respect to $q(z)$, maximizing $\mathcal{L}(q)$ directly minimizes $KL(q(z) \parallel p(z|x))$.

We can decompose the ELBO to expose its regularizing properties:

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(z, x)] - \mathbb{E}_q[\log q(z)] = \mathbb{E}_q[\log p(x|z) + \log p(z)] - \mathbb{E}_q[\log q(z)]$$

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x|z)] - \left( \mathbb{E}_q[\log q(z)] - \mathbb{E}_q[\log p(z)] \right)$$

$$\mathcal{L}(q) = \underbrace{\mathbb{E}_{q_\lambda(z)}[\log p(x|z)]}_{\text{Reconstruction Term}} - \underbrace{KL(q_\lambda(z) \parallel p(z))}_{\text{Penalty/Regularization Term}}$$

### 2.4 The Mean Field Assumption

To make the optimization over $\mathcal{Q}$ practical, we must constrain its functional form. The **Mean Field Assumption** decomposes $q(z)$ into independent factors for each latent variable:

$$q_\lambda(z) = \prod_{i=1}^K q_{\lambda_i}(z_i)$$

While computationally efficient, this assumption strips away any structural correlation between distinct latent components, forcing the variational posterior to align along the coordinate axes.

### 2.5 Black Box Variational Inference (BBVI)

Traditional VI requires evaluating model-specific expectations analytically, limiting its scalability. Black Box Variational Inference automates this process by evaluating the gradient of the ELBO using Monte Carlo architectures.

To optimize $\mathcal{L}(q)$ using gradient ascent, we compute its derivative with respect to the variational parameters $\lambda$:

$$\nabla_\lambda \mathcal{L}(q) = \nabla_\lambda \mathbb{E}_{q_\lambda(z)}\left[\log p(z, x) - \log q_\lambda(z)\right]$$

$$\nabla_\lambda \mathcal{L}(q) = \nabla_\lambda \int_z q_\lambda(z) \left[\log p(z, x) - \log q_\lambda(z)\right] dz$$

Distributing the derivative via the product rule:

$$\nabla_\lambda \mathcal{L}(q) = \int_z \left(\nabla_\lambda q_\lambda(z)\right) \left[\log p(z, x) - \log q_\lambda(z)\right] dz + \int_z q_\lambda(z) \left(-\nabla_\lambda \log q_\lambda(z)\right) dz$$

Using the identity $\nabla_\lambda q_\lambda(z) = q_\lambda(z) \nabla_\lambda \log q_\lambda(z)$ (the **score function** or **log-derivative trick**):

$$\nabla_\lambda \mathcal{L}(q) = \int_z q_\lambda(z) \nabla_\lambda \log q_\lambda(z) \left[\log p(z, x) - \log q_\lambda(z)\right] dz - \int_z \nabla_\lambda q_\lambda(z) dz$$

Since $\int_z q_\lambda(z) dz = 1$, its gradient is zero ($\int_z \nabla_\lambda q_\lambda(z) dz = 0$). This leaves the standard score function estimator:

$$\nabla_\lambda \mathcal{L}(q) = \mathbb{E}_{q_\lambda(z)} \left[ \left(\log p(z, x) - \log q_\lambda(z)\right) \cdot \nabla_\lambda \log q_\lambda(z) \right]$$

Approximating this expectation via $M$ empirical samples $\tilde{z}^{(j)} \sim q_\lambda(z)$ produces:

$$\nabla_\lambda \mathcal{L}(q) \approx \frac{1}{M} \sum_{j=1}^M \left[ \left(\log p(\tilde{z}^{(j)}, x) - \log q_\lambda(\tilde{z}^{(j)})\right) \cdot \nabla_\lambda \log q_\lambda(\tilde{z}^{(j)}) \right]$$

> [!warning] While this BBVI estimator requires only the un-normalized joint distribution $p(z, x)$ , it exhibits exceptionally high variance because it samples products of loose log-probability bounds. This requires specialized variance-reduction algorithms like control variates or pathwise reparameterization.

## 3. Practical Implementation & Self-Study Bridge

An analysis of the practical self-study (`ML-2026-Self study 4.ipynb`) highlights a direct connection to the theory. The objective is to perform Bayesian Linear Regression on a synthesized dataset ($N=50$, $true\_w_0 = 1.0$, $true\_w_1 = 0.5$) with Gaussian observation noise of precision $\gamma = 4.0$ ($\sigma = 0.5$).

### 3.1 Model Decomposition into PGM Syntax

The generative process is written in Pyro syntax inside `lin_reg_model(data)`:

Python

```python
def lin_reg_model(data):
    w0 = pyro.sample("w0", dist.Normal(0.0, 10.0))
    w1 = pyro.sample("w1", dist.Normal(w0, 10.0))

    with pyro.plate("data_plate"):
        pyro.sample("y", dist.Normal(data["x"] * w1 + w0, 1.0), obs=data["y"])
```

This script maps to the joint probability model:

$$p(y, w_0, w_1 | x) = p(w_0) \cdot p(w_1 | w_0) \cdot \prod_{i=1}^{N} p(y_i | x_i, w_0, w_1)$$

Crucially, the prior exhibits structural dependency: $w_1 \sim \mathcal{N}(w_0, 10.0)$, meaning the prior mean of the slope depends directly on the instantiation of the intercept.

### 3.2 Constructing a Non-Mean-Field Variational Guide

Standard mean-field routines assume full factorization: $q(w_0, w_1) = q(w_0)q(w_1)$. As shown in the slide visualizations (Slide 9), this assumption discards correlations and underestimates parameter uncertainty.

To fix this, the customized guide in the self-study implements a **Structured/Dependent Variational Distribution**:

$$q(w_0, w_1) = q(w_0) \cdot q(w_1 | w_0)$$

Python

```python
def lin_reg_guide(data):
    # Intercept Variational Distribution: q(w0)
    w0_mean = pyro.param("w0_mean", torch.tensor(0.0))
    w0_scale = pyro.param("w0_scale", torch.tensor(1.0), constraint=constraints.positive)
    w0 = pyro.sample("w0", dist.Normal(w0_mean, w0_scale))

    # Conditioned Slope Variational Distribution: q(w1 | w0)
    w1_base = pyro.param("w1_base", torch.tensor(0.0))      # Intercept for w1 mean
    w1_coeff = pyro.param("w1_coeff", torch.tensor(1.0))    # Covariance coupling parameter
    w1_scale = pyro.param("w1_scale", torch.tensor(1.0), constraint=constraints.positive)

    # Injecting the linear dependency trick
    w1_dynamic_mean = w1_base + (w1_coeff * w0)
    pyro.sample("w1", dist.Normal(w1_dynamic_mean, w1_scale))
```

### 3.3 Core Mechanism of the Dependency Trick

By setting `w1_dynamic_mean = w1_base + (w1_coeff * w0)`, the guide injects a conditional mean dependency during SVI execution. When Pyro draws a sample $\tilde{w}_0 \sim q(w_0)$, it scales the location parameter of $q(w_1)$.

This structure allows the variational approximation to capture linear correlations between $w_0$ and $w_1$ across the computational graph, circumventing the variance-underestimation bottleneck typical of mean field models.

### 3.4 Parameter Execution and Hyperparameter Logic

- **`pyro.infer.SVI`**: The inference engine that wraps the model and guide execution.
    
- **`Trace_ELBO()`**: Instantiates the loss computational graph. It constructs Monte Carlo expectations of the joint probability execution trace against the guide sample traces to compute the ELBO value.
    
- **`pyro.optim.SGD({"lr": 0.0001})`**: Implements Stochastic Gradient Descent over the variational parameters. The lower learning rate prevents unstable gradient updates caused by high-variance score function estimators.
    
- **`constraint=constraints.positive`**: Applies a transformation to scale parameters. This ensures that the scale updates remain valid standard deviations ($\sigma > 0$) throughout gradient optimization, preventing math errors during sampling routines.
    

### 3.5 Convergence Trace Evaluation

Reviewing the step-by-step SVI training trace demonstrates successful optimization:

- **Initialization (Step 0)**:
    
    $$\text{Loss}: 609.37 \quad \mu_{w_0}: -0.0867 \pm 0.8655 \quad \mathbb{E}[\mu_{w_1}]: -0.1423 \pm 0.9793 \quad [base: -0.06, coeff: 0.89]$$
    
- **Convergence (Step 4900)**:
    
    $$\text{Loss}: 62.06 \quad \mu_{w_0}: 1.1272 \pm 0.3437 \quad \mathbb{E}[\mu_{w_1}]: 0.4711 \pm 0.0648 \quad [base: 0.83, coeff: -0.32]$$
    

The optimized variational parameters recover the underlying true values ($true\_w_0 = 1.0, true\_w_1 = 0.5$). The non-zero value of `w1_coeff` ($-0.32$) confirms that the guide successfully tracked the internal parameter correlations.

## 4. Critical Insights & Conceptual Connections

### 4.1 Point Estimates vs. Full Variational Posteriors

Maximum Likelihood Estimation (MLE) or Maximum A Posteriori (MAP) inference provides single point estimates ($\hat{\theta}$). While computationally cheap, point estimates lack uncertainty tracking. In contrast, SVI computes an full distribution over the parameters ($q_\lambda(z)$), which provides built-in confidence intervals for the learned models.

### 4.2 The Core Variance Bottleneck in SVI

- **Score Function Estimator (`Trace_ELBO`)**: Used in vanilla BBVI. It handles both continuous and discrete variables because it does not take derivatives _through_ the sample itself, but rather scales the log-probability of the distribution. However, this leads to significant sample variance, slowing down convergence.
    
- **Pathwise / Path-Derivative Estimator (`TraceGraph_ELBO` / Reparameterization)**: If variables are continuous, we express samples via a deterministic mapping ($z = g_\lambda(\epsilon), \epsilon \sim \mathcal{N}(0, I)$). Taking derivatives _through_ $g_\lambda$ directly leverages the gradient of the log-likelihood surface, which drastically reduces variance.
    

### 4.3 Mode-Seeking Mechanics: The Reverse KL Trap

Maximizing the ELBO minimizes $KL(q \parallel p)$. Because the denominator is the true posterior, if $p(z|x) \to 0$, the ratio $\frac{q(z)}{p(z|x)}$ explodes unless $q(z) \to 0$ rapidly. Consequently, the optimization algorithm penalizes placing probability mass where the true posterior lacks support. This structure explains why Variational Inference under-reports variance and focuses heavily on single local modes when approximating multimodal targets.

# Lecture 8: Learning from Graph Data: Link Prediction and Structural Similarity

## 1. Executive Summary & Core Objectives

- **Core Focus**: This lecture initiates the module on learning from graph and network data, shifting focus from tabular features to relational dependencies encoded within the topology of a network.
    
- **Link Prediction Task**: Recasts the topological question "Where are missing or future edges likely to form?" into a machine learning classification and ranking problem based on structural similarity measures.
    
- **Key Concepts**: Graph representations (adjacency matrices/lists) , degree distributions (power-law behaviors) , local structural metrics (Jaccard, Cosine) , and global random-walk approaches including **PageRank** and **SimRank**.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1 Basic Graph Elements and Topological Properties

A network is formalized as a graph $G = (V, E)$ or $G = (V, E, W)$, where $V = \{v_1, \dots, v_n\}$ represents the vertex (node) set , $E = \{e_1, \dots, e_m\}$ represents the edge (link) set , and $W$ denotes edge annotations such as weights, labels, or signs.

- **Directed Graphs**: Edges are ordered pairs $(u, v)$ mapping asymmetrical relationships (e.g., follower models on Twitter). Nodes possess distinct in-degrees ($d_i^{in}$) and out-degrees ($d_i^{out}$).
    
- **Undirected Graphs**: Edges are unordered pairs mapping symmetrical relationships (e.g., Facebook friendships). Every undirected edge is computationally treated as a bi-directional reciprocal link.
    

#### Degree Distribution and the Power-Law Scale-Free Property

The degree distribution $p_d$ signifies the probability that a randomly selected node has exactly degree $d$:

$$p_d = \frac{n_d}{n}$$

where $n_d$ is the count of vertices with degree $d$.

Real-world web and social networks consistently deviate from a standard Gaussian bell curve, exhibiting a heavy-tailed **Power-Law Distribution** (Scale-Free networks):

$$p_d = \beta d^{-\alpha}$$

Taking the natural logarithm of both sides transforms the non-linear relationship into a linear system suitable for regression analysis:

$$\log(p_d) = \log(\beta) - \alpha \log(d)$$

where $\alpha$ is the power-law exponent (typically falling within the range $2 \le \alpha \le 3$) and $\beta$ is the intercept parameter.

> [!note] A scale-free network implies that small occurrences (nodes with a very small number of connections) are exceptionally common, whereas massive structural hubs (e.g., celebrity accounts on social media with millions of connections) are extremely rare but topologically crucial.

### 2.2 Local Structural Similarity Measures (Structural Equivalence)

Local measures assess the likelihood of a link between node $v_i$ and $v_j$ strictly by evaluating their immediate localized neighborhoods, denoted as $N(v_i)$.

#### Vertex Similarity / Common Neighbors

The simplest baseline measure computes the cardinality of the intersection of the two vertex neighborhoods:

$$Sim_{vertex}(v_i, v_j) = |N(v_i) \cap N(v_j)|$$

#### Jaccard Similarity Coefficient

Normalizes the common neighbors count by dividing it by the cardinality of the union of their neighborhoods, penalizing pairs that are connected to large, unshared hub structures:

$$Sim_{jaccard}(v_i, v_j) = \frac{|N(v_i) \cap N(v_j)|}{|N(v_i) \cup N(v_j)|}$$

#### Cosine Similarity (Ochiai Coefficient)

Computes the geometric mean of the node degrees as the denominator, tracking the cosine angle of the neighborhood vectors in an unweighted adjacency space:

$$Sim_{cosine}(v_i, v_j) = \frac{|N(v_i) \cap N(v_j)|}{\sqrt{|N(v_i)| \cdot |N(v_j)|}}$$

### 2.3 Global Random Walk Frameworks

#### 2.3.1 PageRank (Stationary Markov Chains)

PageRank computes a global prestige score for each node based on the concept of an infinite random surfer moving along a web graph's directed link structure.

Let the random walk be defined over a row-stochastic transition probability matrix $P \in \mathbb{R}^{n \times n}$, where the probability of moving from page $i$ to page $j$ is inversely proportional to the out-degree of the source node:

$$P_{i,j} = \begin{cases} \frac{1}{d^{out}(i)} & \text{if } (i, j) \in E \\ 0 & \text{otherwise} \end{cases}$$

The state distribution at step $t$ is modeled as a discrete-time first-order Markov Chain:

$$q^{(t)} = q^{(t-1)}P$$

A distribution vector $q^*$ is declared **stationary** if it serves as a fixed point under transition operations:

$$q^* = q^*P$$

By definition, $q^*$ represents the principal left eigenvector of the transition matrix $P$ corresponding to the eigenvalue $\lambda = 1$. To guarantee that the power iteration sequence $lim_{t \to \infty} q^{(t)}$ converges uniquely to $q^*$, the Markov chain must be **ergodic**. Ergodicity requires two fundamental properties:

1. **Irreducibility**: Every node must be structurally reachable from every other node in the graph.
    
2. **Aperiodicity**: Transitions cannot occur cyclically across partitioned subsets of nodes.
    

##### Complication: Dangling Pages and Teleportation

Real-world networks frequently contain **dangling pages**—nodes with an out-degree $d^{out}(v) = 0$. These create absorbing sinks that trap the random surfer, breaking row-stochastic mathematical compliance and causing the power iteration to lose mass.

To enforce ergodicity across arbitrary graph structures, the **Google PageRank Matrix** integrates a uniform **teleportation vector**:

$$P_{PageRank} = (1 - \alpha)P + \alpha U$$

where $\alpha \in [0, 1]$ represents the teleportation parameter (or damping factor, conventionally fixed near $0.15$) , indicating the probability that a surfer breaks away from the link structure to jump to a completely random node. $U$ is a dense uniform matrix where $U_{i,j} = \frac{1}{n}$ for all pairs. This modification ensures a strictly positive probability ($P_{ij} > 0$) of transitioning between any two nodes in a single step, guaranteeing a unique stationary solution.

#### 2.3.2 SimRank (Structural Context Proximity)

While PageRank measures absolute global importance , **SimRank** calculates topological similarity between pairs of individual nodes based on the recursive premise that _"two objects are structurally similar if they are referenced by similar objects"_.

Formally, let $I(a)$ represent the set of immediate in-neighbors of node $a$. The SimRank equation is defined as:

$$s(a, b) = \begin{cases} 1 & \text{if } a = b \\ 0 & \text{if } I(a) = \emptyset \text{ or } I(b) = \emptyset \\ \frac{C}{|I(a)||I(b)|} \sum_{i=1}^{|I(a)|} \sum_{j=1}^{|I(b)|} s(I_i(a), I_j(b)) & \text{if } a \neq b \end{cases}$$

where $C \in (0, 1)$ acts as a decay factor or confidence level parameter steering the propagation velocity of structural similarity across edges.

Because the equation defines a mutual recursive relationship, it cannot be evaluated analytically in one pass. It is instead solved using **Power Iteration to a Fixed Point**:

1. **Initialization ($k=0$)**:
    
    $$R_0(a, b) = \begin{cases} 1 & \text{if } a = b \\ 0 & \text{if } a \neq b \end{cases}$$
    
2. **Iterative Update ($k+1$)**:
    
    $$R_{k+1}(a, b) = \frac{C}{|I(a)||I(b)|} \sum_{i=1}^{|I(a)|} \sum_{j=1}^{|I(b)|} R_k(I_i(a), I_j(b)) \quad (\text{for } a \neq b)$$
    

The values $R_k(a, b)$ are monotonically non-decreasing as a function of the iteration index $k$, typically stabilizing within approximately $k \approx 5$ steps.

## 3. Practical Implementation & Self-Study Bridge

An examination of the self-study script (`LinkPredictionStructuralSimilarity.ipynb`) shows how these theoretical structural models are translated into computational architectures using the `networkx` framework.

### 3.1 Local Structural Evaluation Mechanics

Exercise 1 evaluates how a local metric changes when an existing prominent structural edge is dynamically hidden from the network topology.

Python

```
import networkx as ntx

# Target an influential structural connection inside the Zachary Karate Club Network
u, v = 0, 2
G_ex1 = ntx.karate_club_graph()

# Compute local baseline Jaccard coefficient on the true unaltered topology
preds_before = list(ntx.jaccard_coefficient(G_ex1, [(u, v)]))
score_before = preds_before[0][2] # Results in 0.2381

# Simulate an unobserved/missing edge state by removing it from the network
G_ex1.remove_edge(u, v)

# Compute the structural similarity index over the altered topology
preds_after = list(ntx.jaccard_coefficient(G_ex1, [(u, v)]))
score_after = preds_after[0][2] # Results in 0.2632
```

> [!brainstorm]
> 
> Notice that hiding the true edge $(0, 2)$ causes its local Jaccard coefficient to _increase_ from $0.2381$ to $0.2632$. This happens because removing the edge shrinks the denominator (the cardinality of the union $|N(u) \cup N(v)|$) by removing the nodes from each other's immediate neighborhood lists, while leaving their shared mutual connections unchanged. This shows why local metrics are highly sensitive to small variations in topology.

### 3.2 Automated Link Prediction Experiment Pipeline

The self-study implements an empirical pipeline designed to evaluate link prediction over a network by splitting it into training and testing components.

Python

```
import random
import pandas as pd

def run_link_prediction(seed_value, threshold=0.20):
    random.seed(seed_value)
    G = ntx.karate_club_graph()
    original_edges = list(G.edges())
    
    # Define an 80/20 train/test split ratio
    num_to_hide = int(0.20 * len(original_edges)) # 15 edges hidden
    test_edges = random.sample(original_edges, num_to_hide)
    test_set = set((min(u, v), max(u, v)) for u, v in test_edges)
    
    # Construct the Training Graph (masked topology)
    train_G = G.copy()
    train_G.remove_edges_from(test_edges)
    
    # Compute neighborhood structural overlap for all non-existent links
    jaccard_output = ntx.jaccard_coefficient(train_G)
    df_preds = pd.DataFrame(jaccard_output, columns=['node_u', 'node_v', 'similarity'])
    
    # Filter candidates based on structural similarity
    high_sim_predictions = df_preds[df_preds['similarity'] >= threshold]
    
    hits = 0
    for _, row in high_sim_predictions.iterrows():
        pred_pair = (min(row['node_u'], row['node_v']), max(row['node_u'], row['node_v']))
        if pred_pair in test_set:
            hits += 1
            
    hit_rate = (hits / len(high_sim_predictions)) * 100 # Precision
    recall = (hits / len(test_set)) * 100               # Recall/Capture Rate
```

#### Evaluation Traces and Seed Sensitivity

Executing this script over different random seeds shows how variations in masked topologies impact performance:

- **`Seed 10`**: Predictions Made = $144$ | True Positives (Hits) = $6$ | **Precision** = $4.17\%$ | **Recall** = $40.00\%$
    
- **`Seed 42`**: Predictions Made = $125$ | True Positives (Hits) = $2$ | **Precision** = $1.60\%$ | **Recall** = $13.33\%$
    
- **`Seed 2026`**: Predictions Made = $142$ | True Positives (Hits) = $4$ | **Precision** = $2.82\%$ | **Recall** = $26.67\%$
    

The low precision scores ($1.6\% - 4.17\%$) reflect a fundamental challenge in link prediction: the severe **class imbalance** between true hidden edges and the massive pool of all non-existent node pairs in the graph.

### 3.3 Large-Scale Stream Optimization on Benchmark Datasets (CORA)

When transitioning from toy datasets like the Karate Club ($n=34$) to larger real-world graphs like the **CORA citation network** ($n=2,708$, $m=5,278$), scaling challenges emerge. Computing a full Jaccard matrix explicitly requires evaluating $\approx 3.66 \times 10^6$ node pairs, which can easily trigger out-of-memory errors if handled poorly.

The self-study addresses this by using an **on-the-fly streaming generator expression** to compute and filter similarities without allocating a massive intermediate matrix in memory:

Python

```
# Streaming generator optimization to avoid memory bloat
jaccard_gen = ntx.jaccard_coefficient(train_G)

# Filter stream entries dynamically via a generator comprehension
filtered_preds = (
    (u, v, p) for u, v, p in jaccard_gen if p >= 0.25
)

# Instantiate the DataFrame ONLY from elements that pass the filter
df_preds = pd.DataFrame(filtered_preds, columns=['node_u', 'node_v', 'similarity'])
```

#### CORA Benchmark Results

- **Graph Dimensions**: $2,708$ nodes, $5,278$ edges.
    
- **Computation Time**: $5.74$ seconds using streaming generator optimization.
    
- **Evaluation**: Candidates Above Threshold = $8,391$ | Hits Recovered = $127$ out of $1,055$ hidden links | **Precision** = $1.51\%$ | **Recall** = $12.04\%$.
    

## 4. Critical Insights & Conceptual Connections

### 4.1 Local vs. Global Proximity Measures

|**Dimension**|**Local Measures (e.g., Jaccard, Cosine) PDF+ 1**|**Global Frameworks (e.g., PageRank, SimRank) PDF+ 1**|
|---|---|---|
|**Computational Cost**|$\mathcal{O}(n \cdot \langle d \rangle^2)$ — Highly efficient, relying on immediate neighbors.|$\mathcal{O}(K \cdot n^2)$ or $\mathcal{O}(K \cdot m)$ — Requires iterative power methods over the full topology.|
|**Robustness to Manipulation**|Highly vulnerable to **Link Spamming** (creating artificial neighbor structures easily alters scores).|Robust; altering global stationary states requires coordinated structural manipulation across multiple paths.|
|**Coverage Limitations**|**Zero-Similarity Sparsity**: If two nodes do not share common neighbors, local metrics drop to $0$, even if they are closely connected via a short path.|Captures long-range similarities across the entire graph network.|

### 4.2 Ranking vs. Classification in Link Prediction Evaluation

Evaluating link prediction performance solely through simple metrics like accuracy can be misleading due to structural sparsity. For example, if a graph contains $100$ nodes, there are $\approx 4,950$ possible edge positions. If only $150$ true edges exist, a model that predicts "no link" everywhere achieves $96.9\%$ accuracy while failing completely at the actual prediction task.

To address this, real-world link prediction models evaluate rankings using position-aware evaluation metrics:

- **Hit Rate at $K$**: Measures whether a hidden true edge appears anywhere within the top $K$ structural recommendations.
    
- **Mean Reciprocal Rank (MRR)**: Adjusts for the position of correct predictions by averaging the reciprocal of the rank of the first true positive link:
    
    $$MRR = \frac{1}{|M|} \sum_{i=1}^{|M|} \frac{1}{\text{rank}(i)}$$
    

> [!warning] Metrics that ignore list positions (like a simple hit rate threshold) treat all predictions equally. In contrast, rank-aware metrics like MRR penalize models that place true links lower down in the recommendation list.

### 4.3 Structural Sparsity: The Adjacency Matrix Constraint

While an **Adjacency Matrix** $A \in \mathbb{R}^{n \times n}$ provides a clear mathematical representation where $A_{i,j} \in \{0, 1\}$ , it becomes highly inefficient for large, sparse real-world networks. In the CORA network, an adjacency matrix requires storing $2,708^2 \approx 7.33 \times 10^6$ values, yet fewer than $0.15\%$ of those cells contain a $1$.

This explains why graph frameworks use **Adjacency Lists** for sparse computation. An adjacency list acts like an inverted index, storing only the concrete neighbor connections for each node and avoiding the memory overhead of tracking non-existent edges.


# Lecture 9: Link Prediction with Node Embedding Models (Shallow Embeddings)

## 1. Executive Summary & Core Objectives

- **Core Focus**: This lecture introduces graph representation learning via shallow node embedding models, replacing manual feature engineering and heuristic local metrics with continuous optimization paradigms.
    
- **The Representation Paradigm**: recast structural node properties into dense, low-dimensional coordinate spaces ($\mathbb{R}^d$) through an overarching **Encoder-Decoder Framework**.
    
- **Key Frameworks Covered**: Matrix Factorization techniques (**Truncated SVD**, **Funk-SVD**, **Laplacian Eigenmaps**) and Random Walk paradigms (**DeepWalk**, **Node2Vec**).
    
- **Primary Objective**: Formulate algorithms that minimize neighborhood reconstruction losses to dynamically infer hidden relational links, while exposing the fundamental bottlenecks of transductive shallow lookup structures.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1 The Generalized Encoder-Decoder Framework

Graph embedding methods optimize low-dimensional vector representations such that structural proximities in the input graph graph map to geometric proximities in a latent embedding space. This architecture factorizes into two central components:

```
                  ┌────────────────┐
                  │ Input Graph G  │
                  └───────┬────────┘
                          │
                          ▼ (Node u, Node v)
                 ┌──────────────────┐
                 │  Shallow Lookup  │
                 │   Encoder (ENC)  │
                 └────────┬─────────┘
                          │
      ┌───────────────────┴───────────────────┐
      ▼                                       ▼
┌──────────────┐                       ┌──────────────┐
│ Embedding Zu │                       │ Embedding Zv │
└──────┬───────┘                       └──────┬───────┘
       │                                      │
       └──────────────────┬───────────────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Pairwise Score  │
                 │   Decoder (DEC)  │
                 └────────┬─────────┘
                          │
                          ▼ Decoded Score ≈ S[u,v]
                 ┌──────────────────┐
                 │ Structural Loss  │
                 │ Optimization (L) │
                 └──────────────────┘
```

#### 1. The Encoder ($\text{ENC}$)

Maps a discrete node $v \in \mathcal{V}$ into a dense continuous coordinate coordinate vector $\mathbf{z}_v \in \mathbb{R}^d$. In shallow configurations, this is a direct matrix lookup operation:

$$\text{ENC}(v) = \mathbf{Z}[v] = \mathbf{z}_v$$

where $\mathbf{Z} \in \mathbb{R}^{|\mathcal{V}| [cite_start]\times d}$ represents the full weight parameter matrix of trainable hidden parameters.

#### 2. The Decoder ($\text{DEC}$)

Reconstructs pair-specific graph similarities from the latent space embeddings:

$$\text{DEC}(\mathbf{z}_u, \mathbf{z}_v) \approx \mathbf{S}[u,v]$$

where $\mathbf{S}[u,v]$ defines the user-specified ground-truth structural similarity matrix (e.g., Adjacency matrix $\mathbf{A}$, common neighbor scores, or multi-hop transition probabilities).

#### 3. Loss Function Optimization

The parameters inside embedding lookup table $\mathbf{Z}$ are updated iteratively by minimizing a generalized empirical reconstruction loss function over all candidate node pairs in training subset $\mathcal{D}$:

$$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} \ell\left(\text{DEC}(\mathbf{z}_u, \mathbf{z}_v), \mathbf{S}[u,v]\right)$$

### 2.2 Matrix Factorization & Inner Product Methods

#### 2.2.1 Truncated Singular Value Decomposition (SVD)

When treating the decoder explicitly as an inner product operation, the score simplifies to a vector dot product:

$$\text{DEC}(\mathbf{z}_u, \mathbf{z}_v) = \mathbf{z}_u^T \mathbf{z}_v$$

By fixing the target similarity matrix $\mathbf{S} \triangleq \mathbf{A}$ (the input graph's adjacency layout), the matrix optimization objective minimizes the sum of squared errors:

$$\mathcal{L} \approx \|\mathbf{Z}\mathbf{Z}^T - \mathbf{A}\|_2^2$$

Under an exact full SVD configuration, an arbitrary sparse input tensor target matrix $\mathbf{R}$ factorizes into three distinct components:

$$\mathbf{R} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$$

To filter noise and enforce low-dimensional compression, the rank is truncated to the top-$k$ largest singular values along the diagonal of $\mathbf{\Sigma}$, retaining the associated column parameters within left and right singular vectors $\mathbf{U}_k$ and $\mathbf{V}_k^T$.

#### 2.2.2 Funk-SVD Matrix Completion

Standard SVD breaks down when the input matrix contains missing entries. Funk-SVD resolves this computational constraint by evaluating the reconstruction loss _strictly over observed entry indices_ within sparse subset $\mathcal{D}$, letting the model fill in unobserved elements during training:

$$\text{Error} = \|\mathbf{R} - \mathbf{A}\mathbf{B}\|_F^2 = \sum_{(m,u) \in \mathcal{D}} \left(R_{mu} - \sum_{k=1}^K A_{mk} B_{ku}\right)^2$$

To optimize this large-scale system via Stochastic Gradient Descent (SGD), the gradients are evaluated on an isolated random sample $R_{mu}$. Incorporating $L_2$ structural regularization (weight decay parameter $\lambda$) protects against parameter explosion on sparse nodes:

$$\mathcal{L}_{\text{reg}} = \sum_{(m,u) \in \mathcal{D}} \left(R_{mu} - \mathbf{a}_m^T \mathbf{b}_u\right)^2 + \lambda \left(\|\mathbf{A}\|_F^2 + \|\mathbf{B}\|_F^2\right)$$

Taking partial derivatives yields the explicit parameter updates for learning rate $\eta$:

$$A_{mk} \leftarrow A_{mk} + \eta \cdot \left[\left(R_{mu} - \sum_{i=1}^K A_{mi}B_{iu}\right)B_{ku} - \lambda A_{mk}\right]$$

$$B_{ku} \leftarrow B_{ku} + \eta \cdot \left[\left(R_{mu} - \sum_{i=1}^K A_{mi}B_{iu}\right)A_{mk} - \lambda B_{ku}\right]$$

> [!note] To stabilize Funk-SVD before optimization, global network popularity signals must be decoupled from personalized structural alignments. This is achieved by subtracting structural biases:
> 
> $$R_{mu} \leftarrow R_{mu} - \left(\frac{1}{U_m}\sum_{s}R_{ms} + \frac{1}{M_u}\sum_{r}R_{ru} - \frac{1}{N}\sum_{s}\sum_{r}R_{sr}\right)$$
> 
> where $\bar{R}_m$ and $\bar{R}_u$ correspond to the localized row/column structural coordinate means.

#### 2.2.3 Laplacian Eigenmaps

Rather than maximizing dot products, Laplacian Eigenmaps specify the decoder as a squared Euclidean distance metric to minimize separation between strongly linked nodes:

$$\text{DEC}(\mathbf{z}_u, \mathbf{z}_v) = \|\mathbf{z}_u - \mathbf{z}_v\|_2^2$$

$$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} \text{DEC}(\mathbf{z}_u, \mathbf{z}_v) \cdot A[u,v] = \sum_{(u,v) \in \mathcal{D}} A[u,v] \|\mathbf{z}_u - \mathbf{z}_v\|_2^2$$

Applying algebraic properties maps this optimization task directly to a trace maximization problem over the unnormalized graph Laplacian matrix $\mathbf{L}$:

$$\mathcal{L} = 2 \cdot \text{Tr}(\mathbf{Z}^T \mathbf{L} \mathbf{Z}), \quad \text{where } \mathbf{L} = \mathbf{D} - \mathbf{A}$$

Here, $\mathbf{D}$ acts as the diagonal degree matrix ($\mathbf{D}_{ii} = \sum_j W_{ij}$). Low-dimensional layouts are recovered by extracting the eigenvectors associated with the smallest non-zero eigenvalues of $\mathbf{L}$.

### 2.3 Shallow Random Walk Embedding Frameworks

Matrix factorization struggles to capture higher-order, multi-hop structural insights beyond immediate neighbor overlaps. Random walk strategies solve this by optimizing embedding spaces based on co-occurrence probabilities within short random walks.

$$\text{DEC}(\mathbf{z}_u, \mathbf{z}_v) = \mathbf{z}_u^T \mathbf{z}_v \propto P_R(v|u)$$

where $P_R(v|u)$ defines the analytical conditional probability that node $v$ is visited during a random walk sequence initiated at vertex $u$.

#### 2.3.1 The Full Categorical Softmax and the Computational Bottleneck

Using a standard Softmax formulation, the exact conditional probability can be written as:

$$P(v|\mathbf{z}_u) = \frac{\exp(\mathbf{z}_u^T \mathbf{z}_v)}{\sum_{n \in \mathcal{V}} \exp(\mathbf{z}_u^T \mathbf{z}_n)}$$

Maximizing graph likelihood involves minimizing the cross-entropy loss function:

$$\mathcal{L} = \sum_{u \in \mathcal{V}} \sum_{v \in N_R(u)} -\log\left(\frac{\exp(\mathbf{z}_u^T \mathbf{z}_v)}{\sum_{n \in \mathcal{V}} \exp(\mathbf{z}_u^T \mathbf{z}_n)}\right)$$

> [!warning] Computing this loss function exactly is computationally intractable, scaling as $\mathcal{O}(|\mathcal{V}|^2)$ due to the partition function summation over every node in the denominator for each step.

#### 2.3.2 Optimization via Negative Sampling

To scale to large graphs, models swap the dense partition function for a binary classification objective using negative sampling:

$$\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} -\log\left(\sigma(\mathbf{z}_u^T \mathbf{z}_v)\right) - \gamma \sum_{i=1}^k \log\left(\sigma(-\mathbf{z}_u^T \mathbf{z}_{n_i})\right)$$

where $\sigma(x) = \frac{1}{1 + e^{-x}}$, $\gamma$ is a scaling bias weight, and $k$ controls the number of non-neighbor noise nodes sampled from a unigram distribution.

#### 2.3.2 DeepWalk vs. Node2Vec Walk Strategies

The definition of the node neighborhood $N_R(u)$ depends on the chosen sampling strategy:

- **DeepWalk**: Draws samples using a uniform row-stochastic random walk transition strategy. Each step chooses an adjacent vertex with equal probability:
    
    $$P(v_i | v_{i-1}) = \frac{1}{d(v_{i-1})}$$
    
- **Node2Vec**: Implements a second-order biased random walk framework to balance local structural context (**Breadth-First Search / BFS**) and macro global configurations (**Depth-First Search / DFS**).
    

When a walk traverses edge $(t, v)$ and stands at node $v$, the unnormalized transition probability to a subsequent neighbor $x$ is scaled by a dynamic modifier $\alpha_{pq}(t, x)$:

$$\pi_{vx} = \alpha_{pq}(t, x) \cdot W_{vx}$$

The bias modifier $\alpha_{pq}(t, x)$ is parameterized by a **return parameter $p$** and an **in-out parameter $q$**:

$$\alpha_{pq}(t, x) = \begin{cases} \frac{1}{p} & \text{if } d_{tx} = 0 \quad \text{(Encourages returning to previous node } t\text{)} \\ 1 & \text{if } d_{tx} = 1 \quad \text{(Maintains immediate neighborhood distance)} \\ \frac{1}{q} & \text{if } d_{tx} = 2 \quad \text{(Encourages moving outward to unvisited nodes)} \end{cases}$$

where $d_{tx}$ represents the shortest path distance between nodes $t$ and $x$.

- **Low Return Parameter $p$ ($1/p$)**: Constrains the walk sequence to a local area, encouraging a BFS-like view that clusters local community structures.
    
- **Low In-Out Parameter $q$ ($1/q$)**: Drives the sequence outward across long-range structural paths, encouraging a DFS-like view that uncovers structural roles across the network.
    

## 3. Practical Implementation & Self-Study Bridge

An analysis of the practical self-study (`LinkPredictionsOnShallowEmbeddings.ipynb`) shows how these theoretical representation frameworks are implemented using graph toolkits.

### 3.1 Mapping Spatial Layouts to Node Embeddings

The self-study illustrates a direct coordinate mapping method, extracting two-dimensional structural features from a force-directed layout algorithm.

Python

```python
import networkx as ntx
import numpy as np

# Load the classic Zachary Karate Club social graph network
zachary = ntx.karate_club_graph()

# Compute a 2D spring embedding layout (force-directed optimization)
layout = ntx.spring_layout(zachary, seed=0)

# Instantiate the shallow lookup matrix parameter tensor Z
X = np.zeros((zachary.order(), 2))
for i in range(zachary.order()):
    X[i, :] = layout[i]
```

This procedure creates a concrete embedding matrix $\mathbf{Z} \in \mathbb{R}^{34 \times 2}$ where each row stores the dense latent parameters for a node.

### 3.2 Evaluation Strategy: The Edge-Masking Protocol

To validate link prediction accuracy, the implementation masks a subset of true edges during training and evaluates the decoder's ability to recover them.

Python

```
import random

random.seed(10)
# Step 1: Uniformly sample a 20% validation split from true edge coordinates
sampled_edges = random.sample(list(zachary.edges), round(0.2 * zachary.number_of_edges()))

# Step 2: Mask/Remove these validation links to isolate the training sub-graph
for uN, vN in sampled_edges:
    zachary.remove_edge(uN, vN)
```

By removing these edges, the network layout adapts to an incomplete training topology. When the force-directed layout is re-run (`layoutN`), nodes that lost their connections repulse each other and separate spatially.

### 3.3 Reconstructing Predictions via Dot-Product Decoders

The dot product decoder evaluates candidate pairs across the revised spatial configuration:

Python

```python
# Compute inner product similarity matrices across the embedding representations
SimEmbPositionXN = [[0 for _ in range(zachary.order())] for _ in range(zachary.order())]

for i in range(zachary.order()):
    for j in range(zachary.order()):
        # Decoder logic mapping: DEC(zi, zj) = zi^T * zj
        SimEmbPositionXN[i][j] = np.dot(XN[i, :], X[j, :])
```

Evaluating the dot product over masked links shows reduced scores because the underlying spring layout algorithm forces unlinked vertices apart, reducing their vector alignment.

### 3.4 Top-K Rank-Aware Hit Rate Pipeline

The self-study measures predictive accuracy using a rank-aware target evaluation function loop:

Python

```python
k = 10  # Define target ranking evaluation cutoff range threshold
countHits = 0

for u, v in sampled_edges:
    LinkPredictionList = SimEmbPositionXN[u]
    # Extract the indices that sort the similarities in ascending order
    sort_index = np.argsort(LinkPredictionList)
    
    # Calculate the sorted rank index position of hidden node v
    position_in_the_list = list(sort_index).index(v)
    
    # If the hidden link falls within the top K validation tier, register a hit
    if position_in_the_list < k - 1:
        countHits += 1

HitRate = countHits / len(sampled_edges)  # Evaluates to 0.4375 (43.75% retrieval)
```

> [!brainstorm]
> 
> While this top-$K$ hit rate successfully captures precision within a localized ranking window, it does not distinguish where the correct predictions fall inside that window. For example, a hidden edge recovered at rank 1 is given the same weight as an edge recovered at rank 9. For more rigorous evaluation, ranking metrics like Mean Reciprocal Rank (MRR) or Normalized Discounted Cumulative Gain (NDCG) should be prioritized instead.

### 3.5 Scaling Beyond Toy Geometries to Production Architectures

While the notebook utilizes an illustrative 2D coordinate spring mapping space, production workflows scale these pipelines using dedicated matrix backends:

#### 1. PyTorch Low-Rank SVD Optimization

For large, sparse graphs, full matrix factorization becomes a performance bottleneck. Using `torch.svd_lowrank`, PyTorch computes truncated singular value compositions without allocating memory for full dense decompositions:

Python

```python
import torch

# Obtain sparse adjacency tensor representation
adj_matrix = ntx.to_scipy_sparse_array(zachary)
values = adj_matrix.data
indices = np.vstack((adj_matrix.row, adj_matrix.col))

i = torch.LongTensor(indices)
v = torch.FloatTensor(values)
shape = adj_matrix.shape

sparse_tensor = torch.sparse_coo_tensor(i, v, torch.Size(shape))

# Direct low-rank estimation function filtering top singular factors
U, S, V = torch.svd_lowrank(sparse_tensor, q=20)
# Node embeddings matrix extraction
Z_embeddings = torch.mm(U, torch.diag(S))
```

#### 2. PyTorch Geometric Native Node2Vec Implementation

For random walk frameworks, the `torch_geometric.nn.models.Node2Vec` module provides highly optimized sampling engines that automate negative sampling loss optimization:

Python

```python
from torch_geometric.nn.models import Node2Vec

# Initialize PyG Node2Vec framework instance configurations
model = Node2Vec(
    edge_index=torch.tensor(list(zachary.edges)).t().contiguous(),
    embedding_dim=64,
    walk_length=20,
    context_size=10,
    walks_per_node=10,
    p=1.0,  # Return parameter
    q=0.5,  # In-out parameter (Biased towards global DFS paths)
    sparse=True
)

# Access embedding parameters using PyG lookup optimizations
loader = model.loader(batch_size=128, shuffle=True, num_workers=4)
optimizer = torch.optim.SparseAdam(model.parameters(), lr=0.01)

# Training loops directly execute gradient backpropagation through negative bounds
```

## 4. Critical Insights & Conceptual Connections

### 4.1 Foundations and Core Limitations of Shallow Embeddings

Shallow embedding models map each node to an isolated row in a parameter lookup matrix. While mathematically clear, this architecture introduces three significant bottlenecks:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SHALLOW EMBEDDING LOOKUP LIMITATIONS                 │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Parameter Non-Sharing          │ 2. Feature Insensitivity           │
├───────────────────────────────────┼────────────────────────────────────┤
│                                   │                                   │
│      Embedding Lookup Matrix      │       Discrete Graph Space         │
│               Node v              │            Node Attributes         │
│         ┌───────────────┐         │               ┌───────┐            │
│       1 │               │         │        Node v │ text  │            │
│       2 │               │         │               └───────┘            │
│         ├───────────────┤         │         [Isolated From Table]      │
│     v   │  [z1, z2, z3] │◀────────┼───┐                                │
│         ├───────────────┤         │   │ No structural inductive link   │
│         │               │         │   │ to carry continuous node labels│
│       V │               │         │   │                                │
│         └───────────────┘         │   │                                │
│                                   │   │                                │
│  * Parameters scale linearly with │   │ 3. Transductive Limitation     │
│    graph size: O(|V| * d)         │   │                                │
│  * No shared neural weights across│   │   * Out-of-Sample Node (v_new) │
│    distinct node entries          │   │     cannot be parsed.          │
│                                   │   │   * Requires a full retrain    │
│                                   │   │     execution step.            │
└───────────────────────────────────┴───┴────────────────────────────────┘
```

1. **No Weight Parameter Sharing**: Each node vector is learned independently, meaning no parameters are shared across nodes. The total parameters scale linearly with the number of vertices ($\mathcal{O}(|\mathcal{V}| \cdot d)$), leading to high memory overhead on large graphs.
    
2. **Inability to Leverage Node Features**: The encoder depends entirely on discrete node indices. As a result, internal node attributes (such as textual profiles, demographic fields, or multi-modal vectors) cannot be integrated into the representation space.
    
3. **The Transductive Bottleneck**: Shallow architectures are fundamentally transductive, meaning they can only generate embeddings for nodes that were present during the training phase. If an out-of-sample vertex $v_{\text{new}}$ is added to the graph later, the model cannot infer its embedding without re-running the entire optimization pipeline over the expanded topology.
    

### 4.2 Mathematical Equivalence: Random Walks and Matrix Factorization

A key conceptual breakthrough in graph representation learning is the formal proof that **random-walk objectives are mathematically equivalent to factorizing a shifted graph proximity matrix**.

Specifically, optimizing DeepWalk's negative sampling loss yields an implicit factorization of a matrix tracking multi-hop transition probabilities (known as the _NetMF_ framework theorem):

$$\mathbf{M} = \log\left(\text{vol}(G)\left(\frac{1}{T}\sum_{r=1}^T \mathbf{P}^r\right)\mathbf{D}^{-1}\right) - \log(\gamma)$$

where $\mathbf{P} = \mathbf{D}^{-1}\mathbf{A}$ represents the base transition matrix, $\text{vol}(G)$ is the volume of the graph, and $\gamma$ acts as the negative sample size scale bias. This alignment reveals that matrix decomposition and random walk context streams optimize the same underlying structural geometries.

### 4.3 Regularization and Bias Correction Dynamics

#### Overfitting Risks in Sparse Adjacency Reconstruction

Because real-world graph matrices are typically highly sparse, models like Funk-SVD are vulnerable to overfitting on observed rows and columns. Nodes with very low degrees can easily experience vector explosions during stochastic gradient updates.

Applying an $L_2$ regularization penalty ($\lambda$) restrains the parameters, preventing the model from fitting to local topological noise and encouraging smoother geometric variations across the latent space.

#### Structural Popularity vs. Personalized Preferences

In link prediction and recommendation tasks, raw adjacency scores are often dominated by high-degree structural hubs (e.g., highly cited baseline papers or viral videos).

Explicitly subtracting user, item, and global mean biases during pre-processing ensures that the inner product decoder isolates _true personalized structural alignments_ rather than simply reflecting the high connectivity of popular hub nodes.

### 4.4 Analytical Comparison of Structural Link Models

|**Dimension**|**Local Topological Overlap (e.g., Jaccard, Cosine)**|**Matrix Factorization Methods (e.g., SVD, Funk-SVD)**|**Shallow Random Walk Models (e.g., DeepWalk, Node2Vec)**|
|---|---|---|---|
|**Algorithmic Context**|Hand-crafted neighborhood heuristics.|Deterministic coordinate dimension reductions.|Stochastic sampling and neighborhood optimization.|
|**Structural Reach**|Restricted to immediate, localized neighborhoods.|Multi-hop factorization across the full matrix.|Dynamic multi-hop reach via biased walk parameters.|
|**Out-of-Sample Handling**|**Inductive**: Can evaluate any node pair on the fly using active neighborhood lists.|**Transductive**: Requires computing fresh dimensions across new matrix variants.|**Transductive**: Out-of-sample entries require a full retraining pass.|
|**Primary Failure Modes**|**Sparsity Constraints**: Fails when nodes share no immediate neighbors.|**Missingness Constraints**: Standard SVD degrades under severe missing entries.|**Variance Bottleneck**: High sample variance slows convergence rates.|
# Lecture 10: Link Prediction with Graph Neural Networks

## 1. Executive Summary & Core Objectives

- **Core Focus**: This lecture lifts the link prediction task from local topological heuristics and shallow node embeddings to advanced deep learning architectures using **Graph Neural Networks (GNNs)**.
    
- **The Paradigm Shift**: Traditional shallow embedding models suffer from significant limitations: they do not share parameters across nodes, fail to leverage native node attributes, and are strictly transductive (unable to compute embeddings for out-of-sample nodes added post-training). GNNs solve these issues by replacing lookup tables with generalized, differentiable encoders that learn deep structural representations based on both graph topology and node features.
    
- **Key Mechanisms**: This module details the general formalization of the **Message Passing** framework , examines neighborhood aggregation extensions (such as symmetric normalization, set pooling, and neighborhood attention) , and explores structural updates designed to mitigate the effects of over-smoothing.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1 The Generalized Message Passing Framework

GNNs process graph-structured data by iteratively propagating and transforming feature vectors across localized neighborhoods. Let $G = (V, E)$ be a graph where each vertex $u \in V$ is initially assigned an input feature vector $h_u^{(0)} = x_u$. The generalized message passing update rule at iteration (or layer) $k+1$ is defined as:

$$h_u^{(k+1)} = \text{UPDATE}^{(k)} \left( h_u^{(k)}, \text{AGGREGATE}^{(k)} \left( \{ h_v^{(k)}, \forall v \in \mathcal{N}(u) \} \right) \right)$$

Where $\mathcal{N}(u)$ denotes the set of immediate spatial neighbors of node $u$, and $m_{\mathcal{N}(u)}^{(k)} = \text{AGGREGATE}^{(k)}(\dots)$ is the aggregated neighborhood "message" vector. Both $\text{UPDATE}$ and $\text{AGGREGATE}$ must be parameterized, differentiable functions.

Unfolding this message passing sequence for $K$ iterations generates a local computation graph configured as a tree structure around the target node. After $K$ layers of message passing, the final node embedding is extracted from the output vector:

$$\text{ENC}(u) = z_u = h_u^{(K)}$$

### 2.2 The Basic Graph Neural Network Layer (Vanilla GCN)

In a baseline structural setup, the aggregation step computes a sum over neighbor features, and the update function applies a linear transformation followed by an element-wise activation function:

$$h_u^{(k+1)} = \sigma \left( W_{\text{self}}^{(k)} h_u^{(k)} + W_{\text{neigh}}^{(k)} \sum_{v \in \mathcal{N}(u)} h_v^{(k)} + b^{(k)} \right)$$

Where $W_{\text{self}}^{(k)}, W_{\text{neigh}}^{(k)} \in \mathbb{R}^{d^{(k)} \times d^{(k-1)}}$ are trainable parameter weight matrices, $b^{(k)} \in \mathbb{R}^{d^{(k)}}$ is a bias vector, and $\sigma(\cdot)$ is an element-wise non-linearity (e.g., Sigmoid, Tanh, or ReLU).

#### Explicit Graph-Level Self-Loop Matrix Formulation

Instead of handling self-updates and neighbor updates through separate weight matrices, we can add self-loops directly to the structural adjacency layout:

$$\mathcal{N}(u) \leftarrow \mathcal{N}(u) \cup \{u\}$$

This simplifies the node-level operation into a single unified aggregation step. Let $A \in \mathbb{R}^{|V| \times |V|}$ be the baseline binary adjacency matrix, $I \in \mathbb{R}^{|V| \times |V|}$ be the identity matrix tracking self-loops, and $H^{(t-1)} \in \mathbb{R}^{|V| \times d^{(t-1)}}$ be the full node feature matrix at step $t-1$. The integrated graph-level matrix propagation step is defined as:

$$H^{(t)} = \sigma \left( (A + I) H^{(t-1)} W^{(t)} \right)$$

### 2.3 Advanced Neighborhood Aggregation Extensions

#### 2.3.1 Neighborhood Normalization

Relying on a basic summation operation scales the message vectors proportionally with node degrees, which can cause numerical instability and optimization failures in graphs with highly skewed degree distributions. To fix this, we can normalize the neighborhood messages using one of two approaches:

- **Node-Degree Average Aggregator**:
    
    $$m_{\mathcal{N}(u)} = \frac{\sum_{v \in \mathcal{N}(u)} h_v}{|\mathcal{N}(u)|}$$
    
- **Symmetric Graph Convolutional Normalization**:
    
    $$m_{\mathcal{N}(u)} = \sum_{v \in \mathcal{N}(u)} \frac{h_v}{\sqrt{|\mathcal{N}(u)||\mathcal{N}(v)|}}$$
    

> [!note] Normalization is highly valuable when localized node attributes provide stronger predictive signals than the underlying graph structure, or when the network exhibits wide variations in node degrees.

#### 2.3.2 Permutation-Invariant Set Aggregators

Because the neighborhood $\mathcal{N}(u)$ is an unordered set, the aggregation function must be permutation-invariant to ensure consistent outputs regardless of node ordering.

- **Set Pooling (Deep Sets)**: Modeled as a universal set function approximator using Multi-Layer Perceptrons (MLPs):
    
    $$m_{\mathcal{N}(u)} = \text{MLP}_{\theta} \left( \sum_{v \in \mathcal{N}(u)} \text{MLP}_{\phi}(h_v) \right)$$
    
- **Janossy Pooling**: Evaluates the canonical output by averaging predictions across a randomly sampled subset of permutations $\Pi$:
    
    $$m_{\mathcal{N}(u)} = \text{MLP}_{\theta} \left( \frac{1}{|\Pi|} \sum_{\pi \in \Pi} \rho_{\phi} \left( h_{v_1}, h_{v_2}, \dots, h_{v_{|\mathcal{N}(u)|}} \right)_{\pi} \right)$$
    

#### 2.3.3 Neighborhood Attention (Graph Attention Networks - GAT)

Rather than treating all neighbors equally or scaling contributions strictly by node degrees, attention mechanisms dynamically compute the relative importance of each incoming edge:

$$m_{\mathcal{N}(u)} = \sum_{v \in \mathcal{N}(u)} \alpha_{u,v} h_v$$

The attention coefficient $\alpha_{u,v}$ represents a softmax distribution over the localized spatial neighborhood:

$$\alpha_{u,v} = \frac{\exp \left( \text{LeakyReLU} \left( \mathbf{a}^T \left[ W h_u \parallel W h_v \right] \right) \right)}{\sum_{v' \in \mathcal{N}(u)} \exp \left( \text{LeakyReLU} \left( \mathbf{a}^T \left[ W h_u \parallel W h_{v'} \right] \right) \right)}$$

Where $\mathbf{a} \in \mathbb{R}^{2d'}$ is a learnable attention vector, $W \in \mathbb{R}^{d' \times d}$ is a shared linear transformation matrix, and $\parallel$ denotes vector concatenation.

### 2.4 Mitigating Over-Smoothing with Advanced Updates

> [!warning]
> 
> **The Over-Smoothing Bottleneck**: Stacking multiple basic message passing layers often causes node representations to converge toward uniform values across the network. As the number of iterations increases, the aggregated embeddings become dominated by global neighborhood averages, washing out node-specific features.

To preserve individual node identities over deeper network horizons, standard updates can be replaced with structural architectures that explicitly maintain historical states.

- **Concatenation-Based Update**: Appends the prior layer's target state directly onto the newly aggregated neighborhood message vector:
    
    $$\text{UPDATE}_{\text{concat}} \left( h_u, m_{\mathcal{N}(u)} \right) = \left[ \text{UPDATE}_{\text{base}} \left( h_u, m_{\mathcal{N}(u)} \right) \parallel h_u \right]$$
    
- **Gated Linear Interpolation Update**: Employs learnable gating vectors to smoothly balance the neighbor contributions against the current internal node representation:
    
    $$\text{UPDATE}_{\text{interpolate}} \left( h_u, m_{\mathcal{N}(u)} \right) = \alpha_1 \circ \text{UPDATE}_{\text{base}} \left( h_u, m_{\mathcal{N}(u)} \right) + \alpha_2 \circ h_u$$
    
    Where $\alpha_1, \alpha_2 \in [0,1]^d$ represent learnable gating parameters satisfying $\alpha_2 = 1 - \alpha_1$, and $\circ$ denotes the Hadamard element-wise product.
    

## 3. Practical Implementation & Self-Study Bridge

An analysis of the practical self-study framework (`LinkPredictionWithGNN.ipynb`) highlights how generalized message-passing mathematics translate into concrete computational layers using the **PyTorch Geometric (PyG)** library.

### 3.1 Custom Message Passing Subclass Construction

The custom `GCNConv` layer subclasses PyG's native `MessagePassing` module, showcasing the execution mechanics of spatial graph convolutions.

Python

```
class GCNConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        # Configure the pipeline to use an explicit 'add' aggregation step
        super().__init__(aggr='add')  
        
        # Define the parameter weight matrix for linear transformations
        self.lin = Linear(in_channels, out_channels, bias=False)
        
        # Configure the element-wise non-linear activation function
        self.nonlin = nn.ReLU()

    def forward(self, x, edge_index):
        # Step 1: Inject self-loops into the topological layout matrix (A + I)
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        # Step 2: Apply the linear transformation to the input feature matrix
        x = self.lin(x)

        # Step 3: Map the transformed vectors through the activation function
        x = self.nonlin(x)
        
        # Step 4: Propagate messages across the graph topology
        out = self.propagate(edge_index, x=x)
        return out
```

#### Code-to-Theory Alignment Analysis

1. `super().__init__(aggr='add')`: Sets the baseline aggregation operator to a sum, mirroring the unnormalized spatial pooling definition: $m_{\mathcal{N}(u)} = \sum h_v$.
    
2. `add_self_loops(edge_index, ...)`: Updates the adjacency representation to include self-loops, matching the matrix formulation $A + I$ discussed on slide page 23.
    
3. `self.lin(x)` followed by `self.propagate(...)`: Implements the vanilla propagation sequence. Features are linearly transformed _before_ being distributed across neighbor coordinates via the underlying message-passing pipeline.
    

### 3.2 Graph-Level Network Container and Link Predictor Decoder

The container class `MyGnn` dynamically links multiple message passing convolutions together and terminates with a pairwise inner-product decoder to evaluate edge probabilities.

Python

```
class MyGnn(nn.Module):
    def __init__(self, dims):
        super().__init__()
        self.layers = torch.nn.ModuleList()

        # Chain spatial message-passing blocks based on the configuration array
        for d in range(len(dims) - 2):
            self.layers.append(GCNConv(dims[d], dims[d+1]))
            
        # Append a final linear transformation to align the dimensions
        self.layers.append(nn.Linear(dims[-2], dims[-1], bias=True))
        
        # Terminate with a Sigmoid activation to map scores to probabilities
        self.layers.append(nn.Sigmoid())

    def forward(self, x, graph, batch):
        h = x
        for l in self.layers:
            if isinstance(l, GCNConv):
                h = l.forward(h, graph)
            else:
                h = l.forward(h)

        # Pairwise Dot Product Decoder: Reconstructs the full similarity matrix
        dot_pr = torch.matmul(h, torch.transpose(h, 0, 1))
        return dot_pr
```

#### The Decoder Integration

The line `torch.matmul(h, torch.transpose(h, 0, 1))` implements the dot product decoder layer defined on slide page 34:

$$\text{DEC}\left( h_u^{(k)}, h_v^{(k)} \right) = h_u^{(k)T} h_v^{(k)}$$

This operation parallelizes similarities across all pairs, evaluating the reconstruction loss against the target binary adjacency matrix mask.

### 3.3 Comparative Evaluation Pipeline: Karate Club vs. CORA Network

The experimental pipeline evaluates link prediction accuracy across different dataset dimensionalities, configurations, and hidden layer shapes.

Python

```
# Extract the binary adjacency mask to serve as the ground-truth target
A = ntx.adjacency_matrix(zachary).todense()
target = torch.tensor(np.minimum(A, np.ones(A.shape)), dtype=torch.float)

# Optimize parameters using Mean Squared Error (MSE) loss
loss_fn = nn.MSELoss(reduction='mean')
optimizer = torch.optim.Adam(gnn.parameters(), lr=0.001)
```

#### Empirical Performance Summary Metrics

The model was tested across varying structural layouts, depths, and spatial resolutions, yielding the following HitRate@10 performance marks:

- **Karate Club Graph (2 Input Dimensionality Features)**:
    
    - Shape `[2, 3, 2]` (1 Convolution Layer $\rightarrow$ 1-Hop Receptive Reach): **HitRate@10 = $25.0\%$**
        
    - Shape `[2, 5, 2]` (1 Convolution Layer $\rightarrow$ 1-Hop Receptive Reach): **HitRate@10 = $25.0\%$**
        
    - Shape `[2, 8, 4, 2]` (2 Convolution Layers $\rightarrow$ 2-Hop Receptive Reach): **HitRate@10 = $41.7\%$**
        

> [!brainstorm] **Receptive Field Expansion Insights**: Scaling the model layout from a single convolution layer (`[2,3,2]`) to a two-layer message passing sequence (`[2,8,4,2]`) improves accuracy from $25.0\%$ to $41.7\%$. This performance boost occurs because stacking convolutions expands the local receptive field to capture 2-hop neighbor relationships, giving the link predictor access to broader structural context.

- **CORA Citation Network ($1,433$ Bag-of-Words Content Feature Coordinates)**:
    
    - Layout Configuration `[1433, 512, 128, 64]`: **HitRate@10 = $0.50\%$**
        
    - Layout Configuration `[1433, 256, 64, 32]`: **HitRate@10 = $0.60\%$**
        

The low retrieval rates on the CORA network highlight a critical limitation of the unnormalized baseline implementation (`aggr='add'`). Without symmetric degree normalization, high-degree hub nodes dominate the summation steps, leading to gradient explosion and optimization failures on large graphs.

## 4. Critical Insights & Conceptual Connections

### 4.1 Feature Integration Paradigms: Content vs. Structure

Shallow embedding models operate transductively because they map fixed node indices to coordinate lookups, ignoring internal node attributes. GNNs solve this by accepting arbitrary initial feature vectors ($h_u^{(0)} = x_u$), enabling a variety of inductive modeling approaches:

- **Content-Driven Features**: Initializing vectors with rich textual, attribute, or profile indicators (e.g., CORA's $1,433$-dimensional bag-of-words arrays) allows the model to align structural propagation directly with node content features.
    
- **Structural/Identity Baseline Profiles**: In the absence of native node attributes, graphs can be parameterized using structural signals like node statistics (degrees, centrality metrics) or one-hot identity vectors. However, relying on one-hot identity dimensions ties the parameter dimensions to a fixed graph size, reverting the model to a transductive framework that cannot generalize to unseen nodes.
    

### 4.2 Receptive Fields: Convolutions in CNNs vs. GNNs

The iterative aggregation of neighborhood features across multiple GNN layers shares a direct conceptual connection with localized spatial kernel filters in Convolutional Neural Networks (CNNs).

```
 ┌──────────────────────────────────────────┐     ┌──────────────────────────────────────────┐
 │       2D REGULAR CNN GRID CONVOLUTION    │     │    GRAPH NEURAL NETWORK CONVOLUTION      │
 ├──────────────────────────────────────────┤     ├──────────────────────────────────────────┤
 │                                          │     │                                          │
 │         ┌───┬───┬───┐                    │     │                   (Node v1)              │
 │         │   │   │   │                    │     │                      │                   │
 │         ├───┼───┼───┤                    │     │                      ▼                   │
 │         │   │ X │   │                    │     │      (Node v2) ──► Target ◄── (Node v3)  │
 │         ├───┼───┼───┤                    │     │                      ▲                   │
 │         │   │   │   │                    │     │                      │                   │
 │         └───┴───┴───┘                    │     │                   (Node v4)              │
 │                                          │     │                                          │
 │  * Fixed, rigid grid neighborhood        │     │  * Non-Euclidean, irregular structure    │
 │  * Spatial alignment defines coordinates  │     │  * Permutation-invariant aggregations     │
 │  * Fixed parameter footprint per pixel   │     │  * Shared parameters across all vectors  │
 └──────────────────────────────────────────┘     └──────────────────────────────────────────┘
```

However, while a CNN operates over rigid, regular grids where spatial coordinates dictate order, a GNN functions within irregular, non-Euclidean spaces. GNN layers must handle neighborhoods of varying sizes while maintaining permutation invariance, using shared parameter matrices ($W$) to extract localized structural patterns across arbitrary topologies.

### 4.3 Structural Comparisons of Link Prediction Architectures

| **Evaluation Dimension**     | **Local Topological Overlap Heuristics (Lecture 8)**                           | **Shallow Embedding Models (Lecture 9)**                                                 | **Graph Neural Network Architectures (Lecture 10)**                                |
| ---------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Model Structure**          | Fixed mathematical formulas; no parameter learning.                            | Low-dimensional coordinate matrix lookups ($Z$).                                         | Deep neural network propagation layers ($W$).                                      |
| **Feature Integration**      | Completely ignores node-level content features.                                | Incapable of utilizing continuous node attributes.                                       | Dynamically integrates graph topology with node attributes.                        |
| **Inductive Generalization** | **Inductive**: Evaluates any pair on the fly using active neighborhood lists.  | **Transductive**: Cannot infer embeddings for out-of-sample nodes.                       | **Inductive**: Computes representations for unseen nodes via learned weights.      |
| **Primary Failure Modes**    | **Zero-Similarity Sparsity**: Drops to zero if no common neighbors are shared. | **Parameter Explosion**: Scalability scales linearly with graph size $\mathcal{O}V\cdot$ | **Over-Smoothing**: Representations risk turning uniform over deep layer horizons. |

# Lecture 11: Node and Graph Classification

## 1. Executive Summary & Core Objectives

This lecture covers the paradigms of **Node Classification** and **Graph Classification**, building upon prior graph representation learning techniques. The core objective is to leverage both graph topology and node feature spaces to predict discrete categories for individual nodes within a single network, or across entirely distinct graph instances.

Key themes include:

- Transitioning from localized neighborhood aggregation to full **Transformer architectures** via multi-head graph attention mechanisms.
    
- Scaling graph embeddings into global metrics using advanced **Graph Pooling** and **Graph Coarsening** strategies.
    
- Contrasting traditional transductive relational learning algorithms, such as **Label Propagation** and **Iterative Classification (ICA)**, with modern deep inductive Graph Neural Networks (GNNs).
    

## 2. Theoretical Foundations & Mathematical Models

### Neighborhood Attention Mechanics

Traditional GNN aggregators treat neighbor contributions uniformly or scale them solely based on rigid structural properties like node degrees (e.g., GCN). **Neighborhood Attention** dynamically weights neighbor influence according to downstream task relevance.

The localized message aggregation vector $m_{\mathcal{N}(u)}$ for a target node $u$ is given by:

$$m_{\mathcal{N}(u)}=\sum_{v\in \mathcal{N}(u)}\alpha_{u,v}h_{v}$$

Where $\mathbf{h}_v$ represents the hidden feature representation of neighbor node $v$. The attention coefficient $\alpha_{u,v}$ defines the relative importance of node $v$ to node $u$.

#### Attention Formulations

1. **GAT Concatenation Variant:**
    
    $$\alpha_{u,v}=\frac{\exp\left(\mathbf{a}^{T}\left[\mathbf{W}\mathbf{h}_{u}\oplus \mathbf{W}\mathbf{h}_{v}\right]\right)}{\sum_{v^{\prime}\in \mathcal{N}(u)}\exp\left(\mathbf{a}^{T}\left[\mathbf{W}\mathbf{h}_{u}\oplus \mathbf{W}\mathbf{h}_{v^{\prime}}\right]\right)} $$
    
    Where $\mathbf{a}$ is a learnable parameter vector, $\mathbf{W}$ is a shared linear transformation matrix, and $\oplus$ denotes concatenation.
    
2. **Bilinear/Dot-Product Variant:**
    
    $$\alpha_{u,v}=\frac{\exp\left(\mathbf{h}_{u}^{T}\mathbf{W}\mathbf{h}_{v}\right)}{\sum_{v^{\prime}\in \mathcal{N}(u)}\exp\left(\mathbf{h}_{u}^{T}\mathbf{W}\mathbf{h}_{v^{\prime}}\right)}$$
    
3. **Multi-Layer Perceptron (MLP) Variant:**
    
    $$\alpha_{u,v}=\frac{\exp\left(\text{MLP}(\mathbf{h}_{u},\mathbf{h}_{v})\right)}{\sum_{v^{\prime}\in \mathcal{N}(u)}\exp\left(\text{MLP}(\mathbf{h}_{u},\mathbf{h}_{v^{\prime}})\right)}$$
    

### Multi-Head Attention & Transformer Integration

To stabilize learning and capture orthogonal contextual relationships, neighborhood attention extends to **Multi-Head Attention**. Here, $K$ independent attention heads compute separate message streams that are subsequently concatenated:

$$m_{\mathcal{N}(u)}=\left[\mathbf{a}_{1}\oplus \mathbf{a}_{2}\oplus \dots \oplus \mathbf{a}_{K}\right]$$

$$\mathbf{a}_{k}=\mathbf{W}_{k}\sum_{v\in \mathcal{N}(u)}\alpha_{u,v,k}\mathbf{h}_{v}$$

This direct mapping links graph domains to standard **Transformer Architectures**. In standard sequence text transformers, self-attention maps dependencies across all tokens arbitrarily. GNN attention explicitly restricts this context to the localized graph neighborhood structure $\mathcal{N}(u)$.

### Graph Embedding Aggregation & Pooling

To solve **Graph Classification** tasks, variable-sized collections of node embeddings must be compressed into a static global graph vector $\mathbf{z}_{\mathcal{G}}$.

#### Flat Pooling

- **Sum/Mean Aggregation:**
    
    $$\mathbf{z}_{\mathcal{G}}=\frac{\sum_{u\in\mathcal{V}}\mathbf{z}_{u}}{f_{n}(|\mathcal{V}|)} $$
    
    While computationally trivial, flat pooling strips away structural hierarchies and is mostly effective for small graph boundaries.
    

#### Hierarchical Attention & Recurrent Pooling

By integrating an LSTM cells with soft-attention, graph embeddings are generated via sequential state tracking over $T$ steps:

$$q_{t}=\text{LSTM}(o_{t-1},q_{t-1}) $$

$$e_{v,t}=f_{a}(\mathbf{z}_{v},q_{t}),\quad \forall v\in\mathcal{V}$$

$$a_{v,t}=\frac{\exp(e_{v,t})}{\sum_{u\in\mathcal{V}}\exp(e_{u,t})},\quad \forall v\in\mathcal{V} $$

$$o_{t}=\sum_{v\in\mathcal{V}}a_{v,t}\mathbf{z}_{v}$$

$$\mathbf{z}_{\mathcal{G}}=o_{1}\oplus o_{2}\oplus \dots \oplus o_{T}$$

#### Graph Coarsening via Clustering

Graph coarsening constructs multi-layer topological hierarchies by grouping nodes into dense structural communities.

1. Compute a parameterized cluster assignment matrix $\mathbf{S}$ map:
    
    $$\mathbf{S}=f_{c}(G,\mathbf{Z}) \in \mathbb{R}^{|\mathcal{V}|\times c}$$
    
2. Coarsen the graph adjacency matrix $\mathbf{A}$:
    
    $$\mathbf{A}^{\text{new}}=\mathbf{S}^{T}\mathbf{A}\mathbf{S} \in \mathbb{R}^{c\times c}$$
    
3. Project features to the new cluster space:
    
    $$\mathbf{X}^{\text{new}}=\mathbf{S}^{T}\mathbf{X} \in \mathbb{R}^{c\times d} $$
    

### Classical Relational Learning Paradigms

#### Iterative Classification Algorithm (ICA)

ICA models relational dependencies by feeding neighbor attributes and label statistics into a standard base classifier.

```
Algorithm 1: ICA(V, E, W, Y_l)
1: Compute initial feature matrix Φ¹ from V, E, W, Y_l
2: Train base classifier using Φ¹
3: for t = 1 to convergence do
4:   Apply classifier to Φ_u^t to compute predicted labels Y_u^t
5:   Update local conditional feature representations Φ_u^(t+1) based on new neighbor labels
6: end for
7: return final labels
```

(Ref: )

#### Label Propagation via Random Walks (Zhu & Ghahramani)

Label propagation establishes transductive label alignment by modeling probability vectors diffusing over graph paths.

Nodes are sorted so that labeled entries occupy index fields prior to unlabeled ones ($V_l$ before $V_u$). The overall random walk transition matrix $\mathbf{P}$ is split into blocks:

$$\mathbf{P}=\begin{pmatrix}\mathbf{P}_{ll} & \mathbf{P}_{lu} \\ \mathbf{P}_{ul} & \mathbf{P}_{uu}\end{pmatrix}=\begin{pmatrix}\mathbf{I} & \mathbf{0} \\ \mathbf{P}_{ul} & \mathbf{P}_{uu}\end{pmatrix}$$

By pinning the true labeled boundary states using identity matrices ($\mathbf{I}$), labeled nodes act as absorbing sinks during random-walk convergence.

$$\mathbf{P}^{\infty}=\lim_{t\to\infty}\mathbf{P}^{t}=\begin{pmatrix}\mathbf{I} & \mathbf{0} \\ (\mathbf{I}-\mathbf{P}_{uu})^{-1}\mathbf{P}_{ul} & \mathbf{0}\end{pmatrix}$$

The stationary distribution over the unlabeled nodes settles exactly to:

$$\mathbf{Y}_{u}=\mathbf{P}_{ul}^{\infty}\mathbf{Y}_{l}=(\mathbf{I}-\mathbf{P}_{uu})^{-1}\mathbf{P}_{ul}\mathbf{Y}_{l} $$

## 3. Practical Implementation & Self-Study Bridge

### Exercise 1: Transductive Pipeline on Zachary's Karate Club

The self-study setup establishes an unsupervised graph feature extraction step followed by a structural classifier model.

Python

```
# Extracting DeepWalk PPMI Low-Rank Matrix Factorization
# (Abstracted core logic from deepwalk_ppmi_embedding)
# Step 1 & 2: Build Empirical Random-Walk Co-occurrence Count Over Context Windows Matrix
# Step 3: Transform Raw Joint Metrics to Positive Pointwise Mutual Information
eps = 1e-12
total = cooccurrence.sum()
row_sums = cooccurrence.sum(axis=1, keepdims=True)
col_sums = cooccurrence.sum(axis=0, keepdims=True)
ppmi = np.maximum(np.log((cooccurrence * total + eps) / (row_sums @ col_sums + eps)), 0.0)

# Step 4: SVD Low-Rank Structural Embedding Extraction
u, singular_values, _ = np.linalg.svd(ppmi, full_matrices=False)
embeddings = u[:, :16] * np.sqrt(singular_values[:16])
```

#### Code-to-Theory Bridge

The code implements an explicit **DeepWalk matrix factorization framework**. Instead of optimizing a stochastic skip-gram objective with negative sampling, it directly computes the exact multi-hop co-occurrence statistics across random walks.

By applying Positive Pointwise Mutual Information ($\operatorname{PPMI}$), the raw co-occurrence counts are converted into a normalized cross-entropy representation:

$$\operatorname{PPMI}(i,j) = \max\left(\log\frac{C_{ij}\sum_{a,b} C_{ab}}{(\sum_b C_{ib})(\sum_a C_{aj})},\;0\right)$$

SVD then reduces the dimensionality of this dense association profile into stable, lower-rank coordinates:

$$\operatorname{PPMI} \approx \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T \implies \mathbf{Z} = \mathbf{U}_d\boldsymbol{\Sigma}_d^{1/2}$$

This process structures a continuous vector space where distance correlates with structural similarity.

The down-stream evaluation maps these transductive embeddings via an `sklearn` Pipeline using a `StandardScaler()` and a standard `LogisticRegression` model. This classification model fits hyperplane margins directly onto the static coordinates.

Because the target graph is limited to 34 instances, a single static split introduces high variance. The evaluation minimizes this by wrapping the data inside a `RepeatedStratifiedKFold(n_splits=5, n_repeats=20)` setup, balancing out tiny class distributions across 100 separate evaluation cycles.

> [!note]
> 
> This framework represents a **transductive** setting. The entire topological structural map ($A$) is exposed during step 1 to build the raw embeddings. However, out-of-sample label security is preserved because the downstream logistic classifier never accesses the evaluation masks during its training phase.

### Exercise 2: Inductive GNN Framework on Cora Citation Network

Using PyTorch Geometric, five deep architecture variants were evaluated on the Cora citation benchmark using the standard `Planetoid` public split.

Python

```python
class NodeClassifier(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, model_type='GCN', num_layers=2, heads=8, dropout=0.5, activation='relu'):
        super().__init__()
        self.activation = activation_from_name(activation)
        self.dropout = dropout
        self.convs = torch.nn.ModuleList()
        
        # Select Layer Aggregator Logic
        if model_type.upper() == 'GCN':
            self.convs.append(GCNConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(GCNConv(hidden_channels, hidden_channels))
            self.convs.append(GCNConv(hidden_channels, out_channels))
            
        elif model_type.upper() == 'SAGE':
            self.convs.append(SAGEConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(SAGEConv(hidden_channels, hidden_channels))
            self.convs.append(SAGEConv(hidden_channels, out_channels))
            
        elif model_type.upper() == 'GAT':
            self.convs.append(GATConv(in_channels, hidden_channels, heads=heads, dropout=dropout))
            for _ in range(num_layers - 2):
                self.convs.append(GATConv(hidden_channels * heads, hidden_channels, heads=heads, dropout=dropout))
            self.convs.append(GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=dropout))

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = self.activation(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        return self.convs[-1](x, edge_index)
```

#### Parameter & Configuration Analysis

|**Configuration Name**|**Core Convolution Operator**|**Target Layer Depth**|**Intermediary Non-Linearity**|**Architectural & Optimization Multipliers**|
|---|---|---|---|---|
|**Baseline GCN**|`GCNConv`|2 Layers|`ReLU`|Receptive Field: 2-hops. Uses symmetric renormalization tracking.|
|**Deeper GCN**|`GCNConv`|3 Layers|`ReLU`|Receptive Field: 3-hops. Expanded graph path reach; susceptible to over-smoothing.|
|**Activation Swap**|`GCNConv`|2 Layers|`ELU`|Continuous negative gradient response $\alpha(e^x - 1)$ prevents dead neurons.|
|**GraphSAGE Check**|`SAGEConv`|2 Layers|`ReLU`|Inductive design. Learns decoupled neighborhood projections before concat steps.|
|**Multi-Head GAT**|`GATConv`|2 Layers|`ELU`|Uses 8 attention heads. Intermediary channels are concatenated, output head is averaged.|

All architectural variations are optimized using `torch.optim.Adam` with multi-class `F.cross_entropy` loss calculated across the `train_mask`. An early stopping monitor with `patience=100` tracks validation accuracy to prevent overfitting on local neighborhood features.

## 4. Critical Insights & Conceptual Connections

### Node Classification vs. Link Prediction Geometric Trade-offs

A common point of confusion is assuming that the top-performing model on a link prediction task will automatically win on a node classification task. This is incorrect due to fundamental geometric and structural differences between the two tasks:

```
                  NODE CLASSIFICATION MATRIX
                  
     Target Space                     Data Split Mechanics
 ┌──────────────────────┐            ┌──────────────────────┐
 │ Single Node Vector   │            │ Mask Labels Only     │
 │ [ v ] -> Class Logit │            │ Topology Intact      │
 └──────────────────────┘            └──────────────────────┘
            ▲                                    ▲
            └─────────────────┬──────────────────┘
                              │
                    STRUCTURAL OBJECTIVES
                              │
                    Homophily Separation
                    Clusters form by label
                    
                              │
            ┌─────────────────┴──────────────────┐
            ▼                                    ▼
     Decoder Framework                Negative Sampling Mode
 ┌──────────────────────┐            ┌──────────────────────┐
 │ Class Head Matrix    │            │ Not Required         │
 │ Softmax Output       │            │ (Task works over     │
 └──────────────────────┘            │ explicit labels)     │
                                     └──────────────────────┘
```

```
                   LINK PREDICTION MATRIX
                   
     Target Space                     Data Split Mechanics
 ┌──────────────────────┐            ┌──────────────────────┐
 │ Pairwise Node Edge   │            │ Extract Target Edges │
 │ (u, v) -> Existence  │            │ Alter Adjacency Map  │
 └──────────────────────┘            └──────────────────────┘
            ▲                                    ▲
            └─────────────────┬──────────────────┘
                              │
                    STRUCTURAL OBJECTIVES
                              │
                    Pairwise Compatibility
                    Proximity reconstruction
                    
                              │
            ┌─────────────────┴──────────────────┐
            ▼                                    ▼
     Decoder Framework                Negative Sampling Mode
 ┌──────────────────────┐            ┌──────────────────────┐
 │ Dot-Product/MLP      │            │ Critical Element     │
 │ Sigmoid Link Score   │            │ Samples unlinked     │
 └──────────────────────┘            │ pairs as 0 targets   │
                                     └──────────────────────┘
```

- **Geometric Constraints:** Node classification favors continuous neighborhood **homophily**, mapping same-class nodes into dense, compact clusters. In contrast, link prediction requires structural **proximity matching** and relational pairwise compatibility, often favoring global random-walk approaches (like Node2Vec) that capture positional roles rather than clean class separation boundaries.
    

### Key Gotchas & Model Diagnostics

> [!warning]
> 
> **The 3-Layer GCN Performance Drop (Over-smoothing):**
> 
> Increasing GCN depth from 2 layers to 3 layers often leads to a drop in validation accuracy. This is driven by **over-smoothing**. As layer depth $l \to \infty$, the localized convolution operation acts as a Laplacian smoothing filter. This causes individual node feature vectors across connected components to converge toward a uniform distribution, making them less linearly separable for downstream classification heads.

> [!brainstorm]
> 
> **Transductive vs. Inductive Data Splits:**
> 
> Algorithms like standard Label Propagation ($LP-ZHU$) are strictly transductive, requiring the complete target graph structure to evaluate unlabeled nodes. If an entirely new node structure is added, the model must recalculate the matrix inverse $(\mathbf{I}-\mathbf{P}_{uu})^{-1}$ across the new graph boundary. Conversely, inductive architectures (like GraphSAGE) learn parameter weights that generalize directly to unseen topologies without re-running the entire optimization pipeline.

# Lecture 12: Graph Kernels

## 1. Executive Summary & Core Objectives

This lecture explores the synthesis of kernel methods with structured graph data. Non-vectorial data domains—such as molecular structures, social networks, and protein interaction maps—cannot be natively processed by traditional coordinate-based machine learning models. Rather than engineering flat feature vectors that flatten the topology, **graph kernels** evaluate similarity directly over discrete graph metrics while satisfying the algorithmic guarantees of **Positive Semi-Definite (PSD)** operators.

The primary objectives of this module are:

- To generalize foundational **R-convolution frameworks** from discrete string sequences to continuous topological representations.
    
- To resolve structural identity and subgraph parsing challenges through **Graphlet Counting**, **Random Walks**, and iterative **Weisfeiler-Lehman subtree refinement**.
    
- To bridge the computational gap between expressive topology metrics and large-scale graph classification workflows.
    

## 2. Theoretical Foundations & Mathematical Models

### 2.1. The Kernel Trick on Structured Objects

In maximum-margin frameworks like Support Vector Machines (SVMs), non-linear classification boundaries are constructed by projecting an input space $\mathcal{X}$ into a high-dimensional Hilbert feature space $\mathcal{H}$ via a mapping $\phi: \mathcal{X} \to \mathcal{H}$. Since computing explicit feature vectors $\phi(x)$ is often intractable, the **Kernel Trick** replaces the inner product $\langle \phi(x), \phi(x') \rangle_{\mathcal{H}}$ with a primitive scalar function $K(x, x')$ evaluating directly on the raw domain:

$$K(x, x') = \langle \phi(x), \phi(x') \rangle$$

According to **Mercer's Theorem**, any symmetric function $K: \mathcal{X} \times \mathcal{X} \to \mathbb{R}$ serves as a valid kernel if its associated Gram matrix $K_{ij} = K(x_i, x_j)$ is **positive semi-definite (PSD)** over any finite subset $\{x_1, \dots, x_N\} \subseteq \mathcal{X}$, satisfying:

$$\sum_{i=1}^N \sum_{j=1}^N c_i c_j K(x_i, x_j) \ge 0, \quad \forall c_i \in \mathbb{R}$$

By abstracting $\mathcal{X}$ to the domain of finite graphs $\mathcal{G}$, we can build powerful structural classifiers without needing explicit vectorizations.

### 2.2. Convolution Kernels (Haussler's R-Convolution)

Proposed by David Haussler (1999), **convolution kernels** define an axiomatic framework for building valid kernels over discrete, structured objects by decomposing them into their constituent parts.

Let $\mathcal{D}$ be a structured data space, and $\mathcal{P}$ be the space of its components. Define a ternary relation $\mathcal{R}$ on $\mathcal{P} \times \mathcal{D}$ such that $(p, d) \in \mathcal{R}$ evaluates to true if and only if $p$ is a valid structural component of $d$. We denote the inverse relation mapping an object to its set of decompositions as:

$$\mathcal{R}^{-1}(d) = \{p \in \mathcal{P} \mid (p, d) \in \mathcal{R}\}$$

If $K_P$ is a valid base kernel defined on the component space $\mathcal{P}$, the generalized $R$-convolution kernel $K_D$ on $\mathcal{D}$ is formalized as the sum over all cross-component pairs:

$$K_D(d, d') = \sum_{p \in \mathcal{R}^{-1}(d)} \sum_{p' \in \mathcal{R}^{-1}(d')} K_P(p, p')$$

> [!note]
> 
> The valid choice of the relation $\mathcal{R}$ determines the concrete instance of the kernel. For standard fixed-dimensional vector dot products, $\mathcal{R}$ maps an item to its zero-indexed feature value pair $(i, x[i])$, where $K_P((i, y), (j, z)) = y \cdot z$ if $i=j$, else $0$.

### 2.3. String Kernels as R-Convolutions

Applying $R$-convolutions to sequence mining yields foundational text and genomic metrics over an alphabet $\Sigma$.

#### String Kernel 1 (Binary Occurrence Kernel)

Let component space $\mathcal{P} = \Sigma^n$ represent the space of all possible contiguous $n$-grams. The membership relation $(u, s) \in \mathcal{R}$ holds true if $u$ appears as a contiguous substring within sequence $s$. Defining $K_P(u, v) = \mathbf{1}[u = v]$, the sequence convolution kernel counts unique matching sub-sequences:

$$K_D^{(1)}(s, t) = |\{u \in \Sigma^n \mid u \in \mathcal{R}^{-1}(s) \land u \in \mathcal{R}^{-1}(t)\}|$$

Its underlying explicit feature representation is binary: $\phi_u^{0/1}(s) = \mathbf{1}[u \text{ occurs in } s]$.

#### String Kernel 2 ($n$-Spectrum Kernel)

If we inject tracking indices by establishing $\mathcal{P} = \mathbb{N} \times \Sigma^n$, where $((k, u), s) \in \mathcal{R}$ specifies that substring $u$ initiates precisely at index $k$ within sequence $s$, the R-convolution maps directly to the classical **$n$-spectrum kernel**:

$$K_D^{(2)}(s, t) = \sum_{u \in \Sigma^n} \text{count}_u(s) \cdot \text{count}_u(t)$$

Where $\text{count}_u(s)$ is the total frequency of $u$ within sequence $s$.

### 2.4. Graphlet Kernels

Graphlet kernels evaluate graph similarity by counting matching subgraphs of a fixed small size $k \in \{3, 4, 5\}$. Let $\mathcal{G}_k = \{g_1, g_2, \dots, g_m\}$ represent the complete set of distinct, non-isomorphic connected graphlets of size $k$.

```
Size 3 Graphlets:
  g1: o---o---o  (3-node path)
  g2: o---o
       \ /
        o      (Triangle)
```

There are two primary mathematical conventions for extracting graphlet count feature maps $\boldsymbol{\phi}(G)$ on a host graph $G = (V, E)$:

#### Version 1: Labelled Induced Occurrences

This metric counts the total number of distinct injective mappings (isomorphisms) from a template graphlet $g \in \mathcal{G}_k$ onto induced subgraphs of $G$:

$$\phi_g^{(1)}(G) = |\{ f: V_g \hookrightarrow V \mid (u, v) \in E_g \iff (f(u), f(v)) \in E \}|$$

#### Version 2: Unlabelled Induced Occurrences

This metric counts the number of distinct subsets of vertices $V' \subseteq V$ of size $k$ whose induced subgraph $G[V']$ is isomorphic to $g$:

$$\phi_g^{(2)}(G) = |\{ V' \subseteq V \mid |V'| = k \land G[V'] \simeq g \}|$$

The two metrics are directly linked by the size of the automorphism group of the template graphlet:

$$\phi_g^{(1)}(G) = |\text{Aut}(g)| \cdot \phi_g^{(2)}(G)$$

For instance, a 3-node path ($P_3$) has $|\text{Aut}(P_3)| = 2$ due to endpoint symmetry, while a triangle ($K_3$) has $|\text{Aut}(K_3)| = 3! = 6$.

> [!brainstorm]
> 
> **Limitations:** Evaluating exact graphlet counts requires checking all $\binom{|V|}{k}$ subsets. Subgraph isomorphism testing is **NP-hard**. Consequently, global graphlet kernels are computationally intractable for larger graphs when $k > 5$.

### 2.5. Random Walk Kernels

Rather than tracking fixed subgraphs, **Random Walk Kernels** compute similarity by evaluating the alignment of node-label sequences generated by simultaneous random walks across two graphs.

Let $G=(V, E, L)$ and $G'=(V', E', L')$ be two node-labeled graphs over an alphabet $\Sigma$. A stochastic walk selects a uniform starting node $v_0 \in V$, moves uniformly to adjacent neighbors, and terminates at any step with a fixed termination probability $p_t \in (0, 1)$. This stochastically defines a probability distribution $p_G(\mathbf{s})$ over any sequential label combination $\mathbf{s} = (l_1, l_2, \dots, l_m) \in \Sigma^*$.

The **Label Sequence Kernel** sums the product of these label probabilities across all possible sequences of infinite length:

$$K(G, G') = \sum_{\mathbf{s} \in \Sigma^*} p_G(\mathbf{s}) p_{G'}(\mathbf{s})$$

Using direct tensor products or dynamic programming on the **direct product graph** $G_\times = G \times G'$, this infinite sum can be solved exactly in $\mathcal{O}(n^4)$ time using matrix inversion:

$$\mathbf{K} = \sum_{l=0}^\infty \lambda^l (\mathbf{A}_\times)^l = (\mathbf{I} - \lambda \mathbf{A}_\times)^{-1}$$

Where $\mathbf{A}_\times$ represents the adjacency matrix of the product graph, and $\lambda$ acts as a geometric damping factor ensuring convergence.

### 2.6. The 1-Dimensional Weisfeiler-Lehman (WL) Subtree Kernel

The **Weisfeiler-Lehman (WL) Kernel** sidesteps the combinatorics of graphlets and the convergence issues of random walks by leveraging an iterative color-refinement heuristic from the 1-WL graph isomorphism test.

#### Algorithmic Sequence (1-WL Refinement)

1. **Initialization:** Assign an initial structural code $c^{(0)}(v)$ to every node $v \in V$. If the nodes are unlabelled, initialize them to a uniform baseline string constant $c^{(0)}(v) = \text{"1"}$.
    
2. **Neighborhood Multiset Extraction:** For each node $v$, gather the labels of its immediate neighbors $N(v) = \{u \in V \mid (v, u) \in E\}$ into a sorted multiset:
    
    $$M^{(t)}(v) = \{\!\{ c^{(t-1)}(u) \mid u \in N(v) \}\!\}$$
    
3. **Injective Hash Map Refinement:** Update each node's code by applying an injective hashing function $H$ to the pair containing the node's own current label and its sorted neighborhood multiset:
    
    $$c^{(t)}(v) = H \left( c^{(t-1)}(v), \text{sort}\left(M^{(t)}(v)\right) \right)$$
    
4. **Termination:** Iterate steps 2 and 3 up to a predefined maximum depth $h$.
    

#### Kernel Computation

Let $\mathcal{C}^{t}$ represent the global dictionary space of unique hashes generated during iteration $t$. Each individual unique hash $\kappa \in \mathcal{C}^t$ forms a feature dimension. The explicit structural mapping $\phi^{\kappa}(G)$ counts how many times label $\kappa$ occurs in graph $G$ at step $t$:

$$\phi^{\kappa}(G) = |\{v \in V \mid c^{t}(v) = \kappa\}|$$

The unnormalized **WL Subtree Kernel of Depth $h$** is defined as the inner product of the concatenated feature histograms extracted across all refinement rounds from $0$ to $h$:

$$K_{\text{WL}}^{(h)}(G, G') = \sum_{t=0}^h \sum_{\kappa \in \mathcal{C}^t} \phi^{\kappa}(G) \phi^{\kappa}(G')$$

## 3. Practical Implementation & Self-Study Bridge

This section connects the theoretical equations directly to Python implementations using `networkx`, `numpy`, and `scikit-learn`.

### 3.1. Core Imports and Infrastructure Setup

All structured implementations share a uniform data processing backend:

Python

```
import numpy as np
import networkx as nx
import pandas as pd
import itertools
from collections import Counter, defaultdict
```

### 3.2. String Kernels: Binary $n$-Spectrum Implementation

To map Haussler’s String Convolution Kernel 1 (Binary Occurrence Count), we write an explicit inner-product generator using Python `set` intersections to compute the binary features $\boldsymbol{\phi}^{0/1}(s)$:

Python

```
def extract_distinct_n_grams(string: str, n: int) -> set:
    """Extracts the unique set of contiguous constituent n-grams."""
    if n <= 0:
        raise ValueError("Sub-sequence chunk width n must be >= 1")
    return {string[i : i + n] for i in range(len(string) - n + 1)}

def binary_n_spectrum_kernel(s: str, t: str, n: int) -> int:
    """Computes Haussler's String Kernel 1 via explicit feature intersections."""
    set_s = extract_distinct_n_grams(s, n)
    set_t = extract_distinct_n_grams(t, n)
    # The set intersection maps directly to the dot product of binary feature vectors
    return len(set_s & set_t)
```

### 3.3. Graphlet Features Counter

The code below counts graphlet occurrences using both the unlabelled induced subgraph method ($\phi_g^{(2)}(G)$) and the labelled isomorphic projection method ($\phi_g^{(1)}(G)$):

Python

```
def compute_graphlet_isomorphisms(template: nx.Graph, host_subgraph: nx.Graph) -> int:
    """Calculates the exact number of label-preserving bijective mappings (symmetries)."""
    matcher = nx.algorithms.isomorphism.GraphMatcher(template, host_subgraph)
    return sum(1 for _ in matcher.isomorphisms_iter())

def extract_induced_graphlet_features(G: nx.Graph, k: int = 3):
    """
    Extracts the graphlet counts for size k=3 templates.
    Returns:
       phi_1: Array counting explicit isomorphic projections (Labelled)
       phi_2: Array counting distinct vertex set selections (Unlabelled)
    """
    # Define distinct size-3 templates
    g1 = nx.path_graph(3)      # o---o---o
    g2 = nx.cycle_graph(3)     # Triangle
    
    phi_2 = {"g1": 0, "g2": 0}
    phi_1 = {"g1": 0, "g2": 0}
    
    # Iterate through all combinations of vertices of size k
    for nodes in itertools.combinations(G.nodes(), k):
        subgraph = G.subgraph(nodes)
        if nx.is_isomorphic(subgraph, g1):
            phi_2["g1"] += 1
            phi_1["g1"] += compute_graphlet_isomorphisms(g1, subgraph)
        elif nx.is_isomorphic(subgraph, g2):
            phi_2["g2"] += 1
            phi_1["g2"] += compute_graphlet_isomorphisms(g2, subgraph)
            
    return phi_1, phi_2
```

### 3.4. Weisfeiler-Lehman Subgraph Refinement and Gram Matrix Execution

To evaluate the Weisfeiler-Lehman kernel, we can use `networkx.weisfeiler_lehman_subgraph_hashes`. This function handles color-refinement and neighborhood hashing, returning a list of hashes for each node across $h$ rounds. We parse these histograms to compute the unnormalized Gram matrix $\mathbf{K}$:

Python

```
def compile_wl_histogram(hashes_dict: dict, h: int) -> Counter:
    """Aggregates hashed features across all refinement layers up to depth h."""
    histogram = Counter()
    for node_hashes in hashes_dict.values():
        if len(node_hashes) < h:
            raise ValueError(f"Requested depth h={h} exceeds available refinement steps.")
        # Concatenate hashes from iteration 0 up to depth h
        histogram.update(node_hashes[:h])
    return histogram

def compute_wl_kernel_matrix(graphs: list, h: int, node_attr: str = None) -> np.ndarray:
    """
    Computes the empirical unnormalized Gram matrix using the WL subtree kernel.
    Time Complexity: O(N^2 * h * |V|)
    """
    num_graphs = len(graphs)
    # Step 1: Extract iterative structural color hashes for all graphs uniformly
    graph_hashes = [
        nx.weisfeiler_lehman_subgraph_hashes(G, node_attr=node_attr, iterations=h, digest_size=16)
        for G in graphs
    ]
    
    # Step 2: Compile the concatenated feature count vectors
    histograms = [compile_wl_histogram(gh, h) for gh in graph_hashes]
    
    # Step 3: Compute the pairwise inner products
    K = np.zeros((num_graphs, num_graphs), dtype=np.int64)
    for i in range(num_graphs):
        for j in range(num_graphs):
            dot_product = sum(
                count_i * histograms[j].get(feature, 0)
                for feature, count_i in histograms[i].items()
            )
            K[i, j] = dot_product
            
    return K
```

### 3.5. Parameter and Configuration Analysis

#### The Depth Hyperparameter $h$

The refinement depth $h$ defines the structural radius of the subtree features. When $h=1$, the kernel behaves like a simple bag-of-characters model, pairing node features with their immediate degree footprints. As $h$ increases, the features capture increasingly larger local neighborhoods.

```
  h = 1: 1-hop neighborhood (immediate neighbors)
  h = 2: 2-hop neighborhood (neighbors of neighbors)
  h = 3: 3-hop neighborhood (global structure propagation)
```

However, choosing too large a value for $h$ can lead to **over-fitting**. High-order hashes can become overly specific to individual graphs, mapping each to a unique feature dimension. This causes the Gram matrix's off-diagonal entries to drop to zero ($K_{ij} \to 0$), removing the cross-graph similarity needed for downstream classifiers.

#### Kernel Normalization

Because raw counts naturally scale with graph size, larger graphs produce higher inner products and inflate the entries of the Gram matrix. To remove this size bias, we apply a cosine normalization in the Hilbert feature space:

$$K_{\text{normalized}}(G, G') = \frac{K(G, G')}{\sqrt{K(G, G) \cdot K(G', G')}}$$

This standardizes all self-similarity entries to $1$, ensuring that the kernel measures topological alignment rather than node density.

## 4. Critical Insights & Conceptual Connections

### 4.1. The Expressive Limits of Graph Isomorphism: The WL Test Failure Cases

While the 1-WL color refinement test is highly expressive, it is **not a complete graph isomorphism test**. It can fail to distinguish certain non-isomorphic graphs that share highly symmetric regular topologies.

Consider two distinct synthetic benchmarks:

- Graph $G_A$: A disconnected union of two independent triangles ($C_3 \cup C_3$).
    
- Graph $G_B$: A single connected 6-node ring ($C_6$).
    

```
Graph G_A (C_3 union C_3):          Graph G_B (C_6 Ring):
     o---o         o---o                 o-------o
      \ /           \ /                 /         \
       o             o                 o           o
                                        \         /
                                         o-------o
```

Both graphs contain exactly six nodes, and every node has a uniform degree of 2.

When we run the 1-WL algorithm, every node across both $G_A$ and $G_B$ initializes to the same baseline label (e.g., $c^{(0)} = 1$). In the first refinement round, every node aggregates the same sorted neighborhood multiset, $\{\!\{1, 1\}\!\}$, which maps to a single new hash (e.g., $c^{(1)} = \text{"1\_[1, 1]"}$).

Because the neighborhood structures are identical, the refinement step cannot separate the nodes. As a result, $G_A$ and $G_B$ generate identical feature histograms across all rounds, yielding equal kernel values even though they have completely different global connectivities.

### 4.2. Comparative Trade-offs and Computational Complexities

When choosing a graph kernel for an application, you must balance expressive power against computational cost:

|**Kernel Family**|**Primary Feature Primitives**|**Pairwise Computational Complexity**|**Notable Limitations / Disadvantages**|
|---|---|---|---|
|**Graphlet Kernel**|Non-isomorphic subgraphs of size $k \in \{3, 4, 5\}$|$\mathcal{O}(|V|
|**Random Walk Kernel**|Hashed label matches along infinite walks|$\mathcal{O}(|V|
|**Weisfeiler-Lehman Kernel**|Hashed neighborhood subtrees up to depth $h$|$\mathcal{O}(h \cdot|E|

### 4.3. Experimental Validation: Evaluation on NCI1 Molecular Data

To evaluate the Weisfeiler-Lehman subtree kernel in a realistic setting, we test it on the **NCI1 dataset**, a standard graph classification benchmark consisting of 4,110 chemical compounds screened for activity against non-small cell lung cancer.

The target labels are binary ($1$ for active anti-cancer compounds, $0$ for inactive). Pairwise similarity matrices are computed using the WL kernel across a range of iteration depths ($h \in \{1, 2, 3, 4, 5\}$). These normalized Gram matrices are then used to train a C-Support Vector Classifier ($C$-SVC).

```
                [ NCI1 Dataset: 4,110 Graphs ]
                              |
               [ Compute Pairs via WL Kernel ]
                              |
       +----------------------+----------------------+
       |                      |                      |
    (h = 1)                (h = 3)                (h = 5)
       |                      |                      |
[ Gram Matrix K_1 ]    [ Gram Matrix K_3 ]    [ Gram Matrix K_5 ]
       |                      |                      |
 [ C-SVC Train ]        [ C-SVC Train ]        [ C-SVC Train ]
       |                      |                      |
 Accuracy: ~75.2%       Accuracy: ~84.6%       Accuracy: ~81.3%
 (Under-fitting)         (Optimal Peak)         (Over-fitting)
```

#### Typical Experimental Insights

- **Performance Progression:** At $h=1$, accuracy is limited because the features only capture local atom types and their immediate degrees, failing to identify larger functional groups.
    
- **Optimal Peak:** Accuracy typically peaks around $h=3$ or $h=4$. At this depth, the subtree features capture larger molecular sub-structures (such as aromatic rings and carbon chains) that correlate strongly with chemical activity.
    
- **Performance Plateau/Drop:** Beyond $h=5$, performance often plateaus or declines. The high-order subtree hashes become overly specific, reducing the unnormalized similarity between distinct molecules and making it harder for the classifier to generalize.
    

> [!important]
> 
> **Methodological Best Practice:** To ensure an unbiased evaluation, the test set must remain completely held out. Hyperparameters like the refinement depth $h$ and the SVM regularization constant $C$ should be tuned exclusively using cross-validation on the training set. Assessing multiple values of $h$ directly on the test set inflates performance metrics and leaks information from the test data.