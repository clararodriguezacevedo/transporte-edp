from Conexion import Conexion
from Nodo import Nodo
from Grafo import Grafo
from Solicitud import Solicitud

#########TODO: Hacer una clase leer_csv
import csv
def leer_csv_nodos(): # Crea una lista con todos los nodos
    try:
        with open("nodos.csv","r",encoding="utf-8",newline="") as archivo:
            archivo.readline()
            lector=csv.reader(archivo)
            ciudades=[]

            for fila in lector:
                nodo=Nodo(fila[0])
                ciudades.append(nodo)

            return ciudades # Devuelve una lista con todos los nodos

    except FileNotFoundError:
        print("No se encontro el archivo nodos")

def leer_csv_conexiones():
    ciudades=leer_csv_nodos() ########ver si esto lo hago en el main y se lo paso como parametro

    ####### TODO: GENERAR AUTOMATICAMENTE UN GRAFO PARA CADA MODO DE CONEXION
    grafos=[Grafo("Ferroviaria"),Grafo("Fluvial"),Grafo("Aerea"),Grafo("Automotor")] # Lista con los 4 grafos que tengo, uno por cada modo

    try:
        with open("./conexiones.csv","r",encoding="utf-8",newline="") as archivo:
            archivo.readline() # salteo la fila de los titulos
            lector=csv.reader(archivo)

            for fila in lector:
                nodo1 = next(n for n in ciudades if n.ciudad == fila[0]) # Toma los nodos generados anteriormente para que coincidan con los datos del csv
                nodo2 = next(n for n in ciudades if n.ciudad == fila[1])
                conexion=Conexion(nodo1,nodo2,fila[2],fila[3],fila[4],fila[5]) #creo la conexion

                for elemento in ciudades:
                    if elemento.ciudad==nodo1.ciudad: # Ver si puedo encontrar el nodo en la lista de otra forma
                        elemento.enlazar_conexion(conexion)
                    if elemento.ciudad==nodo2.ciudad:
                        elemento.enlazar_conexion(conexion)

                grafo=Grafo(fila[2]) # Agrego la conexion al grafo correspondiente, segun el modo
                for elemento in grafos:
                    if elemento==grafo:
                        elemento.enlazar_conexion_grafo(conexion)

            return ciudades, grafos # Devuelve la misma lista ciudad que leer_csv_nodos, pero ahora tienen enlazadas las conexiones, y la lista de los grafos

    except FileNotFoundError:
        print("No se encontro el archivo conexiones")

def leer_csv_solicitues(ciudades):
    try:
        with open("solicitudes.csv","r",encoding="utf-8",newline="") as archivo:
            archivo.readline()
            lector=csv.reader(archivo)
            origen = None
            destino = None
            for fila in lector: # Anidamos for loops, pero en realidad el primer nivel es una sola iteracion, porque la solicitud tiene una sola fila. Usamos readlline entonces hay que hacerlo por fila.
                for ciudad in ciudades:
                    if ciudad.ciudad == fila[2]:
                        origen = ciudad
                    if ciudad.ciudad == fila[3]:
                        destino = ciudad
                solicitud=Solicitud(fila[0],fila[1],origen, destino)

            return solicitud

    except FileNotFoundError:
        print("No se encontro el archivo.")

if __name__=="__main__":
    try:
        ciudades,grafos=leer_csv_conexiones()

        # para ver cada ciudad y sus conexiones
        # for elemento in ciudades:
        #     elemento.mostrar_info()
        #     print("")

        print("-----------------")

        #para ver cada grafo
        # for elemento in grafos:
        #     print("")
        #     elemento.__repr__()
        #     elemento.mostrar_info_grafo()

        solicitud = leer_csv_solicitues(ciudades)
        caminos = solicitud.construir_arbol()
        for camino in caminos:
            for n in camino:
                print(f"{n}, ", end="")
            print("\n")

    except ValueError as e:
        print(e)


