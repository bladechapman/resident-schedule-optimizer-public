from csv_utils import parse_csv
from all_schedules import all_possible_schedules
from group_schedules import group_schedules
from common import Grouping
from flow_solver import Solver


def build_subgraph_for_grouping(self, grouping: Grouping, residents: list[str], preferences: dict[str, list[dict[str, int]]]):



if __name__ == "__main__":
    with open("preferences.csv", newline="") as csvfile:
        rotations, sub_specialties, residents, preferences = parse_csv(csvfile)

        all_schedules = all_possible_schedules(sub_specialties)
        all_groups = group_schedules(all_schedules, len(sub_specialties))
        # since group_schedules takes a long time, you could pickle it after the first compute 

        solver = Solver()
