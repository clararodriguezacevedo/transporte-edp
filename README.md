# transporte-edp
Clase Lector CSV: Esta clase lee los archivos nodos.csv, conexiones.csv, y solicitudes.csv. El producto es una lista de objetos Nodos con Conexiones enlazadas y una lista de Grafos por modo, al igual que una cola de objetos Solicitud. Usamos una cola para que las Solicitudes luego se procesen en el orden en el que se ingresaron.

Clase Interfaz: Al instanciar esta clase, el usuario puede ingresar la cantidad de solicitudes que quiera procesar, al igual que las solicitudes mismas. Para cada solicitud, se ingresa y valida origen, destino y cantidad de kilogramos. Para hacerlo, utilizamos tkinter. De todos modos, desde el main se puede optar por ignorar la interfaz y procesar una solicitud por defecto, proveniente de un CSV pregenerado.

Clase Nodo: Una clase que tiene como atributos el nombre de la ciudad, las Conexiones en un diccionario ordenado por modo de transporte, y los Nodos vecinos en otro diccionario ordenado por modo de transporte. 
Se genera una instancia por cada ciudad, al leer el archivo de Nodos. Cada Nodo contiene a sus Nodos vecinos, y a las Conexiones de cada modo con las que está enlazado.

Clase Conexion: Una clase que contiene el origen, el destino, el modo de transporte, la distancia en kilómetros, la restricción y el valor de la restricción (si efectivamente tiene una restricción) de una Conexión. 
Las instancias se generan al leer Conexiones.csv. Los Nodos de cada ciudad de origen y destino se enlazan al generar la Conexión. Luego, la Conexión se almacena a sí misma dentro de cada Nodo. (si efectivamente tiene una restricción) de una Conexión. El tramo está representado como un set de Nodos (no tienen orden, entonces Azul-Junín es igual a Junín-Azul)

Clase Grafo: Clase que permite crear distintos Grafos por modo de transporte. Las Conexiones por modo de transporte se van enlazando en el Grafo al leer conexiones.csv en la clase LectorCSV.

Clase Solicitud: Una vez que ya se hayan creado los Nodos de cada ciudad, sus Conexiones y que se hayan creado los Grafos por tipo de transporte, se lee el archivo solicitudes.csv o se ingresan mediante la interfaz las distintas solicitudes y se crea un objeto Solicitud por cada una. Cada solicitud tiene un Id de Carga, un peso en kg que se quiere transportar, un objeto Nodo de origen y un objeto Nodo de destino.

Clase Modo: Cada instancia de esta clase contiene de atributos el modo de transporte, la velocidad máxima, la  capacidad máxima, el costo fijo, el costo por kilómetro y el costo por kilogramo de cada diferente modo de transporte.

Clase Camino: Una clase que contiene de atributos el modo de transporte, el costo total del camino, el tiempo total, la cantidad de vehículos necesaria para realizar ese Camino, una lista con las Conexiones que forman el Camino, y un diccionario con los registros de las 

Clase Itinerario: Cada objeto Itinerario tiene como atributos a un objeto Solicitud, a un objeto Camino con el tiempo óptimo y a un objeto Camino con el costo óptimo (que son None hasta que se hayan encontrado mediante las funciones de la clase). 

La clase Itinerario tiene un método recursivo construir_arbol, que busca todos los caminos posibles entre la ciudad de origen y la ciudad de destino, usando un modo de transporte específico.
Para lograrlo, utiliza una búsqueda en profundidad (DFS). Recorre los Nodos partiendo desde el origen y va guardando tanto los Nodos visitados como las Conexiones (tramos) recorridas. Si llega al destino, guarda ese camino.
En cada paso, evita volver a visitar nodos ya recorridos para no generar ciclos. Si un vecino es válido, continúa la búsqueda desde allí. Cuando finaliza una rama del recorrido, retrocede para intentar otros caminos.
Al finalizar, devuelve una lista con todos los caminos posibles representados como listas de Conexiones.

La clase Itinerario tiene un método “privado” _calcular_costo_tiempo_camino, que calcula el costo total y el tiempo total de cada camino y también devuelve los costos, tiempos, y distancias acumulados para realizar los gráficos.

También contiene calcular_costos_y_tiempos, que recibe un diccionario con la información de cada modo de transporte (con sus restricciones). Teniendo en cuenta la solicitud actual, llama a construir_arbol para generar todos los caminos necesarios. Luego, utiliza _calcular_costo_tiempo_camino con cada uno. 

Gráficos: La clase Itinerario tiene una función óptimos que recibe esa lista de Caminos y encuentra el Camino con el tiempo y el costo óptimo. Asimismo, la función crear_gráficos  tiene los gráficos informativos correspondientes y la función crear_txt_con_optimos genera un “optimos.txt” con la información de los Caminos óptimos. 
Por otro lado, mediante la función comparacion_modos se colectan los costos totales y tiempos totales que se generan para cada una de las posibilidades de la solicitud. 
Luego, se utiliza la función comparacion_modos_grafico para visualizar estos datos mediante un gráfico de barras. De esta manera, conociendo las rutas de cada uno de los modos, el usuario puede observar cual es el más costoso y el más lento. 










