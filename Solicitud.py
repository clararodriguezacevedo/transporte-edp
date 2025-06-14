from Conexion import Conexion
from Modo import Modo
from Nodo import Nodo
import math
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from Modulo import validar_numero

class Solicitud:
    def __init__(self,id_carga,peso_kg,origen,destino):
        
        self.id_carga = id_carga
        self.peso_kg = validar_numero(peso_kg)
        self.origen = Solicitud.validar_nodo(origen)
        self.destino = Solicitud.validar_nodo(destino)

    def __str__(self):
        return f"Origen: {self.origen.ciudad, self.origen}. Destino: {self.destino.ciudad, self.destino}"

    @staticmethod
    def validar_nodo(nodo):
        if not isinstance(nodo, Nodo):
            raise ValueError('No has ingresado un Nodo')
        else:
            return nodo