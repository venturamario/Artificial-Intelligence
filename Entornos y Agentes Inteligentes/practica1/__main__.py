"""
        ASIGNATURA: Inteligencia Artificial
        TRABAJO: Práctica 1
        CURSO: 2022-2023
        AUTORES: Mario Ventura & Luis Miguel Vargas
        Grado en Ingeniería Informática (GIN3)
"""

from practica1 import agent, joc

"""
========================================================================================================================
                                    MAIN PARA LLAMAR A LOS ALGORITMOS E INICIAR JUEGO
========================================================================================================================
"""

def main():

    #---> MAIN PARA ALGORITMOS AMPLITUD, A* Y GENÉTICO
    ranaM = agent.Rana("Mario")
    lab = joc.Laberint([ranaM], parets=True)
    lab.comencar()



    #---> MAIN PARA ALGORITMO MINIMAX
    # ranaM = agent.Rana("Mario")
    # ranaL = agent.Rana("Luismi")
    # lab = joc.Laberint([ranaM, ranaL], parets=True)
    # lab.comencar()


if __name__ == "__main__":
    main()
