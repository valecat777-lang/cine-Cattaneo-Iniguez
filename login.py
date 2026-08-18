import tkinter as tk
from tkinter import messagebox
from sistema import Sistema
from registro import VentanaRegistro

class VentanaLogin:
    def __init__(self, root, sistema):
        self.root = root
        self.root.title("Cine - Iniciar Sesión")
        self.root.geometry("250x250")
        self.sistema = sistema

        # --- Elementos de la interfaz ---
        tk.Label(self.root, text="Nombre de Usuario:").pack(pady=10)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack(pady=10)
        self.entry_contrasenia = tk.Entry(self.root, show="*")
        self.entry_contrasenia.pack(pady=5)

        # Botones
        tk.Button(self.root, text="Ingresar", command=self.ingresar).pack(pady=10)
        tk.Button(self.root, text="Crear Cuenta", command=self.abrir_registro).pack(pady=5)

    def ingresar(self):
        usuario_texto = self.entry_usuario.get()
        contrasenia_texto = self.entry_contrasenia.get()

        # Le pedimos al sistema que verifique las credenciales
        usuario_logueado = self.sistema.iniciar_sesion(usuario_texto, contrasenia_texto)

        if usuario_logueado:
            messagebox.showinfo("Bienvenido", f"¡Hola, {usuario_logueado.nombre}!")
            # Aquí podrías destruir la ventana de login y abrir el menú principal del cine
            # self.root.destroy()
            # abrir_menu_principal() 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        # Abre una ventana secundaria (Toplevel) para que el usuario se registre
        ventana_secundaria = tk.Toplevel(self.root)
        VentanaRegistro(ventana_secundaria, self.sistema)

if __name__ == "__main__":
    # 1. Creamos el cerebro del programa y cargamos los JSON
    mi_sistema_cine = Sistema()
    mi_sistema_cine.cargar_datos()

    # 2. Creamos la ventana principal de tkinter
    root = tk.Tk()
    
    # 3. Conectamos la interfaz con el cerebro
    app = VentanaLogin(root, mi_sistema_cine)
    
    # 4. Arrancamos el loop gráfico
    root.mainloop()