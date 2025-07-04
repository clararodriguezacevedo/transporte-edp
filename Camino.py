from Conexion import Conexion 
from Modulo import validar_modo

class Camino():
    def __init__(self, modo:str, costo_total: float, tiempo_total: float, cantidad_vehiculos: int, conexiones: list, registros: dict):
        self.modo = validar_modo(modo)
        self.costo_total = costo_total
        self.tiempo_total = tiempo_total
        self.cantidad_vehiculos = cantidad_vehiculos
        self.conexiones = self.validar_lista_conexiones(conexiones) 
        self.registros = registros
        self.puntos_interes= self.calcular_puntos_interes()

    def __str__(self):
        texto = f"\nModo: {self.modo} - Costo: {self.costo_total}, Tiempo: {self.tiempo_total} minutos, Cantidad vehiculos: {self.cantidad_vehiculos}, Cantidad de puntos de interes: {self.puntos_interes}\nCamino:\n"
        for conexion in self.conexiones:
            texto += f" - {conexion}\n"
        return texto
    
    @staticmethod
    def validar_lista_conexiones(lista_conexiones):
        if not isinstance(lista_conexiones, list):   
            raise TypeError('No has ingresado una lista con conexiones')         
        for conexion in lista_conexiones:
            if not isinstance(conexion, Conexion):
                raise ValueError('No has ingresado una Conexion')
        return lista_conexiones

    def calcular_puntos_interes(self):
        puntos = 0
        for conexion in self.conexiones:
               puntos+= conexion.origen.puntos_de_interes
        return puntos