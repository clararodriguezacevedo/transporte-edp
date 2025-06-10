from Conexion import Conexion
import matplotlib.pyplot as plt
import networkx as nx

# class Nodo_:
#     def __init__(self,conexion):
#         self.conexion = conexion   #instancia de conexion
#         self.siguiente = None
      
    
class Grafo:
    modos_permitidos = {'ferroviaria', 'automotor', 'fluvial', 'aerea'}

    def __init__(self, modo): #############tal vez conviene no pasar el modo como atributo y hacer una clase grafo por cada modo (grafo_ferroviario, grafo_fluvial, etc.)
        self.modo=Grafo.validar_modo(modo) #cada modo (ferroviario, fluvial...) seria una instancia de grafo
        self.conexiones=[] #lista con las conexiones de ese modo (podria ser otra estructura)

    # def __str__(self):
    #     return f"Este es el grafo {self.modo}"

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


    def mostrar_info_grafo(self):
        for elemento in self.conexiones:
            print(elemento)

    # def enlazar_conexion_grafo(self,conexion): #agrega la conexion al grafo
    #     if not isinstance(conexion,Conexion):
    #         raise ValueError("No se ingreso una conexion")
        
        
    #     nuevo_nodo = Nodo(conexion)          #Creamos un nuevo nodo con la conexion
        
    #     if self.primero is None:
    #         self.primero = nuevo_nodo     # Primer conexion de la lista
    #     else:
    #         actual = self.primero         # 
    #         while actual.siguiente:       # Mientras el ultimo no sea None
    #             actual = actual.siguiente 
    #         actual.siguiente = nuevo_nodo    
    
    # def _construir_adyacencias(self):
    #     adyacencias = {}
    #     for conexion in self.conexiones:
    #         nodo1, nodo2 = tuple(conexion.tramo)
    #         distancia = conexion.distancia

    #         adyacencias.setdefault(nodo1, {})[nodo2] = distancia
    #         adyacencias.setdefault(nodo2, {})[nodo1] = distancia

    #     for nodo,vecinos in adyacencias:
    #         print(f"{nodo.ciu} se conecta con:")
    #         for vecino, distancia in vecinos.items():
    #             print(f"  - {vecino.id} a {distancia} km")

    def enlazar_conexion_grafo(self,conexion): #agrega la conexion al grafo
        if not isinstance(conexion,Conexion):
            raise ValueError("No se ingreso una conexion")
        self.conexiones.append(conexion)

    def __eq__(self,other):
        if not isinstance(other,Grafo):
            raise ValueError("No se ingreso un grafo")
        return self.modo==other.modo

    @classmethod
    def validar_modo(cls,modo):
        if modo.lower() in cls.modos_permitidos:
            return modo.lower()
        else:
            raise ValueError('No has ingresado un modo de conexion valido')


