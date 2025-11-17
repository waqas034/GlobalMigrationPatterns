import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load dataset ---
DATA_PATH = r"data/API_SP.URB.TOTL.IN.ZS_DS2_en_csv_v2_129596.csv"
PLOTS_DIR = r"plots"

# Skip metadata rows
df = pd.read_csv(DATA_PATH, skiprows=4)

# Drop any unnamed columns (like Unnamed: 69)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(f"Dataset shape after dropping extra columns: {df.shape}")
print(df.head())

# Drop unneeded columns
df_clean = df.drop(columns=['Indicator Name', 'Indicator Code'])
df_clean = df_clean.rename(columns={'Country Name': 'Country', 'Country Code': 'Code'})

# Melt dataset to long format
df_long = df_clean.melt(id_vars=['Country', 'Code'], 
                        var_name='Year', 
                        value_name='Urban_Pop_Percent')

# Convert Year to int safely (ignore non-numeric if any remain)
df_long = df_long[pd.to_numeric(df_long['Year'], errors='coerce').notnull()]
df_long['Year'] = df_long['Year'].astype(int)

# Convert Urban_Pop_Percent to numeric
df_long['Urban_Pop_Percent'] = pd.to_numeric(df_long['Urban_Pop_Percent'], errors='coerce')

print(df_long.head())

# === Visualization directory ===
os.makedirs(PLOTS_DIR, exist_ok=True)

# --- Top and bottom urbanized countries (latest year 2024) ---
latest_year = df_long[df_long['Year'] == 2024].sort_values(by='Urban_Pop_Percent', ascending=False)
print("Top 10 urbanized countries in 2024:")
print(latest_year[['Country', 'Urban_Pop_Percent']].head(10))
print("Bottom 10 urbanized countries in 2024:")
print(latest_year[['Country', 'Urban_Pop_Percent']].tail(10))

# --- Plot global urbanization trends ---
plt.figure(figsize=(14,6))
sns.lineplot(data=df_long.groupby('Year')['Urban_Pop_Percent'].mean().reset_index(),
             x='Year', y='Urban_Pop_Percent')
plt.title("Global Average Urbanization Over Time")
plt.ylabel("Urban population (% of total)")
plt.grid(True)
plt.savefig(os.path.join(PLOTS_DIR, "global_avg_urban.png"))
plt.close()

# --- Sample country trends (top 10 urbanized countries 2024) ---
top_countries = latest_year['Country'].head(10)
plt.figure(figsize=(16,8))
sns.lineplot(data=df_long[df_long['Country'].isin(top_countries)], 
             x='Year', y='Urban_Pop_Percent', hue='Country', marker='o')
plt.title("Urbanization Trends for Top 10 Countries (2024)")
plt.ylabel("Urban population (% of total)")
plt.legend(loc='lower right')
plt.grid(True)
plt.savefig(os.path.join(PLOTS_DIR, "urban_trend_top10.png"))
plt.close()

# --- Histogram of urbanization in 2024 ---
plt.figure(figsize=(12,6))
sns.histplot(latest_year['Urban_Pop_Percent'], bins=30, kde=True)
plt.title("Distribution of Urbanization in 2024")
plt.xlabel("Urban population (% of total)")
plt.ylabel("Number of countries")
plt.savefig(os.path.join(PLOTS_DIR, "urbanization_in_2024.png"))
plt.close()

# --- Heatmap for selected countries over time (first 20 for example) ---
selected_countries = df_long['Country'].unique()[:20]
pivot_df = df_long[df_long['Country'].isin(selected_countries)].pivot(index='Country', columns='Year', values='Urban_Pop_Percent')
plt.figure(figsize=(18,10))
sns.heatmap(pivot_df, annot=False, cmap='YlGnBu')
plt.title("Urbanization % Over Time for Selected Countries")
plt.savefig(os.path.join(PLOTS_DIR, "urban_percent_selected_countries.png"))
plt.close()
