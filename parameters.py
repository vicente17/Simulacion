'''
Módulo que contiene los parámetros a usar para la simulación. Deben ser variados
en el momento de realizar el análisis de sensibilidad.

Los tiempos y tasas de llegada serán tratados en horas, los pesos serán tratados
en toneladas.
'''

cantidad_dias_simulacion = 28  # días

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
tiempo_limpieza_sorting_high = 30/60  # horas

tiempo_limpieza_desgrane_low = 20/60  # horas
tiempo_limpieza_desgrane_high = 30/60  # horas

velocidad_descarga = 20  # toneladas/hora

velocidad_sorting_automatico = 12  # toneladas/hora
velocidad_sorting_manual = 4  # toneladas/hora

'''
Cambio velocidad secado para debuggear.
'''
velocidad_secado = 1.75  # unidades/hora
velocidad_desgrane = 25  # toneladas/hora

'''
Cambio las unidades para debuggear
'''

cantidad_modulos_secador_1 = 3  # unidades
cantidad_modulos_secador_2 = 4  # unidades
cantidad_modulos_secador_3 = 2  # unidades
cantidad_modulos_secador_4 = 5  # unidades
cantidad_modulos_secador_5 = 3  # unidades

'''
Divido por 10 la capacidad para debuggear.
'''

capacidad_modulos_secador_1 = 130  # m^3
capacidad_modulos_secador_2 = 200  # m^3
capacidad_modulos_secador_3 = 174  # m^3
capacidad_modulos_secador_4 = 228  # m^3
capacidad_modulos_secador_5 = 228  # m^3

toneladas_cierre_modulo = 21  # toneladas
#horas_cierre_modulo = 5  # horas
humedad_final_secado = 0.125
