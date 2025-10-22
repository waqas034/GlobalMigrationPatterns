import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Paths ---
DATA_PATH = "data/HDR25_Statistical_Annex_HDI_Trends_Table.xlsx"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


# --- Finding correct sheet automatically ---
xls = pd.ExcelFile(DATA_PATH)
sheet_name = [s for s in xls.sheet_names if "HDI" in s or "Table 2" in s][0]
print(f"Using sheet: {sheet_name}")

# --- Read file (auto-detect header row) ---
df = pd.read_excel(DATA_PATH, sheet_name=sheet_name, header=None)

header_row = None
for i in range(10):
    if "Country" in df.iloc[i].astype(str).values or "HDI rank" in df.iloc[i].astype(str).values:
        header_row = i
        break

if header_row is None:
    raise ValueError("Could not detect header row automatically. Check Excel format.")

df = pd.read_excel(DATA_PATH, sheet_name=sheet_name, header=header_row)
df = df.rename(columns=lambda x: str(x).strip())

country_col = [c for c in df.columns if "Country" in c or "country" in c.lower()]
if not country_col:
    raise ValueError("Could not find 'Country' column.")
country_col = country_col[0]

# --- Keeping only relevant columns ---
years = [str(y) for y in range(1990, 2024) if str(y) in df.columns]
df = df[[country_col] + years]

# --- Drop group/category headers and convert to numeric ---
df[years] = df[years].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=[country_col])
df = df[df[years].notna().any(axis=1)]
df = df[~df[country_col].str.contains("development", case=False, na=False)]
df = df.set_index(country_col)

print(f"Cleaned data shape: {df.shape}")

# --- Summary ---
print("\n=== HDI Summary (first 5 rows) ===")
print(df.head())

# --- Plot 1: Global average HDI trend ---
plt.figure(figsize=(10, 5))
df[years].mean().plot(marker='o', color='teal')
plt.title("Average Global HDI Trend (1990–2023)")
plt.ylabel("Average HDI")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "hdi_global_trend.png"))
plt.close()

# --- Plot 2: Top 10 countries (2023) ---
top10 = df["2023"].sort_values(ascending=False).head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top10.values, y=top10.index, palette="crest")
plt.title("Top 10 Countries by HDI (2023)")
plt.xlabel("HDI Value")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "hdi_top10_2023.png"))
plt.close()

# --- Plot 3: Bottom 10 countries (2023) ---
bottom10 = df["2023"].sort_values().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=bottom10.values, y=bottom10.index, palette="rocket")
plt.title("Bottom 10 Countries by HDI (2023)")
plt.xlabel("HDI Value")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "hdi_bottom10_2023.png"))
plt.close()

# --- Plot 4: Correlation heatmap ---
plt.figure(figsize=(8, 6))
sns.heatmap(df[years].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between HDI Across Years")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "hdi_correlation_heatmap.png"))
plt.close()
