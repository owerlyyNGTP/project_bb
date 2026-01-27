from game_logic import GameLogic
from button import UIButton
from constants import (TETROMINO_AREA_Y, TEXT_COLOR, SCREEN_WIDTH,
                       SCREEN_HEIGHT, GRID_COLOR, GRID_ROWS, GRID_COLS,
                       CELL_SIZE, GRID_MARGIN_X, GRID_MARGIN_Y)
from windows.base_window import BaseWindow
from tetromino_manager import TetrominoManager
from databases import db
import arcade
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ClassicWindow(BaseWindow):
    def __init__(self):
        super().__init__("Classic Mode")

        self.back_button = UIButton(
            x=SCREEN_WIDTH - 100,
            y=SCREEN_HEIGHT - 50,
            width=150,
            height=40,
            text="← Меню",
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

        self.title_text_line1 = arcade.Text(
            "CLASSIC",
            30,
            SCREEN_HEIGHT - 170,
            arcade.color.WHITE,
            48,
            align="left",
            anchor_x="left",
            anchor_y="center",
            bold=True
        )

        self.title_text_line2 = arcade.Text(
            "MODE",
            30,
            SCREEN_HEIGHT - 220,
            arcade.color.WHITE,
            48,
            align="left",
            anchor_x="left",
            anchor_y="center",
            bold=True
        )
        self.game_logic = GameLogic()

        self.current_score = 0
        self.record_score = db.get_classic_record()

        self.current_text = arcade.Text(
            f"Текущий: {self.current_score}",
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT - 80,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        self.record_text = arcade.Text(
            f"Рекорд: {self.record_score:,}",
            SCREEN_WIDTH // 2 + 50,
            SCREEN_HEIGHT - 80,
            (255, 215, 0),
            24,
            anchor_x="center"
        )

        self.tetromino_title_text = arcade.Text(
            "ДОСТУПНЫЕ ФИГУРЫ:",
            SCREEN_WIDTH // 2,
            TETROMINO_AREA_Y + 40,
            arcade.color.LIGHT_GRAY,
            20,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

        self.tetromino_manager = TetrominoManager(
            count=3,
            area_y=TETROMINO_AREA_Y - 30,
            spacing=150,
            size_multiplier=0.7
        )

        self.ui_buttons = [self.back_button, self.restart_button]
        self.show_separators = True

        self.show_game_over = False

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

        if self.show_separators:
            self.draw_separators()

        self.tetromino_manager.draw()

        self.draw_game_grid()

        if self.hover_grid_x is not None and self.hover_grid_y is not None:
            if self.can_place_at_hover:
                self.draw_preview()

        for button in self.ui_buttons:
            button.draw()

        self.title_text_line1.draw()
        self.title_text_line2.draw()

        self.current_text.x = SCREEN_WIDTH // 2 - 200 + self.shake_offset_x
        self.current_text.y = SCREEN_HEIGHT - 80 + self.shake_offset_y
        self.current_text.draw()

        self.record_text.draw()

        self.tetromino_title_text.x = SCREEN_WIDTH // 2 + self.shake_offset_x
        self.tetromino_title_text.y = TETROMINO_AREA_Y + 40 + self.shake_offset_y
        self.tetromino_title_text.draw()

        if self.show_game_over:
            self.draw_game_over_message()

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

        border_rect = arcade.XYWH(
            GRID_MARGIN_X + (GRID_COLS * CELL_SIZE) // 2 + offset_x,
            GRID_MARGIN_Y + (GRID_ROWS * CELL_SIZE) // 2 + offset_y,
            GRID_COLS * CELL_SIZE + 4,
            GRID_ROWS * CELL_SIZE + 4
        )
        arcade.draw_rect_outline(border_rect, TEXT_COLOR, 4)

    def draw_tetromino_area(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        area_rect = arcade.XYWH(
            SCREEN_WIDTH // 2 + offset_x,
            TETROMINO_AREA_Y - 30 + offset_y,
            SCREEN_WIDTH - 100,
            100
        )
        arcade.draw_rect_filled(area_rect, (40, 40, 60))

        arcade.draw_rect_outline(area_rect, GRID_COLOR, 2)

    def draw_separators(self):
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y

        manager_spacing = self.tetromino_manager.spacing
        separator_height = 80
        separator_y_center = TETROMINO_AREA_Y - 30 + offset_y

        arcade.draw_line(
            SCREEN_WIDTH // 2 - manager_spacing // 2 + offset_x,
            separator_y_center - separator_height // 2,
            SCREEN_WIDTH // 2 - manager_spacing // 2 + offset_x,
            separator_y_center + separator_height // 2,
            GRID_COLOR, 2
        )

        arcade.draw_line(
            SCREEN_WIDTH // 2 + manager_spacing // 2 + offset_x,
            separator_y_center - separator_height // 2,
            SCREEN_WIDTH // 2 + manager_spacing // 2 + offset_x,
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
                    if ui_button.text == "← Меню":
                        self.close()
                        from windows.main_menu_window import MainMenuWindow
                        new_window = MainMenuWindow()
                        arcade.run()
                        return True

                    elif ui_button.text == "Рестарт":
                        self.restart_game()
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

                        self.current_score = self.game_logic.score
                        self.current_text.text = f"Текущий: {self.current_score}"
                        self.tetromino_manager.refresh()

                        if self.game_logic.check_game_over(self.tetromino_manager.tetrominos):
                            is_new_record = db.save_record(
                                game_mode="classic",
                                score=self.game_logic.score,
                                level=None
                            )

                            if is_new_record:
                                self.record_score = self.game_logic.score
                                self.record_text.text = f"Рекорд: {self.record_score:,}"
                            self.show_game_over = True
                            return True
                        return True

            return True

        return False

    def restart_game(self):
        self.game_logic.reset()
        self.current_score = 0
        self.current_text.text = f"Текущий: {self.current_score}"
        self.record_score = db.get_classic_record()
        self.record_text.text = f"Рекорд: {self.record_score:,}"
        self.tetromino_manager.refresh()
        self.show_game_over = False
        self.shake_offset_x = 0
        self.shake_offset_y = 0
