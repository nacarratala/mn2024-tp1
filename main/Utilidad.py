import random
from copy import copy

import numpy as np


# Solo para test
def imprimirMatriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])


# Solo para test
def notificarPosibleErrorNumerico():
    print("ADVERTENCIA: Posible error numerico")


# Solo para test
def enteroRandom(desde, hasta):
    return random.randrange(desde, hasta)


# Solo para test
def floatRandom(desde, hasta):
    return random.uniform(desde, hasta)


# Solo para test
def vectorDeEnterosRandom(dimension, desde, hasta):
    vectorSolucion = [0] * dimension
    for i in range(dimension):
        vectorSolucion[i] = enteroRandom(desde, hasta)
    return np.array(vectorSolucion, dtype=np.int_)


# Solo para test
def vectorDeFloatsRandom(dimension, desde, hasta):
    vector = [0.0] * dimension
    for i in range(dimension):
        vector[i] = floatRandom(desde, hasta)
    return np.array(vector, dtype=np.float64)


def vectorDeFloats128Random(dimension, desde, hasta):
    ## CHEQUEAR
    # return np.random.default_rng().(size=dimension, dtype='complex')
    return


# Solo para test
def vectorDeFloatsRandom32(dimension, desde, hasta):
    vector = vectorDeFloatsRandom(dimension, desde, hasta)
    return convertirAVectorDeFloats32(vector)


def convertirAVectorDeFloats32(vector64):
    return np.array(vector64, dtype=np.float32)


# Solo para test
def matrizDeEnterosRandom(dimension, desde, hasta):
    matriz = [[0] * dimension for _ in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            matriz[i][j] = enteroRandom(desde, hasta)
    return np.matrix(matriz, dtype=np.int_)


# Solo para test
def matrizDeFloatsRandom(dimension, desde, hasta):
    matriz = [[0.0] * dimension for _ in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            matriz[i][j] = floatRandom(desde, hasta)
    return np.matrix(matriz, dtype=np.float64)


def matrizDeFloatsRandom32(dimension, desde, hasta):
    matriz64 = matrizDeFloatsRandom(dimension, desde, hasta)
    return convertirAMatrizDeFloats32(matriz64)


def convertirAMatrizDeFloats32(matriz64):
    matriz32 = copy(matriz64)
    for i in range(len(matriz64)):
        matriz32[i] = convertirAVectorDeFloats32(matriz64[i])
    return np.matrix(matriz32, dtype=np.float32)


# Solo para test
def matrizTridiagonalDeEnterosRandom(dimension, desde, hasta):
    vectorA = [0] * (dimension - 1)
    vectorB = [0] * dimension
    vectorC = [0] * (dimension - 1)
    for i in range(dimension - 1):
        vectorA[i] = enteroRandom(desde, hasta)
        vectorB[i] = enteroRandom(desde, hasta)
        vectorC[i] = enteroRandom(desde, hasta)
    vectorB[dimension - 1] = enteroRandom(desde, hasta)
    return [vectorA, vectorB, vectorC]


# Solo para test
def matrizTridiagonalCompletaDeEnterosRandom(dimension, desde, hasta):
    matrizTridiagonal = [[0] * dimension for _ in range(dimension)]
    matrizTridiagonal[0][0] = enteroRandom(desde, hasta)
    matrizTridiagonal[0][1] = enteroRandom(desde, hasta)
    for i in range(1, dimension - 1):
        matrizTridiagonal[i][i - 1] = enteroRandom(desde, hasta)
        matrizTridiagonal[i][i] = enteroRandom(desde, hasta)
        matrizTridiagonal[i][i + 1] = enteroRandom(desde, hasta)
    matrizTridiagonal[dimension - 1][dimension - 2] = enteroRandom(desde, hasta)
    matrizTridiagonal[dimension - 1][dimension - 1] = enteroRandom(desde, hasta)
    return matrizTridiagonal


def vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorSolucion):
    n = len(vectorSolucion)
    nuevoVectorSolucion = [0] * n
    nuevoVectorSolucion[0] = vectorSolucion[0]
    for i in range(1, n):
        nuevoVectorSolucion[i] = nuevoVectorSolucion[i - 1] * vectorDeInversos[i - 1] + vectorSolucion[i]
    return nuevoVectorSolucion


# A = vector de Rn (diagonal)
# B = vector de Rn-1 (arriba de la diagonal)
# c = vector de Rn-1 (abajo de la diagonal)
# vector = vector de Rn
def matrizTridiagonalPorVector(a, b, c, vector):
    n = len(vector)
    solucion = [0] * n
    solucion[0] = a[0] * vector[0] + b[0] * vector[1]
    solucion[n - 1] = c[n - 2] * vector[n - 2] + a[n - 1] * vector[n - 1]
    for i in range(1, n - 1):
        solucion[i] = c[i - 1] * vector[i - 1] + a[i] * vector[i] + b[i] * vector[i + 1]
    return solucion


# Solo para test
def recuperarVectoresAByCDeMatriz(matrix):
    n = len(matrix)
    vectorA = [0] * (n - 1)
    vectorB = [0] * n
    vectorC = [0] * (n - 1)
    vectorB[0] = matrix[0][0]
    vectorC[0] = matrix[0][1]
    for i in range(1, n - 1):
        vectorA[i - 1] = matrix[i][i - 1]
        vectorB[i] = matrix[i][i]
        vectorC[i] = matrix[i][i + 1]
    vectorA[n - 2] = matrix[n - 1][n - 2]
    vectorB[n - 1] = matrix[n - 1][n - 1]
    return [vectorA, vectorB, vectorC]


def normaInfinitoDeVector(vector):
    maxEnModulo = 0
    for i in range(len(vector)):
        if abs(vector[i]) > maxEnModulo:
            maxEnModulo = abs(vector[i])
    return maxEnModulo
