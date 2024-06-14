from common import SubSpecialty, Schedule

def all_possible_schedules(available_subspecialties: list[SubSpecialty]) -> list[Schedule]:
    if len(available_subspecialties) == 0:
        return []
    elif len(available_subspecialties) == 1:
        return [[available_subspecialties[0]]]
    else:
        schedules = []
        for i in range(0, len(available_subspecialties)):
            head = available_subspecialties[i]
            tail = available_subspecialties[0:i] + available_subspecialties[i + 1:]

            for tail_schedule in all_possible_schedules(tail):
                schedules.append([head] + tail_schedule)

        return schedules

if __name__ == "__main__":
    subspecialties = ["AVA", "DVA", "Aesthetics", "Research", "Capstone", "Cornea"]
    aps = all_possible_schedules(subspecialties)

    assert len(aps) == 720  # 6 factorial possible schedules
