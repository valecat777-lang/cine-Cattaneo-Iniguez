import tkinter as tk
from tkinter import messagebox

from sistema import Administrador, Cliente


class VentanaRegistro:
    FONDO = "#10121b"
    TARJETA = "#1b1f2d"
    CAMPO = "#292e3f"
    TEXTO = "#f7f7fb"
    TEXTO_SUAVE = "#aeb6ca"
    ROJO = "#e5394f"
    ROJO_ACTIVO = "#c92d41"

    def __init__(self, root, sistema):
        self.ventana = root
        self.sistema = sistema
        self.ventana.title("Tu cine de confianza | Crear cuenta")
        self.ventana.geometry("500x710")
        self.ventana.minsize(450, 650)
        self.ventana.configure(bg=self.FONDO)
        self.ventana.transient(self.ventana.master)
        self.ventana.grab_set()
        self._crear_interfaz()
        self.entry_nombre.focus_set()

    def _crear_interfaz(self):
        contenedor = tk.Frame(self.ventana, bg=self.FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=38, pady=28)

        tk.Label(contenedor, text="Tu cine de confianza", font=("Arial", 22, "bold"), fg=self.ROJO, bg=self.FONDO).pack()
        tk.Label(contenedor, text="CREÁ TU CUENTA Y VIVÍ EL CINE", font=("Arial", 9, "bold"), fg=self.TEXTO_SUAVE, bg=self.FONDO).pack(pady=(2, 18))

        tarjeta = tk.Frame(contenedor, bg=self.TARJETA, padx=28, pady=22)
        tarjeta.pack(fill=tk.BOTH, expand=True)
        tk.Label(tarjeta, text="Unite a Tu cine de confianza", font=("Arial", 17, "bold"), fg=self.TEXTO, bg=self.TARJETA).pack(anchor="w")
        tk.Label(tarjeta, text="Completá tus datos para comenzar.", font=("Arial", 10), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(anchor="w", pady=(4, 13))

        self.entry_nombre = self._crear_campo(tarjeta, "NOMBRE")
        self.entry_apellido = self._crear_campo(tarjeta, "APELLIDO")
        self.entry_dni = self._crear_campo(tarjeta, "DNI")
        self.entry_usuario = self._crear_campo(tarjeta, "USUARIO")
        self.entry_contrasenia = self._crear_campo(tarjeta, "CONTRASEÑA", ocultar=True)

        

        tk.Button(tarjeta, text="CREAR CUENTA", command=self.registrar, bg=self.ROJO, activebackground=self.ROJO_ACTIVO, fg="white", activeforeground="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", pady=10).pack(fill=tk.X, pady=(19, 0))

    def _crear_campo(self, parent, etiqueta, ocultar=False):
        tk.Label(parent, text=etiqueta, font=("Arial", 9, "bold"), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(anchor="w", pady=(8, 4))
        campo = tk.Entry(parent, show="•" if ocultar else "", bg=self.CAMPO, fg=self.TEXTO, insertbackground=self.TEXTO, relief="flat", font=("Arial", 11))
        campo.pack(fill=tk.X, ipady=7)
        return campo

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        dni = self.entry_dni.get()
        usuario = self.entry_usuario.get()
        contrasenia = self.entry_contrasenia.get()

        #Todos los registros nuevos corresponden a clientes.
        nuevo_usuario = Cliente(usuario, contrasenia, nombre, apellido, dni)

        #Pedirle al sistema que lo valide y guarde en el JSON (funciona igual para ambos)
        exito, mensaje = self.sistema.registrar_usuario(nuevo_usuario)

        #Mostrar el resultado en pantalla
        if exito:
            messagebox.showinfo("Registro exitoso", mensaje)
            self.ventana.destroy()  # Cierra la ventana de registro tras el éxito
        else:
            messagebox.showerror("Error de Registro", mensaje)
