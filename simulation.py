from classes import *

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

        self.hibridos_procesados = defaultdict(int)

        '''
        Medidas de desempeño.
        '''
        self.lotes_recibidos = 0
        self.toneladas_procesadas = 0
        self.carga_recibida = 0
        self.carga_perdida = 0
        self.carga_perdida_sorting = 0
        self.carga_perdida_secado = 0
        self.cantidad_camiones = 0
        self.tiempo_procesamiento = 0
        self.lotes_procesados = 0
        self.tiempo_espera = 0
        self.camiones_descargados = 0

        '''
        Lista que permanece siempre ordenada decrecientemente según el atributo
        tiempo de la clase Evento. Para agregar un elemento, lista.add(elem).
        Para retornar el evento de menor tiempo, lista.pop().
        '''
        self.lista_eventos = SortedList(key=lambda x: -x.tiempo)

    '''
    Método que genera instancia de Evento de tipo "siguiente_dia".
    '''
    def avanzar_a_siguiente_dia(self):
        return Evento((self.reloj//24)*24 + 24, None, 'siguiente_dia')

    '''
    Método que resetea las medidas de desempeño de la simulación.
    '''
    def resetear_estadisticas(self):
        self.__init__()

    '''
    Método que resetea las medidas de desempeño de la simulación.
    '''
    def actualizar_estadisticas(self):
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
        dia_actual = 0
        self.lista_eventos.add(siguiente_dia)

        print()
        print('--------------------------------------------------')
        print()
        print('INICIO DE LA SIMULACIÓN.')
        print()
        print('--------------------------------------------------')
        print()

        tiempo_anterior = self.reloj
        while self.reloj < tiempo_simulacion:

            #if tiempo_anterior != self.reloj:
            #    self.actualizar_estadisticas()

            evento_simulacion = self.lista_eventos.pop()
            self.reloj = evento_simulacion.tiempo

            if self.reloj >= tiempo_simulacion:
                break

            print(f'T = {self.reloj}')
            print(f'EJECUTANDO EVENTO: [{evento_simulacion.tipo}]\n')

            if evento_simulacion.tipo == 'siguiente_dia':

                dia_actual += 1
                if not dia_actual % 7:
                    print('Día domingo. No hay llegada de camiones.')

                    evento_siguiente_dia = self.avanzar_a_siguiente_dia()
                    print("Agregando evento [siguiente día] a la lista de "
                          'eventos. Siguiente día comenzará en T = '
                          f'{evento_siguiente_dia.tiempo}.')
                    self.lista_eventos.add(evento_siguiente_dia)

                else:
                    print(f'Generando llegadas del día.')
                    self.llegada.generar_llegadas()

                    evento_llegada = self.llegada.entregar_lote(self.reloj)
                    print(f"Agregando evento [llegada camión] a la lista de "
                          f"eventos. Camión llegará en T = "
                          f"{evento_llegada.tiempo}")
                    self.lista_eventos.add(evento_llegada)

                    evento_siguiente_dia = self.avanzar_a_siguiente_dia()
                    print("Agregando evento [siguiente día] a la lista de "
                          'eventos. Siguiente día comenzará en T = '
                          f'{evento_siguiente_dia.tiempo}.')
                    self.lista_eventos.add(evento_siguiente_dia)

            if evento_simulacion.tipo == 'llegada_camion':
                lote = evento_simulacion.lote
                print(f'Llegando Lote: (ID = {lote.id}; Tipo = {lote.tipo}; '
                      f'Carga = {lote.carga:.5f}; '
                      f'Humedad = {lote.humedad}; GMO = {lote.gmo}; '
                      f'Tiempo = {lote.tiempo_llegada})')
                self.cantidad_camiones += 1
                self.descarga.recibir_lote(lote)

                self.carga_recibida += lote.carga
                self.lotes_recibidos += 1

                if self.descarga.lineas_desocupadas() and \
                   self.sorting.lineas_desocupadas():
                    evento_comienza_descarga = \
                    self.descarga.generar_evento_comienzo_descarga(self.reloj,
                                                                   lote)
                    if evento_comienza_descarga is not None:
                        print('Agregando evento [comienza descarga de Lote'
                              f'({lote.id})] a la lista de eventos. Descarga '
                              f'comenzará en T = '
                              f'{evento_comienza_descarga.tiempo}.')
                        self.lista_eventos.add(evento_comienza_descarga)

                #cola = [c for c in self.descarga.cola]
                #print(f'Cola camiones: {cola}')
                print(f'Largo cola: {len(self.descarga.cola)}')

                evento_sgte_llegada = self.llegada.entregar_lote(self.reloj)
                if evento_sgte_llegada is not None:
                    print(f"Agregando evento [llegada camión] a la lista de "
                          f"eventos. Camión llegará en T = "
                          f"{evento_sgte_llegada.tiempo}")
                    self.lista_eventos.add(evento_sgte_llegada)

            if evento_simulacion.tipo == 'comienza_descarga':
                print(f'Lineas desocupadas antes: '
                      f'{self.descarga.lineas_desocupadas()}')
                print(f'Híbridos pasando antes: '
                      f'{self.descarga.hibridos_pasando()}')

                evento_fin_descarga =\
                    self.descarga.comenzar_descarga(self.reloj)

                print(f'Lineas desocupadas después: '
                      f'{self.descarga.lineas_desocupadas()}')
                print(f'Híbridos pasando después: '
                      f'{self.descarga.hibridos_pasando()}')

                if evento_fin_descarga is not None:
                    id = evento_fin_descarga.lote.id
                    print(f'Comenzando descarga de Lote('
                          f'{evento_fin_descarga.lote.id}) por línea '
                          f'{evento_fin_descarga.descarga}.')

                    #cola = [c for c in self.descarga.cola]
                    #print(f'Cola camiones: {cola}')
                    print(f'Largo cola: {len(self.descarga.cola)}')

                    print(f'Agregando evento [terminar descarga de Lote({id})]'
                          ' a la lista de eventos. Descarga terminará en T = '
                          f'{evento_fin_descarga.tiempo}.')
                    self.lista_eventos.add(evento_fin_descarga)

                    self.camiones_descargados += 1
                    self.tiempo_espera += \
                        (self.reloj - evento_fin_descarga.lote.tiempo_llegada)

            if evento_simulacion.tipo == 'termina_descarga':
                lote, n = evento_simulacion.lote, evento_simulacion.descarga
                print(f'Descarga de lote {lote.id} por línea {n} terminada.')
                evento_inicio_sorting = self.descarga.terminar_descarga(
                                        lote, n, self.reloj)
                print(f'Agregando evento [comienza sorting de Lote({lote.id})] '
                      'a la lista de eventos. Sorting comenzará en T = '
                      f'{evento_inicio_sorting.tiempo}.')
                self.lista_eventos.add(evento_inicio_sorting)

                if self.descarga.cola and self.sorting.lineas_desocupadas():

                    evento_comienza_descarga = \
                        self.descarga.generar_evento_comienzo_descarga(
                                                            self.reloj, lote)
                    if evento_comienza_descarga is not None:
                        print(f'Agregando evento [comienza descarga] '
                              f'a la lista de eventos. Descarga '
                              f'comenzará en T = '
                              f'{evento_comienza_descarga.tiempo}.')
                        self.lista_eventos.add(evento_comienza_descarga)

            if evento_simulacion.tipo == 'comienza_sorting':
                if self.sorting.lineas_desocupadas():
                    evento =\
                        self.sorting.comenzar_sorting(evento_simulacion.lote,
                                                      self.reloj)
                    print(f'Comenzando proceso de sorting de lote'
                          f' {evento.lote.id}.')
                    print(f'Agregando evento [termina sorting de Lote('
                          f'{evento.lote.id})] a la lista de eventos. Sorting '
                          f'terminará en T = {evento.tiempo}')
                    self.lista_eventos.add(evento)
                else:
                    evento_perdida = Evento(self.reloj, evento_simulacion.lote,
                                            'perdida_carga', sorting=1)
                    print(f'Agregando evento [pérdida de Lote'
                          f'({evento_simulacion.lote.id})] a la lista de evento'
                          f's. Pérdida ocurrirá en T = {evento_perdida.tiempo}')
                    self.lista_eventos.add(evento_perdida)

            if evento_simulacion.tipo == 'termina_sorting':
                id = evento_simulacion.lote.id
                print(f'Terminando proceso de sorting de Lote({id})')

                evento_llenar_modulo = self.sorting.terminar_sorting(
                                                evento_simulacion.lote,
                                                evento_simulacion.sorting,
                                                self.reloj)
                self.lista_eventos.add(evento_llenar_modulo)
                print(f'Lineas de sorting desocupadas: '
                      f'{self.sorting.lineas_desocupadas()}')
                print('Agregando evento [llenar modulo con Lote('
                      f'{evento_llenar_modulo.lote.id})] a la lista de '
                      f'eventos. Llenado de módulo se ejecutará en T = '
                      f'{evento_llenar_modulo.tiempo}.')

                if self.descarga.cola and self.sorting.lineas_desocupadas():

                    evento_comienza_descarga = \
                        self.descarga.generar_evento_comienzo_descarga(
                                                            self.reloj)
                    if evento_comienza_descarga is not None:
                        print(f'Agregando evento [comienza descarga] '
                              f'a la lista de eventos. Descarga '
                              f'comenzará en T = '
                              f'{evento_comienza_descarga.tiempo}.')
                        self.lista_eventos.add(evento_comienza_descarga)

                # SUPUESTO: se gatilla descarga cuando se libera una línea de
                # sorting y existe una línea de descarga desocupada.

            if evento_simulacion.tipo == 'llenar_modulo':
                lote = evento_simulacion.lote
                evento_cierre_modulo = self.secado.recibir_lote(lote,
                                                                self.reloj)

                '''
                for n, secador in self.secado.secadores.items():
                    if secador.hibridos_contenidos:
                        print(f'Secador({n}): {dict(secador.hibridos_contenidos)}')
                '''

                if evento_cierre_modulo is not None:
                    self.lista_eventos.add(evento_cierre_modulo)

            if evento_simulacion.tipo == 'comienza_secado_por_tiempo' \
               or evento_simulacion.tipo == 'comienza_secado_por_capacidad':

                n, m = evento_simulacion.secador, evento_simulacion.modulo
                evento_termina_secado = \
                    self.secado.cerrar_modulo(n, m, self.reloj)
                print(f'Cerrando Módulo({m}) del Secador({n}).')
                self.lista_eventos.add(evento_termina_secado)
                print(f'Agregando evento [termina secado de Módulo({m}) de '
                      f'Secador({n})] a la lista de eventos. Secado '
                      f'terminará en T = '
                      f'{evento_termina_secado.tiempo}.')

            if evento_simulacion.tipo == 'termina_secado':

                # Falta agregar que módulos se cierren por capacidad o tiempo.
                # y que un evento cancele al otro.
                n, m = evento_simulacion.secador, evento_simulacion.modulo
                if self.secado.secadores[n].modulos[m].lote_mezclado is None:
                    raise ValueError(f'No hay carga en Módulo({m}) '
                                     f'de Secador({n}).\n')

                self.secado.abrir_modulo(n, m, self.reloj)
                #print('Terminando secado.')
                print(f'{len(self.secado.esperando_descarga)} módulos '
                      f'esperando descarga.')

                linea_desgrane = self.desgrane.linea_disponible()
                if linea_desgrane is not None:
                    evento_comienza_desgrane =\
                        self.desgrane.comenzar_desgrane(self.reloj)
                    self.lista_eventos.add(evento_comienza_desgrane)

            if evento_simulacion.tipo == 'comienza_desgrane':
                n, m, lote = self.secado.esperando_descarga.pop()
                print(f'Comenzando desgrane de LoteMezclado({lote.id}) desde'
                      f'Módulo({m}) en Secador({n}).')
                print(f'{len(self.secado.esperando_descarga)} otros módulos '
                      f'esperando descarga.')

                evento_termina_desgrane =\
                    self.desgrane.recibir_lote(lote, n, m, self.reloj)
                self.lista_eventos.add(evento_termina_desgrane)
                print(f'Agregando evento [termina desgrane de '
                      f'LoteMezclado({lote.id}) por '
                      f'Línea({evento_termina_desgrane.desgrane})] a la lista '
                      f'de eventos. Desgrane terminará en T = '
                      f'{evento_termina_desgrane.tiempo}.')

            if evento_simulacion.tipo == 'termina_desgrane':
                n, m = evento_simulacion.secador, evento_simulacion.modulo
                l = evento_simulacion.desgrane
                print(f'Terminando desgrane por Línea({l}).')

                evento_vaciar_modulo =\
                    self.desgrane.terminar_desgrane(l, n, m, self.reloj)
                self.lista_eventos.add(evento_vaciar_modulo)

                lote = evento_simulacion.lote
                self.hibridos_procesados[lote.tipo] += lote.carga
                self.toneladas_procesadas += lote.carga
                print(f'Agregando LoteMezclado(ID = {lote.id}; '
                      f'Carga = {lote.carga}) a la lista de lotes procesados.')

                for componente in lote.componentes:
                    self.lotes_procesados += 1
                    self.tiempo_procesamiento += \
                        (self.reloj - componente.tiempo_llegada)

                linea_desgrane = self.desgrane.linea_disponible()
                if linea_desgrane is not None:
                    if self.secado.esperando_descarga:
                        evento_comienza_desgrane = \
                            self.desgrane.comenzar_desgrane(self.reloj)
                        self.lista_eventos.add(evento_comienza_desgrane)
                        print('Agregando evento [comienza desgrane] a la lista '
                              'de eventos. Desgrane comenzará en T = '
                              f'{evento_comienza_desgrane.tiempo}')

            if evento_simulacion.tipo == 'vaciar_modulo':
                n, m = evento_simulacion.secador, evento_simulacion.modulo
                self.secado.vaciar_modulo(n, m, self.reloj)

                '''
                for n, secador in self.secado.secadores.items():
                    if secador.hibridos_contenidos:
                        print(f'Secador({n}): {secador.hibridos_contenidos}')
                '''

            if evento_simulacion.tipo == 'perdida_carga':
                lote = evento_simulacion.lote
                print(f'Se pierden {lote.carga} toneladas de híbrido de '
                      f'Lote({lote.id}) de tipo {lote.tipo} por no existir ',
                      end='')

                self.carga_perdida += lote.carga

                if evento_simulacion.sorting:
                    print('líneas desocupadas en el área de sorting.')
                    print(f'Lineas de sorting desocupadas: '
                          f'{self.sorting.lineas_desocupadas()}')

                    self.carga_perdida_sorting += lote.carga

                elif evento_simulacion.secado:
                    print('no existir módulos disponibles en el área de secado.'
                          )
                    self.carga_perdida_secado += lote.carga



            tiempo_anterior = self.reloj

            print()
            print('-------------------------')
            print()

        print('FIN DE LA SIMULACIÓN.')
        print()
        print('--------------------------------------------------')
        print()

        dias = tiempo_simulacion/24

        print(f'Tons recibidas: {self.carga_recibida}')
        print(f'Tons procesadas: {self.toneladas_procesadas}')
        print(f'Tons perdidas en sorting: {self.carga_perdida_sorting}')
        print(f'Tons perdidas en secado: {self.carga_perdida_secado}')
        print(f'Tons totales perdidas: {self.carga_perdida}')
        print(f'Tons en proceso: '
        f'{self.carga_recibida-self.carga_perdida-self.toneladas_procesadas}')
        print(f'Camiones recibidos: {self.cantidad_camiones}')
        tipos_hibrido = list(self.hibridos_procesados.keys())
        print(f'Cantidad de tipos de híbrido recibidos: {len(tipos_hibrido)}')

        print()

        print(f'Tiempo de procesamiento promedio: '
              f'{self.tiempo_procesamiento/self.lotes_procesados}')
        print(f'Tons promedio recibidas por día: '
              f'{self.carga_recibida / dias}')
        print(f'Tons promedio procesadas por día: '
              f'{self.toneladas_procesadas / dias}')
        print(f'Tons promedio perdidas en sorting por día: '
              f'{self.carga_perdida_sorting / dias}')
        print(f'Tons promedio perdidas en secado por día: '
              f'{self.carga_perdida_secado / dias}')
        print(f'Tons promedio perdidas por día: '
              f'{self.carga_perdida / dias}')
        print(f'Tiempo promedio de espera camiones: '
              f'{self.tiempo_espera / self.camiones_descargados}')
