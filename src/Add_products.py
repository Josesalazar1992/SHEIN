from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection

add_products_bp = Blueprint('add_products', __name__)

@add_products_bp.route('/add_products', methods=['POST'])
def insert_data():

    data = request.json
    db_name = data.get("db_name")
    name = data.get("name")
    sku = data.get("SKU")
    description = data.get("Description")
    size = data.get("Size")
    quantity = data.get("Quantity")
    price = data.get("Price")

    # Validar los datos
    if not all([name, sku, description, size, quantity is not None, price is not None]):
        return jsonify({"status": "error", "message": "Some required fields are missing or invalid."}), 400

    conn = Postgres_connection(db_name)
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()
        # Asume que 'name' es el nombre de la tabla;
        insert_sql = f'''
        INSERT INTO {name} (SKU, Description, Size, Quantity, Price)
        VALUES (%s, %s, %s, %s, %s)
        '''
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
