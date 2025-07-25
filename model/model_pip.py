from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
import os 
import pickle
from azure.storage.blob import BlobServiceClient

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

def load_pipeline(filepath="model/pipeline_final.pkl", local=True):
    if not local :
        conn_str = os.getenv("AZURE_CONNECTION_STRING")
        blob_svc = BlobServiceClient.from_connection_string(conn_str)
        container = blob_svc.get_container_client("model")
        data = container.get_blob_client("pipeline_final.pkl").download_blob().readall()

        
        print(f"Pipeline chargé depuis Azure Blob Storage!")
        return pickle.loads(data)
    
    else:
        with open(filepath, "rb") as f:
            pipeline = pickle.load(f)

        print(f"Pipeline chargé depuis : {filepath}")
        return pipeline
