from button import UIButton
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from windows.base_window import BaseWindow
import arcade
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AdventureMenuWindow(BaseWindow):
    def __init__(self):
        super().__init__("Adventure Mode")

        self.level1_button = UIButton(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 50,
            width=300,
            height=80,
            text="Уровень 1",
            color=(100, 150, 255)
        )

        self.level2_button = UIButton(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 70,
            width=300,
            height=80,
            text="Уровень 2",
            color=(150, 100, 255)
        )

        self.back_button = UIButton(
            x=100,
            y=SCREEN_HEIGHT - 50,
            width=150,
            height=40,
            text="← Назад",
            color=(255, 100, 100)
        )

        self.level2_locked = False

        self.ui_buttons = [self.level1_button,
                           self.level2_button, self.back_button]

        self.title_text = arcade.Text(
            "ADVENTURE MODE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            arcade.color.WHITE,
            48,
            align="center",
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def on_draw(self):
        super().on_draw()
        self.title_text.draw()

        for button in self.ui_buttons:
            button.draw()

        if self.level2_locked:
            arcade.draw_text(
                "LOCKED",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 70,
                arcade.color.RED,
                14,
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
                    if ui_button.text == "Уровень 1":
                        self.close()
                        from windows.level_window import LevelWindow
                        new_window = LevelWindow(1)
                        arcade.run()
                        return True

                    elif ui_button.text == "Уровень 2" and not self.level2_locked:
                        self.close()
                        from windows.level_window import LevelWindow
                        new_window = LevelWindow(2)
                        arcade.run()
                        return True

                    elif ui_button.text == "← Назад":
                        self.close()
                        from windows.main_menu_window import MainMenuWindow
                        new_window = MainMenuWindow()
                        arcade.run()
                        return True
        return False
