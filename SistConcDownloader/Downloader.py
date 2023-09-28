import os
import threading
import tkinter as tk
from tkinter import filedialog
import requests
from tqdm import tqdm

# ____  _____  _    _  _  _  __    _____    __    ____  ____  ____ #  
#(  _ \(  _  )( \/\/ )( \( )(  )  (  _  )  /__\  (  _ \( ___)(  _ \#  
# )(_) ))(_)(  )    (  )  (  )(__  )(_)(  /(__)\  )(_) ))__)  )   /#  
#(____/(_____)(__/\__)(_)\_)(____)(_____)(__)(__)(____/(____)(_)\_)#

#Downloader sencillo, de parte Ponce y Torres
#2023
#Threading para poder generar threads para cada descarga, para descargas concurrentes.
#Utilizamos Tkinter para la interface grafica, y componentes de la GUI, etiquetas, campos de entrada y botones, etc.
#---filedialog, proviene de Tkinter lo usamos para mostrar un cuadro de dialogo para la seleccion del destino de las descargas.
#Requests para realizar solicitudes HTTP, nos va a dar las utilidades para hacer las descargas.


#Creamos la clase y preparamos para armar la ventana de la interface grafica y los botones.
class Downloader:
    def __init__(self, window):
        self.window = window
        self.urls = []
        self.create_widgets()

    def create_widgets(self):
        # Creamos y mostramos la etiqueta y el campo de entrada de la URL
        self.label_url = tk.Label(self.window, text="URL:")
        self.label_url.pack()
        self.entry_url = tk.Entry(self.window, width=50)
        self.entry_url.pack()

        # Etiqueta, campo de entrada y botón "Seleccionar directorio"
        self.label_dest = tk.Label(self.window, text="Destino:")
        self.label_dest.pack()
        self.entry_dest = tk.Entry(self.window, width=50)
        self.entry_dest.pack()
        self.button_dest = tk.Button(
            self.window,
            text="Seleccionar directorio",
            command=self.choose_directory
        )
        self.button_dest.pack()

        # Mas botones "Agregar URL" y "Descargar todo"
        self.button_add = tk.Button(
            self.window,
            text="Agregar URL",
            command=self.add_url
        )
        self.button_add.pack()
        self.button_download = tk.Button(
            self.window,
            text="Descargar todo",
            command=self.start_download
        )
        self.button_download.pack()

        # Widget de texto para mostrar el estado de las descargas
        self.text_status = tk.Text(self.window, height=10, width=50)
        self.text_status.pack()

    def choose_directory(self):
        # Metodo para abrir el diálogo de selección de directorio y establecer el directorio seleccionado
        directory = filedialog.askdirectory()
        self.entry_dest.delete(0, tk.END)
        self.entry_dest.insert(tk.END, directory)

    def add_url(self):
        # Metodo para obtener la URL del campo de entrada y agregarla a la lista de URLs
        url = self.entry_url.get()
        if url:
            self.urls.append(url)
            self.entry_url.delete(0, tk.END)

    def start_download(self):
        # Metodo para obtener el directorio de destino e iniciar la descarga para cada URL en la lista
        destination = self.entry_dest.get()
        if destination and self.urls:
            for url in self.urls:
                # Creamos un hilo separado para cada descarga
                thread = threading.Thread(
                    target=self.download_file,
                    args=(url, destination)
                )
                thread.start()

    def download_file(self, url, destination):
        try:
            # Enviar una solicitud HTTP GET para descargar el archivo
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Lanzar una excepción para cualquier error HTTP

            # Extraer el nombre del archivo y construir la ruta del archivo
            file_name = url.split("/")[-1]
            file_path = os.path.join(destination, file_name)

            # Obtener el tamaño total del archivo a partir de los encabezados de la respuesta
            total_size = int(response.headers.get('content-length', 0))

            # Abrir el archivo para escritura en modo binario y mostrar una barra de progreso
            with open(file_path, "wb") as file:
                with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
                    # Iterar sobre el contenido de la respuesta en fragmentos y escribirlos en el archivo
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))

            self.update_status(f"Descargado {file_name}")
        except requests.RequestException as e:
            self.update_status(f"Error al descargar {url}: {str(e)}")

    def update_status(self, message):
        # Actualizar el estado de la descarga en el widget de texto
        self.text_status.insert(tk.END, message + "\n")
        self.text_status.see(tk.END)


if __name__ == "__main__":
    # Crear la ventana principal
    window = tk.Tk()
    window.title("Descargador de archivos")

    # Crear una instancia de la clase Downloader y comenzar el ciclo de eventos principal
    app = Downloader(window)
    window.mainloop()
