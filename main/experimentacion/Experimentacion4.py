import time

import matplotlib.pyplot as plt

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import matrizTridiagonalCompletaDeEnterosRandom, vectorDeEnterosRandom

# Esta experimentacion busca medir los tiempos de la eliminacion gaussiana sin pivoteo
# para matrices tridiagonales de diferente dimension, pero estas no seran tratadas como tridiagonales.
# Es decir, se asume que no se tiene conocimiento de la tridiagonalidad de las matrices
# Con el objetivo de poner el foco en el analisis del tiempo relacionado con la dimension de la matriz,
# los elementos de la misma estaran definidos unicamente por enteros del 1 al 50.
# El vector solucion se genera de la misma forma
# Los resultados se escriben en experimentacion4.txt. Esta conformado por dos columnas.
# La primera es el valor de n (dimension de la matriz), mientras que la segunda indica los ns que fueron necesarios para resolver
# el sistema
# Para la ejecucion de este test se recomienda tener la advertencia por error numerico desactivada,
# para observar los resutlados mas fieles posibles ya que el print es una operacion costosa

RESULTS_TXT_FILE_NAME = "experimentacion/resultados/experimentacion4.txt"
WRITE_MODE = 'a'


def ejecutar():
    times = []
    dimensiones = [5, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000]
    for n in dimensiones:
        times.append(ejecutarParaDimension(n))
    plt.plot(dimensiones, times)
    plt.xlabel("n")
    plt.ylabel("ns")
    plt.show()


def ejecutarParaDimension(n):
    matrizTridiagonal = matrizTridiagonalCompletaDeEnterosRandom(n, 1, 50)
    vectorSolucion = vectorDeEnterosRandom(n, 1, 50)
    try:
        startTime = time.time_ns()
        EliminacionGaussiana.sinPivoteo(matrizTridiagonal, vectorSolucion)
        solucion = SustitucionHaciaAtras.resolver(matrizTridiagonal, vectorSolucion)
        endTime = time.time_ns() - startTime
        txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
        txtFile.write("{0},{1}\n".format(n, endTime))
        return endTime
    except TypeError:
        ejecutarParaDimension(n)
