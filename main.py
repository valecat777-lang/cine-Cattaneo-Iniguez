'''
IDEASSSSSSSSSS/cosas que pide el profe:

Login de administradores y clientes (Clase (padre) Usuarios, dsp otra clase Administrador que hereda de usuarios y otra clase Cliente que hereda de usuarios)
Los administradores administran funciones
Los clientes compran entradas
Interfaz gráfica (tkinter otra vez?)
Código organizado (duh)
Github y tests D:

'''

class Usuario:
    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña
    def menu(self):
        pass

class Administrador(Usuario):
    def __init__(self, usuario, contraseña):
        super().__init__(usuario, contraseña)
        # agregar atributos específicos para el administrador o nah? supomgo que si igual :(
   
    def menu(self):
        print("Menu administrador")        
    #def agregar_funcion(self):
    #def eliminar_funcion(self):
    #def modificar_funcion(self):
    #def eliminar_usuario(self):
    

class Cliente(Usuario):
    def __init__(self, usuario, contraseña, nombre, apellido, dni):
        super().__init__(usuario, contraseña)
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        # nu se, agregar mas atributos especificos del cliente?
    def menu(self):
        print("Menu cliente")
    #def comprar_entrada(self):
    #def cancelar_entrada(self):
    #def ver_funciones(self):
    
class Funcion:
    def __init__(self, pelicula, sala, fecha, hora, precio, capacidad):
        self.pelicula = pelicula
        self.sala = sala
        self.fecha = fecha
        self.hora = hora
        self.precio = precio
        self.capacidad = capacidad