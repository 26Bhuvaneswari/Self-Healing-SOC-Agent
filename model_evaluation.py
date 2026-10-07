import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Dataset used to train the existing model
DATA_PATH = r"MachineLearningCVE\balanced_training.csv"

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Separate features and target
X = df.drop(columns=["Target"])
y = df["Target"]

# Recreate the SAME test split used during model training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# Load existing trained Random Forest model
model = joblib.load("soc_ml_model.pkl")

print("\nRunning full test-set evaluation...")

# Predict the complete test set
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Confusion matrix
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

# Store results
metrics = {
    "dataset": "CICIDS2017 balanced dataset",
    "test_samples": int(len(X_test)),
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "true_negative": int(tn),
    "false_positive": int(fp),
    "false_negative": int(fn),
    "true_positive": int(tp)
}

# Save results
with open("evaluation_metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

print("\n===== FULL MODEL EVALUATION =====")
print("Accuracy :", metrics["accuracy"], "%")
print("Precision:", metrics["precision"], "%")
print("Recall   :", metrics["recall"], "%")
print("F1 Score :", metrics["f1_score"], "%")

print("\n===== CONFUSION MATRIX =====")
print("TN:", tn)
print("FP:", fp)
print("FN:", fn)
print("TP:", tp)

print("\nResults saved to: evaluation_metrics.json")