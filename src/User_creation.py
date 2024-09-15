from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

user_creation_bp = Blueprint('user_creation', __name__)

# Ruta para crear usuarios
@user_creation_bp.route('/user_creation', methods=['POST'])
def user_creation():
    data = request.json
    table_name = data.get("table_name")
    db_name = data.get("db_name")

    if not table_name or not db_name:
        return jsonify({"status": "error", "message": "Both table name and database name are required."}), 400

    if not table_name.isidentifier() or not db_name.isidentifier():
        return jsonify({"status": "error", "message": "Invalid table or database name."}), 400

    try:
        conn = Postgres_connection(db_name)
        if conn:
            try:
                conn.autocommit = True
                cur = conn.cursor()

                create_table_sql = '''
                    CREATE TABLE {} (
                        SKU VARCHAR(20) PRIMARY KEY,
                        Description TEXT,
                        Size VARCHAR(20),
                        Quantity INTEGER,
                        Price DECIMAL(10, 2)
                    )
                '''.format(table_name)

                cur.execute(create_table_sql)
                conn.commit()

                return jsonify({"status": "success", "message": f"Table '{table_name}' created successfully in database '{db_name}'."}), 200

            except Exception as e:
                conn.rollback()
                return jsonify({"status": "error", "message": str(e)}), 500

            finally:
                if cur:
                    cur.close()
                conn.close()

    except Exception as e:
        return jsonify({"status": "error", "message": "Database does not exist."}), 500


