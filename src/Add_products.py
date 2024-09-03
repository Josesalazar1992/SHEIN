from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection # Importa la coneccion a postgres del file Data_base_connection.

add_products_bp = Blueprint('add_products', __name__) # Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@add_products_bp.route('/add_products', methods=['POST'])
def insert_data():
    data = request.json
    name = data.get("name")
    sku = data.get("SKU")
    description = data.get("Description")
    size = data.get("Size")
    quantity = data.get("Quantity")
    price = data.get("Price")

    if not all([name, sku, description, size, quantity is not None, price is not None]):
        return jsonify({"status": "error", "message": "Data from JSON is missing or incorrect."}), 400

    conn = Postgres_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()
        insert_sql = '''
        INSERT INTO {} (SKU, Description, Size, Quantity, Price)
        VALUES (%s, %s, %s, %s, %s)
        '''.format(name)
        insert_data = (sku, description, size, quantity, price)
        cur.execute(insert_sql, insert_data)
        conn.commit()
        return jsonify({"status": "success", "message": "Data inserted successfully."}), 200

    except Exception as e:
        print(f"Unable to insert data: {e}")
        conn.rollback()
        return jsonify({"status": "error", "message": "Unable to insert data."}), 500
    finally:
        if conn:
            cur.close()
            conn.close()
