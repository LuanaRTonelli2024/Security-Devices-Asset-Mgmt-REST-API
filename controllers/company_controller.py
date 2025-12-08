from flask import jsonify
from database.__init__ import database
import app_config as config
from models.company_model import Company

def create_company(company_data, token):
    try:
        # Apenas valida se o usuário está logado (token presente)
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        company = Company(name=company_data['name'])

        company_dict = {
            "name": company.name
        }

        company_ref = database.collection(config.CONST_COMPANY_COLLECTION).add(company_dict)

        return company_ref[1].id
    
    except Exception as err:
        print(f"Error creating company: {str(err)}")
        raise Exception("Error on creating company!")



def update_company(company_id, new_name, token):
    try:
        # Apenas valida se o usuário está logado (rota protegida)
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        company_ref = database.collection(config.CONST_COMPANY_COLLECTION).document(company_id)

        # Verifica se a empresa existe
        company_doc = company_ref.get()
        if not company_doc.exists:
            raise Exception("Company not found")

        # Atualiza o campo name
        company_ref.update({"name": new_name})

        return True

    except Exception as err:
        print(f"Error updating company: {str(err)}")
        raise Exception("Error on updating company!")



def delete_company(company_id, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        company_ref = database.collection(config.CONST_COMPANY_COLLECTION).document(company_id)

        company_doc = company_ref.get()
        if not company_doc.exists:
            raise Exception("Company not found")

        company_ref.delete()

        return True

    except Exception as err:
        print(f"Error deleting company: {str(err)}")
        raise Exception("Error on deleting company!")



def get_company_by_id(company_id, token):
    try:
        # Apenas valida se o usuário está logado (rota protegida)
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        company_ref = database.collection(config.CONST_COMPANY_COLLECTION).document(company_id)
        company_doc = company_ref.get()

        if not company_doc.exists:
            raise Exception("Company not found")

        data = company_doc.to_dict()
        data["_id"] = company_doc.id

        return data

    except Exception as err:
        print(f"Error fetching company by ID: {str(err)}")
        raise Exception("Error on fetching company by ID!")


def get_all_companies(token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        company_collection = database.collection(config.CONST_COMPANY_COLLECTION)
        companies = company_collection.stream()

        result = []
        for company in companies:
            data = company.to_dict()
            data["_id"] = company.id
            result.append(data)

        return result

    except Exception as e:
        print(f"Error fetching companies: {str(e)}")
        raise Exception("Error on fetching companies!")
