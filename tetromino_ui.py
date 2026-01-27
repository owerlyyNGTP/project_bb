import arcade
from constants import CELL_SIZE


class TetrominoUI:
    TETROMINO_COLORS = {
        'I': arcade.color.CYAN,
        'J': arcade.color.BLUE,
        'L': arcade.color.ORANGE,
        'O': arcade.color.YELLOW,
        'S': arcade.color.GREEN,
        'T': arcade.color.PURPLE,
        'Z': arcade.color.RED
    }

    TETROMINO_SHAPES = {
        'I': [[1, 1, 1, 1]],
        'J': [[1, 0, 0], [1, 1, 1]],
        'L': [[0, 0, 1], [1, 1, 1]],
        'O': [[1, 1], [1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'T': [[0, 1, 0], [1, 1, 1]],
        'Z': [[1, 1, 0], [0, 1, 1]]
    }

    def __init__(self, x, y, shape_type='I', size=CELL_SIZE*0.8):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.size = size
        self.color = self.TETROMINO_COLORS.get(shape_type, arcade.color.WHITE)
        self.shape = self.TETROMINO_SHAPES.get(shape_type, [[1]])
        self.is_selected = False

        self.texture = None
        try:
            self.texture = arcade.load_texture(
                f"assets/images/tetromino_{shape_type.lower()}.png")
        except FileNotFoundError:
            pass

    @property
    def shape_matrix(self):
        return self.shape

    @property
    def color_rgb(self):
        return (self.color.r, self.color.g, self.color.b)

    def draw(self):
        if self.is_selected:
            selection_rect = arcade.XYWH(
                self.x, self.y,
                self.size * max(len(self.shape[0]), 2) + 10,
                self.size * len(self.shape) + 10
            )
            arcade.draw_rect_outline(selection_rect, arcade.color.YELLOW, 3)

        if self.texture:
            arcade.draw_texture_rectangle(
                self.x, self.y,
                self.size * max(len(self.shape[0]), 2),
                self.size * len(self.shape),
                self.texture
            )
        else:
            rows = len(self.shape)
            cols = len(self.shape[0])
            start_x = self.x - (cols * self.size) / 2 + self.size / 2
            start_y = self.y + (rows * self.size) / 2 - self.size / 2

            for r in range(rows):
                for c in range(cols):
                    if self.shape[r][c]:
                        pos_x = start_x + c * self.size
                        pos_y = start_y - r * self.size

                        block_rect = arcade.XYWH(
                            pos_x,
                            pos_y,
                            self.size * 0.9,
                            self.size * 0.9
                        )
                        arcade.draw_rect_filled(block_rect, self.color)

                        arcade.draw_rect_outline(
                            block_rect, arcade.color.WHITE, 2)
