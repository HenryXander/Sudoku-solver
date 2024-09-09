from .backtrack_search import backtracking_search_CSP as bts
from CSP import CSP
from itertools import product
import pygame
import sys


pygame.init()

WIDTH, HEIGHT = 540, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

font = pygame.font.SysFont("comicsans", 40)


def draw_board(board):
    screen.fill(WHITE)
    for i in range(10):
        if i % 3 == 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(screen, BLACK, (60 * i, 0), (60 * i, 540), thick)
        pygame.draw.line(screen, BLACK, (0, 60 * i), (540, 60 * i), thick)

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                text = font.render(str(num), True, BLACK)
                screen.blit(text, (j * 60 + 20, i * 60 + 10))

    pygame.display.flip()

def solve_sudoku(csp, board):
    result = bts(csp, "pc2")
    if result == "Failure":
        return board
    else:
        for var, value in result.items():
            i = int(var[0])
            j = int(var[1])

            board[i][j] = value
        return board

def get_constraints():
    constraints = {}
    for i, j in product(range(9), repeat=2):
        var1 = f"{i}{j}"
        row_neighbors = [f"{i}{col}" for col in range(9) if col != j]
        col_neighbors = [f"{row}{j}" for row in range(9) if row != i]
        box_neighbors = [f"{row}{col}" for row in range(i - i % 3, i - i % 3 + 3) for col in
                         range(j - j % 3, j - j % 3 + 3) if (row, col) != (i, j)]

        all_neighbors = row_neighbors + col_neighbors + box_neighbors
        constraints[var1] = all_neighbors

    binary_constraints = {}

    def is_different(values):
        value_1 = values[0]
        value_2 = values[1]
        return value_1 != value_2

    for main_box, constraint in constraints.items():
        for box in constraint:
            binary_constraint_id = (main_box, box)
            new_binary_constraint = {
                binary_constraint_id: is_different
            }
            binary_constraints = binary_constraints | new_binary_constraint
    return binary_constraints

def initialize_CSP(initial_board):
    variables = [f"{i}{j}" for i, j in product(range(9), repeat=2)]
    domains = {var: list(range(1, 10)) if initial_board[i][j] == 0 else [initial_board[i][j]] for var, (i, j) in zip(variables, product(range(9), repeat=2))}
    constraints = get_constraints()
    csp = CSP(variables, domains, constraints)
    return csp

def main():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    draw_board(board)
    running = True
    csp = initialize_CSP(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("thinking...")
                        solve_sudoku(csp, board)
                        draw_board(board)
        draw_board(board)

if __name__ == "__main__":
    main()
