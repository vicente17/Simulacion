from classes import *
from sortedcontainers import SortedList
import sys



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

        print('INICIO DE LA SIMULACIÓN.')
        print()
        print('-------------------------')
        print()

        while self.reloj < tiempo_simulacion:

            evento_simulacion = self.lista_eventos.pop()
            self.reloj = evento_simulacion.tiempo

            if self.reloj >= tiempo_simulacion:
                break

            print(f'T = {self.reloj}.')
            print(f'EJECUTANDO EVENTO: [{evento_simulacion.tipo}]\n')

            if evento_simulacion.tipo == 'siguiente_dia':

                print(f'Generando llegadas del día.')
                self.llegada.generar_llegadas()

                evento_llegada = self.llegada.entregar_lote(self.reloj)
                print(f"Agregando evento [llegada camión] a la lista de "
                      f"eventos. Camión llegará en T = "
                      f"{evento_llegada.tiempo}")
                self.lista_eventos.add(evento_llegada)

                evento_siguiente_dia = self.avanzar_a_siguiente_dia()
                print("Agregando evento [siguiente día] a la lista de eventos. "
                      f'Siguiente día comenzará en T = '
                      f'{evento_siguiente_dia.tiempo}.')
                self.lista_eventos.add(evento_siguiente_dia)

            if evento_simulacion.tipo == 'llegada_camion':
                lote = evento_simulacion.lote
                print(f'Llegando Lote(ID = {lote.id}; Carga = {lote.carga:.5f};'
                      f' Humedad = {lote.humedad}; GMO = {lote.gmo}).')
                self.descarga.recibir_lote(evento_simulacion.lote)

                if self.descarga.lineas_desocupadas() and \
                   self.sorting.lineas_desocupadas():
                    evento_comienza_descarga = \
                    self.descarga.generar_evento_comienzo_descarga(self.reloj,
                                                                   lote)
                    if evento_comienza_descarga is not None:
                        print('Agregando evento [comienza descarga de Lote'
                              f'({lote.id}] a la lista de eventos. Descarga '
                              f'comenzará en T = '
                              f'{evento_comienza_descarga.tiempo}.')
                        self.lista_eventos.add(evento_comienza_descarga)

                evento_sgte_llegada = self.llegada.entregar_lote(self.reloj)
                if evento_sgte_llegada is not None:
                    print(f"Agregando evento [llegada camión] a la lista de "
                          f"eventos. Camión llegará en T = "
                          f"{evento_sgte_llegada.tiempo}")
                    self.lista_eventos.add(evento_sgte_llegada)

            if evento_simulacion.tipo == 'comienza_descarga':
                print(f'Comenzando descarga de lote número'
                      f'{evento_simulacion.lote.id} por línea '
                      f'{evento_simulacion.descarga}.')
                evento_fin_descarga = self.descarga.comenzar_descarga(self.reloj)
                if evento_fin_descarga is not None:
                    id = evento_fin_descarga.lote.id
                    print(f'Agregando evento [terminar descarga de Lote({id})]'
                          ' a la lista de eventos. Descarga terminará en T = '
                          f'{evento_fin_descarga.tiempo}.')
                    self.lista_eventos.add(evento_fin_descarga)

            if evento_simulacion.tipo == 'termina_descarga':
                lote, n = evento_simulacion.lote, evento_simulacion.descarga
                print(f'Descarga de lote {lote.id} por línea {n} terminada.')
                evento_inicio_sorting = self.descarga.terminar_descarga(
                                        lote, n, self.reloj)
                print(f'Lineas de descarga desocupadas: '
                      f'{self.descarga.lineas_desocupadas()}')
                print(f'Agregando evento [comienza sorting de Lote({lote.id})] '
                      'a la lista de eventos. Sorting comenzará en T = '
                      f'{evento_inicio_sorting.tiempo}.')
                self.lista_eventos.add(evento_inicio_sorting)

                if self.descarga.cola:
                    evento = self.descarga.comenzar_descarga(self.reloj)
                    id = evento.lote.id
                    print(f'Agregando evento [comienza descarga de Lote({id})]'
                          ' a la lista de eventos. Descarga comenzará en T = '
                          f'{evento.tiempo}.')
                    self.lista_eventos.add(evento)

            if evento_simulacion.tipo == 'comienza_sorting':

                if self.sorting.lineas_desocupadas():
                    evento = self.sorting.comenzar_sorting(evento_simulacion.lote,
                                                           self.reloj)
                    print(f'Comenzando proceso de sorting de lote'
                          f' {evento.lote.id}.')
                    print(f'Agregando evento [termina sorting de Lote('
                          f'{evento.lote.id})] a la lista de eventos. Sorting '
                          f'terminará en T = {evento.tiempo}')
                    self.lista_eventos.add(evento)
                else:
                    print(f'Se desecha Lote({evento_simulacion.lote.id}) por no'
                          f' existir líneas desocupadas en el área de sorting.')

            if evento_simulacion.tipo == 'termina_sorting':
                id = evento_simulacion.lote.id
                print(f'Terminando proceso de sorting de Lote({id})')

                evento_comienza_secado = self.sorting.terminar_sorting(
                                                evento_simulacion.lote,
                                                evento_simulacion.sorting,
                                                self.reloj)
                self.lista_eventos.add(evento_comienza_secado)
                print(f'Lineas de sorting desocupadas: '
                      f'{self.sorting.lineas_desocupadas()}')
                print('Agregando evento [comienza secado de Lote('
                      f'{evento_comienza_secado.lote.id})] a la lista de '
                      f'eventos. Secado comenzará en T = '
                      f'{evento_comienza_secado.tiempo}.')

                if self.descarga.lineas_desocupadas():
                    evento_comienza_descarga = \
                        self.descarga.comenzar_descarga(self.reloj)
                    if evento_comienza_descarga is not None:
                        id_1 = evento_comienza_descarga.lote.id
                        print('Agregando evento [comienza descarga de Lote('
                              f'{id_1})] a la lista de eventos. Descarga '
                              f'terminará en T = '
                              f'{evento_comienza_descarga.tiempo}.')
                        self.lista_eventos.add(evento_comienza_descarga)

                # SUPUESTO: se gatilla descarga cuando se libera una línea de
                # sorting y existe una línea de descarga desocupada.

            if evento_simulacion.tipo == 'comienza_secado':
                pass

            if evento_simulacion.tipo == 'termina_secado':
                pass

            if evento_simulacion.tipo == 'comienza_desgrane':
                pass

            if evento_simulacion.tipo == 'termina_desgrane':
                pass

            print()
            print_eventos_pendientes = False
            if print_eventos_pendientes:
                print('EVENTOS PENDIENTES: ', end='')
                lista = [(evento.tipo, f'T = {evento.tiempo}')
                         for evento in reversed(self.lista_eventos)]
                print(lista)
                print()
            print('-------------------------')
            print()

        print('FIN DE LA SIMULACIÓN.')
