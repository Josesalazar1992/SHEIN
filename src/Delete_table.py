from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

delete_table_bp = Blueprint('delete_table', __name__)

@delete_table_bp.route('/delete_table', methods=['POST'])
def delete_table():
    data = request.json
    name = data.get("name")
    db_name = data.get("db_name")

    # Validar que el nombre de la tabla sea seguro
    if not name or not db_name:
        return jsonify({"status": "error", "message": "Both table name and database name are required."}), 400

    # Conexión a la base de datos
    conn = Postgres_connection(db_name)
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()

        # Verificar si la tabla existe en la base de datos
        check_table_sql = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            )
        """
        cur.execute(check_table_sql, (name,))
        table_exists = cur.fetchone()[0]  # True si la tabla existe, False si no

        if table_exists:
            # Usar DROP TABLE para eliminar la tabla
            drop_sql = f"DROP TABLE IF EXISTS {name}"
            cur.execute(drop_sql)
            conn.commit()

            return jsonify({"status": "success", "message": f"Table '{name}' deleted successfully."}), 200

        elif not table_exists:
            # Si la tabla no existe, retornar un error
            return jsonify({"status": "error", "message": f"Table '{name}' does not exist."}), 400

    except Exception as e:
        print(f"Unable to delete table: {e}")
        conn.rollback()
        return jsonify({"status": "error", "message": f"Unable to delete table '{name}'."}), 500

    finally:
        if conn:
            cur.close()
            conn.close()
