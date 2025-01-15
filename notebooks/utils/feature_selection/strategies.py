import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.feature_selection import RFECV
from sklearn.decomposition import PCA

def adjust_indeces(X: pd.DataFrame, y: pd.DataFrame | pd.Series, feature_selection) -> pd.DataFrame:
    X = pd.DataFrame(feature_selection.transform(X), columns=X.columns[feature_selection.support_])
    
    if not X.index.equals(y.index):
        X = X.reset_index(drop=True)
        y = y.reset_index(drop=True)
    
    X['is_fraud'] = y
    return X
    

class RecursiveFeatureSelection:
    def __init__(self, estimator, score, step, folds, n_jobs):
        self.estimator = estimator
        self.score = score
        self.step = step
        self.folds = folds
        self.n_jobs = n_jobs

        self.rfe = RFECV(
            estimator=self.estimator,
            step=self.step,
            cv=self.folds,
            scoring=self.score,
            verbose=-1,
            n_jobs=self.n_jobs
        )
    
    def fit(self, X, y):
        self.rfe.fit(X, y)
