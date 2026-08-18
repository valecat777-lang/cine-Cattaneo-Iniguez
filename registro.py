import tkinter as tk
from tkinter import messagebox
from sistema import Cliente, Administrador  # IMPORTANTE: Ahora importamos también Administrador

class VentanaRegistro:
    def __init__(self, root, sistema):
        #ventana secundaria para el registro de usuarios
        self.ventana = root
        self.ventana.title("Registro de Nuevo Usuario")
        self.ventana.geometry("300x420")
        self.sistema = sistema

        # Elementos de la interfaz para el registro
        tk.Label(self.ventana, text="Nombre:").pack(pady=2)
        self.entry_nombre = tk.Entry(self.ventana)
        self.entry_nombre.pack(pady=2)

        tk.Label(self.ventana, text="Apellido:").pack(pady=2)
        self.entry_apellido = tk.Entry(self.ventana)
        self.entry_apellido.pack(pady=2)

        tk.Label(self.ventana, text="DNI:").pack(pady=2)
        self.entry_dni = tk.Entry(self.ventana)
        self.entry_dni.pack(pady=2)

        tk.Label(self.ventana, text="Nombre de Usuario:").pack(pady=2)
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack(pady=2)

        tk.Label(self.ventana, text="Contraseña:").pack(pady=2)
        self.entry_contrasenia = tk.Entry(self.ventana, show="*")
        self.entry_contrasenia.pack(pady=2)

        #Selector de Tipo de Usuario ---
        tk.Label(self.ventana, text="Tipo de Cuenta:").pack(pady=2)
        
        # Variable para guardar la opción elegida (por defecto "cliente")
        self.tipo_var = tk.StringVar(value="cliente") 
        
        frame_radios = tk.Frame(self.ventana)
        frame_radios.pack(pady=2)
        
        tk.Radiobutton(frame_radios, text="Cliente", variable=self.tipo_var, value="cliente").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_radios, text="Administrador", variable=self.tipo_var, value="administrador").pack(side=tk.LEFT, padx=5)

        # Botón para confirmar el registro
        tk.Button(self.ventana, text="Registrarse", command=self.registrar).pack(pady=15)

    def registrar(self):
        #Obtener los textos escritos por el usuario
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        dni = self.entry_dni.get()
        usuario = self.entry_usuario.get()
        contrasenia = self.entry_contrasenia.get()

      #Leer qué tipo de cuenta seleccionó el usuario
        tipo_seleccionado = self.tipo_var.get()

        #Crear el objeto correspondiente (Administrador o Cliente)
        if tipo_seleccionado == "administrador":
            nuevo_usuario = Administrador(usuario, contrasenia, nombre, apellido, dni)
        else:
            nuevo_usuario = Cliente(usuario, contrasenia, nombre, apellido, dni)

        #Pedirle al sistema que lo valide y guarde en el JSON (funciona igual para ambos)
        exito, mensaje = self.sistema.registrar_usuario(nuevo_usuario)

        #Mostrar el resultado en pantalla
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.ventana.destroy()  # Cierra la ventana de registro tras el éxito
        else:
            messagebox.showerror("Error de Registro", mensaje)