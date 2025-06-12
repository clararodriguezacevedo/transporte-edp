from Conexion import Conexion


class Nodo:
    def __init__(self,ciudad):
        self.ciudad=ciudad
        #self.conexiones={"Ferroviaria":[],"Fluvial":[],"Aerea":[],"Automotor":[]} #diccionario que incluye las conexiones que este nodo tiene, segun el modo
        #tal vez sea mejor poner distintos atributos? tipo self.ferroviaria, self.fluvial, etc EN ESTE ARCHIVO PRUEBO ESTO
        self.vecinos={"fluvial":[], "ferroviaria":[],"aerea":[],"automotor":[]}
        self.ferroviaria=[]
        self.fluvial=[]
        self.aerea=[]
        self.automotor=[]

    def __hash__(self):
        return hash(self.ciudad)

    def __str__(self):
        return self.ciudad

    def enlazar_conexion(self,conexion): #agrega la conexion segun el modo, al atributo correspondiente
        if not isinstance(conexion,Conexion):
            raise ValueError("No se ingreso una conexion")

        match conexion.modo:
            case "ferroviaria":
                self.ferroviaria.append(conexion)
                for nodo in conexion.tramo:
                    if nodo.ciudad != self.ciudad:
                        self.vecinos["ferroviaria"].append(nodo)
            case "fluvial":
                self.fluvial.append(conexion)
                for nodo in conexion.tramo:
                    if nodo.ciudad != self.ciudad:
                        self.vecinos["fluvial"].append(nodo)
            case "aerea":
                self.aerea.append(conexion)
                for nodo in conexion.tramo:
                    if nodo.ciudad != self.ciudad:
                        self.vecinos["aerea"].append(nodo)
            case "automotor":
                self.automotor.append(conexion)
                for nodo in conexion.tramo:
                    if nodo.ciudad != self.ciudad:
                        self.vecinos["automotor"].append(nodo)

    def mostrar_info(self): #muestra la ciudad del nodo, y todas sus conexiones
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

        # ############esto seguro se puede hacer mucho mejor, cambio hecho rapido
        # print("Modo Ferroviario: ")
        # if self.ferroviaria != []:
        #     for elemento in self.ferroviaria:
        #         print(elemento)
        # else:
        #     print("No hay conexiones en este modo.")
        # print("Modo Fluvial: ")
        # if self.fluvial != []:
        #     for elemento in self.fluvial:
        #         print(elemento)
        # else:
        #     print("No hay conexiones en este modo.")
        # print("Modo Aereo: ")
        # if self.aerea != []:
        #     for elemento in self.aerea:
        #         print(elemento)
        # else:
        #     print("No hay conexiones en este modo.")
        # print("Modo Automotor: ")
        # if self.automotor != []:
        #     for elemento in self.automotor:
        #         print(elemento)
        # else:
        #     print("No hay conexiones en este modo.")

    def __eq__(self,other): #dos nodos son iguales si son la misma ciudad (usado al leer conexiones.csv)
        if not isinstance(other,Nodo):
            raise ValueError(f"No se ingreso un nodo.")
        return self.ciudad==other.ciudad
