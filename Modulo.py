# from Nodo import Nodo
# from Solicitud import Solicitud
# from Camino import Camino

def validar_numero(num):
        try:
            return float(num)
        except ValueError:
            raise ValueError("No se ingreso un numero")
        # else:
        #     return float(num)
