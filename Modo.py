class Modo:
    
    def __init__(self, modo:str, velocidad, capacidad:float, costo_f,cperkm,cperkg):

        self.modo = modo
        self.velocidad=velocidad
        self.capacidad = capacidad
        self.costo_f=costo_f
        self.cperkg=cperkg
        self.cperkm=cperkm       
    
    # def __eq__(self,other):
    #     if not isinstance(self,other):
    #         raise ValueError("No se ingreso un modo")
        
    def __str__(self):
        return f'Es un modo {self.modo}'
    
    #Getters y Setters
    def get_modo(self):
        return self.modo
    
    def get_velocidad(self):
        return self.velocidad

    def get_capacidad(self):
        return self.capacidad



