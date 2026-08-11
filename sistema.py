# ACA ES DONDE VAN A IR LAS CLASES Y LA MAYORIA DE LA LOGICAAA, dsp hacemos unos import en "main.py" para que no quede
# super largo y complicado el codigo principal 

class Usuario:
    def __init__(self, usuario, contrasenia, nombre, apellido, dni):
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = "usuario"

    def menu(self):
        pass

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "contrasenia": self.contrasenia,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tipo": self.tipo
        }
    

class Administrador(Usuario):
    def __init__(self, usuario, contrasenia, nombre, apellido, dni):
        super().__init__(usuario, contrasenia, nombre, apellido, dni)
        self.tipo = "admin"
        
    def menu(self):
        print("Menu administrador")        


class Cliente(Usuario):
    def __init__(self, usuario, contrasenia, nombre, apellido, dni):
        super().__init__(usuario, contrasenia, nombre, apellido, dni)
        self.tipo = "cliente"
        
    def menu(self):
        print("Menu cliente")


class Funcion:
    def __init__(self, pelicula, sala, fecha, hora, precio, capacidad):
        self.pelicula = pelicula
        self.sala = sala
        self.fecha = fecha
        self.hora = hora
        self.precio = precio
        self.capacidad = capacidad
    
    def hay_lugares(self):
        return self.capacidad > 0
    
    def vender_entrada(self):
        if self.capacidad > 0:
            self.capacidad -= 1
            return True
        return False
    
    def to_dict(self):  #Este va a ser el metodo que cuando se cree un obj, lo va a convertir en un diccionario para json
        return {
            "pelicula": self.pelicula,
            "sala": self.sala,
            "fecha": self.fecha,
            "hora": self.hora,
            "precio": self.precio,
            "capacidad": self.capacidad
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

class Entrada:
    def __init__(self, id_entrada, cliente, funcion):
        self.id_entrada = id_entrada
        self.cliente = cliente
        self.pelicula = funcion.pelicula
        self.sala = funcion.sala
        self.fecha = funcion.fecha
        self.hora = funcion.hora
        self.precio = funcion.precio
    
    def to_dict(self):
        return {
            "id": self.id_entrada,
            "cliente": self.cliente.usuario,
            "pelicula": self.pelicula,
            "sala": self.sala,
            "fecha": self.fecha,
            "hora": self.hora,
            "precio": self.precio
        }
        
class Sistema:

    def __init__(self):
        self.usuarios = [] #lista vacía como atributo del objeto Sistema para guardar todos los usuarios
        self.funciones = [] #idem pero pa funciones
        self.entradas = [] #idem idem pero para guardar todas las compras :p
        self.usuario_actual = None #quien los quiere usar actualmente :p
    
    def existe_usuario(self, nombre_usuario): #validacion para que no se puedan registrar dos usuarios con el mismo nombre
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return True
        return False
        
    def registrar_usuario(self, usuario):
        if self.existe_usuario(usuario.usuario):
            return False
        self.usuarios.append(usuario)
        return True
  
    def iniciar_sesion(self, nombre_usuario, contrasenia):
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario and usuario.contrasenia == contrasenia:
                self.usuario_actual = usuario
                return usuario
        return None      