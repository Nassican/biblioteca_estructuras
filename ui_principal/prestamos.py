import os
import json

path_to_json = os.path.join(os.path.dirname(__file__), "../databases/prestamos.json")


class Libro:
    def __init__(self, isbn, titulo, autor, fecha):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.fecha = fecha
        self.sig = None


class Prestamo:
    def __init__(self, uuid, libros):
        self.uuid = uuid
        self.libros = libros
        self.sig = None


class Lista:
    def __init__(self):
        self.pri = None
        self.ult = None

    def ingresar_libro(self, isbn, titulo, autor, fecha):
        if self.pri is None:
            #print("Lista vacía, agregado al principio")
            self.pri = Libro(isbn, titulo, autor, fecha)
            self.ult = self.pri
        else:
            aux = self.pri
            while aux is not None:
                if aux.isbn == isbn:
                    print('Código ISBN repetido.')
                    return
                aux = aux.sig

            nuevo_nodo = Libro(isbn, titulo, autor, fecha)
            self.ult.sig = nuevo_nodo
            self.ult = nuevo_nodo

    def agregar_prestamo(self, uuid, libros):
        nuevo_prestamo = Prestamo(uuid, libros)
        if self.pri is None:
            self.pri = nuevo_prestamo
            self.ult = nuevo_prestamo
        else:
            aux = self.pri
            while aux.sig is not None:
                aux = aux.sig
            aux.sig = nuevo_prestamo
            self.ult = nuevo_prestamo

    def imprimir_prestamos(self):
        print("=================================== LISTA DE PRESTAMOS ===================================")
        print("")
        if self.pri is None:
            print("No hay préstamos para imprimir.")
            return

        aux = self.pri
        while aux is not None:
            print(f'UUID: {aux.uuid}, Libros:')
            for libro in aux.libros:
                print(f'  ISBN: {libro.isbn}, Título: {libro.titulo}, Autor: {libro.autor}, Fecha: {libro.fecha}')
            aux = aux.sig
        print("")

    def agregar_libros_desde_json(self, datos_libro):
        isbn = datos_libro.get("ISBN")
        titulo = datos_libro.get("Titulo")
        autor = datos_libro.get("Autor")
        fecha = datos_libro.get("Fecha")

        self.ingresar_libro(isbn, titulo, autor, fecha)

    def cargar_prestamos_desde_json(self):
        with open(path_to_json, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            prestamos_data = data.get("prestamos", [])

            for prestamo_data in prestamos_data:
                libros_prestamo = []
                for libro_data in prestamo_data.get("prestamos", []):
                    libro = Libro(libro_data["ISBN"], libro_data["Titulo"], libro_data["Autor"], libro_data["Fecha"])
                    libros_prestamo.append(libro)

                self.agregar_prestamo(prestamo_data["uuid"], libros_prestamo)

    def try_cargar_prestamos_desde_json(self):
        try:
            self.cargar_prestamos_desde_json()
        except FileNotFoundError:
            print("No se encontró el archivo de préstamos.")
        except Exception as e:
            print(f"El archivo de préstamos está vacío. {e}")

    def actualizar_prestamos_desde_json(self, path_to_json):
        self.pri = None
        self.ult = None
        self.cargar_prestamos_desde_json()


ListaPrestamos = Lista()
