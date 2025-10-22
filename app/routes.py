from flask import Blueprint, request, jsonify, render_template
from .api import ghanapost

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/get_location', methods=['POST'])
def get_location_route():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({"error": "Address code is required"}), 400
    
    defaults = ghanapost.get_default_params()
    response = ghanapost.get_location(code, defaults)
    return jsonify({"response": response})

@main.route('/api/get_address', methods=['POST'])
def get_address_route():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    defaults = ghanapost.get_default_params()
    response = ghanapost.get_address(latitude, longitude, defaults)
    return jsonify({"response": response})
