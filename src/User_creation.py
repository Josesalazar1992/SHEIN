from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection # Importa la coneccion a postgres del file Data_base_connection.

user_creation_bp = Blueprint('user_creation', __name__) #Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@user_creation_bp.route('/user_creation', methods=['POST'])
def user_creation():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"status": "error", "message": "Name of the client is required."}), 400

    conn = Postgres_connection()
    if conn:
        try:
            cur = conn.cursor()
            create_table_sql = '''
            CREATE TABLE {} (
                SKU VARCHAR(20) PRIMARY KEY,
                Description TEXT,
                Size VARCHAR(20),
                Quantity INTEGER,
                Price DECIMAL(10, 2)
            )
            '''.format(name)
            cur.execute(create_table_sql)
            conn.commit()
            return jsonify({"status": "success", "message": f"Client '{name}' created."}), 200

        except Exception as e:
            conn.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"status": "error", "message": "Unable to connect to database"}), 500
