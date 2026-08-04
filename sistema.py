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
    

class Administrador(Usuario):
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        super().__init__(usuario, contraseña, nombre, apellido, dni)
        self.tipo = "admin"
        # agregar atributos específicos para el administrador o nah? supomgo que si igual :(
    def menu(self):
        print("Menu administrador")        
    #def agregar_funcion(self):
    #def eliminar_funcion(self):
    #def modificar_funcion(self):


class Cliente(Usuario):
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        super().__init__(usuario, contraseña, nombre, apellido, dni)
        self.tipo = "cliente"
        # nu se, agregar mas atributos especificos del cliente?
    def menu(self):
        print("Menu cliente")
    #def comprar_entrada(self):
    

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