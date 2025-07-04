modos_permitidos = ('ferroviaria', 'automotor', 'fluvial', 'aerea')  #Usamos una tupla porque es inmutable


def validar_numero(num):
        try:
            return float(num)
        except ValueError:
            raise ValueError("No se ingreso un numero")


def validar_modo(modo):
    modos_permitidos = {'ferroviaria', 'automotor', 'fluvial', 'aerea'}
    if modo.lower() in modos_permitidos:
        return modo.lower()
    else:
        raise ValueError('No has ingresado un modo de conexion valido')