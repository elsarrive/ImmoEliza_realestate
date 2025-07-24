from sklearn.base import BaseEstimator, TransformerMixin
from config.config import (
    bool_cols, numerical_median_cols, numerical_zero_cols, numerical_conditional_dict, to_drop_cols)

# ===================================
# IMPUTERS
# ===================================
def bool_transform(X, columns = None):
    """ 
    - Fill missing value with 'False' 
    - Convertion of boolean to binary value
    - Return dataframe modified
    """
    X_copy = X.copy()
    columns = columns or bool_cols
    
    bool_map = {
        'True' : 1, 
        True : 1, 
        'False' : 0,
        False : 0
    }
    for col in columns:
           if col in X_copy.columns:  
            X_copy[col] = X_copy[col].map(bool_map).fillna(0).astype(int)
    
    return X_copy
        
    
class NumMedianImputer(BaseEstimator, TransformerMixin):
    """ 
     - Fill missing value with th median
     - Save the median in a dictionnary 
     - Return dataframe modified
    """
    def __init__(self, columns=None):
        self.columns = columns or numerical_median_cols
        self.medians_ = {}

    def fit(self, X, y=None):
        cols = [col for col in self.columns if col in X.columns]

        for col in cols: 
            self.medians_[col] = X[col].median()
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col, median_val in self.medians_.items():
            if col in X_copy.columns:
                X_copy[col] = X_copy[col].fillna(median_val)
        return X_copy

def num_zero_imputer(X, columns = None):
    X_copy = X.copy()
    cols = [col for col in X_copy.columns if col in numerical_zero_cols]

    for col in cols: 
        X_copy[col] = X_copy[col].fillna(0)

    return X_copy
    
class NumConditionalImputer(BaseEstimator, TransformerMixin):
    def __init__(self, dict_config=None):
        self.dict_config = dict_config or numerical_conditional_dict
        self.strategy = self.dict_config['strategy']
        self.mapping = self.dict_config['columns']
        self.medians_ = {}
        
    def fit(self, X, y=None):
        for dep_var in self.mapping.keys():
            if dep_var in X.columns:
                self.medians_[dep_var] = X[dep_var].median()
        return self

    def transform(self, X):
        X_copy = X.copy()

        for dep_var, inc_var in self.mapping.items(): 
            if (dep_var in X_copy.columns) and (inc_var in X_copy.columns):
                mask_true = (X_copy[inc_var] == True) & (X_copy[dep_var].isna())
                if mask_true.any():
                    if self.strategy['if_true'] == 'median':
                        X_copy.loc[mask_true, dep_var] = self.medians_[dep_var]
                    else: 
                        X_copy.loc[mask_true, dep_var] = self.strategy['if_true']
                    

                mask_false = (X_copy[inc_var] == 'False') & (X_copy[dep_var].isna())
                if mask_false.any():
                        X_copy.loc[mask_false, dep_var] =  self.strategy['if_false']
                   
                mask_missing = (X_copy[inc_var].isna()) & (X_copy[dep_var].isna())
                if mask_missing.any():
                        X_copy.loc[mask_missing, dep_var] =  self.strategy['if_missing']

        return X_copy

# ===================================
# DROPPING
# ===================================
def drop_rows(X, columns = None):
    
    X_copy = X.copy()
    columns = columns or to_drop_cols

    X_copy = X_copy.drop(columns=[col for col in columns if col in X.columns])
    return X_copy