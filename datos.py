#leer/escribir los json + contraseñas (hay que averiguar si conviene hashearlas y como se hace tal cosaaaa :p)
import json
import os  # permite comprobar si un archivo existe

#from sistema import Administrador, Cliente, Entrada, Funcion

# Archivos donde se guardan los datos.
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_FUNCIONES = "funciones.json"
ARCHIVO_COMPRAS = "compras.json"


# FUNCIONES GENERALES PARA JSON

def leer_json(nombre_archivo):
    # si el archivo no existe, devuelve una lista vacía.
    if not os.path.exists(nombre_archivo):
        return []

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            # verif que el contenido sea una lista:
            if isinstance(datos, list):
                return datos
            return []

    except (json.JSONDecodeError, OSError):   # si hay un error al leer el archivo, devuelve una lista vacía
        return []


def escribir_json(nombre_archivo, datos): # Guarda los datos en el archivo json
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        return True

    except OSError:
        return False


# USUARIOS:

def cargar_usuarios():  # funcion que carga los usuarios guardados en usuarios.json
    from sistema import Administrador, Cliente          # Importación local
    datos = leer_json(ARCHIVO_USUARIOS)
    usuarios = []

    for datos_usuario in datos:
        try:
            tipo = datos_usuario.get("tipo", "cliente")

            if tipo == "administrador":
                usuario = Administrador(
                    datos_usuario["usuario"],
                    datos_usuario["contrasenia"],
                    datos_usuario["nombre"],
                    datos_usuario["apellido"],
                    datos_usuario["dni"]
                )

            else:
                usuario = Cliente(
                    datos_usuario["usuario"],
                    datos_usuario["contrasenia"],
                    datos_usuario["nombre"],
                    datos_usuario["apellido"],
                    datos_usuario["dni"]
                )

            usuarios.append(usuario)

        except (KeyError, TypeError): # si faltan datos de un usuario, se ignora ese registro
            continue
    return usuarios


def guardar_usuarios(usuarios): # convierte los usuarios a diccionarios y los guarda en json
    datos = []

    for usuario in usuarios:
        datos.append(usuario.to_dict())
    return escribir_json(ARCHIVO_USUARIOS, datos)


# MOVIES DEL CINE:

def cargar_funciones():            # Carga las funciones guardadas en funciones.json
    from sistema import Funcion     # Importación local
    datos = leer_json(ARCHIVO_FUNCIONES)
    funciones = []

    for datos_funcion in datos:
        try:
            funcion = Funcion(
                datos_funcion["pelicula"],
                datos_funcion["sala"],
                datos_funcion["fecha"],
                datos_funcion["hora"],
                float(datos_funcion["precio"]),
                int(datos_funcion["capacidad"])
            )
            funciones.append(funcion)

        except (KeyError, TypeError, ValueError):
            # Si faltan datos o hay valores incorrectos,
            # se ignora esa función.
            continue
    return funciones


def guardar_funciones(funciones):     # Convierte las funciones a diccionarios y las guarda en json
    datos = []

    for funcion in funciones:
        datos.append(funcion.to_dict())
    return escribir_json(ARCHIVO_FUNCIONES, datos)


# COMPRAS / ENTRADAS:

def cargar_entradas(usuarios):
    # Carga las entradas guardadas en compras.json:
    from sistema import Entrada          # Importación local
    datos = leer_json(ARCHIVO_COMPRAS)
    entradas = []

    # Permite encontrar un usuario rápidamente por su nombre:
    usuarios_por_nombre = {}

    for usuario in usuarios:
        usuarios_por_nombre[usuario.usuario.lower()] = usuario

    for datos_entrada in datos:
        try:
            nombre_cliente = datos_entrada["cliente"].lower()

            # Busca al cliente correspondiente:
            cliente = usuarios_por_nombre.get(nombre_cliente)

            # Si el cliente no existe, no se carga la entrada:
            if cliente is None:
                continue

            # Crea una entrada con los datos guardados:
            entrada = Entrada.__new__(Entrada)

            entrada.id_entrada = int(datos_entrada["id"])
            entrada.cliente = cliente
            entrada.pelicula = datos_entrada["pelicula"]
            entrada.sala = datos_entrada["sala"]
            entrada.fecha = datos_entrada["fecha"]
            entrada.hora = datos_entrada["hora"]
            entrada.precio = float(datos_entrada["precio"])

            entradas.append(entrada)

        except (KeyError, TypeError, ValueError):
            # Si faltan datos o hay valores incorrectos: se ignora esa entrada
            continue

    return entradas


def guardar_entradas(entradas):
    # Convierte las entradas a diccionarios y las guarda en json
    datos = []

    for entrada in entradas:
        datos.append(entrada.to_dict())

    return escribir_json(ARCHIVO_COMPRAS, datos)


