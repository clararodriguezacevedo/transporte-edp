from Conexion import Conexion
from Modos import Modo
import math

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
        # caminos = []

        # def dfs(actual, camino, visitados):
        #     visitados.add(actual)
        #     camino.append(actual)

        #     if actual == self.destino:
        #         caminos.append(list(camino))  # Copiamos el camino actual
        #     else:
        #         for vecino in actual.vecinos[modo]:
        #             if vecino not in visitados:
        #                 dfs(vecino, camino, visitados)

        #     # Backtrack
        #     camino.pop()
        #     visitados.remove(actual)

        # dfs(self.origen, [], set())
        # return caminos
    
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
    
    def calcular_costos(self):
        combinaciones = {} 
            
        tren= Modo("ferroviaria", 100,150000,100,[20,15],3)
        auto = Modo("automotor", 80, 30000, 30, 5, [1,2])
        barco= Modo("maritima",40,100000,[500,1500],15,2)
        avion = Modo("aereo",[600, 400], 5000, 750, 40, 10)
                
        for modo in Conexion.modos_permitidos:
            caminos_conexiones = self.construir_arbol(modo)
            
            # if modo=="automotor":
            #     for camino in caminos_conexiones:
            #         for conexion in camino:
            #             if conexion.valor_restriccion < self.peso_kg:
            #                 caminos_conexiones.remove(camino)
                
            combinaciones[modo] = caminos_conexiones
        
            match modo:
                case "ferroviaria":
                    for camino in combinaciones[modo]:
                        costo_total = 0
                        tiempo_total = 0
                        
                        for conexion in camino:
                            velocidad = tren.velocidad
                            capacidad = tren.capacidad
                            costo_f = tren.costo_f
                            cperkg = tren.cperkg
                            cperkm = tren.cperkm[(0 if conexion.distancia < 200 else 1)]
                            cantidad_vehiculos = math.ceil(self.peso_kg / capacidad)
                            if conexion.restriccion:
                                velocidad = conexion.valor_restriccion
                            tiempo = conexion.distancia / velocidad
                            costo = cantidad_vehiculos(costo_f + cperkm * conexion.distancia) + cperkg * self.peso_kg
                            
                            costo_total += costo
                            tiempo_total += tiempo
                            
                        print(f"Costo total del camino: {costo_total}, Tiempo total: {tiempo_total}")
                        print([n.tramo for n in camino])

               
  
                            
    
            






