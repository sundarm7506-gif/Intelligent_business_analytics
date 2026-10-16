from sqlalchemy import text
from app.database.connection import engine
def get_total_revenue():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT SUM(total_amount) FROM orders")
        )
        total_revenue = result.scalar()
        return total_revenue
def get_total_orders():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        )
        total_orders = result.scalar()
        return total_orders
def get_average_order_value():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT AVG(total_amount) FROM orders")
        )
        average_order_value = result.scalar()
        return average_order_value
def get_monthly_sales():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    YEAR(order_date) AS year,
                    MONTH(order_date) AS month,
                    SUM(total_amount) AS revenue
                FROM orders
                GROUP BY YEAR(order_date), MONTH(order_date)
                ORDER BY year, month
            """)
        )
        return result.fetchall()
def get_top_products():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    p.product_name,
                    SUM(oi.quantity) AS total_quantity
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                GROUP BY p.product_id, p.product_name
                ORDER BY total_quantity DESC
                LIMIT 5
            """)
        )
        return result.fetchall()
def get_product_revenue():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    p.product_name,
                    SUM(oi.quantity * oi.unit_price) AS revenue
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                GROUP BY p.product_id, p.product_name
                ORDER BY revenue DESC
                LIMIT 5
            """)
        )
        return result.fetchall()
def get_sales_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT SUM(total_amount) AS revenue
                FROM orders
                WHERE order_date = :selected_date
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()  
def get_sales_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT SUM(total_amount) AS revenue
                FROM orders
                WHERE order_date = :selected_date
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()      
def get_orders_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*) 
                FROM orders
                WHERE order_date = :selected_date
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()
def get_top_products_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    p.product_name,
                    SUM(oi.quantity) AS total_quantity
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                JOIN orders o
                    ON oi.order_id = o.order_id
                WHERE o.order_date = :selected_date
                GROUP BY p.product_id, p.product_name
                ORDER BY total_quantity DESC
                LIMIT 5
            """),
            {
                "selected_date": selected_date
            }
        )
        return result.fetchall()    