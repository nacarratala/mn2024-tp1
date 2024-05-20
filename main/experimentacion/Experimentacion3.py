import time

import matplotlib.pyplot as plt

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import matrizTridiagonalDeEnterosRandom, vectorDeEnterosRandom

# Esta experimentacion busca medir los tiempos de la eliminacion gaussiana sin pivoteo
# para matrices tridiagonales de diferente dimension.
# Con el objetivo de poner el foco en el analisis del tiempo relacionado con la dimension de la matriz,
# los elementos de la misma estaran definidos unicamente por enteros del 1 al 50.
# El vector solucion se genera de la misma forma
# Los resultados se escriben en experimentacion3.txt. Esta conformado por dos columnas.
# La primera es el valor de n (dimension de la matriz), mientras que la segunda indica los ns que fueron necesarios para resolver
# el sistema
# Para la ejecucion de este test se recomienda tener la advertencia por error numerico desactivada,
# para observar los resutlados mas fieles posibles ya que el print es una operacion costosa

RESULTS_TXT_FILE_NAME = "experimentacion/resultados/experimentacion3.txt"
WRITE_MODE = 'a'
ITERATION_COUNT = 500


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
    if n == 0:
        return
    matrizTridiagonal = matrizTridiagonalDeEnterosRandom(n, 1, 50)
    vectorA = matrizTridiagonal[0]
    vectorB = matrizTridiagonal[1]
    vectorC = matrizTridiagonal[2]
    vectorSolucion = vectorDeEnterosRandom(n, 1, 50)
    endTime = -1
    for i in range(ITERATION_COUNT):
        try:
            startTime = time.time_ns()
            EliminacionGaussiana.paraMatrizTridiagonal(vectorA, vectorB, vectorC, vectorSolucion)
            solucion = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorB, vectorC, vectorSolucion)
            newEndTime = time.time_ns() - startTime
            if endTime == -1 or newEndTime < endTime:
                endTime = newEndTime
        except TypeError:
            ejecutarParaDimension(n)
    print("n: ", n, " time: ", endTime)
    txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0},{1}\n".format(n, endTime))
    return endTime
