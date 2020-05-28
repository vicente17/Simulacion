from simulation import *
from time import time
from random import seed

'''
Seteamos una semilla para eliminar la aleatoriedad en cada iteración.
'''
semillas = True
if semillas:
    np.random.seed(0)
    seed(0)

planta = Planta()
print()
inicio = time()

planta.simular(cantidad_dias_simulacion * 24)
planta.mostrar_estadisticas()
final = time()
print()
print(f'Tiempo en correr: {final-inicio:.3f} segundos.\n')
