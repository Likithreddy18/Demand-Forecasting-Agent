# Demand-Forecasting-Agent


This project provides a **Demand Forecasting Agent** built with **FastAPI**, **Nixtla’s TimeGPT**, and **SQLAlchemy** for storing forecasts in a PostgreSQL database. It also includes a **Streamlit** web application for visualizing and interacting with forecast data.

## Features

- **Forecast Generation**:  
  Uses Nixtla (TimeGPT) to generate demand forecasts for multiple products.

- **FastAPI Service**:  
  Exposes REST endpoints to query forecast data (e.g., `/forecast/{product_id}?days_ahead=N`).

- **Database Integration**:  
  Stores forecast results in a PostgreSQL database for persistent access.

- **Duplicate Removal**:  
  Ensures no duplicate forecasts are stored when the agent is run multiple times.

- **Streamlit Dashboard**:  
  An interactive webapp for exploring and visualizing forecast data.

## Repository Structure

```
.
├── Dockerfile                  # Docker instructions for containerizing the app
├── config.py                   # Loads environment variables (DB, API keys)
├── entrypoint.sh               # Entry script (if using a Docker entrypoint)
├── forecast_agent.py           # Generates forecasts & writes them to the DB
├── forecast_api.py             # FastAPI service exposing the forecast endpoints
├── remove_duplicates.py        # (Optional) Script to clean up duplicate forecasts
├── requirements.txt            # Python dependencies
├── streamlit_app.py            # Streamlit web application for forecast visualization
└── data/
    └── realistic_food_demand_dataset.csv   # Example synthetic dataset
```

## Getting Started

### Prerequisites

- **Python 3.9+**
- **PostgreSQL** (local or hosted)
- **Docker** (optional, for containerization)
- **Git** and a GitHub account
- **Nixtla API Key** (TimeGPT) if you want to generate real forecasts

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file or export environment variables directly. For example:

```bash
# .env file (example)
DATABASE_URL=postgresql://username:password@host:5432/dbname
TIMEGPT_API_KEY=your_timegpt_api_key
DATA_DIR=data
```

> **Note:** Make sure `config.py` uses `os.getenv("DATABASE_URL")` and `os.getenv("TIMEGPT_API_KEY")`.

## Usage

### 1. Run the Forecast Agent

The agent reads from your synthetic dataset (or real data), generates forecasts, and stores them in the DB.

```bash
python forecast_agent.py
```

### 2. Remove Duplicates (Optional)

If you have a separate script to clean duplicates, run:

```bash
python remove_duplicates.py
```

### 3. Start the FastAPI Service

```bash
uvicorn forecast_api:app --reload
```

Open your browser at [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API via Swagger UI.

### 4. Streamlit Dashboard

**Locally**:
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) to interact with the dashboard.

## Deployed Webapp

A live version of the **Streamlit dashboard** is available at:
> **[Streamlit Webapp](https://demand-forecasting-agent-3vzhhixwbk6awoykbuet72.streamlit.app/)**

You can enter a product ID and forecast horizon to visualize predictions. The dashboard communicates with the FastAPI service to fetch forecast data.

## Docker 

### Build the Docker Image

```bash
docker build -t forecasting-agent .
```

### Run the Container

```bash
docker run -p 8000:8000 forecasting-agent
```

The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs).  
If you included an entrypoint script that runs `forecast_agent.py` and `remove_duplicates.py` first, those will run before the API starts.

## FAQ / Troubleshooting

1. **Relation "product_forecasts" does not exist**  
   - Ensure `forecast_agent.py` has been run and successfully created the table in the database.
   - Check that `DATABASE_URL` points to the correct DB instance.

2. **Connection refused**  
   - Verify you have the correct DB credentials or you’re using the correct environment variables on your hosting platform (e.g., Railway).

3. **TimeGPT / Nixtla errors**  
   - Make sure your Nixtla API key is valid and set as an environment variable.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## License

[MIT License](LICENSE)

## Contact

For questions or feedback, reach out via [email](chlikith@utexas.edu).

---

**Enjoy exploring and forecasting with this Demand Forecasting Agent!**
