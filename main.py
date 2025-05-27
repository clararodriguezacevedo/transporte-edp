class Nodo ():
    def __init__(self, nombre:str):
        self.nombre = nombre

    def __str__(self):
        return f'Ciudad: {self.nombre}'

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre


