from sqlalchemy import text
from db import engine

with engine.connect() as conn:
    print(conn.execute(text("SHOW TABLES")).fetchall())