def validar_numero(num):
        try:
            float(num)
        except TypeError as e:
            print('No has ingresado un valor')
        else:
            return float(num)