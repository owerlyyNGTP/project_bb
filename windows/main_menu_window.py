from button import UIButton
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from windows.base_window import BaseWindow
import arcade
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MainMenuWindow(BaseWindow):
    def __init__(self):
        super().__init__("Block Blast - Главное меню")

        self.adventure_button = UIButton(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            width=250,
            height=70,
            text="Adventure",
            color=(100, 200, 100)
        )

        self.classic_button = UIButton(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 100,
            width=250,
            height=70,
            text="Classic",
            color=(255, 150, 50)
        )

        self.records_button = UIButton(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 200,
            width=250,
            height=70,
            text="История рекордов",
            color=(150, 100, 255)
        )

        self.ui_buttons = [self.adventure_button, self.classic_button, self.records_button]

        self.title_text = arcade.Text(
            text="BLOCK BLAST",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT - 150,
            color=arcade.color.WHITE,
            font_size=48,
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

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for button in self.ui_buttons:
            button.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for ui_button in self.ui_buttons:
                if ui_button.is_hovered:
                    if ui_button.text == "Adventure":
                        self.close()
                        from windows.adventure_menu_window import AdventureMenuWindow
                        new_window = AdventureMenuWindow()
                        arcade.run()
                        return True

                    elif ui_button.text == "Classic":
                        self.close()
                        from windows.classic_window import ClassicWindow
                        new_window = ClassicWindow()
                        arcade.run()
                        return True
                    
                    elif ui_button.text == "История рекордов":
                        self.close()
                        from windows.records_window import RecordsWindow
                        new_window = RecordsWindow()
                        arcade.run()
                        return True
        return False
