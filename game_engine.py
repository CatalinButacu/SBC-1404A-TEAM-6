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
def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        matrix = [line.strip().split() for line in file]
    return matrix

def print_positions_and_words(matrix):
    for i, row in enumerate(matrix):
        for j, word in enumerate(row):
            print(f"Position: ({i}, {j}), Word: {word}")


def write_matrix_to_file(filename, matrix):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(row) + '\n')

def update_matrix_at_position(filename, row, col, word):
    # Read the matrix from the file
    matrix = read_matrix_from_file(filename)
    
    # Update the matrix at the specified position
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[row]):
        matrix[row][col] = word
    else:
        print("Invalid row or column index")
        return
    
    # Write the updated matrix back to the file
    write_matrix_to_file(filename, matrix)




# LOCAL MAIN
if __name__ == "__main__":
    init_sistem_env()
    set_state_of_sistem(SISTEM_ASTEAPTA)
    all_facts = get_all_facts_list()
    print_all_facts()
