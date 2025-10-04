import os
import json
import requests

API_KEY = os.environ.get("API_KEY")
OWNER_ID = os.environ.get("ROBLOX_OWNER_ID")
OWNER_TYPE = os.environ.get("ROBLOX_OWNER_TYPE", "User")

ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"

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
        "creatorTargetId": int(OWNER_ID),
        "creatorType": creator_type
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











