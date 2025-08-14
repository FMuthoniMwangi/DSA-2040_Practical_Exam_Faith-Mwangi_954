# data_mining/classification/mining_iris_basket.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import random

# Apriori
try:
    from mlxtend.frequent_patterns import apriori, association_rules
except ImportError:
    apriori = None
    association_rules = None

# ------------------------
# Config
# ------------------------
OUTPUT_DIR = "task3_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
TASK1_OUTPUT = os.path.join("data_mining/task1_output") 
SCALED_CSV = os.path.join(TASK1_OUTPUT, "iris_scaled.csv")

# ------------------------
# Load preprocessed data
# ------------------------
df = pd.read_csv(SCALED_CSV)
X = df.drop(columns=["species"])
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ------------------------
# Part A: Classification
# ------------------------
# 1. Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

metrics_dt = {
    "accuracy": accuracy_score(y_test, y_pred_dt),
    "precision": precision_score(y_test, y_pred_dt, average='macro'),
    "recall": recall_score(y_test, y_pred_dt, average='macro'),
    "f1": f1_score(y_test, y_pred_dt, average='macro')
}

# Visualize tree
plt.figure(figsize=(12,8))
plot_tree(dt, feature_names=X.columns, class_names=y.unique(), filled=True)
plt.title("Decision Tree on Iris Dataset")
plt.savefig(os.path.join(OUTPUT_DIR, "decision_tree.png"))
plt.close()

# 2. KNN Classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

metrics_knn = {
    "accuracy": accuracy_score(y_test, y_pred_knn),
    "precision": precision_score(y_test, y_pred_knn, average='macro'),
    "recall": recall_score(y_test, y_pred_knn, average='macro'),
    "f1": f1_score(y_test, y_pred_knn, average='macro')
}

# Save metrics
pd.DataFrame([metrics_dt, metrics_knn], index=["Decision Tree", "KNN"]).to_csv(os.path.join(OUTPUT_DIR, "classification_metrics.csv"))

# ------------------------
# Part B: Association Rule Mining
# ------------------------
# Generate synthetic basket data
items_pool = ['milk', 'bread', 'beer', 'diapers', 'eggs', 'cheese', 'cola', 'chips', 'butter', 'yogurt',
              'ham', 'cereal', 'coffee', 'tea', 'cookies', 'juice', 'nuts', 'fruit', 'vegetables', 'soda']

num_transactions = 30
transactions = [random.choices(items_pool, k=random.randint(3,8)) for _ in range(num_transactions)]
df_trans = pd.DataFrame({"transaction": transactions})

# Convert to one-hot encoding for Apriori
all_items = sorted(set(item for trans in transactions for item in trans))
onehot = pd.DataFrame([{item: (item in t) for item in all_items} for t in transactions])

# Apply Apriori
if apriori is not None:
    freq_items = apriori(onehot, min_support=0.2, use_colnames=True)
    rules = association_rules(freq_items, metric="confidence", min_threshold=0.5)
    rules = rules.sort_values("lift", ascending=False).head(5)
    rules.to_csv(os.path.join(OUTPUT_DIR, "top5_association_rules.csv"), index=False)
else:
    rules = None

# Save synthetic transactions
df_trans.to_csv(os.path.join(OUTPUT_DIR, "synthetic_transactions.csv"), index=False)

print("[INFO] Task 3 complete. Outputs in:", OUTPUT_DIR)
