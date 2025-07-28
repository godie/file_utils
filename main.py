# main.py
import tkinter as tk
from gui_app import FileSearchApp # Importa nuestra clase de la GUI

if __name__ == "__main__":
    root = tk.Tk() # Crea la ventana principal de Tkinter
    app = FileSearchApp(root) # Instancia nuestra aplicación GUI
    root.mainloop() # Inicia el bucle de eventos de Tkinter