import os
import json
import requests

API_KEY = os.environ.get("API_KEY")
OWNER_ID = os.environ.get("ROBLOX_OWNER_ID")
OWNER_TYPE = os.environ.get("ROBLOX_OWNER_TYPE", "User")

ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"
ASSET_OPERATION_URL = "https://apis.roblox.com/assets/v1/operations/"

def upload_asset_file(path, name, description, asset_type):
    if not API_KEY:
        raise RuntimeError("Falta API_KEY en variables de entorno")

    headers = {"x-api-key": API_KEY}

    # aseguramos OWNER_ID como int si se puede
    try:
        owner_id_int = int(OWNER_ID)
    except Exception:
        raise RuntimeError(f"ROBLOX_OWNER_ID no es un entero válido: {OWNER_ID}")

    # Construir creator correctamente
# Determinar tipo e ID de creador
    if OWNER_TYPE.lower() == "user":
        creator_type = "User"
    else:
        creator_type = "Group"

    request_payload = {
        "assetType": asset_type,
        "name": name,
        "displayName": name,
        "description": description,
        "creationContext": {
            "creator": {
                "userId": int(OWNER_ID)  # o groupId si OWNER_TYPE != "user"
            }
        }
    }
    
    print("DEBUG - request_payload:", json.dumps(request_payload))

    with open(path, "rb") as f:
        # enviar 'request' como campo de formulario, y el archivo en fileContent
        data = {"request": json.dumps(request_payload)}
        files = {"fileContent": (os.path.basename(path), f, "image/png")}
        resp = requests.post(ASSETS_URL, headers=headers, data=data, files=files, timeout=120)

    print("UPLOAD STATUS:", resp.status_code)
    print("UPLOAD TEXT:", resp.text)

    # si da error, devolvemos la info para debug (no solo raise)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        # raise con info para logs
        raise RuntimeError(f"Upload failed {resp.status_code}: {resp.text}")

    return resp.json()

def wait_for_assetid(operation_id, max_tries : int, interval : int):
    headers = {"x-api-key": API_KEY}

#SEGUIR ESTA FUNCION
