#!/usr/bin/env python3
import networkx as nx
from networkx.classes.function import neighbors
import yaml
import sys
import numpy as np
from numpy.random import randint as nprandint
from random import randint

if len(sys.argv) < 4:
    sys.stderr.write("not enough arguments\n")
    sys.stderr.write(
        f"Usage: {__file__} <node_count|int> <max_cost|int> <graph_type|string>\n")
    sys.stderr.write(
        "Acceptable graph types are: binomial, power_law or and small_world\n")
    sys.exit(1)

node_count = int(sys.argv[1])
max_cost = int(sys.argv[2])
graph_type = sys.argv[3]

n = int(np.ceil(node_count * 0.5))
neighbors = 1 if n == 0 else n
# neighbors = nprandint(1, node_count)

print(neighbors)

if graph_type == "binomial":
    edge_count = node_count // 4 if node_count > 4 else node_count // 2
    G = nx.binomial_graph(node_count, neighbors)
else:
    if graph_type == "power_law":
        G = nx.extended_barabasi_albert_graph(node_count, neighbors, 0, 0)
        # G = nx.barabasi_albert_graph(node_count, neighbors)
    else:
        G = nx.watts_strogatz_graph(node_count, neighbors, 0)
        # G = nx.connected_watts_strogatz_graph(node_count, neighbors, 0.2)

# values to be collected from users
# node_count = 3
# edge_count = 2
# ultimately, we would want every service to start a single pod
replicas = [3] * node_count

# replicas = [2, 4, 2]

# costs = [2, 2, 4]
# create a list of random costs
costs = list(nprandint(max_cost + 1, size=node_count))
# costs = [3] * node_count
# costs = [randint(1, max_cost + 1)] * node_count

# bads = [0, 0, 1]
# randomly allow some services to have bad pods
bads = nprandint(2, size=node_count)
# bads = [0] * node_count

fname = "test.yaml"
# =================================

map = {}
for i in range(node_count):
    map[i] = 'testapp-svc-%s' % i

# G = nx.binomial_graph(node_count, edge_count)

H = nx.relabel_nodes(G, map)

configs = []

for item in map.items():
    config_tmpl = {}
    idx = item[0]
    config_tmpl['index'] = idx
    config_tmpl['replicas'] = replicas[idx]
    config_tmpl['cost'] = int(costs[idx])
    config_tmpl['bads'] = int(bads[idx])
    svc = []
    # too expensive???
    for edge in H.edges:
        if edge[0] == 'testapp-svc-%s' % idx:
            svc.append('testapp-svc-%s:5000/svc/%s' %
                       (edge[1][-1], edge[1][-1]))
    config_tmpl['svc'] = svc
    configs.append(config_tmpl)

with open(fname, 'w') as file:
    yaml.dump(configs, file)
