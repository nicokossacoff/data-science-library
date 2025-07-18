import matplotlib.pyplot
import numpy as np
import torch
import matplotlib
import sklearn.metrics as metrics

def plot_decision_boundary(model: torch.nn.Module, X: torch.Tensor, y: torch.Tensor, ax: matplotlib.axes.Axes = None):
    """
    Plots the decision boundary for a 2D PyTorch model.

    Args:
        model (torch.nn.Module): Trained PyTorch model.
        X (torch.Tensor): Input features of shape (n_samples, 2).
        y (torch.Tensor): Labels of shape (n_samples,).
    """
    # Move the model and the data to CPU (works better with Numpy and Matplotlib)
    model = model.to(device='cpu')
    X, y = X.cpu().numpy(), y.cpu().numpy()

    # Compute the boundaries for the plot using the min and max values of the input data
    # It adds a small margin to the min and max values for better visualization
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

    # Calculate the grid points
    # The numpy.meshgrid function uses two 1D arrays to create two 2D grid of points representing all the possible combinations of x and y values
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 101),
                         np.linspace(y_min, y_max, 101))
    grid = torch.from_numpy(np.column_stack((xx.ravel(), yy.ravel()))).float()

    # Set the model to evaluation mode and make predictions
    model.eval()
    with torch.inference_mode():
        # Get predictions from the model
        scores = model(grid)
    
    if scores.dim() == 1 or (scores.dim() == 2 and scores.shape[1] == 1):
        y_pred = torch.sigmoid(scores)
    else:
        y_pred = torch.softmax(scores, dim=1)

    # Reshape predictions to match the grid shape
    y_pred = y_pred.reshape(xx.shape).detach().numpy()

    # Create a new axes if not provided
    if ax is None:
        _, ax = matplotlib.pyplot.subplots(figsize=(8, 6))
    
    # Plot the decision boundary
    contour = ax.contourf(xx, yy, y_pred, cmap=matplotlib.pyplot.cm.RdYlBu, alpha=0.7)
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=matplotlib.pyplot.cm.RdYlBu)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_title('Decision Boundary')

    if ax is None:
        matplotlib.pyplot.show()
        
    return contour, scatter