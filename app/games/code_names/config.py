import math

N_BLUE = 9
N_RED = 8
N_WHITE = 7
N_BLACK = 1

N_TOTAL = sum([N_BLUE, N_RED, N_WHITE, N_BLACK])
SIDE_LEN = math.sqrt(N_TOTAL)
assert SIDE_LEN.is_integer()
SIDE_LEN = int(SIDE_LEN)

CODE_NAMES = [str(i) for i in range(50)]
