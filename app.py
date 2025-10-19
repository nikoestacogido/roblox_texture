from PIL import Image
from datetime import datetime
import time
import os
from fastapi import FastAPI, Request
from roblox_upload import upload_asset_file, wait_for_assetid, geat_public_id

makers = {
    "aspire" : "test",
    "practice" : "test",
    "hoop" : "mantra",
    "swift" : "mantra"
    }

key = "none"

#Creating key
exact_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
key = f"_{exact_time}"

def create_shirt(model_name, badge_name, team_name, sponsor_name, patch_name, fabric_colour, pattern_name, pattern_colour, number, state, skin_name):
    #Loading
    maker_name = makers[model_name]

    img_fabric = Image.open(f"assets/fabrics/fabric_{fabric_colour}.png").convert("RGBA")
    img_model = Image.open(f"assets/makers/{maker_name}/{model_name}/{model_name}.png").convert("RGBA")
    img_model_top = Image.open(f"assets/makers/{maker_name}/{model_name}/{model_name}_top.png").convert("RGBA")
    img_model_arm_front = Image.open(f"assets/makers/{maker_name}/{model_name}/{model_name}_arm_front.png").convert("RGBA")
    img_model_arm_side = Image.open(f"assets/makers/{maker_name}/{model_name}/{model_name}_arm_side.png").convert("RGBA")
    img_model_arm_up = Image.open(f"assets/makers/{maker_name}/{model_name}/{model_name}_arm_up.png").convert("RGBA")
    img_badge = Image.open(f"assets/badges/{team_name}/badge_{badge_name}.png").convert("RGBA")
    img_sponsor = Image.open(f"assets/sponsors/{sponsor_name}.png").convert("RGBA")
    img_patch = Image.open(f"assets/patches/patch_{patch_name}.png").convert("RGBA")
    img_pattern = Image.open(f"assets/patterns/{pattern_name}/{pattern_colour}.png").convert("RGBA")
    img_number = Image.open(f"assets/numbers/{number}.png").convert("RGBA")
    img_state = Image.open(f"assets/states/{state}.png").convert("RGBA")
    img_skin = Image.open(f"assets/skins/{skin_name}.png").convert("RGBA")
    
    create_front(img_fabric , img_model , img_badge , img_sponsor , img_patch , img_pattern , img_state, img_skin)
    create_back(img_fabric, img_pattern, img_number, img_state)
    create_side(img_fabric, img_state)
    create_top(img_fabric, img_model_top, img_state)
    create_bottom(img_fabric, img_state)
    create_arm_front_back_inner(img_fabric, img_model_arm_front, img_skin, img_state)
    create_arm_outter_sides(img_fabric, img_model_arm_side, img_skin, img_state)
    create_arm_down(img_skin)
    create_arm_up(img_fabric, img_model_arm_up, img_state)

def create_front(fabric, model, badge, sponsor, patch, pattern, state, skin):
    face_front = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    #Resize
    badge = badge.resize((30, 30))
    patch = patch.resize((15, 15))
    sponsor = sponsor.resize((65, 65))
    skin = skin.resize((128, 128))
    
    #Layering
    face_front = Image.alpha_composite(face_front, skin) #Hacer agujeros de skins?
    face_front = Image.alpha_composite(face_front, fabric)
    face_front = Image.alpha_composite(face_front, pattern)
    face_front = Image.alpha_composite(face_front, model)
    
    #Badge, sponsor and patch position
    temp_canva = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    temp_canva.paste(badge, (17, 19), badge)
    temp_canva.paste(patch, (56, 38), patch)
    temp_canva.paste(sponsor, (32, 51), sponsor)
    face_front = Image.alpha_composite(face_front, temp_canva)
    
    #State layering
    face_front = Image.alpha_composite(face_front, state)
    
    #Render
    face_front.save("torso_front" + key + ".png")

def create_back(fabric, pattern, number, state):
    face_back = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    face_back = Image.alpha_composite(face_back, fabric)
    face_back = Image.alpha_composite(face_back, pattern)
    face_back = Image.alpha_composite(face_back, number)
    face_back = Image.alpha_composite(face_back, state)
    face_back.save("torso_back" + key + ".png")
    
def create_side(fabric, state):
    face_side = Image.new("RGBA", (64, 128), (0, 0, 0, 0))
    fabric = fabric.resize((64, 128))
    face_side = Image.alpha_composite(face_side, fabric)
    state = state.resize((64, 128))
    face_side = Image.alpha_composite(face_side, state)
    face_side.save("torso_left" + key + ".png")
    face_side.save("torso_right" + key + ".png")

def create_top(fabric, model, state):
    face_top = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    fabric = fabric.resize((128, 64))
    face_top = Image.alpha_composite(face_top, fabric)
    face_top = Image.alpha_composite(face_top, model)
    state = state.resize((128, 64))
    face_top = Image.alpha_composite(face_top, state)
    face_top.save("torso_top" + key + ".png")

def create_bottom(fabric, state):
    face_bottom = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    fabric = fabric.resize((128, 64))
    face_bottom = Image.alpha_composite(face_bottom, fabric)
    state = state.resize((128, 64))
    face_bottom = Image.alpha_composite(face_bottom, state)
    face_bottom.save("torso_bottom" + key + ".png")

def create_arm_front_back_inner(fabric, model_arm_front , skin, state):
    face_frontback = Image.new("RGBA", (64, 128), (0,0,0,0))
    face_frontback.alpha_composite(skin)
    fabric = fabric.resize((64, 32))
    face_frontback.alpha_composite(fabric)
    face_frontback.alpha_composite(model_arm_front)
    state = state.resize((64, 32))
    face_frontback.alpha_composite(state)
    face_frontback.save("leftright_arm_FBLR" + key + ".png")

def create_arm_outter_sides(fabric, model_arm_side, skin, state):
    face_outter = Image.new("RGBA", (64, 128), (0,0,0,0))
    face_outter.alpha_composite(skin)
    fabric = fabric.resize((64, 32))
    face_outter.alpha_composite(fabric)
    face_outter.alpha_composite(model_arm_side)
    state = state.resize((64, 32))
    face_outter.alpha_composite(state)
    face_outter.save("leftright_arm_outter" + key + ".png")

def create_arm_down(skin):
    face_down = Image.new("RGBA", (64, 64), (0,0,0,0))
    skin = skin.resize((64, 64))
    face_down.alpha_composite(skin)
    face_down.save("leftright_arm_down" + key + ".png")

def create_arm_up(fabric, model_arm_up, state):
    face_up = Image.new("RGBA", (64, 64), (0,0,0,0))
    fabric = fabric.resize((64, 64))
    face_up.alpha_composite(fabric)
    face_up.alpha_composite(model_arm_up)
    state = state.resize((64, 64))
    face_up.alpha_composite(state)
    face_up.save("leftright_arm_up" + key + ".png")

def get_images(key):
    #Guardar tuplas con su posicion
    images = []
    images_path = []
    images.append((Image.open("torso_front" + key + ".png").convert("RGBA"), (231, 74))) #image[0] -> obj img , image[1] -> tuple de posiciones (referenciar para acceder)
    images_path.append(os.path.abspath("torso_front" + key + ".png"))
    images.append((Image.open("torso_back" + key + ".png").convert("RGBA"), (427, 74)))
    images_path.append(os.path.abspath("torso_back" + key + ".png"))
    images.append((Image.open("torso_left" + key + ".png").convert("RGBA"), (361, 74)))
    images_path.append(os.path.abspath("torso_left" + key + ".png"))
    images.append((Image.open("torso_right" + key + ".png").convert("RGBA"), (165, 74)))
    images_path.append(os.path.abspath("torso_right" + key + ".png"))
    images.append((Image.open("torso_top" + key + ".png").convert("RGBA"), (231, 8))) 
    images_path.append(os.path.abspath("torso_top" + key + ".png"))
    images.append((Image.open("torso_bottom" + key + ".png").convert("RGBA"), (231, 204)))
    images_path.append(os.path.abspath("torso_bottom" + key + ".png"))
  
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (440, 355))) #left arm back
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (308, 355))) #left arm front
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (85, 355))) #right arm back
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (217, 355))) #right arm front
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (506, 355))) #left arm right side
    images.append((Image.open("leftright_arm_FBLR" + key + ".png").convert("RGBA"), (19, 355))) #right arm left side
    images_path.append(os.path.abspath("leftright_arm_FBLR" + key + ".png"))
    images.append((Image.open("leftright_arm_outter" + key + ".png").convert("RGBA"), (151, 355))) #right arm right side
    images.append((Image.open("leftright_arm_outter" + key + ".png").convert("RGBA"), (374, 355))) #left arm left side
    images_path.append(os.path.abspath("leftright_arm_outter" + key + ".png"))
    images.append((Image.open("leftright_arm_down" + key + ".png").convert("RGBA"), (217, 485))) #right arm down
    images.append((Image.open("leftright_arm_down" + key + ".png").convert("RGBA"), (308, 485))) #left arm down
    images_path.append(os.path.abspath("leftright_arm_down" + key + ".png"))
    images.append((Image.open("leftright_arm_up" + key + ".png").convert("RGBA"), (217, 289))) #right arm up
    images.append((Image.open("leftright_arm_up" + key + ".png").convert("RGBA"), (308, 289))) #left arm up
    images_path.append(os.path.abspath("leftright_arm_up" + key + ".png"))
    return images, images_path

def stick_in_template(temp_ref, images : list):
    template_face = Image.new("RGBA", (585, 559), (0,0,0,0))
    templates = {
        "shirt" : "assets/Template-Shirts-R15.png",
        "pants" : "assets/Template-Pants-R15.png"
        }
    
    template = Image.open(templates[temp_ref]).convert("RGBA")
    template_face.paste(template, (0, 0), template)
    
    for image in images:
        img = image[0]
        pos = image[1]
        template_face.paste(img, pos, img)
    
    template_face.save("full_temp" + key + ".png")

def clean_images(imgs_path):
    for image in imgs_path:
        os.remove(image)

#RECIBIR REQUESTS

server_app = FastAPI()

@server_app.post("/generate_shirt")
async def generate_shirt(request: Request):
    data = await request.json()
    print("Datos recibidos:", data)
    

    create_shirt(data.get("model_name"), data.get("badge_name") , data.get("team"), data.get("sponsor"), data.get("patch_name"), data.get("fabric_colour"), data.get("pattern"), data.get("pattern_colour"), data.get("number") , data.get("state"), data.get("skin"))
    time.sleep(5)
    imgs , imgs_path = get_images(key)
    stick_in_template("shirt", imgs)

    #SUBIR A ROBLOX
    path = os.path.abspath("full_temp" + key + ".png")
    incoming_json = upload_asset_file(path, name = "aurelionshirt" + key, description = "gran esfuerzo", asset_type = "Decal")
    operation_id = incoming_json.get("operationId")
    done = incoming_json.get("done")
    #Funcion de esperar el assetid con el operation id

    internal_asset_id = wait_for_assetid(operation_id, 20, 5)
    catalog_response = geat_public_id("aurelionshirt" + key)
    print(catalog_response)
    
    return {"status": "ok", "asset_id": 9090} #DEVOLVER EL ID del asset
    time.sleep(3)
    clean_images(imgs_path)







