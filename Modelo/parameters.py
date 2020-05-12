'''
Módulo que contiene los parámetros a usar para la simulación. Deben ser variados
en el momento de realizar el análisis de sensibilidad.

Los tiempos y tasas de llegada serán tratados en horas, los pesos serán tratados
en toneladas.
'''

cantidad_dias_simulacion = 7

duracion_turno = 14  # horas

tasa_llegada = 18/duracion_turno  # llegadas/hora

carga_minima = 10.5  # toneladas
carga_maxima = 21

humedad_inicial_minima= 33
humedad_inicial_maxima = 35

cantidad_total_tipos_hibrido = 120
probabilidad_gmo = 0.5

tipos_hibrido_minimo = 6
tipos_hibrido_maximo = 12

tiempo_limpieza_descarga_low = 20/60
tiempo_limpieza_descarga_mid = 30/60
tiempo_limpieza_descarga_high = 30/60

velocidad_descarga = 3/60  # horas/tonelada

velocidad_sorting_automatico = 5/60  # horas/tonelada
velocidad_sorting_manual = 15/60  # horas/tonelada