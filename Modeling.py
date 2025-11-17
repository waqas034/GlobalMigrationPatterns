import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
import statsmodels.api as sm
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score

# === Paths ===
DATA_PATH = "processed/merged_global_migration_data.csv"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# === Load Cleaned Data ===
df = pd.read_csv(DATA_PATH)
print(f"Loaded merged dataset: {df.shape[0]} rows")

# Convert to numeric and drop missing
for col in ["Migration", "GDP_per_capita", "HDI", "Urbanization"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Migration", "GDP_per_capita", "HDI", "Urbanization"])

# === Aggregate Data (Average per Country) ===
df_country = df.groupby("Country", as_index=False).agg({
    "Migration": "mean",
    "GDP_per_capita": "mean",
    "HDI": "mean",
    "Urbanization": "mean"
})
print(f"Aggregated dataset: {df_country.shape[0]} countries")


# ======================================================
# 1. OLS REGRESSION (CLASSICAL STATISTICAL ANALYSIS)
# ======================================================
print("\nRunning OLS Regression...")

X = df_country[["GDP_per_capita", "HDI", "Urbanization"]]
y = df_country["Migration"]

X = sm.add_constant(X)
ols_model = sm.OLS(y, X).fit()
print(ols_model.summary())

# === Regression Plots ===
sns.regplot(x="GDP_per_capita", y="Migration", data=df_country, scatter_kws={'alpha':0.6})
plt.title("Regression: Migration vs GDP per Capita")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "regression_migration_gdp.png"))
plt.close()

sns.regplot(x="HDI", y="Migration", data=df_country, scatter_kws={'alpha':0.6})
plt.title("Regression: Migration vs HDI")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "regression_migration_hdi.png"))
plt.close()

sns.regplot(x="Urbanization", y="Migration", data=df_country, scatter_kws={'alpha':0.6})
plt.title("Regression: Migration vs Urbanization")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "regression_migration_urbanization.png"))
plt.close()


# ======================================================
# 2. RANDOM FOREST FEATURE IMPORTANCE
# ======================================================
print("\nRunning Random Forest...")

rf_model = RandomForestRegressor(n_estimators=300, random_state=42)
rf_model.fit(X[["GDP_per_capita", "HDI", "Urbanization"]], y)

rf_imp = pd.DataFrame({
    "Feature": ["GDP_per_capita", "HDI", "Urbanization"],
    "Importance": rf_model.feature_importances_
})
print("\nRandom Forest – Feature Importance:")
print(rf_imp.sort_values(by="Importance", ascending=False))

plt.figure(figsize=(6,4))
sns.barplot(data=rf_imp, x="Feature", y="Importance")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "rf_feature_importance.png"))
plt.close()


# ======================================================
# 2B. EXTRA TREES FEATURE IMPORTANCE
# ======================================================
print("\nRunning Extra Trees...")

et_model = ExtraTreesRegressor(n_estimators=300, random_state=42)
et_model.fit(X[["GDP_per_capita", "HDI", "Urbanization"]], y)

et_imp = pd.DataFrame({
    "Feature": ["GDP_per_capita", "HDI", "Urbanization"],
    "Importance": et_model.feature_importances_
})
print("\nExtra Trees – Feature Importance:")
print(et_imp.sort_values(by="Importance", ascending=False))

plt.figure(figsize=(6,4))
sns.barplot(data=et_imp, x="Feature", y="Importance")
plt.title("Extra Trees Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "extratrees_feature_importance.png"))
plt.close()


# ======================================================
# 2C. GRADIENT BOOSTING FEATURE IMPORTANCE
# ======================================================
print("\nRunning Gradient Boosting...")

gb_model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)
gb_model.fit(X[["GDP_per_capita", "HDI", "Urbanization"]], y)

gb_imp = pd.DataFrame({
    "Feature": ["GDP_per_capita", "HDI", "Urbanization"],
    "Importance": gb_model.feature_importances_
})
print("\nGradient Boosting – Feature Importance:")
print(gb_imp.sort_values(by="Importance", ascending=False))

plt.figure(figsize=(6,4))
sns.barplot(data=gb_imp, x="Feature", y="Importance")
plt.title("Gradient Boosting Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "gradientboosting_feature_importance.png"))
plt.close()


# ======================================================
# 3. K-MEANS CLUSTERING
# ======================================================
print("\nRunning K-Means Clustering...")

features = df_country[["Migration", "GDP_per_capita", "HDI", "Urbanization"]]
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df_country["KMeans_Cluster"] = kmeans.fit_predict(scaled)

silhouette = silhouette_score(scaled, df_country["KMeans_Cluster"])
print("\nK-Means Silhouette Score:", silhouette)

print("\nCluster Means:")
print(df_country.groupby("KMeans_Cluster")[["Migration", "GDP_per_capita", "HDI", "Urbanization"]].mean())

# Visualization
plt.figure(figsize=(7,5))
sns.scatterplot(x="GDP_per_capita", y="Migration", hue="KMeans_Cluster",
                data=df_country, s=60, palette="viridis")
plt.title("K-Means Clusters: GDP vs Migration")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "kmeans_clusters_gdp_migration.png"))
plt.close()

plt.figure(figsize=(7,5))
sns.scatterplot(x="Urbanization", y="Migration", hue="KMeans_Cluster",
                data=df_country, s=60, palette="viridis")
plt.title("K-Means Clusters: Urbanization vs Migration")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "kmeans_clusters_urbanization_migration.png"))
plt.close()


# ======================================================
# 4. HIERARCHICAL CLUSTERING
# ======================================================
print("\nRunning Hierarchical Clustering...")

linked = linkage(scaled, method='ward')

plt.figure(figsize=(26, 10))
dendrogram(linked,
           labels=df_country["Country"].values,
           leaf_rotation=90,
           leaf_font_size=13)
plt.title("Hierarchical Clustering Dendrogram (Ward)", fontsize=16)
plt.xlabel("Countries", fontsize=14)
plt.ylabel("Distance", fontsize=14)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "hierarchical_dendrogram.png"))
plt.close()

hc = AgglomerativeClustering(n_clusters=3, linkage='ward')
df_country["HierCluster"] = hc.fit_predict(scaled)

print("\nHierarchical Cluster Means:")
print(df_country.groupby("HierCluster")[["Migration", "GDP_per_capita", "HDI", "Urbanization"]].mean())



# ======================================================
# SAVE RESULTS
# ======================================================
df_country.to_csv("processed/model_results_country_level.csv", index=False)

print("\nAll Modeling Complete!")
print("Plots saved in 'plots/' folder.")
print("Model results saved in processed/model_results_country_level.csv")
