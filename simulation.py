from classes import *
from sortedcontainers import SortedList

'''
Representa la planta donde ocurren los procesos. El reloj de simulación se
tratará en horas.
'''
class Planta:
    def __init__(self):
        self.reloj = 0

        self.llegada = Llegada()
        self.descarga = Descarga()
        self.sorting = Sorting()
        self.secado = Secado()
        self.desgrane = Desgrane()

        # agregar Medidas de Desempeño

        '''
        Lista que permanece siempre ordenada decrecientemente según el atributo
        tiempo de la clase Evento. Para agregar un elemento, lista.add(elem).
        Para retornar el Evento de menor tiempo, lista.pop().
        '''
        self.lista_eventos = SortedList(key=lambda x: -x.tiempo)


        '''
        Esquema eventos:
        
        - 'siguiente_dia'
          -> Llegadas.generar_llegadas()
          -> evento_llegada = Llegadas.entregar_lote()
          -> self.lista_eventos.add(evento_llegada)
        
        - 'llegada_camion' (lote)
          -> Descarga.recibir_lote(lote)
          -> evento_siguiente_llegada = Llegada.entregar_lote()
             if evento_siguiente_llegada is not None: 
                Planta.lista_eventos.add(evento_siguiente_llegada)
                
        - 'comienza_descarga' (lote)
          -> 
        
        '''


    '''
    Método que genera instancia de Evento de tipo "siguiente_dia".
    '''
    def avanzar_a_siguiente_dia(self):
        return Evento((self.reloj//24)*24 + 24, None, 'siguiente_dia')

    '''
    Método que retorna el tiempo de ocurrencia del próximo evento.
    '''
    def tiempo_proximo_evento(self):
        if not self.lista_eventos:
            raise ValueError('Tratando de retornar tiempo de evento '
                             'inexistente')
        return self.lista_eventos[0].tiempo

    '''
    Método que resetea las estadísticas de la simulación.
    '''
    def resetear_estadisticas(self):
        pass

    '''
    Método que echa a correr la simulación.
    '''
    def simular(self, tiempo_simulacion):
        self.resetear_estadisticas()
        while self.reloj < tiempo_simulacion:
            break
        pass

    '''
    Método que muestra los resultados de la simulacion.
    '''
    def mostrar_estadisticas(self):
        pass

