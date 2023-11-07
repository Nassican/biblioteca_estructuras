import json
import os


path_to_json = os.path.join(os.path.dirname(__file__), "../databases/usuarios.json")
# Lee los datos de los usuarios desde el json

def cargar_base_de_datos():
  try:
    with open(path_to_json, "r", encoding="utf-8") as json_file:
      data = json.load(json_file)
      return data.get('usuarios', [])
  except FileNotFoundError:
    return []


def verificar_credenciales(username, password):
    usuarios = cargar_base_de_datos()
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario  # Usuario encontrado
    return None  # Usuario no encontrado