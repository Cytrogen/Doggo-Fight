"""
file: ascii_art.py
author: Cytrogen
"""
import pygame

from configs import FONT, TITLE_SIZE, SUBTITLE_SIZE, CENTER_SIZE, COLORS


ascii_dogs = {
    0: [
        r'    ___',
        r' __/_  `.  .-"""-.',
        r" \_,` | \-'  /   )`-')",
        r'  "") `"`    \  ((`"`',
        r" ___Y  ,    .'7 /|",
        r"(_,___/...-` (_/_/"
    ],
    1: [
        r"       ,",
        r"       |`-.__",
        r"       / ' _/",
        r"      ****` ",
        r"     /    }",
        r"    /  \ /",
        " \ /`   \\\\",
        r" `\    /_\\",
    ],
    2: [
        r'',
        r'',
        r'',
        r'',
        r'       __',
        r"  (___()'`;",
        r"  /,    /`",
        r'  \\"--\\'
    ],
    3: [
        '            /)-_-(\\',
        r"             (o o)",
        r"     .-----__/\o/",
        r"    /  __      /",
        r"\__/\ /  \_\ |/",
        r"     \\     ||",
        r"     //     ||",
        r"     |\     |\\"
    ],
    4: [
        r'',
        r'',
        r'',
        r'',
        r'  __      _',
        r"o'')}____//",
        r' `_/      )',
        r' (_(_/-(_/'
    ],
    5: [
        r'',
        r'',
        r' _   _',
        r'/(. .)\    )',
        r'  (*)____/|',
        r'  /       |',
        r' /   |--\ |',
        r'(_)(_)  (_)'
    ],
    6: [
        r'',
        r'',
        r'',
        r'   __',
        r"o-''|\_____/)",
        r' \_/|_)     )',
        r'    \  __  /',
        r'    (_/ (_/'
    ]
}


def draw_dog(screen, x, y, dog_num, size) -> None:
    """
    Draws the ASCII dog.
    绘制ASCII狗。
    :param screen:
    :param x:
    :param y:
    :param dog_num:
    :param size:
    :return:
    """

    global ascii_dogs

    # Draw the ASCII dog line by line
    # 逐行绘制ASCII狗
    font = pygame.font.Font(FONT, size)
    for line in ascii_dogs[dog_num]:
        line_surface = font.render(line, True, COLORS['black'])
        _, line_height = line_surface.get_size()
        screen.blit(line_surface, (x, y))
        y += line_height


def draw_title(screen, text, text_size, position: str | tuple, side: str) -> None:
    """
    Draws the title based on the position.
    根据位置绘制标题。
    :param screen:
    :param text:
    :param text_size:
    :param position:
    :param side:
    :return:
    """
    font = pygame.font.Font(FONT, text_size)
    text = font.render(text, True, COLORS['black'])
    text_rect = text.get_rect()

    # Determine the position of the title based on the passed parameter. If it is a string, determine
    # the position based on the string; if it is a tuple, use the value of the tuple directly.
    # 根据传参确定标题的位置。如果是字符串，则根据字符串确定位置；如果是元组，则直接使用元组的值。
    position_size = None
    if isinstance(position, str):
        position_size = CENTER_SIZE if position == 'center' \
            else TITLE_SIZE if position == 'title' \
            else SUBTITLE_SIZE
    elif isinstance(position, tuple):
        position_size = position

    # Determine the starting point of the text based on the passed parameter. If it is a string,
    # determine the position based on the string; if it is a tuple, use the value of the tuple
    # directly.
    # 根据传参确定文字的起始点位置。如果是字符串，则根据字符串确定位置；如果是元组，则直接使用元组的值。
    match side:
        case 'left':
            text_rect.topleft = position_size
        case 'center':
            text_rect.center = position_size
        case 'right':
            text_rect.topright = position_size

    screen.blit(text, text_rect)


def draw_health_bar(screen, health, max_health, xy: tuple, is_user: bool) -> None:
    """
    Draws the health bar. The user's health bar will show the health value, while the enemy's
    health bar will show question marks.
    绘制生命条。用户的生命条会显示生命值，而敌人的生命条会显示问号。
    :param screen:
    :param health:
    :param max_health:
    :param xy:
    :param is_user:
    :return:
    """
    x, y = xy

    # Draw the background of the health bar. First draw a black rectangle, then draw a white
    # rectangle, so that we can get a black border and white background rectangle.
    # 绘制生命条的背景。先绘制黑色的矩形，再绘制白色的矩形，这样就可以得到一个黑边白底的矩形。
    pygame.draw.rect(
        surface=screen,
        color=COLORS['black'],
        rect=(x - 2, y - 2, 208, 32),
        width=0
    )
    pygame.draw.rect(
        surface=screen,
        color=COLORS['white'],
        rect=(x, y, 204, 28),
        width=0
    )

    # Draw the health bar.
    # 绘制生命条。
    health_bar_width = int(204 * (health / max_health))
    font = pygame.font.Font(FONT, 26)

    # If it is to draw the user's health bar, then draw a green health bar, otherwise draw a red
    # health bar.
    # 如果是绘制用户的狗的生命条，那么绘制绿色的生命条，否则绘制红色的生命条。
    if is_user:
        pygame.draw.rect(
            surface=screen,
            color=COLORS['green'],
            rect=(x, y, health_bar_width, 28),
            width=0
        )
        text = font.render(f'{health}/{max_health}', True, COLORS['black'])
    else:
        start_x = x + (204 - health_bar_width)
        pygame.draw.rect(
            surface=screen,
            color=COLORS['red'],
            # The enemy's health bar is drawn from right to left, so the starting point of the
            # health bar is the starting point of the background plus the difference between the
            # width of the background and the width of the health bar.
            # 敌人的生命条是从右往左绘制的，所以生命条的起始点是背景的起始点加上背景的宽度和生命条的宽度的差。
            rect=(start_x, y, health_bar_width, 28),
            width=0
        )
        text = font.render('???/???', True, COLORS['black'])

    text_rect = text.get_rect()
    text_rect.center = (x + 102, y + 14)
    screen.blit(text, text_rect)


def draw_charge_bar(screen, charge_level, xy: tuple, is_user: bool) -> None:
    """
    Draws the charge bar. The charge bar is a 10 cell bar, charge_level represents the number
    of cells charged.
    绘制充能条。充能条是一个10格的条，charge_level表示充能的格数。
    :param screen:
    :param charge_level:
    :param xy:
    :param is_user:
    :return:
    """
    x, y = xy

    cell_size = 10
    cell_gap = 2

    # Draw the background of the charge bar, a black border and black background rectangle.
    # 绘制充能条的背景，一个黑边黑底的矩形。
    pygame.draw.rect(
        surface=screen,
        color=COLORS['black'],
        rect=(x - 2, y - 2, cell_size * 10 + cell_gap * 10 + 2, cell_size + cell_gap + 2),
        width=0
    )

    # Draw the charge bar.
    # 绘制充能条。
    if is_user:
        for i in range(charge_level):
            pygame.draw.rect(
                surface=screen,
                color=COLORS['yellow'],
                rect=(x + i * (cell_size + cell_gap), y, cell_size, cell_size),
                width=0
            )
    else:
        start_x = x + (10 - charge_level) * (cell_size + cell_gap)
        for i in range(charge_level):
            pygame.draw.rect(
                surface=screen,
                color=COLORS['yellow'],
                rect=(start_x + i * (cell_size + cell_gap), y, cell_size, cell_size),
                width=0
            )


def draw_damage(screen, damage: int, xy: tuple) -> None:
    """
    Draws the damage value.
    绘制伤害值。
    :param screen:
    :param damage:
    :param xy:
    :return:
    """
    font = pygame.font.Font(FONT, 48)
    text = font.render(f'-{damage}!', True, COLORS['red'])
    text_rect = text.get_rect()
    text_rect.center = xy
    screen.blit(text, text_rect)
