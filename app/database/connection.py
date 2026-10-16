from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="sund@r12",
    host="localhost",
    port=3306,
    database="business_analytics_db",
)

engine = create_engine(connection_url)