import torch
from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Optional

class TensorModel(BaseModel):
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

class BatchModel(BaseModel):
    """
    Pydantic model for validating a batch.

    Args:
        batch (Any): The batch to validate.
        batch_dimensions (int): The expected number of dimensions for the batch, default is 2.
        batch_shape (Optional[tuple]): The expected shape for the batch, default is None.
        batch_device (str): The expected device for the batch, default is 'cpu'.
    """
    # batch that holds the actual data to be validated.
    # We use the `Any` type to allow any type of data to be passed in and to avoid errors.
    # We validate the type later in the `validate_batch` method.
    batch: Any

    # Defines the expected number of dimensions for the batch.
    # If the user does not provide a value, it defaults to 2.
    batch_dimensions: int = 2

    # Defines the expected shape for the batch.
    # If the user does not provide a value, it defaults to None.
    # We use the `Optional` type to allow the user to specify a shape or not.
    batch_shape: Optional[tuple] = None

    # Defines the expected device for the batch.
    # If the user does not provide a value, it defaults to 'cpu'.
    # This field must be a string, so we validate it in the `validate_batch_device` method.
    batch_device: str = 'cpu'


    # The `field_validator` decorator is used to validate each field individually.
    # It allows us to define custom validation logic for each field.
    # We use it to validate the type and value of each field.

    # Validates the batch dimensions field.
    # Ensures it is a positive integer. This field will be used to check the dimensions of the batch.
    # This is an important step because we are going to use this value later to validate the batch.
    @field_validator('batch_dimensions')
    @classmethod
    def validate_batch_dimensions(cls, value):
        # Checks if the value is an integer
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        # Checks if the value is a positive integer
        if value <= 0:
            raise ValueError("Value must be a positive integer.")
        return value
    
    # Validates the batch shape field.
    # Ensures the field is a tuple or None.
    # This is an important step because we are going to use this value later to validate the batch.
    @field_validator('batch_shape')
    @classmethod
    def validate_batch_shape(cls, value):
        if value is not None and not isinstance(value, tuple):
            raise ValueError("Value must be a tuple or None.")
        return value
    
    # Validates the batch device field.
    # Ensures the field is a string.
    # This is an important step because we are going to use this value later to validate the batch
    @field_validator('batch_device')
    @classmethod
    def validate_batch_device(cls, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        return value

    # Validates the batch field.
    # Ensures it is a `torch.Tensor` object, checks if the data type is `torch.float32` and its not empty.
    # This is the first validation step for the batch. We only do basic validation that doesn't depend on other fields.
    @field_validator('batch')
    @classmethod
    def validate_batch_basic(cls, value):
        # Only do basic validation that doesn't depend on other fields
        if not isinstance(value, torch.Tensor):
            raise ValueError("Batch must be a torch.Tensor object.")
        
        if value.dtype != torch.float32:
            raise ValueError("Batch must be of type torch.float32.")
        
        if value.numel() == 0:
            raise ValueError("Batch must not be empty.")
        
        return value


    # The `model_validator` decorator is used to validate the model.
    # It allows us to define custom validation logics that depends on multiple fields.
    # We use the mode='after' argument to specify that this validation should be performed after the individual field were already validated and the model was initialized.

    # Validates the batch with constraints.
    # This is the second validation step for the batch. We do more specific validation that depends on other fields.
    @model_validator(mode='after')
    def validate_batch_with_constraints(self):
        # Get the batch
        batch = self.batch
        
        # Validate dimensions
        if batch.dim() != self.batch_dimensions:
            raise ValueError(f"Batch must have {self.batch_dimensions} dimensions.")
        
        # Validate shape if specified
        if (self.batch_shape is not None) and (batch.shape != self.batch_shape):
            raise ValueError(f"Batch shape must be {self.batch_shape}, got {batch.shape}.")
        
        # Validate device
        actual_device = str(batch.device)
        if actual_device != self.batch_device:
            raise ValueError(f"Device must be {self.batch_device}, got {actual_device}.")
        
        return self