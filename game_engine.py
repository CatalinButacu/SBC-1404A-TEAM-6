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
    env.run()


# EXECUTERS
def execute_freeze_state_sistem():
    env.eval("(assert (freeze_state_sistem))")
    env.run(1)

def execute_update_map():
    env.eval("(assert (update_map_now))")
    env.run(1)

def execute_update_file_map_using_matrix(matrix:dict):
    filename = "map_parcurs.txt"
    write_matrices_to_file(filename, matrix)
    print("semnal ajuns in GameEngine")
    print(matrix['state'])
    print(matrix['ids'])

def execute_update_matrix_using_file_map(filename=""):
    pass

# GETTERS
def get_all_facts_list():
    return env.eval("(get-fact-list *)")


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
    for fact in all_facts:
        print(fact)

# READ / WRITE MAP
def read_matrices_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        matrix_state = [list(map(int, line.split())) for line in content[0].strip().split('\n')]
        matrix_ids = [list(map(int, line.split())) for line in content[1].strip().split('\n')]
    return {"state": matrix_state, "ids": matrix_ids}


def write_matrices_to_file(filename, matrix):
    matrix_state = matrix["state"]
    matrix_ids = matrix["ids"]

    with open(filename, 'w') as file:
        for row in matrix_state:
            file.write(' '.join(map(str, row)) + '\n')
        file.write('\n')
        for row in matrix_ids:
            file.write(' '.join(map(str, row)) + '\n')


def update_app_matrix_with_file_matrix(filename, matrix_app):
    # Read the matrices from the file
    matrix = read_matrices_from_file(filename)
    matrix_app = matrix
    return matrix_app

def print_matrices(matrix):
    matrix_state = matrix["state"]
    matrix_ids = matrix["ids"]

    print("State matrix:")
    for row in matrix_state:
        print(' '.join(map(str, row)))

    print("\nIDs matrix:")
    for row in matrix_ids:
        print(' '.join(map(str, row)))




# LOCAL MAIN
if __name__ == "__main__":
    init_sistem_env()
    set_state_of_sistem(SISTEM_ASTEAPTA)
    all_facts = get_all_facts_list()
    print_all_facts()
