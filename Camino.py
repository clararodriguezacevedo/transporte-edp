from Conexion import Conexion 

class Camino():
    def __init__(self, modo:str, costo_total: float, tiempo_total: float, cantidad_vehiculos: int, conexiones: list, registros: dict):
        self.modo = modo
        self.costo_total = costo_total
        self.tiempo_total = tiempo_total
        self.cantidad_vehiculos = cantidad_vehiculos
        self.conexiones = self.validar_lista_conexiones(conexiones) 
        self.registros = registros

    def __str__(self):
        texto = f"\nModo: {self.modo} - Costo: {self.costo_total}, Tiempo: {self.tiempo_total} minutos, Cantidad vehiculos: {self.cantidad_vehiculos}\nCamino:\n"
        for nodo in self.conexiones:
            texto += f" - {nodo}\n"
        return texto
    
    @staticmethod
    def validar_lista_conexiones(lista_conexiones):
        if not isinstance(lista_conexiones, list):   
            raise TypeError('No has ingresado una lista con conexiones')         
        for conexion in lista_conexiones:
            if not isinstance(conexion, Conexion):
                raise ValueError('No has ingresado una Conexion')
        return lista_conexiones

