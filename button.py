import arcade
from constants import BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR


class UIButton:
    def __init__(self, x, y, width, height, text,
                 color=None, hover_color=None,
                 text_color=TEXT_COLOR):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color or BUTTON_COLOR
        self.hover_color = hover_color or BUTTON_HOVER_COLOR
        self.text_color = text_color
        self.is_hovered = False
        self.is_visible = True

        self.text_obj = arcade.Text(
            text=text,
            x=x,
            y=y,
            color=text_color,
            font_size=20,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

    def draw(self):
        if not self.is_visible:
            return

        color = self.hover_color if self.is_hovered else self.color

        rect = arcade.XYWH(self.x, self.y, self.width, self.height)
        arcade.draw_rect_filled(rect, color)

        if self.is_hovered:
            arcade.draw_rect_outline(rect, arcade.color.YELLOW, 3)
            self.text_obj.font_size = 22
            self.text_obj.bold = True
        else:
            self.text_obj.font_size = 20
            self.text_obj.bold = False

        self.text_obj.draw()

    def check_hover(self, x, y):
        if not self.is_visible:
            self.is_hovered = False
            return False

        self.is_hovered = (
            self.x - self.width/2 < x < self.x + self.width/2 and
            self.y - self.height/2 < y < self.y + self.height/2
        )
        return self.is_hovered
