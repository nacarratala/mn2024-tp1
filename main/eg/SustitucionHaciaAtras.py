import numpy as np

from Utilidad import notificarPosibleErrorNumerico
from eg.EliminacionGaussiana import ADVERTENCIA_ACTIVADA, EPSILON


# Toma: Una matriz A y un vector solucion. Opcionalmente toma un threshold que representa el limite de error numerico aceptado
# Devuelve: el vector X tal que matriz A * x = vector solucion
def resolver(matrizA, vectorSolucion):
    n = len(matrizA)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += matrizA[i, j] * x[j]
            if ADVERTENCIA_ACTIVADA and abs(suma) < EPSILON:
                notificarPosibleErrorNumerico()
        x[i] = (vectorSolucion[i] - suma) / matrizA[i, i]
        if ADVERTENCIA_ACTIVADA and abs(x[i]) < EPSILON:
            notificarPosibleErrorNumerico()
    return x


def resolverParaMatrizTridiagonal(vectorB, vectorC, vectorSolucion):
    n = len(vectorB)
    x = [0] * n
    x[n - 1] = vectorSolucion[n - 1] / vectorB[n - 1]
    for i in range(n - 2, -1, -1):
        suma = vectorC[i] * x[i + 1]  # Aca solo me interesa el C, no necesito iterar sobre toda la fila
        if ADVERTENCIA_ACTIVADA and abs(suma) < EPSILON:
            notificarPosibleErrorNumerico()
        x[i] = (vectorSolucion[i] - suma) / vectorB[i]
        if ADVERTENCIA_ACTIVADA and abs(x[i]) < EPSILON:
            notificarPosibleErrorNumerico()
    return x
