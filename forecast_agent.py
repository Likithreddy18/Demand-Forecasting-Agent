#forecast_agent.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from nixtla import NixtlaClient
import config  # Contains your TIMEGPT_API_KEY and optionally other config values

# Set up your database connection using SQLAlchemy's URL.create for safety.
'''engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username="USERNAME",
        password="PASSWORD",  # your raw password; no need to encode here
        host="localhost",
        port=5432,
        database="YOUR LOCAL DATABASE"
    )
)''' #this code is for when you setup

engine = create_engine(config.DATABASE_URL) #This is for railway

# Initialize the Nixtla (TimeGPT) client with your API key.
client = NixtlaClient(api_key=config.TIMEGPT_API_KEY)

# Load your synthetic dataset.
dataset_path = os.path.join(config.DATA_DIR, "realistic_food_demand_dataset.csv")
data = pd.read_csv(dataset_path)

# Get unique product IDs to loop through.
product_ids = data["product_id"].unique()

# Forecast horizon in days.
HORIZON = 7

for product_id in product_ids:
    # Prepare data for the current product (rename columns to 'ds' and 'y' for Nixtla)
    product_data = data[data["product_id"] == product_id][["date", "demand"]].copy()
    product_data.rename(columns={"date": "ds", "demand": "y"}, inplace=True)
    
    if len(product_data) < 30:
        print(f"⚠️ Skipping product {product_id} — not enough data points.")
        continue

    try:
        # Generate forecast for the next HORIZON days.
        forecast_df = client.forecast(df=product_data, h=HORIZON, freq="D")
        
        # Add the product_id column and rename output columns for consistency.
        forecast_df["product_id"] = int(product_id)
        forecast_df.rename(columns={"ds": "forecast_date", "TimeGPT": "predicted_demand"}, inplace=True)
        
        # Drop any duplicate rows just in case.
        forecast_df = forecast_df.drop_duplicates(subset=["forecast_date", "product_id"])
        
        # Insert the new forecast data into the database.
        forecast_df.to_sql("product_forecasts", engine, if_exists="append", index=False)

            
        print(f"✅ Forecast stored for product {product_id}")
    
    except Exception as e:
        print(f"❌ Forecast failed for product {product_id}: {e}")
