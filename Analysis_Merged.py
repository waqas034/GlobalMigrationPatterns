import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Paths ===
DATA_PATH = "processed/merged_global_migration_data.csv"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# === Load Data ===
df = pd.read_csv(DATA_PATH)
print(f"Loaded merged dataset: {df.shape[0]} rows")

# --- Force numeric conversion ---
for col in ["Migration", "GDP_per_capita", "HDI", "Urbanization"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Drop rows with missing or invalid values ---
df = df.dropna(subset=["Migration", "GDP_per_capita", "HDI", "Urbanization"])
print(f"After cleaning: {df.shape[0]} rows remain")

# === Aggregate Migration per Country-Year ===
df_agg = df.groupby(["Country", "Year"], as_index=False).agg({
    "Migration": "sum",
    "GDP_per_capita": "mean",
    "HDI": "mean",
    "Urbanization": "mean"
})
print(f"After aggregation: {df_agg.shape[0]} rows")

# === Correlation Matrix ===
corr = df_agg[["Migration", "GDP_per_capita", "HDI", "Urbanization"]].corr()
print("\n=== Correlation Matrix ===")
print(corr)

plt.figure(figsize=(7,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Migration, GDP, HDI, and Urbanization")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"))
plt.close()

# === Scatter Plots ===

for col in ["GDP_per_capita", "HDI", "Urbanization"]:
    plt.figure(figsize=(7,5))
    sns.scatterplot(x=col, y="Migration", data=df_agg, alpha=0.6)
    plt.title(f"Migration vs {col}")
    plt.xlabel(col)
    plt.ylabel("Migration Stock")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"migration_vs_{col.lower()}.png"))
    plt.close()

# === Yearly Trends ===
plt.figure(figsize=(8,5))
sns.lineplot(data=df_agg.groupby("Year")["Migration"].mean())
plt.title("Average Global Trends (1990–2024)")
plt.ylabel("Mean Value (scaled)")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "global_trends.png"))
plt.close()


print("Analysis complete! Cleaned and plots saved in 'plots/' folder.")
