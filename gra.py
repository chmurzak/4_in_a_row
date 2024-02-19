import pygame
import sys
import numpy as np
import math

pygame.init()

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (0, 0, 0), (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def make_move(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def is_terminal(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(3, COLUMN_COUNT):
            window = [board[r+i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score



def minimax(board, depth, alpha, beta, maximizingPlayer):
    game_over = is_terminal(board)
    if depth == 0 or game_over:
        if game_over:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            make_move(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = np.random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            make_move(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



board = np.zeros((ROW_COUNT, COLUMN_COUNT))
game_over = False

pygame.display.set_caption("4 w rzędzie")

def player_choice_screen():
    font = pygame.font.SysFont("monospace", 30)
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), (0, 0, width // 2, height))
    text_gracz = font.render("Gracz", 1, (255, 255, 255))
    screen.blit(text_gracz, (width // 4 - text_gracz.get_width() // 2, height // 2 - 50))

    pygame.draw.rect(screen, (255, 255, 0), (width // 2, 0, width // 2, height))
    text_komputer = font.render("Komputer", 1, (0, 0, 0))
    screen.blit(text_komputer, (3 * width // 4 - text_komputer.get_width() // 2, height // 2 - 50))

    pygame.display.update()

    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx, _ = pygame.mouse.get_pos()
                if posx < width // 2:
                    return 0
                else:
                    return 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


turn = player_choice_screen()

draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    make_move(board, row, col, 1)

                    if winning_move(board, 1):
                        label = pygame.font.SysFont("monospace", 60).render("Gracz wygrywa!", 1, (255, 0, 0))
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    draw_board(board)

    if turn == 1 and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if col is None:
            col = np.random.randint(0, COLUMN_COUNT)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            make_move(board, row, col, 2)

            if winning_move(board, 2):
                label = pygame.font.SysFont("monospace", 60).render("Komputer wygrywa!", 1, (255, 255, 0))
                screen.blit(label, (40,10))
                game_over = True

            draw_board(board)
            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
