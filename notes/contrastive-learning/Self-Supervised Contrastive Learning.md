2026-01-10 20:51

Status: #Ongoing 

Tags: [[Contrastive Learning]]
***
# TL;DR

- **Contrastive Learning** learns rich representations by pulling similar samples (positive pairs) closer while pushing diverse samples (negatives) apart.
- **Pretext Tasks** are fundamental for generating pseudo-labels and defining positive/negative pairs via data augmentation. While they filter noise, selecting the right task is critical as introduced biases can aid or hinder specific downstream applications.
- **Architectures** often employ dual encoders (Query/Key) or clustering mechanisms. 
- **InfoNCE** is the standard loss function, which maximizes the likelihood of identifying the correct positive sample among a set of negatives.
# Introduction

- **Contrastive Learning** is a training method that aims at grouping similar samples closer and diverse samples far from each other, based on a similarity metric.
- The main idea is to generate, for each sample in the training set, a transformed observation using a data augmentation technique (the technique used depends on the pretext task used for training). The transformed sample is considered a **positive sample**, while the rest of the samples in the batch/dataset are considered **negative samples**.
	- During training the model is trained to differentiate positive samples from the negative ones. The objective is to maximize the similarity between positive samples and minimize the similarity between negative samples.
	- A pretext task is used during training to achieve proper differentiation between representations.
- It has been widely used in domains like computer vision, for tasks such as image classification and image segmentation, and natural language processing (NLP). The self-supervised contrastive learning method has proven to be very effective for learning rich representations from large, unlabeled datasets.
# Pretext Tasks

- Pretext tasks are crucial in self-supervised learning because they force the model to learn rich, contextualized representations from unlabeled data. These tasks generate **pseudo-labels** based on inherent attributes of the data.
## Pros
- Forces the model to be invariant to specific transformations, while remaining discriminative to other samples in the dataset.
- It helps establishing the ground rules for creating positive and negative samples. The original sample (anchor) is transformed using a data augmentation technique based on the pretext task to create the positive sample, while all the other samples are used as negatives.
- It acts as a filter because it keeps the task-relevant information and discards the noise.
- The model trained with these pretext tasks can be used as a pre-trained model for downstream tasks such as classification, regression, etc.
## Cons
- Choosing the right pretext task is essential and is highly dependent on the specific downstream task, since the bias introduced during training can be harmful for some downstream tasks but beneficial for others.

> But the bias introduced through such augmentations could be a double-edged sword, as each augmentation encourages invariances to a transformation which can be beneficial in some cases and harmful in others. (Jaiswal, 7)
# Architectures

## End-to-End training

- This architecture employs two encoders: the Query Encoder ($Q$) and the Key Encoder ($K$). The Query Encoder is in charge of processing the anchor sample and the Key Encoder is in charge of processing the positive and negative samples in the batch.
- The main reason for using two distinct encoders to process the anchor and the positive sample is to force the model to learn what makes both samples the same despite the transformation used.
- This training method requires large batch sizes (between 2048 and 8192) to accumulate enough negative samples.
## Contrastive Clustering training

- This training method employs a clustering algorithm to cluster similar samples together. The goal is not only to make similar samples closer to each other, but also make samples that are similar to each other cluster together.
> (...) imagine we have an image of a cat in the training batch that is the current input to the model. During this pass, all other images in the batch are considered as negative. The issue arises when there are images of other cats in the negative samples. This condition forces the model to learn two images of cats as not similar during training despite both being from the same class. (Jaiswal, 11)
# Loss functions

- The most commonly used self-supervised contrastive loss function is the **InfoNCE** loss, where:
	- $q$ is the anchor embedding
	- $k_{+}$ and $k_{-}$ are the positive and negative samples, respectively.
	- $\text{sim}(.)$ is a similarity metric, usually cosine similarity.
	- $\tau$ is the temperature coefficient used to scale the similarities. It helps the model learn from **hard-negatives** (i.e., negative samples that are very similar to the anchor).
$$\mathcal{L}_{\text{InfoNCE}}=-\log{\left(\frac{\exp{(\text{sim}(q,k_{+})/\tau)}}{\exp{(\text{sim}(q,k_{+})/\tau)}+\sum^{K}_{i=0}\exp{(\text{sim}(q,k_{i})/\tau))}}\right)}$$
- This function calculates the negative log-likelihood of finding the correct positive sample from a set of candidates, which includes the positive and all the negative samples. In other words, in calculates how likely it is to find the positive sample for the current anchor.
***
# References
- Jaiswal, A., Babu, A. R., Zadeh, M. Z., Banerjee, D., Makedon, F. 2021. *A Survey on Contrastive Self-Supervised Learning*. Technologies, 9(1).