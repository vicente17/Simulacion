'''
Módulo que contiene los parámetros a usar para la simulación. Deben ser variados
en el momento de realizar el análisis de sensibilidad.

Los tiempos y tasas de llegada serán tratados en horas, los pesos serán tratados
en toneladas.
'''

cantidad_dias_simulacion = 7  # días

duracion_turno = 14  # horas

tasa_llegada = 18/duracion_turno  # llegadas/hora

carga_minima = 10.5  # toneladas
carga_maxima = 21  # toneladas

humedad_inicial_minima = 0.33
humedad_inicial_maxima = 0.35

cantidad_total_tipos_hibrido = 120  # unidades
probabilidad_gmo = 0.5

tipos_hibrido_minimo = 6  # unidades
tipos_hibrido_maximo = 12  # unidades

tiempo_limpieza_descarga_low = 20/60  # horas
tiempo_limpieza_descarga_mid = 30/60  # horas
tiempo_limpieza_descarga_high = 30/60  # horas

tiempo_limpieza_sorting_low = 20/60  # horas
tiempo_limpieza_sorting_high = 30/20  # horas

velocidad_descarga = 20  # toneladas/hora

velocidad_sorting_automatico = 12  # toneladas/hora
velocidad_sorting_manual = 4  # toneladas/hora

velocidad_secado = 0.0025  # unidades/hora
velocidad_desgrane= 60/25  # toneladas/hora

cantidad_modulos_secador_1 = 14  # unidades
cantidad_modulos_secador_2 = 20  # unidades
cantidad_modulos_secador_3 = 21  # unidades
cantidad_modulos_secador_4 = 24  # unidades
cantidad_modulos_secador_5 = 24  # unidades

capacidad_modulos_secador_1 = 1300  # m^3
capacidad_modulos_secador_2 = 2000  # m^3
capacidad_modulos_secador_3 = 1740  # m^3
capacidad_modulos_secador_4 = 2280  # m^3
capacidad_modulos_secador_5 = 2280  # m^3

toneladas_cierre_modulo = 21  # toneladas
horas_cierre_modulo = 5  # horas
humedad_final_secado= 0.125
