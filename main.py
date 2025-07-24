import pygame
import sys
from level import Level
from snake import Snake
from fruit import Fruit
from sprites import SnakeSprites
from obstacle import Obstacle
from utils import draw_text

pygame.init()

TILE_SIZE = 32
FPS_BASE = 8
MAX_LIVES = 3

info = pygame.display.Info()
SCREEN_WIDTH = (info.current_w // TILE_SIZE) * TILE_SIZE
SCREEN_HEIGHT = (info.current_h // TILE_SIZE) * TILE_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game Full")
clock = pygame.time.Clock()

def show_menu():
    while True:
        screen.fill((0,0,0))
        draw_text(screen, "SNAKE GAME", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//3, size=48)
        draw_text(screen, "Press ENTER to Start", SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2)
        draw_text(screen, "Press ESC to Quit", SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over_screen(score):
    while True:
        screen.fill((0,0,0))
        draw_text(screen, "GAME OVER", SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT//3, size=48, color=(255,50,50))
        draw_text(screen, f"Score: {score}", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2)
        draw_text(screen, "Press R to Restart or ESC to Quit", SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def check_collision_with_obstacles(snake, obstacles):
    head = snake.head()
    for obs in obstacles:
        if obs.position == head:
            return True
    return False
    
def main():
    show_menu()
    COLS = SCREEN_WIDTH // TILE_SIZE
    ROWS = SCREEN_HEIGHT // TILE_SIZE
    level = Level(COLS, ROWS)
    snake = Snake(level)
    fruit = Fruit(level)
    sprites = SnakeSprites()
    score = 0
    lives = MAX_LIVES
    level_num = 1
    paused = False
    fps = FPS_BASE

    obstacles = []
    for _ in range(3):
        occupied = [{'x': seg['x'], 'y': seg['y']} for seg in snake.segments]
        obs = Obstacle(level, occupied)
        obstacles.append(obs)

    while True:
        dt = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    snake.change_direction(event.key)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not paused:
            alive = snake.move()

            if check_collision_with_obstacles(snake, obstacles):
                lives -= 1
                if lives <= 0:
                    if game_over_screen(score):
                        main()
                    return
                else:
                    snake.reset()
                    continue

            if not alive:
                lives -= 1
                if lives <= 0:
                    if game_over_screen(score):
                        main()
                    return
                else:
                    snake.reset()
                    continue

            if snake.head() == fruit.position:
                snake.grow()
                score += 10
                occupied = snake.segments + [fruit.position] + [obs.position for obs in obstacles]
                fruit.spawn(occupied)

                if score % 50 == 0:
                    level_num += 1
                    lives += 1
                    fps += 2
                    occupied = snake.segments + [fruit.position] + [obs.position for obs in obstacles]
                    obs = Obstacle(level, occupied)
                    obstacles.append(obs)

        screen.fill((0, 0, 0))
        level.draw(screen)
        fruit.draw(screen, sprites)
        snake.draw(screen, sprites)
        for obs in obstacles:
            obs.draw(screen)

        draw_hud(screen, score, lives, level_num)

        if paused:
            draw_text(screen, "PAUSED", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, size=50, color=(255,255,0))

        pygame.display.flip()

def draw_hud(surface, score, lives, level):
    bg_color = (0, 0, 0, 150)
    text_color = (255, 255, 255)
    shadow_color = (40, 40, 40)

    font = pygame.font.SysFont("Segoe UI Symbol", 28)

    hud_surface = pygame.Surface((220, 100), pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, bg_color, (0, 0, 220, 100), border_radius=8)
    
    def draw_shadowed_text(text, x, y):
        shadow = font.render(text, True, shadow_color)
        rendered = font.render(text, True, text_color)
        hud_surface.blit(shadow, (x + 2, y + 2))
        hud_surface.blit(rendered, (x, y))
    
    draw_shadowed_text(f" ★ Score: {score}", 10, 10)
    draw_shadowed_text(f"♥ Lives: {lives}", 10, 38)
    draw_shadowed_text(f"⚡ Level: {level}", 10, 66)

    surface.blit(hud_surface, (10, 10))

if __name__ == "__main__":
    main()
