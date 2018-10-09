import math

BLUE_CELLS = 9
RED_CELLS = 8
WHITE_CELLS = 7
BLACK_CELLS = 1
TOTAL_CELLS = sum([BLUE_CELLS, RED_CELLS, WHITE_CELLS, BLACK_CELLS])

CELLS_IN_ROW = math.sqrt(TOTAL_CELLS)
assert CELLS_IN_ROW.is_integer()
CELLS_IN_ROW = int(CELLS_IN_ROW)

def count_cells(color):
    return globals()[f'{color.name}_CELLS']

PX_CELL_SIDE = 100
