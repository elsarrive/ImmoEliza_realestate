import xgboost as xgb
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

from processing.transformers    import (MappingTransformer, EPCtransformer, OneHotTransformer)
from processing.preprocessing   import (bool_transform, NumMedianImputer, num_zero_imputer,
                                        NumConditionalImputer, drop_rows)
from config.config              import (numerical_median_cols, numerical_conditional_dict, to_map_cols)


def create_preprocessing_pipeline():
    preprocessing_steps = [
        ('bool_transformer', FunctionTransformer(bool_transform)),
        ('median_transformer', NumMedianImputer(columns=numerical_median_cols)),
        ('zero_transformer', FunctionTransformer(num_zero_imputer)),
        ('conditionnal_transformer', NumConditionalImputer(numerical_conditional_dict)),
        ('mapping', MappingTransformer(to_map_cols)),
        ('epc_transformer', EPCtransformer()),
        ('onehot_transformer', OneHotTransformer()),
        ('drop_rows', FunctionTransformer(drop_rows))
        ]
    
    return Pipeline(preprocessing_steps)

def create_full_pipeline():
    preprocessing_pipeline = create_preprocessing_pipeline()
    xgb_model = xgb.XGBRegressor(n_estimators=3000, random_state=43, learning_rate=0.05, subsample=0.8)
    full_pipeline = [
        ('preprocessing', preprocessing_pipeline),
        ('model', xgb_model)
    ]

    return Pipeline(full_pipeline)

