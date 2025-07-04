from Conexion import Conexion
import matplotlib.pyplot as plt
import networkx as nx
from Modulo import validar_modo

    
class Grafo:

    def __init__(self, modo): 
        self.modo=validar_modo(modo) #cada modo (ferroviario, fluvial...) seria una instancia de grafo
        self.conexiones=[] #lista con las conexiones de ese modo (podria ser otra estructura)

    def __str__(self):
        return f"Este es el grafo {self.modo}"

    def __repr__(self): #usamos networkx para hacer los grafos, despues los mostramos con matplotlib
        G = nx.Graph()
        for conexion in self.conexiones:
            nodo_a, nodo_b = tuple(conexion.tramo)
            nodo_a = nodo_a.ciudad.replace("_", " ")
            nodo_b = nodo_b.ciudad.replace("_", " ")
            G.add_node(nodo_a)
            G.add_node(nodo_b)
            G.add_edge(nodo_a, nodo_b, distancia=conexion.distancia)

        plt.figure(num="Grafos generados a partir de CSVs",figsize=(6, 4))

        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=800, edgecolors="black")
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
        nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
        # Preparamos las etiquetas de arista (edge labels) extrayendo el atributo 'distancia'
        edge_labels = nx.get_edge_attributes(G, 'distancia')
        # Dibujo de etiquetas sobre cada arista
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.5)  # label_pos controla dónde sobre la arista aparece el texto

        plt.axis("off")
        plt.title(self.modo.capitalize())
        plt.tight_layout()
        plt.show()

    def mostrar_info_grafo(self): #muestra la informacion del grafo y las conexiones que tiene
        print(f"Grafo {self.modo}: ")
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



