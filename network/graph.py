import logging
import os

import networkx as nx

from typing import Tuple, List

import config
from network.dataset import prepare_dataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

ActorName = str
ActorConnectionNumber = int


class ShortestPath:
    def __init__(self):
        self.graph = self._init_graph()

    async def shortest_path(self, target: ActorName,
                            source: ActorName) -> Tuple[ActorConnectionNumber, List[ActorName]]:
        # this will fail if source or target are not in the graph
        # or if there is no path between the source and the target
        sp = nx.shortest_path(self.graph,
                              source=source,
                              target=target,
                              method='dijkstra')
        return len(sp) - 1, sp

    @staticmethod
    def _init_graph():
        graph_path = os.path.join(config.DATASET_PATH, config.GRAPH_FILENAME)
        if not os.path.exists(graph_path):
            dataset = prepare_dataset(config.DATASET_PATH, config.DATASET_FILENAME)
            graph = nx.Graph()
            graph.add_weighted_edges_from(zip(dataset.name_x, dataset.name_y, dataset.cnt))
            nx.write_gpickle(graph, graph_path)
        else:
            graph = nx.read_gpickle(graph_path)
        return graph
