import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = r"data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_24794.csv"
PLOTS_DIR = r"plots"

try:
    # Main World Bank GDP data file
    df = pd.read_csv(DATA_PATH, skiprows=4)
except Exception as e:
    print("Error reading GDP data:", e)
    exit()

# Keep only useful columns
df = df.drop(columns=["Indicator Name", "Indicator Code"], errors="ignore")

# Melt the data to year-wise format
df = df.melt(id_vars=["Country Name", "Country Code"], var_name="Year", value_name="GDP_per_capita")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.dropna(subset=["GDP_per_capita"])
df["GDP_per_capita"] = df["GDP_per_capita"].astype(float)

print(f"Cleaned GDP data shape: {df.shape}")

# === Descriptive stats ===
print("\n=== GDP per Capita Summary ===")
print(df.groupby("Year")["GDP_per_capita"].describe().head())

# === Visualization directory ===
os.makedirs(PLOTS_DIR, exist_ok=True)

# Global GDP trend over years
plt.figure(figsize=(10,5))
global_mean = df.groupby("Year")["GDP_per_capita"].mean()
sns.lineplot(x=global_mean.index, y=global_mean.values)
plt.title("Average Global GDP per Capita Over Time")
plt.xlabel("Year")
plt.ylabel("GDP per Capita (USD)")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "global_gdp_trend.png"))
plt.close()

# Top 10 richest countries (latest year)
latest_year = df["Year"].max()
top10 = (
    df[df["Year"] == latest_year]
    .nlargest(10, "GDP_per_capita")
    .set_index("Country Name")["GDP_per_capita"]
)
plt.figure(figsize=(8,5))
sns.barplot(x=top10.values, y=top10.index, palette="crest")
plt.title(f"Top 10 Countries by GDP per Capita ({int(latest_year)})")
plt.xlabel("GDP per Capita (USD)")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "top10_gdp_countries.png"))
plt.close()

# GDP Distribution (latest year)
plt.figure(figsize=(8,5))
sns.histplot(df[df["Year"] == latest_year]["GDP_per_capita"], bins=40, kde=True)
plt.title(f"GDP per Capita Distribution ({int(latest_year)})")
plt.xlabel("GDP per Capita (USD)")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "gdp_distribution.png"))
plt.close()
