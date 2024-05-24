import difusion.Difusion
from experimentacion import Experimentacion5Bis, Experimentacion1, Experimentacion2, Experimentacion3
from graficador import Exp1VsExp3


def main():
    # LaplacianoDiscreto.resolver()
    # Test1.ejecutar()
    # Experimentacion1.ejecutar()
    # Experimentacion2.ejecutar()
    # Experimentacion3.ejecutar()
    # Exp1VsExp3.graficar(50)
    # Experimentacion5Bis.ejecutar()
    # Experimentacion4.ejecutar()
    # Experimentacion5.ejecutar()
    # Experimentacion5Bis.ejecutar()
    #10, 3, 1, 0.1
    #difusion.Difusion.resolverImplicito(101, 10, 1000, 10)
    # 0.05, 0.2, 0.5, 0.50009, 0.75
    difusion.Difusion.resolverExplicito(101, 10, 1000, 0.75)



if __name__ == '__main__':
    main()
