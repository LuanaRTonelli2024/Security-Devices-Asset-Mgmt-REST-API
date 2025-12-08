from flask import Blueprint, jsonify, request
from controllers.company_controller import create_company, delete_company, update_company, get_company_by_id, get_all_companies
from helpers.token_validation import validate_token
from models.company_model import Company

company = Blueprint("company", __name__)

@company.route('/companies/', methods=['POST'])
def add_company():
    try:
        token = validate_token()
        
        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        company_data = request.json

        if 'name' not in company_data:
            return jsonify({'error': 'Name is needed in the request!'}), 400

        result = create_company(company_data, token)

        return jsonify({"id": result})
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    


@company.route('/companies/<company_id>', methods=['DELETE'])
def delete_company_route(company_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        try:
            delete_company(company_id, token)
            return jsonify({"companyId": company_id}), 200
        except Exception as err:
            if str(err) == "Company not found":
                return jsonify({"error": "Company not found"}), 404
            else:
                raise

    except Exception as err:
        error_message = str(err)
        return jsonify({"error": f"An error occurred: {error_message}"}), 500


@company.route('/companies/<company_id>', methods=['PATCH'])
def update_company_route(company_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        request_data = request.json

        if 'name' not in request_data:
            return jsonify({"error": "Name not found in the request"}), 400

        new_name = request_data['name']

        update_company(company_id, new_name, token)

        return jsonify({"companyId": company_id}), 200
    
    except Exception as e:
        error_message = str(e)
        if error_message == "Company not found":
            return jsonify({"error": error_message}), 404
        else:
            return jsonify({"error": f"An error occurred: {error_message}"}), 500
    except:
        return jsonify({'error': 'Something wrong happened when updating company!'}), 500



@company.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        company_data = get_company_by_id(company_id, token)
        return jsonify(company_data), 200

    except Exception as err:
        error_message = str(err)
        if error_message == "Company not found":
            return jsonify({"error": error_message}), 404
        return jsonify({'error': f'Error fetching company: {error_message}'}), 500


@company.route('/companies/', methods=['GET'])
def list_companies():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401

        companies = get_all_companies(token)
        return jsonify({"companies": companies}), 200

    except Exception as err:
        return jsonify({'error': f'Error in get companies: {str(err)}'}), 500
