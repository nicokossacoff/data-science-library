import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.feature_selection import RFECV
from sklearn.decomposition import PCA

class RecursiveFeatureSelection:
    def __init__(self, estimator, score, step: int, folds: int, n_jobs: int, X_train: pd.DataFrame, y_train: pd.DataFrame | pd.Series, random_state: int = 42):
        '''
        Recursive Feature Selection strategy to select the best features for a given estimator.
        
        Parameters:
        -----------
        :estimator: object | A supervised learning estimator with a fit method that provides information about feature importance through either a coef_ or feature_importances_ attribute.
        :score: object | A scoring function to evaluate the features.
        :step: int | The number of features to remove at each iteration.
        :folds: int | Number of folds to use in the cross-validation.
        :n_jobs: int | Number of jobs to run in parallel.
        :X_train: DataFrame | Sample to be used in the feature selection. It should contain only the features we want to use to train the model.
        :y_train: DataFrame or Series | Sample to be used in the feature selection. It should contain only the target variable.
        :random_state: int | Random seed to be used in the cross-validation. Default is 42.       
        '''
        if not isinstance(X_train, pd.DataFrame):
            raise ValueError(f'X_train argument must be a DataFrame, a {type(X_train)} was given')
        if not isinstance(y_train, (pd.DataFrame, pd.Series)):
            raise ValueError(f'y_train argument must be either a DataFrame or a Series, a {type(y_train)} was given')

        self.estimator = estimator
        self.score = score
        self.step = step
        self.folds = folds
        self.n_jobs = n_jobs
        self.X_train = X_train
        self.y_train = y_train

        self.cv = StratifiedKFold(
            n_splits=self.folds,
            shuffle=True,
            random_state=random_state
        )

        self.rfe = RFECV(
            estimator=self.estimator,
            step=self.step,
            cv=self.cv,
            scoring=self.score,
            verbose=1,
            n_jobs=self.n_jobs
        )
    
    def run_strategy(self):
        self.rfe.fit(self.X_train, self.y_train)

    def get_feature_names(self) -> list:
        if isinstance(self.X_train, pd.DataFrame):
            return self.X_train.columns[self.rfe.support_].to_list()
        else:
            raise ValueError('Features must be a DataFrame')
    
    def get_dataframe(self) -> pd.DataFrame:
        self.df = pd.DataFrame(
            self.rfe.transform(self.X_train),
            columns=self.X_train.columns[self.rfe.support_]
        )
        
        if not self.df.index.equals(self.y_train.index):
            self.df = self.df.reset_index(drop=True)
            self.y_train = self.y_train.reset_index(drop=True)
        
        self.df['is_fraud'] = self.y_train
        return self.df