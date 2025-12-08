from flask import Blueprint, jsonify, request
from controllers.camera_controller import create_camera, delete_camera, update_camera, get_camera_by_id, get_all_cameras, get_cameras_by_company
from helpers.token_validation import validate_token
from models.camera_model import Camera

camera = Blueprint("camera", __name__)

@camera.route('/cameras/', methods=['POST'])
def add_camera():
    try:
        token = validate_token()
        
        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        camera_data = request.json

        if 'companyId' not in camera_data or not camera_data['companyId']:
            return jsonify({'error': 'companyId is required and cannot be empty'}), 400
        if 'name' not in camera_data or not camera_data['name']:
            return jsonify({'error': 'name is required and cannot be empty'}), 400

        result = create_camera(camera_data, token)

        return jsonify({"id": result}), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@camera.route('/cameras/<camera_id>', methods=['DELETE'])
def delete_camera_route(camera_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        try:
            delete_camera(camera_id, token)
            return jsonify({"cameraId": camera_id}), 200
        except Exception as err:
            if str(err) == "Camera not found":
                return jsonify({"error": "Camera not found"}), 404
            else:
                raise

    except Exception as err:
        error_message = str(err)
        return jsonify({"error": f"An error occurred: {error_message}"}), 500


@camera.route('/cameras/<camera_id>', methods=['PATCH'])
def update_camera_route(camera_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        request_data = request.json

        if "companyId" in request_data:
            return jsonify({"error": "companyId cannot be updated"}), 400
        if "_id" in request_data:
            return jsonify({"error": "_id cannot be updated"}), 400

        update_camera(camera_id, request_data, token)

        return jsonify({"cameraId": camera_id}), 200
    
    except Exception as e:
        error_message = str(e)
        if error_message == "Camera not found":
            return jsonify({"error": error_message}), 404
        else:
            return jsonify({"error": f"An error occurred: {error_message}"}), 500
    except:
        return jsonify({'error': 'Something wrong happened when updating camera!'}), 500


@camera.route('/cameras/<camera_id>', methods=['GET'])
def get_camera(camera_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        camera_data = get_camera_by_id(camera_id, token)
        return jsonify(camera_data), 200

    except Exception as err:
        error_message = str(err)
        if error_message == "Camera not found":
            return jsonify({"error": error_message}), 404
        return jsonify({'error': f'Error fetching camera: {error_message}'}), 500


@camera.route('/cameras/', methods=['GET'])
def list_cameras():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        cameras = get_all_cameras(token)
        return jsonify({"cameras": cameras}), 200

    except Exception as err:
        return jsonify({'error': f'Error in get cameras: {str(err)}'}), 500
    


@camera.route('/cameras/company/<company_id>', methods=['GET'])
def get_cameras_by_company_route(company_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        cameras = get_cameras_by_company(company_id, token)
        return jsonify({"cameras": cameras}), 200

    except Exception as err:
        error_message = str(err)
        if error_message == "No cameras found for this company":
            return jsonify({"error": error_message}), 404
        return jsonify({'error': f'Error fetching cameras by company: {error_message}'}), 500