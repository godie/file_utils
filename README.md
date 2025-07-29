# FileFinder

## Descripción

**FileFinder** es una aplicación de escritorio sencilla pero potente, diseñada para ayudarte a **buscar y gestionar archivos** en tu sistema de manera eficiente. Permite buscar archivos por tipo (música, videos, documentos, imágenes, etc.) en un directorio específico y sus subcarpetas, y luego te ofrece la opción de **copiar o mover los archivos encontrados manteniendo su estructura de directorios original**.

La aplicación es ideal para:

* Organizar colecciones grandes de archivos.
* Migrar tipos específicos de archivos a una nueva ubicación.
* Limpiar directorios desordenados.

## Características

* **Búsqueda Recursiva**: Explora directorios y todos sus subdirectorios.
* **Filtro por Tipo de Archivo**: Busca archivos por categorías predefinidas como música, videos, documentos, imágenes, etc.
* **Configuración Flexible**: Los tipos de archivo y sus extensiones son configurables a través de un archivo `config.json` externo que el usuario puede editar. Si el archivo no existe, se crea automáticamente con una configuración por defecto.
* **Gestión de Archivos**: Copia o mueve los archivos seleccionados a un directorio de destino.
* **Preservación de Estructura**: Mantiene la jerarquía de subdirectorios de los archivos encontrados al copiarlos o moverlos.
* **Interfaz Gráfica de Usuario (GUI)**: Fácil de usar gracias a su interfaz intuitiva basada en Tkinter.
* **Multiplataforma**: Disponible como ejecutable para Windows y macOS, o como script Python.

---

## Instalación y Uso

### Para Usuarios Finales (Ejecutable)

Si usas Windows o macOS, la forma más sencilla es descargar la versión precompilada.

1.  Ve a la sección de **[Releases](https://github.com/godie/file_utils/releases)** de este repositorio.
2.  Descarga el archivo `.zip` o `.dmg` más reciente para tu sistema operativo (ej. `file-finder-windows-exe.zip` o `file-finder-macos-dmg.zip`).
3.  **Descomprime el archivo descargado.**
4.  Dentro de la carpeta descomprimida, encontrarás:
    * `FileFinder.exe` (Windows) o `FileFinder.app` (macOS).
    * `config.json`
5.  **Asegúrate de que `FileFinder.exe` (o `FileFinder.app`) y `config.json` estén en la misma carpeta.**
6.  Haz doble clic en el ejecutable para iniciar la aplicación.

### Para Desarrolladores / Ejecutar desde el Código Fuente

Si deseas ejecutar la aplicación desde el código fuente o contribuir al desarrollo:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/godie/file_utils.git](https://github.com/godie/file_utils.git)
    cd file_utils
    ```
2.  **(Opcional pero recomendado) Crea un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
3.  **No se necesitan dependencias externas aparte de Python estándar.**
4.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

---

## Configuración de Tipos de Archivo (`config.json`)

El archivo `config.json` permite personalizar las categorías y extensiones de archivo que FileFinder buscará.

**Si `config.json` no existe en la misma carpeta que el ejecutable, se creará automáticamente con la configuración por defecto la primera vez que inicies la aplicación.**

Puedes abrir `config.json` con cualquier editor de texto plano (como el Bloc de Notas, Visual Studio Code, Notepad++, etc.) y modificarlo.

**Formato de `config.json`:**

```json
{
  "file_types": {
    "Música": [".mp3", ".wav", ".ogg", ".flac"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Mis Documentos": [".pdf", ".docx", ".xlsx", ".pptx"],
    "Otros": [".log", ".txt"]
  }
}