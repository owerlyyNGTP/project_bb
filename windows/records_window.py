import arcade
from button import UIButton
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR
from windows.base_window import BaseWindow
from databases import db
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RecordsWindow(BaseWindow):
    def __init__(self):
        super().__init__("История рекордов")

        self.records = db.get_all_records()

        self.title_text = arcade.Text(
            text="ИСТОРИЯ РЕКОРДОВ",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT - 100,
            color=arcade.color.GOLD,
            font_size=36,
            align="center",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        self.back_button = UIButton(
            x=100,
            y=SCREEN_HEIGHT - 50,
            width=150,
            height=40,
            text="← Назад",
            color=(255, 100, 100)
        )

        self.all_button = UIButton(
            x=SCREEN_WIDTH // 2 - 200,
            y=SCREEN_HEIGHT - 160,
            width=120,
            height=40,
            text="Все",
            color=(100, 150, 255)
        )

        self.classic_button = UIButton(
            x=SCREEN_WIDTH // 2 - 60,
            y=SCREEN_HEIGHT - 160,
            width=120,
            height=40,
            text="Classic",
            color=(100, 150, 255)
        )

        self.adventure_button = UIButton(
            x=SCREEN_WIDTH // 2 + 80,
            y=SCREEN_HEIGHT - 160,
            width=120,
            height=40,
            text="Adventure",
            color=(100, 150, 255)
        )

        self.ui_buttons = [
            self.back_button,
            self.all_button,
            self.classic_button,
            self.adventure_button
        ]

        self.current_filter = "all"

        if self.records:
            self.best_score = max(record[1] for record in self.records)
            self.total_games = len(self.records)
        else:
            self.best_score = 0
            self.total_games = 0

    def apply_filter(self, filter_type: str):
        self.current_filter = filter_type

        if filter_type == "all":
            self.records = db.get_all_records()
        elif filter_type == "classic":
            self.records = db.get_records_by_mode("classic", limit=50)
        elif filter_type == "adventure":
            self.records = db.get_records_by_mode("adventure", limit=50)

    def on_draw(self):
        super().on_draw()

        table_rect = arcade.XYWH(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            SCREEN_WIDTH - 100,
            SCREEN_HEIGHT - 300
        )
        arcade.draw_rect_filled(table_rect, (40, 40, 60))
        arcade.draw_rect_outline(table_rect, TEXT_COLOR, 2)

        arcade.draw_text(
            "Дата",
            SCREEN_WIDTH // 2 - 350,
            SCREEN_HEIGHT - 220,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            "Режим",
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 220,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            "Уровень",
            SCREEN_WIDTH // 2 + 50,
            SCREEN_HEIGHT - 220,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            "Рекорд",
            SCREEN_WIDTH // 2 + 250,
            SCREEN_HEIGHT - 220,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_line(
            SCREEN_WIDTH // 2 - 400,
            SCREEN_HEIGHT - 240,
            SCREEN_WIDTH // 2 + 400,
            SCREEN_HEIGHT - 240,
            TEXT_COLOR,
            2
        )

        y_position = SCREEN_HEIGHT - 270
        records_displayed = 0

        for record in self.records:
            if records_displayed >= 15:
                break

            game_mode, score, level, date = record

            row_color = (50, 50, 70) if records_displayed % 2 == 0 else (
                60, 60, 80)

            row_rect = arcade.XYWH(
                SCREEN_WIDTH // 2,
                y_position - 15,
                SCREEN_WIDTH - 100,
                40
            )
            arcade.draw_rect_filled(row_rect, row_color)

            arcade.draw_text(
                date,
                SCREEN_WIDTH // 2 - 350,
                y_position,
                TEXT_COLOR,
                18,
                anchor_x="center",
                anchor_y="center"
            )

            mode_display = "Classic" if game_mode == "classic" else "Adventure"
            arcade.draw_text(
                mode_display,
                SCREEN_WIDTH // 2 - 150,
                y_position,
                TEXT_COLOR,
                18,
                anchor_x="center",
                anchor_y="center"
            )

            level_display = str(level) if level else "-"
            arcade.draw_text(
                level_display,
                SCREEN_WIDTH // 2 + 50,
                y_position,
                TEXT_COLOR,
                18,
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                f"{score:,}",
                SCREEN_WIDTH // 2 + 250,
                y_position,
                (255, 215, 0) if records_displayed == 0 else arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center",
                bold=(records_displayed == 0)
            )

            y_position -= 45
            records_displayed += 1

        if not self.records:
            arcade.draw_text(
                "Нет сохраненных рекордов",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                TEXT_COLOR,
                24,
                anchor_x="center",
                anchor_y="center"
            )

        arcade.draw_text(
            f"Всего игр: {self.total_games}",
            SCREEN_WIDTH // 2 - 150,
            80,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"Лучший результат: {self.best_score:,}",
            SCREEN_WIDTH // 2 + 150,
            80,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        self.title_text.draw()
        for button in self.ui_buttons:
            button.draw()

        arcade.draw_text(
            f"Текущий фильтр: {self.current_filter.upper()}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 200,
            arcade.color.LIGHT_BLUE,
            16,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for button in self.ui_buttons:
            button.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for ui_button in self.ui_buttons:
                if ui_button.is_hovered:
                    if ui_button.text == "← Назад":
                        self.close()
                        from windows.main_menu_window import MainMenuWindow
                        new_window = MainMenuWindow()
                        arcade.run()
                        return True

                    elif ui_button.text == "Все":
                        self.apply_filter("all")
                        return True

                    elif ui_button.text == "Classic":
                        self.apply_filter("classic")
                        return True

                    elif ui_button.text == "Adventure":
                        self.apply_filter("adventure")
                        return True
        return False
