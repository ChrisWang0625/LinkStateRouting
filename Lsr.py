#!/usr/bin/python

import sys
import time
import pickle
from socket import *

node = sys.argv[1]
port = int(sys.argv[2])
input_file = sys.argv[3]
start_time = time.time()
sockets = []

f = open(input_file)
lines = f.readlines()
f.close()

num_of_neighbours = int(lines[0])
neighbours = []
dict_cost = {}
dict_port = {}
last_received = {}

graph = {node: dict_cost}

router = socket(AF_INET, SOCK_DGRAM)
router.bind(("", port))

for i in range(1, num_of_neighbours + 1):
    variables = lines[i].split()
    name = variables[0]
    neighbours.append(name)
    cost = int(variables[1])
    port = int(variables[2])
    dict_cost[name] = cost
    dict_port[name] = port


def dijkstra(graph_input, start_node, destination_node, visited_nodes, costs, previous_nodes):
    if start_node not in graph_input:
        raise TypeError('the starting node cannot be found in the graph')
    if destination_node not in graph_input:
        raise TypeError('the destination node cannot be found in the graph')

    if start_node == destination_node:
        path = []
        previous = destination_node
        while previous is not None:
            path.append(previous)
            previous = previous_nodes.get(previous, None)
        print "least-cost path to node " + destination_node + ": " + ''.join(path[::-1]) + " and the cost is " + str(
            costs[destination_node])
    else:
        if not visited_nodes:
            costs[start_node] = 0
        for neighbour in graph_input[start_node]:
            if neighbour not in visited_nodes:
                new_distance = costs[start_node] + graph_input[start_node][neighbour]
                if new_distance < costs.get(neighbour, float('inf')):
                    costs[neighbour] = new_distance
                    previous_nodes[neighbour] = start_node
        visited_nodes.append(start_node)
        unvisited_nodes = {}
        for k in graph_input:
            if k not in visited_nodes:
                unvisited_nodes[k] = costs.get(k, float('inf'))
        x = min(unvisited_nodes, key=unvisited_nodes.get)
        dijkstra(graph_input, x, destination_node, visited_nodes, costs, previous_nodes)


while True:

    if (time.time() - start_time) % 1.0 == 0.0 and (time.time() - start_time) % 30.0 != 0.0:
        for name in neighbours:
            s = socket(AF_INET, SOCK_DGRAM)
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            s.sendto(pickle.dumps(graph), ('255.255.255.255', dict_port[name]))
        received_lsp, address = router.recvfrom(1024)
        deserialized_lsp = pickle.loads(received_lsp)
        if last_received != deserialized_lsp:
            last_received = deserialized_lsp
            graph.update(deserialized_lsp)

    if (time.time() - start_time) % 30.0 == 0.0:
        for nebr in graph.keys():
            if nebr != node:
                visited = []
                distances = {}
                predecessors = {}
                dijkstra(graph, node, nebr, visited, distances, predecessors)
