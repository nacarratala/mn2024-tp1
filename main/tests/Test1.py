from copy import copy

from eg import SustitucionHaciaAtras, EliminacionGaussiana
from Utilidad import matrizTridiagonalCompletaDeEnterosRandom, recuperarVectoresAByCDeMatriz, \
    vectorDeEnterosRandom, vectorDeInversosDeTridiagonalPorVectorSolucion


# El objetivo de este test es verificar que la EG tradicional de una matriz tridiagonal devuelva el mismo valor
# que la EG tridiagonal de la dicha matriz. Tambien se chequea que estos resultados coincidan con la solucion
# que genera primero L (producto de haber triangulado) y a partir de ella modifica el vector solucion
def ejecutar():
    n = 10
    matrizTridiagonal = matrizTridiagonalCompletaDeEnterosRandom(n, 1, 50)
    vectoresAByC = recuperarVectoresAByCDeMatriz(matrizTridiagonal)
    vectorA = vectoresAByC[0]
    vectorB = vectoresAByC[1]
    vectorC = vectoresAByC[2]
    copiaDeVectorA = copy(vectorA)
    copiaDeVectorB = copy(vectorB)
    vectorSolucion = vectorDeEnterosRandom(n, 1, 50)
    copia1DeVectorSolucion = copy(vectorSolucion)
    copia2DeVectorSolucion = copy(vectorSolucion)

    EliminacionGaussiana.conPivoteo(matrizTridiagonal, vectorSolucion)
    solucion1 = SustitucionHaciaAtras.resolver(matrizTridiagonal, vectorSolucion)

    EliminacionGaussiana.paraMatrizTridiagonal(vectorA, vectorB, vectorC, copia1DeVectorSolucion)
    solucion2 = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(vectorB, vectorC, copia1DeVectorSolucion)

    vectorDeInversos = EliminacionGaussiana.paraMatrizTridiagonalGenerandoVectorDeInversos(copiaDeVectorA,
                                                                                           copiaDeVectorB, vectorC)
    nuevoVectorSolucion = vectorDeInversosDeTridiagonalPorVectorSolucion(vectorDeInversos, copia2DeVectorSolucion)
    solucion3 = SustitucionHaciaAtras.resolverParaMatrizTridiagonal(copiaDeVectorB, vectorC, nuevoVectorSolucion)

    print(solucion1)
    print(solucion2)
    print(solucion3)

    assert solucion1 == solucion2 == solucion3
