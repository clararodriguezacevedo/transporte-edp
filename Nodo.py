from Conexion import Conexion

class Nodo:
    def __init__(self, ciudad, conexiones=None, vecinos=None):
        self.ciudad = ciudad
        self.conexiones = conexiones if conexiones is not None else {
            "ferroviaria": [],
            "fluvial": [],
            "aerea": [],
            "automotor": []
        }
        self.vecinos = vecinos if vecinos is not None else {
            "ferroviaria": [],
            "fluvial": [],
            "aerea": [],
            "automotor": []
        }


    def __hash__(self):
        return hash(self.ciudad)

    def __str__(self):
        return self.ciudad

    def enlazar_conexion(self,conexion): # Agrega la conexion segun el modo, a self.conexiones.modo
        if not isinstance(conexion,Conexion):
            raise ValueError("No se ingreso una conexion")

        self.conexiones[conexion.modo].append(conexion)
        for nodo in conexion.tramo:
            if nodo.ciudad != self.ciudad: # Busco el otro nodo en la conexion (que no es el actual) y lo agrego como vecino en el actual
                self.vecinos[conexion.modo].append(nodo)

    def mostrar_info(self): # Muestra la ciudad del nodo, y todas sus conexiones
        print(f"\nCiudad: {self.ciudad}")

        print("\nVecinos Ferroviarios: ")
        if self.vecinos["ferroviaria"] != []:
            for vecino in self.vecinos["ferroviaria"]:
                print(vecino.ciudad, end=", ")
        else:
            print("No hay vecinos en este modo.", end=", ")
        print("\nVecinos Fluviales: ")
        if self.vecinos["fluvial"] != []:
            for vecino in self.vecinos["fluvial"]:
                print(vecino.ciudad, end=", ")
        else:
            print("No hay vecinos en este modo.", end=", ")
        print("\nVecinos aereos: ")
        if self.vecinos["aerea"] != []:
            for vecino in self.vecinos["aerea"]:
                print(vecino.ciudad, end=", ")
        else:
            print("No hay vecinos en este modo.", end=", ")
        print("\nVecinos automotores: ")
        if self.vecinos["automotor"] != []:
            for vecino in self.vecinos["automotor"]:
                print(vecino.ciudad, end=", ")
        else:
            print("No hay vecinos en este modo.", end=", ")

    def __eq__(self,other): # Dos nodos son iguales si son la misma ciudad (usado al leer conexiones.csv)
        if not isinstance(other,Nodo):
            raise ValueError(f"No se ingreso un nodo")
        return self.ciudad.lower()==other.ciudad.lower()
