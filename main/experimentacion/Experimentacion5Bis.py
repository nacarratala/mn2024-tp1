import time
from copy import copy

import matplotlib.pyplot as plt
import numpy

from eg import SustitucionHaciaAtras, EliminacionGaussiana
import Utilidad
from Utilidad import matrizTridiagonalDeEnterosRandom, vectorDeEnterosRandom, \
    vectorDeInversosDeTridiagonalPorVectorSolucion

RESULTS_TXT_FILE_NAME = "experimentacion/resultados/experimentacion5.txt"
WRITE_MODE = 'a'
ITERATION_COUNT = 10


def ejecutar():
    dimensiones = range(100, 1001, 100)
    timesTradicional = Utilidad.matrizDeEnterosRandom(len(dimensiones), 1, 50)
    timesOptimizado = Utilidad.matrizDeEnterosRandom(len(dimensiones), 1, 50)
    repeticiones = dimensiones
    # Dimension de la matriz (n)
    # Repeticiones (s)
    # Tiempo Tradicional tiene que ser una matriz de valores en funcion de n y s
    # Tiempo Optimizado tiene que ser otra matriz de valores en funcion de n y s
    # Hay que hacer un heatmap para cada uno y ponerlos en el informe
    for n in dimensiones:
        i = dimensiones.index(n)
        for s in repeticiones:
            j = repeticiones.index(s)
            res = ejecutarParaDimensionYCantidadDeSoluciones(n, s)
            timesTradicional[i][j] = res[0]
            timesOptimizado[i][j] = res[1]

    fig, ax = plt.subplots()
    ax.set_title("Tiempo de resolucion tradicional")
    ax.set_xticks(numpy.arange(len(dimensiones)), labels=repeticiones)
    ax.set_yticks(numpy.arange(len(dimensiones)), labels=dimensiones)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.xlabel("repeticiones")
    plt.xscale("log")
    plt.ylabel("dimensiones")
    plt.yscale("log")
    # ax.imshow(timesTradicional, cmap='hot', interpolation='nearest')
    fig.tight_layout()
    plt.pcolor(timesTradicional)
    plt.colorbar()
    plt.show()

    fig, ax = plt.subplots()
    ax.set_title("Tiempo de resolucion tridiagonal")
    ax.set_xticks(numpy.arange(len(dimensiones)), labels=repeticiones)
    ax.set_yticks(numpy.arange(len(dimensiones)), labels=dimensiones)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.xlabel("repeticiones")
    plt.xscale("log")
    plt.ylabel("dimensiones")
    plt.yscale("log")
    # ax.imshow(timesTradicional, cmap='hot', interpolation='nearest')
    fig.tight_layout()
    plt.pcolor(timesOptimizado)
    plt.colorbar()
    plt.show()

    timesTradicional = []
    timesOptimizado = []

    for n in dimensiones:
        resultado = ejecutarParaDimensionYCantidadDeSoluciones(n, 5)
        timesTradicional.append(resultado[0])
        timesOptimizado.append(resultado[1])

    plt.plot(dimensiones, timesTradicional, label="Tradicional")
    plt.plot(dimensiones, timesOptimizado, label="Optimizado")
    plt.xlabel("n")
    plt.ylabel("ns")
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
    plt.xlabel("n y s")
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
        endTimeTradicional = -1
        for iterationTradicional in range(ITERATION_COUNT):
            startTime = time.time_ns()
            for i in range(s):
                EliminacionGaussiana.paraMatrizTridiagonal(copiasDeVectorA[i], copiasDeVectorB[i], vectorC,
                                                           vectoresSolucion[i])
                SustitucionHaciaAtras.resolverParaMatrizTridiagonal(copiasDeVectorB[i], vectorC, vectoresSolucion[i])
            newEndTimeTradicional = time.time_ns() - startTime
            if endTimeTradicional == -1 or newEndTimeTradicional < endTimeTradicional:
                endTimeTradicional = newEndTimeTradicional
        print("n: ", n, " s: ", s, " time tradicional: ", endTimeTradicional)
        txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
        txtFile.write("{0},{1},{2},".format(n, s, endTimeTradicional))
        endTimeOptimizado = -1
        for iteracionOptimizado in range(ITERATION_COUNT):
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
            newEndTimeOptimizado = time.time_ns() - startTime
            if endTimeOptimizado == -1 or newEndTimeOptimizado < endTimeOptimizado:
                endTimeOptimizado = newEndTimeOptimizado
        print("n: ", n, " s: ", s, " time optimizado: ", endTimeOptimizado)
        txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
        txtFile.write("{0}\n".format(endTimeOptimizado))
        return [endTimeTradicional, endTimeOptimizado]
    except TypeError:
        return ejecutarParaDimensionYCantidadDeSoluciones(n, s)
