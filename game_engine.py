# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:25:34 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

# LIBS
import clips

# GLOBALS
env = clips.Environment()
all_facts = []
SISTEM_ASTEAPTA = 0
SISTEM_DECIDE = 1


# INITS
def init_sistem_env(file_name:str="main.clp"):
    env.clear()
    env.load(file_name)
    env.reset()
    #env.run()


# EXECUTERS
def execute_freeze_state_sistem():
    env.eval("(assert (freeze_state_sistem))")
    env.run(1)

def execute_update_map():
    env.eval("(assert (update_map_now))")
    env.run(1)

def execute_update_file_map_using_matrix(matrix:dict):
    filename = "map_parcurs.txt"
    write_matrix_to_file(filename, matrix)
    execute_update_map()
    set_state_of_sistem(1)
    execute_update_map()
    env.run()

def execute_update_matrix_using_file_map():
    filename = "map_parcurs.txt"
    set_state_of_sistem(0)
    return read_and_transform_matrix(filename)

# GETTERS
def get_all_facts_list():
    return env.eval("(get-fact-list *)")

def get_clips_state():
    facts = get_all_facts_list()
    for fact in facts:
        if "(Sistem asteapta)" in str(fact):
            return True
    return False

def get_agenda_list():
    return env.activations()


# SETTERS
def set_state_of_sistem(decisional_state:int = 0): # 0 - Sistem asteapta, 1 - Sistem decide
    if decisional_state not in (0,1):
        print("[Warning] Decisional_state incompatible")
        return
    new_state = "asteapta" if decisional_state == 0 else "decide"
    fact_to_add = f"(assert (Sistem {new_state}))"
    execute_freeze_state_sistem()
    env.eval(fact_to_add)


# DISPLAY
def print_all_facts():
    print('######### Afisarea bazei de fapte #########')
    for fact in env.facts():
        print(fact)

def print_all_agenda():
    print("\n### AGENDA's ACTIVATIONS")
    for activation in env.activations():
        print(activation)

# READ / WRITE MAP
def read_matrices_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        matrix_state = [list(map(int, line.split())) for line in content[0].strip().split('\n')]
        matrix_ids = [list(map(int, line.split())) for line in content[1].strip().split('\n')]
        file.close()
    return {"state": matrix_state, "ids": matrix_ids}


def write_matrices_to_file(filename, matrix):
    matrix_state = matrix["state"]
    matrix_ids = matrix["ids"]

    with open(filename, 'r+') as file:
        for row in matrix_state:
            file.write(' '.join(map(str, row)) + '\n')
        file.write('\n')
        for row in matrix_ids:
            file.write(' '.join(map(str, row)) + '\n')
        file.close()

def print_matrices(matrix):
    matrix_state = matrix["state"]
    matrix_ids = matrix["ids"]

    print("State matrix:")
    for row in matrix_state:
        print(' '.join(map(str, row)))

    print("\nIDs matrix:")
    for row in matrix_ids:
        print(' '.join(map(str, row)))


def read_and_transform_matrix(filename):
    matrix_state = []
    matrix_ids = []
    with open(filename, 'r') as file:
        for line in file:
            row_state = []
            row_ids = []
            items = line.strip().split()
            for item in items:
                if item == "liber":
                    row_state.append(0)
                    row_ids.append(0)  # Add 0 to IDs matrix when there's no corresponding ID
                elif item == "atacata":
                    row_state.append(1)
                    row_ids.append(0)  # Add 0 to IDs matrix when there's no corresponding ID
                elif item.startswith("N"):
                    if "_a" in item:
                        num = int(item[1:-2])
                        row_state.append(3)  # Set the state matrix value to 3 when encountering "_a"
                    else:
                        num = int(item[1:])
                        row_state.append(2)
                    row_ids.append(num)
                else:
                    row_state.append(3)
                    row_ids.append(int(item))
            matrix_state.append(row_state)
            matrix_ids.append(row_ids)
        file.close()
    return {"state": matrix_state, "ids": matrix_ids}

def execute_update_file_map_using_matrix(matrix:dict):
    filename = "map_parcurs.txt"
    write_matrix_to_file(filename, matrix)
    set_state_of_sistem(1)
    execute_update_map()
    env.run()

def write_matrix_to_file(filename, matrix):
    with open(filename, 'r+') as file:
        state_matrix = matrix["state"]
        ids_matrix = matrix["ids"]
        for state_row, ids_row in zip(state_matrix, ids_matrix):
            row_items = []
            for state, id_ in zip(state_row, ids_row):
                if state == 0:
                    row_items.append("liber")
                elif state == 1:
                    row_items.append("atacata")
                elif state == 2:
                    row_items.append(f"N{id_}")
                elif state == 3:
                    row_items.append(f"N{id_}_a")
            file.write(' '.join(row_items) + '\n')
        file.close()


# LOCAL MAIN
if __name__ == "__main__":
    init_sistem_env()
    set_state_of_sistem(SISTEM_DECIDE)
    all_facts = get_all_facts_list()
    print_all_facts()
    print_all_agenda()
