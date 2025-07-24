from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
import os 
import pickle 

def evaluate_model(model, X_test, y_test):

    y_pred = model.predict(X_test)

    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)

    # RAE = ∑|y_pred - y| / ∑|y - ȳ|
    numerator   = sum(abs(y_pred - y_test))
    denominator = sum(abs(y_test - y_test.mean()))
    rae = numerator / denominator if denominator != 0 else float('nan')

    # 3. Regrouper dans un dict
    metrics = {
        "r2"  : r2,
        "mae" : mae,
        "rmse": rmse,
        "rae" : rae,
    }

    return metrics

def save_pipeline(pipeline_final):
    with open('model/pipeline_final.pkl', "wb") as f:
        pickle.dump(pipeline_final, f)

import os
from pathlib import Path

def load_pipeline(filepath="model/pipeline_final.pkl"):
    print("DEBUG cwd           :", os.getcwd())
    print("DEBUG fichier cherché:", Path(filepath).resolve())
    with open(filepath, "rb") as f:
        pipeline = pickle.load(f)

    print(f"✅ Pipeline chargé depuis : {filepath}")
    return pipeline
