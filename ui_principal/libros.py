import os
import json

path_to_json = os.path.join(os.path.dirname(__file__), "../databases/libros_db.json")


class Libro:
    def __init__(self, titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis):
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.isbn = isbn
        self.año_public = año_public
        self.idioma = idioma
        self.ejemplares = ejemplares
        self.categoria = categoria
        self.sinopsis = sinopsis
        self.sig = None

class Lista:
    def __init__(self):
        self.pri = None
        self.ult = None

    def ingresar_libro(self, titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis):
        if self.pri == None:
            #print("Lista vacia, agregado de primero")
            self.pri = Libro(titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis)
            self.ult = self.pri
            return

        aux = self.pri
        while(aux != None):
            if aux.isbn == isbn:
                print('codigo ISBN repetido.')
                return
            aux = aux.sig

        nuevo_nodo = Libro(titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis)
        self.ult.sig = nuevo_nodo
        self.ult = nuevo_nodo

    def eliminar_libro(self, titulo):
        if self.pri == None:
            print("No hay libros para eliminar")
            return
        else:
            aux = self.pri
            while((aux != None) and (aux.titulo != titulo)):
                dato = aux
                aux = aux.sig
            if aux == None:
                print('El libro no existe')

            elif aux == self.pri:
                if self.pri == None:
                    print("No se puede eliminar el libro")
                    return
                print(f"Se elimina {self.pri.titulo}")
                self.pri = self.pri.sig

            elif aux == self.ult:
                if self.pri == None:
                    print("No se puede eliminar")
                    return
                print(f"Sale {self.ult.titulo}")
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
                    print('Catalogo vacio.')
            else:
                dato.sig = aux.sig

    def buscar_libro(self, titulo):
        if self.pri == None:
            print("No hay libros para buscar.")
            return

        aux = self.pri
        while(aux != None):
            if aux.titulo == titulo:
                print("Libro encontrado!")
                print(f'ISBN: {aux.isbn}, Titulo: {aux.titulo}, Autor: {aux.autor}, Editorial: {aux.editorial}')
            aux = aux.sig
        print("El libro no se encuentra.")

    def imprimir_libros(self):
        print("=================================== LISTA DE LIBROS ===================================")
        print("")
        if self.pri == None:
            print("No hay libros para imprimir.")
            return

        aux = self.pri
        while(aux != None):
            print(f'ISBN: {aux.isbn}, Titulo: {aux.titulo}, Autor: {aux.autor}, Editorial: {aux.editorial}, Ejemplares: {aux.ejemplares}')
            #print(f'ISBN: {aux.isbn}, Titulo: {aux.titulo}, Autor: {aux.autor}, Editorial: {aux.editorial}, Año de publicacion: {aux.año_public}, Idioma: {aux.idioma}, Ejemplares: {aux.ejemplares}, Categoria: {aux.categoria}, Sinopsis: {aux.sinopsis}')
            aux = aux.sig
        print("")

    def agregar_libros_desde_json(lista, datos_libro):
        titulo = datos_libro.get("Titulo")
        autor = datos_libro.get("Autor")
        editorial = datos_libro.get("Editorial")
        isbn = datos_libro.get("ISBN")
        año_public = datos_libro.get("Año de publicacion")
        idioma = datos_libro.get("Idioma")
        ejemplares = datos_libro.get("Ejemplares")
        categoria = datos_libro.get("Categoria")
        sinopsis = datos_libro.get("Sinopsis")

        lista.ingresar_libro(titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis)

    def cargar_libros_desde_json(lista):
        with open(path_to_json, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            libros_data = data.get("Libros", [])

            for libro_data in libros_data:
                lista.agregar_libros_desde_json(datos_libro=libro_data)

    def try_cargar_libros_desde_json(lista):
        try:
            lista.cargar_libros_desde_json()
        except FileNotFoundError:
            print("No se encontró el archivo de libros.")
        except Exception as e:
            print(f"El archivo de libros está vacío. {e}")
            
    def actualizar_libros_desde_json(self, path_to_json):
        self.pri = None
        self.ult = None
        self.cargar_libros_desde_json()
            

ListaLibros = Lista()

#   opcion = 1
#   while opcion != 6:
#       print("---------------------Menu---------------------")
#       print("1. Inicializar lista")
#       print("2. Agregar libro")
#       print("3. Buscar libro")
#       print("4. Imprimir catalogo")
#       print("5. Eliminar libro")
#       print("6. Salir")
#       opcion = int(input("Digite su opcion: "))
#   
#       match opcion:
#           case 1:
#               print("Inicializando lista")
#               lista = Lista()
#           case 2:
#               titulo = input("Digite el titulo: ")
#               autor = input("Digite el autor: ")
#               editorial = input("Digite la editorial: ")
#               isbn = input("Digite el codigo isbn: ")
#               año_public = input("Digite el año de publicacion: ")
#               idioma = input("Digite el idioma: ")
#               ejemplares = input("Digite el numero de ejemplares: ")
#               categoria = input("Digite la categoria: ")
#               sinopsis = input("Digite la sinopsis: ")
#               lista.ingresar_libro(titulo, autor, editorial, isbn, año_public, idioma, ejemplares, categoria, sinopsis)
#           case 3:
#               lista.imprimir_libros()
#               titulo = input("Digite el titulo del libro a buscar: ")
#               lista.buscar_libro(titulo)
#           case 4:
#               print("Catalogo de libros")
#               lista.imprimir_libros()
#           case 5:
#               lista.imprimir_libros()
#               titulo = input("Digite el titulo del libro a eliminar: ")
#               lista.eliminar_libro(titulo)
#           case 6:
#               print(f'Saliendo...')