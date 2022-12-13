#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:23:37 2022

@author: claraschneuwly
"""

import numpy as np
import itertools

# Leer archivo .txt

my_file = open("nodos.txt", "r")
data = my_file.read()
lines = data.split("\n")
my_file.close()

# Cantidad de metros maximo 

m = 2

#Definir clases para representar un grafo en python

class Vertex:
  def __init__(self, key):
      self.key = key
      self.adjacents = dict()

  def add_neighbour(self, node, dist):
      self.adjacents[node] = dist

  def get_neighbours(self):
      return self.adjacents.keys()

  def get_weight(self, node):
      return self.adjacents[node]

  def is_adjacent(self, node):
      """Return True if this vertex is adjacent to node."""
      if node in self.adjacents.keys():
        return True
      else:
        return False


class Graph:
  def __init__(self):
    self.V = {}
 
  def add_vertex(self, key):
      vertex = Vertex(key)
      self.V[key] = vertex

  def get_vertex(self, key):
      return self.V[key]

  def node_in_graph(self, key):
      return key in self.V

  def add_edge(self, node1, node2, dist):
      self.V[node1].add_neighbour(self.V[node2], dist)

  def is_adjacent(self, node1, node2):
      return self.V[node1].is_adjacent(self.V[node2])
  
  def get_pairs(self):
    res = []
    final_dist = 0
    done = []
    for node in self.V.values():
      neighbours = node.get_neighbours()
      for neighbour in neighbours:
        if neighbour not in done:
          dist = node.get_weight(neighbour)
          res += [[node.key,neighbour.key,dist]]
          final_dist += dist
      done += [node]
    return res, final_dist


# Implementacion del agoritmo de Prim

def prim(G):

    res = Graph()

    nearest_neighbour = {}
    smallest_distance = {}

    unvisited = set(G.V.values())
 
    temp = list(G.V.values())[0]
    res.add_vertex(temp.key)
    unvisited.remove(temp)
 
    for node in temp.get_neighbours():
        if node is temp:
            continue
        nearest_neighbour[node] = res.get_vertex(temp.key)
        smallest_distance[node] = temp.get_weight(node)
 
    while (smallest_distance):
        
        # get nearest vertex outside the MST
        outside = min(smallest_distance, key=smallest_distance.get)
        
        # get the nearest neighbour inside the MST
        inside = nearest_neighbour[outside]
 
        # add a copy of the outside vertex to the MST
        res.add_vertex(outside.key)
        # add the edge to the MST
        res.add_edge(outside.key, inside.key, smallest_distance[outside])
        res.add_edge(inside.key, outside.key, smallest_distance[outside])
 
        unvisited.remove(outside)
        del smallest_distance[outside]
        del nearest_neighbour[outside]
 
        for node in outside.get_neighbours():
            if node in unvisited:
                if node not in smallest_distance:
                    smallest_distance[node] = outside.get_weight(node)
                    nearest_neighbour[node] = res.get_vertex(outside.key)
                else:
                    if smallest_distance[node] > outside.get_weight(node):
                        smallest_distance[node] = outside.get_weight(node)
                        nearest_neighbour[node] = res.get_vertex(outside.key)
 
    return res


# Crear el grafo a partir del .txt

def grafo_from_txt(lines):

  graph = Graph()

  for line in lines:

    line = line.split(']')

    a = (line[0]).strip(' []')
    b = (line[1]).strip(' []')
    distancia = int((line[2]).strip(' []'))

    if not graph.node_in_graph(a):
      graph.add_vertex(a)

    if not graph.node_in_graph(b):
      graph.add_vertex(b)

    graph.add_edge(a, b, distancia)
    graph.add_edge(b, a, distancia)

  return graph


def grafo_from_txt_bis(lines,nodes_to_use=None):

  graph = Graph()

  for line in lines:

    line = line.split(']')

    a = (line[0]).strip(' []')
    b = (line[1]).strip(' []')
    distancia = int((line[2]).strip(' []'))

    if a in nodes_to_use:
      if not graph.node_in_graph(a):
        graph.add_vertex(a)

    if b in nodes_to_use:
      if not graph.node_in_graph(b):
        graph.add_vertex(b)

    if a in nodes_to_use and b in nodes_to_use:
      graph.add_edge(a, b, distancia)
      graph.add_edge(b, a, distancia)

  return graph


# Encontrar todo los subconjuntos de nodos posibles

grafo = grafo_from_txt(lines)
nodes = list(grafo.V.keys())

combinations = []

for i in range(len(nodes),1, -1):

  for s in itertools.combinations(nodes, i):
    combinations += [list(s)]

print(combinations)

# Iterar sobre cada conjunto, y encontrar el MST que tiene mas nodos y que tiene costo total <= m

def question_4(combinations,lines,m=25):

  final = {}

  i = 0

  for l in combinations:

    grafo = grafo_from_txt_bis(lines, l)
    Prim = prim(grafo)
    trajectory, distance = Prim.get_pairs()

    if int(distance) <= m:
      final[i] = len(Prim.V.keys())

    i += 1

  mejor = max(final.values())
  respuesta = None
  for j in final.keys():
    if final[j] == mejor:
      respuesta = j
  
  grafo = grafo_from_txt_bis(lines, combinations[respuesta])
  Prim = prim(grafo)
  trajectory, distance = Prim.get_pairs()
  
  return trajectory, distance, len(combinations[respuesta])


# Resultado 

trajectory, distance, s = question_4(combinations,lines,m)

print('Grafo : ' , trajectory)
print('Distancia total : ' , distance, ' metro(s)')
print('Numero de nodos : ', s)