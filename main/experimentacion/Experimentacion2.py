import time

import matplotlib.pyplot as plt

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import vectorDeFloatsRandom, matrizDeFloatsRandom

# Esta experimentacion busca medir los tiempos de la eliminacion gaussiana con pivoteo
# para matrices de diferente dimension.
# Con el objetivo de poner el foco en el analisis del tiempo relacionado con la dimension de la matriz,
# los elementos de la misma estaran definidos unicamente por floats del 1 al 50.
# El vector solucion se genera de la misma forma
# Los resultados se escriben en experimentacion.txt. Esta conformado por dos columnas.
# La primera es el valor de n (dimension de la matriz), mientras que la segunda indica los ns que fueron necesarios para resolver
# el sistema
# Para la ejecucion de este test se recomienda tener la advertencia por error numerico desactivada,
# para observar los resutlados mas fieles posibles ya que el print es una operacion costosa

RESULTS_TXT_FILE_NAME = "experimentacion/resultados/experimentacion2.txt"
WRITE_MODE = 'a'
ITERATION_COUNT = 10


def ejecutar():
    times = []
    dimensiones = range(50, 1001, 50)
    for n in dimensiones:
        times.append(ejecutarParaDimension(n))
    plt.plot(dimensiones, times)
    plt.xlabel("n")
    plt.xscale("log")
    plt.ylabel("ns")
    plt.yscale("log")
    plt.show()


def ejecutarParaDimension(n):
    matrizA = matrizDeFloatsRandom(n, 1, 50)
    vectorSolucion = vectorDeFloatsRandom(n, 1, 50)
    endTime = -1
    for i in range(0, ITERATION_COUNT):
        try:
            startTime = time.time_ns()
            EliminacionGaussiana.conPivoteo(matrizA, vectorSolucion)
            solucion = SustitucionHaciaAtras.resolver(matrizA, vectorSolucion)
            newEndTime = time.time_ns() - startTime
            if endTime == -1 or newEndTime < endTime:
                endTime = newEndTime
        except TypeError:
            ejecutarParaDimension(n)
    print("n: ", n, " time: ", endTime)
    txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0},{1}\n".format(n, endTime))
    return endTime
