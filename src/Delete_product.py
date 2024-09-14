from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection  # Importa la conexión a postgres.

delete_product_bp = Blueprint('delete_product', __name__)  # Convierte cada script en un módulo Flask Blueprint.

@delete_product_bp.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.json
    db_name = data.get("db_name")
    name = data.get("name")  # Nombre de la tabla
    sku = data.get("SKU")  # SKU del producto

    # Verificar que los datos necesarios están presentes
    if not all([name, sku]):
        return jsonify({"status": "error", "message": "Data from JSON is missing or incorrect."}), 400

    conn = Postgres_connection(db_name)  # Conexión a la base de datos
    if conn is None:
        return jsonify({"status": "error", "message": "Could not connect to the database."}), 500

    try:
        cur = conn.cursor()

        # Verificar si el producto con el SKU existe
        check_product_sql = '''
        SELECT EXISTS(
            SELECT 1 FROM {} WHERE SKU = %s
        )
        '''.format(name)
        cur.execute(check_product_sql, (sku,))
        product_exists = cur.fetchone()[0]  # True si existe, False si no

        if not product_exists:
            return jsonify({"status": "error", "message": "El producto no existe."}), 404

        # Si el producto existe, proceder a eliminarlo
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
