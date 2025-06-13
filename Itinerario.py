from Conexion import Conexion
from Modo import Modo
import math
import random

class Itinerario:
    def __init__(self,solicitud):
        self.solicitud=solicitud
    
    def construir_arbol(self, modo):
        caminos_nodos = []
        caminos_conexiones = []

        def dfs(actual, camino_nodo, camino_conexion, visitados):
            visitados.add(actual)
            camino_nodo.append(actual)

            if actual.ciudad == self.solicitud.destino.ciudad:
                caminos_nodos.append(list(camino_nodo))
                caminos_conexiones.append(list(camino_conexion))
            else:
                for vecino in actual.vecinos[modo]:
                    if vecino not in visitados:
                        # Buscar la conexión que une actual con vecino
                        conexion_correcta = None
                        for conexion in actual.conexiones[modo]:
                            if {actual, vecino} == conexion.tramo:
                                conexion_correcta = conexion
                                break

                        if conexion_correcta:
                            camino_conexion.append(conexion_correcta)
                            dfs(vecino, camino_nodo, camino_conexion, visitados)
                            camino_conexion.pop()

            camino_nodo.pop()
            visitados.remove(actual)

        dfs(self.solicitud.origen, [], [], set())
        return caminos_conexiones

    def calcular_costos_y_tiempos(self, modos_config):

        for modo_nombre in Conexion.modos_permitidos:
            modo = modos_config[modo_nombre]
            caminos_conexiones = self.construir_arbol(modo_nombre)
            
            # Si el peso maximo permitido en algun tramo es menor a la carga de la solicitud, directamente descarto el camino 
            if modo_nombre == "automotor":
                caminos_conexiones = [
                    camino for camino in caminos_conexiones
                    if all(not conexion.valor_restriccion or conexion.valor_restriccion >= self.solicitud.peso_kg for conexion in camino)
                ]

            cantidad_vehiculos = math.ceil(self.solicitud.peso_kg / modo.capacidad)
            for camino in caminos_conexiones:
                costo_total, tiempo_total, cantidad_vehiculos = self._calcular_costo_tiempo_camino(modo_nombre, modo, camino, cantidad_vehiculos)
                
                print(f"\nModo: {modo_nombre} - Costo: {costo_total}, Tiempo: {tiempo_total}, Cantidad vehiculos: {cantidad_vehiculos}")
                print("Camino:")
                for nodo in camino:
                    print(f" - {nodo}")

    def _calcular_costo_tiempo_camino(self, modo_nombre, vehiculo, camino, cantidad_vehiculos):
        costo_tramo_total = 0
        tiempo_total = 0

        for conexion in camino:
            distancia = conexion.distancia
            velocidad = vehiculo.velocidad 
            cperkm = vehiculo.cperkm
            cperkg = vehiculo.cperkg
            costo_fijo = vehiculo.costo_f

            match modo_nombre:
                case "ferroviaria":
                    cperkm = vehiculo.cperkm[0 if distancia < 200 else 1]
                    if conexion.restriccion:
                        velocidad = conexion.valor_restriccion

                case "automotor":
                    vehiculos_con_peso_max = self.solicitud.peso_kg // vehiculo.capacidad
                    peso_vehiculo_restante= self.solicitud.peso_kg-vehiculos_con_peso_max*vehiculo.capacidad
                    carga_vehiculos = [vehiculo.capacidad] * vehiculos_con_peso_max
                    if peso_vehiculo_restante != 0:
                        carga_vehiculos.append(peso_vehiculo_restante) 
                    cperkgs_vehiculos = [vehiculo.cperkg[0 if n < 15000 else 1] for n in carga_vehiculos]
                    cperkg = sum(c * kg for c, kg in zip(cperkgs_vehiculos, carga_vehiculos)) / self.solicitud.peso_kg

                case "fluvial":
                    costo_fijo = vehiculo.costo_f[0 if conexion.valor_restriccion == "fluvial" else 1]

                case "aerea":
                    # conexión.valor_restriccion se asume como probabilidad de mal tiempo
                    probabilidad = conexion.valor_restriccion or 0.0
                    velocidad = vehiculo.velocidad[1] if random.random() < probabilidad else vehiculo.velocidad[0]

                case _:
                    raise ValueError(f"Modo de transporte desconocido: {modo_nombre}")

            tiempo = 60 * distancia / velocidad #en minutos
            tiempo_total += tiempo
            costo_tramo_total += cperkm * distancia + costo_fijo

        costo_total = cantidad_vehiculos * costo_tramo_total + cperkg * self.solicitud.peso_kg
        return costo_total, tiempo_total, cantidad_vehiculos