import pygame
import random

# Définition des constantes
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Les différents types de pièces
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Classe de la pièce
class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice([RED, CYAN, GREEN, BLUE, YELLOW, ORANGE, PURPLE])
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Classe principale du jeu
class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        return Piece(random.choice(SHAPES))

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, cell)

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_piece.x + x, self.current_piece.y + y, self.current_piece.color)

    def move_piece(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self):
        temp_piece = Piece(self.current_piece.shape)
        temp_piece.x = self.current_piece.x
        temp_piece.y = self.current_piece.y
        temp_piece.rotate()
        if not self.check_collision(temp_piece, 0, 0):
            self.current_piece.shape = temp_piece.shape

    def check_collision(self, piece, dx, dy):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = piece.x + x + dx
                    board_y = piece.y + y + dy
                    if board_x < 0 or board_x >= BOARD_WIDTH or \
                            board_y >= BOARD_HEIGHT or \
                            self.board[board_y][board_x]:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.current_piece = self.new_piece()
        if self.check_collision(self.current_piece, 0, 0):
            self.game_over = True

    def check_lines(self):
        lines_to_clear = [index for index, row in enumerate(self.board) if all(row)]
        for index in lines_to_clear:
            del self.board[index]
            self.board.insert(0, [0] * BOARD_WIDTH)

    def run(self):
        while not self.game_over:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        if not self.move_piece(0, 1):
                            self.lock_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.move_piece(0, 1)

            self.draw_board()
            self.draw_piece()

            self.check_lines()

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()
