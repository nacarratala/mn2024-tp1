from copy import copy

from Utilidad import notificarPosibleErrorNumerico

EPSILON = 0.0001
ADVERTENCIA_ACTIVADA = False


# Toma: Una matriz A y un vector solucion
# Devuelve: None. Pero modifica la matriz A y el vector solucion acorde a haber realizado EG sin pivoteo
def sinPivoteo(matrizA, vectorSolucion):
    n = len(matrizA)
    for i in range(n):
        for j in range(i + 1, n):
            if matrizA[i][i] == 0:
                return None
            inverso = matrizA[j][i] / matrizA[i][i]
            for k in range(i + 1, n):
                matrizA[j][k] -= inverso * matrizA[i][k]
            matrizA[j][i] = 0
            vectorSolucion[j] -= inverso * vectorSolucion[i]


# Toma: Una matriz A y un vector solucion. Opcionalmente toma un threshold que representa el limite de error numerico aceptado
# Devuelve: None. Pero modifica la matriz A y el vector solucion acorde a haber realizado EG con pivoteo
def conPivoteo(matrizA, vectorSolucion):
    n = len(matrizA)
    for i in range(n):
        if matrizA[i, i] == 0:
            max_row = i
            for j in range(i + 1, n):
                if abs(matrizA[j, i]) > abs(matrizA[max_row, i]):
                    max_row = j
            if max_row != i:
                oldRow = copy(matrizA[i])
                matrizA[i] = matrizA[max_row]
                matrizA[max_row] = oldRow
                oldValue = copy(vectorSolucion[i])
                vectorSolucion[i] = vectorSolucion[max_row]
                vectorSolucion[max_row] = oldValue
            else:
                estadoInvalido("El pivote es 0 y toda su columna tambien")
        for j in range(i + 1, n):
            if ADVERTENCIA_ACTIVADA and (abs(matrizA[j, i]) < EPSILON or abs(matrizA[i, i]) < EPSILON):
                notificarPosibleErrorNumerico()
            inverso = matrizA[j, i] / matrizA[i, i]
            if ADVERTENCIA_ACTIVADA and abs(inverso) < EPSILON:
                notificarPosibleErrorNumerico()
            for k in range(i + 1, n):
                nuevoValor = matrizA[j, k] - (inverso * matrizA[i, k])
                if ADVERTENCIA_ACTIVADA and abs(nuevoValor) < EPSILON:
                    notificarPosibleErrorNumerico()
                matrizA[j, k] = nuevoValor
            matrizA[j, i] = 0
            vectorSolucion[j] -= inverso * vectorSolucion[i]
    return [matrizA, vectorSolucion]


# Toma: los vectores A, B y C de la matriz tridiagonal definida en el enunciado y el vector solucion D
# Devuelve: None
# Observacion: el vector B sufre las modificaciones pertinentes de haber realizado la EG.
# Lo mismo ocurre con el vector A (queda nulo). Por su parte, el vector C no sufre modificaciones
def paraMatrizTridiagonal(vectorA, vectorB, vectorC, vectorSolucion):
    n = len(vectorB)
    for i in range(n - 1):
        if vectorB[i] == 0:
            return estadoInvalido("El pivote es 0 en eliminacion gaussiana de matriz tridiagonal")
        inverso = vectorA[i] / vectorB[i]
        vectorA[i] = 0
        vectorB[i + 1] -= inverso * vectorC[i]
        vectorSolucion[i + 1] -= inverso * vectorSolucion[i]


# Toma: los vectores A y B de la matriz tridiagonal definida en el enunciado
# Devuelve: El vector de inversos multiplicativos usados
# Observacion: el vector B sufre las modificaciones pertinentes de haber realizado la EG.
# Lo mismo ocurre con el vector A (queda nulo). Por su parte, el vector C no sufre modificaciones
def paraMatrizTridiagonalGenerandoVectorDeInversos(vectorA, vectorB, vectorC):
    n = len(vectorB)
    vectorDeInversos = [0] * (n - 1)
    for i in range(n - 1):
        if vectorB[i] == 0:
            return estadoInvalido("El pivote es 0 en eliminacion gaussiana de matriz tridiagonal")
        inverso = vectorA[i] / vectorB[i]
        vectorA[i] = 0
        vectorB[i + 1] -= inverso * vectorC[i]
        vectorDeInversos[i] = -inverso
    return vectorDeInversos


# Actualmente no se usa TODO check
# Toma: el vector A modificado en la eg3SinPivoteo
# Devuelve: la matriz L de la factorizacion LU de la matriz a la cual se le aplico eg3SinPivoteo
def generarMatrizLParaMatrixTridiagonal(vectorA):
    n = len(vectorA) + 1
    matrizL = [[0] * n for _ in range(n)]
    for i in range(n - 1):
        matrizL[i][i] = 1
        matrizL[i + 1][i] = vectorA[i]
    matrizL[n - 1][n - 1] = 1
    return matrizL


def estadoInvalido(motivo):
    print("#####  ERROR #####")
    print(motivo)
    print("##################")
    raise TypeError(motivo)
