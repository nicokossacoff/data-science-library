import numpy as np
import sklearn.metrics as metrics

def binary_accuracy_score(y_true: np.ndarray, y_pred: np.ndarray, ths: float = 0.5) -> float:
    """
    Calculate the accuracy of predictions.

    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.

    Returns:
        float: Accuracy score.
    """
    # Apply threshold for binary classification
    y_pred = (y_pred >= ths).astype(int)

    # Calculate accuracy
    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.accuracy_score(y_true, y_pred)

def binary_precision_score(y_true: np.ndarray, y_pred: np.ndarray, ths: float = 0.5) -> float:
    """
    Calculate the precision of predictions.

    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.

    Returns:
        float: Precision score.
    """
    y_pred = (y_pred >= ths).astype(int)

    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.precision_score(y_true, y_pred)

def binary_recall_score(y_true: np.ndarray, y_pred: np.ndarray, ths: float = 0.5) -> float:
    """
    Calculate the recall of predictions.

    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.

    Returns:
        float: Recall score.
    """
    y_pred = (y_pred >= ths).astype(int)

    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.recall_score(y_true, y_pred)

def binary_f1_score(y_true: np.ndarray, y_pred: np.ndarray, ths: float = 0.5) -> float:
    """
    Calculate the F1 score for binary classification.

    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted probabilities.
        ths (float, optional): Threshold for binary classification. Defaults to 0.5.

    Returns:
        float: F1 score.
    """
    y_pred = (y_pred >= ths).astype(int)

    if len(y_true) == 0:
        return 0.0
    else:
        return metrics.f1_score(y_true, y_pred)