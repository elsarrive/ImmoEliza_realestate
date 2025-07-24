import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder

from config.config import (to_map_cols, epc_config)

# ===================================
# TRANSFORMERS
# ===================================
class MappingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mapping=None):
        self.mapping = mapping or to_map_cols
        self.modes_ = {}

    def fit(self, X, y=None):
        cols = [col for col in self.mapping.keys() if col in X.columns]

        for col in cols: 
            mode_values = X[col].mode()
            if len(mode_values) > 0:
                mode_original = mode_values[0]
                self.modes_[col] = self.mapping[col].get(mode_original, mode_original)   
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col, mapping_dict in self.mapping.items():
            if col in X_copy.columns:
                X_copy[col] = X_copy[col].map(mapping_dict)
        
        for col, mode_val in self.modes_.items():
            if col in X_copy.columns:
                if col == 'floodZoneType':
                    flood_zone_missing = self.mapping['floodZoneType'].get('POSSIBLE_FLOOD_ZONE', 3)
                    X_copy[col] = X_copy[col].fillna(flood_zone_missing)
                else:
                    X_copy[col] = X_copy[col].fillna(mode_val)
            
        return X_copy

class EPCtransformer(BaseEstimator, TransformerMixin):
    def __init__(self, dict_config=None):
        self.dict_config = dict_config or epc_config
        self.flandres = epc_config['flanders_provinces']
        self.wallonie = epc_config['wallonia_provinces']
        self.mapping = epc_config['mapping']
        self.modes_ = {}

    def fit(self, X, y=None):
        X_copy = X.copy()
        
        flanders_mask = (X_copy['province'].isin(self.flandres)) & (~X_copy['epcScore'].isin(epc_config['epc_unwanted'])) & (X_copy['epcScore'].notna())
        if flanders_mask.any():
            flanders_mode = X_copy[flanders_mask]['epcScore'].mode()
            if len(flanders_mode) > 0:
                self.modes_['flanders'] = self.mapping['flanders'].get(flanders_mode[0], flanders_mode[0])
    
        wallonia_mask = (X_copy['province'].isin(self.wallonie)) & (~X_copy['epcScore'].isin(epc_config['epc_unwanted'])) & (X_copy['epcScore'].notna())
        if wallonia_mask.any():
            wallonia_mode = X_copy[wallonia_mask]['epcScore'].mode()
            if len(wallonia_mode) > 0:
                self.modes_['wallonia'] = self.mapping['wallonia'].get(wallonia_mode[0], wallonia_mode[0])
        
        brussels_mask = (~X_copy['province'].isin(self.flandres + self.wallonie)) & (~X_copy['epcScore'].isin(epc_config['epc_unwanted'])) & (X_copy['epcScore'].notna())
        if brussels_mask.any():
            brussels_mode = X_copy[brussels_mask]['epcScore'].mode()
            if len(brussels_mode) > 0:
                self.modes_['brussels'] = self.mapping['brussels'].get(brussels_mode[0], brussels_mode[0])
        
        return self

    def transform(self, X):
        X_copy = X.copy()
        
        def transform_epc_row(row):
            province = row['province']
            epc_score = row['epcScore']

            if province in self.flandres:
                region = 'flanders'
            elif province in self.wallonie:
                region = 'wallonia'
            else: 
                region = 'brussels'
            
            defaut = self.modes_.get(region, region)
            if pd.isna(epc_score) or epc_score in epc_config['epc_unwanted']:
                return defaut
            
            return self.mapping[region].get(epc_score, defaut)

        X_copy['epcScore'] = X_copy.apply(transform_epc_row, axis=1)
        
        return X_copy

class OneHotTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, handle_unknown='ignore', drop='first'):

        self.columns = columns or ['type', 'province']
        self.handle_unknown = handle_unknown
        self.drop = drop
        self.encoders_ = {}
        self.feature_names_ = []

    def fit(self, X, y=None):
        X_copy = X.copy()
        
        for col in self.columns:
            if col in X_copy.columns:
                encoder = OneHotEncoder(
                    handle_unknown=self.handle_unknown, 
                    drop=self.drop,
                    sparse_output=False)
                
                encoder.fit(X_copy[[col]])
                self.encoders_[col] = encoder
                
                feature_names = [f"{col}_{cat}" for cat in encoder.categories_[0]]
                if self.drop == 'first':
                    feature_names = feature_names[1:]  
                self.feature_names_.extend(feature_names)
        
        return self

    def transform(self, X):
        X_copy = X.copy()
        
        for col in self.columns:
            if col in X_copy.columns and col in self.encoders_:
                encoded = self.encoders_[col].transform(X_copy[[col]])
                
                feature_names = [f"{col}_{cat}" for cat in self.encoders_[col].categories_[0]]
                if self.drop == 'first':
                    feature_names = feature_names[1:]
                
                encoded_df = pd.DataFrame(
                    encoded, 
                    columns=feature_names,
                    index=X_copy.index
                )
                
                X_copy = pd.concat([X_copy, encoded_df], axis=1)
                X_copy = X_copy.drop(columns=[col])
        
        return X_copy

    def get_feature_names_out(self, input_features=None):
        """Retourne les noms des features après transformation"""
        return self.feature_names_

