# file_search_logic.py
import os

def search_files(directory, file_extensions):
    """
    Busca archivos con extensiones específicas dentro de un directorio y sus subdirectorios.

    Args:
        directory (str): La ruta del directorio a buscar.
        file_extensions (list): Una lista de extensiones de archivo a buscar (ej. ['.mp3', '.wav']).
                                 La búsqueda es insensible a mayúsculas y minúsculas.

    Returns:
        list: Una lista de rutas completas de los archivos encontrados.
    """
    found_files = []
    normalized_extensions = [ext.lower() for ext in file_extensions]

    for root, _, files in os.walk(directory):
        for file in files:
            for ext in normalized_extensions:
                if file.lower().endswith(ext):
                    found_files.append(os.path.join(root, file))
                    break
    return found_files