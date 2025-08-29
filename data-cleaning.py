import pandas as pd
import numpy as np

# Read both CSV files
startups_df = pd.read_csv("yc_summer2025_startups.csv")
details_df = pd.read_csv("yc_summer2025_startups_details.csv")


# Merge the dataframes by company name
combined_df = pd.merge(
    startups_df, 
    details_df, 
    on='Company', 
    how='outer',  # Keep all companies from both files
    indicator=True  # Shows which file each row came from
)

# # Set pandas to display all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

# Remove the merge indicator column
combined_df = combined_df.drop('_merge', axis=1)
combined_df = combined_df.drop('YC Link', axis=1)

# Save the combined data
output_filename = "yc_combined_startups_data.csv"
combined_df.to_csv(output_filename, index=False)
print(f"\nCombined data saved to: {output_filename}")

print("\nData cleaning complete!")
