from collections import deque, defaultdict
from functions import *
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
    def __init__(self, tiempo, lote, tipo, descarga=None, sorting=None,
                 secador=None, modulo=None):
        self.tiempo = tiempo
        self.lote = lote
        self.tipo = tipo

        self.descarga = descarga
        self.sorting = sorting
        self.modulo = modulo
        self.secador = secador


'''
Entidad que representa un lote de maíz.
'''
class Lote:

    id_counter = 0

    def __init__(self, tipo, gmo, tiempo_llegada, ):
        self.tipo = tipo
        self.gmo = gmo
        self.__humedad = humedad_lote()
        self.carga = carga_camion()
        self.tiempo_llegada = tiempo_llegada
        self.id = self.generate_id()

    def generate_id(self):
        Lote.id_counter += 1
        return self.id_counter

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
            return self.lote_actual.carga / self.velocidad

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


class LineaDesgrane(Linea):
    def __init__(self):
        super().__init__()
        self.velocidad = velocidad_desgrane

    def tiempo_limpieza_por_hibrido(self):
        return limpieza_hibrido_desgrane()


'''
Clase que representa una línea de sorting.
SUPUESTO: las líneas de sorting son indiferentes a GMO/No-GMO. Es decir, todas
sierven para ambos tipos.
'''
class LineaSorting(Linea):
    def __init__(self, automatica):
        super().__init__()
        self.velocidad = velocidad_sorting_automatico if automatica \
                         else velocidad_sorting_manual
        self.tiempo_final_sorting = float('inf')



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
    Asigna un deque de dicts de formato [{tipo, gmo, tiempo_entre_llegadas}] al
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
            self.tiempo_hasta_proxima_llegada = x['tiempo_entre_llegadas']
            return x
        else:
            self.tiempo_hasta_proxima_llegada = float('inf')
            return None

    '''
    Representa la llegada de un camión a la planta. Crea la entidad camión y
    retorna un evento de tipo "llegada_camion".
    '''
    def entregar_lote(self, tiempo_actual):
        entidad_siguiente = self.entidad_siguiente
        attrs = False
        if entidad_siguiente is not None:
            attrs = list(self.entidad_siguiente.values())
        if not attrs:
            return None
        lote = self.generar_camion(*attrs)
        lote.tiempo_llegada += tiempo_actual
        self.entidad_siguiente = self.proxima_entidad()
        return self.generar_evento_llegada(lote)


'''
Módulo que representa el proceso de descarga.
'''
class Descarga:
    def __init__(self):
        self.cola = deque()
        self.lineas = self.generar_lineas_descarga()  # diccionario {n: linea_n}

        self.lineas_ocupadas = 0

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

    '''
    Retorna una lista con los números de las líneas desocupadas.
    '''
    def lineas_desocupadas(self):
        return [u for u, v in self.lineas.items() if not v.ocupada()]

    '''
    Retorna un diccionario cuyas keys son los tipos de híbrido pasando por las
    líneas, y sus values son los números de las líneas correspondientes.
    '''
    def hibridos_pasando(self):
        return {linea.tipo_hibrido: n for n, linea in self.lineas.items()}

    '''
    Retorna (Lote(), num_línea) correspondiente al lote que debe pasar más
    próximamente. Si num_línea es None, no va dirigido específicamente. Si no lo
    es, debe ir a la línea correspondiente.
    
    No considera GMO/No-GMO.
    '''
    def asignar_lote_siguiente(self):
        if not len(self.cola):
            raise ValueError('Intentando asignar un lote inexistente')

        indice = 0
        hibridos_pasando = self.hibridos_pasando()
        for lote in self.cola:
            if lote.tipo in hibridos_pasando:
                linea_correspondiente = hibridos_pasando[lote.tipo]
                self.cola = list(self.cola)
                x = self.cola.pop(indice)
                self.cola = deque(self.cola)
                return x, linea_correspondiente
            indice += 1

        return self.cola.popleft(), None

    '''
    Retorna el número de la primera línea que está desocupada.
    '''
    def asignar_linea_arbitraria(self):
        for n, linea in self.lineas.items():
            if not linea.ocupada():
                return n
        raise ValueError('Todas las líneas están ocupadas.')

    def generar_evento_comienzo_descarga(self, clock, lote):
        return Evento(clock, lote, 'comienza_descarga',)

    '''
    Comienza la descarga de un camión. Retorna un Evento('termina_descarga').
    '''
    def comenzar_descarga(self, clock):
        if not len(self.cola):
            return None

        lote, n = self.asignar_lote_siguiente()
        if n is None:
            n = self.asignar_linea_arbitraria()

        linea = self.lineas[n]
        linea.lote_actual = lote
        linea.tipo_hibrido = lote.tipo

        print(f'Se asigna Lote({lote.id}) a la línea de descarga {n}.')

        tiempo_limpieza = 0
        if lote.tipo != linea.tipo_hibrido:
            tiempo_limpieza += linea.tiempo_limpieza_por_hibrido()
        tiempo_procesamiento = linea.tiempo_en_pasar() + tiempo_limpieza

        return Evento(clock + tiempo_procesamiento, lote,
                      'termina_descarga', descarga=n)


    '''
    Despeja la línea correspondiente. Retorna un Evento('comienza_sorting'),
    '''
    def terminar_descarga(self, lote, n, clock):
        self.lineas[n].desocupar()
        print(f'Desocupando línea de descarga {n}.')
        return Evento(clock, lote, 'comienza_sorting')


'''
Módulo que representa el proceso de sorting.
'''
class Sorting:
    def __init__(self):
        self.lineas = self.generar_lineas_sorting()

    '''
    Genera 2 líneas de sorting automáticas (1, 2) y 2 manuales (3, 4). Crea un 
    diccionario para poder acceder a ellas.
    '''
    def generar_lineas_sorting(self):
        linea_1, linea_2 = LineaSorting(True), LineaSorting(True)
        linea_3, linea_4 = LineaSorting(False), LineaSorting(False)
        return {1: linea_1, 2: linea_2, 3: linea_3, 4: linea_4}

    '''
    Retorna una lista con los números de las líneas desocupadas.
    '''
    def lineas_desocupadas(self):
        return [u for u, v in self.lineas.items() if not v.ocupada()]

    '''
    Asigna una línea a un proceso. Asigna en orden creciente (ya que las
    automáticas corresponden a la 1 y 2).
    '''
    def asignar_linea_sorting(self):
        for n, linea in self.lineas.items():
            if not linea.ocupada():
                return n
        raise ValueError('Todas las líneas de Sorting están ocupadas.')

    '''
    Recibe un lote desde una línea de descarga en alguna de las líneas de
    sorting. Retorna un Evento('termina_sorting')
    '''
    def comenzar_sorting(self, lote, clock):
        n = self.asignar_linea_sorting()
        linea = self.lineas[n]
        linea.lote_actual = lote

        tiempo_procesamiento = linea.tiempo_en_pasar()

        print(f'Se asigna Lote({lote.id}) a la línea de sorting {n}')

        return Evento(clock + tiempo_procesamiento, lote,
                      'termina_sorting', sorting=n)


    '''
    Entrega un lote a alguna de las unidades de secado.
    SUPUESTO: no hay almacenamiento de inventario entre sorting y secado.
    '''
    def terminar_sorting(self, lote, n, clock):
        self.lineas[n].desocupar()
        print(f'Desocupando línea de sorting {n}.')
        return Evento(clock, lote, 'comienza_secado')



















'''
Clase que representa un módulo de un secador.
'''
class Modulo:
    def __init__(self, gmo, capacidad):
        self.gmo = gmo
        self.capacidad = capacidad
        self.velocidad = velocidad_secado
        self.lotes = []
        self.iniciado = False
        self.terminado = None
        self.tipo_hibrido = None
        self.carga = 0
        self.tiempo_inicio_carga = None

    '''
    Calcula la humedad de los lotes presentes en el módulo.
    SUPUESTO: la humedad inicial de un conjunto de lotes es el promedio
    ponderado por las cargas de los lotes que lo componen.
    '''
    def humedad_inicial(self):
        carga_total = sum([lote.carga for lote in self.lotes])
        return sum([lote.humedad * (lote.carga / carga_total) for
                    lote in self.lotes])

    '''
    Calcula el tiempo de secado según el conjunto de lotes en el módulo.
    '''
    def tiempo_secado(self):
        return self.humedad_inicial() / self.velocidad

    '''
    Agrega un lote a la lista de lotes dentro del módulo.
    '''
    def cargar(self, lote, clock=None):
        if self.ocupado():
            if lote.tipo != self.tipo_hibrido:
                raise ValueError('Intentando cargar módulo con distintos tipos '
                                 'de híbrido.')
        else:
            self.tipo_hibrido = lote.tipo
        self.lotes.append(lote)
        self.carga += lote.carga
        self.terminado = False
        if self.tiempo_inicio_carga is None:
            self.tiempo_inicio_carga = clock

    '''
    Abre el módulo, una vez terminado el proceso de secado.
    '''
    def abrir(self):
        self.terminado = True

    '''
    Vacía el módulo y actualiza parámetros correspondientes. Retorna el tipo
    de híbrido que contenía el módulo antes de vaciarse.
    '''
    def vaciar(self):
        tipo_anterior = self.tipo_hibrido

        self.lotes = []
        self.iniciado = False
        self.terminado = None
        self.tipo_hibrido = None
        self.tiempo_inicio_carga = None
        self.carga = 0

        return tipo_anterior

    '''
    Retorna True si el módulo está ocupado, False en caso contrario.
    '''
    def ocupado(self):
        if self.lotes:
            return True
        return False

    '''
    Cierra el módulo e inicia el secado. Retorna evento de término de secado.
    '''
    def iniciar_secado(self, n, m, clock):
        self.iniciado = True
        tiempo_proceso = self.tiempo_secado()
        return Evento(clock + tiempo_proceso, None, 'termina_secado',
                      secador=n, modulo=m)


'''
Clase que representa un secador con sus respectivos módulos.
'''
class Secador:
    def __init__(self, gmo, cantidad, capacidad):
        self.gmo = gmo
        self.capacidad = capacidad
        self.modulos = self.generar_modulos(cantidad, capacidad)
        self.hibridos_contenidos = defaultdict(list)
        self.modulos_vacios = len(self.modulos)

    '''
    Genera los módulos correspondientes al secador.
    '''
    def generar_modulos(self, cantidad, capacidad):
        return {n: Modulo(self.gmo, capacidad) for n in range(1, cantidad+1)}

    '''
    Carga el lote en el módulo m.
    '''
    def lote_a_modulo(self, lote, m, clock):
        modulo = self.modulos[m]
        modulo.cargar(lote, clock)
        self.hibridos_contenidos[lote.tipo].append(m)
        return True



'''
Clase que representa el proceso de Secado.
'''
class Secado:
    def __init__(self):
        self.secadores = self.generar_secadores()

    ''' 
    Genera los 5 secadores correspondientes al proceso de Secado.
    '''
    def generar_secadores(self):
        secador_1 = Secador(True, cantidad_modulos_secador_1,
                            capacidad_modulos_secador_1)
        secador_2 = Secador(True, cantidad_modulos_secador_2,
                            capacidad_modulos_secador_2)
        secador_3 = Secador(True, cantidad_modulos_secador_3,
                            capacidad_modulos_secador_3)
        secador_4 = Secador(False, cantidad_modulos_secador_4,
                            capacidad_modulos_secador_4)
        secador_5 = Secador(False, cantidad_modulos_secador_5,
                            capacidad_modulos_secador_5)
        return {1: secador_1, 2: secador_2, 3: secador_3, 4: secador_4,
                5: secador_5}

    '''
    Retorna tupla (n_secador, m_módulo) según dónde deba dirigirse el lote. Si
    no hay una dirección específica, retorna None.
    '''
    def dirigir_especifico(self, lote):
        for n, secador in self.secadores.items():
            if lote.tipo in secador.hibridos_contenidos:
                lista_modulos = secador.hibridos_contenidos[lote.tipo]
                for m in lista_modulos:
                    if not secador.modulos[m].iniciado:
                        return n, m
        return None

    '''
    Retorna tupla (n_secador, m_módulo) según disponibilidad.
    '''
    def asignar_segun_disponibilidad(self, lote):
        for n, secador in self.secadores.items():
            if secador.modulos_vacios:
                for m, modulo in secador.modulos.items():
                    if not modulo.carga:
                        return n, m
        return None

    '''
    Carga el lote en el módulo m del secador n. Retorna un evento de cierre de
    módulo.
    '''
    def lote_a_secador(self, lote, n, m, clock):
        secador = self.secadores[n]
        evento = secador.lote_a_modulo(lote, m, clock)
        if evento:
            return

    '''
    Carga el lote en el secador y módulo que correspondan. Retorna un evento de
    cierre de módulo.
    '''
    def recibir_lote(self, lote, clock):
        especifico = self.dirigir_especifico(lote)
        if especifico is not None:
            n, m = especifico
        else:
            disponibilidad = self.asignar_segun_disponibilidad(lote)
            if disponibilidad is None:
                print('No existen módulos disponibles.')
                return None
            n, m = disponibilidad
        evento = self.lote_a_secador(lote, n, m, clock)
        return evento

    '''
    Cierra el módulo correspondiente. Retorna evento de término de secado.
    '''
    def cerrar_modulo(self, n, m, clock):
        modulo = self.secadores[n].modulos[m]
        return modulo.iniciar_secado(n, m, clock)

    '''
    Abre el módulo correspondiente, dejándolo disponible para ser descargado.
    '''
    def abrir_modulo(self, n, m):
        modulo = self.secadores[n].modulos[m]
        modulo.abrir()











    '''
    Se asigna el lote a un modulo. Primero se busca algún modulo que tenga el
    mismo lote, en caso contrario se elige el primero desocupado
    '''
    def asignar_lote_siguiente(self):
        if self.lote_siguiente:
            for numero, secador in self.secadores.items():
                if secador.gmo == self.lote_siguiente.gmo:
                    for numero,modulo in self.secador.modulos.items():
                        if modulo.lote_actual == self.lote_siguiente.tipo and not modulo.iniciado:
                            self.modulo.agregar_hibrido(self.lote_siguiente)
                            break
            for numero, secador in self.secadores.items():
                if secador.gmo == self.lote_siguiente.gmo:
                    for numero, modulo in self.secador.modulos.items():
                        if not modulo.lote_actual:
                            self.modulo.agregar_hibrido(self.lote_siguiente)
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
        self.hornos = deque()
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
        '''
        
        Eliminé el insort_by_index. Sale más eficiente implementar una
        SortedList.
        
        insort_by_index(self.fin_de_desgrane,
                        (n_linea_asignada,
                         linea.lote_actual.tiempo_hasta_fin_proceso), 1)
        '''
        ### Falta agregar cosas###
