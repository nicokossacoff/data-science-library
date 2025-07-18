import torch
import torch.nn as nn
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NeuralNetworkV0(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, device: torch.device):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
        
        self.to(device)
    
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.model(X)

class NeuralNetworkV1(nn.Module):
    """
    A simple feed-forward network with three hidden layers for binary classification.
    This model uses fully connected (linear) layers with ReLU activations between them.
    The output layer produces a single value (logit), suitable for binary classification tasks.

    Attributes:
        model (nn.Sequential): The sequential container holding the network layers.
    Args:
        input_size (int): The number of input features.
        hidden_size (list): A list of three integers specifying the number of units in each hidden layer.
        device (torch.device): The device on which to run the model (e.g., 'cpu' or 'cuda').
    Methods:
        forward(X):
            Performs a forward pass through the network.
    Example:
        model = NeuralNetworkV1(input_size=10, hidden_size=[64, 32, 16], device=torch.device('cpu'))
        output = model(torch.randn(5, 10))
    """

    def __init__(self, input_size: int, hidden_size: list, device: torch.device):
        # Initialize the base class
        super().__init__()

        # Validate the number of integers in the hidden_size list
        if len(hidden_size) != 3:
            raise ValueError("hidden_size must be a list of three integers.")
        
        # Define the model architecture
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size[0]),
            nn.ReLU(),
            nn.Linear(hidden_size[0], hidden_size[1]),
            nn.ReLU(),
            nn.Linear(hidden_size[1], hidden_size[2]),
            nn.ReLU(),
            nn.Linear(hidden_size[2], 1)
        )
        
        # Move the model to the specified device
        self.to(device)
    
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.model(X)
    
class NeuralNetworkV2(nn.Module):
    """
    A simple feed-forward network with three hidden layers for binary classification.
    This model uses fully connected (linear) layers with ReLU activations between them. It also includes dropout layers to prevent overfitting.
    The output layer produces a single value (logit), suitable for binary classification tasks.

    Attributes:
        model (nn.Sequential): The sequential container holding the network layers.
    Args:
        input_size (int): The number of input features.
        hidden_size (list): A list of three integers specifying the number of units in each hidden layer.
        device (torch.device): The device on which to run the model (e.g., 'cpu' or 'cuda').
    Methods:
        forward(X):
            Performs a forward pass through the network.
    Example:
        model = NeuralNetworkV1(input_size=10, hidden_size=[64, 32, 16], device=torch.device('cpu'))
        output = model(torch.randn(5, 10))
    """

    def __init__(self, input_size: int, hidden_size: list, dropout: float = None, device: torch.device = 'cpu'):
        # Initialize the base class
        super().__init__()

        # Validate the number of integers in the hidden_size list
        if len(hidden_size) != 3:
            raise ValueError("hidden_size must be a list of three integers.")
        if dropout is None:
            dropout = 0.0
            logging.warning("Dropout value is not provided. The network is trained without dropout layers.")
        
        # Define the model architecture
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size[0]),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size[0], hidden_size[1]),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size[1], hidden_size[2]),
            nn.ReLU(),
            nn.Linear(hidden_size[2], 1)
        )
        
        # Move the model to the specified device
        self.to(device)
    
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return self.model(X)