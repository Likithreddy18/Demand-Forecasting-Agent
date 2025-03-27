from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
import traceback
import config

app = FastAPI()

# Set up your database connection using SQLAlchemy's URL.create for safety.
'''engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username="USERNAME",
        password="PASSWORD",  # your raw password; no need to encode here
        host="localhost",
        port=5432,
        database="DATABASE"
    )
)''' #this code is for when you setup

engine = create_engine(config.DATABASE_URL) #This is for railway

@app.get("/forecast/{product_id}")
def get_forecast(product_id: int, days_ahead: int = 7):
    try:
        # Force cast to int (prevents injection in LIMIT clause)
        product_id = int(product_id)
        days_ahead = int(days_ahead)

        # Build raw SQL with LIMIT directly inserted
        sql = f"""
            SELECT forecast_date, predicted_demand
            FROM product_forecasts
            WHERE product_id = {product_id}
            ORDER BY forecast_date
            LIMIT {days_ahead}
        """

        with engine.connect() as conn:
            df = pd.read_sql(sql, conn)

        return df.to_dict(orient="records")

    except Exception as e:
        print("❌ Internal Server Error:")
        traceback.print_exc()
        return {"error": str(e)}
