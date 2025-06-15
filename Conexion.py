from Modulo import validar_numero
from Modulo import modos_permitidos

class Conexion:
    restricciones_permitidas = {'velocidad_max', 'peso_max', 'prob_mal_tiempo', 'tipo'}

    def __init__(self,origen,destino,modo,distancia,restriccion,valor_restriccion): #los datos del archivo
        self.origen=origen
        self.destino=destino
        self.tramo={origen,destino} #usamos un set para que, por ejemplo, el tramo Zarate-BsAs sea igual al tramo BsAs-Zarate, y asi con todos
        self.modo= Conexion.validar_modo(modo)
        self.distancia= validar_numero(distancia)
        self.restriccion= Conexion.validar_restriccion(restriccion)
        self.valor_restriccion= self.valor_restriccion_valido(valor_restriccion)
        
    def __str__(self):
        return f"Conexion: {self.origen.ciudad} - {self.destino.ciudad}." 

    @classmethod
    def validar_restriccion(cls,restriccion):
        if restriccion == "":
            return None
        elif restriccion in cls.restricciones_permitidas:
            return restriccion
        else:
            raise ValueError(f'No has ingresado una restriccion valida: {restriccion}')

    @classmethod
    def validar_modo(cls,modo):
        if modo.lower() in modos_permitidos:
            return modo.lower()
        else:
            raise ValueError(f'No has ingresado un modo de conexion valido: {modo}')
    
    @staticmethod
    def valor_restriccion_valido(valor):
        try:
            return float(valor)
        except ValueError:
            return valor
