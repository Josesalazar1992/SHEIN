from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection # Importa la coneccion a postgres del file Data_base_connection.

order_creation_bp = Blueprint('order_creation', __name__) #Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@order_creation_bp.route('/order_creation', methods=['POST'])
def order_creation():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"status": "error", "message": "Nombre de la orden no ha sido ingresada."}), 400

    conn = Postgres_connection()
    if conn:
        try:
            cur = conn.cursor() # Crear un cursor
            conn.autocommit = True # Necesario para ejecutar comandos de creación de base de datos
            cur.execute(f"CREATE DATABASE {name};") # Crear la base de datos

            return jsonify({"status": "success", "message": f"Orden de compra '{name}' creada."}), 200

        except Exception as e:
            conn.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

        finally:
            cur.close() # Cerrar la conexión
            conn.close()
    else:
        return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"}), 500
