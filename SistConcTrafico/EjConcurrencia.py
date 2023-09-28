import threading
import time
from colorama import init, Fore, Style

init()

class Semaforo:
    def __init__(self):
        self.rojo = threading.Event()
        self.amarillo = threading.Event()
        self.verde = threading.Event()
        self.tiempo_rojo = 5
        self.tiempo_amarillo = 2
        self.tiempo_verde = 5

    def ciclo_semaforo(self):
        while True:
            self.rojo.set()
            self.print_colored("Luz roja - ¡Detente!", Fore.RED)
            time.sleep(self.tiempo_rojo)
            self.rojo.clear()

            self.amarillo.set()
            self.print_colored("Luz amarilla - Precaución", Fore.YELLOW)
            time.sleep(self.tiempo_amarillo)
            self.amarillo.clear()

            self.verde.set()
            self.print_colored("Luz verde - Adelante", Fore.GREEN)
            time.sleep(self.tiempo_verde)
            self.verde.clear()

    def print_colored(self, text, color):
        print(color + text + Style.RESET_ALL)

if __name__ == "__main__":
    semaforo = Semaforo()

    # Iniciar el ciclo del semáforo en un hilo separado
    semaforo_thread = threading.Thread(target=semaforo.ciclo_semaforo)
    semaforo_thread.start()

    # Simulación de tráfico pasando por el semáforo
    while True:
        time.sleep(1)
        if semaforo.rojo.is_set():
            semaforo.print_colored("Tráfico detenido", Fore.RED)
        elif semaforo.amarillo.is_set():
            semaforo.print_colored("Tráfico con precaución", Fore.YELLOW)
        elif semaforo.verde.is_set():
            semaforo.print_colored("Tráfico fluyendo", Fore.GREEN)