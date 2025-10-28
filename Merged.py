import pandas as pd
import os

# === Paths ===
DATA_DIR = "data"
OUTPUT_DIR = "processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load Migration Data ===
print("Loading Migration Data...")
migration_path = os.path.join(DATA_DIR, "undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx")
xls = pd.ExcelFile(migration_path)
migration_df = pd.read_excel(xls, sheet_name="Table 1", header=10)

migration_df = migration_df[['Region, development group, country or area of destination',
                             'Region, development group, country or area of origin',
                             1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]]

migration_df.columns = ['Destination', 'Origin', '1990', '1995', '2000', '2005', '2010', '2015', '2020', '2024']
migration_df = migration_df.rename(columns={'Destination': 'Country'})
migration_df = migration_df.drop(columns=['Origin'])

# Convert to long format (Country, Year, Migration)
migration_long = migration_df.melt(id_vars=['Country'], var_name='Year', value_name='Migration')
migration_long['Year'] = pd.to_numeric(migration_long['Year'])
print(f"Migration data shape: {migration_long.shape}")

# === Load GDP Data ===
print("Loading GDP Data...")
gdp_path = os.path.join(DATA_DIR, "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_24794.csv")
gdp_df = pd.read_csv(gdp_path, skiprows=4)
gdp_df = gdp_df.drop(columns=["Indicator Name", "Indicator Code"], errors="ignore")
gdp_df = gdp_df.melt(id_vars=["Country Name", "Country Code"], var_name="Year", value_name="GDP_per_capita")
gdp_df["Year"] = pd.to_numeric(gdp_df["Year"], errors="coerce")
gdp_df = gdp_df.dropna(subset=["GDP_per_capita", "Year"])
gdp_df = gdp_df.rename(columns={"Country Name": "Country"})
print(f"GDP data shape: {gdp_df.shape}")

# === Load HDI Data ===
print("Loading HDI Data...")
hdi_path = os.path.join(DATA_DIR, "HDR25_Statistical_Annex_HDI_Trends_Table.xlsx")
xls = pd.ExcelFile(hdi_path)
sheet_name = [s for s in xls.sheet_names if "HDI" in s or "Table 2" in s][0]
hdi_df = pd.read_excel(hdi_path, sheet_name=sheet_name, header=None)

header_row = None
for i in range(10):
    if "Country" in hdi_df.iloc[i].astype(str).values:
        header_row = i
        break

hdi_df = pd.read_excel(hdi_path, sheet_name=sheet_name, header=header_row)
hdi_df.columns = hdi_df.columns.map(str)
country_col = [c for c in hdi_df.columns if "Country" in c][0]

years = [str(y) for y in range(1990, 2024) if str(y) in hdi_df.columns]
hdi_df = hdi_df[[country_col] + years]
hdi_df = hdi_df.rename(columns={country_col: "Country"})
hdi_df = hdi_df.melt(id_vars=["Country"], var_name="Year", value_name="HDI")
hdi_df["Year"] = pd.to_numeric(hdi_df["Year"], errors="coerce")
hdi_df = hdi_df.dropna(subset=["HDI"])
print(f"HDI data shape: {hdi_df.shape}")

# === Standardize Country Names ===
def clean_country_name(name):
    if isinstance(name, str):
        return name.strip().replace("*", "").replace("...", "")
    return name

for df in [migration_long, gdp_df, hdi_df]:
    df["Country"] = df["Country"].apply(clean_country_name)

# === Merge all datasets ===
print("Merging datasets...")
merged_df = migration_long.merge(gdp_df, on=["Country", "Year"], how="inner")
merged_df = merged_df.merge(hdi_df, on=["Country", "Year"], how="inner")
print(f"Merged data shape: {merged_df.shape}")

# === Handle missing values ===
missing_before = merged_df.isna().sum().sum()
merged_df = merged_df.dropna(subset=["Migration", "GDP_per_capita", "HDI"])
missing_after = merged_df.isna().sum().sum()
print(f"Missing values removed: {missing_before - missing_after}")

# === Save merged dataset ===
output_file = os.path.join(OUTPUT_DIR, "merged_global_migration_data.csv")
merged_df.to_csv(output_file, index=False)
print(f"Merged dataset saved at: {output_file}")

print("\nSample of merged data:")
print(merged_df.head())
