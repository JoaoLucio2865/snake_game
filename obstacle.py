import pygame
import random

class Obstacle:
    def __init__(self, level, occupied):
        self.level = level
        self.position = None
        self.block_size = 32
        self.image = pygame.image.load('obstacle.png').convert_alpha()
        self.spawn(occupied)

    def spawn(self, occupied):
        free_positions = []
        for y in range(1, self.level.rows - 1):
            for x in range(1, self.level.cols - 1):
                pos = {'x': x, 'y': y}
                if self.level.tiles[y][x] == 0 and pos not in occupied:
                    free_positions.append(pos)
        self.position = random.choice(free_positions) if free_positions else None

    def draw(self, screen):
        if self.position is None:
            return
        x = self.position['x'] * self.block_size
        y = self.position['y'] * self.block_size
        screen.blit(self.image, (x, y))

