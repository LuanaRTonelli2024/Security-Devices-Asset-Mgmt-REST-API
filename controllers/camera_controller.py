from flask import jsonify
from database.__init__ import database
import app_config as config
from models.camera_model import Camera

def create_camera(camera_data, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")
        
        if "companyId" not in camera_data or not camera_data["companyId"]:
            raise Exception("companyId is required and cannot be empty")
        if "name" not in camera_data or not camera_data["name"]:
            raise Exception("name is required and cannot be empty")



        camera = Camera(
            companyId=camera_data['companyId'],
            name=camera_data['name'],
            location=camera_data['location'],
            ipAddress=camera_data['ipAddress'],
            userName=camera_data['userName'],
            password=camera_data.get('password', ""),
            subnetMask=camera_data.get('subnetMask', ""),
            defaultGateway=camera_data.get('defaultGateway', "")
        )

        camera_dict = {
            "companyId": camera.companyId,
            "name": camera.name,
            "location": camera.location,
            "ipAddress": camera.ipAddress,
            "userName": camera.userName,
            "password": camera.password,
            "subnetMask": camera.subnetMask,
            "defaultGateway": camera.defaultGateway
        }

        camera_ref = database.collection(config.CONST_CAMERA_COLLECTION).add(camera_dict)
        return camera_ref[1].id

    except Exception as err:
        print(f"Error creating camera: {str(err)}")
        raise Exception("Error on creating camera!")


def update_camera(camera_id, new_data, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        camera_ref = database.collection(config.CONST_CAMERA_COLLECTION).document(camera_id)
        camera_doc = camera_ref.get()
        if not camera_doc.exists:
            raise Exception("Camera not found")
        
        if "companyId" in new_data:
            del new_data["companyId"]
        if "_id" in new_data:
            del new_data["_id"]

        if "name" in new_data and not new_data["name"]:
            raise Exception("name cannot be empty")

        camera_ref.update(new_data)
        return True

    except Exception as err:
        print(f"Error updating camera: {str(err)}")
        raise Exception("Error on updating camera!")


def delete_camera(camera_id, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        camera_ref = database.collection(config.CONST_CAMERA_COLLECTION).document(camera_id)
        camera_doc = camera_ref.get()
        if not camera_doc.exists:
            raise Exception("Camera not found")

        camera_ref.delete()
        return True

    except Exception as err:
        print(f"Error deleting camera: {str(err)}")
        raise Exception("Error on deleting camera!")


def get_camera_by_id(camera_id, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        camera_ref = database.collection(config.CONST_CAMERA_COLLECTION).document(camera_id)
        camera_doc = camera_ref.get()

        if not camera_doc.exists:
            raise Exception("Camera not found")

        data = camera_doc.to_dict()
        data["_id"] = camera_doc.id
        return data

    except Exception as err:
        print(f"Error fetching camera by ID: {str(err)}")
        raise Exception("Error on fetching camera by ID!")


def get_all_cameras(token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        camera_collection = database.collection(config.CONST_CAMERA_COLLECTION)
        cameras = camera_collection.stream()

        result = []
        for camera in cameras:
            data = camera.to_dict()
            data["_id"] = camera.id
            result.append(data)

        return result

    except Exception as e:
        print(f"Error fetching cameras: {str(e)}")
        raise Exception("Error on fetching cameras!")
    

def get_cameras_by_company(company_id, token):
    try:
        if not token or "uid" not in token:
            raise Exception("User not authenticated!")

        camera_collection = database.collection(config.CONST_CAMERA_COLLECTION)
        cameras = camera_collection.where("companyId", "==", company_id).stream()

        result = []
        for camera in cameras:
            data = camera.to_dict()
            data["_id"] = camera.id
            result.append(data)

        if not result:
            raise Exception("No cameras found for this company")

        return result

    except Exception as err:
        print(f"Error fetching cameras by company: {str(err)}")
        raise Exception("Error on fetching cameras by company!")