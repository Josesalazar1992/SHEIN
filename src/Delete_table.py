from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

delete_table_bp = Blueprint('delete_table', __name__)

@delete_table_bp.route('/delete_table', methods=['POST'])
def delete_table():
    data = request.json
    name = data.get("name")

    # Validar que el nombre de la tabla sea seguro
    if not name or not name.isidentifier():
        return jsonify({"status": "error", "message": "Invalid or missing table name."}), 400

    # Conexión a la base de datos
    conn = Postgres_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()

        # Usar DROP TABLE para eliminar la tabla
        drop_sql = f"DROP TABLE IF EXISTS {name}"

        # Ejecutar el query
        cur.execute(drop_sql)
        conn.commit()

        return jsonify({"status": "success", "message": f"Table '{name}' deleted successfully."}), 200

    except Exception as e:
        print(f"Unable to delete table: {e}")
        conn.rollback()
        return jsonify({"status": "error", "message": f"Unable to delete table '{name}'."}), 500

    finally:
        if conn:
            cur.close()
            conn.close()
