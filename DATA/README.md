# Data Summary 

Our dataset will consist of multiple publicly available economic and housing-market time series downloaded as CSV files from FRED. The primary dataset is the All-Transactions House Price Index for Charlottesville, VA (MSA), provided by the Federal Housing Finance Agency (FHFA). This quarterly index measures changes in housing prices using sales prices and appraisal data. We will combine this dataset with unemployment rates, active listing count, and mortgage rate data. The datasets contain historical observations at weekly, monthly, and quarterly frequencies. We will standardize these observations to a quarterly time scale and merge them by date to create a consolidated dataset suitable for time-series analysis. Each observation in the resulting dataset will represent one quarter, with columns containing housing price measurements and the corresponding economic indicators. The final dataset size and observation period will be determined after preprocessing and aligning the downloaded CSV files. The count of the data is 2898. The dataset and collection materials are stored in the group’s shared Google Drive folder and can be accessed through the link provided with the project materials.


# Provenance 
All data come from Federal Reserve Economic Data (FRED), a free public database maintained by the Federal Reserve Bank of St. Louis that collects series from their sources. The Charlottesville house price index (ATNHPIUS16820Q) is produced by the Federal Housing Finance Agency (FHFA) from repeat sales and appraisals of homes with mortgages backed by Fannie Mae and Freddie Mac. The unemployment rate (CHAR851URN) comes from the Bureau of Labor Statistics’ Local Area Unemployment Statistics program. The 30-year mortgage rate (MORTGAGE30US) comes from Freddie Mac’s weekly survey of lenders. The active listing count (ACTLISCOU16820) comes from Realtor.com listings in the Charlottesville metro area.


# License
Data from FHFA and the Bureau of Labor Statistics are U.S. government works in the public domain and can be used and shared freely. The mortgage rate data (Freddie Mac) and listing data (Realtor.com) are copyrighted by their providers and redistributed by FRED with permission; FRED’s terms of use allow them for non-commercial research and education with proper citation [3]. Our project is non-commercial academic work that cites every series, and our code and processed data are shared in our GitHub repository.


## Ethical Statements 
Our data are publicly available, aggregated to the city, metro, or national level, and contain no information about individual people or properties, so they pose no privacy risk. However, because housing affordability is a sensitive local issue, we will present our findings as associations rather than causes and acknowledge that metro-level data can hide differences in how rising costs affect different neighborhoods and communities.

# Data Dictionary 

# Exploratory Data 
<img width="3500" height="2100" alt="Screenshot 2026-10-19 at 2 37 31 PM" src="https://github.com/user-attachments/assets/1425b62e-353e-4a25-891e-5fcb8d8ece1c" />

**Figure 1. Standardized Time-Series Trends in Charlottesville Housing Market and Economic Indicators.** The variables exhibit different patterns over time, with mortgage rates generally declining after peaking around 1980, the HPI trending upward, and unemployment fluctuating sharply around 2020. 


<img width="3500" height="2100" alt="Screenshot 2026-10-19 at 2 38 31 PM" src="https://github.com/user-attachments/assets/d07259df-90ae-410c-91e6-3fd241c0da63" />

**Figure 2. Distribution of the Charlottesville All-Transactions House Price Index.** This plot summarizes the distribution of index values. The span from 100 to values ranging around 400 in recent times suggests housing values in the Charlottesville metro area increased by 300% relative to the reference level
