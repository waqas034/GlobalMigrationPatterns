**Impact of Urbanization and Income Levels on Global Migration Patterns: A Statistical Analysis Using UN International Migrant Stock (1990–2024) and HDI Trends**

**Project Overview**
This project investigates how urbanization and income levels influence global migration patterns between 1990 and 2024.
By integrating data from the United Nations (UN DESA), World Bank, and UNDP Human Development Reports, this study aims to uncover relationships between migration trends, socioeconomic development, and urban growth.

**Datasets Used**
1. UN DESA International Migrant Stock (1990–2024)
   - Source: [UN Data Portal](https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx)  
   - Data on migrant stock by destination/origin and year.

2. World Bank Development Indicators
   - Source: [World Bank API](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv)
             [World Bank API](https://api.worldbank.org/v2/en/indicator/SP.URB.TOTL.IN.ZS?downloadformat=csv)
   - Includes GDP per capita and urban population (%).

3. UNDP Human Development Index (HDI) Trends (1990–2023)
   - Source: [UNDP HDR 2025 Statistical Annex – HDI Trends](https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Statistical_Annex_HDI_Trends_Table.xlsx)  

**Data Preparation and Integration**
- All datasets were converted from wide to long format (Country, Year, Value) using pandas melt.
- Country names were standardized to ensure consistency across sources.
- Non-numeric values and missing records were removed.
- Time periods were aligned to create a consistent Country–Year panel.
- Migration data were aggregated at the destination-country level to obtain total migrant stock per country per year.
- The final merged dataset contains over 68,000 country–year observations covering Migration, GDP per capita, HDI, and Urbanization.

**Exploratory Data Analysis (EDA)**
EDA was conducted using pandas, matplotlib, and seaborn to understand trends and relationships:
- Global migration trends from 1990–2024.
- Correlation heatmaps between migration and socioeconomic indicators.
- Scatter plots showing migration versus GDP per capita, HDI, and urbanization.
- Distribution plots and temporal trends for GDP, HDI, urbanization, and migration.

**Statistical and Machine Learning Analysis**
*Regression Analysis*
- Ordinary Least Squares (OLS) regression was used as a baseline.
- Diagnostic results indicated very low explanatory power, multicollinearity, and non-linear relationships.
- OLS was therefore deemed unsuitable for this dataset.

*Machine Learning Models*
To capture non-linear relationships and interactions:
- **Random Forest Regressor**
- **Extra Trees Regressor**
- **Gradient Boosting Regressor**

Feature importance from all three models consistently identified HDI as the strongest predictor of migrant stock, followed by urbanization and GDP per capita.

*Clustering Analysis*
To identify groups of countries with similar migration–development characteristics:
- **K-Means clustering** (k = 3) was applied to standardized country-level indicators.
- Cluster quality was evaluated using the silhouette score.
- **Hierarchical clustering** (Ward method) was used to validate and interpret cluster structure via a dendrogram.

Both methods produced consistent clusters representing:
- Low development / low migration countries
- High development / high migration countries
- Intermediate development countries

**Scripts Included**

*EDA_GDA.py*. *EDA_HDI.py*, *EDA_Migration.py*, *EDA_Urbanization.py* 
Separate exploratory scripts for Migration, GDP, HDI, and Urbanization, respectively.

*Merged.py*
Loads, cleans, reshapes, and merges all datasets into a unified Country–Year panel.

*Analysis_Merged.py*
Performs descriptive analysis, correlation analysis, and global trend visualization.

*Modeling.py*
Implements OLS regression, tree-based machine learning models, K-Means clustering, and hierarchical clustering, and generates all modeling visualizations.

*Comparison.py*
Side-by-side comparison of Feature importance across Random Forest, Extra Trees and Gradient Boosting, with Average cluster characteristics from K-Means and Hierarchical clustering. This confirms consistency and robustness of results across models.

**Outputs**
- Cleaned merged dataset (processed/merged_global_migration_data.csv)
- Country-level modeling results (processed/model_results_country_level.csv)
- All figures saved in the plots/ directory

**Summary**
- Global and regional migration trends analyzed (1990–2024)
- Relationships between migration and development indicators evaluated
- Countries clustered by migration–development patterns
