import pygame

TILE_SIZE = 32

class Level:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.tiles = [[0 for _ in range(cols)] for _ in range(rows)]

    
    def is_wall(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.tiles[x][y] == 1
        return False

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.tiles[y][x] == 1:
                    screen.blit(self.wall_image, (x * TILE_SIZE, y * TILE_SIZE))