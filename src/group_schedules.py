from common import Grouping, Schedule
from multiprocessing import Pool
import os
from functools import reduce

parallelism_level = 4
try:
    e = os.getenv("OPTIMIZER_PARALLELISM")
    if e != None:
        parallelism_level = int(e)
except:
    pass

def group_schedules(all_schedules: list[Schedule], group_size: int) -> list[Grouping]:
    all_valid_groups = []

    with Pool(parallelism_level) as p:
        runs = p.starmap(
                compute_column,
                [(all_schedules[i:], group_size) for i in range(len(all_schedules))]
            )
        all_valid_groups = reduce(lambda a, b: a + b, runs)

    return all_valid_groups

def compute_column(column_schedules: list[Schedule], required_group_size: int) -> list[Grouping]:
    accumulated_groupings: list[Grouping] = [[column_schedules[0]]]
    valid_groupings: list[Grouping] = []
    
    for i in range(len(column_schedules)):
        candidate_schedule = column_schedules[i]

        for group in accumulated_groupings:
            candidate_grouping = group + [candidate_schedule]

            if schedule_violates_group(candidate_schedule, group):
                continue
            elif len(candidate_grouping) == required_group_size:
                valid_groupings.append(candidate_grouping)
            else:
                accumulated_groupings.append(candidate_grouping)

    return valid_groupings

def schedule_violates_group(schedule: Schedule, grouping: Grouping):
    for g in grouping:
        if schedules_conflict(g, schedule):
            return True
    return False

def schedules_conflict(schedule_1: Schedule, schedule_2: Schedule) -> bool:
    for i in range(0, len(schedule_1)):
        if schedule_1[i] == schedule_2[i]:
            return True
    return False


if __name__ == "__main__":
    from all_schedules import all_possible_schedules

    subspecialties = ["A", "B", "C", "D", "E"]
    # subspecialties = ["A", "B", "C", "D", "E", "F"]   # be prepared for this case to take a minute...
    all_possible_schedules = all_possible_schedules(subspecialties)
    groups = group_schedules(all_possible_schedules, len(subspecialties))

    assert len(groups) == 1344
