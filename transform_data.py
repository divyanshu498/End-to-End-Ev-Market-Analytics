import pandas as pd
import numpy as np

print("Starting the data transformation & Normalization process")

# Load the row dataset extracted from the API
raw_file_path = "ev_data_raw.csv"
df = pd.read_csv(raw_file_path)

# Data Clining : Handle missing values and standardize formats
# Fill Missing critical text fields with 'unknown' and numeric fields with 0
df['county'] = df['county'].fillna('unknown')
df['city'] = df['city'].fillna('unknown')
df['zip_code'] = df['zip_code'].fillna('00000')
#Check for 'base_msrp'
if 'base_msrp' in df.columns:df['base_msrp'] = pd.to_numeric(df['base_msrp'], errors='coerce').fillna(0)
else:
    print("warning  'base' column not found in API. Creating default 0 values.") 
    df['base_msrp'] = 0
# Check for 'electric_range'
if 'electric_range' in df.columns: df['electric_range'] = pd.to_numeric(df['electric_range'], errors='coerce').fillna(0)
else:
    print("Warning:'electric_range' not found in API. Creating defauly 0 value.") 
    df['electric_range'] = 0

# Create 'dim_location' Table
# Extract unique location location attributes to avoid redundancy in database
print("Creating dim_location table...")
dim_location = df[['county', 'city', 'state', 'zip_code']].drop_duplicates().reset_index(drop=True)
# Generate a unique auto-incrementing Primary key for locations
dim_location['location_id'] = dim_location.index + 1

# Creat 'dim_vehicle_specs' Table (Dimension Table)
# Extract unique technical specifications of the electric vehicles
print("creating dim_vehicle_specs table...")
dim_vehicle_specs = df[['vin_1_10', 'make', 'model', 'ev_type']].drop_duplicates().reset_index(drop=True)
# Generate a unique auto-incrementing Primary key for vehicle specifications
dim_vehicle_specs['vehicle_id'] = dim_vehicle_specs.index + 1

# Create 'fact_ev_registrations' Table (Fact Table)
# The fact table will store core metrics and reference the dimension table via Foreign Keys
print("Creating fact_ev_registrations table...")

# Map location_id from dim_location back to the main dataframe
df = df.merge(dim_location, on=['county', 'city', 'state', 'zip_code'], how='left')

# Map vehical_id from dim_vehicle_specs back to main dataframe 
df = df.merge(dim_vehicle_specs, on=['vin_1_10', 'make', 'model', 'ev_type'], how='left')

# Extract columns required for the Fact Table 
fact_ev_registrations = df[['dol_vehicle_id', 'vehicle_id', 'location_id', 'model_year', 'electric_range', 'base_msrp']]
#Rename dol_vehicle_id to registration_id to serve as the Primary Key
fact_ev_registrations = fact_ev_registrations.rename(columns={'dot_vehicle_id':'registration_id'})

# Export the normalized DataFrames into separate clean CSV files
print("Exporting normalized tables to CSV...")
dim_location.to_csv("dim_location.csv", index=False)
dim_vehicle_specs.to_csv("dim_vehicle_specs.csv", index=False)
fact_ev_registrations.to_csv("fact_ev_registrations.csv", index=False)

print("\nTransformation complete! Generated 3 normalized files:")
print(f"- dim_location.csv (Rows:{len(dim_location)})")
print(f"- dim_vehicle_specs.csv(Row: {len(dim_vehicle_specs)})")
print(f"- fact_ev_registrations.csv(Row: {len(fact_ev_registrations)})")
print("\nReady for Mysql database import!")