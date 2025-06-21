import torch
from pydantic import BaseModel, field_validator
from typing import Any

class Tensor(BaseModel):
    """
    Pydantic model for validating a `torch.Tensor`.

    Args:
        tensor (torch.Tensor): The tensor to validate.
        tensor_dimensions (int): The expected number of dimensions for the tensor, default is 2.
    """
    tensor: Any
    tensor_dimensions: int = 2

    # Validates the tensor dimensions field.
    # Ensures it is a positive integer. This field will be used to check the dimensions of the tensor.
    # Defaults to 2.
    @field_validator('tensor_dimensions')
    @classmethod
    def validate_tensor_dimensions(cls, value):
        # Validates that the tensor dimensions attribute is an integer.
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        # Validates that the tensor dimensions attribute is a positive integer.
        if value <= 0:
            raise ValueError("Value must be a positive integer.")
        return value

    # Validates the tensor field.
    # Ensures it is a `torch.Tensor` object, checks its data type, dimensions, and ensures it is not empty.
    @field_validator('tensor')
    @classmethod
    def validate_tensor(cls, value, info):
        # Validates that the tensor field is a `torch.Tensor` object.
        if not isinstance(value, torch.Tensor):
            raise ValueError("Value must be a torch.Tensor object.")
        
        # Validates that the tensor field is of type `torch.float32`.
        # We use this data type as it is commonly used in deep learning tasks.
        if value.dtype != torch.float32:
            raise ValueError("Tensor must be of type torch.float32.")
        
        # Validates the dimensions of the tensor.
        # The expected dimensions are retrieved from the model's data (already validated).
        expected_dimensions = info.data.get('tensor_dimensions', 2)
        if value.dim() != expected_dimensions:
            raise ValueError("Tensor must be a 2D tensor.")
        
        # Validates that the tensor is not empty.
        if value.size(0) == 0 or value.size(1) == 0:
            raise ValueError("Tensor must not be empty.")
        return value