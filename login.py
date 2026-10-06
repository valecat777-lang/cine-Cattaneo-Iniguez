import tkinter as tk
from tkinter import messagebox

from registro import VentanaRegistro
from sistema import Sistema


class VentanaLogin:
    FONDO = "#10121b"
    TARJETA = "#1b1f2d"
    CAMPO = "#292e3f"
    TEXTO = "#f7f7fb"
    TEXTO_SUAVE = "#aeb6ca"
    ROJO = "#e5394f"
    ROJO_ACTIVO = "#c92d41"

    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("Bienvenido | Iniciar sesión")
        self.root.geometry("460x590")
        self.root.minsize(420, 540)
        self.root.configure(bg=self.FONDO)

        self._crear_interfaz()
        self.entry_usuario.focus_set()
        self.root.bind("<Return>", lambda evento: self.ingresar())

    def _crear_interfaz(self):
        contenedor = tk.Frame(self.root, bg=self.FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=38, pady=34)

        tk.Label(contenedor, text="Cinemer-K", font=("Arial", 25, "bold"), fg=self.ROJO, bg=self.FONDO).pack()
        tk.Label(contenedor, text="TU PRÓXIMA FUNCIÓN EMPIEZA ACÁ", font=("Arial", 9, "bold"), fg=self.TEXTO_SUAVE, bg=self.FONDO).pack(pady=(2, 22))

        tarjeta = tk.Frame(contenedor, bg=self.TARJETA, padx=28, pady=26)
        tarjeta.pack(fill=tk.X)
        tk.Label(tarjeta, text="¡Bienvenido!", font=("Arial", 17, "bold"), fg=self.TEXTO, bg=self.TARJETA).pack(anchor="w")
        tk.Label(tarjeta, text="Ingresá para ver la cartelera y gestionar tus entradas.", font=("Arial", 10), fg=self.TEXTO_SUAVE, bg=self.TARJETA, wraplength=330, justify="left").pack(anchor="w", pady=(5, 20))

        self.entry_usuario = self._crear_campo(tarjeta, "USUARIO")
        self.entry_contrasenia = self._crear_campo(tarjeta, "CONTRASEÑA", ocultar=True)

        tk.Button(tarjeta, text="INGRESAR", command=self.ingresar, bg=self.ROJO, activebackground=self.ROJO_ACTIVO, fg="white", activeforeground="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", pady=11).pack(fill=tk.X, pady=(22, 10))
        tk.Label(tarjeta, text="¿Todavía no tenés una cuenta?", font=("Arial", 10), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(pady=(4, 2))
        tk.Button(tarjeta, text="CREAR CUENTA", command=self.abrir_registro, bg=self.TARJETA, activebackground="#30374a", fg=self.ROJO, activeforeground=self.ROJO, font=("Arial", 10, "bold"), relief="flat", cursor="hand2").pack()
        tk.Label(contenedor, text="Bienvenido · La mejor experiencia en pantalla grande", font=("Arial", 9), fg="#747d93", bg=self.FONDO).pack(pady=(20, 0))

    def _crear_campo(self, parent, etiqueta, ocultar=False):
        tk.Label(parent, text=etiqueta, font=("Arial", 9, "bold"), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(anchor="w", pady=(10, 5))
        campo = tk.Entry(parent, show="•" if ocultar else "", bg=self.CAMPO, fg=self.TEXTO, insertbackground=self.TEXTO, relief="flat", font=("Arial", 11))
        campo.pack(fill=tk.X, ipady=9)
        return campo

        tk.Button(tarjeta, text="INGRESAR", command=self.ingresar, bg=self.ROJO, activebackground=self.ROJO_ACTIVO, fg="white", activeforeground="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", pady=11).pack(fill=tk.X, pady=(22, 10))
        tk.Label(tarjeta, text="¿Todavía no tenés una cuenta?", font=("Arial", 10), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(pady=(4, 2))
        tk.Button(tarjeta, text="CREAR CUENTA", command=self.abrir_registro, bg=self.TARJETA, activebackground="#30374a", fg=self.ROJO, activeforeground=self.ROJO, font=("Arial", 10, "bold"), relief="flat", cursor="hand2").pack()
        tk.Label(contenedor, text="CINEMARK · La mejor experiencia en pantalla grande", font=("Arial", 9), fg="#747d93", bg=self.FONDO).pack(pady=(20, 0))

    def _crear_campo(self, parent, etiqueta, ocultar=False):
        tk.Label(parent, text=etiqueta, font=("Arial", 9, "bold"), fg=self.TEXTO_SUAVE, bg=self.TARJETA).pack(anchor="w", pady=(10, 5))
        campo = tk.Entry(parent, show="•" if ocultar else "", bg=self.CAMPO, fg=self.TEXTO, insertbackground=self.TEXTO, relief="flat", font=("Arial", 11))
        campo.pack(fill=tk.X, ipady=9)
        return campo

    def ingresar(self):
        usuario_texto = self.entry_usuario.get()
        contrasenia_texto = self.entry_contrasenia.get()
        usuario_logueado = self.sistema.iniciar_sesion(usuario_texto, contrasenia_texto)
        if usuario_logueado:
            messagebox.showinfo("CINEMARK", f"¡Hola, {usuario_logueado.nombre}!")
        else:
            messagebox.showerror("CINEMARK", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        ventana_secundaria = tk.Toplevel(self.root)
        VentanaRegistro(ventana_secundaria, self.sistema)


if __name__ == "__main__":
    mi_sistema_cine = Sistema()
    mi_sistema_cine.cargar_datos()
    root = tk.Tk()
    VentanaLogin(root, mi_sistema_cine)
    root.mainloop()