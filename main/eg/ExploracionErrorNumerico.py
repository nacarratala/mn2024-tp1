import matplotlib.pyplot as plt
import numpy as np

import Utilidad
from eg import EliminacionGaussiana, SustitucionHaciaAtras


def ejecutar():
    diferenciasAbsolutas64 = []
    diferenciasAbsolutas32 = []
    errores = [0.000002, 0.000004, 0.000006, 0.000008,
               0.00002, 0.00004, 0.00008, 0.00008,
               0.0002, 0.0004, 0.0006, 0.0008,
               0.002, 0.004, 0.006, 0.008, 0.002,
               0.02,
               1]

    for n in errores:
        # print(n)
        diferenciasAbsolutas = ejecutarParaError(n)
        diferenciasAbsolutas64.append(diferenciasAbsolutas[0])
        diferenciasAbsolutas32.append(diferenciasAbsolutas[1])
    plt.plot(errores, diferenciasAbsolutas64)
    plt.plot(errores, diferenciasAbsolutas32)

    plt.xlabel("n")
    plt.xscale("log")
    plt.ylabel("dif")
    plt.yscale("log")
    plt.show()


def ejecutarParaError(e):
    A64 = generarA64ParaError(e)
    #A32 = Utilidad.convertirAMatrizDeFloats32(A64)
    A32 = generarA32ParaError(e)

    b64 = generarB64()
    #b32 = Utilidad.convertirAVectorDeFloats32(b64)
    b32 = generarB32()

    respuestaEsperada = generarX()

    EliminacionGaussiana.conPivoteo(A64, b64)
    x64 = SustitucionHaciaAtras.resolver(A64, b64)

    EliminacionGaussiana.conPivoteo(A32, b32)
    x32 = SustitucionHaciaAtras.resolver(A32, b32)

    error64 = restaVectoresDeN3(x64, respuestaEsperada)
    #print("Error 64 para " + str(e) + " " + str(error64))
    error32 = restaVectoresDeN3(x32, respuestaEsperada)
    #print("Error 32 para " + str(e) + " " + str(error32))

    diferenciaAbsoluta64 = Utilidad.normaInfinitoDeVector(error64)
    print("Error 64 para " + str(e) + " " + str(diferenciaAbsoluta64))
    diferenciaAbsoluta32 = Utilidad.normaInfinitoDeVector(error32)
    print("Error 32 para " + str(e) + " " + str(diferenciaAbsoluta32))
    return diferenciaAbsoluta64, diferenciaAbsoluta32


def generarA64ParaError(e):
    matriz = [
        [1, 2 + e, 3 - e],
        [1 - e, 2, 3 + e],
        [1 + e, 2 - e, 3]
    ]
    return np.matrix(matriz, dtype=np.float64)


def generarA32ParaError(e):
    matriz = [
        [1, 2 + e, 3 - e],
        [1 - e, 2, 3 + e],
        [1 + e, 2 - e, 3]
    ]
    return np.matrix(matriz, dtype=np.float32)

def generarX():
    x = [1, 1, 1]
    return np.array(x, dtype=np.float64)


def generarB64():
    x = [6, 6, 6]
    return np.array(x, dtype=np.float64)


def generarB32():
    x = [6, 6, 6]
    return np.array(x, dtype=np.float32)


def restaVectoresDeN3(vector1, vector2):
    return [
        vector1[0] - vector2[0],
        vector1[1] - vector2[1],
        vector1[2] - vector2[2]
    ]


ejecutar()
