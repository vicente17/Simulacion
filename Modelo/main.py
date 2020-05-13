from simulation import *

'''
Seteamos una semilla para eliminar la aleatoriedad en cada iteración.
'''
semilla = True
if semilla:
    np.random.seed(0)

planta = Planta()
planta.simular(cantidad_dias_simulacion * 24)
