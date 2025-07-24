import pygame
TILE_SIZE = 32

class SnakeSprites:
    def __init__(self):
        self.sheet = pygame.image.load('snake-graphics.png').convert_alpha()

    def get_tile(self, tx, ty):
        rect = pygame.Rect(tx*64, ty*64, 64, 64)
        return pygame.transform.scale(self.sheet.subsurface(rect), (TILE_SIZE, TILE_SIZE))

    def draw_segment(self, screen, seg, prev_seg, next_seg, index, length):
        x = seg['x'] * TILE_SIZE
        y = seg['y'] * TILE_SIZE

        tx, ty = 1, 1

        if index == 0:
            if next_seg is None:
                tx, ty = 3, 0
            else:
                if seg['y'] < next_seg['y']:
                    tx, ty = 3, 0
                elif seg['x'] > next_seg['x']:
                    tx, ty = 4, 0
                elif seg['y'] > next_seg['y']:
                    tx, ty = 4, 1
                elif seg['x'] < next_seg['x']:
                    tx, ty = 3, 1
        elif index == length -1:
            if prev_seg is None:
                tx, ty = 3, 2
            else:
                if prev_seg['y'] < seg['y']: 
                    tx, ty = 3, 2
                elif prev_seg['x'] > seg['x']: 
                    tx, ty = 4, 2
                elif prev_seg['y'] > seg['y']:
                    tx, ty = 4, 3
                elif prev_seg['x'] < seg['x']:
                    tx, ty = 3, 3
        else:
            if prev_seg and next_seg:
                if (prev_seg['x'] < seg['x'] and next_seg['x'] > seg['x']) or (next_seg['x'] < seg['x'] and prev_seg['x'] > seg['x']):
                    tx, ty = 1, 0
                elif (prev_seg['y'] < seg['y'] and next_seg['y'] > seg['y']) or (next_seg['y'] < seg['y'] and prev_seg['y'] > seg['y']):
                    tx, ty = 2, 1
                else:
                    if (prev_seg['x'] < seg['x'] and next_seg['y'] > seg['y']) or (next_seg['x'] < seg['x'] and prev_seg['y'] > seg['y']):
                        tx, ty = 2, 0
                    elif (prev_seg['y'] < seg['y'] and next_seg['x'] < seg['x']) or (next_seg['y'] < seg['y'] and prev_seg['x'] < seg['x']):
                        tx, ty = 2, 2
                    elif (prev_seg['x'] > seg['x'] and next_seg['y'] < seg['y']) or (next_seg['x'] > seg['x'] and prev_seg['y'] < seg['y']):
                        tx, ty = 0, 1
                    elif (prev_seg['y'] > seg['y'] and next_seg['x'] > seg['x']) or (next_seg['y'] > seg['y'] and prev_seg['x'] > seg['x']):
                        tx, ty = 0, 0

        tile = self.get_tile(tx, ty)
        screen.blit(tile, (x, y))

    def draw_fruit(self, screen, x, y):
        tile = self.get_tile(0, 3)
        screen.blit(tile, (x, y))
