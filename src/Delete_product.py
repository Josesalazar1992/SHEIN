from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection # Importa la coneccion a postgres del file Data_base_connection.

delete_product_bp = Blueprint('delete_product', __name__) # Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@delete_product_bp.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.json
    name = data.get("name")
    sku = data.get("SKU")

    if not all([name, sku]):
        return jsonify({"status": "error", "message": "Data from JSON is missing or incorrect."}), 400

    conn = Postgres_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()
        delete_sql = '''
        DELETE FROM {}
        WHERE SKU = %s
        '''.format(name)
        cur.execute(delete_sql, (sku,))
        conn.commit()
        return jsonify({"status": "success", "message": "Product deleted successfully."}), 200

    except Exception as e:
        print(f"Unable to delete data: {e}")
        conn.rollback()
        return jsonify({"status": "error", "message": "Unable to delete data."}), 500
    finally:
        if conn:
            cur.close()
            conn.close()
