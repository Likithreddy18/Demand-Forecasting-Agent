#duplicate removal
import os
import pandas as pd
from sqlalchemy import create_engine, URL

# Configure your database connection
'''engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="Helloworld@123",  # your raw password (no need to URL-encode here)
        host="localhost",
        port=5432,
        database="Demand_Forecasting"
    )
)'''
engine = create_engine(config.DATABASE_URL) #This is for railway

# Step 1: Read the entire table into a DataFrame
df = pd.read_sql("SELECT * FROM product_forecasts", engine)
print("Number of rows before cleaning:", len(df))

# Step 2: Remove duplicates based on product_id and forecast_date.
# Adjust the subset list if you want to consider more columns as uniqueness criteria.
df_clean = df.drop_duplicates(subset=["product_id", "forecast_date"], keep="first")
print("Number of rows after cleaning:", len(df_clean))

# Optional: Check which duplicates were dropped (if needed)
# duplicates = df[df.duplicated(subset=["product_id", "forecast_date"], keep=False)]
# print(duplicates)

# Step 3: Write the cleaned DataFrame back to the database.
# Warning: Using if_exists="replace" will drop the existing table and create a new one.
df_clean.to_sql("product_forecasts", engine, if_exists="replace", index=False)

print("Duplicates removed and table updated successfully.")
