from classes import *
from sortedcontainers import SortedList

'''
Representa la planta donde ocurren los procesos. El reloj de simulación se
tratará en horas.
'''
class Planta:
    def __init__(self):
        self.reloj = -1

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
          -> evento_llegada = Llegadas.entregar_lote(tiempo_actual)
          -> self.lista_eventos.add(evento_llegada)
        
        - 'llegada_camion' (lote)
          -> evento_siguiente_llegada = Llegada.entregar_lote()
             if evento_siguiente_llegada is not None: 
                Planta.lista_eventos.add(evento_siguiente_llegada)
                
          -> Descarga.recibir_lote(lote)
          -> if Descarga.hay_linea_desocupada():
                if Sorting.hay_linea_desocupada():
                   evento_termina_descarga = Descarga.comenzar_descarga()
                   Planta.lista_eventos.add(evento_termina_descarga)
                   
        - 'comienza_descarga' (lote)
          -> generar_evento 'termina_descarga'
          
        - 'termina_descarga'
           -> evento_inicio_sorting = Descarga.terminar_descarga(n, clock)

           -> if Descarga.cola:
                 evento = comenzar_descarga
                 Planta.lista_eventos.add(evento)
                 
        - 'comienza_sorting'
           -> if Sorting.hay_linea_desocupada():
                 'comenzar_sorting'
                 generar evento 'termina_sorting'
              else:
                 desechar_lote
        
           
        - 'termina_sorting'
           -> if Secado.hay_espacio(lote):
                 Secado.agregar_a_modulo
                 
        - 'agregar_a_módulo_secado'
           -> if módulo está inicialmente vacío:
                 generar evento 'comienza_secado' (por tiempo de espera)
                 
              else:
                 if módulo cumple capacidad:
                    'comenzar_secado'
                    
        
                 
           
        
                 
        
        '''


    '''
    Método que genera instancia de Evento de tipo "siguiente_dia".
    '''
    def avanzar_a_siguiente_dia(self):
        return Evento((self.reloj//24)*24 + 24, None, 'siguiente_dia')

    '''
    Método que resetea las estadísticas de la simulación.
    '''
    def resetear_estadisticas(self):
        pass

    '''
    Método que muestra los resultados de la simulacion.
    '''
    def mostrar_estadisticas(self):
        pass

    '''
    Método que echa a correr la simulación.
    '''
    def simular(self, tiempo_simulacion):
        self.resetear_estadisticas()

        siguiente_dia = self.avanzar_a_siguiente_dia()
        self.lista_eventos.add(siguiente_dia)

        while self.reloj < tiempo_simulacion:

            print('###############')
            for evento in self.lista_eventos:
                if evento is not None:
                    print(evento.__dict__)
            print('###############')
            print()

            evento_simulacion = self.lista_eventos.pop()
            self.reloj = evento_simulacion.tiempo

            print(f'Tiempo de simulación: {self.reloj}')
            print(f'Se ejecuta el evento: {evento_simulacion.tipo}')

            if evento_simulacion.tipo == 'siguiente_dia':
                self.llegada.generar_llegadas()
                evento_llegada = self.llegada.entregar_lote(self.reloj)
                self.lista_eventos.add(evento_llegada)

            if evento_simulacion.tipo == 'llegada_camion':
                evento_sgte_llegada = self.llegada.entregar_lote(self.reloj)
                print(evento_sgte_llegada.__dict__)
                if evento_sgte_llegada is not None:
                    self.lista_eventos.add(evento_sgte_llegada)

            if evento_simulacion.tipo == 'comienza_descarga':
                evento_fin_descarga = self.descarga.comenzar_descarga(self.reloj)
                print(evento_fin_descarga.__dict__)
                self.lista_eventos.add(evento_fin_descarga)

            if evento_simulacion.tipo == 'termina_descarga':
                lote, n = evento_simulacion.lote, evento_simulacion.llegada
                evento_inicio_sorting = self.descarga.terminar_descarga(
                                        lote, n, self.reloj)
                self.lista_eventos.add(evento_inicio_sorting)

                if self.descarga.cola:
                    evento = self.descarga.comenzar_descarga(self.reloj)
                    self.lista_eventos.add(evento)

            if evento_simulacion.tipo == 'comienza_sorting':
                if self.sorting.lineas_desocupadas():
                    evento = self.sorting.comenzar_sorting(evento_simulacion.lote,
                                                           self.reloj)
                    self.lista_eventos.add(evento)
                else:
                    print('Se desecha lote')


            if evento_simulacion.tipo == 'termina_sorting':
                self.sorting.terminar_sorting(evento_simulacion.lote,
                                              evento_simulacion.n,
                                              self.reloj)

                # Pasar a secado

            print()
            print('Se termina la iteración.')
            print()
