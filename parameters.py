'''
Módulo que contiene los parámetros a usar para la simulación. Deben ser variados
en el momento de realizar el análisis de sensibilidad.

Los tiempos y tasas de llegada serán tratados en horas, los pesos serán tratados
en toneladas.

CONSIDERACIONES:
- Comienzo de los días coincide con el comienzo de los turnos (T=0 son las 10
  AM)
- Los turnos sólo afectan el periodo en que llegan camiones.
- Cierre de módulos dado únicamente por tiempo de espera.
- Camiones pueden esperar una cantidad infinita de tiempo.
- Proceso parte un lunes; el domingo no llegan camiones, aunque lo demás
  continúa normalmente.
- Se considera que se comienza a descargar cuando se desocupa una línea de
  descarga o llega un camión y además existe una línea de sorting disponible.
- No se hace diferencia entre híbridos GMO y No-GMO.
'''

cantidad_dias_simulacion = 13  # días

duracion_turno = 14  # horas

tasa_llegada = 36/duracion_turno  # llegadas/hora

carga_minima = 10.5  # toneladas
carga_maxima = 21  # toneladas

humedad_inicial_minima = 0.33
humedad_inicial_maxima = 0.35

cantidad_total_tipos_hibrido = 120  # unidades
probabilidad_gmo = 0.5

tipos_hibrido_minimo = 6  # unidades
tipos_hibrido_maximo = 12  # unidades

tolerancia_espera_cola = 12  # horas

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
velocidad_secado = 0.025  # unidades/hora
velocidad_desgrane = 25  # toneladas/hora

'''
Cambio las unidades para debuggear
'''

cantidad_modulos_secador_1 = 3  # unidades
cantidad_modulos_secador_2 = 4  # unidades
cantidad_modulos_secador_3 = 2  # unidades
cantidad_modulos_secador_4 = 5  # unidades
cantidad_modulos_secador_5 = 3  # unidades

capacidad_modulos_secador_1 = 1300  # m^3
capacidad_modulos_secador_2 = 2000  # m^3
capacidad_modulos_secador_3 = 1740  # m^3
capacidad_modulos_secador_4 = 2280  # m^3
capacidad_modulos_secador_5 = 2280  # m^3

toneladas_cierre_modulo = 21  # toneladas
horas_cierre_modulo = 7  # horas
humedad_final_secado = 0.125
