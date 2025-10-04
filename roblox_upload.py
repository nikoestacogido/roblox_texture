import os
import requests

API_KEY = os.environ.get("API_KEY")  # configura en Render
OWNER_ID = os.environ.get("ROBLOX_OWNER_ID")  # tu user id (o group id)
OWNER_TYPE = os.environ.get("ROBLOX_OWNER_TYPE", "User")  # "User" o "Group"

UPLOAD_URL = "https://apis.roblox.com/assets/v1/upload"
ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"

def upload_asset_file(path, name, description, asset_type):
    if not API_KEY:
        raise RuntimeError("Falta API_KEY en variables de entorno")

    headers = {"x-api-key": API_KEY}

    # --- Paso 1: Subir archivo ---
    with open(path, "rb") as f:
        files = {"fileContent": (os.path.basename(path), f, "image/png")}
        upload_resp = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=60)
    print("UPLOAD STATUS:", upload_resp.status_code)
    print("UPLOAD TEXT:", upload_resp.text)
    upload_resp.raise_for_status()
    file_id = upload_resp.json()["id"]

    # --- Paso 2: Crear asset con el fileId ---
    data = {
        "assetType": asset_type, 
        "name": name,
        "description": description,
        "ownerId": OWNER_ID,
        "ownerType": OWNER_TYPE,
        "fileId": file_id
    }

    asset_resp = requests.post(ASSETS_URL, headers=headers, json=data, timeout=60)
    print("ASSET STATUS:", asset_resp.status_code)
    print("ASSET TEXT:", asset_resp.text)
    asset_resp.raise_for_status()

    return asset_resp.json()


def wait_for_asset_moderation(asset_id, timeout=300, poll_interval=5):

    #Polling simple usando la Thumbnails API para saber si el thumbnail está 'Completed' o 'Blocked'.
    #No es 100% infalible, pero suele servir para detectar si fue bloqueado.

    t0 = time.time()
    while time.time() - t0 < timeout:
        params = {
            "assetIds": str(asset_id),
            "returnPolicy": "PlaceHolder",
            "size": "420x420",
            "format": "Png",
            "isCircular": "false"
        }
        r = requests.get(THUMBNAILS_URL, params=params, timeout=20)
        if r.status_code == 200:
            data = r.json().get("data", [])
            if data:
                state = data[0].get("state")  # e.g. "Completed", "Blocked", "Pending"
                if state == "Completed":
                    return {"status": "ok", "state": state}
                if state == "Blocked":
                    return {"status": "blocked", "state": state}
        time.sleep(poll_interval)
    return {"status": "timeout"}




