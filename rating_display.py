import arcade
from constants import RATING_COLOR, NEEDED_RATING_COLOR, TEXT_COLOR


class RatingDisplay:
    def __init__(self, x, y, current_rating=0, target_rating=1000,
                 is_record=False, show_target=True):
        self.x = x
        self.y = y
        self.current_rating = current_rating
        self.target_rating = target_rating
        self.is_record = is_record
        self.show_target = show_target

        if self.is_record:
            self.title_text = arcade.Text(
                text="РЕКОРД:",
                x=self.x - 140,
                y=self.y + 10,
                color=TEXT_COLOR,
                font_size=18,
                anchor_y="center"
            )
            self.value_text = arcade.Text(
                text=f"{self.current_rating:,}",
                x=self.x + 50,
                y=self.y + 10,
                color=RATING_COLOR,
                font_size=24,
                anchor_x="right",
                anchor_y="center"
            )
        else:
            self.title_text = arcade.Text(
                text="РЕЙТИНГ:",
                x=self.x - 140,
                y=self.y + 10,
                color=TEXT_COLOR,
                font_size=18,
                anchor_y="center"
            )
            self.value_text = arcade.Text(
                text=f"{self.current_rating:,}",
                x=self.x + 50,
                y=self.y + 10,
                color=RATING_COLOR,
                font_size=24,
                anchor_x="right",
                anchor_y="center"
            )

            if self.show_target:
                self.target_title_text = arcade.Text(
                    text="НУЖНО:",
                    x=self.x - 140,
                    y=self.y - 15,
                    color=TEXT_COLOR,
                    font_size=18,
                    anchor_y="center"
                )
                self.target_value_text = arcade.Text(
                    text=f"{self.target_rating:,}",
                    x=self.x + 50,
                    y=self.y - 15,
                    color=NEEDED_RATING_COLOR,
                    font_size=20,
                    anchor_x="right",
                    anchor_y="center"
                )

    def draw(self):
        background_rect = arcade.XYWH(self.x, self.y, 300, 80)
        arcade.draw_rect_filled(background_rect, (40, 40, 60))
        arcade.draw_rect_outline(background_rect, TEXT_COLOR, 2)

        self.title_text.draw()
        self.value_text.draw()

        if self.show_target and not self.is_record:
            self.target_title_text.draw()
            self.target_value_text.draw()

            progress = min(self.current_rating / self.target_rating, 1.0)
            progress_width = 290 * progress
            progress_x = self.x - 145 + progress_width / 2

            progress_rect = arcade.XYWH(
                progress_x, self.y - 35, progress_width, 6)
            bar_color = (100, 255, 100) if progress >= 1.0 else (100, 150, 255)
            arcade.draw_rect_filled(progress_rect, bar_color)

            outline_rect = arcade.XYWH(self.x, self.y - 35, 290, 6)
            arcade.draw_rect_outline(outline_rect, TEXT_COLOR, 1)
