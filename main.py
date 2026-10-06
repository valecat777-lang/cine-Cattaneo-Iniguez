import tkinter as tk
from sistema import Sistema
from interfaz import VentanaLoginWrapper


# Punto de inicio del programa
def main():
    # Crear el sistema del cine
    sistema_cine = Sistema()

    # Cargar los datos guardados en los archivos JSON
    sistema_cine.cargar_datos()

    # Crear la ventana de login
    root = tk.Tk()
    VentanaLoginWrapper(root, sistema_cine)

    # Iniciar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()