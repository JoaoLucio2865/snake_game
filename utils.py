import pygame

def draw_text(screen, text, x, y, size=30, color=(255,255,255)):
    font = pygame.font.SysFont('Arial', size)
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
