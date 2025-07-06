import torch
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    """
    Configuration class for managing device and hyperparameters for PyTorch neural network training.
    This class automatically detects the available computation device (CUDA, MPS, or CPU) and dynamically sets attributes for each hyperparameter provided in the input dictionary.
    
    Args:
        hyperparameters (dict): A dictionary containing hyperparameter names and their corresponding values.
    """

    def __init__(self, hyperparameters: dict):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        # Generate attributes from every hyperparameter
        for (key, value) in hyperparameters.items():
            setattr(self, key, value)
        
        logging.info(f"Current device: {self.device}")
