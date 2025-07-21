import random
TILE_SIZE = 32

class Fruit:
    def __init__(self, level):
        self.level = level
        self.position = None
        self.spawn([])

    def spawn(self, occupied_positions):
        free_positions = []
        for y in range(1, self.level.rows - 1):
            for x in range(1, self.level.cols - 1):
                pos = {'x': x, 'y': y}
                if self.level.tiles[y][x] == 0 and pos not in occupied_positions:
                    free_positions.append(pos)
        self.position = random.choice(free_positions) if free_positions else None

    def draw(self, screen, sprites):
        if self.position is None:
            return
        x = self.position['x'] * TILE_SIZE
        y = self.position['y'] * TILE_SIZE
        sprites.draw_fruit(screen, x, y)

