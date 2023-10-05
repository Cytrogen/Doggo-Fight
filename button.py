"""
file: button.py
author: Cytrogen
"""
import pygame
import inspect


class Button:
    """
    A class to represent a button.
    一个代表按钮的类。

    ...

    Attributes
    ----------
    rect : pygame.Rect
        The rectangle of the button.
        按钮的矩形。
    text : str
        The text on the button.
        按钮上的文本。
    text_color : tuple
        The color of the text on the button.
        按钮上文本的颜色。
    button_color : tuple
        The color of the button.
        按钮的颜色。
    action : function
        The function to call when the button is clicked.
        单击按钮时要调用的函数。
    next_menu : Menu
        The next menu to draw when the button is clicked.
        单击按钮时要绘制的下一个菜单。

    Methods
    -------
    draw(screen)
        Draw the button.
        绘制按钮。
    click(screen, *args, **kwargs)
        Call the action function.
        调用操作函数。
    """
    def __init__(self, x, y, width, height, text, text_color, button_color, action, next_menu=None):
        """
        Initialize the button.
        初始化按钮。
        :param x:
        :param y:
        :param width:
        :param height:
        :param text:
        :param text_color:
        :param button_color:
        :param action:
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.action = action
        self.next_menu = next_menu

    def draw(self, screen) -> None:
        """
        Draw the button.
        绘制按钮。
        :param screen:
        :return:
        """
        # Draw the button
        pygame.draw.rect(screen, self.button_color, self.rect)
        font = pygame.font.Font('font/Fusion Pixel.ttf', 20)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)

    def click(self, screen, *args, **kwargs) -> None:
        """
        Call the action function.
        调用操作函数。
        :param screen:
        :param args:
        :param kwargs:
        :return:
        """
        # Get the arguments of the action function
        # 获取操作函数的参数
        action_args = inspect.signature(self.action).parameters.keys()

        # If the action function has a screen argument, pass the screen to it
        # 如果操作函数有一个屏幕参数，请将屏幕传递给它
        if 'screen' in action_args:
            self.action(screen, *args, **kwargs)
        # Otherwise, just call the action function
        # 否则，只需调用操作函数
        else:
            self.action(*args, **kwargs)
