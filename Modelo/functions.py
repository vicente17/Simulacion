import numpy as np
from random import shuffle, sample
from collections import deque
from parameters import *

################################################################################
'''
Funciones auxiliares.
'''

def distribucion_llegadas():
    return np.random.exponential(1/tasa_llegada)

def cantidad_hibridos():
    return np.random.randint(tipos_hibrido_minimo, tipos_hibrido_maximo + 1)


def asignacion_hibridos_gmo(ctd_llegadas, ctd_hibridos):
    tipos = sample([c for c in range(1, cantidad_total_tipos_hibrido+1)],
                   ctd_hibridos)
    tipos.extend([tipos[c] for c in np.random.randint(len(tipos),
                                                      size=ctd_llegadas -
                                                           ctd_hibridos)])
    shuffle(tipos)
    gmo = np.random.choice([True, False], ctd_llegadas,
                           p=[probabilidad_gmo, 1 - probabilidad_gmo])
    return list(zip(tipos, gmo))


def tiempos_llegadas(cantidad_tipos_hibrido):
    while True:
        tiempo = 0
        tiempos_entre_llegadas = []
        while True:
            tiempo_hasta_nueva_llegada = distribucion_llegadas()
            tiempo += tiempo_hasta_nueva_llegada
            if tiempo > duracion_turno:
                break
            tiempos_entre_llegadas.append(tiempo_hasta_nueva_llegada)
        if len(tiempos_entre_llegadas) >= cantidad_tipos_hibrido:
            break
    return tiempos_entre_llegadas


################################################################################
'''
Funciones que efectivamente se ocupan.
'''

'''
Retorna una lista de tuplas de formato (hibrido, gmo, tiempo_llegada)
'''
def llegadas():
    ctd = cantidad_hibridos()
    tiempos_llegada = tiempos_llegadas(ctd)
    asignaciones = asignacion_hibridos_gmo(len(tiempos_llegada), ctd)
    return [(u, v, w) for (u, v), w in zip(asignaciones, tiempos_llegada)]

'''
Función que asigna la humedad inicial a un lote.
'''
def humedad_lote():
    return np.random.randint(humedad_inicial_minima,
                             humedad_inicial_maxima + 1) / 100

'''
Función que asigna un peso en toneladas a un lote.
'''
def carga_camion():
    return np.random.uniform(carga_minima, carga_maxima)

'''
Función que retorna el tiempo de limpieza por tipo de híbrido en una linea de
descarga.
'''
def limpieza_hibrido_descarga():
    return np.random.triangular(tiempo_limpieza_descarga_low,
                                tiempo_limpieza_descarga_mid,
                                tiempo_limpieza_descarga_high)

def desired_index(lista, tupla, indice):
    elemento = tupla[indice]
    if lista[0][indice] >= elemento:
        return 0
    for c in range(len(lista)-1):
        if lista[c][indice] <= elemento <= lista[c+1][indice]:
            return c+1
    return len(lista) + 1


def insort_by_index(lista, tupla, indice):
    index = desired_index(lista, tupla, indice)
    lista.insert(index, tupla)


################################################################################

if __name__ == '__main__':
    print('')

