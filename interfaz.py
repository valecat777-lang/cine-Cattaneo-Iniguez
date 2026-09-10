import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Requiere: pip install pillow

from login import VentanaLogin
from sistema import Administrador, Cliente, Funcion, Sistema


class TarjetaPelicula(tk.Frame):
    """Representa una tarjeta/poster individual al estilo Cinemark."""

    def __init__(self, parent, funcion, indice, callback_comprar, es_cliente):
        super().__init__(
            parent, bg="#1e1e2e", bd=1, relief="solid", padx=10, pady=10
        )
        self.funcion = funcion
        self.indice = indice
        self.callback_comprar = callback_comprar

        # --- Cargar y Redimensionar Imagen / Poster ---
        self.poster_image = self.cargar_imagen(
            getattr(funcion, "imagen", "default.jpg")
        )

        label_foto = tk.Label(self, image=self.poster_image, bg="#1e1e2e")
        label_foto.pack(pady=(0, 5))

        # --- Título ---
        lbl_titulo = tk.Label(
            self,
            text=funcion.pelicula,
            font=("Arial", 11, "bold"),
            fg="#ffffff",
            bg="#1e1e2e",
            wraplength=160,
        )
        lbl_titulo.pack()

        # --- Detalles ---
        info_txt = f"Sala: {funcion.sala}\n{funcion.fecha} - {funcion.hora}\n${funcion.precio} | Lugares: {funcion.capacidad}"
        lbl_info = tk.Label(
            self,
            text=info_txt,
            font=("Arial", 9),
            fg="#a6adc8",
            bg="#1e1e2e",
            justify="center",
        )
        lbl_info.pack(pady=4)

        # --- Botón Comprar Ticket ---
        if es_cliente:
            btn_comprar = tk.Button(
                self,
                text="Comprar Ticket",
                bg="#e74c3c",
                fg="white",
                font=("Arial", 9, "bold"),
                activebackground="#c0392b",
                activeforeground="white",
                relief="flat",
                command=lambda: self.callback_comprar(self.indice),
            )
            btn_comprar.pack(fill=tk.X, pady=(5, 0))

    def cargar_imagen(self, ruta_imagen):
        if not os.path.exists(ruta_imagen):
            img = Image.new("RGB", (150, 210), color="#313244")
        else:
            img = Image.open(ruta_imagen)

        img = img.resize((150, 210), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)


class VentanaPrincipalCine:

    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title(
            f"Cinemark / Cine App - {self.sistema.usuario_actual.usuario}"
        )
        self.root.geometry("1000x750")
        self.root.configure(bg="#11111b")

        # Variable para controlar si el admin está editando una función existente (guarda su índice)
        self.indice_edicion = None

        # --- Navbar estilo Cinemark ---
        frame_nav = tk.Frame(self.root, bg="#181825", height=60)
        frame_nav.pack(fill=tk.X)

        label_logo = tk.Label(
            frame_nav,
            text="🎬 CINEMARK",
            font=("Arial", 16, "bold"),
            fg="#e74c3c",
            bg="#181825",
        )
        label_logo.pack(side=tk.LEFT, padx=20, pady=15)

        lbl_user = tk.Label(
            frame_nav,
            text=f"Hola, {self.sistema.usuario_actual.nombre}",
            font=("Arial", 11),
            fg="white",
            bg="#181825",
        )
        lbl_user.pack(side=tk.RIGHT, padx=(5, 20))

        btn_logout = tk.Button(
            frame_nav,
            text="Salir",
            command=self.cerrar_sesion,
            bg="#313244",
            fg="white",
            relief="flat",
        )
        btn_logout.pack(side=tk.RIGHT, padx=5)

        # --- Notebook / Pestañas ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#11111b", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#181825",
            foreground="white",
            padding=[10, 5],
        )
        style.map("TNotebook.Tab", background=[("selected", "#e74c3c")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Tab Cartelera
        self.tab_cartelera = tk.Frame(self.notebook, bg="#11111b")
        self.notebook.add(self.tab_cartelera, text="Cartelera en Vivo")
        self.crear_vista_cartelera()

        # Tab Admin (Edición/Modificación)
        if isinstance(self.sistema.usuario_actual, Administrador):
            self.tab_admin = tk.Frame(self.notebook, bg="#11111b")
            self.notebook.add(self.tab_admin, text="Panel Admin")
            self.crear_vista_admin()

    # -------------------------------------------------------------
    # TAB 1: CARTELERA
    # -------------------------------------------------------------
    def crear_vista_cartelera(self):
        canvas = tk.Canvas(self.tab_cartelera, bg="#11111b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.tab_cartelera, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg="#11111b")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.renderizar_posters()

    def renderizar_posters(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        es_cliente = isinstance(self.sistema.usuario_actual, Cliente)
        columnas_max = 4

        for i, funcion in enumerate(self.sistema.funciones):
            fila = i // columnas_max
            columna = i % columnas_max

            tarjeta = TarjetaPelicula(
                self.scrollable_frame,
                funcion,
                i,
                self.realizar_compra,
                es_cliente,
            )
            tarjeta.grid(row=fila, column=columna, padx=12, pady=12)

    def realizar_compra(self, indice_funcion):
        exito, entrada, mensaje = self.sistema.comprar_entrada(indice_funcion)
        if exito:
            messagebox.showinfo(
                "¡Entrada Comprada!",
                f"{mensaje}\n\nPelícula: {entrada.pelicula}\nTicket ID: {entrada.id_entrada}",
            )
            self.renderizar_posters()
        else:
            messagebox.showerror("Error", mensaje)

    # -------------------------------------------------------------
    # TAB 2: PANEL DE ADMINISTRACIÓN (AGREGAR / MODIFICAR / ELIMINAR)
    # -------------------------------------------------------------
    def crear_vista_admin(self):
        # Frame Superior: Formulario
        self.frame_form = tk.LabelFrame(
            self.tab_admin,
            text=" Cargar / Modificar Película ",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#181825",
            padx=15,
            pady=10,
        )
        self.frame_form.pack(fill=tk.X, padx=10, pady=10)

        campos = [
            ("Película:", "pelicula"),
            ("Sala:", "sala"),
            ("Fecha:", "fecha"),
            ("Hora:", "hora"),
            ("Precio:", "precio"),
            ("Capacidad:", "capacidad"),
            ("Imagen (ej: posters/peli.jpg):", "imagen"),
        ]

        self.entries = {}
        for i, (label_text, key) in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(
                self.frame_form, text=label_text, fg="white", bg="#181825"
            ).grid(row=row, column=col, sticky="w", pady=4, padx=5)
            entry = tk.Entry(self.frame_form, width=25)
            entry.grid(row=row, column=col + 1, pady=4, padx=5)
            self.entries[key] = entry

        # Botones de Acción Formulario
        frame_botones_form = tk.Frame(self.frame_form, bg="#181825")
        frame_botones_form.grid(
            row=(len(campos) // 2) + 1, columnspan=4, pady=10
        )

        self.btn_guardar = tk.Button(
            frame_botones_form,
            text="Guardar Nueva Película",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.guardar_o_modificar_funcion,
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar = tk.Button(
            frame_botones_form,
            text="Cancelar Edición",
            bg="#7f8c8d",
            fg="white",
            command=self.limpiar_formulario,
        )

        # Frame Inferior: Tabla de gestión y eliminación
        frame_tabla = tk.LabelFrame(
            self.tab_admin,
            text=" Películas en Sistema ",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#181825",
            padx=10,
            pady=10,
        )
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = (
            "#",
            "Película",
            "Sala",
            "Fecha",
            "Hora",
            "Precio",
            "Capacidad",
            "Imagen",
        )
        self.tabla_admin = ttk.Treeview(
            frame_tabla, columns=cols, show="headings", height=8
        )

        for col in cols:
            self.tabla_admin.heading(col, text=col)
            width = 40 if col == "#" else 100
            self.tabla_admin.column(col, anchor=tk.CENTER, width=width)

        self.tabla_admin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_admin = ttk.Scrollbar(
            frame_tabla, orient="vertical", command=self.tabla_admin.yview
        )
        self.tabla_admin.configure(yscrollcommand=scrollbar_admin.set)
        scrollbar_admin.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones para Acciones sobre la Selección de la Tabla
        frame_acciones = tk.Frame(self.tab_admin, bg="#11111b")
        frame_acciones.pack(fill=tk.X, padx=10, pady=(0, 10))

        btn_cargar_editar = tk.Button(
            frame_acciones,
            text="✏️ Cargar Selección en Formulario para Editar",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.preparar_edicion,
        )
        btn_cargar_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(
            frame_acciones,
            text="🗑️ Eliminar Película Seleccionada",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.eliminar_funcion_admin,
        )
        btn_eliminar.pack(side=tk.RIGHT, padx=5)

        self.actualizar_tabla_admin()

    def actualizar_tabla_admin(self):
        for item in self.tabla_admin.get_children():
            self.tabla_admin.delete(item)

        for i, f in enumerate(self.sistema.funciones):
            imagen_ruta = getattr(f, "imagen", "default.jpg")
            self.tabla_admin.insert(
                "",
                tk.END,
                values=(
                    i,
                    f.pelicula,
                    f.sala,
                    f.fecha,
                    f.hora,
                    f"${f.precio}",
                    f.capacidad,
                    imagen_ruta,
                ),
            )

    def preparar_edicion(self):
        seleccion = self.tabla_admin.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Seleccione una película de la tabla inferior para modificar.",
            )
            return

        item = self.tabla_admin.item(seleccion[0])
        indice = item["values"][0]
        funcion = self.sistema.funciones[indice]

        # Cargar los datos en los campos de entrada
        self.indice_edicion = indice
        self.entries["pelicula"].delete(0, tk.END)
        self.entries["pelicula"].insert(0, funcion.pelicula)

        self.entries["sala"].delete(0, tk.END)
        self.entries["sala"].insert(0, funcion.sala)

        self.entries["fecha"].delete(0, tk.END)
        self.entries["fecha"].insert(0, funcion.fecha)

        self.entries["hora"].delete(0, tk.END)
        self.entries["hora"].insert(0, funcion.hora)

        self.entries["precio"].delete(0, tk.END)
        self.entries["precio"].insert(0, funcion.precio)

        self.entries["capacidad"].delete(0, tk.END)
        self.entries["capacidad"].insert(0, funcion.capacidad)

        self.entries["imagen"].delete(0, tk.END)
        self.entries["imagen"].insert(0, getattr(funcion, "imagen", ""))

        # Cambiar texto y visibilidad de los botones
        self.btn_guardar.config(
            text="Confirmar Modificación", bg="#f39c12"
        )
        self.btn_cancelar.pack(side=tk.LEFT, padx=5)

    def guardar_o_modificar_funcion(self):
        pelicula = self.entries["pelicula"].get()
        sala = self.entries["sala"].get()
        fecha = self.entries["fecha"].get()
        hora = self.entries["hora"].get()
        precio = self.entries["precio"].get()
        capacidad = self.entries["capacidad"].get()
        imagen = self.entries["imagen"].get()

        if self.indice_edicion is None:
            # Modo Agregar Nueva Película
            nueva_f = Funcion(
                pelicula, sala, fecha, hora, precio, capacidad, imagen
            )
            exito, msj = self.sistema.agregar_funcion(nueva_f)
        else:
            # Modo Modificar Película Existente
            exito, msj = self.sistema.modificar_funcion(
                self.indice_edicion,
                pelicula,
                sala,
                fecha,
                hora,
                precio,
                capacidad,
            )

            if exito:
                # Guardar el campo extra de imagen en el objeto editado
                self.sistema.funciones[self.indice_edicion].imagen = imagen
                self.sistema.guardar_datos()

        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_formulario()
            self.actualizar_tabla_admin()
            self.renderizar_posters()
        else:
            messagebox.showerror("Error", msj)

    def eliminar_funcion_admin(self):
        seleccion = self.tabla_admin.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención", "Seleccione una película de la tabla para eliminar."
            )
            return

        item = self.tabla_admin.item(seleccion[0])
        indice = item["values"][0]
        pelicula_nombre = item["values"][1]

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar la película '{pelicula_nombre}'?",
        )
        if confirmacion:
            exito, msj = self.sistema.eliminar_funcion(indice)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.actualizar_tabla_admin()
                self.renderizar_posters()
            else:
                messagebox.showerror("Error", msj)

    def limpiar_formulario(self):
        self.indice_edicion = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.btn_guardar.config(
            text="Guardar Nueva Película", bg="#2ecc71"
        )
        self.btn_cancelar.pack_forget()

    def cerrar_sesion(self):
        self.sistema.cerrar_sesion()
        self.root.destroy()
        root_login = tk.Tk()
        app = VentanaLoginWrapper(root_login, self.sistema)
        root_login.mainloop()


class VentanaLoginWrapper(VentanaLogin):

    def ingresar(self):
        usuario_texto = self.entry_usuario.get()
        contrasenia_texto = self.entry_contrasenia.get()
        usuario_logueado = self.sistema.iniciar_sesion(
            usuario_texto, contrasenia_texto
        )

        if usuario_logueado:
            self.root.destroy()
            root_main = tk.Tk()
            VentanaPrincipalCine(root_main, self.sistema)
            root_main.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    sistema_cine = Sistema()
    sistema_cine.cargar_datos()

    root = tk.Tk()
    app = VentanaLoginWrapper(root, sistema_cine)
    root.mainloop()