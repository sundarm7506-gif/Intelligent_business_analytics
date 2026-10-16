from sqlalchemy import text
from app.database.connection import engine
def get_total_customers():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        )
        total_customers = result.scalar()
        return total_customers
total_customers = get_total_customers()
print("Total Customers:", total_customers)
def get_new_customers():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM customers
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """)
        )
        new_customers = result.scalar()
        return new_customers
new_customers = get_new_customers()
print("New Customers (Last 30 Days):", new_customers)
def get_repeat_customers():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM (
                    SELECT customer_id
                    FROM orders
                    GROUP BY customer_id
                    HAVING COUNT(order_id) >= 2
                ) AS repeat_customers
            """)
        )
        repeat_customers = result.scalar()
        return repeat_customers
repeat_customers = get_repeat_customers()
print("Repeat Customers:", repeat_customers) 
def get_high_value_customers():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    c.customer_name,
                    SUM(o.total_amount) AS total_spent
                FROM customers c
                JOIN orders o
                    ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.customer_name
                ORDER BY total_spent DESC
                LIMIT 5
            """)
        )
        return result.fetchall() 
high_value_customers = get_high_value_customers()
print("Top 5 High-Value Customers:")
for row in high_value_customers:
    print(row)


def get_customers_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(DISTINCT customer_id)
                FROM orders
                WHERE order_date = :selected_date
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()   
def get_repeat_customers_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM (
                    SELECT customer_id
                    FROM orders
                    WHERE order_date = :selected_date
                    AND customer_id IN (
                        SELECT customer_id
                        FROM orders
                        GROUP BY customer_id
                        HAVING COUNT(order_id) >= 2
                    )
                    GROUP BY customer_id
                ) AS repeat_customers
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()
def get_new_customers_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM customers
                WHERE created_at = :selected_date
            """),
            {
                "selected_date": selected_date
            }
        )

        return result.scalar()  
def get_high_value_customers_by_date(selected_date):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    c.customer_name,
                    SUM(o.total_amount) AS total_spent
                FROM customers c
                JOIN orders o
                    ON c.customer_id = o.customer_id
                WHERE o.order_date = :selected_date
                GROUP BY c.customer_id, c.customer_name
                ORDER BY total_spent DESC
                LIMIT 5
            """),
            {
                "selected_date": selected_date
            }
        )
        return result.fetchall()                
    