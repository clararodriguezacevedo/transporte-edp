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

class Grafico:
    
    @staticmethod
    def graficar_frecuencia_ciudades(itinerario):
        conteo_ciudades = Counter()

        for modo_nombre in modos_permitidos:
            _, caminos_nodos = itinerario.construir_arbol(modo_nombre)

            for camino in caminos_nodos:
                for nodo in camino:
                    conteo_ciudades[nodo.ciudad] += 1

        ciudades_ordenadas = sorted(conteo_ciudades.items(), key=lambda x: x[1], reverse=True)
        nombres_ciudades = [nombre for nombre, _ in ciudades_ordenadas]
        frecuencias = [frecuencia for _, frecuencia in ciudades_ordenadas]

        pyplot.figure(figsize=(12, 6))
        pyplot.bar(nombres_ciudades, frecuencias, color="skyblue")
        pyplot.xlabel("Ciudades")
        pyplot.ylabel("Frecuencia de aparición en caminos")
        pyplot.title("Histograma de Ciudades Más Visitadas")
        pyplot.xticks(rotation=45, ha="right")
        pyplot.tight_layout()
        pyplot.grid(axis="y", linestyle="--", alpha=0.7)
        pyplot.show()
    
    @staticmethod
    def crear_graficos(camino1, camino2):
        pyplot.plot(camino1.registros['tiempo'], camino1.registros['distancia'], color='green', marker='o', label='Camino Tiempo Optimizado')
        pyplot.plot(camino2.registros['tiempo'], camino2.registros['distancia'], color='red', marker='s', label='Camino Costo Optimizado')
        pyplot.xlabel("Tiempo Acumulado (m)")
        pyplot.ylabel("Distancia Acumulada (km)")
        pyplot.title("Distancia Acumulada vs Tiempo Acumulado")
        pyplot.grid(True)
        pyplot.legend()
        pyplot.show()

        pyplot.plot(camino1.registros['distancia'], camino1.registros['costo'], color='green', marker='o', label='Camino Tiempo Optimizado')
        pyplot.plot(camino2.registros['distancia'], camino2.registros['costo'], color='red', marker='s', label='Camino Costo Optimizado')
        pyplot.xlabel("Distancia Acumulada (km)")
        pyplot.ylabel("Costo acumulado ($)")
        pyplot.title("Costo Acumulado vs Distancia Acumulada")
        pyplot.grid(True)
        pyplot.legend()
        pyplot.show()

        pyplot.plot(camino1.registros['tiempo'], camino1.registros['costo'], color='green', marker='o', label='Camino Tiempo Optimizado')
        pyplot.plot(camino2.registros['tiempo'], camino2.registros['costo'], color='red', marker='s', label='Camino Costo Optimizado')
        pyplot.xlabel("Tiempo acumulado (m)")
        pyplot.ylabel("Costo acumulado ($)")
        pyplot.title("Costo Acumulado vs Tiempo Acumulado")
        pyplot.grid(True)
        pyplot.legend()
        pyplot.show()
        
    @staticmethod
    def comparacion_modos(itinerario, modos_config, costos_y_tiempos):
        comparacion_modos = {}  # Diccionario para almacenar sumas de costos y tiempos

        for modo_nombre in modos_permitidos:
            modo = modos_config[modo_nombre]
            caminos_conexiones, caminos_nodos = itinerario.construir_arbol(modo_nombre)
            
            # Filtrar caminos según restricción de peso en "automotor"
            if modo_nombre == "automotor":
                caminos_conexiones = [
                    camino for camino in caminos_conexiones
                    if all(not conexion.valor_restriccion or conexion.valor_restriccion >= itinerario.solicitud.peso_kg for conexion in camino)
                ]

            suma_costos, suma_tiempos = 0, 0  # Variables para acumular costos y tiempos
            cantidad_vehiculos = math.ceil(itinerario.solicitud.peso_kg / modo.capacidad)

            for camino in caminos_conexiones:
                costo_total, tiempo_total, cantidad_vehiculo, registros = itinerario._calcular_costo_tiempo_camino(modo_nombre, modo, camino, cantidad_vehiculos)
    
                # Acumular los valores totales de costo y tiempo por modo de transporte
                suma_costos += costo_total
                suma_tiempos += tiempo_total

            # Almacenar las sumas en el diccionario con formato [costo_total, tiempo_total]
            comparacion_modos[modo_nombre] = [suma_costos, suma_tiempos]

        # Mostrar resultados para depuración
        for modo, valores in comparacion_modos.items():
            print(f"Modo: {modo} -> Costo total: {valores[0]}, Tiempo total: {valores[1]}")

        return comparacion_modos

    @staticmethod
    def comparacion_modos_grafico(itinerario, modos_config, costos_y_tiempos):
        comparacion_modos = Grafico.comparacion_modos(itinerario, modos_config, costos_y_tiempos)
        modos = list(comparacion_modos.keys())
        costos = [comparacion_modos[modo][0] for modo in modos]
        tiempos = [comparacion_modos[modo][1] for modo in modos]

        x = np.arange(len(modos))
        ancho_barra = 0.4

        fig1, ax1 = pyplot.subplots(figsize=(10, 6))
        ax1.bar(x, costos, width=ancho_barra, color="blue", alpha=0.7)
        ax1.set_xticks(x)
        ax1.set_xticklabels(modos, rotation=45)
        ax1.set_ylabel("Costo Total")
        ax1.set_title("Comparación de Costos por Modo de Transporte")

        fig2, ax2 = pyplot.subplots(figsize=(10, 6))
        ax2.bar(x, tiempos, width=ancho_barra, color="orange", alpha=0.7)
        ax2.set_xticks(x)
        ax2.set_xticklabels(modos, rotation=45)
        ax2.set_ylabel("Tiempo Total")
        ax2.set_title("Comparación de Tiempos por Modo de Transporte")

        pyplot.show()
        
    @staticmethod
    def dispersion_costos_tiempos(costos_y_tiempos):
        tiempos_por_modo = {}
        costos_por_modo = {}

        for camino in costos_y_tiempos:
            modo = camino.modo
            if modo not in tiempos_por_modo:
                tiempos_por_modo[modo] = []
                costos_por_modo[modo] = []
            tiempos_por_modo[modo].append(camino.tiempo_total)
            costos_por_modo[modo].append(camino.costo_total)

        # Boxplot de tiempos
        pyplot.figure(figsize=(10, 5))
        pyplot.boxplot(
            [tiempos_por_modo[modo] for modo in tiempos_por_modo],
            labels=list(tiempos_por_modo.keys())
        )
        pyplot.title("Dispersión de Tiempos de los caminos por Modo de Transporte")
        pyplot.ylabel("Tiempo total (minutos)")
        pyplot.grid(True, axis='y', linestyle='--', alpha=0.7)
        pyplot.show()

        # Boxplot de costos
        pyplot.figure(figsize=(10, 5))
        pyplot.boxplot(
            [costos_por_modo[modo] for modo in costos_por_modo],
            labels=list(costos_por_modo.keys())
        )
        pyplot.title("Dispersión de Costos de los caminos por Modo de Transporte")
        pyplot.ylabel("Costo total ($)")
        pyplot.grid(True, axis='y', linestyle='--', alpha=0.7)
        pyplot.show()



    