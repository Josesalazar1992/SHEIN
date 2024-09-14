from flask import Blueprint, request, jsonify
from connection_instance.Data_base_connection import Postgres_connection  # Adjust this import if necessary

user_creation_bp = Blueprint('user_creation', __name__)

@user_creation_bp.route('/user_creation', methods=['POST'])
def user_creation():
    data = request.json
    table_name = data.get("table_name")  # El nombre de la tabla a crear
    db_name = data.get("db_name")  # El nombre de la base de datos en la que se creará la tabla

    # Validar los datos de entrada
    if not table_name or not db_name:
        return jsonify({"status": "error", "message": "Both table name and database name are required."}), 400

    # Validar que los nombres de la tabla y base de datos sean válidos identificadores SQL
    if not table_name.isidentifier() or not db_name.isidentifier():
        return jsonify({"status": "error", "message": "Invalid table or database name."}), 400

    try:
        # Crear una nueva conexión a la base de datos proporcionada
        conn = Postgres_connection(db_name)  # Pass the db_name here
        if conn:
            try:
                conn.autocommit = True  # Habilitar autocommit antes de crear el cursor
                cur = conn.cursor()

                # Crear la tabla
                create_table_sql = '''
                    CREATE TABLE {} (
                        SKU VARCHAR(20) PRIMARY KEY,
                        Description TEXT,
                        Size VARCHAR(20),
                        Quantity INTEGER,
                        Price DECIMAL(10, 2)
                    )
                '''.format(table_name)  # Uso de `format` para crear la tabla con el nombre proporcionado

                cur.execute(create_table_sql)  # Ejecutar la creación de la tabla
                conn.commit()  # Confirmar los cambios en la base de datos

                return jsonify({"status": "success", "message": f"Table '{table_name}' created successfully in database '{db_name}'."}), 200

            except Exception as e:
                conn.rollback()  # Revertir en caso de error
                return jsonify({"status": "error", "message": str(e)}), 500

            finally:
                if cur:
                    cur.close()  # Cerrar el cursor
                conn.close()  # Cerrar la conexión

    except Exception as e:
        return jsonify({"status": "error,  La orden no exite, revise la fecha ", "message": str(e)}), 500

