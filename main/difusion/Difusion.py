# Funcion que resuelve el punto 6 del enunciado
# Guarda el resultado en laplaciano/resultados/laplaciano.txt
import matplotlib.pyplot as plt
import numpy as np

from eg import SustitucionHaciaAtras, EliminacionGaussiana
import Utilidad

IMPLICIT_RESULTS_TXT_FILE_NAME = "difusion/resultados/difusion_implicita.txt"
EXPLICIT_RESULTS_TXT_FILE_NAME = "difusion/resultados/difusion_explicita.txt"

WRITE_MODE = 'a'


def resolverImplicito(n, r, m, alpha):
    vectorAdeMatrizA = [-(1 * alpha)] * n
    vectorBdeMatrizA = [-((-2 * alpha) - 1)] * n
    vectorCdeMatrizA = [-(1 * alpha)] * n
    vectorDeInversos = EliminacionGaussiana.paraMatrizTridiagonalGenerandoVectorDeInversos(vectorAdeMatrizA,
                                                                                           vectorBdeMatrizA,
                                                                                           vectorCdeMatrizA)

    vectoresUCalculados = [[0] * m for _ in range(m)]

    vectorUkMenos1 = generarUiCero(n, r)
    txtFile = open(IMPLICIT_RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0}\n".format(vectorUkMenos1))
    vectoresUCalculados[0] = vectorUkMenos1
    for k in range(1, m):
        nuevoVectorUkMenos1 = Utilidad.vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorUkMenos1)
        vectorUk = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorBdeMatrizA, vectorCdeMatrizA,
                                                                       nuevoVectorUkMenos1)
        txtFile.write("{0}\n".format(vectorUk))
        vectoresUCalculados[k] = vectorUk
        vectorUkMenos1 = vectorUk
    fig, ax = plt.subplots()
    im = ax.imshow(np.transpose(np.array(vectoresUCalculados)), interpolation="none", cmap="viridis", aspect="auto")
    plt.colorbar(im)
    plt.show()


def generarUiCero(n, r):
    vectorU = [0] * n
    for i in range(n):
        if (n // 2) - r < i < (n // 2) + r:
            vectorU[i] = 1
        else:
            vectorU[i] = 0
    return vectorU


def resolverExplicito(n, r, m, alpha):
    vectorAdeMatrizA = [1 * alpha] * n
    vectorBdeMatrizA = [(-2 * alpha) + 1] * n
    vectorCdeMatrizA = [1 * alpha] * n

    vectoresUCalculados = [[0] * m for _ in range(m)]

    vectorUk = generarUiCero(n, r)
    txtFile = open(EXPLICIT_RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0}\n".format(vectorUk))
    vectoresUCalculados[0] = vectorUk
    for k in range(1, m):
        nuevoVectorUk = Utilidad.matrizTridiagonalPorVector(vectorAdeMatrizA, vectorBdeMatrizA, vectorCdeMatrizA, vectorUk)
        txtFile.write("{0}\n".format(vectorUk))
        vectoresUCalculados[k] = nuevoVectorUk
        vectorUk = nuevoVectorUk
    fig, ax = plt.subplots()
    im = ax.imshow(np.transpose(np.array(vectoresUCalculados)), interpolation="none", cmap="viridis", aspect="auto")
    plt.colorbar(im)
    plt.show()
