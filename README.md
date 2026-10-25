# Intelligent Business Operations Analytics Platform

A Python-based business analytics project that analyzes sales, customers, and inventory data to generate useful business insights.

## Features

* Monthly sales revenue analysis
* Top-selling product analysis
* High-value customer identification
* Low-stock inventory monitoring
* Basic sales forecasting
* Interactive dashboard with Streamlit and Plotly
* REST API using FastAPI
* MySQL database integration

## Technologies Used

* Python
* MySQL
* Pandas
* SQLAlchemy
* Streamlit
* Plotly
* FastAPI
* Scikit-learn

## Project Structure

```text
intelligent_business_analytics/
├── app/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── database/
│   └── ml/
├── data/
├── database/
├── .gitignore
└── test_forecasting.py
```

## How to Run

### 1. Install Dependencies

Install the required Python packages in your environment before running the application.

### 2. Run the Streamlit Dashboard

```bash
python -m streamlit run app/dashboard/dashboard.py
```

### 3. Run the FastAPI Server

Open another terminal and run:

```bash
uvicorn app.api.main:app --reload --port 8000
```

API documentation:

`http://127.0.0.1:8000/docs`

## Database Setup

* Install and start MySQL.
* Create the `business_analytics_db` database.
* Use the SQL script in the `database/` folder to create the required tables.
* Configure your database connection locally.
* Never upload database passwords or other secrets to GitHub.

## Forecasting

The project includes a basic forecasting method that uses recent historical sales to estimate future revenue. Forecasts are estimates, not guaranteed results.

## Author

Developed as a Python business analytics portfolio project.
