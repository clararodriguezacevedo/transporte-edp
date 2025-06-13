class Camino():
    def __init__(self, modo:str, costo_total: float, tiempo_total: float, cantidad_vehiculos: int, conexiones: list):
        self.modo = modo
        self.costo_total = costo_total
        self.tiempo_total = tiempo_total
        self.cantidad_vehiculos = cantidad_vehiculos
        self.conexiones = conexiones
      
      
    def __str__(self):
        texto = f"\nModo: {self.modo} - Costo: {self.costo_total}, Tiempo: {self.tiempo_total} minutos, Cantidad vehiculos: {self.cantidad_vehiculos}\nCamino:\n"
        for nodo in self.conexiones:
            texto += f" - {nodo}\n"
        return texto
    