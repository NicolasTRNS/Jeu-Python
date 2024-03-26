import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Définition de la classe Snake
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.grow = False

    def move(self):
        head = self.body[0]
        x, y = head
        if self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1
        elif self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'RIGHT':
            x += 1
        self.body.insert(0, (x, y))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

# Définition de la classe Apple
class Apple:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Fonction principale
def main():
    # Création de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    # Création du serpent et de la pomme
    snake = Snake()
    apple = Apple()

    # Boucle de jeu
    clock = pygame.time.Clock()
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'

        # Déplacement du serpent
        snake.move()

        # Vérification des collisions
        if snake.check_collision():
            running = False

        # Vérification si le serpent mange la pomme
        if snake.body[0] == apple.position:
            snake.grow_snake()
            apple = Apple()

        # Dessin sur l'écran
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        # Limiter le nombre d'images par seconde
        clock.tick(10)

    pygame.quit()

# Lancement du jeu
if __name__ == "__main__":
    main()
