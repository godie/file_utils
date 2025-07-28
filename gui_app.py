# gui_app.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Listbox
import shutil # Importamos shutil para copiar/mover archivos
from file_finder import search_files
import os
import json # Importamos el módulo json
import sys

DEFAULT_FILE_TYPES = {
    "Musica": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Documentos": [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Archivos Comprimidos": [".zip", ".rar", ".7z", ".tar.gz"],
    "Ejecutables": [".exe", ".msi", ".dmg", ".app"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"]
}

class FileSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Buscador y Gestor de Archivos")
        master.geometry("1000x700")

        self.selected_search_path = tk.StringVar()
        self.selected_search_path.set("Ningún directorio de búsqueda seleccionado")

        self.selected_destination_path = tk.StringVar()
        self.selected_destination_path.set("Ningún directorio de destino seleccionado")

        # --- Cargar tipos de archivo desde config.json o usar valores por defecto ---
        self.file_types = self.load_file_types_from_config()

        # Si por alguna razón grave (JSON inválido) no se pudieron cargar, salimos.
        # (Aunque load_file_types_from_config ya manejará la creación/error)
        if not self.file_types:
            messagebox.showerror("Error Crítico de Configuración",
                                 "No se pudieron establecer los tipos de archivo. La aplicación se cerrará.")
            master.destroy()

        self.checkbox_vars = {category: tk.BooleanVar() for category in self.file_types}
        self.found_files_list = []

        self.create_widgets()

    def load_file_types_from_config(self):
        """
        Carga las categorías y extensiones de archivo desde 'config.json'.
        Si el archivo no existe o es inválido, lo crea con la configuración por defecto.
        """
        # Determina la ruta donde debería estar el config.json
        if getattr(sys, 'frozen', False):
            # Si se ejecuta como un ejecutable PyInstaller
            application_path = os.path.dirname(sys.executable)
        else:
            # Si se ejecuta como script Python normal
            application_path = os.path.dirname(os.path.abspath(__file__))

        config_file_path = os.path.join(application_path, "config.json")

        # --- Intenta cargar el config.json existente ---
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Devuelve los tipos de archivo si la carga fue exitosa y tienen la clave esperada
                if "file_types" in config and isinstance(config["file_types"], dict):
                    return config["file_types"]
                else:
                    # Si el JSON es válido pero no tiene la estructura esperada
                    messagebox.showwarning("Advertencia de Configuración",
                                           f"El archivo '{config_file_path}' es válido pero no contiene la clave 'file_types' o no es un diccionario. Se creará con configuración por defecto.")
                    return self._create_default_config(config_file_path)

            except json.JSONDecodeError as e:
                # Si el archivo existe pero no es un JSON válido
                messagebox.showerror("Error de JSON",
                                      f"Error al leer '{config_file_path}': {e}\n"
                                      "El archivo parece corrupto. Se intentará recrear con configuración por defecto.")
                return self._create_default_config(config_file_path)
            except Exception as e:
                # Otros errores inesperados al cargar
                messagebox.showerror("Error Inesperado",
                                      f"Ocurrió un error al cargar la configuración de '{config_file_path}': {e}\n"
                                      "Se intentará recrear con configuración por defecto.")
                return self._create_default_config(config_file_path)
        else:
            # --- Si el archivo no existe, lo crea con la configuración por defecto ---
            messagebox.showinfo("Configuración",
                                f"El archivo de configuración '{config_file_path}' no se encontró. Se creará uno por defecto.")
            return self._create_default_config(config_file_path)

    def _create_default_config(self, config_file_path):
        """
        Crea o sobrescribe el archivo config.json con la configuración por defecto.
        """
        try:
            with open(config_file_path, 'w', encoding='utf-8') as f:
                json.dump({"file_types": DEFAULT_FILE_TYPES}, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Configuración Creada", f"Archivo '{config_file_path}' creado con la configuración por defecto.")
            return DEFAULT_FILE_TYPES
        except Exception as e:
            messagebox.showerror("Error al Crear Configuración",
                                  f"No se pudo crear el archivo de configuración por defecto en '{config_file_path}': {e}\n"
                                  "La aplicación puede no funcionar correctamente.")
            return None # Retorna None para indicar un fallo grave


    def create_widgets(self):
        # --- Frame para la Selección de Ruta de Búsqueda ---
        search_path_frame = tk.LabelFrame(self.master, text="Seleccionar Directorio de Búsqueda", padx=10, pady=10)
        search_path_frame.pack(padx=10, pady=5, fill="x")

        self.search_path_label = tk.Label(search_path_frame, textvariable=self.selected_search_path, wraplength=450)
        self.search_path_label.pack(side="left", fill="x", expand=True)

        self.browse_search_button = tk.Button(search_path_frame, text="Examinar Búsqueda", command=self.browse_search_directory)
        self.browse_search_button.pack(side="right")

        # --- Frame para la Selección de Tipos de Archivo ---
        types_frame = tk.LabelFrame(self.master, text="Seleccionar Tipos de Archivo", padx=10, pady=10)
        types_frame.pack(padx=10, pady=5, fill="x")

        row = 0
        col = 0
        # Ahora el bucle usa self.file_types cargado/creado
        for category, extensions in self.file_types.items():
            cb = tk.Checkbutton(types_frame, text=f"{category} ({', '.join(extensions)})",
                                variable=self.checkbox_vars[category])
            cb.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            col += 1
            if col > 2: # 3 columnas por fila para mejor distribución
                col = 0
                row += 1
        
        # --- Botón de búsqueda ---
        self.search_button = tk.Button(self.master, text="Iniciar Búsqueda", command=self.start_search)
        self.search_button.pack(pady=10)

        # --- Área de Resultados (Listbox para selección múltiple) ---
        results_frame = tk.LabelFrame(self.master, text="Resultados de la Búsqueda (Selecciona para Copiar/Mover)", padx=10, pady=10)
        results_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.results_listbox = Listbox(results_frame, selectmode=tk.MULTIPLE, height=10)
        self.results_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(results_frame, command=self.results_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_listbox.config(yscrollcommand=scrollbar.set)

        # --- Frame para Selección de Ruta de Destino ---
        destination_path_frame = tk.LabelFrame(self.master, text="Seleccionar Directorio de Destino", padx=10, pady=10)
        destination_path_frame.pack(padx=10, pady=5, fill="x")

        self.destination_path_label = tk.Label(destination_path_frame, textvariable=self.selected_destination_path, wraplength=450)
        self.destination_path_label.pack(side="left", fill="x", expand=True)

        self.browse_destination_button = tk.Button(destination_path_frame, text="Examinar Destino", command=self.browse_destination_directory)
        self.browse_destination_button.pack(side="right")

        # --- Frame para Botones de Acción (Copiar/Mover) ---
        action_buttons_frame = tk.Frame(self.master, padx=10, pady=10)
        action_buttons_frame.pack(pady=10)

        self.copy_button = tk.Button(action_buttons_frame, text="Copiar Archivos Seleccionados", command=self.copy_selected_files)
        self.copy_button.pack(side="left", padx=10)

        self.move_button = tk.Button(action_buttons_frame, text="Mover Archivos Seleccionados", command=self.move_selected_files)
        self.move_button.pack(side="right", padx=10)

        # --- Área de Mensajes de Log (para operaciones de copia/movimiento) ---
        log_frame = tk.LabelFrame(self.master, text="Log de Operaciones", padx=10, pady=10)
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=5)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state=tk.DISABLED)

    def browse_search_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_search_path.set(directory)
        else:
            self.selected_search_path.set("Ningún directorio de búsqueda seleccionado")

    def browse_destination_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_destination_path.set(directory)
        else:
            self.selected_destination_path.set("Ningún directorio de destino seleccionado")

    def start_search(self):
        search_dir = self.selected_search_path.get()
        if not os.path.isdir(search_dir):
            messagebox.showerror("Error", "Por favor, selecciona un directorio de búsqueda válido.")
            return

        selected_extensions = []
        for category, extensions in self.file_types.items():
            if self.checkbox_vars[category].get():
                selected_extensions.extend(extensions)

        if not selected_extensions:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un tipo de archivo para buscar.")
            return

        self.results_listbox.delete(0, tk.END)
        self.log_message(f"Buscando archivos en '{search_dir}' con extensiones: {', '.join(selected_extensions)}")

        self.found_files_list = search_files(search_dir, selected_extensions)

        if self.found_files_list:
            self.log_message("\nArchivos encontrados:")
            for file_path in self.found_files_list:
                relative_path = os.path.relpath(file_path, search_dir)
                self.results_listbox.insert(tk.END, relative_path)
        else:
            self.log_message("\nNo se encontraron archivos que coincidan con los criterios.")

    def get_selected_files_full_paths(self):
        selected_indices = self.results_listbox.curselection()
        return [self.found_files_list[i] for i in selected_indices]

    def process_files(self, operation_type):
        selected_files = self.get_selected_files_full_paths()
        destination_dir_base = self.selected_destination_path.get()
        search_dir_base = self.selected_search_path.get()

        if not selected_files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados en la lista de resultados.")
            return

        if not os.path.isdir(destination_dir_base):
            messagebox.showerror("Error", "Por favor, selecciona un directorio de destino válido.")
            return

        self.log_message(f"\nIniciando operación '{operation_type}' a '{destination_dir_base}', manteniendo estructura:")
        successful_operations = 0
        failed_operations = 0

        for source_path in selected_files:
            try:
                relative_path = os.path.relpath(source_path, search_dir_base)
                destination_full_path = os.path.join(destination_dir_base, relative_path)

                os.makedirs(os.path.dirname(destination_full_path), exist_ok=True)

                if operation_type == 'copy':
                    shutil.copy2(source_path, destination_full_path)
                    self.log_message(f"Copiado: '{relative_path}' a '{os.path.dirname(destination_full_path)}'")
                elif operation_type == 'move':
                    shutil.move(source_path, destination_full_path)
                    self.log_message(f"Movido: '{relative_path}' a '{os.path.dirname(destination_full_path)}'")
                successful_operations += 1
            except Exception as e:
                self.log_message(f"Error al {operation_type} '{source_path}': {e}", error=True)
                failed_operations += 1

        self.log_message(f"\nOperación '{operation_type}' completada. Exitosos: {successful_operations}, Fallidos: {failed_operations}")

        if operation_type == 'move' and successful_operations > 0:
            self.log_message("Considera ejecutar una nueva búsqueda para actualizar la lista de resultados tras mover archivos.")

    def copy_selected_files(self):
        self.process_files('copy')

    def move_selected_files(self):
        if messagebox.askyesno("Confirmar Mover", "¿Estás seguro de que quieres MOVER los archivos seleccionados?\n"
                                                  "Esto eliminará los archivos de su ubicación original y recreará su estructura de carpetas en el destino."):
            self.process_files('move')

    def log_message(self, message, error=False):
        self.log_text.config(state=tk.NORMAL)
        if error:
            self.log_text.insert(tk.END, f"ERROR: {message}\n", "error_tag")
            self.log_text.tag_config("error_tag", foreground="red")
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)