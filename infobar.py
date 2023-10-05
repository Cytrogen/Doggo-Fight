"""
file: infobar.py
author: Cytrogen
"""
import pygame

from configs import COLORS


class InfoBar:
    """
    A class to represent an info bar.
    一个代表信息栏的类。

    ...

    Attributes
    ----------
    screen : pygame.Surface
        The screen to draw the info bar on.
        绘制信息栏的屏幕。
    line_height : int
        The height of each line.
        每行的高度。
    x : int
        The x coordinate of the top left corner of the info bar.
        信息栏左上角的x坐标。
    y : int
        The y coordinate of the top left corner of the info bar.
        信息栏左上角的y坐标。
    width : int
        The width of the info bar.
        信息栏的宽度。
    max_lines : int
        The maximum number of lines in the info bar.
        信息栏中的最大行数。
    font : pygame.font.Font
        The font of the text in the info bar.
        信息栏中文本的字体。
    messages : list
        The messages in the info bar.
        信息栏中的消息。

    Methods
    -------
    add_message(message)
        Add a message to the info bar.
        将消息添加到信息栏中。
    draw()
        Draw the info bar.
        绘制信息栏。
    """
    def __init__(self, screen, line_height, xy: tuple, width):
        self.screen = screen
        self.line_height = line_height
        self.xy = xy
        self.width = width

        self.max_lines = 5
        self.font = pygame.font.Font('font/Fusion Pixel.ttf', 16)
        self.messages = []

    def add_message(self, message) -> None:
        """
        Add a message to the info bar.
        将消息添加到信息栏中。
        :param message:
        :return:
        """
        self.messages.append(message)
        # If the number of lines in the info bar exceeds the maximum number of lines,
        # remove the first line.
        # 如果信息栏中的行数超过最大行数，则删除第一行。
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)

    def draw(self) -> None:
        """
        Draw the info bar.
        绘制信息栏。
        :return:
        """
        x, y = self.xy
        # Draw the black border and white background of the info bar.
        # 绘制信息栏的黑色边框和白色背景。
        pygame.draw.rect(
            surface=self.screen,
            color=COLORS['black'],
            rect=(x - 2, y - 2, self.width + 4, self.line_height * self.max_lines + 4),
            width=0
        )
        pygame.draw.rect(
            surface=self.screen,
            color=COLORS['white'],
            rect=(x, y, self.width, self.line_height * self.max_lines),
            width=0
        )

        # Draw the messages in the info bar.
        # 绘制信息栏中的消息。
        y_offset = 0
        for message in self.messages:
            text = self.font.render(message, True, COLORS['black'])
            text_rect = text.get_rect()
            text_rect.topleft = (x + 2, y + y_offset)
            self.screen.blit(text, text_rect)
            y_offset += self.line_height
