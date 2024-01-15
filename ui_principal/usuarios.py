import os
import json

path_to_json = os.path.join(os.path.dirname(__file__), "../databases/usuarios.json")

class Usuario:
    def __init__(self, identificacion, username, nombre, celular, password, rol="usuario"):
        self.identificacion = identificacion
        self.username = username
        self.nombre = nombre
        self.celular = celular
        self.password = password
        self.rol = rol
        self.sig = None


class Lista:
    def __init__(self):
        self.pri = None
        self.ult = None

    def ingresar_ususario(self, identificacion, username, nombre, celular, password, rol):
        if self.pri == None:
            #print("Lista vacia, agregado de primero")
            self.pri = Usuario(identificacion, username,
                               nombre, celular, password, rol)
            self.ult = self.pri
            return

        aux = self.pri
        while (aux != None):
            if aux.identificacion == identificacion:
                print('identificacion repetida.')
                return
            aux = aux.sig

        nuevo_nodo = Usuario(identificacion, username,
                             nombre, celular, password, rol)
        self.ult.sig = nuevo_nodo
        self.ult = nuevo_nodo

    def eliminar_usuario(self, identificacion):
        if self.pri == None:
            print("No hay datos para eliminar")
            return
        else:
            aux = self.pri
            while ((aux != None) and (aux.identificacion != identificacion)):
                dato = aux
                aux = aux.sig
            if aux == None:
                print('Nodo no existe')

            elif aux == self.pri:
                if self.pri == None:
                    print("No se puede sacar")
                    return
                print(f"Sale {self.pri.nombre}")
                self.pri = self.pri.sig

            elif aux == self.ult:
                if self.pri == None:
                    print("No se puede sacar")
                    return
                print(f"Sale {self.ult.nombre}")
                aux = self.pri
                if aux != self.ult:
                    while aux != self.ult:
                        dato = aux
                        aux = aux.sig
                    self.ult = dato
                    self.ult.sig = None
                else:
                    self.pri = None
                    self.ult = None
                    print('Lista vacia.')
            else:
                dato.sig = aux.sig

    def buscar_usuario(self, identificacion):
        if self.pri == None:
            print("No hay datos para buscar.")
            return

        aux = self.pri
        while (aux != None):
            if aux.identificacion == identificacion:
                print("Usuario encontrado!")
                print(
                    f'Identificacion: {aux.identificacion}, Nombre: {aux.nombre}')
            aux = aux.sig

    def imprimir_usuarios(self):
        print("=================================== LISTA DE USUARIOS ===================================")
        print("")
        if self.pri == None:
            print("No hay datos para imprimir.")
            return
        aux = self.pri
        while (aux != None):
            print(
                f'Identificacion: {aux.identificacion}, Nombre: {aux.nombre}, rol: {aux.rol} ')
            aux = aux.sig
        print("")

    def agregar_usuario_desde_json(lista, datos_usuario):
        identificacion = datos_usuario.get("id_personal")
        username = datos_usuario.get("username")
        nombre = datos_usuario.get("nombre")
        celular = datos_usuario.get("cellphone")
        password = datos_usuario.get("password")
        rol = datos_usuario.get("rol", "usuario")  # Por defecto, el rol es "usuario"
    
        lista.ingresar_ususario(identificacion, username, nombre, celular, password, rol)

    def cargar_usuarios_desde_json(lista):
      with open(path_to_json, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        usuarios_data = data.get("usuarios", [])

        for usuario_data in usuarios_data:
          lista.agregar_usuario_desde_json(datos_usuario=usuario_data)

    def try_cargar_usuarios_desde_json(lista):
      try:
        lista.cargar_usuarios_desde_json()
        print("Usuarios cargados desde el archivo.")
      except FileNotFoundError:
        print("No se encontró el archivo de usuarios.")
      except Exception as error:
        print(f"Error al cargar los usuarios: {error}")

    def actualizar_usuarios(self):
        self.pri = None
        self.ult = None
        self.cargar_usuarios_desde_json()


ListaUsuarios = Lista()

#opcion = 1
#while opcion != 7:
#    print("---------------------Menu---------------------")
#    print("1. Inicializar lista")
#    print("2. Agregar Usuario")
#    print("3. Buscar Usuario")
#    print("4. Imprimir Lista")
#    print("5. Eliminar Usuario")
#    print("6. Cargar datos del json")
#    print("7. Salir")
#    opcion = int(input("Digite su opcion: "))
#
#    match opcion:
#        case 1:
#            print("Inicializando lista")
#            lista = Lista()
#        case 2:
#            identificacion = int(input("Digite la identificacion: "))
#            username = input("Digite el username: ")
#            nombre = input("Digite el nombre: ")
#            celular = input("Digite el celular: ")
#            password = input("Digite la contraseña: ")
#            rol = "usuario"
#            lista.ingresar_ususario(
#                identificacion, username, nombre, celular, password, rol)
#        case 3:
#            lista.imprimir_usuarios()
#            identificacion = int(
#                input("Digite la identificacion del ususario a buscar: "))
#            lista.buscar_usuario(identificacion)
#        case 4:
#            print("Lista de usuarios")
#            lista.imprimir_usuarios()
#        case 5:
#            lista.imprimir_usuarios()
#            identificacion = int(
#                input("Digite la identificacion del usuario a eliminar: "))
#            lista.eliminar_usuario(identificacion)
#        case 6:
#            lista.try_cargar_usuarios_desde_json()
#            lista.imprimir_usuarios()
#        case 7:
#            print(f'Saliendo...')
#