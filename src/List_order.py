from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

list_order_bp = Blueprint('list_order', __name__)

# Ruta para crear usuarios
@list_order_bp.route('/list_order', methods=['GET'])
def user_creation():
    try:
        conn = Postgres_connection()
        if conn:
            try:
                conn.autocommit = True
                cur = conn.cursor()

                # Ejecutar consulta para obtener todas las bases de datos
                cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres';")

                # Obtener resultados
                databases = cur.fetchall()

                # Crear una lista con los nombres de las bases de datos
                db_list = [db[0] for db in databases]

                # Cerrar cursor y conexión
                cur.close()
                conn.close()

                # Devolver la lista de bases de datos como JSON
                return jsonify({"databases": db_list}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
