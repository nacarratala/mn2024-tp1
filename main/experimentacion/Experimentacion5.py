import time
from copy import copy

import matplotlib.pyplot as plt

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import matrizTridiagonalDeEnterosRandom, vectorDeEnterosRandom, \
    vectorDeInversosDeTridiagonalPorVectorSolucion

# Esta experimentacion busca medir en tiempo la ventaja de generar la matriz L
# para resolver, dado una matriz tridiagonal de enteros, un conjunto de ecuaciones.
# En otras palabras, busca analizar como afecta a la performance el hecho de guardar esta matriz L
# en vez de realizar reiteradas veces la eliminacion gaussiana
# En este escenario, no solo nos interesa ver como cambia la performance a medida que aumenta la dimension del a matriz,
# sino tambien la relacion que existe entre dicha performance y la cantidad de posibles vectores solucion.
# Con el objetivo de poner el foco en el analisis del tiempo relacionado con la dimension de la matriz,
# los elementos de la misma estaran definidos unicamente por enteros del 1 al 50.
# El vector solucion se genera de la misma forma
# Los resultados se escriben en experimentacion5.txt. Esta conformado por cuatro columnas.
# La primera es el valor de n (dimension de la matriz), la segunda el valor de s (cantidad de vectores solucion),
# la tercera indica los ns que fueron necesarios para resolver el conjunto
# de ecuaciones sin guardar L, mientras que la tercera indica los ns que fueron necesarios para resolver el conjunto
# # de ecuaciones guardando L
# Para la ejecucion de este test se recomienda tener la advertencia por error numerico desactivada,
# para observar los resutlados mas fieles posibles ya que el print es una operacion costosa

RESULTS_TXT_FILE_NAME = "experimentacion/resultados/experimentacion5.txt"
WRITE_MODE = 'a'


def ejecutar():
    timesTradicional = []
    timesOptimizado = []
    dimensiones = range(20, 1001, 20)
    for n in dimensiones:
        resultado = ejecutarParaDimensionYCantidadDeSoluciones(n, 5)
        timesTradicional.append(resultado[0])
        timesOptimizado.append(resultado[1])

    plt.plot(dimensiones, timesTradicional, label="Tradicional")
    plt.plot(dimensiones, timesOptimizado, label="Optimizado")
    plt.xlabel("n")
    plt.xscale("log")
    plt.ylabel("ns")
    plt.yscale("log")
    plt.legend(loc="upper left")
    plt.show()

    timesTradicional = []
    timesOptimizado = []
    for s in dimensiones:
        resultado = ejecutarParaDimensionYCantidadDeSoluciones(5, s)
        timesTradicional.append(resultado[0])
        timesOptimizado.append(resultado[1])

    plt.plot(dimensiones, timesTradicional, label="Tradicional")
    plt.plot(dimensiones, timesOptimizado, label="Optimizado")
    plt.xlabel("s")
    plt.ylabel("ns")
    plt.legend(loc="upper left")
    plt.show()

    timesTradicional = []
    timesOptimizado = []
    for ns in dimensiones:
        resultado = ejecutarParaDimensionYCantidadDeSoluciones(ns, ns)
        timesTradicional.append(resultado[0])
        timesOptimizado.append(resultado[1])

    plt.plot(dimensiones, timesTradicional, label="Tradicional")
    plt.plot(dimensiones, timesOptimizado, label="Optimizado")
    plt.xlabel("n and s")
    plt.ylabel("ns")
    plt.legend(loc="upper left")
    plt.show()


def ejecutarParaDimensionYCantidadDeSoluciones(n, s):
    matrizTridiagonal = matrizTridiagonalDeEnterosRandom(n, 1, 50)
    vectorA = matrizTridiagonal[0]
    vectorB = matrizTridiagonal[1]
    vectorC = matrizTridiagonal[2]
    # Se generan las copias necesarios ya que EliminacionGaussiana resuelve por referencia
    # El vector C no es modificado en la EG
    copiasDeVectorA = [0] * (s + 1)  # S veces para el que no genera L y 1 para el que si (no vuelve a usar A)
    copiasDeVectorB = [0] * (s + 1)  # S veces para el que no genera L y 1 para el que si (no vuelve a usar B)
    for i in range(s + 1):
        copiasDeVectorA[i] = copy(vectorA)
        copiasDeVectorB[i] = copy(vectorB)
    vectoresSolucion = [0] * s
    for i in range(s):
        vectoresSolucion[i] = vectorDeEnterosRandom(n, 1, 50)
    copiasDeVectoresSoluciones = copy(vectoresSolucion)
    try:
        startTime = time.time_ns()
        for i in range(s):
            EliminacionGaussiana.paraMatrizTridiagonal(copiasDeVectorA[i], copiasDeVectorB[i], vectorC,
                                                       vectoresSolucion[i])
            SustitucionHaciaAtras.resolverParaMatrizTridiagonal(copiasDeVectorB[i], vectorC, vectoresSolucion[i])
        endTimeTradicional = time.time_ns() - startTime
        txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
        txtFile.write("{0},{1},{2},".format(n, s, endTimeTradicional))
        startTime = time.time_ns()
        vectorDeInversos = None
        for i in range(s):
            if vectorDeInversos is None:
                # Tomo la ulitma copia de A y B(hasta aqui se usaron S copias)
                # Las modifico una unica vez y ya quedan re-utilizables para las proximas iteraciones
                vectorDeInversos = EliminacionGaussiana.paraMatrizTridiagonalGenerandoVectorDeInversos(
                    copiasDeVectorA[s], copiasDeVectorB[s], vectorC)
            vectorSolucion = copiasDeVectoresSoluciones[i]
            nuevoVectorSolucion = vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorSolucion)
            SustitucionHaciaAtras.resolverParaMatrizTridiagonal(copiasDeVectorB[s], vectorC, nuevoVectorSolucion)
        endTimeOptimizado = time.time_ns() - startTime
        txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
        txtFile.write("{0}\n".format(endTimeOptimizado))
        return [endTimeTradicional, endTimeOptimizado]
    except TypeError:
        ejecutarParaDimensionYCantidadDeSoluciones(n, s)
