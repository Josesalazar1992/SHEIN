from flask import Flask
from flask_cors import CORS
from src.Add_products import add_products_bp
from src.Delete_product import delete_product_bp
from Test_files.Postman_test import postman_test_bp
from src.User_creation import user_creation_bp
from src.Order_creation import order_creation_bp
from src.Delete_order import delete_order_bp
from src.Delete_table import delete_table_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints, Módulo de Enrutador que combina las diferentes aplicaciones en una sola instancia de Flask
app.register_blueprint(add_products_bp)
app.register_blueprint(delete_product_bp)
app.register_blueprint(postman_test_bp)
app.register_blueprint(user_creation_bp)
app.register_blueprint(order_creation_bp)
app.register_blueprint(delete_order_bp)
app.register_blueprint(delete_table_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
