import pygame

from configs import FONT, COLORS


class InputBox:
    """
    A class to represent an input box.
    一个代表输入框的类。

    ...

    Attributes
    ----------
    box_body : pygame.Rect
        The body of the input box.
        输入框的主体。
    color_inactive : tuple
        The color of the input box when it is inactive.
        输入框处于非活动状态时的颜色。
    color_active : tuple
        The color of the input box when it is active.
        输入框处于活动状态时的颜色。
    color : tuple
        The color of the input box.
        输入框的颜色。
    active : bool
        Whether the input box is active.
        输入框是否处于活动状态。

    Methods
    -------
    handle_event(event)
        Handle the events of the input box.
        处理输入框的事件。
    draw(screen)
        Draw the input box.
        绘制输入框。
    """
    def __init__(self, rect: pygame.Rect = pygame.Rect(275, 200, 250, 32)):
        self.box_body: pygame.Rect = rect
        self.color_inactive = COLORS['light_grey']
        self.color_active = COLORS['dark_grey']
        self.color = self.color_inactive
        self.active = False
        self.text = 'TYPE HERE'
        self.done = False
        self.font = pygame.font.Font(FONT, 24)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle the events of the input box.
        处理输入框的事件。
        :param event:
        :return:
        """
        # If the user clicks on the input box, it is activated.
        # 如果用户点击了输入框，输入框就会变成活动状态。
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box_body.collidepoint(event.pos):
                self.active = not self.active
                if self.text == 'TYPE HERE':
                    self.text = ''
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        # If the user presses a key on the keyboard and the input box is active, then
        # the character of the key is added to the input box.
        # 如果用户按下了键盘上的某个键，且输入框处于活动状态，就将该键的字符添加到输入框中。
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # The maximum number of characters in the input box is 15.
                    # 输入框中的最大字符数为15。
                    if len(self.text) <= 15:
                        self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Draw the input box.
        绘制输入框。
        :param screen:
        :return:
        """
        text_surface = self.font.render(self.text, True, self.color)
        width = max(250, text_surface.get_width() + 10)
        self.box_body.w = width
        screen.blit(text_surface, (self.box_body.x + 5, self.box_body.y + 5))
        pygame.draw.rect(screen, self.color, self.box_body, 2)
