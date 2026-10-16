# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:53:59 2021

@author: Xinmeng Zheng Zhang
"""

import math

class LineException(Exception):
    pass

class MetroException(Exception):
    pass

class Line():
    def __init__(self, stations = [], times = []):
        """
        Constructora de la clase Line que representa las líneas
        de metro de Madrid. Cada línea de metro viene definida con 4 listas: 
        una lista de estaciones, otra de tiempos, la tercera indica el estado
        de las estaciones y la última, el estado de las vías. La creación 
        de objetos de la clase Line inicializa la información de dichos elementos.

        Attributes
        ----------
        station : list
            lista de nombres de estaciones. 
            The default is [].
        time : list
            lista de tiempos del trayecto entre estaciones consecutivas. 
            The default is [].
        station_open : list
            lista de estaciones abiertas y cerradas 
            (True indica abierta y False, cerrada).
        section_open : list
            lista de estaciones transitables o intransitables
            (True indica transitable y False, intransitable)

        Returns
        -------
        None.

        """
        self._station = stations
        self._time = times
        self._station_open = [True]*len(self._station)
        self._section_open = [True]*len(self._station)
        
    def __repr__(self):
        text = ''
        text += f'Estaciones: {self._station}\nTiempos: {self._time}\n'
        text += f'Cerradas: {self.get_closed_stations_l()}\n'
        text += f'Intransitables: {self.get_closed_section_l()}\n'
        return text
    
    def __str__(self):
        text = ''
        for i, e in enumerate(self._station):
            if self._station_open[i] == False:
                text += f'{e} (CERRADA)'
            else:
                text += str(e)
            if i < len(self._station)-1:
                text += ' --> '
        sec_closed = self.get_closed_section_l()
        if len(sec_closed) != 0:
            if len(sec_closed) == 1:
                text += f'\nCorte en línea: {sec_closed[0]}'
            else:
                text += f'\nCorte en línea: {sec_closed[0]}-{sec_closed[-1]}'
        return text
    
    def contains_station(self, e):
        """
        Comprueba si la línea contiene una estación de nombre e.

        Parameters
        ----------
        e : str
            nombre de la estación.

        Returns
        -------
        boolean
            devuelve el valor True la estación está en la línea y False en 
            caso contrario.

        """
        return e in self._station
    
    def previous_e(self, e):
        """
        Devuelve la estación anterior a la dada.

        Parameters
        ----------
        e : str
            nombre de la estación dada.

        Raises
        ------
        LineException
            lanza excepción si la estación e no pertenece a la línea y si la 
            estación e es cabecera de línea.

        Returns
        -------
        str
            nombre de la estación anterior a e.

        """
        if self.contains_station(e):
            i = self._station.index(e)
            if i == 0:
                raise LineException(f'La estación {e} es cabecera de línea.')
            else:
                return self._station[i-1]
        else:
            raise LineException(f'La estación {e} no pertenece a la línea.')
            
    def next_e(self, e):
        """
        Devuelve la estación posterior a la dada.

        Parameters
        ----------
        e : str
            nombre de la estación dada.

        Raises
        ------
        LineException
            lanza excepción si la estación e no pertenece a la línea y si la 
            estación e es la última de la línea.

        Returns
        -------
        str
            nombre de la estación posterior a e.

        """
        if self.contains_station(e):
            i = self._station.index(e)
            if i == len(self._station)-1:
                raise LineException(f'La estación {e} es la última de la línea.')
            else:
                return self._station[i+1]
        else:
            raise LineException(f'La estación {e} no pertenece a la línea.')
        
    def cost_origin2destination(self, start, finish):
        """
        Calcula la cantidad de segundos que se tarda en recorrer el
        trayecto en la línea desde la estación start hasta la estación finish.
        Devuelve None si alguna de las estaciones start o finish está cerrada,
        también si existen estaciones intransitables (algún tramo cerrado entre
                                                      start y finish).

        Parameters
        ----------
        start : str
            nombre de estación origen.
        finish : str
            nombre de estación destino.

        Raises
        ------
        LineException
            lanza excepción si alguna de las estaciones start o finish no 
            pertenece a la línea.

        Returns
        -------
        cost : int
            tiempo en segundos para ir desde start hasta finish.

        """
        if self.contains_station(start) and self.contains_station(finish):
            pos_s = self._station.index(start)
            pos_f = self._station.index(finish)
            if self.station_closed(start) or self.station_closed(finish) or self.section_closed(pos_s, pos_f):
                return None
            else:    
                cost = 0
                if pos_s < pos_f:
                    for i in range(pos_s, pos_f):
                        cost += self._time[i]
                else:
                    for i in range(pos_f, pos_s):
                        cost += self._time[i]
                return cost
        else:
            raise LineException('Alguna de las estaciones no pertenecen a la línea.')
            
    def acceso(self):
        return self._station
    
    def intersection(self, otro):
        """
        Compara dos listas y devuelve una lista nueva con los elementos que tienen
        en común.

        Parameters
        ----------
        otro : list
            otra lista como lo es self.

        Returns
        -------
        common : list
            lista intersección.

        """
        common = []
        for e in self._station:
            if e in otro._station:
                common.append(e)
        return common
    
    def station_closed(self, e):
        """
        Comprueba el estado de una estación es ya cerrada.

        Parameters
        ----------
        e : str
            nombre de la estación.

        Returns
        -------
        closed : boolean
            devuelve True si la estación se encuentra cerrada y False si está abierta.

        """
        closed = True
        pos = self._station.index(e)
        if self._station_open[pos] == True:
            closed = False
        return closed
    
    def section_closed(self, pos_s, pos_f):
        """
        Comprueba si existe alguna estación intransitable
        por tramo cerrado entre la estación inicial y final.

        Parameters
        ----------
        pos_s : int
            índice que indica la posición de la estación inicial.
        pos_f : int
            índice que indica la posición de la estación final.

        Returns
        -------
        closed : boolean
            True si hay algún tramo cerrado, False en caso contrario.

        """
        closed = False
        if pos_s < pos_f:
            for i in range(pos_s+1, pos_f-1):
                if self._section_open[i] == False:
                    closed = True
        else:
            for i in range(pos_f+1, pos_s-1):
                if self._section_open[i] == False:
                    closed = True
        return closed
    
    def close_station_l(self, e):
        """
        Cierra la estación e cambiando su estado a False que indica cerrada.
        Si la estación e ya se encuentra cerrada, el método no tiene 
        ningún efecto.

        Parameters
        ----------
        e : str
            nombre de la estación.

        Returns
        -------
        None.

        """
        if not self.station_closed(e):
            pos = self._station.index(e)
            self._station_open[pos] = False 
        
    def get_closed_stations_l(self):
        """
        Devuelve la lista de estaciones cerradas de la línea.

        Returns
        -------
        st_closed : list
            lista de estaciones cerradas.

        """
        st_closed = []
        for station in self._station:
            if self.station_closed(station):
                st_closed.append(station)
        return st_closed
        
    def open_station_l(self, e):
        """
        Abre la estación e cambiando su estado a True que indica abierta.
        Si la estación e ya se encuentra abierta, el método no tiene 
        ningún efecto.

        Parameters
        ----------
        e : str
            nombre de la estación.

        Returns
        -------
        None.

        """
        if self.station_closed(e):
            pos = self._station.index(e)
            self._station_open[pos] = True 
        
    def close_section_l(self, start, finish):
        """
        Cierra el tramo desde la estación start hasta la estación finish,
        cambiando el estado de las estaciones entre ellas a intransitables.
        Si la línea ya tiene otro tramo cortado, el método no tiene 
        ningún efecto.

        Parameters
        ----------
        start : str
            nombre de la estación donde inicia el tramo.
        finish : str
            nombre de la estación donde termina el tramo.

        Returns
        -------
        None.

        """
        if not self.section_closed(0, len(self._section_open)-1):
            pos_s = self._station.index(start)
            pos_f = self._station.index(finish)
            if pos_s < pos_f:
                for i in range(pos_s, pos_f+1):
                    self._section_open[i] = False
            else:
                for i in range(pos_f, pos_s+1):
                    self._section_open[i] = False
        
    def get_closed_section_l(self):
        """
        Devuelve la lista de estaciones intransitables por tramo cerrado de una línea.

        Returns
        -------
        list_closed : list
            lista de estaciones intransitables.

        """
        list_closed = []
        for i, e in enumerate(self._section_open):
            if e == False:
                station = self._station[i]
                list_closed.append(station)
        return list_closed
        
    def open_section_l(self):
        """
        Abre el tramo cerrado de una línea cambiando el estado de sus estaciones.
        Si la línea no tiene ningún tramo cortado, el método no tiene ningún efecto.

        Returns
        -------
        None.

        """
        for i, e in enumerate(self._section_open):
            if e == False:
                self._section_open[i] = True
        

class Metro():
    def __init__(self):
        self._line = {}
        self._connection = {}
    
    def __repr__(self):
        text = 'LINEAS DE METRO\n'
        for l in self._line:
            text += l + '\n' + repr(self._line[l]) + '\n'
        text += 'CONEXIONES\n'
        for c in self._connection:
            text += c + '\n' + repr(self._connection[c]) + '\n'
        return text
    
    def __str__(self):
        text = 'LINEAS DE METRO\n'
        for l in self._line:
            text += str(l) + '\n' + str(self._line[l]) + '\n'
        text += 'CONEXIONES\n'
        for c in self._connection:
            text += str(c) + '\n' + str(self._connection[c]) + '\n'
        return text
            
    def add_line(self, line_name, line):
        """
        Añade a la red de metro la línea line con el nombre line_name.
        También debe añadir los transbordos existentes entre líneas que comparten
        estaciones invocando al método add_connections().

        Parameters
        ----------
        line_name : str
            clave del elemento del diccionario de líneas.
        line : Line
            valor del elemento del diccionario de líneas.

        Raises
        ------
        MetroException
            lanza excepción si en la red ya existe una línea con el nombre line_name.

        Returns
        -------
        None.

        """
        if line_name in self._line:
            raise MetroException(f'En la red ya existe una línea con el nombre {line_name}')
        else:
            self._line[line_name] = line
            self.add_connections(line_name)
        
    def add_connections(self, line_name):
        """
        Actualiza la información de los transbordos añadiendo los transbordos 
        existentes entre líneas que comparten estaciones a partir de las estaciones 
        de la línea indicada.

        Parameters
        ----------
        line_name : str
            nombre de la línea indicada, que ha sido previamente añadida a la 
            red de metro por el método add_line().

        Returns
        -------
        None.

        """
        for station in self._line[line_name].acceso():
            if station in self._connection:
                self._connection[station].append(line_name)
            else:
                self._connection[station] = [line_name]
        
    @staticmethod
    def load_metro(file_name):
        """
        Método estático que lee el fichero proporcionado y rellena dicha información 
        los dos diccionarios que representan la red de metro.
        
        Parameters
        ----------
        file_name : file
            fichero con los datos de la red de metro.

        Returns
        -------
        metro : Metro
            objeto de clase Metro creado con la información del fichero.

        """
        metro = Metro()
        f = open(file_name, 'r')
        string = f.readline()
        while string != '':
            stations = []
            times = []
            line_name = string.strip()
            string = f.readline()
            list_line = string.strip().split('->')
            for i in range(len(list_line)):
                if i % 2 == 0:
                    stations.append(list_line[i])
                else:
                    times.append(int(list_line[i]))
            line = Line(stations, times)
            metro.add_line(line_name, line)
            string = f.readline()
        f.close()
        return metro
    
    def get_connections(self, e, line_name):
        """
        Devuelve el listado líneas de la red con las que podemos 
        conectar haciendo transbordo desde la estación e de la línea cuyo nombre
        es line_name (comprueba si la estación existe y está donde dice estar).

        Parameters
        ----------
        e : str
            nombre de la estación indicada.
        line_name : str
            nombre de la línea indicada.

        Returns
        -------
        connect : list
            lista de nombres de las líneas con las que está conectado la estación.

        """
        if self.contains_station2(line_name, e):
            if not self._line[line_name].station_closed(e):
                connect = []
                for line in self._connection[e]:
                    if line != line_name:
                        connect.append(line)
                return connect
            else:
                raise MetroException(f'La estación {e} está cerrada y no puede hacer transbordos.')
    
    def cost_origin2destination_transfer(self, start, finish):
        """
        Calcula la cantidad mínima de segundos que se tarda en realizar
        un trayecto que comienza en la estación start y termina en la estación
        finish. Si las estaciones origen y destino no están en la misma línea y
        las líneas a las que pertenecen no tienen estaciones en común, entonces 
        el trayecto implicaría más de un transbordo (trayecto no apto).

        Parameters
        ----------
        start : str
            nombre de estación de origen.
        finish : str
            nombre de estación de destino.

        Raises
        ------
        MetroException
            lanza excepción si alguna de las estaciones start o finish no pertenece
            a la red de metro.

        Returns
        -------
        None
            si el trayecto es no apto (máximo un transbordo por trayecto).
        int
            valor mínimo de tiempo en ruta posible para ir de origen a destino.

        """
        if start in self._connection and finish in self._connection:
            l_costs = []
            for line_s in self._connection[start]:
                for line_f in self._connection[finish]:
                    com_stations = self._line[line_s].intersection(self._line[line_f])
                    if line_s != line_f and len(com_stations) == 0:
                        cost = math.inf
                    elif line_s == line_f:
                        cost = self._line[line_s].cost_origin2destination(start, finish)
                        if cost == None:
                            cost = math.inf
                    else:
                        for station in com_stations:
                            cost1 = self._line[line_s].cost_origin2destination(start, station)
                            cost2 = self._line[line_f].cost_origin2destination(station, finish)  
                            if cost1 == None:
                                cost1 = math.inf
                            elif cost2 == None:
                                cost2 = math.inf
                            cost = cost1 + 300 + cost2      
                    l_costs.append(cost)
            if min(l_costs) != math.inf:
                return min(l_costs)
            else:
                return None
        else:
            raise MetroException('Alguna de las estaciones no pertenece a la red de metro.')
                
    def contains_station2(self, line_name, e):
        """
        Método auxiliar que comprueba si la estación existe en la red de metro 
        y pertenece a la línea indicada que también debe existir en la red.

        Parameters
        ----------
        e : str
            nombre de estación.
        line_name : str
            nombre de línea.

        Raises
        ------
        MetroException
            lanza excepción si la línea line_name no pertenece a la red de metro
            y si la estación e no pertenece a la red de metro.
        LineException
            lanza excepción si la estación e no pertenece a la línea.

        Returns
        -------
        bool
            devuelve True si pasa las tres pruebas.

        """
        if line_name not in self._line:
            raise MetroException(f'La línea {line_name} no existe en la red de metro.')
        elif e not in self._connection:
            raise MetroException(f'La estación {e} no existe en la red de metro.')
        elif not self._line[line_name].contains_station(e):
            raise LineException(f'La estación {e} no pertenece a la línea {line_name}.')
        else:
            return True
        
    def get_line(self, line_name):
        """
        Devuelve un objeto de tipo Line cuyo nombre es line_name.

        Parameters
        ----------
        line_name : str
            nombre de la línea solicitada.

        Raises
        ------
        MetroException
            lanza excepción si la línea line_name no pertenece a la red de metro.

        Returns
        -------
        Line
            línea correspondiente al nombre de línea line_name.

        """
        if line_name in self._line:
            return self._line[line_name]
        else:
            raise MetroException(f'{line_name} no pertenece a la red de metro.')
            
    def close_station(self, line_name, e):
        """
        Primero comprueba si la estación e existe y está en la línea inidicada
        existente también invocando a contains_station2 que devuelve excepciones en 
        casos contrarios. Luego llama a close_station_l para cerrar la estación e.

        Parameters
        ----------
        line_name : str
            nombre de la línea a la que pertenece la estación e.
        e : str
            nombre de la estación a cerrar.

        Returns
        -------
        None.

        """
        if self.contains_station2(line_name, e):
            self._line[line_name].close_station_l(e)
                        
    def get_closed_stations(self, line_name):
        """
        Devuelve la lista de estaciones cerradas de la línea con nombre line_name.

        Parameters
        ----------
        line_name : str
            nombre de la línea.

        Raises
        ------
        MetroException
            lanza excepción si la línea line_name no pertenece a la red de metro.

        Returns
        -------
        list
            lista de estaciones cerradas.

        """
        if line_name in self._line:
           return self._line[line_name].get_closed_stations_l()
        else:
            raise MetroException(f'La línea {line_name} no existe en la red de metro.')
        
    def open_station(self, line_name, e):
        """
        Primero comprueba si la estación e existe y está en la línea inidicada
        existente también invocando a contains_station2 que devuelve excepciones en 
        casos contrarios. Luego llama a open_station_l para abrir la estación e.

        Parameters
        ----------
        line_name : str
            nombre de la línea a la que pertenece la estación e.
        e : str
            nombre de la estación a abrir.

        Returns
        -------
        None.

        """
        if self.contains_station2(line_name, e):
            self._line[line_name].open_station_l(e)
        
    def close_section(self, line_name, start, finish):
        """
        Cierra el tramo de la línea de metro cuyo nombre es line_name
        que comienza en la estación start y termina en la estación finish. Primero
        comprueba si la estación e existe y está en la línea inidicada existente
        también.

        Parameters
        ----------
        line_name : str
            línea a la que pertenece el tramo.
        start : str
            nombre de la estación donde inicia el tramo.
        finish : str
            nombre de la estación donde termina el tramo.

        Returns
        -------
        None.

        """
        if self.contains_station2(line_name, start) and self.contains_station2(line_name, finish):
            self._line[line_name].close_section_l(start, finish)
                
        
    def get_closed_section(self, line_name):
        """
        Devuelve la lista de estaciones intransitables por tramo cerrado de la línea
        con nombre line_name.

        Parameters
        ----------
        line_name : str
            nombre de la línea.

        Raises
        ------
        MetroException
            lanza excepción si la línea line_name no pertenece a la red de metro.

        Returns
        -------
        list
            lista de estaciones cerradas.

        """
        if line_name in self._line:
            return self._line[line_name].get_closed_section_l()
        else:
            raise MetroException(f'La línea {line_name} no existe en la red de metro.')
        
    def open_section(self, line_name):
        """
        Abre el tramo cerrado de la línea de metro cuyonombre es line_name.
        
        Parameters
        ----------
        line_name : TYPE
            DESCRIPTION.

        Raises
        ------
        MetroException
            lanza excepción si la línea line_name no pertenece a la red de metro.

        Returns
        -------
        None.

        """
        if line_name in self._line:
            self._line[line_name].open_section_l()
        else:
            raise MetroException(f'La línea {line_name} no existe en la red de metro.')
                