import os
import requests
import time
import json
API_KEY = os.environ.get("ROBLOX_API_KEY")  # configura en Render
OWNER_ID = os.environ.get("ROBLOX_OWNER_ID")  # tu user id (o group id)
OWNER_TYPE = os.environ.get("ROBLOX_OWNER_TYPE", "User")  # "User" o "Group"
ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"
THUMBNAILS_URL = "https://thumbnails.roblox.com/v1/assets"

def wait_for_asset_id(operationid, timeout = 120):
    url = f"{ASSETS_URL}/operations/{operationid}"
    start = time.time()
    headers = {"x-api-key": API_KEY}
    while True:
        resp = requests.get(url, headers = headers)
        resp.raise_for_status()
        operation = resp.json()
        if operation.get("done"):
            if "response" in operation:
                return operation["response"]
            raise Exception(operation.get("error", "La operación falló."))
        if time.time() - start > timeout:
            raise TimeoutError("La operación tardó demasiado.")
        time.sleep(1)

def upload_asset_file(path, name, description, asset_type):
    headers = {"x-api-key": API_KEY}
    request = {
        "assetType": asset_type, 
        "displayName": name,
        "description": description,
        "creationContext" : {
            "creator" : {
                "userId" : str(OWNER_ID)
            }
        }
    }

    with open(path, "rb") as f:
        files = {
            "request" : (None, json.dumps(request), "application/json"),
            "fileContent" : (os.path.basename(path), f, "image/png")
        }
        resp = requests.post(ASSETS_URL, headers=headers, files=files, timeout=60)
    resp.raise_for_status()
    return wait_for_asset_id(resp.get("operationId"))
