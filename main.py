from simulation import *
from time import time

'''
Seteamos una semilla para eliminar la aleatoriedad en cada iteración.
'''
semilla = True
if semilla:
    np.random.seed(0)

planta = Planta()
print()
inicio = time()
planta.simular(cantidad_dias_simulacion * 24)
planta.mostrar_estadisticas()
final = time()
print(f'Tiempo en correr: {final-inicio:.3f} segundos.\n')
