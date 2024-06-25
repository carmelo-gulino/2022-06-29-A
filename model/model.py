import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_sol = None
        self.graph = None

    def build_graph(self, n_canzoni):
        self.graph = nx.DiGraph()
        nodes = DAO.get_nodes(n_canzoni)
        self.graph.add_nodes_from(nodes)
        for a1 in self.graph.nodes:
            for a2 in self.graph.nodes:
                if a1 != a2:
                    delta = a1.n_canzoni - a2.n_canzoni
                    if delta > 0:
                        self.graph.add_edge(a2, a1, weight=abs(delta))
                    elif delta < 0:
                        self.graph.add_edge(a1, a2, weight=abs(delta))
        return self.graph

    def get_sorted_successors(self, chosen_album):
        result = []
        for s in self.graph.successors(chosen_album):
            bilancio = self.get_bilancio(s)
            result.append((s, bilancio))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def get_bilancio(self, album):
        s_entranti = 0
        for p in self.graph.predecessors(album):
            s_entranti += self.graph[p][album]['weight']
        s_uscenti = 0
        for s in self.graph.successors(album):
            s_uscenti += self.graph[album][s]['weight']
        return s_entranti - s_uscenti

    def get_percorso(self, a1, a2, x):
        self.best_sol = []
        parziale = [a1]
        bilancio_a1 = self.get_bilancio(a1)
        self.ricorsione(parziale, a2, x, bilancio_a1)
        return self.best_sol

    def ricorsione(self, parziale, a2, x, bilancio_a1):
        ultimo = parziale[-1]
        if len(parziale) > len(self.best_sol) and ultimo == a2:
            self.best_sol = copy.deepcopy(parziale)
            print(parziale)
        nodi_possibili = [s for s in self.graph.successors(ultimo) if self.get_bilancio(s) > bilancio_a1]
        for successor in nodi_possibili:
            if successor not in parziale and self.graph[ultimo][successor]['weight'] >= x:
                parziale.append(successor)
                self.ricorsione(parziale, a2, x, bilancio_a1)
                parziale.pop()
