## **2 Background**
### **2.2 Learning to Hash**
---
#### **What is Learning to Hash?**
Before diving into equations, let’s understand what **learning to hash** means.  

- Imagine you have a **large database of images**, and you want to **quickly find similar images** to a given one.  
- Instead of comparing every pixel in every image, hashing helps by **converting images into short binary codes** (like `101001` or `110110`).  
- Similar images should have **similar binary codes** so that searching becomes fast.  
- The process of **creating these binary codes** using **mathematical functions** is called **learning to hash**.  

Now, let’s go through the equations used in this process.

---

#### **Hash Function Representation**
$$b = h(x) = \text{sgn}(w^T x + \beta)$$
#### **Breaking It Down**
- This equation **defines how an image (or any data point)** is converted into a binary hash code.
- $x$ is the **input data** (like an image represented as numbers).
- $w$ is a **weight vector** that helps transform the input.
- $\beta$ is a **bias term** that adjusts the transformation.
- $w^T x$ means **multiplying the input data by the weight vector** (this is called a **dot product**).
- The **sgn (sign) function** makes sure the output is either **+1** or **-1** (binary representation).  
  - If the result is **positive**, it gives **+1**.  
  - If the result is **negative**, it gives **-1**.

#### **Why This Matters?**
This function is crucial because it allows us to convert data into **binary hash codes** efficiently.

---

#### **Hamming Distance in Hash Space**
$$d^h_{ij} = ||b_i - b_j||_1$$
#### **What is Hamming Distance?**
- The **Hamming Distance** measures **how many bits are different** between two binary codes.
- Example:
  - **Binary Code 1:** `10101`
  - **Binary Code 2:** `10011`
  - Hamming Distance = **2** (since two bits are different).

#### **Breaking It Down**
- $b_i$ and $b_j$ are the **binary codes** of two data points.
- $||b_i - b_j||_1$ means **count the number of different bits**.
- The **smaller the Hamming distance**, the **more similar** the data points are.

#### **Why This Matters?**
If we can **quickly calculate** how different two binary codes are, we can **efficiently find similar images**.

---

#### **Similarity in Hash Space**
$$s^h_{ij} = M - d^h_{ij}$$
##### **Breaking It Down**
- $M$ is the **total number of bits in the hash code**.
- $d^h_{ij}$ is the **Hamming distance** between two codes.
- The similarity score $s^h_{ij}$ is calculated as:
  - If two binary codes are **completely identical**, the similarity is **maximum**.
  - If two binary codes are **completely different**, the similarity is **minimum**.

##### **Example**
If we use a **5-bit binary code**:
- Binary 1: `10101`
- Binary 2: `10111`
- Hamming Distance = 1
- $M = 5$, so Similarity = $5 - 1 = 4$

##### **Why This Matters?**
This helps us define **how close** two binary codes are.

---

### **Pairwise Similarity Preserving Methods**
These methods ensure that **images that are similar in the original dataset remain similar in the hash codes**.

---
#### **1. Similarity-Distance Product Minimization (SDPM)**
$$\sum_{(i,j)} s^o_{ij} d^h_{ij}$$
- **$s^o_{ij}$** = How similar two items were **before hashing**.
- **$d^h_{ij}$** = Hamming Distance after hashing.
- This function tries to **minimize the total difference** between similar items.

---
#### **2. Similarity-Similarity Product Maximization (SSPM)**
$$\sum_{(i,j)} s^o_{ij} s^h_{ij}$$
- This function **tries to maximize similarity** in both the original and hashed space.

---
#### **3. Similarity-Similarity Difference Minimization (SSDM)**
$$\sum_{(i,j)} (s^o_{ij} - s^h_{ij})^2$$
- **Goal:** Ensure that the similarity scores **before and after hashing** are as close as possible.

---
Spectral Hashing (SH) is a **data-dependent hashing method** that creates **binary hash codes** while preserving the structure of the original dataset.  

The key **goal of SH** is to ensure that **similar points in the original data remain close** in the new **binary space**. It does this by using **spectral graph theory** to learn a **hash function** that adapts to the dataset's distribution.

---
## **3.3 Locality-Sensitive Hashing (LSH)**
Locality-Sensitive Hashing (LSH) is a simple method that helps to **find similar items quickly** by hashing them into **buckets**. LSH ensures that **similar data points** have a **high probability** of getting the **same hash code**.

---
### **Step 1: Understanding Similarity in LSH**
LSH works by projecting data into a lower-dimensional space while preserving similarity. One common way to measure similarity is **Cosine Similarity**.

#### **Cosine Similarity Equation**
$$\text{Cosine Similarity}(a,b) = \frac{a \cdot b}{|a||b|}$$
#### **Breaking It Down**
- Measures **how similar two vectors are**, regardless of their size.
- **Dot product $a \cdot b$** finds the alignment between two vectors.
- **Example:**
  - If two images are **identical**, cosine similarity = **1**.
  - If two images are **completely different**, cosine similarity = **0**.

---
### **Step 2: LSH Hashing Function**
$$h(v) = [\text{sgn}(v \cdot r_1), \text{sgn}(v \cdot r_2), ..., \text{sgn}(v \cdot r_k)]$$
#### **Breaking It Down**
- **$v$** = Data vector (like an image represented as numbers).
- **$r_1, r_2, ..., r_k$** = Random projection vectors.
- **Sign function ($\text{sgn}$)**:
  - If the dot product is **positive**, it returns **1**.
  - If the dot product is **negative**, it returns **-1**.
- This function **creates a binary hash code** based on **random projections**.

---
### **Step 3: How LSH Works**
1. **Generate Random Projection Vectors ($r_i$)**:
   - These random vectors define the hash functions.
2. **Compute Dot Product with Data ($v \cdot r_i$)**:
   - Projects data onto random directions.
3. **Apply Sign Function ($\text{sgn}$)**:
   - Converts projections into **binary codes**.
4. **Store Hash Codes in Buckets**:
   - Similar items will have **similar hash codes** and fall into the **same bucket**.

---
### **Why LSH Works Well**
- **Fast similarity search**: Since similar data points are mapped to the **same bucket**, searching for nearest neighbors is much faster.
- **Good for high-dimensional data**: Instead of comparing every pair of data points, LSH reduces the search space significantly.
- **Works for different distance measures**: LSH can be adapted for **Euclidean distance**, **Cosine similarity**, and other distance metrics.

---
### **Final Takeaways**
1. **LSH**: Uses random projections to generate binary hash codes quickly.
2. **Spectral Hashing (SH)**: Uses graph structures to generate compact binary codes.
3. **Deep Supervised Hashing (DSH)**: Uses deep learning to improve retrieval performance.
4. **HashNet**: Solves the gradient problem by using smooth relaxations.
5. **Bihalf**: Ensures that each bit in the hash code carries meaningful information.

---

## **3.4 Iterative Quantization (ITQ)**
Iterative Quantization (ITQ) is a method that **improves the quality of binary hash codes** by finding an optimal rotation of data points. The goal is to minimize the **quantization error** when converting real-valued projections into binary codes.

---
### **Step 1: Understanding Quantization Error**
When converting continuous values into binary values (**+1 or -1**), some information is lost. **ITQ minimizes this loss** by applying a **rotation matrix** that aligns the data optimally before binarization.

#### **Quantization Error Equation**
$$Q(B,R) = \| B - VR \|_F^2$$
#### **Breaking It Down**
- **$B$** = The binary matrix containing the hash codes (**+1 or -1**).
- **$V$** = The input data after Principal Component Analysis (PCA) transformation.
- **$R$** = The rotation matrix that helps minimize quantization error.
- **$\|\cdot\|_F^2$** = Frobenius norm, which measures the overall quantization error.

---
### **Step 2: Computing the Binary Code Matrix**
To generate the binary codes, we apply the sign function:
$$B = \text{sgn}(VR)$$
#### **Breaking It Down**
- We first **project the data** using the rotation matrix $R$.
- Then, we **apply the sign function** to get **binary values**.

---
### **Step 3: Updating the Rotation Matrix**
Since $R$ is unknown initially, we iteratively update it to reduce the quantization error.

#### **Rotation Matrix Update Process**
1. Compute $C$:
   $$C = B^T V$$
2. Compute Singular Value Decomposition (SVD):
   $$C = U S V^T$$
3. Update $R$:
   $$R = U V^T$$
---
### **Step 4: ITQ Algorithm**
1. **Apply PCA** to reduce dimensionality of the data.
2. **Initialize $R$ randomly**.
3. **Iterate until convergence**:
   - Update binary codes: $$B = \text{sgn}(VR)$$
   - Update rotation matrix using SVD.

---
### **Why ITQ Works Well**
- **Minimizes quantization error**: Ensures that the binary codes are as close as possible to the projected data.
- **Preserves similarity**: Ensures that similar data points remain close after binarization.
- **Fast and efficient**: Only requires **matrix multiplications and SVD**, making it computationally feasible.

---
## **Final Takeaways**
1. **LSH**: Uses random projections for fast similarity search.
2. **ITQ**: Finds an optimal rotation to minimize quantization loss.
3. **Spectral Hashing (SH)**: Uses graph structures for compact binary codes.
4. **Deep Supervised Hashing (DSH)**: Uses deep learning to learn hash codes.
5. **HashNet**: Uses smooth relaxations to improve training.
6. **Bihalf**: Ensures that all bits in the hash code carry meaningful information.

---


## **3.5 Spectral Hashing (SH)**
### **Step 2: Constructing the Graph Laplacian**
The **Graph Laplacian** helps us analyze how data points are **clustered together**.

#### **2.1 What is the Laplacian Matrix $L$?**
The **Laplacian matrix** is a way to represent the **structure of the graph**. It is defined as:

$$
L = D - W
$$

- **$W$** is the **affinity matrix** (how strongly points are connected).
- **$D$** is the **degree matrix**, which tells us **how many connections** each node has.
  - The degree matrix is computed as:

  $$
  D_{ii} = \sum_j W(i, j)
  $$

👉 **Key Idea:**  
- If two points **belong to the same cluster**, their Laplacian value will be **low**.
- If two points **belong to different clusters**, their Laplacian value will be **high**.

---

### **Step 3: Minimizing the Hamming Distance**
Our goal is to **assign binary codes** so that similar points stay close **in Hamming space**.

#### **3.1 What is Hamming Distance?**
The **Hamming distance** measures **how many bits differ** between two binary codes.

##### **Example:**
- Binary code 1: `10101`
- Binary code 2: `10011`
- **Hamming distance** = 2 (two bits are different)

#### **3.2 Spectral Hashing Optimization Function**
We want to **find binary codes $b_i$** that minimize the following function:

$$
\min_Y \sum_{i,j} W(i,j) ||b_i - b_j||^2
$$

- **$b_i$ and $b_j$** are binary codes of two data points.
- **$||b_i - b_j||^2$** measures their difference.
- **$W(i, j)$** ensures that **similar points** should have **similar binary codes**.

#### **Expanding the Distance Formula**
We rewrite the squared distance:

$$
||b_i - b_j||^2 = 2k - 2b_i^T b_j
$$

- **$k$** is the number of bits in the binary code.
- **$b_i^T b_j$** measures the **similarity** between binary codes.

#### **3.3 Final Objective Function**
Using matrix notation, we simplify it to:

$$
\min_Y \text{trace}(Y^TLY)
$$

where:
- **$Y$** represents the **binary hash codes**.
- **$L$** is the **Laplacian matrix**.

👉 **Key Idea:**  
- **If two points are similar**, their binary codes should have **low Hamming distance**.
- This function ensures that **similarity in the original space is preserved** in the binary space.

---

### **Step 4: Eigenfunction Approximation**
Finding the **exact solution** to this problem is computationally expensive. Instead, SH uses **eigenfunctions** to approximate it.

#### **4.1 Defining the Range of Data**
We compute the **range of data values**:

$$
R = \max(X_{\text{PCA}}) - \min(X_{\text{PCA}})
$$

- **$X_{\text{PCA}}$** is the data after **Principal Component Analysis (PCA)**.
- **$R$** represents the **spread** of the data along each axis.

#### **4.2 Compute the Fundamental Frequency**
We define the **fundamental frequency**:

$$
\omega_0 = \frac{\pi}{R}
$$

- This **controls how the data is partitioned** into binary values.

#### **4.3 Enumerate Higher Frequencies**
For higher-order approximations, we use:

$$
\omega_i = m_i \cdot \omega_0, \quad m_i \in \{0,1,2,\dots\}
$$

- The integer **$m_i$** determines different **frequency levels**.
- This **allows different partitioning schemes** in the binary space.

#### **4.4 Compute the Eigenfunctions**
The **eigenfunctions** are defined as:

$$
\varphi_i(x) = \sin\left( \frac{\pi}{2} + \omega_i x \right)
$$

- These functions **determine how data points are mapped** into binary space.

#### **4.5 How Spectral Hashing Uses Partitioning**
Unlike **Locality-Sensitive Hashing (LSH)**, which uses **random projections**, SH **analyzes the dataset structure** and applies partitioning based on the **eigenfunctions of the data distribution**.

👉 **Key Idea:** SH **automatically determines the best partitioning strategy** by balancing **low and high frequency partitioning**.

- **Low-frequency partitioning** is used in **important dimensions** (large-scale structure).
- **High-frequency partitioning** is used in **less important dimensions** (fine details).

#### **How SH Determines Partitioning Frequencies**
1. **Most important dimensions (from PCA)** → **Low-frequency partitioning** (Large regions assigned the same binary code).
2. **Less important dimensions** → **High-frequency partitioning** (More partitions, finer adjustments).
3. **Eigenfunctions naturally divide the data space** into partitions that **optimize binary encoding**.

This ensures that **similar data points are grouped together** while still capturing finer details when necessary.

---

### **Step 5: Generating the Binary Codes**
Finally, we generate the **binary hash codes** by applying the **sign function**:

$$
B(i, j) = \text{sgn}(\Phi(x))
$$

- **$\Phi(x)$** is the function that encodes the input.
- **The sign function ensures binary output**:
  - **If the value is positive**, we assign **+1**.
  - **If the value is negative**, we assign **-1**.

---

### **Why Spectral Hashing Works Well**
1. **Preserves similarity:** Ensures similar points stay close in the hash space.
2. **Uses eigenfunctions:** Finds the best partitions automatically.
3. **Computationally efficient:** Faster than deep learning methods.
4. **Automatically adapts to data:** Uses **low-frequency partitioning for important dimensions** and **high-frequency partitioning for less important ones**.



## **3.6 Deep Supervised Hashing (DSH)**
Deep Supervised Hashing (DSH) is a deep learning method that **learns binary codes** using a Convolutional Neural Network (CNN). It ensures that similar images get similar hash codes.

---
### **Step 1: Defining the Loss Function**
$$L(b_1, b_2, s) = \frac{1}{2} (1 - s) d_H(b_1, b_2) + \frac{1}{2} s \max(m - d_H(b_1, b_2), 0)$$
#### **Breaking It Down**
- **$b_1, b_2$**: The binary hash codes of two images.
- **$s$**: **1 if images are similar, 0 if they are not**.
- **$d_H(b_1, b_2)$**: Hamming Distance between the hash codes.
- **$m$**: The margin (threshold for dissimilar pairs).

#### **Understanding the Terms**
- If two images **should be similar** ($s=1$), we **penalize them if their Hamming distance is too large**.
- If two images **should be different** ($s=0$), we **penalize them if their Hamming distance is too small**.

---
### **Step 2: Using a Relaxed Loss for Optimization**
$$L_r = \sum_{i=1}^{N} \left\{ \frac{1}{2} (1 - s_i) ||b_{i,1} - b_{i,2}||^2_2 + \frac{1}{2} s_i \max(m - ||b_{i,1} - b_{i,2}||^2_2, 0) + \alpha (|| |b_{i,1}| - 1 ||_1 + || |b_{i,2}| - 1 ||_1) \right\}$$
- This **relaxes the binary constraint** so that CNN training is possible.

---
## **3.7 HashNet**
HashNet solves the **gradient vanishing** problem in hashing.

---
### **Step 1: Weighted Maximum Likelihood**
$$\min_{\Theta} \sum_{s_{ij} \in S} w_{ij} \left( \log(1 + e^{\alpha \langle b_i, b_j \rangle}) - \alpha s_{ij} \langle b_i, b_j \rangle \right)$$
- **$w_{ij}$**: Controls the importance of different training pairs.
- Uses a **weighted similarity loss** to learn better binary codes.

---
### **Step 2: Tanh Relaxation**
$$\lim_{\beta \to \infty} \tanh(\beta z) = \text{sgn}(z)$$
- **Tanh function approximates the sign function** for smooth optimization.

---
## **3.8 Bihalf**
Bihalf ensures that binary codes **maximize information** by making each bit **equally likely to be 0 or 1**.

---
### **Step 1: Using Optimal Transport**
$$W_1(P_U, P_B) = \min_{\gamma \in \Gamma(P_U, P_B)} \sum_{i,j} \pi_{ij} (u_i - b_j)^2$$
- Ensures that the **continuous features** are well mapped to binary codes.

---
### **Step 2: Gradient Update with STE**
$$\frac{\partial L}{\partial U} = \frac{\partial L}{\partial B} + \alpha (U - B)$$
- Uses the **Straight-Through Estimator (STE)** to enable backpropagation.

---

## **4 Understanding Eigenvalues, Eigenvectors, and Eigenfunctions**
Eigenvalues, eigenvectors, and eigenfunctions are fundamental mathematical concepts used in **Spectral Hashing (SH)** and other machine learning techniques. These concepts help in **understanding the structure of data, reducing dimensionality, and optimizing transformations**.

This section explains each term **step by step**, using **simple language** and **examples**.

---

### **4.1 What is an Eigenvector and Eigenvalue?**
#### **4.1.1 What is a Vector?**
Before we talk about **eigenvectors**, we need to understand **vectors**.

A **vector** is a mathematical object that represents both **magnitude (size)** and **direction**. It can be written as:
$$v = \begin{bmatrix} v_1 \\ v_2 \end{bmatrix}$$
- **$v_1$ and $v_2$** are the components of the vector.
- Vectors are used to represent **data points, forces, velocities, or any quantity with direction**.

For example:
- A 2D point **(3,4)** can be written as the vector:
  $$v = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$$

---

#### **4.1.2 What is a Matrix?**
A **matrix** is a collection of numbers arranged in a grid. It is often used to **transform vectors**.

Example matrix:
$$A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$
This matrix can be used to transform a vector by **multiplication**.

---

#### **4.1.3 What is an Eigenvector and Eigenvalue?**
An **eigenvector** of a matrix **$A$** is a **special vector** that **does not change direction** when multiplied by **$A$**.

Mathematically, this is written as:
$$Av = \lambda v$$
where:
- **$A$** is the matrix (transformation).
- **$v$** is the **eigenvector**.
- **$\lambda$** is the **eigenvalue**, which tells how much the eigenvector is stretched or shrunk.

---

#### **4.1.4 Example: Finding Eigenvectors and Eigenvalues**
Let’s consider this transformation matrix:
$$A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$
We want to find its **eigenvectors and eigenvalues**.

1. **Step 1: Solve the characteristic equation**  
   We solve the equation:
   $$\det(A - \lambda I) = 0$$
   Expanding the determinant gives:
   $$(2 - \lambda)(2 - \lambda) - (1 \times 1) = 0$$
   $$\lambda^2 - 4\lambda + 3 = 0$$
   Solving for $\lambda$:
   $$\lambda_1 = 3, \quad \lambda_2 = 1$$

2. **Step 2: Find the eigenvectors**  
   For $\lambda_1 = 3$, solving $(A - 3I)v = 0$ gives:
   $$v_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
   For $\lambda_2 = 1$, solving $(A - I)v = 0$ gives:
   $$v_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}$$

---

#### **4.1.5 What Do Eigenvectors and Eigenvalues Mean?**
- **Eigenvectors** represent **directions** that stay the same during transformation.
- **Eigenvalues** tell **how much the vector is scaled** along that direction.
- If $\lambda > 1$, the vector is **stretched**.
- If $0 < \lambda < 1$, the vector is **shrunk**.
- If $\lambda = 1$, the vector remains the **same size**.
- If $\lambda = 0$, the vector is mapped to **zero**.

---

### **4.2 What is an Eigenfunction?**
#### **4.2.1 What is a Function?**
A **function** is a rule that takes an input **$x$** and produces an output **$f(x)$**.

Example:
- $$f(x) = x^2$$
- If **$x=2$**, then **$f(2) = 4$**.

---

#### **4.2.2 What is an Eigenfunction?**
An **eigenfunction** is a function that **does not change shape** when a mathematical operation is applied to it.

Mathematically, for an operator **$\mathcal{L}$**:
$$\mathcal{L} \varphi(x) = \lambda \varphi(x)$$
where:
- **$\mathcal{L}$** is an **operator** (like differentiation or matrix multiplication).
- **$\varphi(x)$** is the **eigenfunction**.
- **$\lambda$** is the **eigenvalue**.

---

#### **4.2.3 Example: Eigenfunctions of the Derivative**
Consider the second derivative operator:
$$\mathcal{L} = \frac{d^2}{dx^2}$$
Applying it to a function:
$$\frac{d^2}{dx^2} \sin(\omega x) = -\omega^2 \sin(\omega x)$$
We see that:
- The function **stays the same** ($\sin(\omega x)$).
- It is only **scaled by $-\omega^2$**.
- So, $\sin(\omega x)$ is an **eigenfunction** of $\frac{d^2}{dx^2}$ with eigenvalue **$-\omega^2$**.

---

### **4.3 Why Are Eigenvalues and Eigenfunctions Important in Hashing?**
1. **Spectral Analysis**  
   - Spectral Hashing (SH) uses **eigenfunctions** to find **optimal binary partitions** of the data.

2. **Graph Laplacian**  
   - The **Laplacian matrix $L$** has **eigenvectors** that reveal the **intrinsic structure** of the data.

3. **Dimensionality Reduction**  
   - Eigenvalues help in **PCA (Principal Component Analysis)**, which reduces high-dimensional data.

---

### **4.4 Eigenvalues and Eigenfunctions in Spectral Hashing**
In **Spectral Hashing (SH)**, we compute **eigenfunctions** to **partition data efficiently**.

1. **First, Define the Range**
   $$R = \max(X_{\text{PCA}}) - \min(X_{\text{PCA}})$$
   - This finds the **spread of the data**.

2. **Compute the Fundamental Frequency**
   $$\omega_0 = \frac{\pi}{R}$$
   - This defines the **basic partition frequency**.

3. **Enumerate Modes**
   $$\omega_i = m_i \cdot \omega_0, \quad m_i \in \{0,1,2,\dots\}$$
   - Different $m_i$ values define **different partitions**.

4. **Compute the Eigenfunctions**
   $$\varphi_i(x) = \sin\left( \frac{\pi}{2} + \omega_i x \right)$$
   - These **functions split the data** into binary representations.

5. **Generate Binary Codes**
   $$B(i, j) = \text{sgn}(\Phi(x))$$
   - The **sign function** converts the eigenfunction into **binary** form.

---

### **4.5 Final Takeaways**
- **Eigenvectors** tell us **important directions in data**.
- **Eigenvalues** tell us **how much each direction contributes**.
- **Eigenfunctions** generalize eigenvectors to **continuous spaces**.
- **Spectral Hashing (SH)** uses these concepts to generate **compact binary codes**.

---
## 5. **Nyström Method in Spectral Hashing**
The **Nyström method** is a technique used to approximate large matrices, particularly in spectral methods, when computing the **eigenvectors of a graph Laplacian** becomes computationally expensive. In **Spectral Hashing**, it is used for **out-of-sample extension**, which means extending the learned binary hash function to new data points that were not part of the training set.

However, **Nyström extension is computationally expensive**, so Spectral Hashing **avoids it** by using **modes instead**. This explanation will break it down in simple and intuitive terms.

---

### **5.1 Why Do We Need the Nyström Method?**
Spectral Hashing **finds eigenfunctions** to generate binary hash codes, but there is a **problem**: 

1. **Computing eigenfunctions is expensive for large datasets**  
   - If we compute eigenfunctions for **millions of data points**, the process becomes infeasible.
   - The standard approach requires **solving an eigenvalue problem** for a **large similarity matrix**, which takes **$O(n^3)$** time for $n$ data points.
  
2. **We need to compute hash codes for new data points**  
   - Once hashing is learned on the training set, we must **extend the learned function to new inputs**.  
   - This is called **out-of-sample extension**.

---

### **5.2 How the Nyström Method Works**
The **Nyström method** provides an **approximate solution** by using only a **small subset** of data points instead of the full dataset. 

#### **Step 1: Select a Subset of Data**
- Instead of computing the **full** eigenvalue decomposition of the matrix, we select **a subset of $m$ data points**, where $m \ll n$.
- This reduces the complexity to **$O(m^2k + k^3)$** instead of **$O(n^3)$**.

#### **Step 2: Approximate the Large Matrix**
- Let $K$ be the **affinity matrix** (computed using a Gaussian kernel or other similarity measures).  
- We split $K$ into:
  
  $$
  K = \begin{bmatrix} A & B \\ B^T & C \end{bmatrix}
  $$

  where:
  - **$A$** is the **small subset** of size **$m \times m$** (we fully compute this).
  - **$B$ and $C$** represent interactions with the remaining data.

- The Nyström approximation reconstructs the **full eigenvectors** using only **$A$ and $B$**.

#### **Step 3: Compute Eigenvectors on the Small Matrix**
- Solve the **eigenproblem** only for **$A$**, obtaining eigenvectors **$U$** and eigenvalues **$\Lambda$**.

#### **Step 4: Extend to the Full Dataset**
- The eigenvectors for the full matrix are **approximated** as:

  $$
  \tilde{K} = B^T A^{-1} B
  $$

- The **new data points** are projected into the same eigenfunction space **without computing the full matrix**.

---

### **5.3 What is a Gaussian Kernel?**
The **Gaussian kernel** is a function that measures the similarity between two data points based on their Euclidean distance. It is commonly used in kernel methods and spectral hashing to construct the **affinity matrix $K$**.

#### **Mathematical Definition**
The Gaussian kernel is defined as:

$$
K(x_i, x_j) = \exp\left( -\frac{||x_i - x_j||^2}{2\sigma^2} \right)
$$

where:
- **$x_i, x_j$** are two data points.
- **$||x_i - x_j||^2$** is the squared Euclidean distance.
- **$\sigma$** is the bandwidth parameter that controls how quickly similarity decreases with distance.

#### **Intuition Behind the Gaussian Kernel**
- If **$x_i$ and $x_j$ are very close**, the similarity is **close to 1**.
- If **$x_i$ and $x_j$ are far apart**, the similarity approaches **0**.
- The parameter **$\sigma$ controls the sensitivity**:
  - **Small $\sigma$** → Only very close points are considered similar.
  - **Large $\sigma$** → More points are considered similar.

This kernel is used to construct the **affinity matrix $K$**, which describes the relationships between data points in Spectral Hashing.

---

### **5.4 Why Is the Nyström Method Computationally Expensive?**
Even though the Nyström method reduces computation **compared to the full eigendecomposition**, it is still expensive because:

1. **The cost of computing $B^T A^{-1} B$ is $O(m^2n)$**  
   - If we select a large $m$, the cost **grows quadratically** with $m$.
  
2. **Computing the eigenvectors of $A$ still requires $O(m^3)$ operations**  
   - Even with a smaller subset, solving the eigenproblem still has significant overhead.

3. **Extending to new points requires linear complexity $O(n)$**  
   - For each **new query point**, we must compute the Nyström extension.
   - This **is as expensive as nearest neighbor search**, making it impractical for large-scale retrieval.

---

### **5.5 Why Does Spectral Hashing Avoid Nyström?**
Spectral Hashing **avoids the Nyström method** because computing **out-of-sample extension using Nyström is too expensive**. Instead, it uses a **simpler and more efficient approach**.

#### **Instead of Nyström, SH Uses Analytical Eigenfunctions**
Instead of explicitly computing eigenfunctions on a similarity graph (which would require Nyström), SH assumes the **data follows a separable distribution** and **directly computes the eigenfunctions analytically**.

#### **Key Idea: Eigenfunctions of a Uniform Distribution**
- If data is assumed to be **uniformly distributed**, the **eigenfunctions** are known analytically:
  
  $$
  \varphi_k(x) = \sin\left(\frac{\pi}{2} + \frac{k\pi}{b-a} x\right)
  $$

- The **eigenvalues** are:
  
  $$
  \lambda_k = 1 - e^{-\frac{\epsilon^2}{2} \left(\frac{k\pi}{b-a}\right)^2}
  $$

- **This avoids matrix inversion and expensive approximations!**

---

### **5.6 Summary**
| Method | Computational Cost | Used in Spectral Hashing? | Why? |
|--------|--------------------|--------------------------|------|
| **Full Eigendecomposition** | $O(n^3)$ | ❌ No | Too expensive for large datasets |
| **Nyström Method** | $O(m^2n + m^3)$ | ❌ No | Still expensive, requires out-of-sample extension |
| **Analytical Eigenfunctions (Modes)** | $O(k)$ | ✅ Yes | Directly computed, no approximation needed |

#### **Key Takeaways**
- **Nyström method** is used to approximate large matrix eigenproblems, but it's still **too slow for Spectral Hashing**.
- **Spectral Hashing avoids Nyström** by assuming **data follows a rectangular distribution**, allowing **direct computation of eigenfunctions**.
- **This makes Spectral Hashing much more efficient**, as it eliminates the need for expensive out-of-sample extensions.


## 6. **Principal Component Analysis (PCA)**
**Principal Component Analysis (PCA)** is a technique used to **reduce the dimensionality of data** while keeping as much important information as possible. It finds the **best directions** to represent the data and removes unnecessary details.

PCA is used in **Spectral Hashing** to determine the **important axes of variation** in the dataset before computing eigenfunctions.

---

### **6.1 Why Do We Need PCA?**
Imagine you have **high-dimensional data** (for example, images with thousands of pixels).  
Some of this data is **redundant** or **not useful**.  

👉 **Goal of PCA:**  
1. **Find the most important directions** where data varies the most.  
2. **Remove unnecessary dimensions** to make computations faster.  
3. **Keep as much meaningful information as possible** while using fewer numbers.  

---

### **6.2 Intuition: Finding the Best Line to Represent Data**
#### **Example: Data in 2D**
Let’s say we have **points on a 2D plane**:

- The data points **spread mostly along a diagonal**.
- Instead of storing **both x and y coordinates**, we can **find a new axis** along the diagonal.
- This **new axis** is the **Principal Component**.

#### **Example: Reducing from 3D to 2D**
- Imagine you have **a cloud of points in 3D space**.
- Most of the variation happens **along a flat plane**.
- We can **ignore the least important axis** and still keep most of the information.

👉 **PCA finds these important axes and removes unnecessary dimensions!**

---

### **6.3 How PCA Works (Step-by-Step)**
PCA follows these steps mathematically:

#### **Step 1: Center the Data (Subtract the Mean)**
To ensure our data is **centered at zero**, we compute the mean for each feature and subtract it:

$$
X_{\text{centered}} = X - \mu
$$

where:
- **$X$** is the original data matrix.
- **$\mu$** is the mean of each feature (column).
- **$X_{\text{centered}}$** ensures that our data is centered at zero.

---

#### **Step 2: Compute the Covariance Matrix**
The **covariance matrix** shows how features vary together:

$$
C = \frac{1}{n} X_{\text{centered}}^T X_{\text{centered}}
$$

where:
- **$C$** is an **$d \times d$** matrix (if we have **$d$** dimensions).
- Each element **$C_{ij}$** shows how strongly **feature $i$ is related to feature $j$**.
- Large values mean the features are strongly correlated.

---

#### **Step 3: Compute Eigenvectors and Eigenvalues**
To find the **principal components**, we solve the **eigenvalue problem**:

$$
Cv = \lambda v
$$

where:
- **$v$** are the **eigenvectors** (principal components).
- **$\lambda$** are the **eigenvalues** (importance of each direction).

---

#### **Step 4: Select the Top \( k \) Principal Components**
Not all principal components are equally important.  
- **The largest eigenvalues** correspond to the **most important directions**.
- **The top \( k \) eigenvectors** correspond to the principal components that capture the most variance.

##### **What Are the Top \( k \) Principal Components?**
The **top \( k \) principal components** are the **most important directions** in which the data varies the most. They are chosen by sorting **eigenvalues** in descending order and keeping the top \( k \) eigenvectors.

👉 **Intuition:**
- If we have **3D data**, but most of the variation happens in **2D**, we **drop the least important axis**.
- PCA **automatically determines** which dimensions to keep.

##### **Example: Reducing a 3D Dataset to 2D**
1. Compute eigenvalues:  
   - **\( \lambda_1 = 5.2, \lambda_2 = 3.8, \lambda_3 = 0.2 \)**  
   - Since **\( \lambda_3 \)** is very small, we **ignore the third dimension**.

2. Select top **\( k = 2 \)** principal components:
   - Choose eigenvectors corresponding to the **two largest eigenvalues**.

3. Construct transformation matrix:
   $$
   V_k =
   \begin{bmatrix}
     v_1 & v_2
   \end{bmatrix}
   $$

4. Transform data:
   $$
   X_{\text{PCA}} = X_{\text{centered}} V_k
   $$

Now, the data is **in 2D instead of 3D**, but it **still captures most of the important information**.

---

#### **Step 5: Project Data Onto New Axes**
The final transformed data is:

$$
X_{\text{PCA}} = X_{\text{centered}} V_k
$$

where:
- **$X_{\text{PCA}}$** is the reduced data.
- **$V_k$** contains the **top \( k \) principal components**.

This means our original **high-dimensional data** is now represented using **fewer dimensions** while keeping the most important information.

---

### **6.4 Why Are Top \( k \) Principal Components Important in Spectral Hashing?**
Spectral Hashing **first applies PCA** to **align the data** before computing eigenfunctions.  
This ensures:
1. **Redundant dimensions are removed**.
2. **Data is aligned along the most important axes**.
3. **Eigenfunctions are computed more efficiently**.

This makes the **hashing process more effective and computationally efficient**.

---

### **6.5 Summary**
| Step | What Happens? |
|------|--------------|
| **1. Center Data** | Subtract mean from each feature |
| **2. Compute Covariance Matrix** | Measure relationships between features |
| **3. Find Eigenvectors & Eigenvalues** | Determine important directions |
| **4. Select Top \( k \) Principal Components** | Keep the most important eigenvectors |
| **5. Transform Data** | Project data onto new axes |


## 7. **Precision@K, Average Precision, and Mean Average Precision (mAP)**

In **information retrieval** and **hashing-based search**, we need ways to **evaluate how well the system retrieves relevant results**. Three important evaluation metrics are:

1. **Precision@K** – Measures how many relevant results are in the top $K$ retrieved items.
2. **Average Precision (AP)** – Measures how well relevant items are ranked in a single query.
3. **Mean Average Precision (mAP)** – Averages AP over multiple queries to evaluate overall system performance.

These metrics are used in **Spectral Hashing** and other **retrieval systems** to measure how well the binary hash codes preserve similarity.

---

### **7.1 What is Precision@K?**
**Precision@K** measures the fraction of the **top $K$ retrieved items** that are **actually relevant**.

#### **Mathematical Definition**
If a retrieval system returns **$K$** items, and out of those, $R_K$ are relevant, then:

$$
\text{Precision@K} = \frac{R_K}{K}
$$

#### **Example**
Imagine you search for **"cats"**, and the system returns **5 images**:
1. 🐱 (Relevant)
2. 🐶 (Not Relevant)
3. 🐱 (Relevant)
4. 🦁 (Relevant)
5. 🦊 (Not Relevant)

There are **3 relevant items in the top 5**, so:

$$
\text{Precision@5} = \frac{3}{5} = 0.6
$$

👉 **Interpretation:**  
- If **Precision@K is high**, most retrieved results are relevant.
- If **Precision@K is low**, many retrieved results are irrelevant.

---

### **7.2 What is Average Precision (AP)?**
**Average Precision (AP)** measures **how well the relevant items are ranked**.  
If relevant items appear **earlier** in the ranking, AP is **higher**.

#### **Mathematical Definition**
Average Precision is computed as:

$$
AP = \frac{1}{R} \sum_{k=1}^{N} P(k) \cdot \text{rel}(k)
$$

where:
- **$N$** is the total number of retrieved items.
- **$R$** is the total number of relevant items.
- **$P(k)$** is **Precision@K** at position $k$.
- **$\text{rel}(k)$** is **1 if item at position $k$ is relevant, 0 otherwise**.

#### **Example**
If the system retrieves **5 items**, and the relevant ones are at **positions 1, 3, and 4**:

| Rank $k$ | Item | Relevant? $\text{rel}(k)$ | Precision@K $P(k)$   |
| -------- | ---- | ------------------------- | -------------------- |
| 1        | 🐱   | ✅ (Relevant)              | $\frac{1}{1} = 1.0$  |
| 2        | 🐶   | ❌ (Not Relevant)          | -                    |
| 3        | 🐱   | ✅ (Relevant)              | $\frac{2}{3} = 0.67$ |
| 4        | 🦁   | ✅ (Relevant)              | $\frac{3}{4} = 0.75$ |
| 5        | 🦊   | ❌ (Not Relevant)          | -                    |

The **Average Precision** is:

$$
AP = \frac{1}{3} \left( 1.0 + 0.67 + 0.75 \right) = \frac{2.42}{3} = 0.81
$$

👉 **Interpretation:**  
- If all relevant items are **ranked at the top**, AP is **high**.
- If relevant items appear **late in the ranking**, AP is **low**.

---

### **7.3 What is Mean Average Precision (mAP)?**
**Mean Average Precision (mAP)** is the **average of AP across multiple queries**.

#### **Mathematical Definition**
If we have **$Q$ queries**, then:

$$
mAP = \frac{1}{Q} \sum_{q=1}^{Q} AP_q
$$

where:
- **$AP_q$** is the Average Precision for query $q$.
- **$Q$** is the number of queries.

#### **Example**
If we evaluate **3 queries**, and their **Average Precisions are:**
- Query 1 → **AP = 0.81**
- Query 2 → **AP = 0.67**
- Query 3 → **AP = 0.92**

Then the **mAP** is:

$$
mAP = \frac{0.81 + 0.67 + 0.92}{3} = 0.80
$$

👉 **Interpretation:**  
- **Higher mAP** means the system ranks relevant items **consistently well** across many queries.
- **Lower mAP** means the system struggles to rank relevant items consistently.

---

### **7.4 Summary**
| Metric | What It Measures | Best Value | Used In |
|--------|-----------------|------------|---------|
| **Precision@K** | How many of the **top $K$** retrieved items are relevant | **1.0** (100% relevant) | Quick relevance check |
| **Average Precision (AP)** | How well **relevant items** are ranked in a single query | **1.0** (perfect ranking) | Single query evaluation |
| **Mean Average Precision (mAP)** | The **overall ranking performance** across multiple queries | **1.0** (perfect system) | Full system evaluation |

### **Why Is mAP Important in Spectral Hashing?**
In Spectral Hashing, we use **mAP** to evaluate how well the binary hash codes preserve similarity.  
- If **mAP is high**, the hash codes are good at retrieving similar items.  
- If **mAP is low**, the hash function needs improvement.


