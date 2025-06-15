import csv
from Conexion import Conexion
from Nodo import Nodo
from Grafo import Grafo
from Solicitud import Solicitud

class LectorCSV:
    # Clase para manejar la lectura de archivos CSV relacionados con nodos, conexiones y solicitudes

    def __init__(self, archivo_nodos="archivos_ejemplo/original/nodos.csv", archivo_conexiones="archivos_ejemplo/original/conexiones.csv", archivo_solicitudes="archivos_ejemplo/original/solicitudes.csv"):
        self.archivo_nodos = archivo_nodos
        self.archivo_conexiones = archivo_conexiones
        self.archivo_solicitudes = archivo_solicitudes

    def set_archivo_solicitudes(self, nuevo_archivo_solicitudes):
        self.archivo_solicitudes = nuevo_archivo_solicitudes

    def leer_nodos(self):
        # Lee el archivo de nodos y devuelve una lista de objetos Nodo
        # Valida que cada fila tenga al menos una columna
        
        ciudades = []
        try:
            with open(self.archivo_nodos, "r", encoding="utf-8", newline="") as archivo:
                archivo.readline()  # Saltea encabezado
                lector = csv.reader(archivo)
                for fila in lector:
                    if len(fila) >= 1 and fila[0].strip():
                        ciudades.append(Nodo(fila[0].strip()))
                    else:
                        print(f"Fila invalida en {self.archivo_nodos}: {fila}")
            return ciudades
        except FileNotFoundError:
            raise FileNotFoundError("No se encontro el archivo de nodos")
            return []

    def leer_conexiones(self):
        # Lee el archivo de conexiones
        # Devuelve una lista de nodos con conexiones enlazadas y una lista de grafos por modo
        # Valida que cada fila tenga al menos 6 campos y que las ciudades existan
        ciudades = self.leer_nodos()

        modos = ["Ferroviaria", "Fluvial", "Aerea", "Automotor"]
        grafos = [Grafo(modo) for modo in modos]

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

        except FileNotFoundError:
            raise FileNotFoundError("No se encontro el archivo de conexiones")

    def leer_solicitud(self, ciudades):
        # Lee el archivo de solicitudes
        # Devuelve un objeto Solicitud utilizando la lista de ciudades ya cargadas
        # Valida que haya una sola fila y que las ciudades de origen/destino existan
        try:
            solicitudes=[]
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
                #return Solicitud(id_solicitud, tipo, origen, destino)

        except FileNotFoundError:
            raise FileNotFoundError("No se encontro el archivo de solicitudes")
