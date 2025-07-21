TILE_SIZE = 32

DIRECTIONS = {
    'UP': (0, -1),
    'RIGHT': (1, 0),
    'DOWN': (0, 1),
    'LEFT': (-1, 0)
}

KEY_DIRECTION = {
    1073741906: 'UP',
    1073741905: 'DOWN',
    1073741903: 'RIGHT',
    1073741904: 'LEFT'
}

class Snake:
    def __init__(self, level):
        self.level = level
        self.segments = []
        self.direction = 'RIGHT'
        self.grow_segments = 0
        self.init_snake()

    def init_snake(self):
        self.segments = []
        x, y = 10, 10
        for i in range(4):
            self.segments.append({'x': x - i, 'y': y})

    def head(self):
        return self.segments[0]

    def move(self):
        dir_vector = DIRECTIONS[self.direction]
        next_x = (self.head()['x'] + dir_vector[0]) % self.level.cols
        next_y = (self.head()['y'] + dir_vector[1]) % self.level.rows

        # Colisão com o próprio corpo
        for seg in self.segments:
            if seg['x'] == next_x and seg['y'] == next_y:
                return False

        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.segments.pop()

        self.segments.insert(0, {'x': next_x, 'y': next_y})
        return True

    def grow(self):
        self.grow_segments += 1

    def change_direction(self, key):
        opposites = {'UP':'DOWN', 'DOWN':'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
        new_dir = KEY_DIRECTION.get(key)
        if new_dir and new_dir != opposites[self.direction]:
            self.direction = new_dir

    def reset(self):
        self.init_snake()
        self.direction = 'RIGHT'
        self.grow_segments = 0

    def draw(self, screen, sprites):
        for i, seg in enumerate(self.segments):
            prev_seg = self.segments[i-1] if i > 0 else None
            next_seg = self.segments[i+1] if i < len(self.segments)-1 else None
            sprites.draw_segment(screen, seg, prev_seg, next_seg, i, len(self.segments))
