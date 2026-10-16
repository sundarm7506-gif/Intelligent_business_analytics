from app.ml.forecasting import forecast_from_database
import streamlit as st
import plotly.express as px

from app.analytics.sales import (
    get_total_revenue,
    get_total_orders,
    get_monthly_sales,
    get_top_products,
    get_top_products_by_date,
    get_sales_by_date,
    get_orders_by_date,
)

from app.analytics.customers import (
    get_total_customers,
    get_repeat_customers,
    get_high_value_customers,
    get_new_customers,
    get_customers_by_date,
    get_repeat_customers_by_date,
    get_new_customers_by_date,
    get_high_value_customers_by_date,
)

from app.analytics.inventory import get_low_stock_products


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)


# --------------------------------
# Dashboard Title
# --------------------------------

st.title("📊 Business Analytics Dashboard")
st.write("Welcome to the Business Analytics Platform")


# --------------------------------
# Date Filter
# --------------------------------

st.subheader("📅 Filter")

selected_date = st.date_input("Select Date")

st.write("Selected Date:", selected_date)


# --------------------------------
# KPI Metrics
# --------------------------------

revenue = get_sales_by_date(selected_date)
orders = get_orders_by_date(selected_date)
customers = get_customers_by_date(selected_date)
repeat_customers = get_repeat_customers_by_date(selected_date)
new_customers = get_new_customers_by_date(selected_date)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"₹{revenue or 0:,.2f}",
)

col2.metric(
    "Total Orders",
    orders or 0,
)

col3.metric(
    "Total Customers",
    customers or 0,
)

col4.metric(
    "Repeat Customers",
    repeat_customers or 0,
)

col5.metric(
    "New Customers",
    new_customers or 0,
)


# --------------------------------
# Monthly Sales
# --------------------------------

st.subheader("📈 Monthly Sales")

monthly_sales = get_monthly_sales()

months = [
    f"{row.year}-{row.month:02d}"
    for row in monthly_sales
]

revenues = [
    float(row.revenue or 0)
    for row in monthly_sales
]

monthly_chart_data = {
    "Month": months,
    "Revenue": revenues,
}

if monthly_chart_data["Month"]:
    fig_monthly = px.line(
        monthly_chart_data,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend",
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
    )
else:
    st.info("No monthly sales data available.")


# --------------------------------
# Top 5 Products
# --------------------------------

st.subheader("🏆 Top 5 Products")

top_products = get_top_products_by_date(selected_date)

product_names = [
    row.product_name
    for row in top_products
]

quantities = [
    int(row.total_quantity or 0)
    for row in top_products
]

top_products_data = {
    "Product": product_names,
    "Quantity Sold": quantities,
}

if product_names:
    fig_products = px.bar(
        top_products_data,
        x="Quantity Sold",
        y="Product",
        orientation="h",
        text="Quantity Sold",
        title="Top 5 Products by Quantity Sold",
    )

    fig_products.update_traces(
        textposition="outside",
    )

    fig_products.update_layout(
        xaxis_title="Quantity Sold",
        yaxis_title="Product",
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True,
    )
else:
    st.info("No product sales found for the selected date.")


# --------------------------------
# Low Stock Products
# --------------------------------

st.subheader("⚠️ Low Stock Products")

low_stock_products = get_low_stock_products()

stock_product_names = [
    row.product_name
    for row in low_stock_products
]

stock_quantities = [
    int(row.stock_quantity or 0)
    for row in low_stock_products
]

stock_data = {
    "Product": stock_product_names,
    "Current Stock": stock_quantities,
}

if stock_product_names:
    fig_stock = px.bar(
        stock_data,
        x="Product",
        y="Current Stock",
        text="Current Stock",
        title="Low Stock Products",
    )

    fig_stock.update_layout(
        xaxis_title="Product",
        yaxis_title="Current Stock",
        height=400,
    )

    fig_stock.update_traces(
        textposition="outside",
    )

    st.plotly_chart(
        fig_stock,
        use_container_width=True,
    )
else:
    st.success("No low-stock products found.")


# --------------------------------
# High-Value Customers
# --------------------------------

st.subheader("👑 Top 5 High-Value Customers")

high_value_customers = get_high_value_customers_by_date(
    selected_date
)

customer_names = [
    row.customer_name
    for row in high_value_customers
]

total_spent = [
    float(row.total_spent or 0)
    for row in high_value_customers
]

# Create a DataFrame for Plotly
customer_data = {
    "Customer": customer_names,
    "Total Spent": total_spent,
}

if customer_names:
    fig_customers = px.bar(
        customer_data,
        x="Customer",
        y="Total Spent",
        text="Total Spent",
        title="Top 5 High-Value Customers",
    )

    fig_customers.update_layout(
        xaxis_title="Customer",
        yaxis_title="Total Spent (₹)",
        height=400,
    )

    fig_customers.update_traces(
        textposition="outside",
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True,
    )
else:
    st.info("No high-value customers found for the selected date.")
# Sales Forecast
st.subheader("📈 Sales Forecast")

try:
    forecast_df = forecast_from_database(future_months=3)

    st.line_chart(
    forecast_df.set_index("month")[
        "predicted_revenue"
    ]
)

    st.dataframe(forecast_df, use_container_width=True)

except Exception as e:
    st.warning(f"Sales forecast unavailable: {e}")    