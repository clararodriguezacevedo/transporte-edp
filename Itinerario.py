from Conexion import Conexion
from Modo import Modo
from Camino import Camino
import matplotlib.pyplot as pyplot
from Solicitud import Solicitud

import math
import random

class Itinerario:
    def __init__(self,solicitud) :
        self.solicitud= Itinerario.validar_solicitud(solicitud)
        self.camino_tiempo_optimo = None
        self.camino_costo_optimo = None
    
    def __str__(self):
        if self.camino_tiempo_optimo == None and self.camino_costo_optimo == None:
            return"No se han encontrado los itinerarios optimos"
        else :
            return self.camino_tiempo_optimo, self.camino_costo_optimo
    
    #getters y setters
    '''def get_solicitud(self):
        return self.solicitud
    def set_solicitud(self, other):
        if validar_solicitud(other):
            self.solicitud = other
    def get_camino_tiempo_optimo(self):
        return self.camino_tiempo_optimo
    def set_camino_tiempo_optimo(self, other):
        if validar_camino(other):
            self.get_camino_tiempo_optimo = other
    def get_camino_costo_optimo(self):
        return self.camino_costo_optimo
    def set_camino_costo_optimo(self, other):
        if validar_camino(other):
            self.get_camino_costo_optimo = other'''
    
        

    @staticmethod
    def validar_camino(camino):
        if not isinstance(camino, Camino):
            raise ValueError("No se ingreso un camino.")
        return camino
    
    @staticmethod
    def validar_solicitud(solicitud):
        if not isinstance(solicitud, Solicitud):
            raise ValueError("No has ingresado una Solicitud")    
        return solicitud
        return solicitud

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
        
        costos_y_tiempos = [] #armo una lista con todos los caminos con sus costos y tiempos

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
                costo_total, tiempo_total, cantidad_vehiculo, registros = self._calcular_costo_tiempo_camino(modo_nombre, modo, camino, cantidad_vehiculos)
                info_camino = Camino(modo_nombre, costo_total, tiempo_total, cantidad_vehiculos,camino, registros)
                costos_y_tiempos.append(info_camino)
            
                
                #print(f"\nModo: {modo_nombre} - Costo: {costo_total}, Tiempo: {tiempo_total}, Cantidad vehiculos: {cantidad_vehiculos}")
                #print("Camino:")
                #for nodo in camino:
                #    print(f" - {nodo}")
        for info_camino in costos_y_tiempos:
            print(info_camino)      
        return costos_y_tiempos

    def _calcular_costo_tiempo_camino(self, modo_nombre, vehiculo, camino, cantidad_vehiculos):
        costo_tramo_total = 0
        tiempo_total = 0
        #empiezo tres listas con registro de la informacion que voy a necesitar para hacer los graficos
        registro_tiempo = [0] 
        registro_distancia = [0]
        registro_costo = [vehiculo.costo_f]

        for conexion in camino:
            distancia = conexion.distancia
            velocidad = vehiculo.velocidad 
            cperkm = vehiculo.cperkm
            cperkg = vehiculo.cperkg
            costo_fijo = vehiculo.costo_f
            i = 0 #inicio un contador para asegurarme de contar solo 1 vez los costos fijos en el registro

            match modo_nombre:
                case "ferroviaria":
                    cperkm = vehiculo.cperkm[0 if distancia < 200 else 1]
                    if conexion.restriccion:
                        velocidad = conexion.valor_restriccion

                case "automotor":
                    vehiculos_con_peso_max = int(self.solicitud.peso_kg // vehiculo.capacidad)
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
                    if conexion.valor_restriccion:
                        probabilidad = conexion.valor_restriccion #or 0.0
                    else:
                        probabilidad = 0.0
                    velocidad = vehiculo.velocidad[1] if random.random() < probabilidad else vehiculo.velocidad[0]

                case _:
                    raise ValueError(f"Modo de transporte desconocido: {modo_nombre}")

            tiempo = 60 * distancia / velocidad #en minutos
            tiempo_total += tiempo
            costo_tramo_total += cperkm * distancia + costo_fijo
            
            registro_costo.append(costo_tramo_total*cantidad_vehiculos + cperkg* self.solicitud.peso_kg)
            registro_tiempo.append(tiempo_total)
            registro_distancia.append(distancia)

        registros = {'tiempo': registro_tiempo, 'costo': registro_costo, 'distancia': registro_distancia} #guardo la informacion de los registros en un diccionario
        costo_total = cantidad_vehiculos * costo_tramo_total + cperkg * self.solicitud.peso_kg
        return costo_total, tiempo_total, cantidad_vehiculos, registros
    
    def optimos(self, costos_y_tiempos): 
        camino_tiempo_optimo = None
        camino_costo_optimo = None
        
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
            elif actual.costo_total == camino_costo_optimo: #si los costos son iguales, me quedo con el camino mas rapido
                if camino_costo_optimo.tiempo_total > actual.tiempo_total:
                    camino_costo_optimo = actual
        
        self.camino_tiempo_optimo = camino_tiempo_optimo
        self.camino_costo_optimo = camino_costo_optimo
        return camino_tiempo_optimo, camino_costo_optimo
    
    def crear_graficos(self, camino1, camino2):
        print(camino1.registros)
        print(camino2.registros)

        pyplot.plot(camino1.registros['tiempo'], camino1.registros['distancia'], color = 'green', marker = 'o')
        pyplot.plot(camino2.registros['tiempo'], camino2.registros['distancia'], color = 'red', marker = 's')
        pyplot.xlabel("Tiempo Acumulado (m)")
        pyplot.ylabel("Distancia Acumulada (km)")
        pyplot.title("Distancia Acumulada vs Tiempo Acumulado")
        pyplot.grid(True)
        pyplot.show()
        
        pyplot.plot(camino1.registros['distancia'], camino1.registros['costo'], color = 'green', marker = 'o')
        pyplot.plot(camino2.registros['distancia'], camino2.registros['costo'], color = 'red', marker = 's')
        pyplot.xlabel("Distancia Acumulada (km)")
        pyplot.ylabel("Costo acumulado ($)")
        pyplot.title("Costo Acumulado vs Distancia Acumulada")
        pyplot.grid(True)
        pyplot.show()
    
        pyplot.plot(camino1.registros['tiempo'], camino1.registros['costo'], color = 'green', marker = 'o')
        pyplot.plot(camino2.registros['tiempo'], camino2.registros['costo'], color = 'red', marker = 's')
        pyplot.xlabel("Tiempo acumulado (m)")
        pyplot.ylabel("Costo acumulado ($)")
        pyplot.title("Costo Acumulado vs Tiempo Acumulado")
        pyplot.grid(True)
        pyplot.show()
        
    def crear_txt_con_optimos(self, solicitud, camino_tiempo_optimo, camino_costo_optimo, modo_escritura):
        with open("optimos.txt", modo_escritura) as archivo:
            archivo.write(f"Solicitud: {solicitud.id_carga} \n")
            if camino_costo_optimo and camino_tiempo_optimo:
                archivo.write("Camino con el minimo tiempo de entrega:\n")
                archivo.write(f'{camino_tiempo_optimo}\n')
                archivo.write("Camino con el minimo costo total:\n")
                archivo.write(f'{camino_costo_optimo}\n')
            else:
                archivo.write(f"No existen caminos que unan {solicitud.origen} y {solicitud.destino}")

            


 
    
                
                
                
        
        
        
        
        
        