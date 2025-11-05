import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import os

# === Paths ===
DATA_PATH = "processed/merged_global_migration_data.csv"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# === Load Cleaned Data ===
df = pd.read_csv(DATA_PATH)
print(f"Loaded merged dataset: {df.shape[0]} rows")

# Convert to numeric and drop missing
for col in ["Migration", "GDP_per_capita", "HDI"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Migration", "GDP_per_capita", "HDI"])

# === Aggregate Data (Average per Country) ===
df_country = df.groupby("Country", as_index=False).agg({
    "Migration": "mean",
    "GDP_per_capita": "mean",
    "HDI": "mean"
})
print(f"Aggregated dataset: {df_country.shape[0]} countries")

# === REGRESSION ANALYSIS ===
print("\nRunning Regression Analysis...")
X = df_country[["GDP_per_capita", "HDI"]]
y = df_country["Migration"]

# Add constant for intercept
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())

# === Scatter plots for regression relationships ===
sns.regplot(x="GDP_per_capita", y="Migration", data=df_country, scatter_kws={'alpha':0.5})
plt.title("Regression: Migration vs GDP per Capita")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "regression_migration_gdp.png"))
plt.close()

sns.regplot(x="HDI", y="Migration", data=df_country, scatter_kws={'alpha':0.5})
plt.title("Regression: Migration vs HDI")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "regression_migration_hdi.png"))
plt.close()

# === CLUSTERING ANALYSIS ===
print("\nRunning K-Means Clustering...")

# Scale features for clustering
features = df_country[["Migration", "GDP_per_capita", "HDI"]]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Choose number of clusters (e.g., 3 for simplicity)
kmeans = KMeans(n_clusters=3, random_state=42)
df_country["Cluster"] = kmeans.fit_predict(scaled_features)

# === Visualize Clusters ===
plt.figure(figsize=(7,5))
sns.scatterplot(
    x="GDP_per_capita", y="Migration",
    hue="Cluster", data=df_country, palette="viridis", s=60
)
plt.title("Country Clusters: Migration vs GDP per Capita")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "clusters_migration_gdp.png"))
plt.close()

plt.figure(figsize=(7,5))
sns.scatterplot(
    x="HDI", y="Migration",
    hue="Cluster", data=df_country, palette="viridis", s=60
)
plt.title("Country Clusters: Migration vs HDI")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "clusters_migration_hdi.png"))
plt.close()

print("Modeling complete! Regression results and cluster plots saved in 'plots/' folder.")
