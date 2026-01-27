from game_logic import GameLogic
from tetromino_manager import TetrominoManager
from button import UIButton
from constants import (TETROMINO_AREA_Y, SCREEN_WIDTH,
                       SCREEN_HEIGHT, GRID_COLOR, GRID_ROWS, GRID_COLS,
                       CELL_SIZE, GRID_MARGIN_X, GRID_MARGIN_Y, TEXT_COLOR)
from windows.base_window import BaseWindow
from databases import db
import arcade
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LevelWindow(BaseWindow):
    def __init__(self, level_number=1):
        super().__init__(f"Level {level_number}")
        self.level_number = level_number

        self.title_y = SCREEN_HEIGHT - 50
        self.rating_y = SCREEN_HEIGHT - 50

        self.tetromino_area_y = TETROMINO_AREA_Y - 20

        self.back_button = UIButton(
            x=SCREEN_WIDTH - 100,
            y=SCREEN_HEIGHT - 50,
            width=150,
            height=40,
            text="← Назад",
            color=(255, 100, 100)
        )

        self.restart_button = UIButton(
            x=SCREEN_WIDTH - 250,
            y=SCREEN_HEIGHT - 50,
            width=150,
            height=40,
            text="Рестарт",
            color=(100, 200, 100)
        )

        self.game_logic = GameLogic()

        if level_number == 1:
            self.game_logic.moves_left = 30
            self.target_rating = 1000
        else:
            self.game_logic.moves_left = 25
            self.target_rating = 2000

        self.current_rating = 0

        self.tetromino_manager = TetrominoManager(
            count=3,
            area_y=self.tetromino_area_y,
            spacing=150,
            size_multiplier=0.7
        )

        self.title_text = arcade.Text(
            f"УРОВЕНЬ {self.level_number}",
            30,
            self.title_y,
            arcade.color.WHITE,
            36,
            align="left",
            anchor_x="left",
            anchor_y="center",
            bold=True
        )

        self.rating_text = arcade.Text(
            f"Рейтинг: {self.current_rating:,} / {self.target_rating:,}",
            SCREEN_WIDTH // 2,
            self.rating_y,
            arcade.color.WHITE,
            24,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

        self.moves_text = arcade.Text(
            f"Ходы: {self.game_logic.moves_left}",
            SCREEN_WIDTH // 2,
            self.rating_y - 35,
            arcade.color.WHITE,
            20,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

        self.tetromino_title_text = arcade.Text(
            "ВЫБЕРИТЕ ФИГУРУ:",
            SCREEN_WIDTH // 2,
            self.tetromino_area_y + 80,
            arcade.color.LIGHT_GRAY,
            20,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

        self.ui_buttons = [self.back_button, self.restart_button]

        self.show_game_over = False
        self.show_win = False

        self.hover_grid_x = None
        self.hover_grid_y = None
        self.can_place_at_hover = False

        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def on_draw(self):
        super().on_draw()

        offset_x, offset_y = self.game_logic.get_shake_offset()
        self.shake_offset_x = offset_x
        self.shake_offset_y = offset_y

        self.game_logic.update_shake()

        self.draw_grid()
        self.draw_tetromino_area()
        self.draw_separators()
        self.tetromino_manager.draw()

        self.draw_game_grid()

        if self.hover_grid_x is not None and self.hover_grid_y is not None:
            if self.can_place_at_hover:
                self.draw_preview()

        for button in self.ui_buttons:
            button.draw()

        self.title_text.draw()

        self.rating_text.x = SCREEN_WIDTH // 2 + self.shake_offset_x
        self.rating_text.y = self.rating_y + self.shake_offset_y
        self.rating_text.draw()

        self.moves_text.x = SCREEN_WIDTH // 2 + self.shake_offset_x
        self.moves_text.y = self.rating_y - 30 + self.shake_offset_y
        self.moves_text.draw()

        self.tetromino_title_text.x = SCREEN_WIDTH // 2 + self.shake_offset_x
        self.tetromino_title_text.y = self.tetromino_area_y + 60 + self.shake_offset_y
        self.tetromino_title_text.draw()

        if self.show_game_over:
            self.draw_game_over_message()
        elif self.show_win:
            self.draw_win_message()

    def draw_grid(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        grid_rect = arcade.XYWH(
            GRID_MARGIN_X + (GRID_COLS * CELL_SIZE) // 2 + offset_x,
            GRID_MARGIN_Y + (GRID_ROWS * CELL_SIZE) // 2 + offset_y,
            GRID_COLS * CELL_SIZE,
            GRID_ROWS * CELL_SIZE
        )
        arcade.draw_rect_filled(grid_rect, (20, 20, 40))

        for row in range(GRID_ROWS + 1):
            y = GRID_MARGIN_Y + row * CELL_SIZE + offset_y
            arcade.draw_line(
                GRID_MARGIN_X + offset_x, y,
                GRID_MARGIN_X + GRID_COLS * CELL_SIZE + offset_x, y,
                GRID_COLOR, 2
            )

        for col in range(GRID_COLS + 1):
            x = GRID_MARGIN_X + col * CELL_SIZE + offset_x
            arcade.draw_line(
                x, GRID_MARGIN_Y + offset_y,
                x, GRID_MARGIN_Y + GRID_ROWS * CELL_SIZE + offset_y,
                GRID_COLOR, 2
            )

    def draw_tetromino_area(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        area_rect = arcade.XYWH(
            SCREEN_WIDTH // 2 + offset_x,
            TETROMINO_AREA_Y + offset_y,
            SCREEN_WIDTH - 100,
            120
        )
        arcade.draw_rect_filled(area_rect, (40, 40, 60))

        arcade.draw_rect_outline(area_rect, GRID_COLOR, 2)

    def draw_separators(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        separator_height = 80
        separator_y_center = TETROMINO_AREA_Y + offset_y

        arcade.draw_line(
            SCREEN_WIDTH // 2 - 120 // 2 + offset_x,
            separator_y_center - separator_height // 2,
            SCREEN_WIDTH // 2 - 120 // 2 + offset_x,
            separator_y_center + separator_height // 2,
            GRID_COLOR, 2
        )

        arcade.draw_line(
            SCREEN_WIDTH // 2 + 120 // 2 + offset_x,
            separator_y_center - separator_height // 2,
            SCREEN_WIDTH // 2 + 120 // 2 + offset_x,
            separator_y_center + separator_height // 2,
            GRID_COLOR, 2
        )

    def draw_game_grid(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        grid = self.game_logic.get_grid_state()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if grid[r][c] != 0:
                    x = GRID_MARGIN_X + c * CELL_SIZE + CELL_SIZE // 2 + offset_x
                    y = GRID_MARGIN_Y + (GRID_ROWS - 1 - r) * \
                        CELL_SIZE + CELL_SIZE // 2 + offset_y

                    colors = [
                        (0, 0, 0),
                        (255, 100, 100),
                        (100, 255, 100),
                        (100, 100, 255),
                        (255, 255, 100),
                        (255, 100, 255),
                        (100, 255, 255),
                    ]
                    color = colors[min(grid[r][c], len(colors) - 1)]

                    block_rect = arcade.XYWH(
                        x, y, CELL_SIZE * 0.9, CELL_SIZE * 0.9)
                    arcade.draw_rect_filled(block_rect, color)
                    arcade.draw_rect_outline(block_rect, TEXT_COLOR, 2)

    def draw_preview(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        selected = self.tetromino_manager.get_selected()
        if selected and self.hover_grid_x is not None and self.hover_grid_y is not None:
            shape = selected.shape_matrix
            color_tuple = selected.color_rgb

            for r in range(len(shape)):
                for c in range(len(shape[0])):
                    if shape[r][c]:
                        x = GRID_MARGIN_X + \
                            (self.hover_grid_x + c) * \
                            CELL_SIZE + CELL_SIZE // 2 + offset_x
                        y = GRID_MARGIN_Y + (
                            GRID_ROWS - 1 - (self.hover_grid_y + r)) * CELL_SIZE + CELL_SIZE // 2 + offset_y

                        block_rect = arcade.XYWH(
                            x, y, CELL_SIZE * 0.9, CELL_SIZE * 0.9)
                        arcade.draw_rect_filled(
                            block_rect, (*color_tuple, 150))
                        arcade.draw_rect_outline(
                            block_rect, arcade.color.WHITE, 2)

    def draw_game_over_message(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        overlay_rect = arcade.XYWH(
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + offset_y,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )
        arcade.draw_rect_filled(overlay_rect, (0, 0, 0, 200))

        arcade.draw_text(
            "ИГРА ОКОНЧЕНА!",
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + 50 + offset_y,
            arcade.color.RED,
            48,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            f"Финальный счет: {self.game_logic.score}",
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + offset_y,
            arcade.color.WHITE,
            32,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Нажмите 'Рестарт' для новой игры",
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 - 60 + offset_y,
            arcade.color.YELLOW,
            24,
            anchor_x="center",
            anchor_y="center"
        )

    def draw_win_message(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        overlay_rect = arcade.XYWH(
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + offset_y,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )
        arcade.draw_rect_filled(overlay_rect, (0, 0, 0, 200))

        arcade.draw_text(
            "УРОВЕНЬ ПРОЙДЕН!",
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + 50 + offset_y,
            arcade.color.GOLD,
            48,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            f"Счет: {self.game_logic.score} (Требовалось: {self.target_rating})",
            SCREEN_WIDTH // 2 + offset_x,
            SCREEN_HEIGHT // 2 + offset_y,
            arcade.color.WHITE,
            32,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for button in self.ui_buttons:
            button.check_hover(x, y)

        selected = self.tetromino_manager.get_selected()
        if selected:
            grid_x = int(
                (x - GRID_MARGIN_X - self.shake_offset_x) // CELL_SIZE)
            grid_y = GRID_ROWS - 1 - \
                int((y - GRID_MARGIN_Y - self.shake_offset_y) // CELL_SIZE)

            if 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS:
                self.hover_grid_x = grid_x
                self.hover_grid_y = grid_y
                shape = selected.shape_matrix
                self.can_place_at_hover = self.game_logic.can_place_tetromino(
                    shape, grid_x, grid_y)
            else:
                self.hover_grid_x = None
                self.hover_grid_y = None
                self.can_place_at_hover = False
        else:
            self.hover_grid_x = None
            self.hover_grid_y = None
            self.can_place_at_hover = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for ui_button in self.ui_buttons:
                if ui_button.is_hovered:
                    if ui_button.text == "← Назад":
                        self.close()
                        from windows.adventure_menu_window import AdventureMenuWindow
                        new_window = AdventureMenuWindow()
                        arcade.run()
                        return True
                    elif ui_button.text == "Рестарт":
                        self.restart_level()
                        return True

            idx, shape = self.tetromino_manager.check_click(x, y)
            if idx is not None:
                return True

            selected = self.tetromino_manager.get_selected()
            if selected:
                grid_x = int(
                    (x - GRID_MARGIN_X - self.shake_offset_x) // CELL_SIZE)
                grid_y = GRID_ROWS - 1 - \
                    int((y - GRID_MARGIN_Y - self.shake_offset_y) // CELL_SIZE)

                if 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS:
                    if self.game_logic.can_place_tetromino(selected.shape_matrix, grid_x, grid_y):
                        self.game_logic.place_tetromino(
                            selected.shape_matrix, grid_x, grid_y)
                        lines_cleared, points = self.game_logic.check_and_clear_lines()

                        if lines_cleared > 0:
                            pass

                        self.current_rating = self.game_logic.score
                        self.rating_text.text = f"Рейтинг: {self.current_rating:,} / {self.target_rating:,}"
                        self.moves_text.text = f"Ходы: {self.game_logic.moves_left}"
                        self.tetromino_manager.refresh()

                        if self.game_logic.check_game_over(self.tetromino_manager.tetrominos):
                            is_new_record = db.save_record(
                                game_mode="adventure",
                                score=self.game_logic.score,
                                level=self.level_number
                            )
                            self.show_game_over = True

                        if self.game_logic.check_win_condition(self.target_rating):
                            db.save_record(
                                game_mode="adventure",
                                score=self.game_logic.score,
                                level=self.level_number
                            )
                            self.show_win = True

                        return True

            return True
        return False

    def restart_level(self):
        self.game_logic.reset()
        if self.level_number == 1:
            self.game_logic.moves_left = 30
            self.target_rating = 1000
        else:
            self.game_logic.moves_left = 25
            self.target_rating = 2000

        self.current_rating = 0
        self.rating_text.text = f"Рейтинг: {self.current_rating:,} / {self.target_rating:,}"
        self.moves_text.text = f"Ходы: {self.game_logic.moves_left}"
        self.tetromino_manager.refresh()
        self.show_game_over = False
        self.show_win = False
        self.shake_offset_x = 0
        self.shake_offset_y = 0
