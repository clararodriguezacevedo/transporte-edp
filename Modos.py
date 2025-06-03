class Modo:
    def __init__(self,modo:str,velocidad:int,capacidad:int,cf:int,cperkm:int,cperkg:int):
        self.modo=modo
        self.velocidad=velocidad
        self.capacidad=capacidad
        self.cf=cf
        self.cperkm=cperkm
        self.cperkg=cperkg
    
    def __eq__(self,other):
        if not isinstance(self,other):
            raise ValueError("No se ingreso un modo")
        
    def __str__(self):
        return f'Es un modo {self.modo}'
    