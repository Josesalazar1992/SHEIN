from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

delete_order_bp = Blueprint('delete_order', __name__)

@delete_order_bp.route('/delete_order', methods=['POST'])
def delete_order():
    data = request.json
    name = data.get("name")

    if not name or not name.isidentifier():
        return jsonify({"status": "error", "message": "Invalid or missing database name."}), 400

    conn = Postgres_connection()
    if conn:
        try:
            conn.autocommit = True  # Habilitar autocommit antes de crear el cursor
            cur = conn.cursor()  # Crear un cursor

            # Terminar todas las conexiones activas a la base de datos
            cur.execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid();
            """, (name,))  # Usar parámetros para evitar inyección de SQL

            # Borrar la base de datos
            cur.execute(f"DROP DATABASE IF EXISTS {name};")

            return jsonify({"status": "success", "message": f"Database '{name}' deleted."}), 200

        except Exception as e:
            conn.rollback()  # Revertir en caso de error
            return jsonify({"status": "error", "message": str(e)}), 500

        finally:
            if cur:
                cur.close()  # Cerrar el cursor
            conn.close()  # Cerrar la conexión
    else:
        return jsonify({"status": "error", "message": "Unable to connect to the database."}), 500
