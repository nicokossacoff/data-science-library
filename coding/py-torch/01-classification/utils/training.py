import torch
import torch.nn as nn
import torchmetrics
import warnings

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_scores_to_probabilities(scores: torch.Tensor) -> torch.Tensor:
    """
    Converts model scores to probabilities based on the number of output classes.

    Args:
        scores (torch.Tensor): Model output scores.

    Returns:
        torch.Tensor: Probabilities after applying sigmoid or softmax.
    """
    if scores.dim() == 1 or (scores.dim() == 2 and scores.shape[1] == 1):
        return torch.sigmoid(scores)
    else:
        return torch.softmax(scores, dim=1)
    
def compute_metrics(predictions: torch.Tensor, ground_truth: torch.Tensor, device: torch.device, task: str = 'binary', num_classes: int = 2, threshold: float = 0.5) -> dict:
    """
    Computes accuracy, F1 score, precision, and recall for the given predictions and ground truth.

    Args:
        predictions (torch.Tensor): Model predictions (probabilities for binary, class indices for multiclass).
        ground_truth (torch.Tensor): Ground truth labels.
        device (torch.device): Device to run the metrics on ('cpu' or 'cuda').
        task (str): Type of task ('binary' or 'multiclass').
        num_classes (int): Number of classes for multiclass classification.
        threshold (float): Threshold for binary classification (only used when task='binary').

    Returns:
        dict: Dictionary containing accuracy, F1 score, precision, and recall.
    """
    try:
        if task not in ['binary', 'multiclass']:
            raise ValueError("Task must be either 'binary' or 'multiclass'.")
        # Since MPS devices may have compatibility issues with some torchmetrics functions, we move the tensors to CPU
        if device.type == 'mps':
            predictions = predictions.cpu()
            ground_truth = ground_truth.cpu()

        # Compute metrics based on the task type
        if task == 'binary':
            return {
                'accuracy': torchmetrics.functional.accuracy(predictions, ground_truth, task='binary', threshold=threshold),
                'f1_score': torchmetrics.functional.f1_score(predictions, ground_truth, task='binary', threshold=threshold),
                'precision': torchmetrics.functional.precision(predictions, ground_truth, task='binary', threshold=threshold),
                'recall': torchmetrics.functional.recall(predictions, ground_truth, task='binary', threshold=threshold)
            }
        elif task == 'multiclass':
            return {
                'accuracy': torchmetrics.functional.accuracy(predictions, ground_truth, task='multiclass', num_classes=num_classes),
                'f1_score': torchmetrics.functional.f1_score(predictions, ground_truth, task='multiclass', num_classes=num_classes, average='weighted'),
                'precision': torchmetrics.functional.precision(predictions, ground_truth, task='multiclass', num_classes=num_classes, average='weighted'),
                'recall': torchmetrics.functional.recall(predictions, ground_truth, task='multiclass', num_classes=num_classes, average='weighted')
            }
    except Exception as error:
        # Fallback to CPU computation if there are device-specific issues
        warnings.warn(f"Device-specific metric computation failed, falling back to CPU: {error}")
        predictions_cpu = predictions.cpu()
        ground_truth_cpu = ground_truth.cpu()
        
        if task == 'binary':
            return {
                'accuracy': torchmetrics.functional.accuracy(predictions_cpu, ground_truth_cpu, task='binary', threshold=threshold),
                'f1_score': torchmetrics.functional.f1_score(predictions_cpu, ground_truth_cpu, task='binary', threshold=threshold),
                'precision': torchmetrics.functional.precision(predictions_cpu, ground_truth_cpu, task='binary', threshold=threshold),
                'recall': torchmetrics.functional.recall(predictions_cpu, ground_truth_cpu, task='binary', threshold=threshold)
            }
        elif task == 'multiclass':
            return {
                'accuracy': torchmetrics.functional.accuracy(predictions_cpu, ground_truth_cpu, task='multiclass', num_classes=num_classes),
                'f1_score': torchmetrics.functional.f1_score(predictions_cpu, ground_truth_cpu, task='multiclass', num_classes=num_classes, average='weighted'),
                'precision': torchmetrics.functional.precision(predictions_cpu, ground_truth_cpu, task='multiclass', num_classes=num_classes, average='weighted'),
                'recall': torchmetrics.functional.recall(predictions_cpu, ground_truth_cpu, task='multiclass', num_classes=num_classes, average='weighted')
            }


def binary_validation_step(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader, criterion: torch.nn.Module, device: torch.device, ths: float = 0.5) -> dict:
    """
    Performs a validation step on the model using the provided dataloader for binary classification.

    Args:
        model (torch.nn.Module): PyTorch model to validate.
        dataloader (torch.utils.data.DataLoader): Dataloader for the validation data.
        criterion (torch.nn.Module): Criterion to compute the loss.
        device (torch.device): Device to run the validation on ('cpu', 'cuda', or 'mps').
        ths (float): Threshold for binary classification (default: 0.5).

    Returns:
        dict: Dictionary containing average validation loss, accuracy, F1 score, precision, and recall.
    """
    # We are going to use these lists to save the predictions and ground truth labels for each batch
    predictions = []
    ground_truth = []

    # Initialize the loss accumulator
    validation_loss_accum = 0.0

    for (X, y) in dataloader:
        # Set the model to evaluation mode
        model.eval()

        # Start inference mode
        with torch.inference_mode():
            # Move data to the specified device
            X, y = X.to(device), y.to(device)
            
            # Forward pass
            scores = model(X)
            scores = scores.squeeze()

            # Convert scores to probabilities
            # If the model outputs only one score for every example in the dataset, then this function applies the sigmoid function.
            # If the model outputs multiple scores, we apply softmax for multi-class classification.
            y_pred = convert_scores_to_probabilities(scores)
            
            # Save predictions and ground truth as tensors (keep on same device)
            predictions.append(y_pred.detach())
            ground_truth.append(y.detach())

            # Calculate the loss
            loss = criterion(scores, y.float())
            validation_loss_accum += loss.item()

    # Concatenate all predictions and ground truth tensors (stays on device)
    predictions = torch.cat(predictions, dim=0)
    ground_truth = torch.cat(ground_truth, dim=0)

    # Calculate the average validation loss
    validation_loss = validation_loss_accum / len(dataloader)

    # Calculate metrics using the helper function (torchmetrics will handle thresholding internally)
    metrics = compute_metrics(predictions, ground_truth, device, task='binary', threshold=ths)

    # Save the results in a dictionary
    result = {
        'loss': validation_loss,
        'accuracy': metrics['accuracy'].item(),
        'f1_score': metrics['f1_score'].item(),
        'precision': metrics['precision'].item(),
        'recall': metrics['recall'].item()
    }
    
    return result

def multiclass_validation_step(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader, criterion: torch.nn.Module, device: torch.device, num_classes: int) -> dict:
    """
    Performs a validation step on the model using the provided dataloader for multiclass classification.

    Args:
        model (torch.nn.Module): PyTorch model to validate.
        dataloader (torch.utils.data.DataLoader): Dataloader for the validation data.
        criterion (torch.nn.Module): Criterion to compute the loss.
        device (torch.device): Device to run the validation on ('cpu', 'cuda', or 'mps').
        num_classes (int): Number of classes for multiclass classification.

    Returns:
        dict: Dictionary containing average validation loss, accuracy, F1 score, precision, and recall.
    """

    # Save the predictions and ground truth labels
    predictions = []
    ground_truth = []

    # Initialize the loss accumulator
    validation_loss_accum = 0.0

    for (X, y) in dataloader:
        # Set the model to evaluation mode
        model.eval()

        # Start inference mode
        with torch.inference_mode():
            # Move data to the specified device
            X, y = X.to(device), y.to(device)
            
            # Forward pass
            scores = model(X)
            scores = scores.squeeze()

            # Convert scores to probabilities
            # If the model outputs a single score, we apply sigmoid for binary classification.
            # If the model outputs multiple scores, we apply softmax for multi-class classification.
            y_pred = convert_scores_to_probabilities(scores)

            # Convert predictions to class labels
            # For multiclass classification, we take the argmax across the class dimension.
            y_pred = torch.argmax(y_pred, dim=1)
            
            # Save predictions and ground truth as tensors (keep on same device)
            predictions.append(y_pred.detach())
            ground_truth.append(y.detach())

            # Calculate the loss
            loss = criterion(scores, y.float())
            validation_loss_accum += loss.item()

    # Concatenate all predictions and ground truth tensors (stays on device)
    predictions = torch.cat(predictions, dim=0)
    ground_truth = torch.cat(ground_truth, dim=0)

    # Calculate the average validation loss
    validation_loss = validation_loss_accum / len(dataloader)

    # logging.info(f"Prediction probabilities | min: {predictions.min():.4f} | max: {predictions.max():.4f} | mean: {predictions.mean():.4f}")

    
    # Calculate metrics using the helper function
    metrics = compute_metrics(predictions, ground_truth, device, task='multiclass', num_classes=num_classes)

    # Save the results in a dictionary
    result = {
        'loss': validation_loss,
        'accuracy': metrics['accuracy'].item(),
        'f1_score': metrics['f1_score'].item(),
        'precision': metrics['precision'].item(),
        'recall': metrics['recall'].item()
    }
    
    return result