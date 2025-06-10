
class Solicitud:
    def __init__(self,id_carga,peso_kg,origen,destino):
        # self.ciudades = ciudades
        self.id_carga = id_carga
        self.peso_kg = peso_kg
        self.origen = origen ## TODO: Validar todos los parametros de las clases
        self.destino = destino
        
        # origen = self.verificar_ubicacion(self.ciudades, origen)
        # destino = self.verificar_ubicacion(self.ciudades, destino)
        # if not origen:
        #     raise ValueError('No has ingresado un origen existente')
        # if not destino:
        #     raise ValueError('No has ingresado un destino existente')
    
    def __str__(self):
        return f"Origen: {self.origen.ciudad, self.origen}. Destino: {self.destino.ciudad, self.destino}"
    
    def verificar_modos(self):
        pass

    def verificar_ubicacion(ciudades, ubicacion):
        for elemento in ciudades:
            if elemento.ciudad == ubicacion:
              return elemento.ciudad
        return False
    
    def construir_arbol(self):
        caminos = []

        def dfs(actual, camino, visitados):
            visitados.add(actual)
            camino.append(actual)

            if actual == self.destino:
                caminos.append(list(camino))  # Copiamos el camino actual
            else:
                for vecino in actual.vecinos["automotor"]:
                    if vecino not in visitados:
                        dfs(vecino, camino, visitados)

            # Backtrack
            camino.pop()
            visitados.remove(actual)

        dfs(self.origen, [], set())
        print(caminos)
        return caminos
        


    
        
    
 