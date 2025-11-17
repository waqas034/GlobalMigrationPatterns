**Impact of Urbanization and Income Levels on Global Migration Patterns: A Statistical Analysis Using UN International Migrant Stock (1990–2024) and HDI Trends**

Project Overview
This project investigates how urbanization and income levels influence global migration patterns between 1990 and 2024.
By integrating data from the United Nations (UN DESA), World Bank, and UNDP Human Development Reports, this study aims to uncover relationships between migration trends, socioeconomic development, and urban growth.



Datasets Used
1. UN DESA International Migrant Stock (1990–2024)
   - Source: [UN Data Portal](https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx)  
   - Data on migrant stock by destination/origin and year.

2. World Bank Development Indicators
   - Source: [World Bank API](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv)  
   - Includes GDP per capita and urban population (%).

3. UNDP Human Development Index (HDI) Trends (1990–2023)
   - Source: [UNDP HDR 2025 Statistical Annex – HDI Trends](https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Statistical_Annex_HDI_Trends_Table.xlsx)  


Exploratory Data Analysis (EDA)
   - Descriptive statistics and visualizations using `pandas`, `matplotlib`, and `seaborn`.  
   - Global and regional migration trend plots (1990–2024).  
   - Correlation heatmaps for migration vs. development indicators.  
   - Scatter plots for HDI, GDP, and urbanization relationships with migration.

Statistical & Machine Learning Models (Next)
   - Regression Analysis:** Multiple and panel regression to assess impacts on migration stock.  
   - Clustering:** K-Means and Hierarchical Clustering to group countries with similar migration-development profiles.



---

**New Scripts Added**
- Merged.py:  
  - Loaded and cleaned three datasets — UN DESA Migration, World Bank GDP, and UNDP HDI Trends.  
  - Standardized column names and country names.  
  - Converted all datasets into a uniform long format (`Country`, `Year`, `Value`).  
  - Merged them into a single file: `processed/merged_global_migration_data.csv`.  
  - Removed missing or invalid entries.

- Analysis_Merged.py:  
  - Conducted descriptive and correlation analysis on the merged dataset.  
  - Computed and visualized global averages (1990–2024).  
  - Generated key plots:
    - Correlation heatmap (`Migration`, `GDP per capita`, `HDI`)
    - Migration vs GDP per capita
    - Migration vs HDI
    - Global average trends (1990–2024)
  - Saved visual outputs under the `plots/` folder.

**Results Summary**
- Final merged dataset: **68953 records → cleaned to 66123 records → aggregated 772 records**
- Correlation results indicate:
  - GDP per capita and HDI are moderately correlated.
  - Migration has weak but observable relationships with development factors.
- Visual trends confirm steady global growth in both HDI and GDP alongside rising migrant stock.

**Objective 1 Achieved**
> Analyzed and visualized global and regional trends in international migrant stock (1990–2024), setting the foundation for regression and clustering steps (Objectives 2 & 3).

---


**Objective 2 & 3: Statistical Modeling and Country Clustering**

Modeling.py:
- Imported and analyzed the cleaned merged dataset (merged_global_migration_data.csv).
- Aggregated migration, GDP per capita, and HDI by country to remove duplication.
- Conducted Multiple Linear Regression (OLS) using statsmodels to assess how GDP per capita and HDI influence migration levels.
- Applied K-Means Clustering (k=3) to group countries based on development and migration characteristics.

Generated regression and clustering plots:
- Regression: Migration vs GDP per capita
- Regression: Migration vs HDI
- Country Clusters (Migration vs GDP)
- Country Clusters (Migration vs HDI)

- Saved all results and figures in the plots/ directory.

**Results Summary (Objectives 2 & 3)**

- Regression results showed a very weak statistical relationship between migration and the two predictors (GDP per capita and HDI).
- R² = 0.002, p-value > 0.05 → indicates that neither variable alone strongly explains migration levels.
- This suggests that other factors (e.g., urbanization, policies, geography, or conflict) play significant roles.

K-Means clustering identified three broad groups of countries:
- Cluster 0 – Low migration, lower GDP & HDI (developing nations).
- Cluster 1 – Moderate migration with mid-level GDP and HDI (emerging economies).
- Cluster 2 – High migration with strong economic and human development indicators (developed regions).

- The clustering visualizations help categorize global migration patterns across different development levels.

**Objective 2 Achieved**

Evaluated statistical relationships between migration and key socioeconomic indicators (GDP per capita, HDI) using regression analysis.

**Objective 3 Achieved**

Classified countries into development–migration clusters using K-Means, highlighting global disparities and migration trends.

---

**Updates Completed Today**
1. Urbanization Dataset Integrated
- Loaded the World Bank Urban Population (% of total population) dataset.
- Cleaned dataset.
- Converted year columns to numeric and reshaped data into long format.
- Merged Urbanization with Migration, GDP per capita, and HDI into the unified dataset.
- Added Urbanization to the aggregated country-level dataset for analysis.

2. Enhanced Exploratory Data Analysis (EDA)
- Added Urbanization to the correlation heatmap (Migration, GDP, HDI, Urbanization).
- Created a new scatter plot: Migration vs Urbanization.
- Updated global trend plots to include Urbanization (1990–2024).
- Regenerated and saved all updated plots in the plots/ directory.

3. New Models Implemented
- **Extra Trees Regressor**
- **Gradient Boosting Regressor**
- **Hierarchical Clustering**

4. Added and Updated all necessary files
- Updated Merged.py
- Udpated Analysis_Merged.py
- Updated Modeling.py
- Added EDA_Urbanization.py
- Added Comparison.py

5. All necessary coding completed

**Next Steps**
Project completed but yet in a temptative stage, which will be reviewed and updated after taking feedback.

---



4. Feature importance charts for all models

