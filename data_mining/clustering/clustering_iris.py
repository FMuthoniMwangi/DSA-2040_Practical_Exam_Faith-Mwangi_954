# data_mining/clustering/clustering_iris.py
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

# ------------------------
# Setup logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------
# Config
# ------------------------
DATASET_PATH = os.path.join("data_mining/task1_output/iris_scaled.csv")  # Task1 preprocessed data
OUTPUT_DIR = "data_mining/clustering/task2_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
FEATURES = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# ------------------------
# Load preprocessed data
# ------------------------
df = pd.read_csv(DATASET_PATH)
X = df[FEATURES].values
y_true = df['species'].values
logging.info(f"Loaded preprocessed data from {DATASET_PATH} with shape {X.shape}")

# ------------------------
# K-Means Clustering
# ------------------------
k_values = [2, 3, 4]
results = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_
    
    # Metrics
    ari = adjusted_rand_score(y_true, labels)
    sil = silhouette_score(X, labels)
    inertia = kmeans.inertia_
    
    results.append({
        'k': k,
        'ARI': ari,
        'Silhouette': sil,
        'Inertia': inertia
    })
    
    # Scatter plot (petal length vs width) with clusters
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=X[:,2], y=X[:,3], hue=labels, palette='Set1', s=60)
    # annotate centroids
    for i, c in enumerate(centroids):
        plt.scatter(c[2], c[3], marker='X', s=200, c='black')
        plt.text(c[2]+0.05, c[3]+0.05, f"C{i}", fontsize=10)
    plt.xlabel("Petal Length (cm)")
    plt.ylabel("Petal Width (cm)")
    plt.title(f"K-Means Clustering (k={k})")
    plt.legend(title="Cluster")
    plt.tight_layout()
    scatter_path = os.path.join(OUTPUT_DIR, f"kmeans_k{k}_scatter.png")
    plt.savefig(scatter_path)
    plt.close()
    logging.info(f"Saved scatter plot for k={k} at {scatter_path}")

# ------------------------
# Elbow curve
# ------------------------
inertia_vals = [r['Inertia'] for r in results]
plt.figure(figsize=(6, 4))
plt.plot(k_values, inertia_vals, 'o-', color='blue')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Curve for K-Means")
plt.grid(True)
elbow_path = os.path.join(OUTPUT_DIR, "kmeans_elbow.png")
plt.savefig(elbow_path)
plt.close()
logging.info(f"Saved elbow curve at {elbow_path}")

# ------------------------
# Save results table
# ------------------------
results_df = pd.DataFrame(results)
results_csv_path = os.path.join(OUTPUT_DIR, "kmeans_results.csv")
results_df.to_csv(results_csv_path, index=False)
logging.info(f"Saved K-Means metrics table at {results_csv_path}")

print("[INFO] Clustering complete. Outputs saved in 'task2_output/'")
