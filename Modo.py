import random

class Modo:
    def __init__(self, capacidad:float):
        self.capacidad = capacidad
        
    def __str__(self):
        return f'Es un modo {self.modo}'
    
    def aplicar_restricciones(self, conexion, itinerario):
        pass
    

class Ferroviaria(Modo):
    def __init__(self, velocidad:float, capacidad:float, costo_f:float, cperkm: list, cperkg:float):
        super().__init__(capacidad)
        self.velocidad = velocidad
        self.costo_f = costo_f
        self.cperkm = cperkm
        self.cperkg = cperkg
    
    def aplicar_restricciones(self, conexion, itinerario):
        cperkm = self.cperkm[0 if conexion.distancia < 200 else 1]
        velocidad = self.velocidad
        if conexion.restriccion:
            velocidad = conexion.valor_restriccion
        return velocidad,cperkm,self.cperkg,self.costo_f

class Automotor(Modo):
    def __init__(self, velocidad:float, capacidad:float, costo_f:float, cperkm:float, cperkg:list):
        super().__init__(capacidad)
        self.velocidad = velocidad
        self.costo_f = costo_f
        self.cperkm = cperkm
        self.cperkg = cperkg
        
    def aplicar_restricciones(self, conexion, itinerario):
        vehiculos_con_peso_max = int(itinerario.solicitud.peso_kg // self.capacidad)
        peso_vehiculo_restante= itinerario.solicitud.peso_kg-vehiculos_con_peso_max*self.capacidad
        carga_vehiculos = [self.capacidad] * vehiculos_con_peso_max
        if peso_vehiculo_restante != 0:
            carga_vehiculos.append(peso_vehiculo_restante) 
        cperkgs_vehiculos = [self.cperkg[0 if n < 15000 else 1] for n in carga_vehiculos]
        cperkg = sum(c * kg for c, kg in zip(cperkgs_vehiculos, carga_vehiculos)) / itinerario.solicitud.peso_kg
        return self.velocidad,self.cperkm,cperkg,self.costo_f

class Fluvial(Modo):
    def __init__(self, velocidad:float, capacidad:float, costo_f:list, cperkm:float, cperkg:float):
        super().__init__(capacidad)
        self.velocidad = velocidad
        self.costo_f = costo_f
        self.cperkm = cperkm
        self.cperkg = cperkg
    
    def aplicar_restricciones(self, conexion, itinerario):
        costo_f = self.costo_f[0 if conexion.valor_restriccion == "fluvial" else 1]
        return self.velocidad,self.cperkm,self.cperkg,costo_f
        

class Aerea(Modo):
    def __init__(self, velocidad:list, capacidad:float, costo_f:float, cperkm:float, cperkg:float):
        super().__init__(capacidad)
        self.velocidad = velocidad
        self.costo_f = costo_f
        self.cperkm = cperkm
        self.cperkg = cperkg
    
    def aplicar_restricciones(self, conexion,itinerario):
        # conexion.valor_restriccion se asume como probabilidad de mal tiempo
        if conexion.valor_restriccion:
            probabilidad = conexion.valor_restriccion
        else:
            probabilidad = 0.0
        velocidad = self.velocidad[1] if random.random() < probabilidad else self.velocidad[0]
        return velocidad,self.cperkm,self.cperkg,self.costo_f
        

