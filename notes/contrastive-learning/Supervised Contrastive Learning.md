2026-01-11 15:52

Status: #Ongoing 

Tags: [[Contrastive Learning]]
***
# TL;DR

- **Supervised Contrastive Learning** leverages available class labels to guide the representation learning process, effectively overcoming the inherent limitations of self-supervised methods.
- **False Negatives & Sampling**: It addresses the issue where self-supervised models inadvertently push apart distinct samples of the same class. Instead, it utilizes *all* samples of the same class in a batch as positive pairs, ensuring tighter intra-class clustering.
- **Task Relevance**: By relying on class labels rather than pretext task invariances, the model extracts features that are directly relevant to the downstream task, avoiding the potential bias introduced by specific data augmentations.
- **Generalized InfoNCE Loss**: The loss function is adapted to handle multiple positive pairs per anchor, averaging the log-likelihood across all same-class samples in the batch to produce more robust embeddings.
# Introduction

- The [[Self-Supervised Contrastive Learning]] method has revolutionized representation learning by enabling the model to learn reach representations from unlabeled data.
- This method faces inherent limitations due to the lack of labels. The **Supervised Contrastive Learning** can avoid these limitations by leveraging label information.
# Limitations solved

- These limitations found in the self-supervised contrastive learning method, that can be avoid in the supervised learning method, are:
	- The model treats only a transformed version of the anchor as a positive instance, while all the other instances in the batch are treated as negatives. During training, the anchor and the positive instance are pull together, while the negative instances are pushed away.
		- This is a problem, because samples from the same semantic class are being pushed apart in the embedding space.
		- When class labels are available, all samples from the same class can be used as positive instances. The model can now learn to only push away instances from different classes.
	- The model is trained with only one positive sample for each anchor. This limits the model's ability to learn rich representation, and most of the time it only learns to be invariant to a specific transformation.
		- In the supervised learning paradigm multiple positive instances are sampled from the current batch, instead of using different views from the same sample.
	- The performance of self-supervised contrastive models on downstream tasks are highly dependent of the pretext task used during training. The pretext task used during training defines the data augmentation technique needed to transform the data.
		- During training the model tries to filter task-relevant information. If the pretext task is not correctly defined, this information will simply be irrelevant for the downstream task.
		- In the supervised learning paradigm the task-relevant information is included in the class-labels, bypassing the need for pretext tasks to extract relevant information.
# Loss functions

- In Kohsla et al., the authors proposed the following contrastive loss function, which is a adaptation of the InfoNCE loss, a very popular self-supervised contrastive loss:
$$\mathcal{L}=-\sum_{i\in I}\frac{1}{|P(i)|}\sum_{p\in P(i)}\log{\left(\frac{\exp{(z_{i}\cdot z_{p}/\tau)}}{\sum_{a\in A(i)}\exp{(z_{i}\cdot z_{a}/\tau)}}\right)}$$
  - Here:
	- $I\equiv\{1,\ldots,2N\}$ includes all samples in the batch (original and augmented).
	- $z_{i}$ is the anchor sample and $z_{j(i)}$ is its augmented version.
	- $A(i)\equiv I\textbackslash\{i\}$  includes all samples in the batch (original and augmented) except the anchor sample.
	- $P(i)\equiv\{p\in A(i):y_{p}=y_{i}\}$ includes all samples with the same class label than the anchor (i.e., the positive pairs). $|P(i)|$ is its cardinality.
- This function calculates the average of the log-likelihood for all positive pairs of an anchor. This formulation forces the model to pay close attention to all positive pairs, resulting in a more robust clustering.
***
# References
- Khosla, P., Teterwak, P., Wang, C., Sarna, A., Tian, Y., Isola, P., Maschinot, A., Liu, C., Krishnan, D. 2020. _Supervised Contrastive Learning_. Advances in Neural Information Processing Systems, 33, 18661–18673.