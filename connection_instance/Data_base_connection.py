# Con el fin de utilizar Python para interactuar con una base de datos PostgreSQL, 
# tenemos que hacer una conexión. Esto se hace con la función psycopg2 connect(), 
# que crea una nueva sesión de base de datos y devuelve una nueva instancia de conexión.

import psycopg2
from psycopg2 import OperationalError

def Postgres_connection() -> psycopg2.extensions.connection:

# Establishes a connection to the PostgreSQL database and returns the connection object.
# If an error occurs, returns None.

    conn = None
    try:
        # Stablish connection
        conn = psycopg2.connect(
            database="Clientes",
            user="postgres",
            host="localhost",
            password="Cyberark1",
            port=5432
        )
        print("Connection successful.")
    except OperationalError as e:
        print(f"Database connection error: {e}")
    return conn
