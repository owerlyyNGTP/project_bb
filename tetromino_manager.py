import random
from tetromino_ui import TetrominoUI
from constants import SCREEN_WIDTH, TETROMINO_AREA_Y, CELL_SIZE


class TetrominoManager:
    ALL_SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

    def __init__(self, count=3, area_y=TETROMINO_AREA_Y,
                 spacing=150, size_multiplier=0.7):
        self.count = count
        self.area_y = area_y
        self.spacing = spacing
        self.size = CELL_SIZE * size_multiplier
        self.tetrominos = []
        self.selected_index = None

        self.generate_random()

    def generate_random(self, allow_duplicates=False):
        self.tetrominos = []
        self.selected_index = None

        if allow_duplicates:
            selected_shapes = random.choices(self.ALL_SHAPES, k=self.count)
        else:
            if self.count <= len(self.ALL_SHAPES):
                selected_shapes = random.sample(self.ALL_SHAPES, self.count)
            else:
                selected_shapes = random.choices(self.ALL_SHAPES, k=self.count)

        center_x = SCREEN_WIDTH // 2
        if self.count == 3:
            positions = [
                center_x - self.spacing,
                center_x,
                center_x + self.spacing
            ]
        elif self.count == 2:
            positions = [
                center_x - self.spacing//2,
                center_x + self.spacing//2
            ]
        else:
            positions = [center_x]

        for i, shape in enumerate(selected_shapes):
            self.tetrominos.append(
                TetrominoUI(
                    x=positions[i],
                    y=self.area_y,
                    shape_type=shape,
                    size=self.size
                )
            )

        return self.tetrominos

    def get_tetrominos(self):
        return self.tetrominos

    def get_shapes(self):
        return [t.shape_type for t in self.tetrominos]

    def refresh(self, allow_duplicates=False):
        return self.generate_random(allow_duplicates)

    def check_click(self, x, y):
        click_radius = self.size * 2

        for i, tetromino in enumerate(self.tetrominos):
            if (tetromino.x - click_radius / 2 < x < tetromino.x + click_radius / 2 and
                    tetromino.y - click_radius / 2 < y < tetromino.y + click_radius / 2):
                self.select_tetromino(i)
                return i, tetromino.shape_type

        return None, None

    def select_tetromino(self, index):
        for i, tetromino in enumerate(self.tetrominos):
            tetromino.is_selected = (i == index)
        self.selected_index = index

    def get_selected(self):
        if self.selected_index is not None:
            return self.tetrominos[self.selected_index]
        return None

    def draw(self):
        for tetromino in self.tetrominos:
            tetromino.draw()
