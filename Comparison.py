import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Feature importance data ---
feature_importance = pd.DataFrame({
    "Feature": ["GDP_per_capita", "HDI", "Urbanization"],
    "Random Forest": [0.341902, 0.421346, 0.236752],
    "Extra Trees": [0.469544, 0.268559, 0.261897],
    "Gradient Boosting": [0.275687, 0.394275, 0.330038]
})

# --- Cluster means data ---
cluster_means = pd.DataFrame({
    "Cluster": ["KMeans 0", "KMeans 1", "KMeans 2",
                "Hier 0", "Hier 1", "Hier 2"],
    "Migration": [129920, 582617, 102628, 341686, 259538, 120525],
    "GDP_per_capita": [1353, 41823, 7642, 1025, 46111, 7416],
    "HDI": [0.511, 0.878, 0.740, 0.472, 0.894, 0.723],
    "Urbanization": [32.7, 80.3, 64.4, 31.0, 81.3, 60.6]
})

# --- Plotting ---
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# --- Left: Feature Importance ---
x = np.arange(len(feature_importance))
width = 0.25

axes[0].bar(x - width, feature_importance["Random Forest"], width, label="Random Forest")
axes[0].bar(x, feature_importance["Extra Trees"], width, label="Extra Trees")
axes[0].bar(x + width, feature_importance["Gradient Boosting"], width, label="Gradient Boosting")

axes[0].set_xticks(x)
axes[0].set_xticklabels(feature_importance["Feature"])
axes[0].set_ylabel("Feature Importance")
axes[0].set_title("Regression Feature Importance")
axes[0].legend()
axes[0].grid(axis="y", linestyle="--", alpha=0.7)

# --- Right: Cluster Means ---
cluster_means_plot = cluster_means.set_index("Cluster")
cluster_means_plot[["Migration", "GDP_per_capita", "HDI", "Urbanization"]].plot(
    kind="bar", ax=axes[1], width=0.7)
axes[1].set_title("Cluster Summary (KMeans & Hierarchical)")
axes[1].set_ylabel("Value")
axes[1].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("plots/comparison_feature_cluster.png", dpi=300)
plt.close()
