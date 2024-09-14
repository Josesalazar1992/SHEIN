import psycopg2
from psycopg2 import OperationalError

def Postgres_connection(db_name = None) -> psycopg2.extensions.connection:

    # Establishes a connection to the PostgreSQL database and returns the connection object.
    # If an error occurs, returns None.
    
    conn = None
    try:
        # Stablish connection using the dynamic db_name
        conn = psycopg2.connect(
            database=db_name,  # Use the db_name passed from user_creation
            user="postgres",
            host="localhost",
            password="Cyberark1",
            port=5432
        )
        print(f"Connection to database '{db_name}' successful.")
    except OperationalError as e:
        print(f"Database connection error: {e}")
    return conn
