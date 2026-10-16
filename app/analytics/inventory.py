from sqlalchemy import text
from app.database.connection import engine
def get_low_stock_products():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    p.product_name,
                    i.stock_quantity,
                    i.reorder_level
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
                WHERE i.stock_quantity <= i.reorder_level
                ORDER BY i.stock_quantity ASC
            """)
        )
        return result.fetchall()
low_stock = get_low_stock_products()
print("Low Stock Products:")
for row in low_stock:
    print(row)