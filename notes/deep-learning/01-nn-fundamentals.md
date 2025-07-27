***
# Introduction

- A **neural network** is a mathematical entity loosely inspired by the human brain. It uses interconnected units (also called neurons) in a layered structure resembling the human brain.
<figure>
	<img src='attachments/00-nn-architecture.png' style="display: block; margin: 0 auto;"/>
	<figcaption><b>Figure 1.</b> This is a simple neural network architecture. There are three main components: (1) the input layer, which contains the inputs to the model; (2) the hidden layers, which define the intermediate computations (or representations); and (3) the output layer, which contains the model's output.
	</figcaption>
</figure>
- Their main goal is to approximate some unknown function $\hat{f}$. The network defines a mapping (i.e., a flexible mathematical entity), $y=f(x,\theta)$, that tries to best approximate this function.
- The most common neural network architecture is called **feedforward** neural network, and that's because the information flows through the function starting at the input vector ($x$), then moving through the intermediate representations, and finally to the output ($y$).
- These networks are typically represented by composing together many different functions, and are associated with a directed acyclic graph (DAG). For example, the neural network in Figure 1 could be represented as:$$f(x)=f^{(3)}\left(f^{(2)}\left(f^{(1)}(x)\right)\right)$$
	- Each function $f^{(i)}$ represents a layer in the network. In the example above, $f^{(1)}$ represents the first hidden layer, $f^{(2)}$ is the second hidden layer, and so on. 
		- The number of layers defines the depth of the model.
	- These functions are vector-to-vector functions, where every element in the output vector is the activation of a hidden-unit. 
- During training, we want $f(x)\longrightarrow\hat{f}(x)$. The training data provides us with a target output, $y$, for every training point, $x$. Thus, the training examples specify what the output layer should return at each point, i.e., given $x$ it must return a value close to $y$.
- The behavior of the hidden layers is not specified explicitly by the training data, so the learning algorithm must decide how to use these layers. This is what makes the neural network learn the patterns in the data.

## Hidden-units

- Hidden-units are artificial neurons or nodes that reside within the hidden layers of a neural network. These units significantly contribute to the learning process by learning meaningful representations of the input data.
- Each hidden unit receives inputs from all the units in the preceding layer (this could be either the input layer or another hidden layer). These inputs are then combined using a weighted sum and passed through an activation function (e.g., ReLU, tanh, etc.) that introduces non-linearity, giving the neural network the capacity to learn complex patterns.
<figure>
	<img src='attachments/01-hidden-unit-calc.png' style="display: block; margin: 0 auto;"/>
	<figcaption><b>Figure 2.</b> Activation of a hidden-unit. It receives the weighted sum of the inputs of the preceding layer and then pass it through a non-linear activation function.
	</figcaption>
</figure>