# En este módulo se encuentran las clases y la lógica principal
# del sistema de gestión del cine

from hashlib import sha256  # para hashear las contraseñas


def hash_password(contrasenia):  # función para hashear la contraseña usando SHA-256
    return sha256(contrasenia.encode("utf-8")).hexdigest()


# USUARIOS:


class Usuario:
    def __init__(self, usuario, contrasenia, nombre, apellido, dni, tipo="usuario"):
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = tipo

    def menu(
        self,
    ):  # Método abstracto pensado para ser redefinido por las clases hijas.
        raise NotImplementedError

    def to_dict(
        self,
    ):  # Convierte el objeto Usuario en un diccionario para poder guardarlo en JSON.
        return {
            "usuario": self.usuario,
            "contrasenia": self.contrasenia,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tipo": self.tipo,
        }


class Administrador(Usuario):
    def __init__(self, usuario, contrasenia, nombre, apellido, dni):
        super().__init__(
            usuario, contrasenia, nombre, apellido, dni, tipo="administrador"
        )

    def menu(self):
        return "administrador"


class Cliente(Usuario):
    def __init__(self, usuario, contrasenia, nombre, apellido, dni):
        super().__init__(usuario, contrasenia, nombre, apellido, dni, tipo="cliente")

    def menu(self):
        return "cliente"


# FUNCIONES/PELIS DEL CINE:


class Funcion:
    def __init__(self, pelicula, sala, fecha, hora, precio, capacidad):
        self.pelicula = pelicula
        self.sala = sala
        self.fecha = fecha
        self.hora = hora
        self.precio = precio
        self.capacidad = capacidad

    def hay_lugares(self):  # Devuelve True si todavía quedan lugares disponibles.
        return self.capacidad > 0

    def vender_entrada(
        self,
    ):  # Reduce en uno la capacidad de la función y devuelve True si la venta pudo realizarse
        if self.capacidad > 0:
            self.capacidad -= 1
            return True
        return False

    def to_dict(
        self,
    ):  # Este va a ser el metodo que cuando se cree un obj, lo va a convertir en un diccionario para json
        return {
            "pelicula": self.pelicula,
            "sala": self.sala,
            "fecha": self.fecha,
            "hora": self.hora,
            "precio": self.precio,
            "capacidad": self.capacidad,
        }

    def mostrar(self):

        print(f"""
            Película: {self.pelicula}
            Sala: {self.sala}
            Fecha: {self.fecha}
            Hora: {self.hora}
            Precio: ${self.precio}
            Lugares: {self.capacidad}
            """)


# ENTRADAS:


class Entrada:
    def __init__(self, id_entrada, cliente, funcion):
        self.id_entrada = id_entrada
        self.cliente = cliente
        self.pelicula = funcion.pelicula
        self.sala = funcion.sala
        self.fecha = funcion.fecha
        self.hora = funcion.hora
        self.precio = funcion.precio

    def to_dict(self):  # convierte la entrada en diccionario para guardarla en json
        return {
            "id": self.id_entrada,
            "cliente": self.cliente.usuario,
            "pelicula": self.pelicula,
            "sala": self.sala,
            "fecha": self.fecha,
            "hora": self.hora,
            "precio": self.precio,
        }


# SISTEMA:


class Sistema:
    def __init__(self):
        self.usuarios = []  # lista vacía como atributo del objeto Sistema para guardar todos los usuarios
        self.funciones = []  # idem pero pa funciones
        self.entradas = []  # idem idem pero para guardar todas las compras :p
        self.usuario_actual = None  # quien los quiere usar actualmente :p, None by default pq no hay nadie logueado al principio duh ;p

    def existe_usuario(self, nombre_usuario):
    # Verifica si ya existe un usuario con ese nombre
        nombre_usuario = nombre_usuario.strip().lower()
        for usuario in self.usuarios:
            if usuario.usuario.lower() == nombre_usuario:
                return True
        return False

    def registrar_usuario(self, usuario):
        # Verifica que el nombre de usuario no esté repetido.
        if self.existe_usuario(usuario.usuario):
            return False, "El nombre de usuario ya existe."

        # Verifica datos obligatorios.
        if not usuario.usuario.strip():
            return False, "El usuario no puede estar vacío."

        if not usuario.contrasenia:
            return False, "La contraseña no puede estar vacía."

        if not usuario.nombre.strip():
            return False, "El nombre no puede estar vacío."

        if not usuario.apellido.strip():
            return False, "El apellido no puede estar vacío."

        dni = str(usuario.dni).strip()

        if not dni.isdigit():
            return False, "El DNI debe contener solamente números."

        if len(dni) < 8 or len(dni) < 7:
            return False, "El DNI debe tener 7 u 8 números."
        #El dni no puede estar repetido, si ya hay un usuario con ese dni, no se puede registrar otro
        for u in self.usuarios:
            if u.dni == dni:
                return False, "El DNI ya está registrado."
        

        # Guardamos el usuario con el nombre limpio.
        usuario.usuario = usuario.usuario.strip()

        # La contraseña se guarda hasheada.
        usuario.contrasenia = hash_password(usuario.contrasenia)

        self.usuarios.append(usuario)
        self.guardar_datos()

        return True, "Usuario registrado correctamente."

    def iniciar_sesion(
        self, nombre_usuario, contrasenia
    ):  # busca un usuario que coincida con el usuario y contraseña
        contrasenia_hash = hash_password(
            contrasenia
        )  # si existe, lo establece como usuario actual

        for usuario in self.usuarios:
            if (
                usuario.usuario.lower() == nombre_usuario.lower()
                and usuario.contrasenia == contrasenia_hash
            ):
                self.usuario_actual = usuario
                return usuario
        return None

    def cerrar_sesion(self):  # para cerrar la sesion del usuario actual
        self.usuario_actual = None

    def _validar_datos_funcion(self, pelicula, sala, fecha, hora, precio, capacidad):
        # Verifica que los textos obligatorios no estén vacíos.
        if not str(pelicula).strip():
            return False, "La película no puede estar vacía."

        if not str(sala).strip():
            return False, "La sala no puede estar vacía."

        if not str(fecha).strip():
            return False, "La fecha no puede estar vacía."

        if not str(hora).strip():
            return False, "La hora no puede estar vacía."

        # Verifica que precio sea numérico.
        try:
            precio = float(precio)
        except (ValueError, TypeError):
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor a 0."

        # Verifica que capacidad sea un número entero.
        try:
            capacidad = int(capacidad)
        except (ValueError, TypeError):
            return False, "La capacidad debe ser un número entero."

        if capacidad <= 0:
            return False, "La capacidad debe ser mayor a 0."

        return True, ""


    def agregar_funcion(self, funcion):
        # Verifica que el usuario actual sea un administrador antes de permitir agregar una función.
        if not isinstance(self.usuario_actual, Administrador):
            return False, "Solo los administradores pueden agregar funciones."
        valido, mensaje = self._validar_datos_funcion(
            funcion.pelicula,
            funcion.sala,
            funcion.fecha,
            funcion.hora,
            funcion.precio,
            funcion.capacidad
        )

        if not valido:
            return False, mensaje

        funcion.pelicula = funcion.pelicula.strip()
        funcion.sala = funcion.sala.strip()
        funcion.fecha = funcion.fecha.strip()
        funcion.hora = funcion.hora.strip()
        funcion.precio = float(funcion.precio)
        funcion.capacidad = int(funcion.capacidad)

        self.funciones.append(funcion)
        self.guardar_datos()

        return True, "Función agregada correctamente."

    def eliminar_funcion(self, indice):  # eliminar por indice
        #Verifica que el usuario actual sea un administrador antes de permitir eliminar una función.
        if not isinstance(self.usuario_actual, Administrador):
            return False, "Solo los administradores pueden eliminar funciones."
        if 0 <= indice < len(self.funciones):
            self.funciones.pop(indice)
            self.guardar_datos()

            return True, "Función eliminada correctamente."

        return False, "La función seleccionada no existe."

    def modificar_funcion(self, indice, pelicula, sala, fecha, hora, precio, capacidad):
        #Verifica que el usuario actual sea un administrador antes de permitir modificar una función.
        if not isinstance(self.usuario_actual, Administrador):
            return False, "Solo los administradores pueden modificar funciones."
        # Verifica que la función exista.
        if not (0 <= indice < len(self.funciones)):
            return False, "La función seleccionada no existe."

        valido, mensaje = self._validar_datos_funcion(
            pelicula,
            sala,
            fecha,
            hora,
            precio,
            capacidad
        )

        if not valido:
            return False, mensaje

        funcion = self.funciones[indice]

        funcion.pelicula = str(pelicula).strip()
        funcion.sala = str(sala).strip()
        funcion.fecha = str(fecha).strip()
        funcion.hora = str(hora).strip()
        funcion.precio = float(precio)
        funcion.capacidad = int(capacidad)

        self.guardar_datos()

        return True, "Función modificada correctamente."

    def buscar_funcion(
        self, pelicula
    ):  # busca funciones cuya película coincida parcial o totalmente con el texto ingresado
        texto = pelicula.strip().lower()
        resultados = []

        for funcion in self.funciones:
            if texto in funcion.pelicula.lower():
                resultados.append(funcion)
        return resultados

    def generar_id_entrada(self):     # Genera automáticamente el próximo ID de entrada.
        if not self.entradas:
            return 1

        return max(entrada.id_entrada for entrada in self.entradas) + 1

    def comprar_entrada(
        self, indice_funcion
    ):  # realiza la compra de una entrada para la función indicada
        if self.usuario_actual is None:  # solo los clientes logueados pueden comprar
            return False, None, "Debe iniciar sesión para comprar entradas."

        if not isinstance(
            self.usuario_actual, Cliente
        ):  # este valida que el usuario actual sea un cliente para poder comprar
            return False, None, "Solo los clientes pueden comprar entradas."

        if not (0 <= indice_funcion < len(self.funciones)):
            return False, None, "La función seleccionada no existe."

        funcion = self.funciones[indice_funcion]

        if not funcion.vender_entrada():  # este valida que haya lugar, si la capacidad es 0 entonces la funcion esta agotada por lo tannnnto no hay venta,
            return (
                False,
                None,
                "No hay entradas disponibles para la función seleccionada.",
            )  # si la capaxidad es mayor que 0 se descuenta 1 lugar

        id_entrada = self.generar_id_entrada()          # genera automáticamente el id de la entrada

        entrada = Entrada(id_entrada, self.usuario_actual, funcion)

        self.entradas.append(entrada)
        self.guardar_datos()

        return True, entrada, "Entrada comprada exitosamente."
    
    def entradas_del_usuario_actual(
        self,
    ):  # devuelve las entradas compradas por el usuario actualmente logueado
        if self.usuario_actual is None:
            return []

        entradas_usuario = []

        for entrada in self.entradas:
            if entrada.cliente.usuario == self.usuario_actual.usuario:
                entradas_usuario.append(entrada)

        return entradas_usuario

    # DATOS:

    def cargar_datos(self):  # carga los usuarios, funciones y entradas desde los archivos json
                             # sistema.py no abre directamente el .json, solo se encarga de la logica
        from datos import cargar_entradas, cargar_funciones, cargar_usuarios

        self.usuarios = cargar_usuarios()
        self.funciones = cargar_funciones()
        self.entradas = cargar_entradas(self.usuarios)

    def guardar_datos(self):
        from datos import guardar_entradas, guardar_funciones, guardar_usuarios

        guardar_usuarios(self.usuarios)
        guardar_funciones(self.funciones)
        guardar_entradas(self.entradas)
