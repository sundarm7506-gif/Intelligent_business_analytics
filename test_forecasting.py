from app.ml.forecasting import forecast_from_database

try:
    result = forecast_from_database(future_months=3)

    print("\nSales Forecast:")
    print(result.to_string(index=False))

except Exception as e:
    print("Forecasting Error:", e)