
from LectorCSV import LectorCSV
from Modo import Modo
from Itinerario import Itinerario
from Solicitud import Solicitud
from Interfaz import Interfaz

if __name__ == "__main__":
    try:
        # Crear instancia del lector
        lector = LectorCSV()

        # Leer datos desde los archivos CSV
        ciudades, grafos = lector.leer_conexiones()

        # # Mostrar informacion de cada ciudad y sus conexiones
        # print("\nInformacion de ciudades y conexiones:")
        # for ciudad in ciudades:
        #     ciudad.mostrar_info()
        #     print("")

        # # Mostrar informacion de cada grafo
        # print("\nInformacion de grafos:")
        # for grafo in grafos:
        #     print("")
        #     grafo.__repr__()
        #     grafo.mostrar_info_grafo()

        # Leer solicitud
        interfaz = Interfaz(ciudades)
        interfaz.crear_solicitud()

        # Dejar esta linea si se quiere calcular los costos con las solicitudes ingresadas en la interfaz
        lector.set_archivo_solicitudes("nuevas_solicitudes.csv") # Comentar esta linea si se quiere usar el archivo dado solicitudes.csv, que es el default

        solicitudes = lector.leer_solicitud(ciudades)

        # Definir configuracion de modos de transporte
        modos_config = {
            "ferroviaria": Modo("ferroviaria", 100, 150000, 100, [20, 15], 3),
            "automotor": Modo("automotor", 80, 30000, 30, 5, [1, 2]),
            "fluvial": Modo("maritima", 40, 100000, [500, 1500], 15, 2),
            "aerea": Modo("aerea", [600, 400], 5000, 750, 40, 10)
        }

        # Calcular costos y tiempos
        print("\nResultados de la solicitud:")
        for solicitud in solicitudes:
            print(f"Solicitud {solicitud.id_carga}: ")
            itinerario=Itinerario(solicitud)
            costos_y_tiempos = itinerario.calcular_costos_y_tiempos(modos_config)
            camino_tiempo_optimo, camino_costo_optimo = itinerario.optimos(costos_y_tiempos)            
            print(f'Camino con el minimo tiempo de entrega:\n{camino_tiempo_optimo}\nCamino con el minimo costo total:\n{camino_costo_optimo}')
            #itinerario.crear_graficos(camino_tiempo_optimo, camino_costo_optimo)
            if solicitud == solicitudes[0]:
                itinerario.crear_txt_con_optimos(solicitud, camino_tiempo_optimo, camino_costo_optimo,"w")
            else:
                itinerario.crear_txt_con_optimos(solicitud, camino_tiempo_optimo, camino_costo_optimo,"a")
        #solicitud.calcular_costos_y_tiempos(modos_config)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Excepcion no controlada: {e}")

