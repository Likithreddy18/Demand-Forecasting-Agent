import streamlit as st
import requests
import pandas as pd
import altair as alt


# Set the base URL for your FastAPI service.
# If you're running locally, it might be "http://localhost:8000"
# In production on Railway, use the public URL provided by Railway.
BASE_URL = st.secrets.get("BASE_URL", "https://demand-forecasting-agent-production.up.railway.app")

# Title and description
st.title("Forecast Dashboard")
st.markdown("This dashboard shows the forecasted demand for various products. Use the sidebar to adjust parameters.")

# Sidebar for inputs
st.sidebar.header("Input Parameters")
product_id = st.sidebar.number_input("Enter Product ID", min_value=1000, step=1, value=1001)
days_ahead = st.sidebar.slider("Forecast Days Ahead", min_value=1, max_value=30, value=7)

# Fetch Forecast Data
def fetch_forecast(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

if st.sidebar.button("Get Forecast"):
    api_url = f"{BASE_URL}/forecast/{product_id}?days_ahead={days_ahead}"
    with st.spinner("Fetching forecast data..."):
        try:
            forecast_data = fetch_forecast(api_url)
            if not forecast_data:
                st.warning("No forecast data found for the given product.")
            else:
                df = pd.DataFrame(forecast_data)
                df["forecast_date"] = pd.to_datetime(df["forecast_date"])
                
                # Display summary metrics
                st.subheader("Summary Metrics")
                st.metric("Average Forecast", round(df["predicted_demand"].mean(), 2))
                st.metric("Max Forecast", round(df["predicted_demand"].max(), 2))
                st.metric("Min Forecast", round(df["predicted_demand"].min(), 2))
                
                st.subheader("Forecast Data")
                st.dataframe(df)
                
                # Plot with Altair
                chart = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X('forecast_date:T', title='Date'),
                    y=alt.Y('predicted_demand:Q', title='Predicted Demand')
                ).properties(
                    title='Forecasted Demand'
                )
                st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching forecast: {e}")
