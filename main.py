from simulation import *
from time import time
from random import seed
import sys
import os

'''
Seteamos una semilla para eliminar la aleatoriedad en cada iteración.
'''
semillas = True
if semillas:
    np.random.seed(0)
    seed(0)

planta = Planta()
print()



printear_pasos = False
if not printear_pasos:
    sys.stdout = open(os.devnull, 'w')  # bloqueamos prints

inicio = time()
planta.simular(cantidad_dias_simulacion * 24)

if not printear_pasos:
    sys.stdout = sys.__stdout__  # reactivamos prints

final = time()

output = True
path_output = 'resultados.txt'
if output:
    orig_stdout = sys.stdout
    f = open(path_output, 'w')
    sys.stdout = f

planta.mostrar_estadisticas()
print()
print(f'Tiempo en correr: {final-inicio:.3f} segundos.\n')

if output:
    sys.stdout = orig_stdout
    f.close()
