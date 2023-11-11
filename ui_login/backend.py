import json
import os
import uuid
import requests


path_to_json = os.path.join(os.path.dirname(__file__), "../databases/usuarios.json")
# Lee los datos de los usuarios desde el json

def cargar_base_de_datos():
  try:
    with open(path_to_json, "r", encoding="utf-8") as json_file:
      data = json.load(json_file)
      return data.get('usuarios', [])
  except FileNotFoundError:
    return []

def actualizar_base_de_datos(usuarios):
    with open(path_to_json, "w", encoding="utf-8") as json_file:
      json.dump({"usuarios": usuarios}, json_file, indent=2)


def verificar_credenciales(username, password):
    usuarios = cargar_base_de_datos()
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario  # Usuario encontrado
    return None  # Usuario no encontrado

def usuario_esta_disponible(username):
    usuarios = cargar_base_de_datos()
    existing_usernames = [user["username"] for user in usuarios]
    return username not in existing_usernames

def id_personal_esta_disponible(id_personal):
    usuarios = cargar_base_de_datos()
    for usuario in usuarios:
      if usuario["id_personal"] == id_personal:
        return False # Ya existe un usuario con ese id_personal
    return True # No existe un usuario con ese id_personal

def generate_uuid():
    return str(uuid.uuid4())

def register_user_in_database(new_user):
    usuarios = cargar_base_de_datos()
    usuarios.append(new_user)
    actualizar_base_de_datos(usuarios)
    
def obtener_json(api_url):
    try:
      response = requests.get(api_url)
      response.raise_for_status()  # Lanza una excepción si la respuesta indica un error HTTP

      json_data = response.json()
      print(json_data)
      return json_data
    except requests.exceptions.RequestException as e:
      print(f"Error al hacer la solicitud a la API: {e}")
      return None