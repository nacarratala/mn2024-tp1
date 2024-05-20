# Funcion que resuelve el punto 4 del enunciado
# Guarda el resultado en laplaciano/resultados/laplaciano.txt
import matplotlib.pyplot as plt

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import vectorDeInversosDeTridiagonalPorVectorSolucion

RESULTS_TXT_FILE_NAME = "laplaciano/resultados/laplaciano.txt"
WRITE_MODE = 'a'


def resolver():
    n = 101
    vectorA = [1] * n
    vectorB = [-2] * n
    vectorC = [1] * n
    vectorSolucionDa = generarVectorDa(n)
    # Consigo mi vector de inversos y al mismo tiempo triangulo la matriz (leer contrato de funcion)
    vectorDeInversos = EliminacionGaussiana.paraMatrizTridiagonalGenerandoVectorDeInversos(vectorA, vectorB, vectorC)
    # Hasta aqui el vector solucion no sufrio modificaciones. Debo multiplicarlo por mi M (vector de inversos)
    nuevoVectorSolucionDa = vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorSolucionDa)
    solucionFinalDa = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorB, vectorC, nuevoVectorSolucionDa)
    txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0}\n{1}\n\n\n".format("Solucion final para vector Da", solucionFinalDa))

    vectorSolucionDb = generarVectorDb(n)
    nuevoVectorSolucionDb = vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorSolucionDb)
    solucionFinalDb = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorB, vectorC, nuevoVectorSolucionDb)
    txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0}\n{1}\n\n\n".format("Solucion final para vector Db", solucionFinalDb))

    vectorSolucionDc = generarVectorDc(n)
    nuevoVectorSolucionDc = vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, vectorSolucionDc)
    solucionFinalDc = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorB, vectorC, nuevoVectorSolucionDc)
    txtFile = open(RESULTS_TXT_FILE_NAME, WRITE_MODE)
    txtFile.write("{0}\n{1}\n\n\n".format("Solucion final para vector Dc", solucionFinalDc))

    plt.plot(solucionFinalDa, label="(a)")
    plt.plot(solucionFinalDb, label="(b)")
    plt.plot(solucionFinalDc, label="(c)")
    plt.xlabel("x")
    plt.ylabel("u")
    plt.legend(loc="lower left")
    plt.show()


def generarVectorDa(n):
    vectorD = [0] * n
    vectorD[n // 2 + 1] = 4 / n
    return vectorD


def generarVectorDb(n):
    valor = 4 / (n ** 2)
    vectorD = [valor] * n
    return vectorD


def generarVectorDc(n):
    vectorD = [0] * n
    for i in range(n):
        vectorD[i] = (- 1 + 2 * i / (n - 1)) * 12 / (n ** 2)
    return vectorD
