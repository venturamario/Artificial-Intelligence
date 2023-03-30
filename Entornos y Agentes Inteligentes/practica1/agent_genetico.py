"""
        ASIGNATURA: Inteligencia Artificial
        TRABAJO: Práctica 1
        CURSO: 2022-2023
        AUTORES: Mario Ventura & Luis Miguel Vargas
        Grado en Ingeniería Informática (GIN3)
"""

import random
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, Direccio
from practica1.entorn import AccionsRana

"""
========================================================================================================================
                                    BÚSQUEDA MEDIANTE ALGORITMO GENÉTICO
========================================================================================================================
"""
nombreAgente = "Mario"
tamanoPoblacion = 25


class Individuo:

    # Constructor init
    def __init__(self):
        self.__info = []
        self.__fitness = -1

    # Getters
    def get_toda_info(self):
        return self.__info
    def get_info(self, i):
        return self.__info[i]
    def get_fitness(self):
        return self.__fitness
    def get_lenght_info(self):
        return len(self.__info)
    def get_infor_partition_inf(self, index):
        return self.__info[: index]
    def get_infor_partition_sup(self, index):
        return self.__info[index:]


    # Setters
    def append_info(self, accion, direccion):
        self.__info.append((accion, direccion))
    def set_info_at(self, i, accion, direccion):
        self.__info[i]=(accion, direccion)
    def config_info(self, info):
        self.__info=info
    def set_info_partition(self, i):
        self.__info=self.__info[:i]
    def set_fitness(self, i):
        self.__fitness=i


class Genetica:

    # Constructor init
    def __init__(self, pob: int, inicial: tuple, posPizza, paredes):
        self.__tamano_poblacion = pob
        self.__poblacion = []
        self.__posicion_inicial = inicial
        self.posPizza = posPizza
        self.__fitness = 0
        self.__paredes = paredes
        self.__num_genes = 14

    # Comprobar si un estado pasado por parámetro es válido
    def es_valido(self, posicion):
        # Fila y columna del estado cuya validez de quiere comprobar
        columna, fila = list(posicion)

        # Comprobar si la posición está contenida dentro del tablero (no excede los límites)
        if columna > 7 or columna < 0:
            return False
        if fila > 7 or fila < 0:
            return False
        # Comprobar si la posición coincide con la de una pared
        if posicion in self.__paredes:
            return False
        # Si nada de lo anterior sucede, la posición es válida
        return True

    # Comprobar si un estado pasado por parámetro es el estado meta al que se pretende llegar
    def es_meta(self, posicion):
        return posicion == self.posPizza

    # Setter del fitness de la poblacion
    def set_fitness_poblacion(self, i):
        self.__fitness=i

    # Getter del fitness de la población
    def get_fitness_poblacion(self):
        return self.__fitness

    # Inicialización de la población
    def generar_poblacion(self):

        # Listas de posibles acciones y direcciones
        lista_acciones = [AccionsRana.BOTAR, AccionsRana.ESPERAR, AccionsRana.MOURE]
        lista_direcciones = [Direccio.DALT, Direccio.BAIX, Direccio.DRETA, Direccio.ESQUERRE]

        # Se recorrerá la población para crear acciones aleatorias
        for individuo in range(self.__tamano_poblacion + 1):
            indv = Individuo()       # Individuo que realizará una acción aleatoria
            for n in range(self.__num_genes):

                """
                Se escogen acciones aleatorias que se realizarán en una dirección aleatoria. Este es el factor de
                aleatoriedad que tienen todos los algoritmos genéticos y que permiten, precisamente, simular un cruce
                genético real
                """
                accion_aleatoria = random.randint(0, len(lista_acciones) - 1)
                direccion_aleatoria = random.randint(0, len(lista_direcciones) - 1)

                #Se añaden estas acciones y direcciones a la lista de información del individuo creado
                accion = lista_acciones.__getitem__(accion_aleatoria)
                direccion = lista_direcciones.__getitem__(direccion_aleatoria)
                indv.append_info(accion, direccion)

            self.fitness(indv)
            if indv.get_fitness() != 1000:      # Máximo establecido (por ejemplo)
                individuo += 1
                self.__poblacion.append(indv)    #Añadir el individuo a la poblacion

        #Recalcular el fitness de la población
        self.calcular_fitness_poblacion()

    """
    RECIBE ------>  Posicion actual del agente, dirección en que se debe mover 
    DEVUELVE ---->  Nueva posición
    HACE -------->  Dada una posición del agente en el tablero, calcula cuál será su nueva posición en función
                    de la acción que tenga que hacer y en la dirección en que la haga
    """
    def calcular_posicion(self, posicion, direccion: Direccio, magnitut):
            posicion = joc.Laberint._calcula_casella(posicion, direccion, magnitut)
            return posicion

    """
        RECIBE ------>  Objeto individuo 
        DEVUELVE ---->  void (función de fitness)
        HACE -------->  Dada una posición del agente en el tablero, calcula cuál será su nueva posición en función
                        de la acción que tenga que hacer y en la dirección en que la haga.
                        Distancia manhattan + coste
        """
    def fitness(self, individuo: Individuo):

        posicion = self.__posicion_inicial
        longitud_info_individuo = individuo.get_lenght_info()
        salida = 0

        for i in range(longitud_info_individuo):
            accion_individuo, direccion_individuo = individuo.get_info(i)

            #Comprobar qué acción hace la rana
            if accion_individuo != AccionsRana.ESPERAR:
                if accion_individuo == AccionsRana.BOTAR:
                    # ---> La rana Mario salta
                    posicion_individuo = self.calcular_posicion(posicion, direccion_individuo, 2)    # 2 = casillas de desplazamiento
                else:
                    # ---> La rana mario se mueve
                    posicion_individuo = self.calcular_posicion(posicion, direccion_individuo, 1)    # 1 = casillas de desplazamiento
            else:
                # La rana Mario espera
                posicion_individuo = posicion       # Si la rana espera no se mueve, no hay que actualizar posición

            # Comprobar si la posición nueva es válida
            if not self.es_valido(posicion_individuo):
                individuo.set_info_partition(i)

                # Si el gen es malo no lo añadimos
                if individuo.get_lenght_info() == 1:
                    individuo.set_fitness(1000)
                break

            # Comprobar si el estado nuevo es meta
            if self.es_meta(posicion_individuo):
                individuo.set_fitness(0)
                salida = -1
                break

            posicion = posicion_individuo

        # Informacion actualizada
        if salida != -1:
            columna_pizza, fila_pizza = self.posPizza                   # Posición de la piza en el tablero
            columna_rana, fila_rana = posicion                          # Nueva posición actualizada
            desplazamiento_columna = abs(columna_pizza - columna_rana)  # abs() para evitar valores negativos
            desplazamiento_fila = abs(fila_pizza - fila_rana)           # abs() para evitar valores negativos
            fitness = (desplazamiento_fila + desplazamiento_columna)    # Establecer fitness nuevo
            individuo.set_fitness(fitness)                              # Setter del nuevo fitness

    # Calcular el fitness medio de la población
    def calcular_fitness_poblacion(self):
        # Entero que actuará a modo de contador
        fitness_total_poblacion = 0
        # Aumentar el contador del fitness total de la poblacion con un incremento con el fitness de cada individuo
        for individuo in self.__poblacion:
            fitness_individuo = individuo.get_fitness()
            # Si el fitness es 1000 (fitness malísimo) lo descartamos
            if fitness_individuo != 1000:
                fitness_total_poblacion += individuo.get_fitness()      # Aumentar contador de fitness total
        # Media aritmetica del fitness de la poblacion
        self.__fitness = fitness_total_poblacion / self.__tamano_poblacion

    # Seleccionar qué individuos sobreviven y realizar cruces genéticos y mutaciones
    def seleccionar_individuos(self):

        # Listas y contadores de individuos candidatos y descartados
        candidatos = []
        numero_candidatos = 0
        descartados = []
        numero_descartados=0
        contador_iteraciones = 0

        # Controladores de si hay solución y cuál es esta solución
        hay_solucion = False
        solucion = None

        print("\n\n\n\n\n\n\n\n\n\nFitness de la poblacion: ", self.__fitness)
        print("\n\n\n\n\n\n")

        while not hay_solucion:
            '''
            Se filtra la población y se escogen individuos en función del fitness que estos tengan. Cuanto más alto
            sea este fitness, peor para el individuo, pues menos probabilidad tendrá de ser escogido.
            Fitness = 1000 como máximo (peor caso).
            Esta función será llamada varias veces durante el transcurso de la ejecución del algoritmo, hasta que en
            una población se encuentre un individuo con fitness 0 (solución)
            '''
            for individuo_iteracion in self.__poblacion:

                # Obtener el fitness del individuo de la iteracion x
                fitness_individuo_iteracion = individuo_iteracion.get_fitness()

                # Mejor caso: fitness = 0 = solucion
                if (fitness_individuo_iteracion == 0):
                    solucion = individuo_iteracion      # Se establece a este como solución
                    hay_solucion = True                        # Fin de la iteración. No se sigue filtrando
                    break

                # Si el fitness es menor o igual, este es un individuo candidato
                if (fitness_individuo_iteracion <= self.__fitness):
                    numero_candidatos += 1                          # Aumenta el contador de candidatos
                    candidatos.append(individuo_iteracion)          # Se añade a la lista de candidatos
                    self.__poblacion.remove(individuo_iteracion)    # Se elimina a este de la población actual

                # Si el fitness del individuo es mayor que el de la población, el individuo se descarta
                elif (fitness_individuo_iteracion > self.__fitness):
                    numero_descartados += 1  # Aumenta el contador de individuos descartados
                    descartados.append(individuo_iteracion)  # Se añade a la lista de individuos descartados
                    self.__poblacion.remove(individuo_iteracion)  # El individuo se elimina de la población

            if not (hay_solucion):
                """
                Dado que para hacer un cruce siempre se necesita un mínimo de 2 individuos (pensar en poblaciones de
                animales reales), deberemos tener en cuenta la posibilidad de que la población haya tenido muy mal
                fitness individual, y no haya ningun individuo en la lista de candidatos. 
                En este caso se escogerán 2 individuos de la lista de descartados para ponerlos en la lista de
                individuos candidatos, asegurando así el tamaño mínimo necesario de la próxima población
                """
                if (len(candidatos) < 2):
                    candidatos.append(descartados.pop(0))
                    candidatos.append(descartados.pop(0))

                # Realizar cruces genéticos entre individuos hasta llegar al tamaño requerido de la población
                while len(self.__poblacion) < self.__tamano_poblacion :

                    # Mensaje que se mostrará por consola
                    print("Realizando combinaciones genéticas...")

                    """
                    Las combinaciones genéticas se hacen de forma que se esogen 2 candidatos, se mira cuál es la longuitud
                    de sus genes (array info), se escoge el minimo de estas y se usa como número o índice de
                    partición de los arrays, que posteriormente se reconstruyen
                    """
                    candidato1 = candidatos.__getitem__(random.randint(0, len(candidatos)-1))       # Candidato 1
                    candidato2 = candidatos.__getitem__(random.randint(0, len(candidatos)-1))       # Candidato 2

                    self.__poblacion.append(candidato1)                             # Se añade a la poblacion
                    self.__poblacion.append(candidato2)                             # Se añade a la poblacion
                    longitud_info_candidato1 = candidato1.get_lenght_info()         # Longitud 1
                    longitud_info_candidato2 = candidato2.get_lenght_info()         # Longitud 2

                    # Comprobar cuál es el menor de ambos en cuanto a longitud de información
                    menor = min(longitud_info_candidato1, longitud_info_candidato2)

                    # Escoger indice de particion aleatorio y partir los arrays de informacion
                    indice_de_particion = random.randint(0, menor)
                    mitad_inferior_candidato1 = candidato1.get_infor_partition_inf(indice_de_particion)
                    mitad_superior_candidato1 = candidato1.get_infor_partition_sup(indice_de_particion)
                    mitad_inferior_candidato2 = candidato2.get_infor_partition_inf(indice_de_particion)
                    mitad_superior_candidato2 = candidato2.get_infor_partition_sup(indice_de_particion)
                    nueva_info_candidato1= []       # Nueva lista de genes del candidato 1
                    nueva_info_candidato2=[]        # Nueva lista de genes del candidato 2

                    # Reensamblar los arrays mediante las particiones producidas
                    for individuo_iteracion in range(len(mitad_inferior_candidato1)):
                        nueva_info_candidato1.append(mitad_inferior_candidato1[individuo_iteracion])
                    for individuo_iteracion in range(len(mitad_inferior_candidato2)):
                        nueva_info_candidato2.append(mitad_inferior_candidato2[individuo_iteracion])
                    for individuo_iteracion in range(len(mitad_superior_candidato2)):
                        nueva_info_candidato1.append(mitad_superior_candidato2[individuo_iteracion])
                    for individuo_iteracion in range(len(mitad_superior_candidato1)):
                        nueva_info_candidato2.append(mitad_superior_candidato1[individuo_iteracion])

                    # Nuevos individuos hijo fruto del cruce genético de los padres
                    individuo_hijo1 = Individuo()
                    individuo_hijo2 = Individuo()
                    # Dar genes a los hijos
                    individuo_hijo1 .config_info(nueva_info_candidato1)
                    individuo_hijo2.config_info(nueva_info_candidato2)

                    """
                    Una vez se han creado dos hijos con cierta aleatoriedad, se deberá crear mutaciones sobre estos
                    con el objetivo de que tras estas mutaciones, los individuos estén todavía más cerca de una
                    posible solución, simulando una vez más un cruce real entre individuos de una especie animal
                    """

                    # Se crea un índice aleatorio de mutación genética
                    indice_aleatorio_mutación = random.randint(0,400)

                    # Usar la aleatoriedad de esté índice conjuntamente con otros datos numéricos para hace mutaciones
                    if (250 < indice_aleatorio_mutación < 300 or contador_iteraciones > 200) and individuo_hijo1 .get_lenght_info() > 0:
                        if contador_iteraciones > 200:
                            """
                            Mutación genética nº 1
                            """
                            self.mutar_individuo(individuo_hijo1 , individuo_hijo1 .get_lenght_info() // 2)
                        else:
                            """
                            Mutación genética nº 2
                            """
                            self.mutar_individuo(individuo_hijo1 )
                    elif (350 < indice_aleatorio_mutación < 400 or contador_iteraciones > 200) and individuo_hijo2.get_lenght_info() > 0:
                        if contador_iteraciones > 200:
                            """
                            Mutación genética nº 3
                            """
                            self.mutar_individuo(individuo_hijo2, individuo_hijo2.get_lenght_info() // 2)
                        else:
                            """
                            Mutación genética nº 4
                            """
                            self.mutar_individuo(individuo_hijo2)

                    # Establecer nuevos fitness
                    self.fitness(individuo_hijo1)
                    self.fitness(individuo_hijo2)
                    if (individuo_hijo1.get_lenght_info() == 0 or individuo_hijo2.get_lenght_info() == 0):
                        print("----< INDIVIDUO CON INFORMACIÓN GENÉTICA DE TAMAÑO 0 >----")
                    if (individuo_hijo1.get_fitness() <= self.__fitness and individuo_hijo1.get_fitness() != 1000):
                        self.__poblacion.append(individuo_hijo1)
                    if individuo_hijo2.get_fitness()<=self.__fitness and individuo_hijo2.get_fitness()!=1000:
                        self.__poblacion.append(individuo_hijo2)

                # Recalcular el fitness de la poblacion
                self.calcular_fitness_poblacion()
        # Si hay_solucion == true, significa que se ha encontrado una solucion. Se devuelve esta solucion
        if hay_solucion:
            return self.devolver_solucion(solucion)

    # Devuelve la solucion
    def devolver_solucion(self, individuo: Individuo):
        # Lista de acciones
        acciones=[]
        pos = self.__posicion_inicial

        # Recorrer la info del individuo recibido por parametro
        for info in range(len(individuo.get_toda_info())):
            gen = individuo.get_info(info)
            accion_individuo, direccion_individuo = gen
            # Comprobar qué acción hace el individuo
            if accion_individuo != AccionsRana.ESPERAR:
                if accion_individuo == AccionsRana.BOTAR:
                    #print("SALTAR")
                    pos_indv = self.calcular_posicion(pos, direccion_individuo, 2)
                else:
                    #print("MOVERSE")
                    pos_indv = self.calcular_posicion(pos, direccion_individuo, 1)

            else:
                #print("ESPERAR")
                pos_indv = pos
            # Comprobar si el estado es meta
            if self.es_meta(pos_indv):
                acciones.append(gen)
                break
            else:
                acciones.append(gen)
            pos = pos_indv
        # Devolver la lista de acciones
        return acciones

    # Realiza la mutación genética de un individuo
    def mutar_individuo(self, individuo: Individuo, numero_genes = 1):

        # Lista de acciones del individuo y direcciones en las que las puede realizar
        acciones = [AccionsRana.BOTAR, AccionsRana.ESPERAR, AccionsRana.MOURE]
        direcciones = [Direccio.DALT, Direccio.BAIX, Direccio.ESQUERRE, Direccio.DRETA]

        # Recorrer los genes del individuo
        for n in range(numero_genes):
            #Generación de 3 índices aleatorios para hacer un setter de las acciones y direcciones
            indice_acciones = random.randint(0, len(acciones)-1)
            indice_direcciones = random.randint(0, len(acciones)-1)
            indice_genes = random.randint(0, individuo.get_lenght_info() - 1)
            # Mutar el gen
            individuo.set_info_at(indice_genes, acciones[indice_acciones], direcciones[indice_direcciones])


class Rana(joc.Rana):

    # Constructor info
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
        print("================================================")
        print("======= RECORRIDO CON ALGORITMO GENÉTICO =======")
        print("================================================\n")

    # Para limpiar la consola
    def clearScreen(self):
        idx = 50
        while (idx > 0):
            print("\n")
            idx-=1

    """
    RECIBE ----> Estado actual del agente en el entorno, ubicación de la pizza, ubicación de las paredes
    DEVUELVE --> void (simplemente da valor a la lista de acciones que debe hacer la rana)
    HACE ------> Dada la posición de la pizza y de las paredes en el tablero, busca una forma de llegar hasta la pizza
                    desde el estado que se recibe por parametro mediante llamadas a otras funciones
    """
    def busqueda(self, estado_inicial, solucion, paredes):

        # Generar poblacion
        genetica = Genetica(tamanoPoblacion, estado_inicial, solucion, paredes)
        genetica.generar_poblacion()
        solucion = genetica.seleccionar_individuos()

        # Lista de acciones
        acciones = []
        for i in solucion:
            accio, dir = i
            # Contemplar el caso de que la acción sea un salto ya que en ese caso hay que esperar durante dos turnos
            if accio == AccionsRana.BOTAR:
                acciones.append(i)
                # --> Para esperar dos turnos se añaden dos acciones de espera
                acciones.append(AccionsRana.ESPERAR)
                acciones.append(AccionsRana.ESPERAR)
            else:
                acciones.append(i)

        # Establecer esta lista como la de la clase
        self.__acciones = acciones

    # Función de actuación de la rana
    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:

        # Definir estado inicial, posición de paredes, y posición de pizza
        pizza = percep[ClauPercepcio.OLOR]
        paredes = percep[ClauPercepcio.PARETS]
        estado_inicial = percep[ClauPercepcio.POSICIO][nombreAgente]

        # Buscar solución
        if self.__acciones is None:
            self.busqueda(estado_inicial, pizza, paredes)
            self.clearScreen()
            self.presentacion()

        # Sacar acciones
        if self.__acciones:
            acc = self.__acciones.pop(0)
            print("ACCIÓN DE LA RANA ----> " + str(acc))
            return acc

        else:
            # Solo se entra en esta condición una vez ya no hay acciones por hacer, cosa que solo sucede
            # si ya se ha llegado hasta la pizza
            print("La rana " + nombreAgente + " espera porque no hay pizza para comer >:( ")
            return AccionsRana.ESPERAR