import numpy as np
import pandas as pd


df = pd.read_csv('processed/cleaned_dataset.csv')

# List of columns to calculate monthly sums for
columns_to_process = [
    'Laufwerke', 'Speicherwerke', 'Total Hydraulisch', 'Kernkraftwerke', 
    'Thermisch', 'Windkraft', 'Photovoltaik', 'Total Erneuerbar'
]

# Group by month, sum the specified columns and round
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
df_monthly_sums = df[df['Datum'].dt.year == 2025].groupby(df['Datum'].dt.strftime('%m'))[columns_to_process].sum().round(1)

# Reset the index to make 'Monat' a column
df_monthly_sums = df_monthly_sums.reset_index()

# Rename the date column to 'Monat'
df_monthly_sums.rename(columns={'Datum': 'Monat'}, inplace=True)

# Add a row with total sums for each column at the end
total_row = pd.DataFrame(df_monthly_sums[columns_to_process].sum()).T
total_row['Monat'] = 'Total'
df_monthly_sums = pd.concat([df_monthly_sums, total_row], ignore_index=True)

df_monthly_sums.to_csv('processed/monthly_sums.csv', index=False)