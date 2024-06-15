import csv

def parse_csv(csv_iterable):
    rows = [row for row in csv.reader(csv_iterable)]
    header_row = rows[0]
    data_rows = rows[1:]

    rotations = header_row[2:]
    sub_specialties = gather_sub_specialties(data_rows)
    residents = gather_residents(data_rows)

    determine_valid_input(rotations, sub_specialties, residents)

    # build preferences defined from CSV
    resident_preferences: dict[str, list[dict[str, int]]] = {}
    for row in data_rows:
        resident = row[0]
        cost = int(row[1])
        index_to_sub_specialty = dict(filter(lambda x: x[1] != '', enumerate(row[2:])))
        
        if resident not in resident_preferences:
            resident_preferences[resident] = [{} for _ in range(len(sub_specialties))]

        for rotation_index, sub_specialty in index_to_sub_specialty.items():
            resident_preferences[resident][rotation_index][sub_specialty] = cost

    return (rotations, sub_specialties, residents, resident_preferences)

def gather_sub_specialties(data_rows: list[list[str]]):
    sub_specialty_set: set[str] = set()
    for row in data_rows:
        for non_empty_cell in filter(lambda x: x != '', row[2:]):
            sub_specialty_set.add(non_empty_cell)
    return list(sub_specialty_set)

def gather_residents(data_rows: list[list[str]]):
    resident_set: set[str] = set()
    for row in data_rows:
        for non_empty_cell in filter(lambda x: x != '', row[:1]):
            resident_set.add(non_empty_cell)
    return list(resident_set)

def determine_valid_input(rotations: list[str], sub_specialties: list[str], residents: list[str]):
    if len(rotations) != len(sub_specialties):
        raise ValueError(f"Different number of Blocks and Subjects: {rotations} {sub_specialties}")

    if len(sub_specialties) != len(residents):
        raise ValueError(f"Different number of Subjects and Residents: {sub_specialties} {residents}")

