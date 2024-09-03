from flask import Blueprint, request, jsonify

postman_test_bp = Blueprint('postman_test', __name__) #Convierte cada script en un módulo Flask Blueprint, lo que te permitirá incluirlos en la aplicación principal.

@postman_test_bp.route('/test-data', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify({"status": "success", "received_data": data}), 200
