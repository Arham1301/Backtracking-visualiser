import pygame, sys
from pygame.locals import *
import numpy as np

def is_valid_and_empty(x, y, board, size):
    return 0 <= x < size and 0 <= y < size and board[x][y] == 0

def calculate_accessibility(x, y, moves, board, size):
    count = 0
    for move in moves:
        if is_valid_and_empty(x + move[0], y + move[1], board, size):
            count += 1
    return count

def determine_next_move(current_pos, moves, board, size):
    x, y = current_pos
    min_accessibility = 8
    for move in moves:
        new_x = x + move[0]
        new_y = y + move[1]
        new_access = calculate_accessibility(new_x, new_y, moves, board, size)
        if is_valid_and_empty(new_x, new_y, board, size) and new_access < min_accessibility:
            current_pos[0], current_pos[1] = new_x, new_y
            min_accessibility = new_access

def display_tour(size, positions):
    knight_img = pygame.image.load("knight.png")

    pygame.init()
    screen = pygame.display.set_mode((32 * size, 32 * size))
    pygame.display.set_caption("Knight's Tour")
    bg_img = pygame.image.load("chess.png")
    index = 0

    font = pygame.font.SysFont("Ubuntu", 16)
    texts = []
    rects = []

    while True:
        screen.blit(bg_img, (0, 0))
        if index < size * size:
            screen.blit(knight_img, (positions[index][0] * 32, positions[index][1] * 32))
            texts.append(font.render(str(index + 1), True, (255, 255, 255)))
            rects.append(texts[index].get_rect())
            rects[index].center = (positions[index][0] * 32 + 16, positions[index][1] * 32 + 16)
            index += 1
        else:
            screen.blit(knight_img, (positions[index - 1][0] * 32, positions[index - 1][1] * 32))

        for _ in range(10000000):
            pass

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        for i in range(index):
            screen.blit(texts[i], rects[i])

        pygame.display.update()

def is_solution(board, size):
    return all(board[i][j] != 0 for i in range(size) for j in range(size))

size = int(input("Enter N, size of the board (NxN): "))
start_x = int(input("Enter initial x position: ")) % size
start_y = int(input("Enter initial y position: ")) % size
current_x, current_y = start_x, start_y
move_num = 2
current_move = [start_x, start_y]
knight_moves = [[2, 1], [2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
board = np.zeros((size, size))
board[start_x][start_y] = 1
positions = []

for _ in range(size * size):
    current_move[0], current_move[1] = current_x, current_y
    determine_next_move(current_move, knight_moves, board, size)
    current_x, current_y = current_move
    board[current_x][current_y] = move_num
    move_num += 1

board[current_x][current_y] -= 1

solution_found = is_solution(board, size)
if solution_found:
    k = 1
    while k <= size * size:
        for i in range(size):
            for j in range(size):
                if board[i][j] == k:
                    positions.append([i, j])
                    k += 1
    print(board)
else:
    alt_moves = [[2, 1], [-2, 1], [2, -1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
    board = np.zeros((size, size))
    current_x, current_y = start_x, start_y
    board[start_x][start_y] = 1
    positions = []
    move_num = 2
    current_move = [start_x, start_y]

    for _ in range(size * size):
        current_move[0], current_move[1] = current_x, current_y
        determine_next_move(current_move, alt_moves, board, size)
        current_x, current_y = current_move
        board[current_x][current_y] = move_num
        move_num += 1

    board[current_x][current_y] -= 1

    solution_found = is_solution(board, size)
    if solution_found:
        k = 1
        while k <= size * size:
            for i in range(size):
                for j in range(size):
                    if board[i][j] == k:
                        positions.append([i, j])
                        k += 1
        print(board)

if not positions:
    print("Didn't find a solution.")
print("Knight's positions: ", positions)

if size <= 32 and solution_found:
    display_tour(size, positions)
