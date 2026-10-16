import pandas as pd

from app.analytics.sales import get_monthly_sales


def forecast_sales(monthly_sales, future_months=3):
    """
    Forecast future sales using the average of recent months.
    """

    if future_months < 1:
        raise ValueError("Future months must be at least 1.")

    if not monthly_sales or len(monthly_sales) < 2:
        raise ValueError(
            "At least 2 months of sales data is required."
        )

    df = pd.DataFrame(monthly_sales).copy()

    required_columns = {"year", "month", "revenue"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Data must contain year, month, and revenue columns."
        )

    for column in ["year", "month", "revenue"]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df = df.dropna(
        subset=["year", "month", "revenue"]
    ).copy()

    if len(df) < 2:
        raise ValueError(
            "At least 2 valid monthly sales records are required."
        )

    df = df.sort_values(
        ["year", "month"]
    ).reset_index(drop=True)

    df["date"] = pd.to_datetime(
        {
            "year": df["year"].astype(int),
            "month": df["month"].astype(int),
            "day": 1
        },
        errors="coerce"
    )

    df = df.dropna(subset=["date"]).copy()

    if len(df) < 2:
        raise ValueError(
            "At least 2 valid monthly dates are required."
        )

    # Use the latest 3 months when available
    recent_sales = df["revenue"].tail(3)

    # Calculate average monthly revenue
    average_revenue = recent_sales.mean()

    # Generate future month dates
    last_date = df["date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.offsets.MonthBegin(1),
        periods=future_months,
        freq="MS"
    )

    # Use average revenue as a simple baseline forecast
    predictions = [round(max(0, average_revenue), 2)] * future_months

    results = pd.DataFrame({
        "month": future_dates.strftime("%B %Y"),
        "predicted_revenue": predictions
    })

    return results


def forecast_from_database(future_months=3):
    """
    Fetch monthly sales from MySQL and forecast future revenue.
    """

    monthly_sales = get_monthly_sales()

    if not monthly_sales or len(monthly_sales) < 2:
        raise ValueError(
            "At least 2 months of sales data is required."
        )

    sales_data = []

    for row in monthly_sales:
        sales_data.append({
            "year": int(row[0]),
            "month": int(row[1]),
            "revenue": float(row[2] or 0)
        })

    return forecast_sales(
        sales_data,
        future_months=future_months
    )