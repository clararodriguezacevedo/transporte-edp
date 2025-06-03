from Conexion import Conexion

class Grafo:
    modos_permitidos = {'ferroviaria', 'automotor', 'fluvial', 'aerea'}
    
    def __init__(self, modo): #############tal vez conviene no pasar el modo como atributo y hacer una clase grafo por cada modo (grafo_ferroviario, grafo_fluvial, etc.)
        self.modo=Grafo.validar_modo(modo) #cada modo (ferroviario, fluvial...) seria una instancia de grafo
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
        
    @classmethod
    def validar_modo(cls,modo):
        if modo.lower() in cls.modos_permitidos:
            return modo.lower()
        else:
            raise ValueError('No has ingresado un modo de conexion valido')
        