"""
        ASIGNATURA: Inteligencia Artificial
        TRABAJO: Práctica 1
        CURSO: 2022-2023
        AUTORES: Mario Ventura & Luis Miguel Vargas
        Grado en Ingeniería Informática (GIN3)
"""


from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio

"""
========================================================================================================================
                                    BÚSQUEDA MEDIANTE RECORRIDO EN AMPLITUD
========================================================================================================================
"""
nombre_agente = "Mario"

class Estado:

    # Constructor init
    def __init__(self, posPizza, posAgente, posPared, padre=None):
        self.__posPizza = posPizza
        self.__posAgente = posAgente
        self.__posPared = posPared
        self.__padre = padre

    def __hash__(self):
        return hash(tuple(self.__posAgente))

    def __eq__(self, other):
        return self.getposAg() == other.getposAg()

    def getposAg(self):
        return self.__posAgente

    def __lt__(self, other):
        return False

    @property
    def padre(self):
        return self.__padre

    @padre.setter
    def padre(self, value):
        self.__padre = value

    # Función para detectar si la posicion del agente coincide con la posición de la pizza
    def es_meta(self) -> bool:
        return (self.__posAgente[nombre_agente][0] == self.__posPizza[0]) and (
                self.__posAgente[nombre_agente][1] == self.__posPizza[1])

    # Función para ver si se trata de una casilla valida o de una pared
    def es_valido(self) -> bool:
        # Iteración para comprobar si la posición coincidiria con la de una pared
        for pared in self.__posPared:
            if (self.__posAgente[nombre_agente][0] == pared[0]) and (self.__posAgente[nombre_agente][1] == pared[1]):
                return False
        # Devuelve True si la posición está dentro del tablero
        return 0 <= self.__posAgente[nombre_agente][0] <= 7 and 0 <= self.__posAgente[nombre_agente][1] <= 7

    # Función que genera todos los estados hijo de un estado n a partir de los posibles movimientos en n
    def genera_hijos(self):
        # Lista de hijos del estado actual
        hijos = []

        # --> ESTADOS HIJO FRUTO DE UN MOVIMIENTO SIMPLE
        movimientos = {"DRETA": (self.__posAgente[nombre_agente][0] + 1, self.__posAgente[nombre_agente][1]),
                  "ESQUERRE": (self.__posAgente[nombre_agente][0] - 1, self.__posAgente[nombre_agente][1]),
                  "DALT": (self.__posAgente[nombre_agente][0], self.__posAgente[nombre_agente][1] - 1),
                  "BAIX": (self.__posAgente[nombre_agente][0], self.__posAgente[nombre_agente][1] + 1)}
        # Obtención de claves para crear los estados hijos y añadirlos a la lista
        claves = list(movimientos.keys())
        for c in claves:
            # Crear nuevo estado hijo
            estado_hijo = ((Estado(self.__posPizza, {nombre_agente: movimientos[c]}, self.__posPared,
                                     (self, (AccionsRana.MOURE, Direccio.__getitem__(c))))))
            # Si el estado es valido se añade
            if estado_hijo.es_valido():
                hijos.append(estado_hijo)     #Hijo añadido


        # --> ESTADOS HIJO FRUTO DE UN SALTO
        saltos = {"DRETA": (self.__posAgente[nombre_agente][0] + 2, self.__posAgente[nombre_agente][1]),
                 "ESQUERRE": (self.__posAgente[nombre_agente][0] - 2, self.__posAgente[nombre_agente][1]),
                 "DALT": (self.__posAgente[nombre_agente][0], self.__posAgente[nombre_agente][1] - 2),
                 "BAIX": (self.__posAgente[nombre_agente][0], self.__posAgente[nombre_agente][1] + 2)}
        # Obtención de claves para crear los estados hijos y añadirlos a la lista
        claves = list(saltos.keys())
        for c in claves:
            # Crear nuevo estado hijo
            estado_hijo = ((Estado(self.__posPizza,  {nombre_agente: saltos[c]}, self.__posPared,
                                     (self, (AccionsRana.BOTAR, Direccio.__getitem__(c))))))
            # Si el estado es valido se añade
            if estado_hijo.es_valido():
                hijos.append(estado_hijo)     #Hijo añadido

        # Devolver la lista de hijos creada
        return hijos


class Rana(joc.Rana):

    # Constructor init
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None
        self.__turnos_espera = 0

    def pinta(self, display):
        pass

    # Presentación por consola
    def presentacion(self):
        print("=====================================")
        print("======= RECORRIDO EN AMPLITUD =======")
        print("=====================================\n")

    # Para limpiar la consola
    def clearScreen(self):
        idx = 50
        while (idx > 0):
            print("\n")
            idx-=1

    """
    RECIBE ----> Estado actual del agente en el entorno
    DEVUELVE --> void (simplemente usa las listas de abiertos y cerrados)
    HACE ------> Busqueda una forma de llegar hasta la solución (llegar a donde se encuentra la pizza)
                sin tener en cuenta el peso de las acciones ni la existencia de heurísticas o caminos mejores
    """
    def _busqueda(self, estado):
        self.__abiertos = []
        self.__cerrados = set()
        estado_actual = None

        self.__abiertos.append(estado)

        while self.__abiertos:
            estado_actual = self.__abiertos.pop(0)
            self.__abiertos = self.__abiertos[1:]

            if estado_actual in self.__cerrados:
                continue

            if not estado_actual.es_valido():
                self.__cerrados.add(estado_actual)
                continue

            estados_hijos = estado_actual.genera_hijos()

            if estado_actual.es_meta():
                break

            for hijo in estados_hijos:
                self.__abiertos.append(hijo)
            self.__cerrados.add(estado_actual)

        if estado_actual.es_meta():
            acciones = []
            it = estado_actual

            while it.padre is not None:
                padre, accion = it.padre
                acciones.append(accion)
                it = padre
            self.__acciones = acciones
            return True

    """
        RECIBE ----> Percepción del agente
        DEVUELVE --> Acción que debe hacer el agente
        HACE ------> Sigue la información almacenada en la lista de abiertos y hace uso de ella (hace uso también
                    de la lista de cerrados) para devolver la acción que debería seguir la rana para 
                    seguir el camino encnontrado hacia la solución.
        """
    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estado = Estado(percep[ClauPercepcio.OLOR], percep[ClauPercepcio.POSICIO], percep[ClauPercepcio.PARETS],
                        padre=None)

        # Buscar un camino a la solucion si todavia no se ha hecho
        if self.__acciones is None:
            self._busqueda(estado)
            self.clearScreen()
            self.presentacion()
            #print(self.__acciones)

        # Comprobar si quedan acciones por hacer (si aun hay acciones en la lista)
        if self.__acciones:
            # Si turno > 0 significa que se ha saltado recientemente y se debe esperar
            if self.__turnos_espera > 0:
                self.__turnos_espera -= 1
                print("La rana " + nombre_agente + " espera")
                return AccionsRana.ESPERAR
            else:
                acciones_list = self.__acciones.pop()

                if acciones_list[0] == AccionsRana.MOURE:
                    print("La rana " + nombre_agente + " se desplaza")
                    return acciones_list[0], acciones_list[1]
                elif acciones_list[0] == AccionsRana.BOTAR:
                    self.__turnos_espera = 2
                    print("La rana " + nombre_agente + " salta")
                    return acciones_list[0], acciones_list[1]
        else:
            # Solo se entra en esta condición una vez ya no hay acciones por hacer, cosa que solo sucede
            # si ya se ha llegado hasta la pizza
            print("La rana " + nombre_agente + " espera porque no hay pizza para comer >:( ")
            return AccionsRana.ESPERAR