import torch
import sklearn.metrics as metrics

def binary_accuracy_score(y_true: torch.Tensor, y_pred: torch.Tensor, ths: float = 0.5) -> float:
    """
    Calculate the accuracy of predictions.
    
    Args:
        y_true (torch.Tensor): True labels.
        y_pred (torch.Tensor): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.
    
    Returns:
        float: Accuracy score.
    """
    # Move tensors to CPU
    y_true = y_true.cpu().numpy()
    y_pred = y_pred.cpu().numpy()

    # Apply threshold for binary classification
    y_pred = (y_pred >= ths).astype(int)

    # Calculate accuracy
    # If y_true is empty, return 0.0 to avoid division by zero
    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.accuracy_score(y_true, y_pred)
    
def binary_precision_score(y_true: torch.Tensor, y_pred: torch.Tensor, ths: float = 0.5) -> float:
    """
    Calculate the precision of predictions.
    
    Args:
        y_true (torch.Tensor): True labels.
        y_pred (torch.Tensor): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.
    
    Returns:
        float: Precision score.
    """
    # Move tensors to CPU
    y_true = y_true.cpu().numpy()
    y_pred = y_pred.cpu().numpy()

    # Apply threshold for binary classification
    y_pred = (y_pred >= ths).astype(int)

    # Calculate precision
    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.precision_score(y_true, y_pred)

def binary_recall_score(y_true: torch.Tensor, y_pred: torch.Tensor, ths: float = 0.5) -> float:
    """
    Calculate the recall of predictions.
    
    Args:
        y_true (torch.Tensor): True labels.
        y_pred (torch.Tensor): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.
    
    Returns:
        float: Recall score.
    """
    # Move tensors to CPU
    y_true = y_true.cpu().numpy()
    y_pred = y_pred.cpu().numpy()

    # Apply threshold for binary classification
    y_pred = (y_pred >= ths).astype(int)

    # Calculate recall
    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.recall_score(y_true, y_pred)

def binary_f1_score(y_true: torch.Tensor, y_pred: torch.Tensor, ths: float = 0.5) -> float:
    """
    Calculate the F1 score for binary classification.
    
    Args:
        y_true (torch.Tensor): True labels.
        y_pred (torch.Tensor): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.
    
    Returns:
        float: F1 score.
    """
    # Move tensors to CPU
    y_true = y_true.cpu().numpy()
    y_pred = y_pred.cpu().numpy()

    # Apply threshold for binary classification
    y_pred = (y_pred >= ths).astype(int)

    # Calculate F1 score
    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.f1_score(y_true, y_pred)