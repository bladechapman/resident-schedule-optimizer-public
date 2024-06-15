from ortools.graph.python.min_cost_flow import SimpleMinCostFlow
from csv_utils import parse_csv
from all_schedules import all_possible_schedules
from group_schedules import group_schedules
from common import Grouping
from flow_solver import Solver
from base64 import standard_b64encode
import os
import pickle

def build_subgraph_for_grouping(solver: Solver,
                                grouping: Grouping,
                                group_identifier: int,
                                residents: list[str],
                                preferences: dict[str, list[dict[str, int]]]
                                ):
    resident_nodes: dict[str, int] = {}
    schedule_nodes: dict[int, int] = {}

    # connect residents to source
    for resident in residents:
        resident_node = solver.assign_node()
        resident_nodes[resident] = resident_node
        solver.add_edge(solver.SOURCE_NODE_INDEX, resident_node, 1, 0)

    # connect schedules to sink
    for i in range(len(grouping)):
        schedule_node = solver.assign_node()
        schedule_nodes[i] = schedule_node
        solver.add_edge(schedule_node, solver.SINK_NODE_INDEX, 1, 0)

    # add cross edges between residents and schedules
    for resident, resident_node in resident_nodes.items():
        for schedule_idx, schedule_node in schedule_nodes.items():
            cost = compute_cost_for_schedule(grouping[schedule_idx], preferences[resident])
            solver.add_edge(resident_node, schedule_node, 1, cost)
            solver.annotate(resident_node, schedule_node, {
                "resident": resident,
                "group": group_identifier,
                "schedule": grouping[schedule_idx],
                "cost": cost
            })

def compute_cost_for_schedule(schedule: list[str], resident_preferences: list[dict[str, int]]):
    HIGH_COST=100
    cost = 0
    for rotation_idx, subject in enumerate(schedule):
        preferences_for_rotation = resident_preferences[rotation_idx]
        if subject in preferences_for_rotation:
            cost += preferences_for_rotation[subject]
        else:
            cost += HIGH_COST
    return cost

def extract_solution_txt(solver: Solver, flow_instance: SimpleMinCostFlow, flow_solution):
    flow_sum = 0
    selected_annotations = []
    if flow_solution == flow_instance.OPTIMAL:
        for i in range(flow_instance.num_arcs()):
            head = flow_instance.head(i)
            tail = flow_instance.tail(i)
            flow = flow_instance.flow(i)

            if (tail, head) in solver.edge_annotations and flow == 1:
                annotation = solver.edge_annotations[(tail, head)]
                selected_annotations.append(annotation)
            
            if tail == solver.SOURCE_NODE_INDEX:
                flow_sum += flow

    grouped_annotations = {}
    for annotation in selected_annotations:
        key = annotation["group"]
        if key not in grouped_annotations:
            grouped_annotations[key] = { "cost": annotation["cost"], "annotations": [annotation] }
        else:
            grouped_annotations[key]["cost"] += annotation["cost"]
            grouped_annotations[key]["annotations"].append(annotation)

    sorted_grouped_annotations = sorted(grouped_annotations.values(), key=lambda x: x["cost"])
 
    solution_str = f"Max flow: {flow_sum}\n"
    for i, group in enumerate(sorted_grouped_annotations):
        solution_str += (f"Option {i + 1} | Cost: {group['cost']}\n")
        for annotation in group["annotations"]:
            solution_str += ("\t{:15s} {} {}\n".format(annotation["resident"], annotation["cost"], annotation["schedule"]))

    return solution_str

if __name__ == "__main__":
    with open("preferences.csv", newline="") as csvfile:
        rotations, sub_specialties, residents, preferences = parse_csv(csvfile)

        # since group_schedules takes a long time, we pickle it after the first compute 
        cache_key = standard_b64encode(",".join(sub_specialties).encode("ascii")).decode("utf8")
        cache_file_location = f".cache.{cache_key}.pkl"
        if os.path.isfile(cache_file_location):
            with open(cache_file_location, 'rb') as f:
                all_groups = pickle.load(f)
        else:
            all_schedules = all_possible_schedules(sub_specialties)
            all_groups = group_schedules(all_schedules, len(sub_specialties))
            with open(cache_file_location, 'wb') as f:
                pickle.dump(all_groups, f)

        solver = Solver()
        for i in range(len(all_groups)):
            build_subgraph_for_grouping(solver, all_groups[i], i, residents, preferences)
        flow, flow_solution = solver.solve()

        print(extract_solution_txt(solver, flow, flow_solution))
