from flask import Flask
from src.Add_products import add_products_bp
from src.Delete_product import delete_product_bp
from Test_files.Postman_test import postman_test_bp
from src.User_creation import user_creation_bp

app = Flask(__name__)

# Register Blueprints, Módulo de Enrutador que combina las diferentes aplicaciones en una sola instancia de Flask
app.register_blueprint(add_products_bp)
app.register_blueprint(delete_product_bp)
app.register_blueprint(postman_test_bp)
app.register_blueprint(user_creation_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
