from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

delete_order_bp = Blueprint('delete_order', __name__)

@delete_order_bp.route('/delete_order', methods=['POST'])
def delete_order():
    data = request.json
    name = data.get("name")

    # Validar que el nombre de la base de datos sea válido
    if not name or not name.isidentifier():
        return jsonify({"status": "error", "message": "Invalid or missing database name."}), 400

    conn = Postgres_connection()
    if conn:
        try:
            conn.autocommit = True  # Habilitar autocommit
            cur = conn.cursor()  # Crear un cursor

            # Verificar si la base de datos existe
            cur.execute("""
                SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = %s);
            """, (name,))
            db_exists = cur.fetchone()[0]  # True si la base de datos existe, False si no

            if not db_exists:
                return jsonify({"status": "error", "message": f"The database '{name}' does not exist."}), 404

            # Terminar todas las conexiones activas a la base de datos
            cur.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid();
            """, (name,))  # Usar parámetros para evitar inyección de SQL

            # Borrar la base de datos
            cur.execute(f"DROP DATABASE IF EXISTS {name};")

            return jsonify({"status": "success", "message": f"Database '{name}' deleted successfully."}), 200

        except Exception as e:
            conn.rollback()  # Revertir en caso de error
            return jsonify({"status": "error", "message": str(e)}), 500

        finally:
            if cur:
                cur.close()  # Cerrar el cursor
            conn.close()  # Cerrar la conexión
    else:
        return jsonify({"status": "error", "message": "Unable to connect to the database."}), 500
