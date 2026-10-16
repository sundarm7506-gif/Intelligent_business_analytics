from app.ml.forecasting import forecast_from_database
from fastapi import FastAPI, HTTPException
from app.analytics.inventory import get_low_stock_products
from app.analytics.sales import (
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_monthly_sales,
    get_top_products,
)
from app.analytics.customers import (
    get_total_customers,
    get_new_customers,
    get_repeat_customers,
    get_high_value_customers
)
app = FastAPI(title="Business Analytics API")
@app.get("/")
def home():
    return {"message": "Business Analytics API is running"}
@app.get("/revenue")
def revenue():
    total_revenue = get_total_revenue()
    return {
        "total_revenue": total_revenue
    }
@app.get("/orders")
def orders():
    total_orders = get_total_orders()
    return {
        "total_orders": total_orders
    }
@app.get("/average-order-value")
def average_order_value():
    aov = get_average_order_value()
    return {
        "average_order_value": aov
    }
@app.get("/monthly-sales")
def monthly_sales():
    sales = get_monthly_sales()
    return {
        "monthly_sales": [
            {
                "year": row.year,
                "month": row.month,
                "revenue": float(row.revenue)
            }
            for row in sales
        ]
    }
@app.get("/top-products")
def top_products():
    products = get_top_products()
    return {
        "top_products": [
            {
                "product_name": row.product_name,
                "total_quantity": row.total_quantity
            }
            for row in products
        ]
    }
@app.get("/low-stock")
def low_stock():
    products = get_low_stock_products()
    return {
        "low_stock_products": [
            {
                "product_name": row.product_name,
                "stock_quantity": row.stock_quantity,
                "reorder_level": row.reorder_level
            }
            for row in products
        ]
    } 
@app.get("/customers")
def customers():
    total_customers = get_total_customers()
    return {
        "total_customers": total_customers
    } 
@app.get("/new-customers")
def new_customers():
    new_customers = get_new_customers()
    return {
        "new_customers": new_customers
    }   
@app.get("/repeat-customers")
def repeat_customers():
    repeat_customers = get_repeat_customers()
    return {
        "repeat_customers": repeat_customers
    } 
@app.get("/high-value-customers")
def high_value_customers():
    customers = get_high_value_customers()
    return {
        "high_value_customers": [
            {
                "customer_name": row.customer_name,
                "total_spent": float(row.total_spent)
            }
            for row in customers
        ]
    } 
@app.get("/forecast")
def get_sales_forecast(future_months: int = 3):
    try:
        forecast = forecast_from_database(
            future_months=future_months
        )

        return forecast.to_dict(orient="records")

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )              