import torch
import torch.nn as nn

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