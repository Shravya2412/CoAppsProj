import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the CSV file
    csv_file_path = os.path.join(current_dir, "data", "Top Indian Places to Visit.csv")

    # Load the dataset
    data = pd.read_csv(csv_file_path)

    # Dropping missing values
    data.dropna(inplace=True)

    # Define the target column
    target_column = "Best Time to visit"

    # Split features and target variable
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define preprocessing steps for numerical and categorical features
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_features = X.select_dtypes(include=["object"]).columns
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    # Define the model
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Create a pipeline with preprocessing and model
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])

    # Fit the model
    pipeline.fit(X_train, y_train)

    # Make predictions
    y_pred = pipeline.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Save the trained model
    model_file_path = os.path.join(current_dir, "model.pkl")
    joblib.dump(pipeline, model_file_path)
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train_model()
