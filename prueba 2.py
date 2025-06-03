#PRUEBA CON DISTINTOS ATRIBUTOS EN EL NODO PARA CADA MODO

class Nodo:
    def __init__(self,ciudad):
        self.ciudad=ciudad
        #self.conexiones={"Ferroviaria":[],"Fluvial":[],"Aerea":[],"Automotor":[]} #diccionario que incluye las conexiones que este nodo tiene, segun el modo
        #tal vez sea mejor poner distintos atributos? tipo self.ferroviaria, self.fluvial, etc EN ESTE ARCHIVO PRUEBO ESTO
        self.ferroviaria=[]
        self.fluvial=[]
        self.aerea=[]
        self.automotor=[]
        
    def __str__(self):
        return f"Ciudad: {self.ciudad}"
    
    def enlazar_conexion(self,conexion): #agrega la conexion segun el modo, al atributo correspondiente
        if not isinstance(conexion,Conexion):
            raise ValueError("No se ingreso una conexion")

        ###########esto seguro se puede hacer mucho mejor, cambio hecho rapido
        if conexion.tipo=="Ferroviaria":
            self.ferroviaria.append(conexion)
        elif conexion.tipo=="Fluvial":
            self.fluvial.append(conexion)
        elif conexion.tipo=="Aerea":
            self.aerea.append(conexion)
        elif conexion.tipo=="Automotor":
            self.automotor.append(conexion)
    
    def mostrar_info(self): #muestra la ciudad del nodo, y todas sus conexiones
        print(f"Ciudad: {self.ciudad}")
        
        ############esto seguro se puede hacer mucho mejor, cambio hecho rapido
        print("Modo Ferroviario: ")
        if self.ferroviaria != []:
            for elemento in self.ferroviaria:
                print(elemento)
        else:
            print("No hay conexiones en este modo.")
        print("Modo Fluvial: ")
        if self.fluvial != []:
            for elemento in self.fluvial:
                print(elemento)
        else:
            print("No hay conexiones en este modo.")
        print("Modo Aereo: ")
        if self.aerea != []:
            for elemento in self.aerea:
                print(elemento)
        else:
            print("No hay conexiones en este modo.")
        print("Modo Automotor: ")
        if self.automotor != []:
            for elemento in self.automotor:
                print(elemento)
        else:
            print("No hay conexiones en este modo.")
        
    def __eq__(self,other): #dos nodos son iguales si son la misma ciudad (usado al leer conexiones.csv)
        if not isinstance(other,Nodo):
            raise ValueError("No se ingreso un nodo.")
        return self.ciudad==other.ciudad


class Conexion:
    def __init__(self,origen,destino,tipo,distancia,restriccion,valor_restriccion): #los datos del archivo
        self.tramo={origen,destino} #usamos un set para que, por ejemplo, el tramo Zarate-BsAs sea igual al tramo BsAs-Zarate, y asi con todos
        self.tipo=tipo
        self.distancia=distancia
        self.restriccion=restriccion
        self.valor_restriccion=valor_restriccion
    
    def __str__(self):
        return f"Conexion: {self.tramo}"


class Grafo:
    def __init__(self, modo): #############tal vez conviene no pasar el modo como atributo y hacer una clase grafo por cada modo (grafo_ferroviario, grafo_fluvial, etc.)
        self.modo=modo #cada modo (ferroviario, fluvial...) seria una instancia de grafo
        self.conexiones=[] #lista con las conexiones de ese modo (podria ser otra estructura)
    
    def __str__(self):
        return f"Este es el grafo {self.modo}"
    
    def mostrar_info_grafo(self):
        for elemento in self.conexiones:
            print(elemento)
    
    def enlazar_conexion_grafo(self,conexion): #agrega la conexion al grafo
        if not isinstance(conexion,Conexion):
            raise ValueError("No se ingreso una conexion")
        self.conexiones.append(conexion)
    
    def __eq__(self,other):
        if not isinstance(other,Grafo):
            raise ValueError("No se ingreso un grafo")
        return self.modo==other.modo
        
#########ver si hago una clase leer_csv
import csv
def leer_csv_nodos(): #crea una lista con todos los nodos
    try:
        with open("nodos.csv","r",encoding="utf-8",newline="") as archivo:
            archivo.readline()
            lector=csv.reader(archivo)
            ciudades=[]
            
            for fila in lector:
                nodo=Nodo(fila[0])
                ciudades.append(nodo)

            return ciudades #devuelve una lista con todos los nodos
        
    except FileNotFoundError:
        print("No se encontro el archivo")

def leer_csv_conexiones(): 
    ciudades=leer_csv_nodos() ########ver si esto lo hago en el main y se lo paso como parametro
    
    grafos=[Grafo("Ferroviaria"),Grafo("Fluvial"),Grafo("Aerea"),Grafo("Automotor")] #lista con los 4 grafos que tengo, uno por cada modo
    
    try:
        with open("conexiones.csv","r",encoding="utf-8",newline="") as archivo:
            archivo.readline() # salteo la fila de los titulos
            lector=csv.reader(archivo)
            
            for fila in lector:
                conexion=Conexion(fila[0],fila[1],fila[2],fila[3],fila[4],fila[5]) #creo la conexion
                nodo1=Nodo(fila[0]) #agrego la conexion al nodo de origen
                for elemento in ciudades:
                    if elemento==nodo1:#ver si puedo encontrar el nodo en la lista de otra forma
                        elemento.enlazar_conexion(conexion)
                nodo2=Nodo(fila[1]) #agrego la conexion al nodo de destino
                for elemento in ciudades:
                    if elemento==nodo2:
                        elemento.enlazar_conexion(conexion)
                
                grafo=Grafo(fila[2]) #agrego la conexion al grafo correspondiente, segun el tipo
                for elemento in grafos:
                    if elemento==grafo:
                        elemento.enlazar_conexion_grafo(conexion)
            
            return ciudades,grafos #devuelve la misma lista ciudad que leer_csv_nodos, pero ahora tienen enlazadas las conexiones, y la lista de los grafos

    except FileNotFoundError:
        print("No se encontro el archivo")

if __name__=="__main__":
    try:
        ciudades,grafos=leer_csv_conexiones() 
        
        #para ver cada ciudad y sus conexiones
        for elemento in ciudades:
            elemento.mostrar_info()
            print("")
        
        print("-----------------")
        
        #para ver cada grafo
        for elemento in grafos:
            print("")
            print(elemento)
            elemento.mostrar_info_grafo()
            
    except ValueError as e:
        print(e)
