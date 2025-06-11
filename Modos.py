class Modo:
    def __init__(self,modo:str,cantidad_vehiculos:int,costo_tot:int,costo_f:int,cperkm:int,cperkg:int,tiempo:int):
        self.modo=modo
        self.cantidad_vehiculos=cantidad_vehiculos
        self.costo_tot=costo_tot
        self.costo_f=costo_f
        self.cperkg=cperkg
        self.cperkm=cperkm
        self.tiempo=tiempo
        
    
    def __eq__(self,other):
        if not isinstance(self,other):
            raise ValueError("No se ingreso un modo")
        
    def __str__(self):
        return f'Es un modo {self.modo}'
    


    
    


        
