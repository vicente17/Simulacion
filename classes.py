from collections import deque
from functions import *
from bisect import insort
from parameters import *

'''
Insort es una función que inserta eficientemente (O(n)) un elemento en una
lista ordenada. Se usa de la forma insort(lista, elemento). Será útil en el
momento de tener que agregar eventos a una lista de eventos ordenados por tiempo
de ocurrencia.

DETALLE: se debe agregar siempre el tiempo en el reloj al finalizar o comenzar
procesos, para que se refleje el tiempo real de ocurrencia. Es decir, 
clock.t + lote.tiempo_hasta_finalizacion_proceso
'''

################################################################################

'''
Clase que representa un evento que ocurre en la simulación.
'''
class Evento:
    def __init__(self, tiempo, lote, tipo, descarga=None, sorting=None):
        self.tiempo = tiempo
        self.lote = lote
        self.tipo = tipo
        self.linea_descarga = descarga
        self.linea_sorting = sorting

    def diccionario_eventos(self):
        eventos = {
            'llegada_camion': 1,
            'termino_descarga': 2,
            'siguiente_dia': 100
        }

'''
Entidad que representa un lote de maíz.
'''
class Lote:
    def __init__(self, tipo, gmo, tiempo_llegada):
        self.tipo = tipo
        self.gmo = gmo
        self.humedad = humedad_lote()
        self.carga = carga_camion()
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_hasta_fin_proceso = float('inf')

    @property
    def humedad(self):
        return self.__humedad

    @humedad.setter
    def humedad(self, valor):
        if valor < 0:
            self.__humedad = 0
        else:
            self.__humedad = valor


'''
Clase que representa una linea.
'''
class Linea:
    def __init__(self):
        self.tipo_hibrido = None
        self.lote_actual = None
        self.velocidad = 0  # asignar después; depende si es Descarga o Sorting.

    '''
    Retorna True si la linea está ocupada, False en caso contrario.
    '''
    def ocupada(self):
        if self.lote_actual:
            return True
        return False

    '''
    Retorna el tiempo (en horas) que se demorará el lote en pasar por la línea.
    '''
    def tiempo_en_pasar(self):
        if not self.ocupada():
            raise AttributeError('Se le está pidiendo un tiempo de pasada a una'
                                 ' línea desocupada')
        else:
            return self.lote_actual.carga * self.velocidad

    '''
    Desocupa la línea.
    '''
    def desocupar(self):
        self.lote_actual = None


'''
Clase que representa una línea de descarga.
SUPUESTO: no existe limpieza en relación a GMO.
'''
class LineaDescarga(Linea):
    def __init__(self, gmo):
        super().__init__()
        self.gmo = gmo  # indica si es una línea correspondiente a GMO o No-GMO.
        self.velocidad = velocidad_descarga
        self.tiempo_final_descarga = float('inf')

    '''
    Retorna el tiempo de limpieza correspondiente a cambio de híbrido.
    '''
    def tiempo_limpieza_por_hibrido(self):
        return limpieza_hibrido_descarga()


'''
Clase que representa una línea de sorting.
SUPUESTO: las líneas de sorting son indeferentes a GMO/No-GMO. Es decir, todas
sierven para ambos tipos.
'''
class LineaSorting(Linea):
    def __init__(self, automatica):
        super().__init__()
        self.velocidad = velocidad_sorting_automatico if \
            automatica else velocidad_sorting_manual
        self.tiempo_final_sorting = float('inf')

'''
Clase que representa cada modulo del horno
'''

class Modulo(Linea):
    def __init__(self,gmo,capacidad):
        super().__init__()
        self.capacidad = capacidad
        self.velocidad = velocidad_secado
        self.hibridos = []
        self.iniciado = False
        self.cargado = False

    '''
    Funcion que calcula el tiempo de secado de un conjunto de hibridos
    Supuesto : La humedad inicial del secado es el promedio de los hibridos que lo componen.
    '''

    def tiempo_secado_por_hibrido(self):
        humedad=0
        for hibrido in self.hibridos:
            humedad += hibrido.humedad
        humedad = humedad/len(self.hibridos)
        return (humedad-humedad_final_secado)/velocidad_secado

    def agregar_hibrido(self,hibrido):
        self.hibridos.append(hibrido)

    def vaciar(self):
        self.hibridos = []
        self.iniciado = False
        self.cargado = False


class LineaDesgrane(Linea):
    def __init__(self):
        self.velocidad = velocidad_desgrane

    def tiempo_limpieza_por_hibrido(self):
        return limpieza_hibrido_desgrane()


################################################################################

'''
Módulo que representa la llegada de camiones.
'''
class Llegada:
    def __init__(self):
        self.entidad_siguiente = None  # próxima entidad que llegará
        self.tiempo_hasta_proxima_llegada = float('inf')

    '''
    Genera una entidad Lote.
    '''
    def generar_camion(self, tipo, gmo, tiempo_llegada):
        return Lote(tipo, gmo, tiempo_llegada)

    '''
    Genera un evento de tipo "llegada_camion".
    '''
    def generar_evento_llegada(self, lote):
        return Evento(lote.tiempo_llegada, lote, 'llegada_camion')

    '''
    Asigna un deque de tuplas de formato [(tipo, gmo, tiempo_entre_llegadas)] al
    atributo llegadas. Debe ser ejecutado cada día de la simulación.
    '''
    def generar_llegadas(self):
        self.llegadas = deque(llegadas())
        self.entidad_siguiente = self.proxima_entidad()

    '''
    Método que retorna la entidad que llegará próximamente. Si no corresponde
    que lleguen más camiones en el día, retorna None.
    '''
    def proxima_entidad(self):
        if self.llegadas:
            x = self.llegadas.popleft()
            self.tiempo_hasta_proxima_llegada = x[2]
            return x
        else:
            self.tiempo_hasta_proxima_llegada = float('inf')
            return None

    '''
    Representa la llegada de un camión a la planta. Crea la entidad camión y
    retorna un evento de tipo "llegada_camion".
    '''
    def entregar_lote(self):
        attrs = self.entidad_siguiente
        if not attrs:
            return None
        lote = self.generar_camion(*attrs)
        self.entidad_siguiente = self.proxima_entidad()
        return self.generar_evento_llegada(lote)



'''
DESCARGA EN REMODELAMIENTO.
'''




'''
Módulo que representa el proceso de descarga.
'''
class Descarga:
    def __init__(self):
        self.cola = deque()
        self.largo_cola = 0
        self.lineas = self.generar_lineas_descarga()  # diccionario {n: linea_n}
        self.hibridos_pasando = {}  # diccionario {tipo_híbrido: num_línea}
        self.lineas_ocupadas = 0
        self.cola_fin_descargas = deque()

    '''
    Genera 2 líneas de descarga destinadas a GMO, y 2 destinadas a No-GMO. Crea
    un diccionario para poder acceder a ellas.
    '''
    def generar_lineas_descarga(self):
        linea_1, linea_2 = LineaDescarga(True), LineaDescarga(True)
        linea_3, linea_4 = LineaDescarga(False), LineaDescarga(False)
        return {1: linea_1, 2: linea_2, 3: linea_3, 4: linea_4}

    '''
    Recibe a un camión y lo agrega a la cola para las líneas de descarga.
    '''
    def recibir_lote(self, lote):
        self.cola.append(lote)
        self.largo_cola += 1

        '''
        Agregar generación de evento 'termino_descarga'
        '''

    '''
    Retorna el menor tiempo en que una de las líneas termina de descargar.
    '''
    def tiempo_finalizacion_proxima_descarga(self):
        if self.cola_fin_descargas:
            return self.cola_fin_descargas[0].tiempo_hasta_fin_proceso

    '''
    Retorna tupla (lote, linea) correspondiente al siguiente lote a pasar por
    las líneas de descarga y un parámetro que determina si hay una línea en
    específico por la cual debe pasar.
    
    CORRESPONDE A LA DECISIÓN: hacer pasar el lote que corresponda a un híbrido
    que ya está pasando por alguna de las líneas.
    
    NO SE ESTÁ CONSIDERANDO EL HECHO DE QUE LAS LÍNEAS DE DESCARGA CORRESPONDAN
    A GMO/NO-GMO.
    '''
    def asignar_lote_siguiente(self):
        if not len(self.cola):
            raise ValueError('Intentando asignar un lote inexistente')
        self.largo_cola -= 1
        indice = 0
        for lote in self.cola:
            if lote.tipo in self.hibridos_pasando:
                linea_correspondiente = self.hibridos_pasando[lote.tipo]
                if not indice:
                    x = self.cola.popleft()
                else:
                    x = self.cola.pop(indice)
                return x, linea_correspondiente
            indice += 1
        return self.cola.popleft(), None

    '''
    Comienza a descargar un lote en alguna de las líneas, dependiendo si va
    dirigido específicamente a una o no. Agrega el lote a la línea que
    corresponda y appendea en la cola de fin de descargas de manera tal que
    esta quede ordenada según los tiempos.
    '''
    def comenzar_descarga(self):
        lote, n = self.asignar_lote_siguiente()
        if n is not None:
            n_linea_asignada = n
        else:
            '''
            DECISIÓN: elegir línea desocupada de menor número. EVALUAR
            REEMPLAZAR POR PRIORIDAD DE HÍBRIDO.
            
            FALTA AGREGAR TIEMPO DE SIMULACIÓN.
            '''
            n_linea_asignada = None
            for num, linea in self.lineas.items():
                if not linea.ocupada():
                    n_linea_asignada = num
                    break
            if n_linea_asignada is None:
                raise ValueError('Tratando de comenzar descarga cuando no hay '
                                 'líneas desocupadas.')
        linea = self.lineas[n_linea_asignada]
        if n is not None:
            tiempo_limpieza = 0
        else:
            tiempo_limpieza = linea.tiempo_limpieza_por_hibrido()
        lote.tiempo_hasta_fin_proceso = (lote.carga / linea.velocidad) + \
                                        tiempo_limpieza  # sumar clock.t
        self.hibridos_pasando[lote.tipo] = n_linea_asignada
        linea.lote_actual = lote
        linea.tipo_hibrido = lote.tipo
        insort_by_index(self.cola_fin_descargas,
                        (n_linea_asignada,
                         linea.lote_actual.tiempo_hasta_fin_proceso), 1)

    '''
    
    '''
    def terminar_descarga(self, n_linea):
        # eliminar hibrido pasando por linea
        # eliminar lote_Actual en linea
        # ejecutar entregar lote para pasar la entidad al sorting
        pass

    '''
    Entrega un lote a alguna de las líneas de sorting. Se ejecuta en el momento
    en que se termina de descargar un camión.
    SUPUESTO: no hay almacenamiento de inventario entre descarga y sorting.
    '''
    def entregar_lote(self, lote, sorting):
        sorting.recibir_lote(lote)




'''
DESCARGA EN REMODELAMIENTO.
'''




'''
Módulo que representa el proceso de sorting.
'''
class Sorting:
    def __init__(self):
        pass

    '''
    Genera 2 líneas de sorting automáticas y 2 manuales. Crea un diccionario
    para poder acceder a ellas.
    '''
    def generar_lineas_sorting(self):
        linea_1, linea_2 = LineaSorting(True), LineaSorting(True)
        linea_3, linea_4 = LineaSorting(False), LineaSorting(False)
        self.lineas = {1: linea_1, 2: linea_2, 3: linea_3, 4: linea_4}

    '''
    Recibe un lote desde una línea de descarga en alguna de las líneas de
    sorting.
    '''
    def recibir_lote(self):
        pass

    '''
    Entrega un lote a alguna de las unidades de secado.
    SUPUESTO: no hay almacenamiento de inventario entre sorting y secado.
    '''
    def entregar_lote(self):
        pass

'''
Clase que representa un secador con sus respectivos modulos modulos y clases
'''
class Secador:
    def __init__(self,gmo,cantidad,capacidad):
        self.modulos = generar_modulos(cantidad,capacidad)
        self.gmo = gmo

    def generar_modulos(self,cantidad,capacidad):
        for i in range(cantidad):
            modulos = {}
            modulos[i] = Modulo(capacidad)
        return modulos
'''
Módulo que representa el proceso de secado.
'''
class Secado:
    def __init__(self):
        self.secadores =  self.generar_secadores()
        self.lote_siguiente = False

    ''' 
    Se crean los 5 secadores del secado
    '''
    def generar_secadores(self):
        secador_1 = Secador(False,cantidad_modulos_secador_1
                          ,capacidad_modulos_secador_1)
        secador_2 = Secador(False, cantidad_modulos_secador_2,
                          capacidad_modulos_secador_2)
        secador_3 = Secador(False, cantidad_modulos_secador_3,
                          capacidad_modulos_secador_3)
        secador_4 = Secador(True, cantidad_modulos_secador_4,
                          capacidad_modulos_secador_4)
        secador_5 = Secador(True, cantidad_modulos_secador_5,
                          capacidad_modulos_secador_5)
        return {1: secador_1, 2: secador_2, 3: secador_3, 4: secador_4,
                5: secador_5}
    '''
    Se asigna el lote a un modulo, primero se busca algun modulo que tenga el
    mismo lote, en caso contrario se elige el primero desocupado
    '''
    def asignar_lote_siguiente(self):
        if self.lote_siguiente:
            for numero, secador in self.secadores.items():
                if secador.gmo == self.lote_siguiente.gmo:
                    for numero,modulo in self.secador.modulos.items():
                        if modulo.lote_actual == self.lote_siguiente.tipo and not modulo.iniciado:
                            self.modulo.hibridos.append(self.lote_siguiente)
                            break
            for numero, secador in self.secadores.items():
                if secador.gmo == self.lote_siguiente.gmo:
                    for numero, modulo in self.secador.modulos.items():
                        if not modulo.lote_actual:
                            self.modulo.hibridos.append(self.lote_siguiente)
                            break
            print('NO HAY MODULO DISPONIBLE')
'''
Módulo que representa el proceso de desgrane.
'''
class Desgrane:
    def __init__(self):
        self.lineas= self.generar_lineas_desgrane()
        self.hornos_secado_listo: {} #diccionario {1: { 1: tipo ..} 2: { 1:tipo }}
        self.hibridos_pasando = {}  # diccionario {num_linea: hibrido
        self.fin_de_desgrane= deque()
        self.hornos= deque()
    '''
    Creacion de las 2 lineas de desgrane.
    '''
    def generar_lineas_desgrane(self):
        return {1: LineaDesgrane(), 2: LineaDesgrane()}
    '''
    Se asigna el sigueinte lote primero se busca uno del mismo tipo, 
    en segundo lugar se busca el lote de menor tamaño
    '''
    def asignar_lote_siguiente(self):
        contador = 0
        menor = 0
        for lote in self.hornos:
            if lote.tipo in self.hibridos_pasando:
                linea_correspondiente = self.hibridos_pasando[lote.tipo]
                return linea_correspondiente, self.hornos.popleft(contador)
            else:
                contador += 1
                if lote.carga < menor:
                    menor = lote.carga
                    eleccion_lote = lote
        if contador == len(self.hornos):
            return None, self.hornos.remove(eleccion_lote)
    '''
    Si se agrega el tiempo de limpieza y se cambia la el hibrido en la linea    
    '''
    def comenzar_desgrane(self):
        lote, n = self.asignar_lote_siguiente()
        if n is not None:
            n_linea_asignada = n
        else:
            n_linea_asignada = None
            for num, linea in self.lineas.items():
                if not linea.ocupada():
                    n_linea_asignada = num
                    break
            if n_linea_asignada is None:
                raise ValueError('Tratando de comenzar descarga cuando no hay '
                'líneas desocupadas.')
        linea = self.lineas[n_linea_asignada]
        if n is not None:
            tiempo_limpieza = 0
        else:
            tiempo_limpieza = linea.tiempo_limpieza_por_hibrido()
        lote.tiempo_hasta_fin_proceso = (lote.carga / linea.velocidad) + \
                                        tiempo_limpieza  # sumar clock.t
        self.hibridos_pasando[n_linea_asignada] = lote.tipo #Nose si se elimina la otra lines
        insort_by_index(self.fin_de_desgrane,
                        (n_linea_asignada,
                         linea.lote_actual.tiempo_hasta_fin_proceso), 1)
        ### Falta agregar cosas###
