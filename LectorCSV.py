import csv
from Conexion import Conexion
from Nodo import Nodo
from Grafo import Grafo
from Solicitud import Solicitud
from Modulo import modos_permitidos
from collections import deque

class LectorCSV:
    # Clase para manejar la lectura de archivos CSV relacionados con nodos, conexiones y solicitudes

    def __init__(self, nombre_archivos="original"):
        self.archivo_nodos = "archivos_ejemplo/" + nombre_archivos +"/nodos.csv"
        self.archivo_conexiones =  "archivos_ejemplo/" + nombre_archivos +"/conexiones.csv"
        self.archivo_solicitudes =  "archivos_ejemplo/" + nombre_archivos +"/solicitudes.csv"

    def set_archivo_solicitudes(self, nuevo_archivo_solicitudes):
        self.archivo_solicitudes = nuevo_archivo_solicitudes

    def leer_nodos(self):
        # Lee el archivo de nodos y devuelve una lista de objetos Nodo
        # Valida que cada fila tenga al menos una columna
        
        ciudades = [] #armamos una lista con los Nodos porque necesitamos una estructura Mutable e Iterable y en la que se mantenga un orden

        try:
            with open(self.archivo_nodos, "r", encoding="utf-8", newline="") as archivo:
                archivo.readline()  # Saltea encabezado
                lector = csv.reader(archivo)
                for fila in lector:
                    if len(fila) >= 1 and fila[0].strip():
                        ciudades.append(Nodo(fila[0].strip(), fila[1].strip()))
                    else:
                        print(f"Fila invalida en {self.archivo_nodos}: {fila}")
            return ciudades
        except Exception:
            raise FileNotFoundError("No se encontro el archivo de nodos")


    def leer_conexiones(self):
        # Lee el archivo de conexiones
        # Devuelve una lista de nodos con conexiones enlazadas y una lista de grafos por modo
        # Valida que cada fila tenga al menos 6 campos y que las ciudades existan
        ciudades = self.leer_nodos()

        grafos = [Grafo(modo) for modo in modos_permitidos]

        try:
            with open(self.archivo_conexiones, "r", encoding="utf-8", newline="") as archivo:
                archivo.readline()  # Saltea encabezado
                lector = csv.reader(archivo)

                for fila in lector:
                    if len(fila) < 6:
                        print(f"Fila incompleta en {self.archivo_conexiones}: {fila}")
                        continue

                    nombre_nodo1, nombre_nodo2, modo, *datos = [col.strip() for col in fila]

                    nodo1 = next((n for n in ciudades if n.ciudad == nombre_nodo1), None)
                    nodo2 = next((n for n in ciudades if n.ciudad == nombre_nodo2), None)

                    if not nodo1 or not nodo2:
                        raise ValueError(f"Ciudad no encontrada en {self.archivo_conexiones}: {nombre_nodo1}, {nombre_nodo2}")

                    conexion = Conexion(nodo1, nodo2, modo, *datos)

                    for nodo in (nodo1, nodo2):
                        nodo.enlazar_conexion(conexion)

                    for grafo in grafos:
                        if grafo.modo.lower() == modo.lower():
                            grafo.enlazar_conexion_grafo(conexion)
                            break
                        
                return ciudades, grafos

        except Exception:
            raise FileNotFoundError("No se encontro el archivo de conexiones")

    def leer_solicitud(self, ciudades):
        # Lee el archivo de solicitudes
        # Devuelve una lista con instancias de Solicitud utilizando la lista de ciudades ya cargadas
        # Valida que las ciudades de origen/destino existan
        try:
            solicitudes = deque() #usamos una cola asi las solicitudes se procesan en el orden en el que se ingresaron
            with open(self.archivo_solicitudes, "r", encoding="utf-8", newline="") as archivo:
                archivo.readline()
                lector = csv.reader(archivo)

                for fila in lector:
                    if len(fila) < 4:
                        raise ValueError(f"Fila invalida en {self.archivo_solicitudes}: {fila}")
                        
                    id_solicitud, tipo, nombre_origen, nombre_destino = [campo.strip() for campo in fila]
                    origen = next((c for c in ciudades if c.ciudad == nombre_origen), None)
                    destino = next((c for c in ciudades if c.ciudad == nombre_destino), None)

                    if not origen or not destino:
                        raise ValueError(f"Origen o destino no encontrado en {self.archivo_solicitudes}: {nombre_origen}, {nombre_destino}")
                        
                    solicitud=Solicitud(fila[0],fila[1],origen, destino)
                    solicitudes.append(solicitud)

                return solicitudes

        except Exception:
            raise FileNotFoundError("No se encontro el archivo de solicitudes")
