"""
        ASIGNATURA: Inteligencia Artificial
        TRABAJO: Práctica 1
        CURSO: 2022-2023
        AUTORES: Mario Ventura & Luis Miguel Vargas
        Grado en Ingeniería Informática (GIN3)
"""

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

"""
========================================================================================================================
                                    BÚSQUEDA MEDIANTE ALGORITMO MINIMAX
========================================================================================================================
"""

# Límite de profundidad que permitirá reducir el coste computacional y el tiempo de ejecución
LIMITE_MAX_PROFUNDIDAD = 4

class Estado:

    # Constructor init
    def __init__(self, posPizza, posAgentes, paredes, nombre, peso=0, pare=None):
        self.__posicion_agentes = posAgentes
        self.__posPizza = posPizza
        self.__nombreMax = nombre
        self.__paredes = paredes
        self.__peso = peso
        self.__pare = pare
    def __eq__(self, other):
        return self.__posicion_agentes == other.getPos_agente()
    def __lt__(self, other):
        return False
    def __hash__(self):
        return hash(tuple(self.__posicion_agentes))

    @property
    def pare(self):
        return self.__pare
    @pare.setter
    def pare(self, value):
        self.__pare = value

    # Evaluación de los estados
    def evaluar(self, clave):
        return self.es_meta(clave), self.calcular_puntuacion(clave)
    def es_meta(self, clave):
        return ((self.__posicion_agentes[clave][0] == self.__posPizza[0]) and (
                self.__posicion_agentes[clave][1] == self.__posPizza[1]))
    """
    Esta función retorna un booleano que indica si un estado es válido. La función es exactamente la misma que en los
    otros algoritmos implementados en el sentido de las comprobaciones que se hacen. Se comprueba si la posicion
    no coincide con la de una pared, si la posicion no se sale del tablero.
    Sin embargo, ahora debemos tener en cuenta la existencia de 2 o más agentes sobre el tablero, lo cuál no solo
    complica las comprobaciones mencionadas, sino que además introduce una nueva comprobación a tener en cuenta:
    Comprobar que las dos posiciones de los agentes no coincidan ya que no pueden estar ambas en la misma casilla.
    """
    def es_valido(self):

        # Obtener el índice del adversario para poder hacer las comprobaciones
        clave = self.getPos_adversario()

        """
        Comprobar que los dos agentes se encuentren en posiciones diferentes. Deben estar en posiciones (x,y) diferentes,
        aunque pueden compartir una fila o una columna pero no ambas.
        """
        # COMPROBAR FILA
        if (self.__posicion_agentes[clave][0] == self.__posicion_agentes[self.__nombreMax][0]):
            # SI LA FILA ES LA MISMA, COMPROBAR QUE LA COLUMNA NO LO SEA
            if (self.__posicion_agentes[clave][1] == self.__posicion_agentes[self.__nombreMax][1]):
                return False
        # Comprobar si alguno de los agentes se encuentra en una posición en la que hay una pared
        for pared_iteracion in self.__paredes:
            if ((self.__posicion_agentes[clave][0] == pared_iteracion[0]) and (self.__posicion_agentes[clave][1] == pared_iteracion[1])):
                return False
        # Comprobar si la posoción se encuentra dentro del tablero y no excede los límites
        return (self.__posicion_agentes[clave][0] <= 7) and (self.__posicion_agentes[clave][0] >= 0) \
               and (self.__posicion_agentes[clave][1] <= 7) and (self.__posicion_agentes[clave][1] >= 0)

    # Getters
    def getPos_agente(self):
        return self.__posicion_agentes
    def getPos_adversario(self):
        claves = list(self.__posicion_agentes.keys())
        for indice in range(2):
            if (self.__nombreMax != claves[indice]):
                return claves[indice]
            #Posibilidad de que no se devuelva nada
        return None

    # Calcular la distancia entre el agente y la pizza
    def calcular_distancia_pizza(self, clave):
        distancia_acumulada = 0
        for idx in range(2):
            distancia_acumulada += abs(self.__posPizza[idx] - self.__posicion_agentes[clave][idx])
        # Devolver la distancia acumulada
        return distancia_acumulada

    # Calcular la puntuación de un agente (saber si va ganando o no)
    def calcular_puntuacion(self, clave):
        # Obtener las claves a modo de lista
        claves = list(self.__posicion_agentes.keys())
        # Calcular puntuaciones
        if (clave == claves[0]):
            # Caso 1: mayor que 0
            puntuacion_agente = self.calcular_distancia_pizza(claves[1]) - self.calcular_distancia_pizza(claves[0])
        else:
            puntuacion_agente = self.calcular_distancia_pizza(claves[0]) - self.calcular_distancia_pizza(claves[1])
        return puntuacion_agente

    # Generación de estados hijo dado un estado actual
    def genera_hijos(self):

        """
        Genera todos los posibles estados hijo a partir de un estado dado. Dado el estado inicial, esta función desplegará
        todos los estados del juego y sus hijos de estos. Sobre estos hijos se vuelve a aplicar la misma operación de
        generación de hijos, etc...
        Estos estados hijos se hacen teniendo en cuenta las posibles acciones que puede hacer el agente en el estado
        nuevo_estado_hijo en el que se encuentre y las posibles direcciones en las que las pueda hacer.
        """
        # Lista de estados hijos
        hijos = []
        # Obtener la posicion del agente adversario
        posicion_adversario = self.getPos_adversario()

        # ---------> ESTADOS HIJO QUE NACEN FRUTO DE UN DESPLAZAMIENTO NORMAL DE 1 CASILLA
        movimientos_simples = {"ESQUERRE": (-1, 0),
                                "DRETA": (+1, 0),
                                "DALT": (0, -1),
                                "BAIX": (0, +1)}
        claves_movimientos = list(movimientos_simples.keys())   # Claves de la lista
        # Generación de los estados hijos
        for accion,direccion in enumerate(movimientos_simples.values()):
            # Suma de coordenadas usando la funcion zip de python
            coordenadas = [sum(tup) for tup in zip(self.__posicion_agentes[self.__nombreMax], direccion)]
            # Copiamos las coordenadas obtenidas del agente y actualizamos las del que se ha movido
            copia_coordenadas = self.__posicion_agentes.copy()
            copia_coordenadas[self.__nombreMax] = coordenadas

            # Generación de un nuevo objeto estado que será el estado hijo
            nuevo_estado_hijo = Estado(self.__posPizza, copia_coordenadas, self.__paredes, posicion_adversario, 0,
                            (self, (AccionsRana.MOURE, Direccio.__getitem__(claves_movimientos[accion]))))
            # Si el nuevo estado hijo generado es válido, se añade a la lista de hijos
            if (nuevo_estado_hijo.es_valido()):
                # Añadir a la lista
                hijos.append(nuevo_estado_hijo)



        # ---------> ESTADOS HIJO QUE NACEN FRUTO DE UN SALTO DE 2 CASILLAS
        movimientos_salto = {"ESQUERRE": (-2, 0),
                "DRETA": (+2, 0),
                "DALT": (0, -2),
                "BAIX": (0, +2)}
        # Generación de los estados
        for accion, direccion in enumerate(movimientos_salto.values()):
            # Suma de coordenadas usando la funcion zip de python
            coordenadas = [sum(tup) for tup in zip(self.__posicion_agentes[self.__nombreMax], direccion)]
            # Copiamos las coordenadas obtenidas del agente y actualizamos las del que se ha movido
            copia_coordenadas = self.__posicion_agentes.copy()
            copia_coordenadas[self.__nombreMax] = coordenadas

            # Generación de un nuevo objeto estado que será el estado hijo
            nuevo_estado_hijo = Estado(self.__posPizza, copia_coordenadas, self.__paredes, posicion_adversario, 0,
                                (self, (AccionsRana.BOTAR, Direccio.__getitem__(claves_movimientos[accion]))))
            # Si el nuevo estado hijo generado es válido, se añade a la lista de hijos
            if (nuevo_estado_hijo.es_valido()):
                # Añadir a la lista
                hijos.append(nuevo_estado_hijo)

        # Devolver los hijos generados
        return hijos


class Rana(joc.Rana):

    #
    HAY_SOLUCION = False

    # Constructor init
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.turnos_espera = 0      # Establece los turnos de espera que quedan si la rana salta

    def pinta(self, display):
        pass

    # Función que implementa el funcionamiento de un algoritmo Minimax
    def miniMax(self, estado, nivel_profundidad, turno_MAX = True):
        """
        Evalua el estado recibido por parámetro. Es importante que se reciba el estado por parametro y que se tenga
        en cuenta que el estado y su evaluación será diferente para cada agente aunque la configuración del tablero
        no se mueva. Esto se debe a que cada agente tiene su posición y estas son diferentes, con lo cual sus distancias
        a la pizza también lo son (aunque pueden ser iguales en algunos casos) al igual que sus puntuaciones.
        """
        meta, score = estado.evaluar(self.nom)

        # ---> COMPROBACIÓN DE CASOS TRIVIALES:
        # Se encuentra estado meta
        if meta:
            return score, estado

        # Se ha alcanzado el límite de profundidad establecido como máximo en el programa (4)
        if nivel_profundidad == LIMITE_MAX_PROFUNDIDAD:
            return score, estado

        """
        Cuando se llama a la función de forma recursiva, se suma 1 al parametro de nivel para indicar un nivel más
        de profundidad, se le da el estado hijo, y se niega el booleano que indica si es turno del jugador MAX.
        Esto se hace para que los turnos de MAX y MIN se intercalen siempre
        NOT turnoMAX = turnoMIN, NOT turnoMIN = turnoMAX
        """
        # Lista con las puntuaciones de los hijos
        puntuacion_hijos = []
        # En caso de que no se alcance ningún caso trivial, se sigue con las llamadas recursivas
        for estado_hijo in estado.genera_hijos():
            puntuacion_hijos.append(self.miniMax(estado_hijo, nivel_profundidad+1, not turno_MAX))

        # Devolver el mayor o menor valor de las puntuaciones de los hijos dependiendo de quién es el turno
        if turno_MAX:
            return max(puntuacion_hijos)        # TURNO DE MAX
        else:
            return min(puntuacion_hijos)        # TURNO DE MIN

    """
    Funciones que devuelven el maximo o el minimo valor almacenado en una lista de valores. Se usan para ser llamadas
    desde la función minimax, con el objetivo de que se pueda escoger el máximo y el mínimo de la puntuación de
    los hijos de un estado, en los turnos de MAX y de MIN respectivamente
    """
    def max(self, lista_valores):
        # Contendrá el máximo
        mayor = 0
        # Elemento en indice mayor: lista[mayor]
        elemento = None

        for elemento_aux in lista_valores:
            if (elemento_aux[1] > mayor):
                mayor = elemento_aux[1]
                elemento = elemento_aux
        # Devolver elemento mayor y valor mayor
        return mayor, elemento
    def min(self, lista_valores):
        # Contendrá el mínimo
        menor = 9999
        # Elemento en indice menor: lista[menor]
        elemento = None

        for elemento_aux in lista_valores:
            if (elemento_aux[1] < menor):
                menor = elemento_aux[1]
                elemento = elemento_aux
        # Devolver elemento menor y valor menor
        return menor, elemento

    # Función actúa
    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        # Percibir el estado actual para la rana 'self' conocer el inicio del juego
        estado_actual = Estado(percep[ClauPercepcio.OLOR], percep[ClauPercepcio.POSICIO], percep[ClauPercepcio.PARETS], self.nom)
        actual = self.miniMax(estado_actual, 0)[1]
        #Crear una lista con todos los agentes interviniendo en el juego
        lista_agentes = percep[ClauPercepcio.POSICIO].keys()

        # Si alguno de los agentes de la lista ha llegado a la posición de la pizza, ha ganado
        for agente_iteracion in lista_agentes:
            if (percep[ClauPercepcio.POSICIO][agente_iteracion] == percep[ClauPercepcio.OLOR]):
                #print("El agente "+agente_iteracion+" se come la pizza")   2 veces!! corregir
                self.HAY_SOLUCION = True

        # Si ya se ha comido la pizza alguien los agentes se quedan esperando
        if self.HAY_SOLUCION:
            print("La rana " + self.nom + " espera porque no hay pizza para comer >:( ")
            return AccionsRana.ESPERAR

        # Establecer como padre
        while actual.pare is not None:
            pare, accio = actual.pare
            actual = pare

        # Control de los 2 turnos de espera reglamentarios por cada salto
        if (self.turnos_espera > 0):
            if self.turnos_espera == 2:
                print("La rana " + self.nom + " espera un turno porque ha saltado. Turno de espera 1")
            else:
                print("La rana " + self.nom + " espera un turno porque ha saltado. Turno de espera 2")
            self.turnos_espera -= 1
            return AccionsRana.ESPERAR
        else:
            if (accio[0] == AccionsRana.BOTAR):
                print("La rana "+self.nom+" ha saltado")
                self.turnos_espera = 2
            else:
                print("La rana " + self.nom + " se mueve")
            return accio[0],accio[1]