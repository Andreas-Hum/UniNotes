
## 1. Core Frameworks and Baseline Proactive Agent Concepts

### Proactive vs. Reactive Paradigms

- **Definition:** Reactive models only execute inference when explicitly prompted by a user. Proactive agents continuously monitor multimodal environmental sensory inputs to dynamically predict when, how, and why to execute helpful interventions without explicit user instructions.
    
- **Trade-off:** Reactive models incur computation costs only during direct interaction. Proactive agents require continuous context checks and inference loops over time, leading to major computational bottlenecks, high token consumption, and substantial memory requirements.

### ContextAgent
- **Definition:** A state-of-the-art framework for context-aware proactive agents that extracts multi-dimensional contexts from wearable sensor streams and historical profiles to predict when assistance is needed, executing automatic tool chains if triggered.
    
- **Practical Role:** Serves as the baseline capability model. It uses a supervised fine-tuned (SFT) reasoning model to achieve high proactive accuracy, but its original architecture is heavily unoptimized for computational efficiency.

### ContextAgentBench (and ContextAgentBench-Lite)

- **Definition:** The benchmark dataset used to evaluate proactive agents. It contains 1,000 samples across nine daily scenarios and twenty unique tool configurations. The Lite version contains 300 human-verified samples paired with raw sensor streams (egocentric video and audio waves).
    
- **Practical Role:** Provides a fixed, repeatable baseline dataset to measure task accuracy degradation whenever compression or optimization techniques are applied.
    

### ReAct (Reasoning + Acting)

- **Definition:** A classic reactive prompting technique that enforces iterative thoughts, actions, and observations.
    
- **Oral Exam Context:** Unlike proactive architectures, ReAct still depends strictly on an initial, explicit user instruction and does not solve the decision problem of _when_ to intervene.
    

### ProAgent

- **Definition:** An end-to-end proactive assistant framework designed to process sensory contexts on smart glasses. It prioritizes on-demand, capability-driven hierarchical context extraction but operates with low computational and training efficiency.
    

### General Model Mathematical Mapping

The proactive decision process is formalized as a continuous evaluation of contextual states over time.

- **Sensory Context Extraction Equation:**
    $$C=(C_V,C_A,N)$$
    - **Variables:**
        - $C$: The structured context summary.
        - $C_V$: Visual context extracted from egocentric video streams.
        - $C_A$: Audio context extracted from speech waveforms.
        - $N$: Textual context taken from smartphone notification logs.
    - **Reasoning:** Raw sensory data is extremely high-dimensional and computationally impossible for an LLM to digest directly. This extraction step converts massive perception streams into dense textual summaries.
- **Context-Aware Reasoner Equation:**
    $$(T,PS,TC)=A_S(C,P)$$
    
    - **Variables:**
        - $A_S$: The supervised fine-tuned (SFT) large language model acting as the cognitive decision engine.
        - $C$: The extracted sensory context representation.
        - $P$: The user's historical profile and preference matrix (persona context).
        - $T$: Step-by-step cognitive thought traces (Chain-of-Thought).
        - $PS$: The scalar proactive score.
        - $TC$: The planned tool chain.
    - **Reasoning:** The model processes the surrounding environmental context alongside the user's personal habits to output its reasoning trace ($T$), decide the urgency of the situation ($PS$), and formulate a plan of actions ($TC$) simultaneously.
- **Action Trigger Thresholding:**
    $$\text{Operational State}=\begin{cases}\text{Passive (Stay Silent)},&\text{if }PS<\theta\\\text{Active (Execute }TC\text{ and generate response }R\text{)},&\text{if }PS\ge\theta\end{cases}$$
    
    - **Variables:**
        
        - $PS$: Proactive score mapped to a discrete five-point scale, where $PS\in\{1,2,3,4,5\}$ (1 means no proactivity; 5 means urgent intervention).
            
        - $\theta$: The adjustable operational threshold parameter.
            
        - $R$: The final response generated to assist the user.
            
    - **Reasoning:** To avoid overwhelming the user with unnecessary prompts, the agent remains silent if the predicted score is below the threshold $\theta$. When $PS$ meets or exceeds the threshold, active tool execution and user assistance are triggered.
        
- **Planned Tool Chain Representation:**
    
    $$TC=((t_i,a_i))_{i=1}^m\quad t_i\in\mathcal{T}$$
    
    - **Variables:**
        
        - $\mathcal{T}$: The complete set of available tools (e.g., 20 tools in the benchmark).
            
        - $t_i$: The specific tool selected at step $i$.
            
        - $a_i$: The dynamically generated arguments and parameters for tool $t_i$.
            
        - $m$: The total number of sequential tool calls (capped at 5 in the benchmark).
            
    - **Reasoning:** When proactivity is triggered, the model executes a structured sequence of API calls. Each call must contain highly precise arguments to prevent runtime execution errors.
        

## 2. Fine-Tuning and Parameter-Efficient Adaptation (LoRA / QLoRA)

### PEFT (Parameter-Efficient Fine-Tuning)

- **Definition:** An adaptation paradigm where instead of retraining the billions of parameters of a pre-trained language model, the base model is frozen and a tiny set of auxiliary parameters is trained.
    
- **Trade-off:** Dramatically reduces training VRAM requirements and optimizer storage , but does not natively reduce the underlying model size or memory footprint during standard active deployment unless the weights are physically merged post-training.
    

### LoRA (Low-Rank Adaptation)

- **Definition:** A PEFT technique that parameterizes weight updates as the product of two low-rank, high-dimensional matrices.
    
- **Motivation:** Storing the gradients, activations, and optimizer tracking states (like momentum and variance in 32-bit Adam) for a full 7B or 8B parameter model requires roughly 98 GB of VRAM during training. LoRA restricts optimization strictly to the low-rank adapter matrices, cutting trainable parameters and VRAM requirements.
    

### QLoRA (Quantized Low-Rank Adaptation)

- **Definition:** An advanced optimization that loads the frozen base model in an aggressive 4-bit NormalFloat (NF4) format, while keeping 16-bit trainable LoRA adapters to compute stable gradients.
    
- **Trade-off:** Compresses training memory for a 7B model down to under 6 GB (a 47% reduction) , but introduces a slight training speed penalty (up to 30% slower) due to the computational overhead of dynamically dequantizing weights during forward and backward passes.
    

### Rank ($r$) and Alpha ($\alpha$) Scaling

- **Rank ($r$):** A hyperparameter that defines the inner dimension of the low-rank projection. It controls the expressive capacity of the adapter. Instruct-tuned dense models (Llama-3.1 and Qwen2.5) saturate at $r=32$, whereas reasoning models (DeepSeek-R1) benefit continuously up to $r=64$ due to the high-capacity space needed to map thought traces to strict JSON configurations.
    
- **Alpha ($\alpha$):** A constant scaling factor applied to the adapter weight update. It acts as a learning rate stabilizer when scaling $r$.
    

### Targeted Modules

- **All Linear:** Applying adapters across all attention projections and MLP layers. This consistently provides the strongest task performance for standard models.
    
- **MLP Only:** Restricting adapters to feed-forward blocks. This is highly efficient and actually outperforms other configurations on reasoning models like DeepSeek-R1. This indicates that MLP blocks serve as the primary site of format-specific alignment (JSON parsing), while adapting DeepSeek's attention matrices directly disrupts its pre-trained step-by-step logic chains.
    

### Low-Rank Weight Approximation Mathematics

During standard training, the model attempts to optimize a high-dimensional weight matrix $W_0 \in \mathbb{R}^{d \times k}$ by adding a weight change update matrix $\Delta W$.

- **LoRA Weight Decomposition:**
    
    $$\Delta W=B\cdot A$$
    
    - **Variables:**
        
        - $W_0$: The original, frozen pre-trained weight matrix of size $d \times k$.
            
        - $\Delta W$: The total accumulated weight update of size $d \times k$.
            
        - $B$: A trainable low-rank matrix of size $d \times r$.
            
        - $A$: A trainable low-rank matrix of size $r \times k$.
            
        - $r$: The adapter rank, where $r\ll\min(d,k)$.
            
    - **Reasoning:** Instead of updating $d \times k$ parameters, the update is factorized into two skinny matrices $B$ and $A$. If $d=4096$ and $k=4096$, updating $W_0$ directly requires tracking $16,777,216$ parameters. Storing these updates in a rank $r=16$ adapter requires tracking only $(4096 \times 16) + (16 \times 4096) = 131,072$ parameters—representing an approximate 99.2% reduction in trainable parameters. Matrix $A$ is initialized using a random Gaussian distribution, and matrix $B$ is initialized to zero, ensuring that $\Delta W=0$ at the start of training and the pre-trained weights remain undisturbed.
        
- **Modified Forward Pass Equation:**
    
    $$h=W_0x+\Delta Wx=W_0x+\frac{\alpha}{r}(B\cdot A)x$$
    
    - **Variables:**
        
        - $h$: The output activation vector.
            
        - $x$: The incoming activation input vector.
            
        - $\alpha$: A constant scaling hyperparameter.
            
    - **Reasoning:** During inference or training, the input $x$ is multiplied by the frozen base weight $W_0$ and passed through the parallel adapter matrices $B$ and $A$. The adapter output is scaled by a constant factor $\frac{\alpha}{r}$. This scaling prevents the magnitude of the adapter's updates from dominating or altering the model's pre-trained representations as rank is scaled.
        
- **Rank-Stabilized LoRA Scaling (rsLoRA):**
    
    $$\text{Scaling factor}=\frac{\alpha}{\sqrt{r}}$$
    
    - **Reasoning:** In standard LoRA, scaling updates by $1 / r$ can damp the gradient signal as rank increases, leading to performance plateaus. Dividing instead by the square root of $r$ preserves the gradient scale across higher rank settings, enabling stable and continuous convergence at ranks as high as 512 or 2048.
        

## 3. Model Quantization and Numeric Representation (LLM.int8, NF4)

### Quantization

- **Definition:** The process of reducing the numerical precision of model weights and activations (converting from 32-bit or 16-bit floating-point representations to low-bit formats like 8-bit or 4-bit integers).
    
- **Trade-off:** Drastically reduces VRAM footprint during both training and inference (allowing larger models to fit on cheaper hardware). However, it introduces quantization errors that can degrade subtle reasoning capabilities and increase latency due to dynamic runtime dequantization overhead.
    

### Outlier Feature Phenomenon

- **Definition:** The sudden emergence of extreme, high-magnitude activation values (outliers) in specific hidden state dimensions once model size scales beyond 6.7 billion parameters.
    
- **Trade-off:** These outliers contain the core coordinate spaces of the model's logic. While they represent only 0.1% of all features, removing or zeroing them out causes the top-1 softmax probability mass to collapse by over 20%, completely destroying reasoning capability.
    

### LLM.int8() Mixed-Precision Quantization

- **Definition:** A quantization method that dynamically splits matrix multiplication into two streams based on activation magnitudes.
    
- **Trade-off:** It isolates outlier activation columns and processes them in lossless 16-bit precision, while performing 8-bit integer operations on the remaining 99.9% of normal dimensions. This preserves perplexity perfectly, but nearly doubles inference latency because of the dynamic overhead of routing and mixing precision formats.
    

### Vector-Wise Quantization

- **Definition:** An optimization that calculates a unique scaling factor for each individual row and column vector rather than applying a single uniform scale across the entire tensor.
    
- **Trade-off:** Prevents a single, extreme outlier feature in one row from scaling down and zeroing out the precision of normal values in adjacent rows, preserving fine-grained features.
    

### 4-bit NormalFloat (NF4) Quantization

- **Definition:** An information-theoretically optimal non-uniform 4-bit quantization scheme designed specifically for normally distributed neural network weights.
    
- **Trade-off:** Unlike uniform integer quantization (INT4), which spaces its bins evenly and leaves zero-centered Gaussian distributions with high reconstruction loss, NF4 spaces its 16 representational bins to hold equal probability mass under a normal distribution. It preserves baseline accuracy within 0.1% while compressing the model footprint by 4 times.
    

### Double Quantization (DQ)

- **Definition:** A hierarchical quantization scheme where the scaling constants used for block-wise weight quantization are themselves quantized.
    
- **Trade-off:** Standard block-wise quantization requires storing 32-bit floating-point scales, creating a metadata overhead of 1.0 bit per parameter. DQ quantizes these 32-bit constants into 8-bit integers with a block size of 256, compressing metadata overhead to approximately 0.127 bits per parameter with zero impact on quality.
    

### Paged Optimizers

- **Definition:** An optimization that uses NVIDIA's unified virtual memory to automatically page optimizer states between GPU VRAM and CPU system RAM.
    
- **Trade-off:** Prevents Out-Of-Memory (OOM) crashes during peak gradient spikes when training under tight hardware constraints, at the cost of transient bus transfer delays.
    

### Dequantization Overhead

- **Definition:** The latency bottleneck caused because physical Tensor Cores on current GPUs only support 16-bit operations (FP16/BF16), requiring 4-bit quantized weights to be dynamically decompressed back to 16-bit for every matrix multiplication.
    
- **Trade-off:** Reduces memory movement across bandwidth limits but increases execution time, resulting in a 30% to 50% slowdown in inference throughput for models like Llama-3.1.
    

### Mixed-Precision Outlier Decomposition Mathematics

The mathematics of isolating emergent activation outliers during matrix multiplication is formulated as a mixed-precision tensor decomposition.

- **Absmax Tensor Quantization (Uniform Baseline):**
    
    $$X_{\text{i8}}=\left\lfloor127\cdot\frac{X_{\text{f16}}}{\|X_{\text{f16}}\|_{\infty}}\right\rceil= \lfloor s_{X_{\text{f16}}}\cdot X_{\text{f16}} \rceil$$
    
    - **Variables:**
        
        - $X_{\text{f16}}$: The high-precision 16-bit floating-point activation tensor.
            
        - $X_{\text{i8}}$: The quantized 8-bit integer tensor.
            
        - $s_{X_{\text{f16}}}$: The scaling factor ($127 / \max(|X|)$).
            
    - **Reasoning:** Values are scaled into the discrete 8-bit signed integer range $[-127, 127]$ by dividing by the absolute maximum (infinity norm) of the tensor and rounding. If a massive outlier exists, $\|X_{\text{f16}}\|_{\infty}$ becomes huge, forcing normal activations to round to zero and causing severe model degradation.
        
- **LLM.int8() Matrix Multiplication Decomposition:**
    
    $$X\cdot W=X_{\text{normal}}\cdot W_{\text{normal}}+X_{\text{outlier}}\cdot W_{\text{outlier}}$$
    
    - **Variables:**
        
        - $X$: The activation matrix of size $s \times h$.
            
        - $W$: The weight matrix of size $h \times o$.
            
        - $X_{\text{outlier}}$: The subset of activation columns where at least one element exceeds a threshold (typically $\ge 6.0$).
            
        - $X_{\text{normal}}$: The remaining $99.9\%$ of normal activation columns.
            
    - **Reasoning:** By identifying and isolating outlier activation columns, we compute the normal coordinates using low-precision integer operations (INT8), while the highly sensitive outlier dimensions are computed in full FP16 precision. The outputs of both streams are accumulated and summed back into a final FP16 tensor.
        
- **4-bit NormalFloat (NF4) Quantile Construction:**
    
    $$q_i=\frac{1}{2}\left[Q\left(\frac{i}{17}\right)+Q\left(\frac{i+1}{17}\right)\right]\quad i\in\{0,\ldots,15\}$$
    
    - **Variables:**
        
        - $q_i$: The $i$-th quantization codebook value mapping to 16 representational bins.
            
        - $Q(\cdot)$: The quantile function (inverse cumulative distribution function) of a standard normal distribution $\mathcal{N}(0,1)$.
            
        - $\frac{i}{17}$: The boundaries of the 16 target bins.
            
    - **Reasoning:** Assuming pre-trained weights follow a Gaussian distribution, the codebook levels are defined by finding the midpoints of 16 equiprobable bins. This guarantees that each interval contains exactly the same expected probability density, mathematically minimizing the mean squared reconstruction error.
        

## 4. Model Pruning and Sparsity Architectures (Wanda, DepGraph)

### Pruning

- **Definition:** A model compression technique that improves inference efficiency by identifying and permanently removing parameters that contribute marginally to predictive performance.
    
- **Trade-off:** Can reduce physical model dimensions , but introduces activation shifts and severe accuracy degradation at moderate to high sparsity levels unless corrected by post-pruning fine-tuning.
    

### Unstructured Pruning

- **Definition:** A pruning strategy that zeroes out individual weights independently based on importance thresholds, without enforcing any structural layout constraints.
    
- **Trade-off:** Preserves task accuracy extremely well even at 50% sparsity , but yields zero physical speedup or VRAM memory reduction on standard hardware since standard deep learning libraries still process zeroed-out parameters as active dense weights.
    

### Structured Pruning

- **Definition:** A pruning strategy that physically deletes coherent parameter groups, such as entire neurons, layers, or feed-forward channels.
    
- **Trade-off:** Provides immediate, linear reductions in GPU memory usage and inference latency on standard commodity hardware. However, it severely disrupts internal representations, causing catastrophic accuracy collapse beyond 10% sparsity.
    

### Semi-Structured Pruning (N:M Sparsity)

- **Definition:** A hybrid pruning pattern where exactly $N$ non-zero weights are preserved within every contiguous block of $M$ parameters.
    
- **Trade-off:** Supports native hardware acceleration (using sparse Tensor Cores on modern GPUs to achieve up to a 2 times speedup by skipping zero-valued operands during matrix multiplication) , but requires strict matching patterns (like 2:4 or 4:8) and specialized inference backends to operate.
    

### WANDA (Weights and Activations)

- **Definition:** A one-shot, training-free pruning approach that ranks weight importance by the product of absolute weight magnitudes and runtime input activation norms.
    
- **Practical Role:** Prevents the removal of weak weights that are connected to highly active features , outperforming standard magnitude pruning without requiring the expensive inverse Hessian calculations used in methods like SparseGPT.
    

### DepGraph / Torch-Pruning

- **Definition:** A dependency-graph framework that models inter-layer dependencies to enable structured pruning of coupled, structurally interdependent parameter groups.
    
- **Practical Role:** Resolves layer dimension mismatches. For example, deleting an output channel in one layer forces the deletion of the corresponding input channel in the next; DepGraph groups these coupled parameters and prunes them jointly to maintain computational graph integrity.
    

### Sparsity and Importance Mapping Mathematics

Pruning enforces parameter sparsity through masking, and relies on data-aware activation norms to calculate structural importance.

- **Hadamard Weight Masking Formulation:**
    
    $$f(x;m\odot\alpha)$$
    
    - **Variables:**
        
        - $\alpha$: The original, dense pre-trained model parameter tensor.
            
        - $m$: A binary pruning mask of the same shape as $\alpha$, where $m\in\{0,1\}^{|\alpha|}$.
            
        - $\odot$: The element-wise Hadamard product operator.
            
    - **Reasoning:** To evaluate or deploy a pruned model, the weights are multiplied by the binary mask $m$. Weights mapped to $0$ are permanently zeroed out.
        
- **WANDA Weight Importance Score:**
    
    $$S_{ij}=|w_{ij}|\cdot\|X_j\|_2$$
    
    - **Variables:**
        
        - $w_{ij}$: The absolute weight magnitude connecting feature channel $j$ to output channel $i$.
            
        - $\|X_j\|_2$: The L2 norm of the input activation column $X_j$.
            
    - **Reasoning:** Traditional pruning only measures weight size ($|w_{ij}|$). WANDA scales this weight magnitude by how frequently and strongly the corresponding input feature activates over a calibration dataset ($\|X_j\|_2$). Weights connecting highly active features are preserved, while those linked to dead or inactive channels are pruned.
        
- **DepGraph Group-Level Importance Aggregation:**
    
    $$I(g)_j=\sum_{l\in g}I_l(j)$$
    
    - **Variables:**
        
        - $I(g)_j$: The consolidated importance score for channel index $j$ within the structurally coupled group $g$.
            
        - $I_l(j)$: The individual channel importance computed at layer $l$ within group $g$.
            
    - **Reasoning:** In structured pruning, deleting output dimensions in layer $A$ forces corresponding deletions in downstream layers. The DepGraph framework aggregates the channel importance scores across all coupled layers in group $g$. The channel with the lowest aggregated score is removed across the entire group, preserving shape consistency across the model.
        

## 5. Knowledge Distillation and Logit Optimization (KL, ULD, GOLD)

### Knowledge Distillation (KD)

- **Definition:** A compression technique where a smaller, efficient "student" model is trained to mimic the behavior and deductive patterns of a larger, high-capacity "teacher" model.
    
- **Trade-off:** Can yield substantial speedups and memory reductions , but risks catastrophic format collapse on structured tasks if prompt truncation or capacity limits prevent the student from learning formatting constraints.
    

### Dark Knowledge

- **Definition:** The latent, rich information contained within the teacher's soft probability distributions, specifically the relative ratios of the negative, non-target class predictions.
    
- **Practical Role:** Standard hard-label training only teaches the model which token is _correct_. Distilling dark knowledge teaches the student model the conceptual similarities and topology learned by the teacher.
    

### Soft Targets and softmax Temperature Scaling

- **Definition:** A probability-smoothing technique that scales raw model logits using a temperature hyperparameter before applying softmax.
    
- **Trade-off:** By raising the temperature, we amplify the signal of incorrect but semantically related tokens, helping the student model learn alternative reasoning pathways.
    

### Universal Logit Distillation (ULD)

- **Definition:** A cross-tokenizer logit distillation loss that uses optimal transport theory to align predictive distributions between teacher and student models that have entirely different vocabularies or architectures.
- **Practical Role:** Overcomes the core limitation of standard KL divergence, which requires identical tokenizers to prevent division-by-zero errors.
    
### GOLD (General On-Policy Logit Distillation)

- **Definition:** An on-policy distillation algorithm that extends ULD by introducing dynamic token merges for sequence alignment and 1:1 mapping fallback methods for vocabulary alignment.
    
- **Practical Role:** Resolves tokenizer misalignment on multi-step reasoning tasks by aligning student-generated outputs with the teacher's distribution without truncating sequences or losing semantic context.
    

### Distillation and Divergence Mathematics

Knowledge distillation operates by matching smoothed probability distributions, using either directional KL divergence or optimal transport distances.

- **Softmax with Temperature Scaling:**
    
    $$q_i=\frac{\exp\left(\frac{z_i}{T}\right)}{\sum_j\exp\left(\frac{z_j}{T}\right)}$$
    
    - **Variables:**
        
        - $z_i$: The unnormalized raw logit score for token $i$.
            
        - $T$: The temperature scaling parameter, where $T\ge 1$.
            
        - $q_i$: The softened target probability for token $i$.
            
    - **Reasoning:** When $T=1$, standard softmax produces a sharp distribution where the dominant target class receives near-total probability. Increasing $T$ above 1 softens the output, revealing the teacher's internal rankings and semantic similarities across non-target tokens.
        
- **Forward KL Divergence (Mean-Seeking / Zero-Avoiding):**
    
    $$D_{\text{KL}}(P_T\|P_S)=\sum_i P_T(i)\log\left(\frac{P_T(i)}{P_S(i)}\right)$$
    
    - **Reasoning:** Because the expectation is calculated under the teacher's distribution $P_T$, if the teacher places a non-zero probability on a token ($P_T(i)>0$), the student is forced to place a non-zero probability there as well ($P_S(i)>0$), otherwise the term explodes to infinity. This mean-seeking behavior forces the student's distribution to stretch across all of the teacher's modes, ensuring output diversity but potentially causing blurry, incoherent token sequences in structured formatting tasks.
        
- **Reverse KL Divergence (Mode-Seeking / Zero-Forcing):**
    
    $$D_{\text{KL}}(P_S\|P_T)=\sum_i P_S(i)\log\left(\frac{P_S(i)}{P_T(i)}\right)$$
    
    - **Reasoning:** Because the expectation is calculated under the student's distribution $P_S$, if the teacher places zero probability on a token ($P_T(i)\to 0$), the student is forced to place zero probability there as well ($P_S(i)\to 0$), to avoid division-by-zero. This mode-seeking behavior forces the student to focus strictly on the dominant peaks of the teacher's distribution, which is ideal for high-precision syntax tasks like JSON generation.
        
- **Universal Logit Distillation (ULD) / Wasserstein Loss:**
    
    $$W_p(P,Q)=\min_{T\in\Pi(P,Q)}\sum_{i=1}^{|\Omega_s|}\sum_{j=1}^{|\Omega_t|}T_{ij}C_{ij}^p$$
    
    - **Variables:**
        
        - $P,Q$: The output probability distributions from the teacher and student, respectively.
            
        - $\Pi(P,Q)$: The set of all joint coupling distributions mapping the student's vocabulary $\Omega_s$ to the teacher's vocabulary $\Omega_t$.
            
        - $C_{ij}$: The transport cost to transform $Q$ into $P$ (often set to 1 for mismatched tokens).
            
    - **Reasoning:** Standard KL divergence requires matching vocabularies; otherwise, unmatched tokens produce undefined values. ULD solves this by framing vocabulary alignment as an optimal transport problem. It uses Wasserstein distance to measure the minimal cost of mapping the student's token probabilities to the teacher's, allowing cross-tokenizer distillation.
        

## 6. Performance and Computational Cost Evaluation Metrics

During your oral exam, you must be prepared to defend both the task accuracy metrics and the physical computational cost metrics used to establish the cost-performance boundary.

### Proactive Task Metrics

- **Acc-P (Accuracy of Proactive Predictions):** Measures whether the model correctly determines if a proactive intervention is required.
    
- **MD (Missed Detections):** The rate at which the model remains passive when a proactive intervention was actually required.
    
- **FD (False Detections):** The rate at which the model triggers an intervention when no assistance was needed.
    
- **RMSE (Root Mean Square Error):** Measures the absolute variance in proactive score predictions on the 1-to-5 scale.
    
- **Precision, Recall, F1-Score (for Tool Calling):** Evaluates the set-based correctness of the predicted tool names against ground-truth tools.
    
- **Acc-Args (Accuracy of Tool Arguments):** Computes whether the dynamically generated parameters for the selected tools match the exact format and value criteria required for successful execution.
    

### Computational Cost Metrics

- **GPU Peak Memory (GB):** The maximum amount of VRAM consumed during model training or active batch inference. It represents the minimum hardware threshold required to prevent Out-Of-Memory crashes.
    
- **GPU Average Memory (GB):** The mean VRAM footprint sustained over the entire training or evaluation loop.
    
- **Batch Time (Average, Minimum, Maximum in seconds):** Measures the physical execution latency per batch during inference. This is critical for assessing real-time capability in continuous live environments.
    
- **Throughput (Samples per Second):** The average number of context frames or evaluation samples the optimized system can process per second. Higher throughput indicates a highly efficient, production-ready system.