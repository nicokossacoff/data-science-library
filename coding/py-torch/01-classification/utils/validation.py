import torch
from pydantic import BaseModel, field_validator
from typing import Any

class Tensor(BaseModel):
    """
    Pydantic model for validating a 2D `torch.Tensor`.

    Args:
        tensor (torch.Tensor): A 2D tensor of type float32.
    """
    tensor: Any

    @field_validator('tensor')
    @classmethod
    def validate_tensor(cls, value):
        if not isinstance(value, torch.Tensor):
            raise ValueError("Value must be a torch.Tensor object.")
        if value.dtype != torch.float32:
            raise ValueError("Tensor must be of type torch.float32.")
        if value.dim() != 2:
            raise ValueError("Tensor must be a 2D tensor.")
        if value.size(0) == 0 or value.size(1) == 0:
            raise ValueError("Tensor must not be empty.")
        return value