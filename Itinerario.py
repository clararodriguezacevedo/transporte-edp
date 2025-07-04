from Conexion import Conexion
from Modo import Modo
from Camino import Camino
import matplotlib.pyplot as pyplot
import numpy as np
from Solicitud import Solicitud
from Modulo import modos_permitidos
from collections import Counter
import math
import copy
import random

class Itinerario:
    def __init__(self,solicitud, ciudades:dict) :
        self.solicitud= self.validar_solicitud(solicitud)
        self.ciudades = ciudades
        self.camino_tiempo_optimo = None
        self.camino_costo_optimo = None
        self.camino_max_puntos_interes = None
    
    def __str__(self):
        if self.camino_tiempo_optimo == None and self.camino_costo_optimo == None:
            return "No se han encontrado los itinerarios optimos"
        else :
            return self.camino_tiempo_optimo, self.camino_costo_optimo
    
    @staticmethod
    def validar_solicitud(solicitud):
        if not isinstance(solicitud, Solicitud):
            raise ValueError("No has ingresado una Solicitud")    
        return solicitud

    def construir_arbol(self, modo):
        caminos_nodos = []
        caminos_conexiones = []

        def dfs(actual, camino_nodo, camino_conexion, visitados):
            visitados.add(actual)
            camino_nodo.append(actual)

            # Si llegamos al destino, guardamos el camino completo en caminos_conexiones
            if actual.ciudad == self.solicitud.destino.ciudad: 
                caminos_nodos.append(list(camino_nodo))
                caminos_conexiones.append(list(camino_conexion))
            else:
                for vecino in actual.vecinos[modo]:
                    if vecino not in visitados:
                        # Buscar la conexion que une actual con vecino
                        conexion_correcta = None
                        for conexion in actual.conexiones[modo]:
                            if {actual, vecino} == conexion.tramo:
                                conexion_correcta = conexion
                                break

                        # Si encontramos una conexion correcta, la agregamos al camino, y continuamos con la busqueda
                        if conexion_correcta:
                            camino_conexion.append(conexion_correcta)
                            dfs(vecino, camino_nodo, camino_conexion, visitados)
                            camino_conexion.pop()

            camino_nodo.pop()
            visitados.remove(actual)

        dfs(self.solicitud.origen, [], [], set())

        return caminos_conexiones, caminos_nodos # Devuelve una lista que incluye todos los caminos posibles entre el orgien y el destino, donde cada camino es una lista de conexiones

    def calcular_costos_y_tiempos(self, modos_config):
        
        costos_y_tiempos = [] # Armo una lista con todos los caminos con sus costos y tiempos

        for modo_nombre in modos_permitidos:
            modo = modos_config[modo_nombre]
            caminos_conexiones, caminos_nodos = self.construir_arbol(modo_nombre)
            
            # Si el peso maximo permitido en algun tramo es menor a la carga de la solicitud, directamente descarto el camino 
            if modo_nombre == "automotor":
                caminos_conexiones = [
                    camino for camino in caminos_conexiones
                    if all(not conexion.valor_restriccion or conexion.valor_restriccion >= self.solicitud.peso_kg for conexion in camino)
                ]

            cantidad_vehiculos = math.ceil(self.solicitud.peso_kg / modo.capacidad)
            for camino in caminos_conexiones:
                modo = copy.deepcopy(modo)
                costo_total, tiempo_total, cantidad_vehiculo, registros = self._calcular_costo_tiempo_camino(modo_nombre, modo, camino, cantidad_vehiculos)
                info_camino = Camino(modo_nombre, costo_total, tiempo_total, cantidad_vehiculos,camino, registros)
                costos_y_tiempos.append(info_camino)

        for info_camino in costos_y_tiempos:
            print(info_camino)      
            
        return costos_y_tiempos # Devuelve una lista de instancias de la clase Camino

    def _calcular_costo_tiempo_camino(self, modo_nombre, vehiculo, camino, cantidad_vehiculos):
        costo_tramo_total = 0
        tiempo_total = 0
        # Empiezo tres listas con registro de la informacion que voy a necesitar para hacer los graficos y el KPI de puntos de interes 
        registro_tiempo = [0] 
        registro_distancia = [0]
        if modo_nombre=="fluvial":
            registro_costo = []
            i = 0
        else:
            registro_costo = [vehiculo.costo_f]

        for conexion in camino:
            distancia = conexion.distancia
            velocidad, cperkm, cperkg, costo_fijo = vehiculo.aplicar_restricciones(conexion, self)
    
            if modo_nombre=="fluvial" and i==0:
                registro_costo.append(costo_fijo)
                i+=1

            tiempo = 60 * distancia / velocidad #en minutos
            tiempo_total += tiempo
            costo_tramo_total += cperkm * distancia + costo_fijo
            
            registro_costo.append(costo_tramo_total*cantidad_vehiculos + cperkg* self.solicitud.peso_kg)
            registro_tiempo.append(tiempo_total)
            registro_distancia.append(registro_distancia[-1] + distancia)

        registros = {'tiempo': registro_tiempo, 'costo': registro_costo, 'distancia': registro_distancia} #guardo la informacion de los registros en un diccionario
        costo_total = cantidad_vehiculos * costo_tramo_total + cperkg * self.solicitud.peso_kg
        return costo_total, tiempo_total, cantidad_vehiculos, registros
    

    def optimos(self, costos_y_tiempos): 
        camino_tiempo_optimo = None
        camino_costo_optimo = None
        camino_max_puntos_interes = None
        
        for actual in costos_y_tiempos:
            if camino_tiempo_optimo == None:
                camino_tiempo_optimo = actual
            elif actual.tiempo_total < camino_tiempo_optimo.tiempo_total:
                camino_tiempo_optimo = actual
            elif actual.tiempo_total == camino_tiempo_optimo.tiempo_total: #si los tiempos son iguales, me quedo con el camino mas barato
                if camino_tiempo_optimo.costo_total > actual.costo_total:
                    camino_tiempo_optimo = actual
            
            if camino_costo_optimo == None:
                camino_costo_optimo = actual
            elif actual.costo_total < camino_costo_optimo.costo_total:
                camino_costo_optimo = actual
            elif actual.costo_total == camino_costo_optimo.costo_total: #si los costos son iguales, me quedo con el camino mas rapido
                if camino_costo_optimo.tiempo_total > actual.tiempo_total:
                    camino_costo_optimo = actual

            if camino_max_puntos_interes == None:
                camino_max_puntos_interes = actual
            elif actual.puntos_interes > camino_max_puntos_interes.puntos_interes:
                camino_max_puntos_interes = actual
        
        self.camino_tiempo_optimo = camino_tiempo_optimo
        self.camino_costo_optimo = camino_costo_optimo
        self.camino_max_puntos_interes = camino_max_puntos_interes
        return camino_tiempo_optimo, camino_costo_optimo, camino_max_puntos_interes
    
    def crear_txt_con_optimos(self, solicitud, camino_tiempo_optimo, camino_costo_optimo, camino_max_puntos_interes, modo_escritura): 
        # Se crea un archivo que incluye los caminos optimos, de cada solicitud ingresada
        with open("optimos.txt", modo_escritura) as archivo:
            archivo.write(f"Solicitud: {solicitud.id_carga} \n")
            if camino_costo_optimo and camino_tiempo_optimo:
                archivo.write("Camino con el minimo tiempo de entrega:\n")
                archivo.write(f'{camino_tiempo_optimo}\n')
                archivo.write("Camino con el minimo costo total:\n")
                archivo.write(f'{camino_costo_optimo}\n')
                archivo.write("Camino con la maxima cantidad de puntos de interes:\n")
                archivo.write(f'{camino_max_puntos_interes}\n')

            else: # Si se ingreso un nodo desconectado, no se encuentran caminos, y se escribe este mensaje
                archivo.write(f"No existen caminos que unan {solicitud.origen} y {solicitud.destino}")

            


 
    
                
                
                
        
        
        
        
        
        