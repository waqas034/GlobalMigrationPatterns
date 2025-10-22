import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = "data/undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

xls = pd.ExcelFile(DATA_PATH)
df = pd.read_excel(xls, sheet_name="Table 1", header=10)

# Keeping only relevant columns
df = df[['Region, development group, country or area of destination',
         'Region, development group, country or area of origin',
         1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]]

df.columns = ['Destination', 'Origin', '1990', '1995', '2000', '2005', '2010', '2015', '2020', '2024']

# Basic overview
print(f"Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Global trend of total migration
df_years = df.loc[:, '1990':'2024'].sum()
plt.figure(figsize=(8,5))
sns.lineplot(x=df_years.index, y=df_years.values, marker="o")
plt.title("Global International Migrant Stock (1990–2024)")
plt.xlabel("Year")
plt.ylabel("Total Migrants")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/migration_global_trend.png")
plt.close()

# Top 10 destination countries (2024)
top_dest = df.groupby('Destination')['2024'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_dest.values, y=top_dest.index, palette="crest")
plt.title("Top 10 Destination Countries (2024)")
plt.xlabel("Migrant Stock")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/migration_top_destinations_2024.png")
plt.close()

# Top 10 origin countries (2024)
top_orig = df.groupby('Origin')['2024'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_orig.values, y=top_orig.index, palette="mako")
plt.title("Top 10 Origin Countries (2024)")
plt.xlabel("Migrant Stock")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/migration_top_origins_2024.png")
plt.close()
