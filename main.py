import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Bird properties
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_X = 50
BIRD_Y = SCREEN_HEIGHT // 2
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Pipe properties
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_FREQUENCY = 1500  # Milliseconds

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Load assets
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(GREEN)

pipe_img = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
pipe_img.fill(GREEN)

# Font
font = pygame.font.SysFont("Arial", 30)

# Game variables
bird_velocity = 0
bird_rect = pygame.Rect(BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT)
pipes = []
last_pipe = pygame.time.get_ticks()
score = 0
game_over = False

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    game_over_text = font.render("Game Over! Click to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

def reset_game():
    global bird_rect, bird_velocity, pipes, score, game_over
    bird_rect.y = BIRD_Y
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = FLAP_STRENGTH
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

    if not game_over:
        # Bird physics
        bird_velocity += GRAVITY
        bird_rect.y += bird_velocity

        # Generate pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipes.append(pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height))
            pipes.append(pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP))
            last_pipe = time_now

        # Move pipes
        for pipe in pipes:
            pipe.x -= PIPE_SPEED

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

        # Collision detection
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_over = True

        # Check if bird hits the ground or ceiling
        if bird_rect.y > SCREEN_HEIGHT or bird_rect.y < 0:
            game_over = True

        # Increase score
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH == BIRD_X:
                score += 0.5  # Each pair of pipes counts as 1 point

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Draw bird
    pygame.draw.rect(screen, GREEN, bird_rect)

    # Draw score
    draw_score()

    # Game over screen
    if game_over:
        draw_game_over()

    # Update display
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()