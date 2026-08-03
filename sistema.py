# ACA ES DONDE VAN A IR LAS CLASES Y LA MAYORIA DE LA LOGICAAA, dsp hacemos unos import en "main.py" para que no quede
# super largo y complicado el codigo principal 

class Usuario:
    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña
        self.tipo = "usuarion"
    def menu(self):
        pass
    

class Administrador(Usuario):
    def __init__(self, usuario, contraseña):
        super().__init__(usuario, contraseña)
        self.tipo = "admin"
        # agregar atributos específicos para el administrador o nah? supomgo que si igual :(
    def menu(self):
        print("Menu administrador")        
    #def agregar_funcion(self):
    #def eliminar_funcion(self):
    #def modificar_funcion(self):


class Cliente(Usuario):
    def __init__(self, usuario, contraseña):
        super().__init__(usuario, contraseña)
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