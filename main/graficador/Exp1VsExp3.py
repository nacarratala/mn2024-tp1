import csv

import matplotlib.pyplot as plt
import numpy as np


def graficar(dimensionAComparar):
    with open(
            "/Users/nacarratala/Documents/facultad/metodos 2023-1C/mn-tp1/experimentacion/resultados/experimentacion1.txt",
            'r') as file:
        csvreader1 = csv.reader(file, delimiter=',')
        dimensiones1 = []
        tiempos1 = []
        for row in csvreader1:
            if int(row[0]) == 50 or int(row[0]) == 100 or int(row[0]) == 150 or int(row[0]) == 200 or int(row[0]) == 250:
                dimensiones1.append(row[0])
                tiempos1.append(float(row[1]))
    with open(
            "/Users/nacarratala/Documents/facultad/metodos 2023-1C/mn-tp1/experimentacion/resultados/experimentacion3.txt",
            'r') as file:
        csvreader2 = csv.reader(file, delimiter=',')
        dimensiones2 = []
        tiempos2 = []
        for row in csvreader2:
            if int(row[0]) == 50 or int(row[0]) == 100 or int(row[0]) == 150 or int(row[0]) == 200 or int(row[0]) == 250:
                dimensiones2.append(row[0])
                tiempos2.append(float(row[1]))





        # Set width of bar
        barWidth = 0.25
        # Set position of bar on X axis
        br1 = np.arange(5)
        br2 = [x + barWidth for x in br1]
        # Make the plot
        plt.bar(br1, tiempos1, color='r', width=barWidth, edgecolor='grey', label='Matriz standard')
        plt.bar(br2, tiempos2, color='g', width=barWidth, edgecolor='grey', label='Matriz tridiagonal')
        # Adding Xticks
        plt.xlabel('Dimension', fontweight='bold', fontsize=8, ha='center')
        plt.ylabel('Nanosegundos', fontweight='bold', fontsize=8, ha='center')
        plt.yscale("log")
        plt.xticks([r + barWidth/2 for r in range(5)], [50, 100, 150, 200, 250], ha='center')
        plt.legend()
        plt.show()
