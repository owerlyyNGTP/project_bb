from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR
import arcade
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BaseWindow(arcade.Window):
    def __init__(self, title=""):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title)
        arcade.set_background_color(BACKGROUND_COLOR)

        self.ui_buttons = []

    def on_draw(self):
        self.clear(BACKGROUND_COLOR)
        for button in self.ui_buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y
        for button in self.ui_buttons:
            button.check_hover(x, y)
