from Conexion import Conexion
from Modo import Modo
import math
import random

class Solicitud:
    def __init__(self,id_carga,peso_kg,origen,destino):
        # self.ciudades = ciudades
        self.id_carga = id_carga
        self.peso_kg = int(peso_kg) ## TODO: SACAR ESTE INT PORQUE HAY QUE VALIDAR! SINO PUEDE TIRAR ERROR
        self.origen = origen ## TODO: Validar todos los parametros de las clases
        self.destino = destino

    def __str__(self):
        return f"Origen: {self.origen.ciudad, self.origen}. Destino: {self.destino.ciudad, self.destino}"

    def verificar_modos(self):
        pass

    def verificar_ubicacion(ciudades, ubicacion):
        for elemento in ciudades:
            if elemento.ciudad == ubicacion:
              return elemento.ciudad
        return False

    def construir_arbol(self, modo):
        caminos_nodos = []
        caminos_conexiones = []

        def dfs(actual, camino_nodo, camino_conexion, visitados):
            visitados.add(actual)
            camino_nodo.append(actual)

            if actual.ciudad == self.destino.ciudad:
                caminos_nodos.append(list(camino_nodo))
                caminos_conexiones.append(list(camino_conexion))
            else:
                for vecino in actual.vecinos[modo]:
                    if vecino not in visitados:
                        # Buscar la conexión que une actual con vecino
                        conexion_correcta = None
                        for conexion in getattr(actual, modo):
                            if {actual, vecino} == conexion.tramo:
                                conexion_correcta = conexion
                                break

                        if conexion_correcta:
                            camino_conexion.append(conexion_correcta)
                            dfs(vecino, camino_nodo, camino_conexion, visitados)
                            camino_conexion.pop()

            camino_nodo.pop()
            visitados.remove(actual)

        dfs(self.origen, [], [], set())
        return caminos_conexiones

    def calcular_costos_y_tiempos(self, modos_config):

        for modo_nombre in Conexion.modos_permitidos:
            modo = modos_config[modo_nombre]
            caminos_conexiones = self.construir_arbol(modo_nombre)
            
            # si el peso maximo permitido en algun tramo es menor a la carga de la solicitud, directamente descarto el camino 
            if modo_nombre == "automotor":
                caminos_conexiones = [
                    camino for camino in caminos_conexiones
                    if all(not conexion.valor_restriccion or conexion.valor_restriccion >= self.peso_kg for conexion in camino)
                ]

            cantidad_vehiculos = math.ceil(self.peso_kg / modo.capacidad)
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
                    vehiculos_con_peso_max = self.peso_kg // vehiculo.capacidad
                    peso_vehiculo_restante= self.peso_kg-vehiculos_con_peso_max*vehiculo.capacidad
                    # if peso_vehiculo_restante<15000:
                    #     cperkg=vehiculo.cperkg[0]*peso_vehiculo_restante 
                    # else:
                    #     cperkg=vehiculo.cperkg[1]*peso_vehiculo_restante
                    # cperkg+=vehiculos_con_peso_max*vehiculo.capacidad*vehiculo.cperkg[1] 
                    carga_vehiculos = [vehiculo.capacidad] * vehiculos_con_peso_max
                    if peso_vehiculo_restante != 0:
                        carga_vehiculos.append(peso_vehiculo_restante) 
                    cperkgs_vehiculos = [vehiculo.cperkg[0 if n < 15000 else 1] for n in carga_vehiculos]
                    cperkg = sum(c * kg for c, kg in zip(cperkgs_vehiculos, carga_vehiculos)) / self.peso_kg

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

        costo_total = cantidad_vehiculos * costo_tramo_total + cperkg * self.peso_kg
        return costo_total, tiempo_total, cantidad_vehiculos


    
    # def calcular_costos(self):
    #     combinaciones = {} 
            
    #     tren= Modo("ferroviaria", 100,150000,100,[20,15],3)
    #     auto = Modo("automotor", 80, 30000, 30, 5, [1,2])
    #     barco= Modo("maritima",40,100000,[500,1500],15,2)
    #     avion = Modo("aereo",[600, 400], 5000, 750, 40, 10)
                
    #     for modo in Conexion.modos_permitidos:
    #         caminos_conexiones = self.construir_arbol(modo)
            
    #         if modo=="automotor": # Es el unico modo en el que puede pasar que un camino sea no valido (si tiene una restriccion con peso menor al peso de la solicitud)
    #             for camino in caminos_conexiones:
    #                 for conexion in camino:
    #                     if conexion.valor_restriccion and conexion.valor_restriccion < self.peso_kg:
    #                         caminos_conexiones.remove(camino)
                
    #         combinaciones[modo] = caminos_conexiones
        
    #         match modo:
    #             case "ferroviaria":
    #                 capacidad = tren.capacidad
    #                 costo_f = tren.costo_f
    #                 cperkg = tren.cperkg
    #                 cantidad_vehiculos = math.ceil(self.peso_kg / capacidad)
                    
    #                 for camino in combinaciones[modo]:
    #                     costo_total = 0
    #                     tiempo_total = 0
    #                     costo_tramo = 0
                        
    #                     for conexion in camino:
    #                         #velocidad = tren.velocidad
    #                         # capacidad = tren.capacidad
    #                         # costo_f = tren.costo_f
    #                         # cperkg = tren.cperkg
    #                         cperkm = tren.cperkm[(0 if conexion.distancia < 200 else 1)]
    #                         #cantidad_vehiculos = math.ceil(self.peso_kg / capacidad)
                        
    #                         if conexion.restriccion:
    #                             velocidad = conexion.valor_restriccion
    #                         else:
    #                             velocidad = tren.velocidad
    #                         tiempo = conexion.distancia / velocidad
    #                         costo_tramo += cperkm * conexion.distancia + costo_f
                            
    #                         tiempo_total += tiempo
                        
    #                     costo_total=cantidad_vehiculos*costo_tramo + cperkg * self.peso_kg
    #                     print(f"Costo total del camino: {costo_total}, Tiempo total: {tiempo_total}")
    #                     # print([n for n in camino])
    #                     for n in camino:
    #                         print(n)

    # #ver si se podria reutilizar una funcion de este estilo en la de arriba.
    # def calcular_costos_tiempo(self, modo,vehiculo,combinaciones):
    #     #estos dos se calculan igual para todos
    #     capacidad = vehiculo.capacidad
    #     cantidad_vehiculos = math.ceil(self.peso_kg / capacidad)
        
    #     for camino in combinaciones[modo]:
    #         costo_total = 0
    #         tiempo_total = 0
    #         costo_tramo = 0
            
    #         for conexion in camino:
    #             match modo:
    #                 case "ferroviaria":
    #                     ###### estos dos tienen restriccion en los otros metodos, pero creo que en este no es necesario que esten en el for de conexion, no se donde meterlo (pasa lo mismo en los otros)
    #                     costo_f = vehiculo.costo_f
    #                     cperkg = vehiculo.cperkg
                        
    #                     cperkm = vehiculo.cperkm[(0 if conexion.distancia < 200 else 1)]
    #                     if conexion.restriccion:
    #                         velocidad = conexion.valor_restriccion
    #                     else:
    #                         velocidad = vehiculo.velocidad
    #                 case "automotor":
    #                     velocidad = vehiculo.velocidad
    #                     costo_f = vehiculo.costo_f
    #                     cperkm = vehiculo.cperkm
    #                     cperkg = vehiculo.cperkg[(0 if self.peso_kg < 15000 else 1)]
    #                     #puede que falte la restriccion de la conexion
    #                 case "fluvial":
    #                     velocidad = vehiculo.velocidad
    #                     cperkm = vehiculo.cperkm
    #                     cperkg = vehiculo.cperkg
    #                     costo_f = vehiculo.costo_f[(0 if conexion.valor_restriccion =="fluvial" else 1)]
    #                     #puede que falte la restriccion de la conexion
    #                 case "aerea":
                        
                        
                    
                        
    #             tiempo = conexion.distancia / velocidad
    #             costo_tramo += cperkm * conexion.distancia + costo_f
                
    #             tiempo_total += tiempo
            
    #         costo_total=cantidad_vehiculos*costo_tramo + cperkg * self.peso_kg
            
  
                            
    
            






