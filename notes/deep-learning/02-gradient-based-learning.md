***
# Introduction

- We train neural networks using the standard procedure common to many machine learning models:
	- First, we define a **loss function**, which measures the discrepancy between the model's prediction and the target output.
	- Second, we specify an **optimization algorithm**, responsible for updating the model's parameters to minimize the loss function.
- However, due to the non-linearity introduced by the activation functions, the loss landscape of neural networks is typically **non-convex**[^1]. As a result, neural networks are usually trained using iterative, gradient-based optimization algorithms that aim to reduce the loss to a sufficiently low value.
- Because the loss function is non-convex, gradient descent algorithms offer no guarantee of convergence to a global minimum and are highly sensitive to the initial parameter values.

# Loss functions

- 

[^1]: A convex function has a single **global** minimum, while non-convex functions may have multiple **local** minima and **saddle points**.

