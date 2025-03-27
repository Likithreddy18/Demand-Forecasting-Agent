import streamlit as st
import requests
import pandas as pd

# Set the base URL for your FastAPI service.
# If you're running locally, it might be "http://localhost:8000"
# In production on Railway, use the public URL provided by Railway.
BASE_URL = st.secrets.get("BASE_URL", "https://demand-forecasting-agent-production.up.railway.app")

st.title("Forecast Dashboard")

# Input: Product ID and forecast horizon (days ahead)
product_id = st.number_input("Enter Product ID", min_value=1000, step=1, value=1001)
days_ahead = st.slider("Forecast Days Ahead", min_value=1, max_value=30, value=7)

# Button to fetch forecasts
if st.button("Get Forecast"):
    # Construct the API URL
    api_url = f"{BASE_URL}/forecast/{product_id}?days_ahead={days_ahead}"
    
    try:
        # Send request to FastAPI endpoint
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if the request failed
        
        # Parse the JSON response into a DataFrame
        forecast_data = response.json()
        if not forecast_data:
            st.warning("No forecast data found for the given product.")
        else:
            df = pd.DataFrame(forecast_data)
            
            # Convert forecast_date to datetime for proper plotting
            df["forecast_date"] = pd.to_datetime(df["forecast_date"])
            
            st.subheader("Forecast Data")
            st.dataframe(df)
            
            # Plot the forecast using Streamlit's built-in line_chart
            st.subheader("Forecast Chart")
            st.line_chart(df.set_index("forecast_date")["predicted_demand"])
            
    except Exception as e:
        st.error(f"Error fetching forecast: {e}")
