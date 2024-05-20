from copy import copy

import Utilidad
from Utilidad import notificarPosibleErrorNumerico
from eg import EliminacionGaussiana, SustitucionHaciaAtras
import numpy as np

A = Utilidad.matrizDeFloatsRandom(5, 1, 1000)
A32 = Utilidad.convertirAMatrizDeFloats32(A)

b = Utilidad.vectorDeFloatsRandom(5, 1, 1000)
b32 = Utilidad.convertirAVectorDeFloats32(b)

EliminacionGaussiana.conPivoteo(A, b)
x = SustitucionHaciaAtras.resolver(A, b)

EliminacionGaussiana.conPivoteo(A32, b32)
x32 = SustitucionHaciaAtras.resolver(A32, b32)

print("\n")
print(x)
print("\n")
print(x32)

diferencia = x32 - x
print("\n")
print(diferencia)

diferenciaNormalizada = Utilidad.normaInfinitoDeVector(diferencia)
print(diferenciaNormalizada)

