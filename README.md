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
