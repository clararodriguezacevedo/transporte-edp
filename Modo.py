class Modo:
    def __init__(self, modo:str, velocidad, capacidad:float, costo_f,cperkm,cperkg):
        self.modo = modo
        self.velocidad=velocidad
        self.capacidad = capacidad
        self.costo_f=costo_f
        self.cperkg=cperkg
        self.cperkm=cperkm       
        
    def __str__(self):
        return f'Es un modo {self.modo}'
    



