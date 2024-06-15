from ortools.graph.python import min_cost_flow
from typing import Any
import sys

class Solver:

    def __init__(self):
        self.START_NODES: list[int] = []
        self.END_NODES: list[int] = []
        self.CAPACITIES: list[int] = []
        self.UNIT_COSTS: list[int] = []
        self.INDEX_ITERATOR = 0

        self.edge_annotations: dict[tuple[int, int], Any] = {}

        self.SOURCE_NODE_INDEX = self.assign_node()
        self.SINK_NODE_INDEX = self.assign_node()

    def assign_node(self) -> int:
        ret = self.INDEX_ITERATOR
        self.INDEX_ITERATOR += 1
        return ret

    def add_edge(self, start_node: int, end_node: int, capacity: int, unit_cost: int):
        self.START_NODES += [start_node]
        self.END_NODES += [end_node]
        self.CAPACITIES += [capacity]
        self.UNIT_COSTS += [unit_cost]

    def solve(self):
        print("building arcs", file=sys.stderr)
        min_cost_flow_instance = min_cost_flow.SimpleMinCostFlow()
        for i in range(len(self.START_NODES)):
            min_cost_flow_instance.add_arc_with_capacity_and_unit_cost(
                self.START_NODES[i],
                self.END_NODES[i],
                self.CAPACITIES[i],
                self.UNIT_COSTS[i]
            )

        min_cost_flow_instance.set_node_supply(self.SOURCE_NODE_INDEX, 9000000)
        min_cost_flow_instance.set_node_supply(self.SINK_NODE_INDEX, -9000000)
        print("done",file=sys.stderr )

        print("solving...",file=sys.stderr )
        flow_solution = min_cost_flow_instance.solve_max_flow_with_min_cost()
        print("done",file=sys.stderr)

        return min_cost_flow_instance, flow_solution

    def annotate(self, startNodeIdx, endNodeIdx, annotation):
        self.edge_annotations[(startNodeIdx, endNodeIdx)] = annotation
