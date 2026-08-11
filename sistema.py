# ACA ES DONDE VAN A IR LAS CLASES Y LA MAYORIA DE LA LOGICAAA, dsp hacemos unos import en "main.py" para que no quede
# super largo y complicado el codigo principal 

class Usuario:
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        self.usuario = usuario
        self.contraseña = contraseña
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = "usuario"

    def menu(self):
        pass

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "contraseña": self.contraseña,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tipo": self.tipo
        }
    

class Administrador(Usuario):
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        super().__init__(usuario, contraseña, nombre, apellido, dni)
        self.tipo = "admin"
        
    def menu(self):
        print("Menu administrador")        


class Cliente(Usuario):
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        super().__init__(usuario, contraseña, nombre, apellido, dni)
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
            "funcion": self.funcion.to_dict(),
            "cliente": self.cliente.to_dict()
        }