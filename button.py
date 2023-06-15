import pygame as pg


class Button:
    def __init__(self, x, y, width, height, screen, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen

        self.button_rect = pg.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

        # display state
        self.display = True

        # default background color
        self.bg_color = pg.Color("#00008b")

        # default text properties (private variables)
        self._text = text
        self._text_color = pg.Color("white")
        self._font = pg.font.SysFont("arial", int(height / 2))

        # border properties
        self.border = True
        self.border_color = pg.Color("white")
        self.border_width = 2

        # click properties
        self.change_on_click = True
        self.left_clicked = False
        self.right_clicked = False
        self.click_color = pg.Color(128, 128, 128)

        # hover properties
        self.change_on_hover = True
        self.is_hovering = False
        self.hover_color = pg.Color("#191970")

        self.init_display_text()

    def inside_rect(self, pos):
        mouse_x, mouse_y = pos
        if mouse_x > self.x - self.width // 2 and mouse_x < self.x + self.width // 2 and mouse_y > self.y - self.height // 2 and mouse_y < self.y + self.height // 2:
            return True
        else:
            return False

    def update(self, mouse_pos):
        if self.display:
            if self.inside_rect(mouse_pos):
                self.is_hovering = True
            else:
                self.is_hovering = False

    def check_clicked(self, mouse_pos, clicks):
        if self.display:
            if self.inside_rect(mouse_pos):
                if clicks == 1:
                    self.left_clicked = True
                elif clicks == 3:
                    self.right_clicked = True

    def check_released(self, mouse_pos, clicks):
        if self.display:
            if self.inside_rect(mouse_pos):
                if clicks == 1:
                    self.left_clicked = False
                elif clicks == 3:
                    self.right_clicked = False

    def set_font(self, font):
        self._font = font
        self.init_display_text()

    def set_text(self, text):
        self._text = text
        self.init_display_text()

    def set_text_color(self, color):
        self._text_color = color
        self.init_display_text()

    def init_display_text(self):
        self.display_text = self._font.render(self._text, True, self._text_color)
        self.text_rect = self.display_text.get_rect(center=(self.x, self.y))

    def render(self):
        if self.display:
            if self.change_on_click and (self.left_clicked or self.right_clicked):
                color = self.click_color
            elif self.change_on_hover and self.is_hovering:
                color = self.hover_color
            else:
                color = self.bg_color

            pg.draw.rect(self.screen, color, self.button_rect)
            if self.border:
                pg.draw.rect(self.screen, self.border_color, self.button_rect, self.border_width)
            self.screen.blit(self.display_text, self.text_rect)
