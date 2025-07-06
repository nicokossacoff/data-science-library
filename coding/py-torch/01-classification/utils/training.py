import torch
import torch.nn as nn
import numpy as np
from utils.metrics import *

def __convert_scores_to_probabilities(scores: torch.Tensor) -> torch.Tensor:
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

def validation_step(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader, criterion: torch.nn.Module, device: torch.device) -> float:
    """
    Performs a validation step on the model using the provided dataloader.

    Args:
        model (torch.nn.Module): PyTorch model to validate.
        dataloader (torch.utils.data.DataLoader): Dataloader for the validation data.
        criterion (torch.nn.Module): Criterion to compute the loss.
        device (str): Device to run the validation on ('cpu' or 'cuda').

    Returns:
        float: Average validation loss.
    """

    # Save the predictions and ground truth labels
    predictions = list()
    ground_truth = list()

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
            y_pred = __convert_scores_to_probabilities(scores)
            
            # Save predictions and ground truth
            predictions.append(y_pred.cpu().numpy())
            ground_truth.append(y.cpu().numpy())

            # Calculate the loss
            loss = criterion(scores, y.float())
            validation_loss_accum += loss.item()

    # Convert predictions and ground truth to numpy arrays
    predictions = np.concatenate(predictions, axis=0)
    ground_truth = np.concatenate(ground_truth, axis=0)

    # Calculate the average validation loss
    validation_loss = validation_loss_accum / len(dataloader)

    # Calculate metrics
    accuracy = binary_accuracy_score(ground_truth, predictions)
    f1_score = binary_f1_score(ground_truth, predictions)
    precision = binary_precision_score(ground_truth, predictions)
    recall = binary_recall_score(ground_truth, predictions)

    # Save the results in a dictionary
    result = {
        'loss': validation_loss,
        'accuracy': accuracy,
        'f1_score': f1_score,
        'precision': precision,
        'recall': recall
    }
    
    return result