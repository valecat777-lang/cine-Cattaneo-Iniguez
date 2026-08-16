# En este módulo se encuentran las clases y la lógica principal
# del sistema de gestión del cine 

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


class Cliente(Usuario):
    def __init__(self, usuario, contraseña):
        super().__init__(usuario, contraseña)
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
        self.usuario_actual = None #quien los quiere usar actualmente :p, None by default pq no hay nadie logueado al principio duh ;p
    
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
    
    def agregar_funcion(self, funcion):
        self.funciones.append(funcion)
    
    def eliminar_funcion(self, indice): #eliminar por indice
        if 0 <= indice < len(self.funciones):
            self.funciones.pop(indice)
            return True
        return False
    
    def modificar_funcion(self, indice, pelicula, sala, fecha, hora, precio, capacidad): #tmb por indice
        if 0 <= indice < len(self.funciones):
            funcion = self.funciones[indice]
            funcion.pelicula = pelicula
            funcion.sala = sala
            funcion.fecha = fecha
            funcion.hora = hora
            funcion.precio = precio
            funcion.capacidad = capacidad
            return True
        return False
    
    def buscar_funcion(self, pelicula):
        resultados = []
        for funcion in self.funciones:
            if pelicula.lower() in funcion.pelicula.lower():
                resultados.append(funcion)
        return resultados
    
    def comprar_entrada(self, funcion):
        if self.usuario_actual is None: #validacionnn si no hay usuario actualmente logueado, no se puede comprar entrada
            return False

        if not isinstance(self.usuario_actual, Cliente):  #este valida que el usuario actual sea un cliente para poder comprar
            return False

        if not funcion.vender_entrada():  #este valida que haya lugar, si la capacidad es 0 entonces la funcion esta agotada por lo tannnnto no hay venta, 
            return False                  #si la capaxidad es mayor que 0 se descuenta 1 lugar

        id_entrada = len(self.entradas) + 1

        entrada = Entrada(id_entrada, self.usuario_actual, funcion)

        self.entradas.append(entrada)

        return True