from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection # Importa la coneccion a postgres del file Data_base_connection.

delete_order_bp = Blueprint('delete_order', __name__) #Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@delete_order_bp.route('/delete_order', methods=['POST'])
def delete_order():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"status": "error", "message": "Name of the database is required."}), 400

    conn = Postgres_connection()
    if conn:
        try:
            cur = conn.cursor() # Crear un cursor
            conn.autocommit = True # Necesario para ejecutar comandos de eliminacion de base de datos

            # Terminar todas las conexiones activas a la base de datos
            cur.execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{name}' AND pid <> pg_backend_pid();
            """)

            cur.execute(f"DROP DATABASE IF EXISTS {name};") # borrar la base de datos

            return jsonify({"status": "success", "message": f"Client '{name}' deleted."}), 200

        except Exception as e:
            conn.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

        finally:
            cur.close() # Cerrar la conexión
            conn.close()
    else:
        return jsonify({"status": "error", "message": "Unable to connect to database"}), 500
