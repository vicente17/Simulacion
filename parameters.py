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

tiempo_limpieza_sorting_low= 20/60
tiempo_limpieza_sorting_high= 30/20


velocidad_descarga = 3/60  # horas/tonelada

velocidad_sorting_automatico = 5/60  # horas/tonelada
velocidad_sorting_manual = 15/60  # horas/tonelada
velocidad_secado = 0.5/2  # %/horas
velocidad_desgrane= 25/60  #horas/tonelada

cantidad_modulos_secador_1 = 14
capacidad_modulos_secador_1 = 1300  #m^3
cantidad_modulos_secador_2 = 20
capacidad_modulos_secador_2 = 2000  #m^3
cantidad_modulos_secador_3 = 21
capacidad_modulos_secador_3 = 1740  #m^3
cantidad_modulos_secador_4 = 24
capacidad_modulos_secador_4 = 2280  #m^3
cantidad_modulos_secador_5 = 24
capacidad_modulos_secador_5 = 2280  #m^3

toneledas_cierre_modulo = 30
horas_cierre_modulo = 5
humedad_final_secado= 12.5  #%