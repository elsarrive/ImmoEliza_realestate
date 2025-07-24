import pandas as pd
from sklearn.model_selection import train_test_split
from processing.pipelines import create_full_pipeline
from model.model_pip import evaluate_model, save_pipeline

df = pd.read_csv('data/dataset_to_preprocess.csv', sep=",")

y = df['price']
X = df.drop(['price'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline = create_full_pipeline()
pipeline.fit(X_train, y_train)

results = evaluate_model(pipeline, X_test, y_test)
save_pipeline(pipeline)

print(results)