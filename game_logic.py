import numpy as np
import random
from constants import GRID_ROWS, GRID_COLS


class GameLogic:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.score = 0
        self.moves_left = 30
        self.game_over = False
        self.game_won = False
        self.shake_intensity = 0
        self.shake_timer = 0

    def can_place_tetromino(self, tetromino_shape, grid_x, grid_y):
        rows = len(tetromino_shape)
        cols = len(tetromino_shape[0])

        if grid_x < 0 or grid_y < 0 or grid_x + cols > GRID_COLS or grid_y + rows > GRID_ROWS:
            return False

        for r in range(rows):
            for c in range(cols):
                if tetromino_shape[r][c] and self.grid[grid_y + r][grid_x + c]:
                    return False
        return True

    def place_tetromino(self, tetromino_shape, grid_x, grid_y, value=1):
        rows = len(tetromino_shape)
        cols = len(tetromino_shape[0])

        for r in range(rows):
            for c in range(cols):
                if tetromino_shape[r][c]:
                    self.grid[grid_y + r][grid_x + c] = value

        self.moves_left -= 1
        return True

    def check_and_clear_lines(self):
        lines_cleared = 0

        rows_to_clear = []
        for r in range(GRID_ROWS):
            if all(self.grid[r][c] != 0 for c in range(GRID_COLS)):
                rows_to_clear.append(r)

        cols_to_clear = []
        for c in range(GRID_COLS):
            if all(self.grid[r][c] != 0 for r in range(GRID_ROWS)):
                cols_to_clear.append(c)

        for r in rows_to_clear:
            for c in range(GRID_COLS):
                self.grid[r][c] = 0
            lines_cleared += 1

        for c in cols_to_clear:
            for r in range(GRID_ROWS):
                self.grid[r][c] = 0
            lines_cleared += 1

        if lines_cleared == 1:
            points = 100
        elif lines_cleared == 2:
            points = 300
        elif lines_cleared >= 3:
            points = 600
        else:
            points = 0

        self.score += points

        if lines_cleared > 0:
            self.start_screen_shake(lines_cleared)

        return lines_cleared, points

    def start_screen_shake(self, intensity):
        self.shake_intensity = intensity * 3
        self.shake_timer = 10

    def update_shake(self):
        if self.shake_timer > 0:
            self.shake_timer -= 1
            return True
        self.shake_intensity = 0
        return False

    def get_shake_offset(self):
        if self.shake_timer > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            return offset_x, offset_y
        return 0, 0

    def check_game_over(self, available_tetrominos):
        if self.game_over:
            return True

        for tetromino in available_tetrominos:
            shape = tetromino.shape_matrix

            for r in range(GRID_ROWS - len(shape) + 1):
                for c in range(GRID_COLS - len(shape[0]) + 1):
                    if self.can_place_tetromino(shape, c, r):
                        return False

        self.game_over = True
        return True

    def check_win_condition(self, target_score):
        if self.score >= target_score:
            self.game_won = True
            return True
        return False

    def get_grid_state(self):
        return self.grid

    def reset(self):
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.score = 0
        self.moves_left = 30
        self.game_over = False
        self.game_won = False
        self.shake_intensity = 0
        self.shake_timer = 0
