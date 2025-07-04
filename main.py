
from LectorCSV import LectorCSV
from Modo import Modo, Automotor, Aerea, Fluvial, Ferroviaria
from Itinerario import Itinerario
from Solicitud import Solicitud
from Interfaz import Interfaz
from Graficos import Grafico

if __name__ == "__main__":
    #try:
        # Crear instancia del lector
        # Por defecto utiliza "original", el archivo nodos, conexiones, y solicitudes de archivos_ejemplo/original
        nombre_carpeta = input("Elija que archivos de ejemplo quiere utilizar, o presione enter para utilizar los originales por defecto: ")
        lector = LectorCSV(nombre_carpeta if nombre_carpeta else "original") # Ingresando como parametro los nombres de las carpetas en archivos_ejemplo se puede elegir que ejemplo ejecutar 

        # Leer datos desde los archivos CSV
        ciudades, grafos = lector.leer_conexiones()

        # Mostrar informacion de cada ciudad y sus conexiones
        print("\nInformacion de ciudades y conexiones:")
        for ciudad in ciudades.values():
            ciudad.mostrar_info()
            print("")

        # Mostrar informacion de cada grafo
        print("\nInformacion de grafos:")
        for grafo in grafos.values():
            print("")
            grafo.mostrar_info_grafo()
            grafo.__repr__()   

        # Leer solicitud
        # Dejar estas lineas si se quiere calcular los costos con las solicitudes ingresadas en la interfaz
        # interfaz = Interfaz(ciudades)
        # interfaz.crear_solicitud()
        # lector.set_archivo_solicitudes("nuevas_solicitudes.csv") # Comentar esta linea si se quiere usar el archivo dado solicitudes.csv, que es el default

        solicitudes = lector.leer_solicitud(ciudades)

        # Definir configuracion de modos de transporte
        modos_config = {
            "ferroviaria": Ferroviaria(100, 150000, 100, [20, 15], 3),
            "automotor": Automotor(80, 30000, 30, 5, [1, 2]),
            "fluvial": Fluvial(40, 100000, [500, 1500], 15, 2),
            "aerea": Aerea([600, 400], 5000, 750, 40, 10)
        }

        # Calcular costos y tiempos
        print("\nResultados de la solicitud:")
        for solicitud in solicitudes:
            print(f"Solicitud {solicitud.id_carga}: ")
            itinerario=Itinerario(solicitud, ciudades)
            costos_y_tiempos = itinerario.calcular_costos_y_tiempos(modos_config)
            camino_tiempo_optimo, camino_costo_optimo, camino_max_puntos_interes = itinerario.optimos(costos_y_tiempos)    
            
            if camino_costo_optimo and camino_tiempo_optimo and camino_max_puntos_interes:     
                print(f'Camino con el minimo tiempo de entrega:\n{camino_tiempo_optimo}\nCamino con el minimo costo total:\n{camino_costo_optimo}\nCamino con la maxima cantidad de puntos de interes:\n{camino_max_puntos_interes}')
                Grafico.crear_graficos(camino_tiempo_optimo, camino_costo_optimo)            
                Grafico.graficar_frecuencia_ciudades(itinerario)            
                Grafico.comparacion_modos_grafico(itinerario, modos_config, costos_y_tiempos)
            else:
                print(f"No existen caminos que unan {solicitud.origen} y {solicitud.destino}")

            if solicitud == solicitudes[0]:
                itinerario.crear_txt_con_optimos(solicitud, camino_tiempo_optimo, camino_costo_optimo,camino_max_puntos_interes,"w")
            else:
                itinerario.crear_txt_con_optimos(solicitud, camino_tiempo_optimo, camino_costo_optimo,camino_max_puntos_interes,"a")
            

    # except ValueError as e:
    #     print(f"Error: {e}")
    # except FileNotFoundError as e:
    #     print(f"Error: {e}")
    # except Exception as e:
    #     print(f"Excepcion no controlada: {e}")

