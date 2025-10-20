import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from app import models

DB_NAME = "winedb"
APP_USER = "wineuser"
APP_PASSWORD = "yourpassword"
DB_HOST = "localhost"
DB_PORT = "5432"

def init_db():
    # Connect as superuser
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",  # superuser
        password="your_postgres_password",
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Create database if not exists
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"✅ Database {DB_NAME} created.")
    else:
        print(f"ℹ️ Database {DB_NAME} already exists.")

    # Create app user if not exists
    cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{APP_USER}'")
    if not cur.fetchone():
        cur.execute(f"CREATE USER {APP_USER} WITH PASSWORD '{APP_PASSWORD}'")
        print(f"✅ User {APP_USER} created.")
    else:
        print(f"ℹ️ User {APP_USER} already exists.")

    # Grant privileges
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {APP_USER}")

    cur.close()
    conn.close()

    # Ensure schema (tables) exist using app user
    engine = create_engine(f"postgresql://{APP_USER}:{APP_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    models.Base.metadata.create_all(bind=engine)
    print("✅ Schema ensured.")

if __name__ == "__main__":
    init_db()