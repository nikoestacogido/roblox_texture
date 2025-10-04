import os
import requests
import time

API_KEY = os.environ.get("API_KEY")  # configura en Render
OWNER_ID = os.environ.get("ROBLOX_OWNER_ID")  # tu user id (o group id)
OWNER_TYPE = os.environ.get("ROBLOX_OWNER_TYPE", "User")  # "User" o "Group"

ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"
THUMBNAILS_URL = "https://thumbnails.roblox.com/v1/assets"

def upload_asset_file(path, name, description, asset_type):

    #Sube el archivo 'path' a la Open Cloud Assets API.
    #Retorna el JSON devuelto por Roblox (imprimilo para ver el assetId exacto).

    if not API_KEY:
        raise RuntimeError("Falta ROBLOX_API_KEY en variables de entorno")

    headers = {"x-api-key": API_KEY}
    data = {
        "assetType": asset_type, 
        "name": name,
        "description": description,
        "ownerId": OWNER_ID,
        "ownerType": OWNER_TYPE,
    }

    with open(path, "rb") as f:
        files = {"fileContent": (os.path.basename(path), f, "image/png")}
        resp = requests.post(ASSETS_URL, headers=headers, data=data, files=files, timeout=60)
    resp.raise_for_status()
    return resp.json()

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

